from esper import Processor
import pygame.display

from components import *


class MovementProcessor(Processor):
    def process(self, *args, **kwargs):
        for ent, (pos, vel) in self.world.get_components(PositionComponent, VelocityComponent):
            pos.x, pos.y = pygame.Vector2(pos.x, pos.y) + pygame.Vector2(vel.x, vel.y)


class RenderProcessor(Processor):
    def __init__(self, surface: Surface, clear_color=(0, 0, 0)):
        self.surface = surface
        self.clear_color = clear_color

    def process(self, *args, **kwargs):
        self.surface.fill(self.clear_color)
        for ent, (sprite, pos) in self.world.get_components(SpriteComponent, PositionComponent):
            rect = sprite.image.get_rect()
            rect.topleft = (pos.x, pos.y)
            self.surface.blit(sprite.image, rect)
        pygame.display.flip()


class OneFrameProcessor(Processor):
    def process(self, *args, **kwargs):
        for ent, (one_frame,) in self.world.get_components(MouseClickComponent):
            self.world.remove_component(ent, one_frame)
