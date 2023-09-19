from abc import ABC, abstractmethod
from time import monotonic
from pygame import Vector2

class Weapon():
    def __init__(self, recoil: float, cooldown_delay: float, ammo: int, reload_time: float) -> None:
        self.recoil = recoil
        self.cooldown_delay = cooldown_delay
        self.ammo = ammo
        self.reload_time = reload_time
        self.remaining_ammo = ammo
        self.last_shot = 0.0
        self.reload_t = 0.0
    
    @abstractmethod
    def shoot(self, origin: Vector2, target: Vector2):
        """
        Shoots a projectile given an origin, a target
        Returns a recoil force
        """
        pass
    
    def can_shoot(self) -> bool:
        """
        Handles the shootting logic like the ammo and cooldown
        After processing, returns True if the weapon can shoot, False otherwise
        """
        if self.remaining_ammo == 0:
            self.reload_t = monotonic()
            self.remaining_ammo = -1
            return False
        
        if self.remaining_ammo == -1:
            if monotonic() - self.reload_t >= self.reload_time:
                self.remaining_ammo = self.ammo
            else:
               return False

        if monotonic() - self.last_shot >= self.cooldown_delay:
            self.last_shot = monotonic()
            self.remaining_ammo -= 1
            return True
        else:
            return False