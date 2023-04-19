from typing import Tuple

from pygame.transform import scale_by
from pygame.image import load


class SpritePreset:
    def __init__(self,
                 image_src: str,
                 scale_factor: Tuple[float, float] = None,
                 origin: Tuple[float, float] = (0, 0)):
        self.image = load(image_src)
        if scale_factor:
            self.image = scale_by(self.image, scale_factor)
        self.origin = origin
