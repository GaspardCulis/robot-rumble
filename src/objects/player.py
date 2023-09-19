from pygame import Rect, Surface, Vector2, constants, transform
import pygame
from pygame.event import Event
from pygame.key import ScancodeWrapper
from pygame.sprite import Group, Sprite
from ..core.collision import CircleShape, CollisionObject, RectShape
from ..core.gravity import PhysicsObject
from ..core.player import PLAYER_SPEED

PLAYER_MASS = 800
PLAYER_HEIGHT=80

all_players: Group = Group()

class Player(PhysicsObject, Sprite):
    def __init__(self, position: Vector2, sprite: Surface):
        super().__init__(mass=PLAYER_MASS, position=position, passive = True, static = False)

        # Degrees
        self.rotation = 0.0
        # Ranges from 0.0 to 1.0
        self.percentage = 0.0

        self.original_image = transform.scale_by(sprite, PLAYER_HEIGHT/sprite.get_rect().height)
        self.image = transform.rotozoom(self.original_image, self.rotation, 1.0)
        self.rect = self.image.get_rect(center=self.original_image.get_rect(center = self.position).center)
        self.radius = PLAYER_HEIGHT/2

        all_players.add(self)

    def update(self, delta: float):
        self.set_rotation(self.rotation + delta * 90)
        
    def process_keys(self, keys: ScancodeWrapper, delta: float):
        """
        Met à jour le joueur en fonction d'un appui de  touche
        """
        if keys[constants.K_d]:
            pass
        if keys[constants.K_q]:
            pass
        if keys[constants.K_z]:
            pass
        if keys[constants.K_s]:
            pass

    def process_collisions(self, colliders: list, delta: float):
        """
        Met à jour le joueur en fonction de potentiels objets en collision
        """
        if not hasattr(self, "first_frame"):
            self.first_frame = False
            return
        for sprite in colliders:
            if pygame.sprite.collide_circle(self, sprite):
                print(sprite)
                self.velocity *= -0.9
                self.velocity += sprite.velocity
                self.position += self.velocity * delta

    def set_rotation(self, rotation: float):
        self.rotation = rotation
        self.image = transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.original_image.get_rect(center = self.position).center)
