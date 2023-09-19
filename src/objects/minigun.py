from pygame import Vector2

from objects.bullet import Bullet
from core.gravity import PhysicsObject
from objects.weapon import Weapon

class Minigun(Weapon):
    def __init__(self):
        super().__init__(10, 0.05, 50, 1.5)

    def shoot(self, position: Vector2, target: Vector2):
        if self.can_shoot():
            direction = (target - position).normalize()
            bullet = Bullet(position + Vector2(1, 0), direction)
 