from asyncio import DatagramTransport

from pygame import Vector2

from core import generation
from network.callback import Callback
from network.connection_state import ConnectionState
from network.converter import Address, DataBuffer, DataConverter
from objects.player import Player


class ClientCallback(Callback):
    def __init__(self, player: Player):
        self.player = player

    def on_connected(self, transport: DatagramTransport, state: ConnectionState, addr: Address, *args):
        state.last_sent_id += 1
        transport.sendto(b'\x03' + DataConverter.write_varlong(state.last_sent_id) + self.player.name.encode("utf-8"), None)

    def welcome_data(self, data: bytes, state: ConnectionState, addr: Address):
        buffer = DataBuffer(data)
        unique_id = buffer.read_varint()
        print("I am player id :", unique_id)
        self.player.unique_id = unique_id
        seed = buffer.read_varlong()
        print("Server is on seed", seed)
        generation.procedural_generation(seed)
        size = buffer.read_varint()
        to_sync = {}
        for _ in range(size):
            uid = buffer.read_varint()
            name = buffer.read_string()
            to_sync[uid] = name
        for p in Player.all:
            p: Player
            if p.unique_id in to_sync:
                p.name = to_sync[p.unique_id]
                del to_sync[p.unique_id]
        for uid, name in to_sync.items():
            p = Player(Vector2(9, 30))
            p.unique_id = uid
            p.name = name
            p.remote = True
            print("Made new player from naming data", p.name)

    def on_disconnect(self, state: ConnectionState, addr: Address):
        pass
