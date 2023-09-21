from pygame import Vector2
from pygame.sprite import Sprite
from objects.blackhole import BlackHole
from objects.weapon import Weapon
from core.sound import Sound

class BlackHoleGun(Weapon):
    def __init__(self, owner) -> None:
        super().__init__(owner, 0.0, 0.0, 1, 15, "blackholegun.png")

    def shoot(self, origin: Vector2, target: Vector2) -> Vector2:
        if super().can_shoot():
            bullet = BlackHole(self.get_bullet_spawnpoint(), target)
            Sound.get().play('black_hole_gun')
        return Vector2(0)

