from time import monotonic
from pygame import Vector2
import pygame as pg
from pygame.sprite import Group, Sprite
from core.gravity import PhysicsObject
from core.spritesheets import parse_spritesheet

BLACK_HOLE_MASS = 100000
BLACK_HOLE_SPEED = 300
BLACK_HOLE_SPRITESHEET = "assets/img/black_hole.png"

class BlackHole(PhysicsObject, Sprite):
    all: Group = Group()
    def __init__(self, position: Vector2, target: Vector2):
        super().__init__(0, position, False, True)

        self.origin = position + Vector2(0)

        self.velocity = (target - position).normalize() * BLACK_HOLE_SPEED
        
        self.scale = 0.4
        self.frames = parse_spritesheet(pg.image.load(BLACK_HOLE_SPRITESHEET), 2, 25)
        self.frame_index = 0
        self.last_frame_skip = monotonic()
        
        self.image = pg.transform.scale_by(self.frames[self.frame_index], self.scale)
        self.rect = self.image.get_rect(center=self.image.get_rect(center = self.position).center)

        self.target = target
        self.at_target = False

        self.all.add(self)

    def update(self, delta) -> None:
        self.position += self.velocity * delta
        
        if not self.at_target:
            if (self.origin - self.position).length() >= (self.origin - self.target).length() :
                self.at_target = True
                self.velocity = Vector2(0)
        elif self.scale < 2:
            self.scale += delta
            self.mass = BLACK_HOLE_MASS * (self.scale - 0.4)/1.6

        if monotonic() - self.last_frame_skip > 0.05:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_frame_skip = monotonic()
        
        self.image = pg.transform.scale_by(self.frames[self.frame_index], self.scale)
        self.rect = self.image.get_rect(center=self.image.get_rect(center = self.position).center)
        
