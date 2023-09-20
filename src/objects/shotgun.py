from pygame import Vector2
from random import random

from pygame.sprite import Sprite

from objects.gunbullet import GunBullet
from objects.weapon import Weapon


class Shotgun(Weapon):
    def __init__(self, owner) -> None:
        super().__init__(owner, 500, 0.0, 1, 2, "shotgun.png")
        
    def shoot(self, position: Vector2, target: Vector2) -> Vector2:
        if self.can_shoot():
            direction = (target - position).normalize()
            for a in range(-10, 10):
                bullet = GunBullet(self.get_bullet_spawnpoint(), target)
            return direction * self.recoil
        return Vector2(0)