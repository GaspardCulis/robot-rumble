import pygame
from pygame import Surface, Vector2
from pygame.sprite import Group, Sprite
from random import random

from core.gravity import PhysicsObject
from objects.planet import Planet

BULLET_MASS = 5
BULLET_SPEED = 1000

class Bullet(PhysicsObject, Sprite):
    all: Group = Group()
    to_sync: list['Bullet'] = []
    is_server: bool = False
    max_id: list[int] = [0]

    def __init__(self, position: Vector2, target: Vector2, sprite: Surface | None, damage: float, spread: float = 0.1, speed: float = BULLET_SPEED):
        super().__init__(BULLET_MASS, position, True, False)

        self.damage = damage
        self.spread = spread
        self.speed = speed
        self.angle = 0
        self.direction_vector = (target - position).normalize()
        self.velocity = (self.direction_vector + Vector2(random()*self.spread, random()*self.spread)) * self.speed

        if sprite:
            self.original_image = sprite
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.image.get_rect(center = self.position).center)

        self.unique_id = self.max_id[0]
        self.max_id[0] += 1
        if not Bullet.is_server:
            Bullet.to_sync.append(self)
        Bullet.all.add(self)

    def kill(self):
        super().kill()
        Bullet.all.remove(self)

    def update(self, delta: float):
        if self.velocity != Vector2(0, 0):
            self.angle = self.velocity.angle_to(Vector2(1, 0))
        if self.image:
            self.rect = self.image.get_rect(center=self.image.get_rect(center = self.position).center)
            self.image = pygame.transform.rotate(self.original_image, self.angle)

        if random() > 0.5: # Don't need to check collisions on every frame
            self.process_collisions()

    def process_collisions(self):
        for planet in Planet.all:
            if pygame.sprite.collide_circle(self, planet):
                self.kill()
                return
