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
        cord_xy = self.pos[0] + hex.pos[0] * rv + hex.pos[1] * rv * math.cos(alfa) + hex.pos[2] * rv * math.cos(alfa * 2), \
                  self.pos[1] - hex.pos[1] * rv * math.sin(alfa) - hex.pos[2] * rv * math.sin(alfa * 2)
        return cord_xy

    def clear(self):
        self.grid = []

    #
    # def create_start_point_way(position_start, radius):
    #     array_s = []
    #     t = HEX_SIZE / radius
    #     n = int(radius / (2 * HEX_SIZE)) + 1
    #     i = 0
    #     while i < math.pi / 2:
    #         for j in range(0, n + 1):
    #             l1 = radius * j / n
    #             array_s.append(test_click((position_start[0] + l1 * math.cos(i), position_start[1] - l1 * math.sin(i))))
    #         i += t
    #     array_s = [i for i in array_s if i != None]
    #     array_s = delete_duplicate(array_s)
    #     return array_s
    #
    # def create_end_point_way(position_end, radius):
    #     array_s = []
    #     t = HEX_SIZE / radius
    #     n = int(radius / (2 * HEX_SIZE)) + 1
    #     i = 0
    #     while i < math.pi / 2:
    #         for j in range(0, n + 1):
    #             l1 = radius * j / n
    #             array_s.append(test_click((position_end[0] - l1 * math.cos(i), position_end[1] + l1 * math.sin(i))))
    #         i += t
    #     array_s = [i for i in array_s if i != None]
    #     array_s = delete_duplicate(array_s)
    #     return array_s
    #
    # def create_wall(start_point, end_point):  # ??
    #     a = HEX_SIZE
    #     b = 3 ** (1 / 2)
    #     wall = []
    #     for x in range(start_point[0], end_point[0] + int(a * b), int(a * b) // 3):
    #         wall.append(search_long_hex(hexsagons_point_center, (x, 0)))
    #         if random.randint(0, 10) % 5 == 1:
    #             wall.append(search_long_hex(hexsagons_point_center, (x, a * b)))
    #             if random.randint(0, 10) == 1:
    #                 wall.append(search_long_hex(hexsagons_point_center, (x, 2 * a * b)))
    #
    #     for x in range(start_point[0], end_point[0] + int(a * b), int(a * b) // 3):
    #         wall.append(search_long_hex(hexsagons_point_center, (x, SCREEN_HEIGHT - 1)))
    #         if random.randint(0, 10) % 5 == 1:
    #             wall.append(search_long_hex(hexsagons_point_center, (x, SCREEN_HEIGHT - a * b / 2)))
    #             if random.randint(0, 10) == 1:
    #                 wall.append(search_long_hex(hexsagons_point_center, (x, SCREEN_HEIGHT - a * b)))
    #
    #     for y in range(start_point[1], end_point[1] + int(a * b), int(a * b) // 3):
    #         wall.append(search_long_hex(hexsagons_point_center, (0, y)))
    #         if random.randint(0, 10) == 1:
    #             wall.append(search_long_hex(hexsagons_point_center, (a * b, y)))
    #
    #     for y in range(start_point[1], end_point[1] + int(a * b), int(a * b) // 3):
    #         wall.append(search_long_hex(hexsagons_point_center, (SCREEN_WIDTH, y)))
    #         if random.randint(0, 10) == 1:
    #             wall.append(search_long_hex(hexsagons_point_center, (SCREEN_WIDTH - a * b / 2, y)))
    #
    #     wall = [i for i in wall if i != None]
    #     wall = delete_duplicate(wall)
    #     wall = [i for i in wall if i not in start_point_way_array]
    #     wall = [i for i in wall if i not in end_point_way_array]
    #     return wall
    #
    # def search_long_hex(center_hex, point):  # возвращает ближайший гексагон (номер) к point
    #     for center in center_hex:
    #         if distance(center, point) <= HEX_SIZE + 1:
    #             hex_number.add(center_hex.index(center))
    #             return center_hex.index(center)
    #
    # def test_click(position):
    #     flag = search_long_hex(hexsagons_point_center, position)
    #     if flag != None:
    #         return flag
    #
    # def create_checkpoint_enemy():
    #     Nw = SCREEN_WIDTH / (HEX_SIZE * (3 ** (1 / 2)))
    #     Nh = SCREEN_HEIGHT / (2 * HEX_SIZE)
    #     hw = HEX_SIZE * 3 ** (1 / 2)
    #     hh = HEX_SIZE * 2
    #     center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    #     vector_array = []
    #     vector_array_n = []
    #     hex_edge = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
    #     point_edge = [
    #         (SCREEN_WIDTH / 2, (Nh - 3) * hh),
    #         (SCREEN_WIDTH / 2, 3 * hh),
    #         (3 * hw, 3 * hh),
    #         ((Nw - 3) * hw, (Nh - 3) * hh),
    #         ((Nw - 3) * hw, SCREEN_HEIGHT / 2),
    #         (3 * hh, SCREEN_HEIGHT / 2)]
    #     for i, point in enumerate(point_edge):
    #         hex_edge[i].append(test_click(point))
    #     for i, point in enumerate(point_edge):
    #         vector_array.append((sig(point[0] - center[0]), sig(point[1] - center[1])))
    #         vector_array_n.append((vector_array[i][1], -vector_array[i][0]))
    #     for i, number in enumerate(hex_edge):
    #         point_edge[i] = hexsagons_point_center[hex_edge[number][0]]
    #     for i, point in enumerate(point_edge):
    #         point_start = point[0] - (HEX_SIZE / 2) * vector_array[i][0], point[1] - (HEX_SIZE / 2) * vector_array[i][1]
    #         if i != 0:
    #             point_middle = point_start[0] - HEX_SIZE * vector_array_n[i][0] - (HEX_SIZE / 3) * vector_array[i][0], \
    #                            point_start[1] - HEX_SIZE * vector_array_n[i][1] - (HEX_SIZE / 3) * vector_array[i][1]
    #         else:
    #             point_middle = point_start[0] - HEX_SIZE * vector_array_n[i][0] - HEX_SIZE * vector_array[i][0], \
    #                            point_start[1] + HEX_SIZE / 2
    #         hex_edge[i].append(test_click(point_middle))
    #         point_end = point[0] - (HEX_SIZE * 1.5) * vector_array[i][0], point[1] - (HEX_SIZE * 1.5) * vector_array[i][
    #             1]
    #         hex_edge[i].append(test_click(point_end))
    #     return hex_edge
    #
    # def search_number_position(hex_group):
    #     # print(hexsagons_point_center[hex_group[0]][0], hexsagons_point_center[hex_group[1]][0], hexsagons_point_center[hex_group[2]][0])
    #     # print(hexsagons_point_center[hex_group[0]][1], hexsagons_point_center[hex_group[1]][1], hexsagons_point_center[hex_group[2]][1])
    #
    #     cord_x = (hexsagons_point_center[hex_group[0]][0] + hexsagons_point_center[hex_group[1]][0] +
    #               hexsagons_point_center[hex_group[2]][0]) / 3
    #
    #     if int(hexsagons_point_center[hex_group[0]][1]) == int(hexsagons_point_center[hex_group[1]][1]):
    #         cord_y = (hexsagons_point_center[hex_group[0]][1] + hexsagons_point_center[hex_group[2]][1]) / 2
    #     else:
    #         cord_y = (hexsagons_point_center[hex_group[0]][1] + hexsagons_point_center[hex_group[1]][1]) / 2
    #
    #     cord = cord_x, cord_y
    #     return cord
    #
    # def garf_friend(hex_number):
    #     a = HEX_SIZE
    #     alfa = math.pi / 3
    #     cord = hexsagons_point_center[hex_number]
    #     array_friend = [search_long_hex(hexsagons_point_center, (cord[0] + a * 3 ** (1 / 2), cord[1])),
    #                     search_long_hex(hexsagons_point_center, (
    #                         cord[0] + a * 3 ** (1 / 2) * math.cos(alfa), cord[1] - a * 3 ** (1 / 2) * math.sin(alfa))),
    #                     search_long_hex(hexsagons_point_center, (cord[0] + a * 3 ** (1 / 2) * math.cos(alfa * 2),
    #                                                              cord[1] - a * 3 ** (1 / 2) * math.sin(alfa * 2))),
    #                     search_long_hex(hexsagons_point_center, (cord[0] - a * 3 ** (1 / 2), cord[1])),
    #                     search_long_hex(hexsagons_point_center, (cord[0] + a * 3 ** (1 / 2) * math.cos(alfa * 4),
    #                                                              cord[1] - a * 3 ** (1 / 2) * math.sin(alfa * 4))),
    #                     search_long_hex(hexsagons_point_center, (cord[0] + a * 3 ** (1 / 2) * math.cos(alfa * 5),
    #                                                              cord[1] - a * 3 ** (1 / 2) * math.sin(alfa * 5)))]
    #     array_friend = [j for j in array_friend if j != None]
    #     array_friend = [j for j in array_friend if j not in default_wall]
    #     return array_friend
    #
    # def create_graf_way():
    #     graf_decstr = {}
    #     a = HEX_SIZE
    #     alfa = math.pi / 3
    #     for i in hexsagons_point_center:
    #         search_long_hex(hexsagons_point_center, i)
    #     # print(hex_number, len(hex_number))
    #     for i in hex_number:
    #         cord = hexsagons_point_center[i]
    #         array_friend = [search_long_hex(hexsagons_point_center, (cord[0] + a * 3 ** (1 / 2), cord[1])),
    #                         search_long_hex(hexsagons_point_center, (
    #                             cord[0] + a * 3 ** (1 / 2) * math.cos(alfa),
    #                             cord[1] - a * 3 ** (1 / 2) * math.sin(alfa))),
    #                         search_long_hex(hexsagons_point_center, (cord[0] + a * 3 ** (1 / 2) * math.cos(alfa * 2),
    #                                                                  cord[1] - a * 3 ** (1 / 2) * math.sin(alfa * 2))),
    #                         search_long_hex(hexsagons_point_center, (cord[0] - a * 3 ** (1 / 2), cord[1])),
    #                         search_long_hex(hexsagons_point_center, (cord[0] + a * 3 ** (1 / 2) * math.cos(alfa * 4),
    #                                                                  cord[1] - a * 3 ** (1 / 2) * math.sin(alfa * 4))),
    #                         search_long_hex(hexsagons_point_center, (cord[0] + a * 3 ** (1 / 2) * math.cos(alfa * 5),
    #                                                                  cord[1] - a * 3 ** (1 / 2) * math.sin(alfa * 5)))]
    #         array_friend = [j for j in array_friend if j != None]
    #         array_friend = [j for j in array_friend if j not in default_wall]
    #         graf_decstr[i] = array_friend
    #
    #     return graf_decstr
