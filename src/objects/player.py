from pygame import Rect, Surface, Vector2, constants, transform
import pygame
import math
from pygame.event import Event
from pygame.key import ScancodeWrapper
from pygame.sprite import Group, Sprite
from core.gravity import PhysicsObject
from objects.planet import Planet

PLAYER_MASS = 800
PLAYER_HEIGHT = 80

class Player(PhysicsObject, Sprite):
    all: Group = Group()
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
        self.onground = False

        self.all.add(self)

    def update(self, delta: float):
        # Rotate towards nearest planet
        nearest_planet = sorted(Planet.all, key=lambda p : p.position.distance_squared_to(self.position))[0]
        target_angle = - math.degrees(math.atan2(nearest_planet.position.y - self.position.y, nearest_planet.position.x - self.position.x)) + 90

        short_angle = (target_angle - self.rotation) % 360
        short_angle = 2 * short_angle % 360 - short_angle 
        
        self.set_rotation(self.rotation + short_angle * delta * 6)
        
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

    def process_collisions(self, delta: float):
        """
        Met à jour le joueur en fonction de potentiels objets en collision
        """
        if not hasattr(self, "first_frame"):
            self.first_frame = False
            return
        self.onground = False
        for planet in Planet.all:
            if pygame.sprite.collide_circle(self, planet):
                # Check if lands on his feets
                collision_normal: Vector2 = (self.position - planet.position).normalize()
                # La différence entre notre rotation et l'angle de la normale au sol
                rotation_normal_diff = abs((collision_normal.angle_to(Vector2(1,0)) + 360)%360 - (self.rotation + 450) % 360)
                if rotation_normal_diff > 20:
                    # Not on feets, bounce
                    velocity_along_normal = self.velocity.dot(collision_normal)
                    reflexion_vector = self.velocity - 2 * velocity_along_normal * collision_normal
                    self.velocity = 0.9 * reflexion_vector
                    self.position += self.velocity * delta
                else:
                    # Clip to the floor
                    clip_position = planet.position + collision_normal * (self.radius + planet.radius)
                    self.position = clip_position
                    self.velocity = Vector2(0)
                    self.onground = True

    def set_rotation(self, rotation: float):
        self.rotation = rotation
        self.image = transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.original_image.get_rect(center = self.position).center)
