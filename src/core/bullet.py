import pygame
from pygame import Vector2

from core.gravity import PhysicsObject

BULLET_MASS = 5


class Bullet(PhysicsObject):

    def __init__(self, position: Vector2, width: int, height: int):
        super().__init__(BULLET_MASS, position, True, False, width, height)
        self.width = width
        self.height = height
