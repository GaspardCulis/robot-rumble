from random import random
from time import perf_counter

from pygame import Rect, Surface, Vector2, transform

from core.imageloader import ImageLoader


class SpriteSheet():
    """
    Class for representing sprites with multiple frames
    """

    def __init__(self, spritesheet_path: str, rows: int, cols: int, frame_delay: float, frame_count: int = -1,
                 sprite_size: None | Vector2 = None, collect: bool = True) -> None:
        if frame_count == -1:
            frame_count = rows * cols
        self.spritesheet_path = spritesheet_path
        self.spritesheet = ImageLoader.get_instance().load(
            spritesheet_path,
            collect=collect
        )
        s = self.spritesheet.get_size()
        if sprite_size == None:
            sprite_size = Vector2(s[0] / cols, s[1] / rows)
        self.sprite_size = sprite_size
        self.rows = rows
        self.cols = cols
        self.original_sprite_size = Vector2(s[0] / cols, s[1] / rows)
        self.frame_count = frame_count
        self.last_frame_skip = perf_counter() + random()  # Add random delay to avoid all sprites updating at the same time
        self.frame_delay = frame_delay
        self.current_frame_index = 0
        self.__update_frame()

    def get_frame(self) -> Surface:
        if perf_counter() - self.last_frame_skip > self.frame_delay:
            self.current_frame_index = (self.current_frame_index + 1) % self.frame_count
            if self.frame_count > 1:
                self.__update_frame()
            self.last_frame_skip = perf_counter()
        return self.frame

    def __update_frame(self):
        r, c = (self.current_frame_index // self.cols), self.current_frame_index % self.cols
        self.frame = transform.scale(
            self.spritesheet.subsurface(  # type: ignore
                Rect(
                    c * self.original_sprite_size.x,
                    r * self.original_sprite_size.y,
                    self.original_sprite_size.x,
                    self.original_sprite_size.y
                )
            ),
            self.sprite_size
        )
