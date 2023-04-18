from collections import defaultdict

import pygame, esper


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 600))
        self.running = True

        self.world = esper.World()

        self.keydown_handlers = defaultdict()
        self.keyup_handlers = defaultdict()
        self.keys_pressed = []

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                pass

    def quit(self):
        self.running = False
        pygame.quit()
