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
    def __init__(self, pos: Tuple[int, int, int]):
        if pos[0] + pos[1] + pos[2] != 0:
            raise Exception('Hex error x+y+z==0')
        self.object = None
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

    @property
    def pos(self):
        return self.x, self.y, self.z

    def __add__(self, other: 'Hex'):
        return Hex((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other: 'Hex'):
        return Hex((self.x - other.x, self.y - other.y, self.z - other.z))

    def __mul__(self, other: int):
        self.x *= other
        self.y *= other
        self.z *= other
        return self

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
        cord = a.x + position[0] - (3 ** (1/2) / 2) * HEX_SIZE, a.y + position[1] - HEX_SIZE
        surface.blit(sun_surf, cord)


class Grid(object):
    def __init__(self, start_position):
        self.grid = []
        self.pos = start_position

    def generate_rect(self, size: int):
        for r in range(size):
            offset = r//2
            for q in range(-offset, size-offset):
                self.grid.append(Hex((q, r, -q-r)))

    def generate_rect_flat_top(self, left: int, right:int, top: int, bottom: int):
        for q in range(left, right):
            q_offset = q//2
            for r in range(top - q_offset, bottom - q_offset):
                self.grid.append(Hex((q, r, -q-r)))

    def generate_hex(self, size):
        for q in range(-size, size + 1):
            r1 = max(-size, -q-size)
            r2 = min(size, -q+size)
            for r in range(r1, r2 + 1):
                self.grid.append(Hex((q, r, -q-r)))

    def generate_trinlge(self, size: int):
        for q in range(size):
            for r in range(size-q):
                self.grid.append(Hex((q, r, -q-r)))

    def generate_bhex(self, size: int):
        self.clear()
        pos_data = set()
        for x in range(-size, size):
            for y in range(-size, size):
                for z in range(-size, size):
                    pos_data.add((x, y, z))
        for p in pos_data:
            self.grid.append(Hex(pos=p))

    def handle_events(self, event):
        pass

    def render(self, surface: Surface):
        for hex in self.grid:
            center = self.get_global_hex_position(hex)
            hex.render(surface, center)

    def get_global_hex_position(self, hex):
        x = self.pos[0] + (hex.x * 3**0.5 + hex.y * 3**0.5/2) * HEX_SIZE
        y = self.pos[1] + (hex.x * 0 + hex.y * 3/2) * HEX_SIZE
        return x, y

    def wall_search(self, radius):
        for i in range(len(self.grid)):
            if sum(map(abs, self.grid[i].pos)) > radius:
                self.grid[i].object = 1

    def clear(self):
        self.grid = []
