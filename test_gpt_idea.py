import pygame
import random

# Устанавливаем размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VIOLET = (148, 0, 211)
COLOR = [(255, 0, 0), (0, 0, 255), (255, 255, 255)]
# Размеры гексагона
HEX_SIZE = 10

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screen.fill(BLACK)


def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)


class Grid(object):
    def __init__(self, surface):
        self.hexsagons = []
        self.center_hex = []
        self.surface = surface
        self.cash = []

    def generation(self):
        a = HEX_SIZE
        b = 3 ** (1 / 2)
        x = a * b / 2 - a * 4
        while x < SCREEN_WIDTH + a * 2:
            y = -a * 2
            while y < SCREEN_HEIGHT:
                self.hexsagons.append([
                    (x, y),
                    (x + b * a / 2, y + a / 2),
                    (x + b * a / 2, y + 3 * a / 2),
                    (x, y + 2 * a),
                    (x - a * b / 2, y + 3 * a / 2),
                    (x - a * b / 2, y + a / 2)])
                y += 6 * a / 2
            x += a * b
        a = HEX_SIZE
        b = 3 ** (1 / 2)
        x = a * b - a * 4
        while x < SCREEN_WIDTH + a * 2:
            y = 3 * a / 2 - a * 2
            while y < SCREEN_HEIGHT:
                self.hexsagons.append([
                    (x, y),
                    (x + b * a / 2, y + a / 2),
                    (x + b * a / 2, y + 3 * a / 2),
                    (x, y + 2 * a),
                    (x - a * b / 2, y + 3 * a / 2),
                    (x - a * b / 2, y + a / 2)])
                y += 6 * a / 2
            x += a * b

        for hexagon in self.hexsagons:
            self.center_hex.append([hexagon[0][0], (hexagon[0][1] + hexagon[3][1]) / 2])

    def render(self):
        for hexagon in self.hexsagons:
            for i in range(6):
                pygame.draw.aaline(self.surface, WHITE, hexagon[i - 1], hexagon[i])

    def draw_polygon(self, polygon):
        self.cash.append(self.hexsagons[polygon])

    def update(self):
        if len(self.cash) != 0:
            for polygon in self.cash:
                pygame.draw.polygon(self.surface, VIOLET, polygon)

    def click(self, position):
        flag = self.seach_long(position)
        if flag != None:
            self.draw_polygon(flag)

    def get_hexagon(self):
        return self.hexsagons

    def seach_long(self, point):  # возвращает ближайший гексагон (номер) к point
        for center in self.center_hex:
            if distance(center, point) < HEX_SIZE:
                return self.center_hex.index(center)


def wall_generate():
    a = HEX_SIZE
    b = 3 ** (1 / 2)

    for x in range(0, SCREEN_WIDTH + int(a * b), int(a * b) - a):
        grid.click((x, 0))
        if random.randint(0, 10) == 1:
            grid.click((x, a * b))

    for x in range(0, SCREEN_WIDTH + int(a * b), int(a * b) - a):
        grid.click((x, SCREEN_HEIGHT - 1))
        if random.randint(0, 10) == 1:
            grid.click((x, SCREEN_HEIGHT - a * b / 2))

    for y in range(0, SCREEN_WIDTH + int(a * b), int(a * b) - a):
        grid.click((1, y))
        if random.randint(0, 10) == 1:
            grid.click((a * b, y))

    for y in range(0, SCREEN_WIDTH + int(a * b), int(a * b) - a):
        grid.click((SCREEN_WIDTH, y))
        if random.randint(0, 10) == 1:
            grid.click((SCREEN_WIDTH - a * b / 2, y))


grid = Grid(screen)
grid.generation()
grid.render()
wall_generate()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                grid.click(pos)
        grid.update()
        pygame.display.flip()
