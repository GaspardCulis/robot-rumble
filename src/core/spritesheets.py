import pygame

from pygame import Rect, Vector2, transform

def parse_spritesheet(spritesheet: pygame.Surface, rows: int, cols: int, frame_count:int = -1, scale: None | Vector2 = None) -> list[pygame.Surface]:
    subsurfaces = []
    sprite_width = spritesheet.get_width() / cols
    sprite_height = spritesheet.get_height() / rows

    frame_index = 0
    for i in range(rows):
        for j in range(cols):
            sub = spritesheet.subsurface(Rect(j * sprite_width, i * sprite_height, sprite_width, sprite_height))
            if scale:
                sub = transform.scale(sub, scale)
            subsurfaces.append(sub)
            frame_index += 1
            if frame_index == frame_count:
                return subsurfaces

    return subsurfaces

