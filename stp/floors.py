from math import pi, cos, sin
from pygame.sprite import Sprite
from pygame import Surface
from pygame.draw import polygon

import config


class EmptyHexagonFloor(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = Surface([config.HEXAGON_SIZE, config.HEXAGON_SIZE])
        self.image.fill((255, 200, 150))
        self.rect = self.image.get_rect()
