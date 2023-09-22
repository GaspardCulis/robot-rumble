from asyncio import DatagramTransport

from core import generation
from network.callback import Callback
from network.connection_state import ConnectionState
from network.converter import Address, DataBuffer
from objects.player import Player


class ClientCallback(Callback):
    def __init__(self, player: Player):
        self.player = player

    def on_connected(self, transport: DatagramTransport, state: ConnectionState, addr: Address, *args):
        pass

    def welcome_data(self, data: bytes, state: ConnectionState, addr: Address):
        buffer = DataBuffer(data)
        unique_id = buffer.read_varint()
        print("I am player id :", unique_id)
        self.player.unique_id = unique_id
        seed = buffer.read_varlong()
        print("Server is on seed", seed)
        generation.procedural_generation(seed)

    def on_disconnect(self, state: ConnectionState, addr: Address):
        pass
