from abc import ABC, abstractmethod
from os import path
from time import monotonic
from pygame import Surface, Vector2
import pygame as pg
from pygame.sprite import Group, Sprite

ASSETS_DIR = "assets/img/weapons"

class Weapon(Sprite):
    all: Group = Group()
    def __init__(self, owner, recoil: float, cooldown_delay: float, ammo: int, reload_time: float, sprite_name: str) -> None:
        super().__init__(Weapon.all)
        self.owner = owner
        self.recoil = recoil
        self.cooldown_delay = cooldown_delay
        self.ammo = ammo
        self.reload_time = reload_time
        self.remaining_ammo = ammo
        self.last_shot = 0.0
        self.reload_t = 0.0
        self.original_image = pg.transform.scale_by(pg.image.load(path.join(ASSETS_DIR, sprite_name)), 2)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.image.get_rect(center = self.owner.position).center)
  
    @abstractmethod
    def shoot(self, origin: Vector2, target: Vector2) -> Vector2:
        """
        Shoots a projectile given an origin, a target
        Returns a recoil force Vector
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

    def update(self, mouse_position: Vector2):
        direction_vector = (mouse_position - self.owner.position).normalize()
        self.image = pg.transform.rotate(self.original_image, -(Vector2(1, 0).angle_to(direction_vector)))
        self.rect = self.image.get_rect(center=self.image.get_rect(center = self.owner.position).center)

    def is_selected(self) -> bool:
        return self.owner.weapons[self.owner.selected_weapon_index] == self
        
