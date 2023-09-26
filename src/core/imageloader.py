import sys
from typing import Dict, Tuple

from pygame import Surface, Vector2, image, transform
from weakref import WeakValueDictionary


class ImageLoader:
    __instance = None

    def __init__(self):
        if ImageLoader.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ImageLoader.__instance = self

        self.loaded_images: WeakValueDictionary[str, Surface] = WeakValueDictionary()
        self.__persistent_img_refs = []

    def load(self, image_path: str, scale: float | int | Vector2 | Tuple[int, int] | None = None,
             alpha_channel: bool = True, collect: bool = True) -> Surface:
        key = f"{image_path}|{scale if scale is not None else ''}|{alpha_channel}"
        img = self.loaded_images.get(key, None)
        if img is None:
            img = image.load(image_path)
            if alpha_channel:
                img = img.convert_alpha()
            else:
                img = img.convert()
            if isinstance(scale, float) or isinstance(scale, int):
                img = transform.scale_by(img, scale)
            elif isinstance(scale, Vector2) or isinstance(scale, tuple):
                img = transform.scale(img, scale)
            self.loaded_images[key] = img
            if not collect: self.__persistent_img_refs.append(img)
            print(f"[{self.__class__.__name__}] Loaded {image_path}" + ("" if scale is None else f" and scale {scale}"))
        return img

    @staticmethod
    def get_instance() -> 'ImageLoader':
        if ImageLoader.__instance is None:
            ImageLoader()
        return ImageLoader.__instance  # type: ignore
