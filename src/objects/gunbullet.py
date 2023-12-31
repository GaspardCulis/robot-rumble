from pygame import Vector2
from pygame.sprite import Group

from core.imageloader import ImageLoader
from objects.bullet import Bullet

BULLET_KB = 60


class GunBullet(Bullet):
    all: Group = Group()

    def __init__(self, position: Vector2, target: Vector2, owner_id: int = 69):
        super().__init__(
            position=position,
            target=target,
            sprite=ImageLoader.get_instance().load("assets/img/bullet.png", 2, collect=False),
            damage=2.5
        )
        self.owner_id = owner_id
        self.kb = BULLET_KB

        GunBullet.all.add(self)

    def kill(self):
        GunBullet.all.remove(self)
        super().kill()
