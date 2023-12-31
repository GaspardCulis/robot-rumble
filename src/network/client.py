import asyncio
from asyncio import DatagramTransport, Task
from time import perf_counter
from typing import Any

from network import serializer
from network.callback import Callback
from network.connection_state import ConnectionState
from network.converter import DataConverter, Address, TICK_RATE, DataBuffer
from objects.player import Player, PLAYER_SPRITESHEETS


async def connect_to_server(callback: Callback, ip: str = "127.0.0.1", port: int = 25565) -> tuple[
    DatagramTransport, 'ClientProtocol']:
    loop = asyncio.get_running_loop()
    transport: DatagramTransport
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ClientProtocol(callback, (ip, port)),
        remote_addr=(ip, port))
    transport.sendto(b'\x01' + DataConverter.write_varint(0), None)
    return transport, protocol


class ClientProtocol(asyncio.DatagramProtocol):
    update_task: Task[None] | None
    transport: asyncio.DatagramTransport
    callback: Callback
    state: ConnectionState | None
    on_connected: asyncio.Event

    def __init__(self, callback: Callback, addr: Address):
        self.update_task = None
        self.state = None
        self.callback = callback
        self.addr = addr
        self.on_connected = asyncio.Event()

    def connection_made(self, transport: asyncio.DatagramTransport):
        print("client started")
        self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
        if self.state is None:
            print("Connected to server")
            self.state = ConnectionState(addr)
            self.state.keepalive_task = asyncio.create_task(self.keep_alive())
            self.update_task = asyncio.create_task(self.send_update_data())
        state: ConnectionState = self.state
        asyncio.ensure_future(self.handle_server_data(data, state))  # go handle packet

    def connection_lost(self, exc: Exception | None) -> None:
        if self.update_task is not None:
            self.update_task.cancel()
        if self.state is None:
            return  # never connected nothing to clean up
        self.state.connected = False
        if self.state.keepalive_task is not None:
            self.state.keepalive_task.cancel()
        if self.state.timeout_task is not None:
            if self.state.timeout_task.done():
                print("Disconnected from server")
            self.state.timeout_task.cancel()
        self.callback.on_disconnect(self.state, self.state.addr)  # TODO send to the server that the client is closing

    async def send_update_data(self):
        while True:
            old_time = perf_counter()
            # serialize all the data to send
            data = serializer.update_player()
            # send the data (this does not block)
            if data is not None:
                self.state.last_sent_id += 1
                self.transport.sendto(b'\x05' + DataConverter.write_varlong(self.state.last_sent_id) + data, None)
            # calculate time taken and sleep if needed
            new_time = perf_counter()
            delta = new_time - old_time
            await asyncio.sleep(1 / TICK_RATE - delta)  # tps target, if time to sleep is negative it skips

    def update_current_state(self, data: bytes):
        serializer.apply_update(data)

    async def keep_alive(self):
        while True:
            await asyncio.sleep(2)
            self.state.last_sent_id += 1
            self.transport.sendto(b'\x00' + DataConverter.write_varlong(self.state.last_sent_id), None)

    async def handle_server_data(self, data: bytes, state: ConnectionState):
        if state.timeout_task is not None:
            state.timeout_task.cancel()
        skip, packet_id = DataConverter.parse_varint(data)
        data = data[skip:]
        skip, last_id = DataConverter.parse_varlong(data)
        data = data[skip:]
        timeout = 10
        # print("CLIENT: got packet id :", packet_id, "last id :", last_id, "data :", data)
        if state.last_received_id < last_id:
            state.last_received_id = last_id
            match packet_id:
                case 0x00:
                    pass  # KeepAlive NO-OP !
                case 0x02:
                    print("Got Second packet, sending last confirmation")
                    self.callback.on_connected(self.transport, state, state.addr)
                case 0x04:
                    self.callback.welcome_data(data, state, state.addr)
                    self.state.connected = True
                    self.on_connected.set()
                case 0x06:
                    if self.state.connected:
                        self.update_current_state(data)
                case 0x08:
                    buffer = DataBuffer(data)
                    p_id = buffer.read_varint()
                    name = buffer.read_string()
                    avatar = buffer.read_varint()
                    print("Got player name", name, "for id", p_id)
                    p: Player  # New player just joined ! ! !
                    for p in Player.all:
                        if p.unique_id == p_id:
                            p.name = name
                            p.set_avatar(avatar)
                            break
                case _:
                    print("Warning ! got an unknown packet ! with id", packet_id, "and data", data)
        else:
            print("Dropping out of order packet id", packet_id)
            if packet_id != 0x06:
                print("Data is", data, "state is", last_id, "wanted", state.last_received_id + 1)

        async def cancel_for_timeout():
            await asyncio.sleep(timeout)
            self.transport.close()

        state.timeout_task = asyncio.create_task(cancel_for_timeout())
