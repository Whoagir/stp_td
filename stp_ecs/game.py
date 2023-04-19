from collections import defaultdict

import esper
import pygame

from systems import *
from components import *
from config import *
from presets import player_preset


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

        self.world = esper.World()

        movement_processor = MovementProcessor()
        render_processor = RenderProcessor(self.surface)
        mouse_click_processor = MouseClickProcessor()
        collide_processor = CollideProcessor()
        collision_processor = CollisionProcessor()

        self.world.add_processor(movement_processor)
        self.world.add_processor(render_processor)
        self.world.add_processor(mouse_click_processor)
        self.world.add_processor(collide_processor)
        self.world.add_processor(collision_processor)

        player = create_sprite_entity(self.world, player_preset)
        self.world.add_component(player, VelocityComponent(x=2, y=1))

        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.keys_pressed = []

        self.keydown_handlers[pygame.K_ESCAPE].append(quit)

    def main_loop(self):
        while self.running:
            self.keys_pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    for hander in self.keydown_handlers[event.key]:
                        hander(event)
                if event.type == pygame.KEYUP:
                    for hander in self.keyup_handlers[event.key]:
                        hander(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.world.create_entity(MouseClickComponent(*event.pos))
            self.world.process()
            self.clock.tick(40)

    def quit(self):
        self.running = False
        pygame.quit()


if __name__ == '__main__':
    g = Game()
    g.main_loop()
