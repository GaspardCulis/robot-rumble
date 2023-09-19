from abc import ABC, abstractmethod
from pygame import Vector2

class Weapon():
    def __init__(self, recoil: float, cooldown_delay: float, ammo: int, reload_time: float) -> None:
        self.recoil = recoil
        self.cooldown_delay = cooldown_delay,
        self.ammo = ammo,
        self.reload_time = reload_time
    
    @abstractmethod
    def shoot(self, origin: Vector2, target: Vector2):
        """
        Shoots a projectile given an origin, a target
        Returns a recoil force
        """
        pass
    
