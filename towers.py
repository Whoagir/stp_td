from pygame.sprite import Sprite
from pygame import Surface


class Tower(Sprite):
    def __init__(self, *gropus):
        super().__init__(*gropus)
        self.image = Surface([15, 15])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

