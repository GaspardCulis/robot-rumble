import math
from os import path
from time import monotonic
import pygame as pg
from pygame import Surface, Vector2, image, Rect, transform
from pygame.sprite import Sprite, collide_circle, Group
from core.collision import CircleShape, CollisionObject
from core.gravity import PhysicsObject
from core.imageloader import ImageLoader
from core.spritesheets import SpriteSheet

PLANET_ASSETS_PATH = "assets/img/planet"

class Planet(PhysicsObject, Sprite):
    all: Group = Group()
    
    def __init__(self, position: Vector2, radius: float, sprite_name: str):
        self.radius = radius
        mass = math.pi * self.radius**2

        super().__init__(mass=mass, position=position, passive=False, static=True)

        scale_multiplier = 2
        if sprite_name.startswith("star"):
            scale_multiplier *= 2
        elif sprite_name.count("ring") > 0:
            scale_multiplier *= 3

        if sprite_name != "planet69.png":
            self.frames = SpriteSheet(path.join(PLANET_ASSETS_PATH, sprite_name), 8, 25, 0.1, sprite_size=Vector2(self.radius * scale_multiplier))
        else:
            self.frames = SpriteSheet(path.join(PLANET_ASSETS_PATH, sprite_name), 1, 1, 1, sprite_size=Vector2(self.radius * scale_multiplier))

        self.image = self.frames.get_frame()
        self.rect = self.image.get_rect()

        self.all.add(self)

    def kill(self):
        super().kill()
        self.all.remove(self)

    def update(self):
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)

        self.image = self.frames.get_frame()