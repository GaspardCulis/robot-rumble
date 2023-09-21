from time import monotonic
from pygame import Vector2
import pygame as pg
from pygame.sprite import Group
from core.spritesheets import SpriteSheet
from objects.bullet import Bullet
from core.sound import Sound

BLACK_HOLE_MASS = 100000
BLACK_HOLE_SPEED = 1000
BLACK_HOLE_SPRITESHEET = "assets/img/black_hole.png"

class BlackHole(Bullet):
    all: Group = Group()
    snd_name: str = 'black_hole'

    def __init__(self, position: Vector2, target: Vector2):
        super().__init__(
            position=position,
            target=target,
            sprite=None,
            damage=0,
            spread=0,
            speed=BLACK_HOLE_SPEED
        )

        self.static = True
        self.passive = False

        self.origin = position + Vector2(0)

        self.scale = 0.4
        self.frames = SpriteSheet(BLACK_HOLE_SPRITESHEET, 2, 25, 0.05)

        self.image = pg.transform.scale_by(self.frames.get_frame(), self.scale)
        self.rect = self.image.get_rect(center=self.image.get_rect(center = self.position).center)
        self.radius = self.rect.height/2
        self.is_active = False
        self.spawn_time = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
        self.target = target
        self.at_target = False
        Sound.get().loop_sound_in_channel(BlackHole.snd_name)

        BlackHole.all.add(self)

    def kill(self):
            super().kill()
            BlackHole.all.remove(self)
            if not bool(BlackHole.all):
                Sound.get().stop_channel(BlackHole.snd_name)

    def update(self, delta) -> None:
        self.position += self.velocity * delta

        if not self.at_target:
            if (self.origin - self.position).length() >= (self.origin - self.target).length() :
                self.at_target = True
                self.velocity = Vector2(0)
        elif self.scale < 2 and not self.is_active:
            self.scale = min(delta*2 + self.scale, 2)
            if self.scale == 2:
                self.is_active = True
                self.spawn_time = monotonic()
        elif monotonic() - self.spawn_time >= 10:
            self.scale = max(self.scale - delta, 0)
            if self.scale <= 0:
                self.kill()
        self.mass = BLACK_HOLE_MASS * (self.scale - 0.4)/1.6  # scale might be updated in network

        self.image = pg.transform.scale_by(self.frames.get_frame(), self.scale)

        self.original_image = self.image
        super().update(delta)

        self.rect = self.image.get_rect(center=self.position)

