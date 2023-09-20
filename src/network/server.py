import asyncio
import hashlib
from typing import Any

from network.connection_state import ConnectionState
from network.converter import DataConverter


async def wait_for_clients(port: int = 25565):
    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ServerProtocol(),
        local_addr=("0.0.0.0", port))


class ServerProtocol(asyncio.DatagramProtocol):
    transport: asyncio.DatagramTransport
    clients: dict[tuple[str | Any, int], ConnectionState]

    def __init__(self):
        self.clients = {}

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
        if addr not in self.clients:
            self.clients[addr] = ConnectionState(addr)
        else:
            state: ConnectionState = self.clients[addr]
            asyncio.ensure_future(self.handle_client_data(data, state))  # go handle packet

    async def handle_client_data(self, data: bytes, state: ConnectionState):
        skip, packet_id = DataConverter.parse_varint(data)
        data = data[skip:]
        skip, last_id = DataConverter.parse_varlong(data)
        data = data[skip:]
        if state.last_recieved_id < last_id:
            state.last_recieved_id = last_id
            match packet_id:
                case 0x00:
                    pass  # KeepAlive NO-OP !
                case 0x02:
                    sha1 = hashlib.sha1()
                    sha1.update(data + "FB44FDEC-978A-406A-8E52-40EF2B2DFB46".encode("utf-8"))
                    state.last_recieved_id += 1  # Would prefer an atomic variable but GIL should ensure this works ?
                    self.transport.sendto(b'\x02' + bytes([state.last_recieved_id]) + sha1.digest(), state.addr)
                    state.connected = True
                case 0x04:
                    pass  # TODO parse data from client
                case _:
                    print("Warning ! got an unknown packet !")
