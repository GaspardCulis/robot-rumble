import asyncio
from time import monotonic

from network import serializer
from network.connection_state import ConnectionState
from network.converter import DataConverter, Address
from network.callback import Callback


async def open_server(callback: Callback, port: int = 25565):
    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ServerProtocol(callback),
        local_addr=("0.0.0.0", port))

    return protocol


class ServerProtocol(asyncio.DatagramProtocol):
    transport: asyncio.DatagramTransport
    callback: Callback
    clients: dict[Address, ConnectionState]

    def __init__(self, callback: Callback):
        self.clients = {}
        self.callback = callback

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Address) -> None:
        if addr not in self.clients:
            self.clients[addr] = ConnectionState(addr)
            self.clients[addr].keepalive_task = asyncio.create_task(self.keep_alive(addr))
        state: ConnectionState = self.clients[addr]
        asyncio.ensure_future(self.handle_client_data(data, state))  # go handle packet

    async def keep_alive(self, addr: Address):
        while True:
            await asyncio.sleep(2)
            self.transport.sendto(b'\x00', addr)

    async def send_update_data(self):
        old_time = monotonic()
        while True:
            # serialize all the data to send
            data = serializer.prepare_update()
            # send the data (this does not block)
            for c, state in self.clients.items():
                state.last_sent_id += 1
                self.transport.sendto(b'\x05' + DataConverter.write_varlong(state.last_sent_id) + data, c)
            # calculate time taken and sleep if needed
            new_time = monotonic()
            delta = new_time - old_time
            old_time = new_time
            await asyncio.sleep(1 / 60 - delta)  # 60 tps target, if time to sleep is negative it skips

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
        if state.last_received_id < last_id:
            state.last_received_id = last_id
            match packet_id:
                case 0x00:
                    pass  # KeepAlive NO-OP !
                case 0x02:
                    timeout = 2
                    self.transport.sendto(b'\x02', state.addr)
                case 0x03:
                    state.connected = True
                    self.callback.on_connected(state.addr)
                case 0x04:
                    pass  # TODO parse data from client
                case _:
                    print("Warning ! got an unknown packet !")

        async def cancel_for_timeout():
            await asyncio.sleep(timeout)
            state.connected = False
            if state.keepalive_task is not None:
                state.keepalive_task.cancel()
            self.callback.on_disconnect(state.addr)
            self.clients.pop(state.addr)

        state.timeout_task = asyncio.create_task(cancel_for_timeout())
