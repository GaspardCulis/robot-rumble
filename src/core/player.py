from typing import List, Any

from pygame import Vector2
import pygame
from pygame.key import ScancodeWrapper
from core.gravity import PhysicsObject
from core.minigun import Minigun

PLAYER_MASS = 20
PLAYER_SPEED = 2
class PlayerObject(PhysicsObject):

    def __init__(self, position: Vector2, inventory:list, width: int, height: int):
        super().__init__(PLAYER_MASS,position, True, False)
        self.percent = 0
        self.inventory = inventory
        self.width = width
        self.height = height
        self.minigun = Minigun()

        self.cdShoot = 0





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
            if self.cdShoot <= 0:
                print("test")
                self.cdShoot = self.minigun.COOLDOWN
                self.minigun.shoot(Vector2(self.position.x + self.width / 2, self.position.y + self.height / 2),
                                   self.velocity)
            else:
                self.cdShoot -= dt
