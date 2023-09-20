from pygame import Vector2
from random import random

from objects.bullet import Bullet
from objects.weapon import Weapon


class Shotgun(Weapon):
    def __init__(self) -> None:
        super().__init__(500, 0.0, 1, 2)

        
    def shoot(self, position: Vector2, target: Vector2) -> Vector2:
        if self.can_shoot():
            direction = (target - position).normalize()
            for a in range(-10, 10):
                bullet = Bullet(position + Vector2(1, 0), direction)
            return direction * self.recoil
        return Vector2(0)