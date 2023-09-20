from pygame import Rect, Surface, Vector2, constants, transform
from pygame.math import lerp
import pygame
import math
from pygame.event import Event
from pygame.key import ScancodeWrapper
from pygame.sprite import Group, Sprite
from core.gravity import PhysicsObject
from objects.minigun import Minigun
from objects.planet import Planet

PLAYER_MASS = 800
PLAYER_HEIGHT = 80
PLAYER_VELOCITY = 500

class Player(PhysicsObject, Sprite):
    all: Group = Group()
    max_id: int = 0

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
        self.jumped = False

        self.input_velocity = Vector2(0)

        self.weapons = [
            Minigun()
        ]
        self.selected_weapon_index = 0
        self.unique_id = self.max_id
        self.max_id += 1
        self.all.add(self)

    def kill(self):
        super().kill()
        self.all.remove(self)

    def update(self, delta: float):
        # Rotate towards nearest planet
        nearest_planet = sorted(Planet.all, key=lambda p : p.position.distance_to(self.position) - p.radius)[0]
        target_angle = - math.degrees(math.atan2(nearest_planet.position.y - self.position.y, nearest_planet.position.x - self.position.x)) + 90

        short_angle = (target_angle - self.rotation) % 360
        short_angle = 2 * short_angle % 360 - short_angle 

        self.process_keys(pygame.key.get_pressed(), delta)
        
        self.set_rotation(self.rotation + short_angle * delta * 6)

        self.process_collisions(delta)
        
    def process_keys(self, keys: ScancodeWrapper, delta: float):
        """
        Met à jour le joueur en fonction d'un appui de  touche
        """

        if keys[constants.K_d]:
            self.input_velocity.x = lerp(self.input_velocity.x, PLAYER_VELOCITY, delta * 2)
        if keys[constants.K_q]:
            self.input_velocity.x = lerp(self.input_velocity.x, -PLAYER_VELOCITY, delta * 2)
        if not (keys[constants.K_d] or keys[constants.K_q]):
            self.input_velocity.x = lerp(self.input_velocity.x, 0, delta * 6)
        if keys[constants.K_z] and not self.jumped:
            speed = Vector2(0, -1).rotate(-self.rotation) * 600
            self.velocity += speed
            self.position += speed * delta  # Move, to avoid clipping instantly
            self.jumped = True
        if keys[constants.K_s]:
            self.input_velocity.y = lerp(self.input_velocity.y, PLAYER_VELOCITY * 0.75, delta*4)
        else:
            self.input_velocity.y = lerp(self.input_velocity.y, 0, delta * 10)

        # Update position
        self.position += self.input_velocity.rotate(-self.rotation) * delta

    def process_collisions(self, delta: float):
        """
        Met à jour le joueur en fonction de potentiels objets en collision
        """
        if not hasattr(self, "first_frame"):
            self.first_frame = False
            return
        for planet in Planet.all:
            if pygame.sprite.collide_circle(self, planet):
                # Check if lands on his feets
                collision_normal: Vector2 = (self.position - planet.position).normalize()
                # La différence entre notre rotation et l'angle de la normale au sol
                rotation_normal_diff = abs((collision_normal.angle_to(Vector2(1,0)) + 360)%360 - (self.rotation + 450) % 360)
                if rotation_normal_diff > 30:
                    # Not on feets, bounce
                    velocity_along_normal = self.velocity.dot(collision_normal)
                    reflexion_vector = self.velocity - 2 * velocity_along_normal * collision_normal
                    self.velocity = 0.5 * reflexion_vector
                else:
                    # Clip to the floor
                    self.velocity = Vector2(0)
                    self.jumped = False
                # In both cases, we want to set the position to the floor
                clip_position = planet.position + collision_normal * (self.radius + planet.radius)
                self.position = clip_position

    def handle_click(self, position: Vector2):
        # Shooting
        self.weapons[self.selected_weapon_index].shoot(self.position, position)

    def set_rotation(self, rotation: float):
        self.rotation = rotation
        self.image = transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.original_image.get_rect(center = self.position).center)
