import pygame
from pygame import Surface
from pygame.sprite import Sprite

from src.objects.player import Player



def weapon_hud(screen: Surface, player: Player):

    rect_width = 100
    rect_height = 100
    police = pygame.font.Font("./assets/font/geom.TTF", 36)

    spacing = 50
    border_color = (255, 255, 255)

    x = 10
    for weapon in player.weapons:
        pygame.draw.rect(screen, border_color, (x, 10, rect_width, rect_height), 3)

        if player.weapons[player.selected_weapon_index] == weapon:
            ammo_text = police.render(str(weapon.remaining_ammo) + "/" + str(weapon.ammo), True, (255,255,255))
            screen.blit(ammo_text, (screen.get_width()-ammo_text.get_width(),screen.get_height()-ammo_text.get_height()))

        x += rect_width + spacing
