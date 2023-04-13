import pygame
pygame.font.init()
FPS = 30
GAME_TITLE = 'Game'
# Устанавливаем размеры окна
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 790
# Цвета
BLACK = (0, 0, 0)
WHITE = (2, 2, 2)
WHITE_T = (255, 255, 255)
WHITE_T2 = (0, 255, 255)
WHITE_T3 = (0, 255, 0) # G
WHITE_T4 = (0, 0, 255) # B
VIOLET = (148, 0, 211)
RED = (180, 0, 0)
CHECK_POINT_ENEMY_COLOR = (70, 70, 70)
WALL_COLOR = (24, 99, 24)
COLOR = [(255, 0, 0), (0, 0, 255), (255, 255, 255)]
# Размеры гексагона
HEX_SIZE = 20
BORDER_RADIUS = 2
COLOR_BORDER_GRID = (40, 40, 40)
COLOR_BORDER_GRID_HIGHTLIGHT = (255, 0, 0)
# шрифты
menu_font_weight = 20
menu_hover_font_weight = 25
menu_font = pygame.font.Font(None, menu_font_weight)
menu_hover_font = pygame.font.Font(None, menu_hover_font_weight)
# картинки
sun_surf = []
for i in range(5):
    sun_surf.append(pygame.image.load('floor' + str(i+1) + '.png'))
    sun_surf[i] = pygame.transform.scale(sun_surf[i], (3 ** (1/2) * HEX_SIZE + 2, 2 * HEX_SIZE + 2))
sun_rect = sun_surf[0].get_rect()
