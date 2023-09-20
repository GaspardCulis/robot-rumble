from pygame import Vector2

from objects.bullet import Bullet
from core.gravity import PhysicsObject
from objects.weapon import Weapon

from core.sound import Sound

class Minigun(Weapon):
    def __init__(self):
        super().__init__(30, 0.05, 50, 1.5)

    def shoot(self, position: Vector2, target: Vector2) -> Vector2:
        if self.can_shoot():
            direction = (target - position).normalize()
            Sound.get().play('minigun')
            bullet = Bullet(position + Vector2(1, 0), direction)
            return direction * self.recoil
        return Vector2(0)
 
