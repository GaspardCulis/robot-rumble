import math
from pygame import Surface, Vector2, image, Rect, transform
from pygame.sprite import Sprite, collide_circle, Group
from core.collision import CircleShape, CollisionObject
from core.gravity import PhysicsObject

class Planet(PhysicsObject, Sprite):
    all = Group()
    
    def __init__(self, position: Vector2, radius: float, sprite: Surface):
        self.radius = radius
        mass = math.pi * self.radius**2

        super().__init__(mass=mass, position=position, passive=False, static=True)

        self.image = transform.scale(sprite, Vector2(self.radius * 2))
        self.rect = self.image.get_rect()

        self.all.add(self)

    def kill(self):
        super().kill()
        self.all.remove(self)

    def update(self):
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)
