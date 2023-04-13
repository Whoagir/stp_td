from pygame import Surface
from pygame.sprite import Sprite, Group


class GameObject:
    def __init__(self):
        pass

    def draw(self, surface: Surface, offset):
        pass

    def update(self, delta):
        pass

    def handle_events(self, event):
        pass
