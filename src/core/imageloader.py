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

    def load(self, image_path: str, scale: float | int | Vector2 | Tuple[int, int] | None = None, alpha_channel: bool = True) -> Surface:
        key = f"{image_path}|{scale if scale != None else ''}|{alpha_channel}"
        if not (key in self.loaded_images):
            img = image.load(image_path)
            if alpha_channel: img = img.convert_alpha()
            else: img = img.convert()
            if isinstance(scale, float) or isinstance(scale, int):
                img = transform.scale_by(img, scale)
            elif  isinstance(scale, Vector2) or isinstance(scale, tuple):
                img = transform.scale(img, scale)
            self.loaded_images[key] = img
            print(f"[{self.__class__.__name__}] Loaded {image_path}" + ("" if scale == None else f" and scale {scale}"))
        return self.loaded_images[key]
        
    @staticmethod
    def get_instance() -> 'ImageLoader':
        if ImageLoader.__instance == None:
            ImageLoader()
        return ImageLoader.__instance # type: ignore
