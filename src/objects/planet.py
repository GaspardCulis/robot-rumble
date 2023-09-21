import math
from os import path
from time import monotonic
import pygame as pg
from pygame import Surface, Vector2, image, Rect, transform
from pygame.sprite import Sprite, collide_circle, Group
from core.collision import CircleShape, CollisionObject
from core.gravity import PhysicsObject
from core.spritesheets import parse_spritesheet

PLANET_ASSETS_PATH = "assets/img/planet"

class Planet(PhysicsObject, Sprite):
    all: Group = Group()
    
    def __init__(self, position: Vector2, radius: float, sprite_name: str):
        self.radius = radius
        mass = math.pi * self.radius**2

        super().__init__(mass=mass, position=position, passive=False, static=True)

        self.frames = list(map(
            lambda x: transform.scale(x, Vector2(self.radius * 2)),
            parse_spritesheet(
                pg.image.load(
                    path.join(PLANET_ASSETS_PATH, sprite_name)
                ).convert_alpha(),
                8, 25
            )
        ))
        self.frame_index = 0
        self.last_frame_skip = monotonic()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

        self.all.add(self)

    def kill(self):
        super().kill()
        self.all.remove(self)

    def update(self):
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)

        if monotonic() - self.last_frame_skip > 0.1:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.last_frame_skip = monotonic()
