from pygame import Vector2

from core.bullet import Bullet
from core.gravity import PhysicsObject
from core.weapon import Weapon

class Minigun(Weapon):
    NAME = 'minigun'
    IMAGE_PATH = ''
    COOLDOWN = 0.2
    def __init__(self):
        super().__init__()

    def shoot(self, position: Vector2, velocity: Vector2):
        bullet = Bullet(Vector2(position.x + 10, position.y), 80, 80)
        bullet.velocity = Vector2(velocity.x + 2, velocity.y + 2)
