import asyncio
from asyncio import Task, DatagramTransport
from time import monotonic

from network import serializer
from network.connection_state import ConnectionState
from network.converter import DataConverter, Address, TICK_RATE, DataBuffer
from network.callback import Callback


async def open_server(callback: Callback, port: int = 25565) -> tuple[DatagramTransport, 'ServerProtocol']:
    loop = asyncio.get_running_loop()
    transport: DatagramTransport
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ServerProtocol(callback),
        local_addr=("0.0.0.0", port))
    return transport, protocol


class ServerProtocol(asyncio.DatagramProtocol):
    update_task: Task[None] | None
    transport: asyncio.DatagramTransport
    callback: Callback
    clients: dict[Address, ConnectionState]
    server_seed: int

    def __init__(self, callback: Callback):
        self.update_task = None
        self.clients = {}
        self.callback = callback
        self.server_seed = -1

    def connection_made(self, transport: asyncio.DatagramTransport):
        print("server started")
        self.transport = transport
        self.update_task = asyncio.create_task(self.send_update_data())

    def datagram_received(self, data: bytes, addr: Address) -> None:
        if addr not in self.clients:
            self.clients[addr] = ConnectionState(addr)
            self.clients[addr].keepalive_task = asyncio.create_task(self.keep_alive(addr))
        state: ConnectionState = self.clients[addr]
        asyncio.ensure_future(self.handle_client_data(data, state))  # go handle packet

    def connection_lost(self, exc: Exception | None) -> None:
        if self.update_task is not None:
            self.update_task.cancel()
        for state in self.clients.values():
            state.connected = False
            if state.keepalive_task is not None:
                state.keepalive_task.cancel()
            if state.timeout_task is not None:
                state.timeout_task.cancel()
            self.callback.on_disconnect(state, state.addr)  # TODO send to the clients that server is closing

    def update_player(self, data):
        serializer.apply_player(data)

    async def keep_alive(self, addr: Address):
        while True:
            await asyncio.sleep(2)
            self.clients[addr].last_sent_id += 1
            self.transport.sendto(b'\x00' + DataBuffer().append_varlong(self.clients[addr].last_sent_id).flip().get_data(), addr)

    async def send_update_data(self):
        while True:
            old_time = monotonic()
            # send the data (this does not block)
            for c, state in self.clients.items():
                # serialize all the data to send, different client needs their own player's data taken out
                data = serializer.prepare_update(state.player_id)
                state.last_sent_id += 1
                self.transport.sendto(b'\x06' + DataConverter.write_varlong(state.last_sent_id) + data, c)
            # calculate time taken and sleep if needed
            new_time = monotonic()
            delta = new_time - old_time
            await asyncio.sleep(1 / TICK_RATE - delta)  # tps target, if time to sleep is negative it skips

    async def handle_client_data(self, data: bytes, state: ConnectionState):
        if state.timeout_task is not None:
            if state.timeout_task.done():
                pass  # TODO client has timed out ? do something specific ?
            state.timeout_task.cancel()
        skip, packet_id = DataConverter.parse_varint(data)
        data = data[skip:]
        skip, last_id = DataConverter.parse_varlong(data)
        data = data[skip:]
        timeout = 10
        # print("SERVER: got packet id :", packet_id, "last id :", last_id, "data :", data)
        if state.last_received_id < last_id:
            state.last_received_id = last_id
            match packet_id:
                case 0x00:
                    pass  # KeepAlive NO-OP !
                case 0x01:
                    print("Client starting connection, sending second packet...")
                    timeout = 2
                    state.last_sent_id += 1
                    self.transport.sendto(b'\x02' + DataConverter.write_varlong(state.last_sent_id), state.addr)
                case 0x03:
                    print("Client connected !")
                    state.connected = True
                    self.callback.on_connected(self.transport, state, state.addr, self.server_seed)
                    self.callback.welcome_data(data, state, state.addr)
                case 0x05:
                    self.update_player(data)
                case _:
                    print("Warning ! got an unknown packet !")
        else:
            print("Dropping out of order packet id", packet_id)

        async def cancel_for_timeout():
            await asyncio.sleep(timeout)
            state.connected = False
            if state.keepalive_task is not None:
                state.keepalive_task.cancel()
            self.callback.on_disconnect(state, state.addr)
            self.clients.pop(state.addr)

        state.timeout_task = asyncio.create_task(cancel_for_timeout())
