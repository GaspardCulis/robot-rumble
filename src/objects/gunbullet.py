import pygame
from pygame import Vector2
from pygame.sprite import Group, Sprite
from random import random

from core.gravity import PhysicsObject
from objects.bullet import Bullet
from objects.planet import Planet

BULLET_MASS = 5
BULLET_SPEED = 1000

class GunBullet(Bullet):
    def __init__(self, position: Vector2, target: Vector2):
        super().__init__(
            position=position,
            target=target,
            sprite=pygame.transform.scale_by(pygame.image.load("assets/img/bullet.png"), 2),
            damage=5
        )

