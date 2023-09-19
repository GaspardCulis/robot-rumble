import pygame
from pygame import Vector2
from pygame.sprite import Group, Sprite

from core.gravity import PhysicsObject

BULLET_MASS = 5


class Bullet(PhysicsObject, Sprite):
    all: Group = Group()
    def __init__(self, position: Vector2):
        super().__init__(BULLET_MASS, position, True, False)

        self.image = pygame.transform.scale_by(pygame.image.load("assets/img/bullet.png"), 2)

        self.rect = self.image.get_rect(center=self.image.get_rect(center = self.position).center)

        self.all.add(self)

    def kill(self):
        super().kill()
        self.all.remove(self)

    def update(self):
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)
