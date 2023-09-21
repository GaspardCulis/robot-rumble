from asyncio import DatagramTransport

from pygame import Vector2, image

from network.callback import Callback
from network.connection_state import ConnectionState
from network.converter import Address, DataBuffer
from objects.player import Player


class ServerCallback(Callback):

    def on_connected(self, transport: DatagramTransport, state: ConnectionState, addr: Address, *args):
        # position is useless, will be instantly updated by client
        new_player = Player(Vector2(9, 30), image.load(
            "assets/img/player.png"))  # A new player just connected, make a new player object
        new_player.remote = True
        print("Player id", new_player.unique_id, "just joined !")
        state.player_id = new_player.unique_id
        state.last_sent_id += 1
        output = DataBuffer()
        output.append_varlong(state.last_sent_id)
        output.append_varint(new_player.unique_id)
        output.append_varlong(args[0])

        transport.sendto(b'\x04' + output.flip().get_data(),
                         addr)  # inform client about the unique id chosen and the seed

    def welcome_data(self, data: bytes, state: ConnectionState, addr: Address):
        pass

    def on_disconnect(self, state: ConnectionState, addr: Address):
        pass
