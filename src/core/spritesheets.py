import pygame

from pygame import Rect

def parse_spritesheet(spritesheet: pygame.Surface, rows: int, cols: int) -> list[pygame.Surface]:
    subsurfaces = []
    sprite_width = spritesheet.get_width() / cols
    sprite_height = spritesheet.get_height() / rows

    for i in range(rows):
        for j in range(cols):
            subsurfaces.append(spritesheet.subsurface(Rect(j * sprite_width, i * sprite_height, sprite_width, sprite_height)))

    return subsurfaces

