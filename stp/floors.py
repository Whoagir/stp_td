from pygame.sprite import Sprite
from pygame.draw import polygon


class Floor(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
