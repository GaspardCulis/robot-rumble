from pygame import Vector2

from objects.gunbullet import GunBullet
from objects.weapon import Weapon

from core.sound import Sound

class Shotgun(Weapon):
    def __init__(self, owner) -> None:
        super().__init__(owner, 800, 0.0, 1, 2, "shotgun.png")
        self.reload_snd = 'reload_shotgun'
        
    def shoot(self, target: Vector2) -> Vector2:
        if self.can_shoot():
            Sound.get().play('shotgun')
            center_bullet = None
            for a in range(-10, 10):
                bullet = GunBullet(self.get_bullet_spawnpoint(), target, self.owner.unique_id)
                if a == 0:
                    center_bullet = bullet
            return center_bullet.direction_vector * self.recoil
        return Vector2(0)