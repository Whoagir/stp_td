import sys
import pygame
from collections import defaultdict

from constant import *
from hex_grid import Grid
from menu import Button, Menu


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font = pygame.font.Font(None, 20)

        self.running = True
        self.objects = []

        self.dt = 0

        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

        self.keydown_handlers[pygame.K_ESCAPE].append(self.quit)

        self.grid = Grid((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - HEX_SIZE / 2))
        self.grid.generate_hex(30)
        self.keydown_handlers.update(self.grid.keydown_handlers)
        self.mouse_handlers.extend(self.grid.mouse_handlers)

    def main_loop(self):
        self.grid.wall_search(25)
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self):
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
                    handler(event.type, event.pos)

    def render(self):
        self.grid.render(self.screen, self.dt)
        for obj in self.objects:
            obj.render(self.screen)
        self.dt += 1
        pygame.display.flip()

    def update(self):
        for obj in self.objects:
            obj.update()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit(-1)


if __name__ == '__main__':
    game = Game()
    game.main_loop()
