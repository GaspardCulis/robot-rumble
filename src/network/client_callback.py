from asyncio import DatagramTransport

from network.callback import Callback
from network.connection_state import ConnectionState
from network.converter import Address, DataConverter
from objects.player import Player


class ClientCallback(Callback):
    def __init__(self, player: Player):
        self.player = player

    def on_connected(self, transport: DatagramTransport, state: ConnectionState, addr: Address):
        pass

    def welcome_data(self, data: bytes, state: ConnectionState, addr: Address):
        _, unique_id = DataConverter.parse_varint(data)
        print("I am player id :", unique_id)
        self.player.unique_id = unique_id

    def on_disconnect(self, state: ConnectionState, addr: Address):
        pass
