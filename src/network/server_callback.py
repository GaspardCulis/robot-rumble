from asyncio import DatagramTransport

from pygame import Vector2

from network.callback import Callback
from network.connection_state import ConnectionState
from network.converter import Address, DataBuffer
from network.server import ServerProtocol
from objects.player import Player


class ServerCallback(Callback):

    def __init__(self):
        self.protocol = None

    def set_protocol(self, protocol: ServerProtocol):
        self.protocol = protocol

    def on_connected(self, transport: DatagramTransport, state: ConnectionState, addr: Address, *args):
        # position is useless, will be instantly updated by client
        new_player = Player(Vector2(9, 30))  # A new player just connected, make a new player object
        new_player.remote = True
        print("Player id", new_player.unique_id, "just joined !")
        state.player_id = new_player.unique_id
        state.last_sent_id += 1
        output = DataBuffer()
        output.append_varint(0x04)
        output.append_varlong(state.last_sent_id)
        output.append_varint(new_player.unique_id)
        output.append_varlong(args[0])
        # inform the client of all of the known player names (empty = not known)
        to_send = []
        for p in Player.all:
            p: Player
            if p.name != "":
                to_send.append((p.unique_id, p.name))
        print("Sending name info", to_send)
        output.append_varint(len(to_send))
        for uid, name in to_send:
            output.append_varint(uid)
            output.append_string(name)

        transport.sendto(output.flip().get_data(),
                         addr)  # inform client about the unique id chosen and the seed

    def welcome_data(self, data: bytes, state: ConnectionState, addr: Address):
        p: Player
        name = ""
        for p in Player.all:
            if p.unique_id == state.player_id:
                p.name = name = data.decode("utf-8")
                break

        buffer = DataBuffer()
        buffer.append_varint(state.player_id)
        buffer.append_string(name)
        self.protocol.broadcast(0x08, buffer.flip().get_data())

    def on_disconnect(self, state: ConnectionState, addr: Address):
        for p in Player.all:
            p: Player
            if p.unique_id == state.player_id:
                super(Player, p).kill()  # do not call .kill() directly, would just remove a life
                p.isDead = True  # just in case it's used somewhere else
                Player.all.remove(p)
                break
