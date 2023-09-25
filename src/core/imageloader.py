import sys
from typing import Dict, Tuple

from pygame import Surface, Vector2, image, transform


class ImageLoader:
    __instance = None

    def __init__(self):
        if ImageLoader.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ImageLoader.__instance = self

        self.loaded_images: Dict[str, Surface] = {}
        self.__persistent_img_refs = []

    def load(self, image_path: str, scale: float | int | Vector2 | Tuple[int, int] | None = None,
             alpha_channel: bool = True, collect: bool = True) -> Surface:
        key = f"{image_path}|{scale if scale != None else ''}|{alpha_channel}"
        if not (key in self.loaded_images):
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
            print(f"[{self.__class__.__name__}] Loaded {image_path}" + ("" if scale == None else f" and scale {scale}"))
        return self.loaded_images[key]

    def collect(self):
        """
        Frees the loaded images not referenced anymore
        """
        to_clear = []
        for key in self.loaded_images.keys():
            if sys.getrefcount(self.loaded_images[key]) <= 2:
                to_clear.append(key)
        for c in to_clear:
            del self.loaded_images[c]
            print(f"[ImageLoader] Free image {c.split('|', 1)[0]}")


    @staticmethod
    def get_instance() -> 'ImageLoader':
        if ImageLoader.__instance == None:
            ImageLoader()
        return ImageLoader.__instance  # type: ignore
