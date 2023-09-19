import math
from pygame import Surface, Vector2, image, Rect, transform
from pygame.sprite import Sprite, collide_circle, Group
from core.collision import CircleShape, CollisionObject
from core.gravity import PhysicsObject

all_planets = Group()

class Planet(PhysicsObject, Sprite):
    def __init__(self, position: Vector2, radius: float, sprite: Surface):
        self.radius = radius
        mass = 4/3 * math.pi * self.radius**3

        super().__init__(mass=mass, position=position, passive=False, static=False)

        self.image = transform.scale(sprite, Vector2(self.radius * 2))
        self.rect = self.image.get_rect()

        all_planets.add(self)

    def update(self):
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)
