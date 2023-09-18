from pygame import Rect, Vector2
import pygame
from pygame.event import Event
from core.collision import CircleShape, CollisionObject, RectShape
from core.gravity import PhysicsObject

PLAYER_MASS = 80

class Player(PhysicsObject, CollisionObject):
    def __init__(self, position: Vector2):
        super().__init__(mass=PLAYER_MASS, position=position, passive = True, static = False,collision_shape=RectShape(position, Vector2(10, 10)) )

        # Ranges from 0.0 to 1.0
        self.percentage = 0.0

    def process_key_event(self, event: Event, delta: float):
        """
        Met à jour le joueur en fonction d'un appui de  touche
        """
        pass

    def process_collisions(self, colliders: list[CollisionObject]):
        """
        Met à jour le joueur en fonction de potentiels objets en collision
        """

    def display(self, screen: pygame.Surface):
        self.shape.debug_draw(screen)
        
    