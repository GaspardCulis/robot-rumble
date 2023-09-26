from asyncio import DatagramTransport

from pygame import Vector2

from network.callback import Callback
from network.connection_state import ConnectionState
from network.converter import Address, DataBuffer
from network.server import ServerProtocol
from objects.player import Player, PLAYER_SPRITESHEETS


class ServerCallback(Callback):

    def __init__(self):
        self.protocol = None

    def set_protocol(self, protocol: ServerProtocol):
        self.protocol = protocol

    def on_connected(self, transport: DatagramTransport, state: ConnectionState, addr: Address, *args):
        new_player = Player(Vector2(9, 30))  # A new player just connected, make a new player object
        new_player.remote = True
        # Spawn player, will be updated by client
        new_player.respawn_on_random_planet()
        # Rotate player, same
        new_player.update(60)
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
                to_send.append((p.unique_id, p.name, p.avatar_index))
        print("Sending name info", to_send)
        output.append_varint(len(to_send))
        for uid, name, avatar in to_send:
            output.append_varint(uid)
            output.append_string(name)
            output.append_varint(avatar)

        transport.sendto(output.flip().get_data(),
                         addr)  # inform client about the unique id chosen and the seed

    def welcome_data(self, data: bytes, state: ConnectionState, addr: Address):
        buffer = DataBuffer(data)
        name = buffer.read_string()
        sprite = buffer.read_varint()
        p: Player
        for p in Player.all:
            if p.unique_id == state.player_id:
                p.name = name
                if len(PLAYER_SPRITESHEETS) > sprite:
                    p.set_avatar(sprite)
                break

        output = DataBuffer()
        output.append_varint(state.player_id)
        output.append_string(name)
        output.append_varint(sprite)
        self.protocol.broadcast(0x08, output.flip().get_data())

    def on_disconnect(self, state: ConnectionState, addr: Address):
        for p in Player.all:
            p: Player
            if p.unique_id == state.player_id:
                super(Player, p).kill()  # do not call .kill() directly, would just remove a life
                p.isDead = True  # just in case it's used somewhere else
                Player.all.remove(p)
                break
