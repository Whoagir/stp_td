import sys
import pygame
from collections import defaultdict

from constant import *


class Hex:
    def __init__(self):
        pass

    def generate_hex_grid(self):
        pass

    def local_to_global(self, hx):
        pass

    def global_to_local(self, pos):
        pass


class Grid:
    def __init__(self):
        pass


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

        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

        self.keydown_handlers[pygame.K_ESCAPE].append(self.quit)

    def main_loop(self):
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
        for obj in self.objects:
            obj.render(self.screen)
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
