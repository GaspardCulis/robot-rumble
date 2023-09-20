import asyncio
import hashlib
from typing import Any

from network.connection_state import ConnectionState
from network.converter import DataConverter


async def connect_to_server(ip: str = "127.0.0.1", port: int = 25565):
    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ClientProtocol(),
        remote_addr=(ip, port))


class ClientProtocol(asyncio.DatagramProtocol):
    transport: asyncio.DatagramTransport
    state: ConnectionState | None

    def __init__(self):
        self.clients = {}
        self.state = None

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
        if self.state is None:
            self.state = ConnectionState(addr)
        else:
            state: ConnectionState = self.state
            asyncio.ensure_future(self.handle_server_data(data, state))  # go handle packet

    async def handle_server_data(self, data: bytes, state: ConnectionState):
        skip, packet_id = DataConverter.parse_varint(data)
        data = data[skip:]
        skip, last_id = DataConverter.parse_varlong(data)
        data = data[skip:]
        if state.last_recieved_id < last_id:
            state.last_recieved_id = last_id
            match packet_id:
                case 0x00:
                    pass  # KeepAlive NO-OP !
                case 0x01:
                    sha1 = hashlib.sha1()
                    sha1.update(data + "FB44FDEC-978A-406A-8E52-40EF2B2DFB46".encode("utf-8"))
                    state.last_recieved_id += 1  # Would prefer an atomic variable but GIL should ensure this works ?
                    self.transport.sendto(b'\x02' + bytes([state.last_recieved_id]) + sha1.digest(), state.addr)
                case 0x05:
                    pass  # TODO parse data from server
                case _:
                    print("Warning ! got an unknown packet !")