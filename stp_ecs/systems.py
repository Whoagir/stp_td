import esper
import pygame.display

from components import *


class RenderProcessor(esper.Processor):
    def __init__(self, surface: Surface, clear_color=(0, 0, 0)):
        self.surface = surface
        self.clear_color = clear_color

    def process(self, *args, **kwargs):
        self.surface.fill(self.clear_color)
        for ent, (rend,) in self.world.get_components(RenderComponent):
            self.surface.blit(rend.image, rend.rect)
        pygame.display.flip()
