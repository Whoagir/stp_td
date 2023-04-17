import sys
import pygame
from collections import defaultdict
from typing import Tuple

import config
from towers import Tower
from grid import HexagonGrid, HexagonGridTypes


class CameraGroup(pygame.sprite.Group):
    def __init__(self, offset=(0, 0)):
        super().__init__()
        self._offset = pygame.Vector2(offset)
        self.is_move = False
        self.ground_surface = pygame.image.load('../media/background.png')
        self.ground_rect = self.ground_surface.get_rect(topleft=(0, 0))

        self._grid = None
        self._show_grid = False

    def move(self, dv):
        self._offset += pygame.Vector2(dv)

    @property
    def offset(self):
        return self._offset

    def set_offset(self, pos: Tuple[float, float]):
        self._offset = pygame.Vector2(pos)

    def show_grid(self, grid: HexagonGrid):
        self._grid = grid
        self._show_grid = True

    def hide_grid(self):
        self._show_grid = False

    def draw_grid_border(self, surface: pygame.Surface, hexagon_size: float):
        for h in self._grid.hexes:
            for edge in self._grid.get_hexagon_edges(h, hexagon_size):
                pygame.draw.line(surface,
                                 config.GRID_COLOR,
                                 self._offset + edge[0],
                                 self._offset + edge[1],
                                 2)

    def custom_draw(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))
        ground_pos = self.ground_rect.topleft + self._offset
        surface.blit(self.ground_surface, ground_pos)
        if self._show_grid:
            self.draw_grid_border(surface, hexagon_size=config.HEXAGON_SIZE)
        for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
            offset_pos = self._offset + sprite.rect.topleft
            surface.blit(sprite.image, offset_pos)


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        self.running = True

        self.down_menu = None
        self.left_menu = None
        self.right_menu = None

        self.camera_group = CameraGroup()
        self.camera_group.set_offset((config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2))

        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.keypressed_handlers = defaultdict(list)
        self.mouse_handlers = []

        self.keydown_handlers[pygame.K_ESCAPE].append(self.quit)
        self.mouse_handlers.append(self.move_camera)
        self.mouse_handlers.append(self.set_tower)
        self.mouse_prev_pos = pygame.Vector2((0, 0))

        self.grid = HexagonGrid(HexagonGridTypes.pointy_top)
        self.grid.generate_hex(grid_size=12)

        self.camera_group.show_grid(self.grid)

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(config.GAME_FPS)

    def set_tower(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                t = Tower(self.camera_group)
                t.rect.topleft = event.pos - self.camera_group.offset

    def move_camera(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.camera_group.is_move = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.camera_group.is_move = False
        if event.type == pygame.MOUSEMOTION:
            if self.camera_group.is_move:
                self.camera_group.move(pygame.Vector2(event.pos)-self.mouse_prev_pos)
        self.mouse_prev_pos = pygame.Vector2(event.pos)

    def handle_events(self):
        pressed = pygame.key.get_pressed()
        for key in self.keypressed_handlers:
            if pressed[key]:
                for handler in self.keypressed_handlers[key]:
                    handler()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            if event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            if event.type in (pygame.MOUSEBUTTONDOWN,
                              pygame.MOUSEBUTTONUP,
                              pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event)

    def draw(self):
        self.camera_group.custom_draw(self.screen)
        pygame.display.flip()

    def update(self):
        self.camera_group.update()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit(-1)


if __name__ == '__main__':
    game = Game()
    game.main_loop()
