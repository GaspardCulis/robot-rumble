from abc import ABC, abstractmethod
from pygame import Vector2

class Weapon():
    @abstractmethod
    def shoot(self, origin: Vector2, target: Vector2) -> float:
        """
        Shoots a projectile given an origin, a target
        Returns a recoil force
        """
        pass
    
