from pygame import Vector2
from objects.weapon import Weapon


class BlackHoleGun(Weapon):
    def __init__(self, recoil: float, cooldown_delay: float, ammo: int, reload_time: float) -> None:
        super().__init__(0.0, 0.0, 1, 15)

    def shoot(self, origin: Vector2, target: Vector2) -> Vector2:
        return super().shoot(origin, target)
