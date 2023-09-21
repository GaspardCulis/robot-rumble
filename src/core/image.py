from typing import Optional, Dict, Any

import pygame
from pygame import Surface, Vector2
import os

from core import spritesheets


class Image:
    transformed_images: dict[tuple[str, int], pygame.Surface]
    transformed_animated: dict[tuple[str, int], list[pygame.Surface]]

    all: dict[str, Surface]
    all_spritesheets: dict[str, list[pygame.Surface]]
    instance: Optional['Image'] = None

    def __init__(self):
        self.all = {}
        self.all_spritesheets = {}
        self.transformed_images = {}
        self.transformed_animated = {}

    @staticmethod
    def get():
        if Image.instance is None:
            Image.instance = Image()
        return Image.instance

    def load_spritesheet(self, path: str, rows: int, cols: int, frame_count: int = -1, has_alpha: bool = True) -> list[
        Surface]:
        path = os.path.abspath(path)
        if path in self.all_spritesheets:
            return self.all_spritesheets[path]
        surfaces = spritesheets.parse_spritesheet(self.load(path, has_alpha), rows, cols, frame_count)
        self.all_spritesheets[path] = surfaces
        return surfaces

    def load_scaled_sprites(self, path: str, rows: int, cols: int, scalar: int) -> list[Surface]:
        path = os.path.abspath(path)
        if (path, scalar) in self.transformed_animated:
            return self.transformed_animated[path, scalar]
        scaled = list(map(
            lambda x: pygame.transform.scale(x, Vector2(scalar)),
            Image.get().load_spritesheet(
                path,
                rows, cols, has_alpha=True
            )
        ))
        self.transformed_animated[path, scalar] = scaled
        return scaled

    def load_scaled(self, path: str, scalar: int) -> Surface:
        path = os.path.abspath(path)
        if (path, scalar) in self.transformed_images:
            return self.transformed_images[path, scalar]
        scaled = pygame.transform.scale(self.load(path, True), Vector2(scalar))
        self.transformed_images[path, scalar] = scaled
        return scaled

    def load(self, path: str, has_alpha: bool = True) -> Surface:
        path = os.path.abspath(path)
        if path in self.all:
            return self.all[path]
        surface = pygame.image.load(path)
        if has_alpha:
            surface = surface.convert_alpha()
        else:
            surface = surface.convert()
        self.all[path] = surface
        return surface
