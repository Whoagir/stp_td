import pygame
import enum
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
HEX_SIZE = 16
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
    sun_surf.append(pygame.image.load('media/floor' + str(i+1) + '.png'))
    sun_surf[i] = pygame.transform.scale(sun_surf[i], (3 ** (1/2) * HEX_SIZE + 2, 2 * HEX_SIZE + 2))
sun_rect = sun_surf[0].get_rect()

floor_n_surf = pygame.image.load('media/floor_normal.png')
floor_n_surf = pygame.transform.scale(floor_n_surf, (3 ** (1/2) * HEX_SIZE + 2, 2 * HEX_SIZE + 2))
floor_n_rect = floor_n_surf.get_rect()
# background
back_surf = pygame.image.load('media/background.png')
back_surf = pygame.transform.scale(back_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
back_rect = back_surf.get_rect()
# tower
tower_surf_array = []
for i in range(5):
    tower_surf_array.append(pygame.image.load('media/floor' + str(i+1) + '.png'))
    tower_surf_array[i] = pygame.transform.scale(tower_surf_array[i], (3 ** (1/2) * HEX_SIZE + 2, 2 * HEX_SIZE + 2))
tower_rect_array = tower_surf_array[0].get_rect()
# enum
class FloorType(enum.Enum):
    external = 1 # внешний пол
    normal = 0 # обычный пол

class TowerType(enum.Enum):
    zircon = 1
    aquamarine = 2
    diamond = 3
    citrin = 4
    ruby = 5
    topaz = 6
    supphire = 7
    peridof = 8
    emerald = 9