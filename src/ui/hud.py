from time import monotonic

import pygame
from pygame import Surface, Vector2, Color

from core.imageloader import ImageLoader
from objects.player import Player

FONT_PATH = "assets/font/geom.TTF"


class Hud():

    def __init__(self, player: Player):

        self.rect_width = 100
        self.rect_height = 100
        self.police = pygame.font.Font(FONT_PATH, 36)
        self.police_small = pygame.font.Font(FONT_PATH, 24)
        self.player = player
        self.spacing = 50
        self.border_color = Color(255, 255, 255)
        self.surfaces = []
        for weapon in self.player.weapons:
            self.surfaces.append(pygame.transform.scale(weapon.original_image, Vector2(150, 150)))

        head_img = ImageLoader.get_instance().load("./assets/img/head.png")
        self.head = pygame.transform.scale(head_img, Vector2(50, 50))

    def weapon_hud(self, screen: Surface):
        x = 10
        k = 10
        for surface in self.surfaces:
            screen.blit(surface, Vector2(k - surface.get_width() / 4, 0 - surface.get_height() / 6))
            k += self.rect_width + self.spacing
        for weapon in self.player.weapons:
            pygame.draw.rect(screen, self.border_color, (x, 10, self.rect_width, self.rect_height), 3, 15)
            timer = monotonic() - weapon.reload_t
            if timer <= weapon.reload_time:
                remaining_time = round(weapon.reload_time - timer, 1)
                cd_text = self.police_small.render(str(remaining_time), True, self.border_color)
            else:
                cd_text = self.police.render("", True, self.border_color)

            screen.blit(cd_text, Vector2(x + self.rect_width - cd_text.get_width() - 10, self.rect_height - 20))

            if self.player.weapons[self.player.selected_weapon_index] == weapon:
                ammo_remaining = max(weapon.remaining_ammo, 0)
                ammo_text = self.police.render(str(ammo_remaining) + "/" + str(weapon.ammo) + " n", True,
                                               (255, 255, 255))
                screen.blit(ammo_text,
                            (screen.get_width() - ammo_text.get_width(), screen.get_height() - ammo_text.get_height()))

            x += self.rect_width + self.spacing

    def hp_hud(self, screen: Surface):

        spacing = 0
        for i in range(1, self.player.lives + 1):
            head_pos = pygame.Rect(10 + spacing, screen.get_height() - 55, 10, 10)
            screen.blit(self.head, head_pos)
            spacing += self.head.get_width() + 10
        if self.player.lives > 0:
            percent_text = self.police.render(": " + str(self.player.percentage) + "%", True, self.border_color)
        else:
            percent_text = self.police.render("PERDU", True, self.border_color)

        screen.blit(percent_text, Vector2(spacing + 30, screen.get_height() - 40))

    def fps_hud(self, screen: Surface, delta: float):
        if delta == 0:
            delta = 1  # windows putain
        fps_text = self.police.render(str(round(1 / delta, 0)) + " FPS", True, self.border_color)
        screen.blit(fps_text, Vector2(screen.get_width() - fps_text.get_width(), 20))
