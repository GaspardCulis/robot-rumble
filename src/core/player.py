from pygame import Vector2
import pygame
from pygame.key import ScancodeWrapper
from core.gravity import PhysicsObject

PLAYER_MASS = 20
PLAYER_SPEED = 0.5
class PlayerObject(PhysicsObject):

    def __init__(self, position: Vector2, inventory:list, width: int, height: int):
        super().__init__(PLAYER_MASS,position, True, False, width, height)
        self.percent = 0
        self.inventory = inventory
        self.width = width
        self.height = height





    def parseInput(self, keys: ScancodeWrapper):

        if keys[pygame.K_z]:
            self.velocity.y = -PLAYER_SPEED
        if keys[pygame.K_s]:
            self.velocity.y = PLAYER_SPEED
        if keys[pygame.K_q]:
            self.velocity.x = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
