from typing import List, Any

from pygame import Vector2
import pygame
from pygame.key import ScancodeWrapper
from .gravity import PhysicsObject

PLAYER_MASS = 20
PLAYER_SPEED = 2
class PlayerObject(PhysicsObject):
    bullets: list[PhysicsObject]

    def __init__(self, position: Vector2, inventory:list, width: int, height: int):
        super().__init__(PLAYER_MASS,position, True, False, width, height)
        self.percent = 0
        self.inventory = inventory
        self.width = width
        self.height = height
        self.bullets = []





    def parseInput(self, keys: ScancodeWrapper, dt: float):

        if keys[pygame.K_z]:
            self.velocity.y -= PLAYER_SPEED * dt
        if keys[pygame.K_s]:
            self.velocity.y += PLAYER_SPEED * dt
        if keys[pygame.K_q]:
            self.velocity.x -= PLAYER_SPEED * dt
        if keys[pygame.K_d]:
            self.velocity.x += PLAYER_SPEED * dt

        if keys[pygame.K_e]:
            bullet = PhysicsObject(20, Vector2(self.position.x + 10, self.position.y), True, False, 80, 80)
            bullet.velocity = Vector2(self.velocity.x + 2, self.velocity.y + 2)
            self.bullets.append(bullet)
