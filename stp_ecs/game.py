from collections import defaultdict

import esper
import pygame

from systems import *
from components import *
from config import *
from presets import player_preset, green_floor_preset, red_floor_preset, purpul_floor_preset
from grid import HexagonGridTypes, generate_hex_grid, hex_to_pixel, get_path


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

        for h in generate_hex_grid(6):
            ent = create_sprite_entity(self.world,
                                       empty_floor_preset,
                                       pos=hex_to_pixel(HexagonGridTypes.pointy_top, h, 31))
            self.world.add_component(ent, HexagonComponent(hexagon=h))

        obstacles = [Hexagon(1, -1, 0), Hexagon(2, -1, -1), Hexagon(2, 0, -2), Hexagon(1, 1, -2), Hexagon(1, 1, -2),
                     Hexagon(0, 2, -2)]
        start = Hexagon(0, 0, 0)
        end = Hexagon(3, 0, -3)
        offset = Hexagon(0, 3, -3)
        for h in obstacles:
            create_sprite_entity(self.world,
                                 red_floor_preset,
                                 pos=hex_to_pixel(HexagonGridTypes.pointy_top, h + offset, 31))
        for h in get_path(obstacles, start, end):
            create_sprite_entity(self.world,
                                 green_floor_preset,
                                 pos=hex_to_pixel(HexagonGridTypes.pointy_top, h + offset, 31))
        create_sprite_entity(self.world,
                             purpul_floor_preset,
                             pos=hex_to_pixel(HexagonGridTypes.pointy_top, start + offset, 31))
        create_sprite_entity(self.world,
                             purpul_floor_preset,
                             pos=hex_to_pixel(HexagonGridTypes.pointy_top, end + offset, 31))

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
