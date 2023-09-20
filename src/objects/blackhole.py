from pygame import Vector2
from pygame.sprite import Sprite
from core.gravity import PhysicsObject

BLACK_HOLE_MASS = 5000
BLACK_HOLE_SPEED = 300

class BlackHole(PhysicsObject, Sprite):
    def __init__(self, position: Vector2, target: Vector2):
        super().__init__(BLACK_HOLE_MASS, position, True, True)

        self.scale = 0.0
        self.frames = "TODO"
