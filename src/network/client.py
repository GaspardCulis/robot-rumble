import asyncio
from asyncio import DatagramTransport
from typing import Any

from network import serializer
from network.callback import Callback
from network.connection_state import ConnectionState
from network.converter import DataConverter, Address


async def connect_to_server(callback: Callback, ip: str = "127.0.0.1", port: int = 25565) -> DatagramTransport:
    loop = asyncio.get_running_loop()
    loop.set_debug(True)
    transport: DatagramTransport
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ClientProtocol(callback, (ip, port)),
        remote_addr=(ip, port))
    transport.sendto(b'\x01' + DataConverter.write_varint(0), None)
    return transport


class ClientProtocol(asyncio.DatagramProtocol):
    transport: asyncio.DatagramTransport
    callback: Callback
    state: ConnectionState | None

    def __init__(self, callback: Callback, addr: Address):
        self.state = None
        self.callback = callback
        self.addr = addr

    def connection_made(self, transport: asyncio.DatagramTransport):
        print("client started")
        self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
        if self.state is None:
            print("Connected to server")
            self.state = ConnectionState(addr)
            self.state.keepalive_task = asyncio.create_task(self.keep_alive())
        state: ConnectionState = self.state
        asyncio.ensure_future(self.handle_server_data(data, state))  # go handle packet

    def connection_lost(self, exc: Exception | None) -> None:
        if self.state is None:
            return  # never connected nothing to clean up
        self.state.connected = False
        if self.state.keepalive_task is not None:
            self.state.keepalive_task.cancel()
        if self.state.timeout_task is not None:
            self.state.timeout_task.cancel()
        self.callback.on_disconnect(self.state.addr)  # TODO send to the server that the client is closing

    def update_current_state(self, data: bytes):
        serializer.apply_update(data)

    async def keep_alive(self):
        while True:
            await asyncio.sleep(2)
            self.state.last_sent_id += 1
            self.transport.sendto(b'\x00' + DataConverter.write_varlong(self.state.last_sent_id), None)

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
        # print("CLIENT: got packet id :", packet_id, "last id :", last_id, "data :", data)
        if state.last_received_id < last_id:
            state.last_received_id = last_id
            match packet_id:
                case 0x00:
                    pass  # KeepAlive NO-OP !
                case 0x02:
                    print("Got Second packet, sending last confirmation")
                    self.state.connected = True
                    self.state.last_sent_id += 1
                    self.transport.sendto(b'\x03' + DataConverter.write_varlong(self.state.last_sent_id), None)
                case 0x03:
                    print("")
                case 0x05:
                    self.update_current_state(data)
                case _:
                    print("Warning ! got an unknown packet !")

        async def cancel_for_timeout():
            await asyncio.sleep(timeout)
            self.transport.close()

        state.timeout_task = asyncio.create_task(cancel_for_timeout())
