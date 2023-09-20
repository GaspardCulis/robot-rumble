import pygame
from pygame import Vector2
from pygame.sprite import Group, Sprite
from random import random

from core.gravity import PhysicsObject

BULLET_MASS = 5
BULLET_SPEED = 1000

class Bullet(PhysicsObject, Sprite):
    all: Group = Group()
    def __init__(self, position: Vector2, direction_vector: Vector2):
        super().__init__(BULLET_MASS, position, True, False)

        self.angle = 0
        self.velocity = (direction_vector + Vector2(random()/10, random()/10)) * BULLET_SPEED
        
        self.original_image = pygame.transform.scale_by(pygame.image.load("assets/img/bullet.png"), 2)
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        self.rect = self.image.get_rect(center=self.image.get_rect(center = self.position).center)

        self.all.add(self)

    def kill(self):
        super().kill()
        self.all.remove(self)

    def update(self):
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)

        self.angle = self.velocity.angle_to(Vector2(1, 0))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
