import pygame
from pygame import Surface, Vector2
from pygame.sprite import Sprite

from objects.player import Player



def weapon_hud(screen: Surface, player: Player):

    rect_width = 100
    rect_height = 100
    police = pygame.font.Font("./assets/font/geom.TTF", 36)

    spacing = 50
    border_color = (255, 255, 255)
    weapon_img_path = "./assets/img/weapons/"

    x = 10
    for weapon in player.weapons:
        pygame.draw.rect(screen, border_color, (x, 10, rect_width, rect_height), 3)

        surface = pygame.image.load(weapon_img_path+(weapon.__class__.__name__+".png").lower())
        surface = pygame.transform.scale(surface, Vector2(150, 150))
        screen.blit(surface, Vector2(x-surface.get_width()/4, 0-surface.get_height()/6))


        if player.weapons[player.selected_weapon_index] == weapon:
            print(player.selected_weapon_index)
            ammo_remaining = max(weapon.remaining_ammo, 0)
            ammo_text = police.render(str(ammo_remaining) + "/" + str(weapon.ammo), True, (255,255,255))
            screen.blit(ammo_text, (screen.get_width()-ammo_text.get_width(),screen.get_height()-ammo_text.get_height()))

        x += rect_width + spacing
