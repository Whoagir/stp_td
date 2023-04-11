import math
import pygame
from pygame import Surface, Rect
from typing import Tuple

from constant import *
from vector import *


def delete_duplicate(seq: list):
    return list(set(seq))


def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)


class Hex:
    def __init__(self, pos):
        self.object = None
        self.pos = pos

    def render(self, surface, position):
        if self.object == 1:
            self.draw_object(surface, position)
        self.draw_hex_border(surface, position)

    def update(self):
        pass

    def draw_hex_border(self, surface, hex_center):
        for i in range(6):
            point_cord = self.get_hex_side(hex_center, i)
            pygame.draw.line(surface, COLOR_BORDER_GRID,
                             point_cord[0], point_cord[1],
                             BORDER_RADIUS)

    def get_hex_side(self, hex_center, num):
        a = HEX_SIZE
        alfa = math.pi / 3
        array_cord_point = (hex_center[0] + a * math.cos(num * alfa + alfa / 2),
                            hex_center[1] + a * math.sin(num * alfa + alfa / 2)), \
                           (hex_center[0] + a * math.cos((1 + num) * alfa + alfa / 2),
                            hex_center[1] + a * math.sin((1 + num) * alfa + alfa / 2))
        return array_cord_point

    def draw_floor(self):
        pass

    def draw_object(self, surface, position):
        a = sun_rect
        cord = a.x + position[0], a.y + position[1]
        surface.blit(sun_surf, cord)


class Grid(object):
    def __init__(self, start_position):
        self.grid = []
        self.pos = start_position

    def generate_rect(self, width: int, height: int):
        self.clear()
        for x in range(width):
            y, z, p = 0, 0, 0
            while abs(y) < height:
                self.grid.append(Hex(pos=(x, y, z)))
                if p:
                    y -= 1
                else:
                    z -= 1
                p = not p

    def generate_bhex(self, size: int):
        self.clear()
        for x in range(-size, size):
            for y in range(-size, size):
                for z in range(-size, size):
                    self.grid.append(Hex(pos=(x, y, z)))

    def handle_events(self, event):
        pass

    def render(self, surface: Surface):
        for hex in self.grid:
            center = self.get_global_hex_position(hex)
            hex.render(surface, center)

    def get_global_hex_position(self, hex):
        a = HEX_SIZE
        b = 3 ** (1 / 2)
        rv = a * b
        alfa = math.pi / 3
        cord_xy = self.pos[0] + hex.pos[0] * rv + hex.pos[1] * rv * math.cos(alfa) + hex.pos[2] * rv * math.cos(
            alfa * 2), \
                  self.pos[1] - hex.pos[1] * rv * math.sin(alfa) - hex.pos[2] * rv * math.sin(alfa * 2)
        return cord_xy

    def wall_search(self, radius):
        for i in range(len(self.grid)):
            if sum(map(abs, self.grid[i].pos)) > radius:
                self.grid[i].object = 1
            else:
                self.grid[i].object = 0
            print(self.grid[i].pos, self.grid[i].object, sum(map(abs, self.grid[i].pos)))
            # self.grid[i].draw_object(surface)

    def clear(self):
        self.grid = []
