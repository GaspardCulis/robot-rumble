from os import path

from pygame import Vector2

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
            output.append_boolean(p.isDead)
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
    valid_ids = set()
    for _ in range(nb_players):  # TODO handle player being disconnected
        pl = read_player(buffer)
        valid_ids.add(pl.unique_id)
        pl.isDead = buffer.read_boolean()
        pl.percentage = buffer.read_float()
        pl.selected_weapon_index = buffer.read_varint()
        pl.weapons[pl.selected_weapon_index].direction = buffer.read_float()
    valid_ids.clear()
    nb_bullets = buffer.read_varlong()

    for _ in range(nb_bullets):
        unique_id = buffer.read_varlong()
        valid_ids.add(unique_id)
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
            bl.to_sync.remove(bl)
            bl.unique_id = unique_id
        else:
            bl.new_position = pos

        if bullet_type == 0x01:
            bl.scale = buffer.read_float()
        bl.velocity = buffer.read_vector_float()
        bl.angle = buffer.read_float()

    b: Bullet
    for b in Bullet.all:
        if b.unique_id not in valid_ids:
            b.kill()  # delete bullet


def update_player() -> bytes | None:
    output = DataBuffer()
    p: Player | None = None
    pl: Player
    for pl in Player.all:
        if not pl.remote:
            p = pl
            break
    if p is None:
        return None
    output.append_varint(p.unique_id)
    output.append_vector_float(p.position)
    output.append_vector_float(p.velocity)
    output.append_float(p.rotation)
    output.append_varint(p.selected_weapon_index)
    output.append_float(p.weapons[p.selected_weapon_index].direction)

    output.append_varlong(len(Bullet.to_sync))
    for b in Bullet.to_sync:
        bullet_type = get_number_from_bullet(b)
        output.append_varint(bullet_type)
        output.append_vector_float(b.position)
        if bullet_type == 0x00:
            b: GunBullet
            output.append_varint(b.owner_id)
        elif bullet_type == 0x01:  # black hole
            b: BlackHole
            output.append_vector_float(b.target)
        output.append_vector_float(b.velocity)
        output.append_float(b.angle)
    Bullet.to_sync.clear()
    return output.flip().get_data()


def apply_player(data: bytes) -> None:
    buffer = DataBuffer(data)
    pl = read_player(buffer)
    weapon_index = buffer.read_varint()
    pl.selected_weapon_index = weapon_index
    pl.weapons[weapon_index].direction = buffer.read_float()
    nb_bullets = buffer.read_varlong()
    for _ in range(nb_bullets):
        bullet_type = buffer.read_varint()
        pos = buffer.read_vector_float()
        args = [pos]
        if bullet_type == 0x00:
            owner_id = buffer.read_varint()
            args.append(Vector2())
            args.append(owner_id)
        elif bullet_type == 0x01:  # black hole
            target = buffer.read_vector_float()
            args.append(target)
        b = make_bullet_from_number(bullet_type, *args)
        b.velocity = buffer.read_vector_float()
        b.angle = buffer.read_float()


def read_player(buffer: DataBuffer) -> Player:
    unique_id = buffer.read_varint()
    pl: Player | None = None
    for p in Player.all:
        if p.unique_id == unique_id:
            pl = p
            break
    pos = buffer.read_vector_float()
    if pl is None:
        pl = Player(pos)
        pl.remote = True
        pl.unique_id = unique_id
    else:
        pl.new_position = pos
    pl.velocity = buffer.read_vector_float()
    pl.rotation = buffer.read_float()
    return pl
