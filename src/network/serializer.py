from os import path

from pygame import image, Vector2

from network.converter import DataBuffer
from objects.blackhole import BlackHole
from objects.gunbullet import GunBullet
from objects.player import Player
from objects.bullet import Bullet


def get_number_from_bullet(b: Bullet) -> int:
    match b:
        case GunBullet():
            return 0x00
        case BlackHole():
            return 0x01


def make_bullet_from_number(bullet_type: int, *args) -> Bullet:
    match bullet_type:
        case 0x00:
            return GunBullet(*args)
        case 0x01:
            return BlackHole(*args)


def prepare_update(player_id: int) -> bytes:
    output = DataBuffer()
    # Take up all the players, and save info
    output.append_varint(len(Player.all.sprites()) - 1)
    p: Player
    for p in Player.all:
        if p.unique_id != player_id:
            output.append_varint(p.unique_id)
            output.append_vector_float(p.position)
            output.append_vector_float(p.velocity)
            output.append_float(p.rotation)
            output.append_float(p.percentage)
            output.append_varint(p.selected_weapon_index)
            output.append_float(p.weapons[p.selected_weapon_index].direction)

    # Take all the bullets, and save info
    b: Bullet
    output.append_varlong(len(Bullet.all.sprites()))
    # print("Amount of bullets", len(Bullet.all.sprites()))
    for b in Bullet.all:
        output.append_varlong(b.unique_id)
        bullet_type = get_number_from_bullet(b)
        output.append_varint(bullet_type)
        output.append_vector_float(b.position)
        if bullet_type == 0x00:
            b: GunBullet
            output.append_varint(b.owner_id)
        elif bullet_type == 0x01:  # black hole
            b: BlackHole
            output.append_float(b.scale)
        output.append_vector_float(b.velocity)
        output.append_float(b.angle)
    return output.flip().get_data()


ASSETS_PATH = "assets/"
IMG_PATH = path.join(ASSETS_PATH, "img/")


def apply_update(data: bytes):
    buffer = DataBuffer(data)
    # Load players
    nb_players = buffer.read_varint()
    for _ in range(nb_players):
        pl = read_player(buffer)
        pl.percentage = buffer.read_float()
        pl.selected_weapon_index = buffer.read_varint()
        pl.weapons[pl.selected_weapon_index].direction = buffer.read_float()

    nb_bullets = buffer.read_varlong()

    for _ in range(nb_bullets):
        unique_id = buffer.read_varlong()
        bl = None
        for b in Bullet.all:
            if b.unique_id == unique_id:
                bl = b
                break
        bullet_type = buffer.read_varint()
        pos = buffer.read_vector_float()
        args = [pos, Vector2()]
        if bullet_type == 0x00:
            args.append(buffer.read_varint())  # owner_id

        if bl is None:
            bl = make_bullet_from_number(bullet_type, *args)
            bl.unique_id = unique_id
        else:
            bl.new_position = pos

        if bullet_type == 0x01:
            bl.scale = buffer.read_float()
        bl.velocity = buffer.read_vector_float()
        bl.angle = buffer.read_float()


def update_player() -> bytes:
    output = DataBuffer()
    p: Player = list(Player.all.spritedict.keys())[0]
    output.append_varint(p.unique_id)
    output.append_vector_float(p.position)
    output.append_vector_float(p.velocity)
    output.append_float(p.rotation)
    output.append_varint(p.selected_weapon_index)
    output.append_float(p.weapons[p.selected_weapon_index].direction)
    return output.flip().get_data()  # TODO also transmit info about using weapons (on-click ? track your own bullets ?)


def apply_player(data: bytes) -> None:
    buffer = DataBuffer(data)
    pl = read_player(buffer)
    weapon_index = buffer.read_varint()
    pl.selected_weapon_index = weapon_index
    pl.weapons[weapon_index].direction = buffer.read_float()


def read_player(buffer: DataBuffer) -> Player:
    unique_id = buffer.read_varint()
    pl: Player | None = None
    for p in Player.all:
        if p.unique_id == unique_id:
            pl = p
            break
    pos = buffer.read_vector_float()
    if pl is None:
        pl = Player(pos, image.load(path.join(IMG_PATH, "player.png")))
        pl.remote = True
        pl.unique_id = unique_id
    else:
        pl.new_position = pos
    pl.velocity = buffer.read_vector_float()
    pl.rotation = buffer.read_float()
    return pl
