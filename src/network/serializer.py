from os import path

from pygame import image, Vector2

from network.converter import DataConverter
from objects.player import Player
from objects.bullet import Bullet


def prepare_update() -> bytes:
    output = bytearray()
    # Take up all the players, and save info
    output.extend(DataConverter.write_varint(len(Player.all.sprites())))
    p: Player
    for p in Player.all:
        output.extend(DataConverter.write_varint(p.unique_id))
        output.extend(DataConverter.write_vector_float(p.position))
        output.extend(DataConverter.write_vector_float(p.velocity))
        output.extend(DataConverter.write_float(p.rotation))
        output.extend(DataConverter.write_float(p.percentage))

    # Take all the bullets, and save info
    b: Bullet
    output.extend(DataConverter.write_varlong(len(Bullet.all.sprites())))
    for b in Bullet.all:
        output.extend(DataConverter.write_varlong(b.unique_id))
        output.extend(DataConverter.write_vector_float(b.position))
        output.extend(DataConverter.write_vector_float(b.velocity))
        output.extend(DataConverter.write_float(b.angle))
    return bytes(output)

ASSETS_PATH="assets/"
IMG_PATH=path.join(ASSETS_PATH, "img/")

def apply_update(data: bytes):
    # Load players
    skipped, nb_players = DataConverter.parse_varint(data)
    data = data[skipped:]
    for _ in range(nb_players):
        skipped, unique_id = DataConverter.parse_varint(data)
        pl = None
        for p in Player.all:
            if p.unique_id == unique_id:
                pl = p
        data = data[skipped:]
        pos = DataConverter.parse_vector_float(data)
        if pl is None:
            pl = Player(pos, image.load(path.join(IMG_PATH, "player.png")))
        else:
            pl.position = pos
        data = data[16:]
        pl.velocity = DataConverter.parse_vector_float(data)
        data = data[16:]
        pl.rotation = DataConverter.parse_float(data)
        data = data[8:]
        pl.percentage = DataConverter.parse_float(data)
        data = data[8:]

    skipped, nb_bullets = DataConverter.parse_varlong(data)
    data = data[skipped:]
    for _ in range(nb_bullets):
        skipped, unique_id = DataConverter.parse_varint(data)
        bl = None
        for p in Bullet.all:
            if p.unique_id == unique_id:
                bl = p
        data = data[skipped:]
        pos = DataConverter.parse_vector_float(data)
        if bl is None:
            bl = Bullet(pos, Vector2())
        else:
            bl.position = pos
        data = data[16:]
        bl.velocity = DataConverter.parse_vector_float(data)
        data = data[16:]
        bl.angle = DataConverter.parse_float(data)
        data = data[8:]
