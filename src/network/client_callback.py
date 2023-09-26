from asyncio import DatagramTransport

from pygame import Vector2

from core import generation
from network.callback import Callback
from network.connection_state import ConnectionState
from network.converter import Address, DataBuffer
from objects.player import Player, PLAYER_SPRITESHEETS


class ClientCallback(Callback):
    def __init__(self, player: Player):
        self.player = player

    def on_connected(self, transport: DatagramTransport, state: ConnectionState, addr: Address, *args):
        state.last_sent_id += 1
        buffer = DataBuffer()
        buffer.append(0x03)
        buffer.append_varlong(state.last_sent_id)
        buffer.append_string(self.player.name)
        buffer.append_varint(self.player.avatar_index)
        transport.sendto(buffer.flip().get_data(), None)

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
            avatar = buffer.read_varint()
            to_sync[uid] = name, avatar
        for p in Player.all:
            p: Player
            if p.unique_id in to_sync:
                p.name, avatar = to_sync[p.unique_id]
                p.set_avatar(avatar)
                del to_sync[p.unique_id]
        for uid, (name, avatar) in to_sync.items():
            p = Player(Vector2(9, 30))
            p.unique_id = uid
            p.name = name
            p.set_avatar(avatar)
            p.remote = True
            print("Made new player from naming data", p.name)

    def on_disconnect(self, state: ConnectionState, addr: Address):
        pass
