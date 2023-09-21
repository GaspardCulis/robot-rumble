import pygame
from pygame import Vector2

from objects.player import Player


class Camera:
    _camera_pos: Vector2
    screen_size: Vector2
    player_to_follow: Player

    def __init__(self, player: Player, screen_size: Vector2):
        self.player_to_follow = player
        self.screen_size = screen_size
        self._camera_pos = Vector2(player.position)  # copy to avoid modifying player pos

    def get_pos(self) -> Vector2:
        return self._camera_pos

    def get_scale(self) -> tuple[int, int]:
        return (1, 1)

    def update(self, delta: float):
        if self.player_to_follow.isDead and len(Player.all) > 0:
            target = Player.all.sprites()[self.player_to_follow.spectated_player_index]
        else:
            target = self.player_to_follow
        dest = -(target.position - self.screen_size / 2)
        # add mouse deviation
        dest.x += (pygame.mouse.get_pos()[0] / self.screen_size.x - 0.5) * -500
        dest.y += (pygame.mouse.get_pos()[1] / self.screen_size.y - 0.5) * -500

        self._camera_pos.x = pygame.math.lerp(self._camera_pos.x, dest.x,
                                              min(delta * abs(max(target.velocity.x / 60, 5)), 1))
        self._camera_pos.y = pygame.math.lerp(self._camera_pos.y, dest.y,
                                              min(delta * abs(max(target.velocity.y / 60, 5)), 1))
