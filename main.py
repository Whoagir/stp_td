import pygame
import esper

from config import *
from hex_grid import *


def main():    
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game")
    clock = pygame.time.Clock()

    pygame.font.init()
    my_font = pygame.font.Font(None, 20)

    start_point_window = (0, 0)
    end_point_window = (SCREEN_WIDTH, SCREEN_HEIGHT)

    center_point_grid = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - HEX_SIZE / 2)

    a = Grid(center_point_grid)
    a.generate_bhex(7)
    a.render(screen)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()

        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
