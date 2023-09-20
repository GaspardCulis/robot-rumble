import asyncio
from typing import Any

from network import serializer
from network.callback import Callback
from network.connection_state import ConnectionState
from network.converter import DataConverter, Address


async def connect_to_server(callback: Callback, ip: str = "127.0.0.1", port: int = 25565):
    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ClientProtocol(callback),
        remote_addr=(ip, port))
    return protocol


class ClientProtocol(asyncio.DatagramProtocol):
    transport: asyncio.DatagramTransport
    callback: Callback
    state: ConnectionState | None

    def __init__(self, callback: Callback):
        self.clients = {}
        self.state = None
        self.callback = callback

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
        if self.state is None:
            self.state = ConnectionState(addr)
        else:
            state: ConnectionState = self.state
            asyncio.ensure_future(self.handle_server_data(data, state))  # go handle packet

    def update_current_state(self, data: bytes):
        serializer.apply_update(data)

    async def keep_alive(self, addr: Address):
        while True:
            await asyncio.sleep(2)
            self.transport.sendto(b'\x00', addr)

    async def handle_server_data(self, data: bytes, state: ConnectionState):
        if state.timeout_task is not None:
            if state.timeout_task.done():
                pass  # TODO server has timed out ? do something specific ?
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
                case 0x01:
                    self.state.connected = True
                case 0x05:
                    self.update_current_state(data)
                case _:
                    print("Warning ! got an unknown packet !")

        async def cancel_for_timeout():
            await asyncio.sleep(timeout)
            state.connected = False
            if state.keepalive_task is not None:
                state.keepalive_task.cancel()
            self.callback.on_disconnect(state.addr)

        state.timeout_task = asyncio.create_task(cancel_for_timeout())
