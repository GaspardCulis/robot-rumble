from pygame import Vector2
from random import random

from objects.bullet import Bullet
from objects.weapon import Weapon


class Shotgun(Weapon):
    def __init__(self) -> None:
        super().__init__(500, 0.0, 1, 2)

        
    def shoot(self, position: Vector2, target: Vector2) -> Vector2:
        if self.can_shoot():
            angle = Vector2(1, 0).angle_to(target - position)
            for a in range(-10, 10):
                bullet = Bullet(position + Vector2(1, 0), angle + a + random() * 4)
            return Vector2(1, 0).rotate(angle) * self.recoil
        return Vector2(0)