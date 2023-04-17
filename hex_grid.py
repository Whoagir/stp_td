import math
import random
from collections import defaultdict
from typing import Optional
from pygame import Surface
from typing import Tuple

from config import *


class Hex:
    def __init__(self, pos: Tuple[int, int, int]):
        if pos[0] + pos[1] + pos[2] != 0:
            raise Exception('Hex error x+y+z==0')
        self.floor = None
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

    def __str__(self):
        return 'Hex' + str(self.pos)

    def render(self, surface, position, dt, highlight=False):
        if self.floor == FloorType.normal:
            self.draw_floor(surface, position)
            #self.draw_object(surface, position, dt)
        self.draw_hex_border(surface, position, highlight=highlight)

    def update(self):
        pass

    def draw_hex_border(self, surface, hex_center, highlight=False):
        for i in range(6):
            point_cord = self.get_hex_side(hex_center, i)
            pygame.draw.line(surface,
                             COLOR_BORDER_GRID_HIGHTLIGHT if highlight else COLOR_BORDER_GRID,
                             point_cord[0],
                             point_cord[1],
                             BORDER_RADIUS)

    def get_hex_side(self, hex_center, num):
        a = HEX_SIZE
        alfa = math.pi / 3
        array_cord_point = (hex_center[0] + a * math.cos(num * alfa + alfa / 2),
                            hex_center[1] + a * math.sin(num * alfa + alfa / 2)), \
                           (hex_center[0] + a * math.cos((1 + num) * alfa + alfa / 2),
                            hex_center[1] + a * math.sin((1 + num) * alfa + alfa / 2))
        return array_cord_point

    def draw_floor(self, surface, position):
        a = floor_n_rect
        cord = a.x + position[0] - (3 ** (1 / 2) / 2) * HEX_SIZE, a.y + position[1] - HEX_SIZE
        surface.blit(floor_n_surf, cord)

    def draw_object(self, surface, position):
        a =
        cord = a.x + position[0] - (3 ** (1 / 2) / 2) * HEX_SIZE, a.y + position[1] - HEX_SIZE
        surface.blit(, cord)


class Grid(object):
    def __init__(self, position):
        self.grid = []
        self.pos = position
        self.current = None

        self.keydown_handlers = defaultdict(list)
        self.keydown_handlers[pygame.K_LEFT].append(self.move_left)
        self.keydown_handlers[pygame.K_RIGHT].append(self.move_right)
        self.keydown_handlers[pygame.K_UP].append(self.move_up)
        self.keydown_handlers[pygame.K_DOWN].append(self.move_down)
        self.keydown_handlers[pygame.K_SPACE].append(self.log_current_pos)

        self.mouse_handlers = [self.mouse_click]

    def generate_rect(self, size: int):
        for r in range(size):
            offset = r // 2
            for q in range(-offset, size - offset):
                self.grid.append(Hex((q, r, -q - r)))

    def generate_rect_flat_top(self, left: int, right: int, top: int, bottom: int):
        for q in range(left, right):
            q_offset = q // 2
            for r in range(top - q_offset, bottom - q_offset):
                self.grid.append(Hex((q, r, -q - r)))

    def get_hex(self, local_pos: Tuple[int, int, int]) -> Optional['Hex']:
        for h in self.grid:
            if (h.x, h.y, h.z) == local_pos:
                return h
        return None

    def set_current(self, local_pos: Tuple[int, int, int]):
        self.current = self.get_hex(local_pos)
        return self.current

    def get_current(self) -> Optional['Hex']:
        return self.current

    def generate_hex(self, size):
        for q in range(-size, size + 1):
            r1 = max(-size, -q - size)
            r2 = min(size, -q + size)
            for r in range(r1, r2 + 1):
                self.grid.append(Hex((q, r, -q - r)))

    def generate_trinlge(self, size: int):
        for q in range(size):
            for r in range(size - q):
                self.grid.append(Hex((q, r, -q - r)))

    def mouse_click(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pos, '~Hex =', self.global_to_local(pos))
            self.current = self.global_to_local(pos)
            if event.button == 3:
                self.current.floor = None
            if event.button == 1:
                self.current.floor = FloorType.normal

    def move_current(self, direction: Tuple[int, int, int]):
        if not self.current:
            return
        self.current.x += direction[0]
        self.current.y += direction[1]
        self.current.z += direction[2]

    def move_left(self, event_key):
        self.move_current(direction=(-1, 0, 1))

    def move_right(self, event_key):
        self.move_current(direction=(1, 0, -1))

    def move_up(self, event_key):
        self.move_current(direction=(0, -1, 1))

    def move_down(self, event_key):
        self.move_current(direction=(0, 1, -1))

    def log_current_pos(self, event_key):
        print('local:', self.current, 'global:', self.local_to_global(self.current))
        self.current.floor = None

    def render(self, surface: Surface, dt):
        for h in self.grid:
            center = self.local_to_global(h)
            h.render(surface, center, dt)
        if self.current:
            self.current.render(surface, self.local_to_global(self.current), dt, highlight=True)

    def local_to_global(self, hex) -> Tuple[float, float]:
        x = self.pos[0] + (hex.x * 3 ** 0.5 + hex.y * 3 ** 0.5 / 2) * HEX_SIZE
        y = self.pos[1] + (hex.y * 3 / 2) * HEX_SIZE
        return x, y

    def global_to_local(self, pos: Tuple[float, float]) -> 'Hex':
        pt = ((pos[0]-self.pos[0]) / HEX_SIZE, (pos[1]-self.pos[1]) / HEX_SIZE)
        q = 3**0.5/3 * pt[0] - 1/3 * pt[1]
        r = 2/3 * pt[1]
        return self.get_hex(local_pos=(round(q), round(r), -round(q)-round(r)))

    def wall_search(self, radius):
        for i in range(len(self.grid)):
            if sum(map(abs, self.grid[i].pos)) < radius:
                # self.grid[i].floor = FloorType.external
                self.grid[i].floor = FloorType.normal

    def clear(self):
        self.grid = []


if __name__ == '__main__':
    pass
