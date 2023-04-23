from enum import Enum
from typing import Tuple
from queue import Queue


def lerp(a: float, b: float, t: float):
    if t < 0:
        t = 0
    if t > 1:
        t = 1
    return a + (b - a) * t


class HexagonGridTypes(Enum):
    flat_top = "flat_top"
    pointy_top = "pointy_top"


HexToPixelMatrix = {
    'pointy_top': ((3 ** 0.5, 3 ** 0.5 / 2),
                   (0, 3 / 2)),
    'flat_top': ((3 / 2, 0),
                 (3 ** 0.5 / 2, 3 ** 0.5))
}

PixelToHexMatrix = {
    'pointy_top': ((3 ** 0.5 / 3, -1 / 3),
                   (0, 2 / 3)),
    'flat_top': ((2 / 3, 0),
                 (-1 / 3, 3 ** 0.5 / 3))
}


class Hexagon:
    def __init__(self, q: int, r: int, s: int = None):
        if not s:
            s = -q - r
        self.q = q
        self.r = r
        self.s = s

    def __iter__(self):
        return [self.q, self.r, self.s]

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise KeyError('Key can only be an int.')
        return [self.q, self.r, self.s][key]

    def __add__(self, other: 'Hexagon') -> 'Hexagon':
        return Hexagon(self.q + other.q, self.r + other.r, self.s + other.s)

    def __iadd__(self, other: 'Hexagon') -> 'Hexagon':
        self.q += other.q
        self.r += other.r
        self.s += other.s
        return self

    def __sub__(self, other: 'Hexagon') -> 'Hexagon':
        return Hexagon(self.q - other.q, self.r - other.r, self.s - other.s)

    def __isub__(self, other: 'Hexagon') -> 'Hexagon':
        self.q -= other.q
        self.r -= other.r
        self.s -= other.s
        return self

    def __mul__(self, other: int) -> 'Hexagon':
        return Hexagon(self.q * other, self.r * other, self.s * other)

    def __imul__(self, other: int) -> 'Hexagon':
        self.q *= other
        self.r *= other
        self.s *= other
        return self

    def __eq__(self, other: 'Hexagon') -> bool:
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __hash__(self):
        return hash((self.q, self.r, self.s))

    def __str__(self):
        return f'Hex(q={self.q}, r={self.r}, s={self.s})'

    def __repr__(self):
        return self.__str__()

    def distance_to(self, hexagon: 'Hexagon'):
        vec = self - hexagon
        return (abs(vec.q) + abs(vec.r) + abs(vec.s)) / 2


def generate_hex_grid(grid_size: int) -> list[Hexagon]:
    result = []
    for q in range(-grid_size, grid_size + 1):
        r1 = max(-grid_size, -q - grid_size)
        r2 = min(grid_size, -q + grid_size)
        for r in range(r1, r2 + 1):
            result.append(Hexagon(q, r, -q - r))
    return result


def hex_to_pixel(grid_type: HexagonGridTypes,
                 hexagon: Hexagon,
                 hexagon_size: float) -> Tuple[float, float]:
    x = (hexagon.q * HexToPixelMatrix[grid_type.value][0][0] +
         hexagon.r * HexToPixelMatrix[grid_type.value][0][1]) * hexagon_size
    y = (hexagon.q * HexToPixelMatrix[grid_type.value][1][0] +
         hexagon.r * HexToPixelMatrix[grid_type.value][1][1]) * hexagon_size
    return x, y


def pixel_to_hex(grid_type: HexagonGridTypes,
                 pos: Tuple[float, float],
                 hexagon_size: float) -> Hexagon:
    pt = (pos[0] / hexagon_size, pos[1] / hexagon_size)
    q = pt[0] * PixelToHexMatrix[grid_type.value][0][0] + pt[1] * PixelToHexMatrix[grid_type.value][0][1]
    r = pt[0] * PixelToHexMatrix[grid_type.value][1][0] + pt[1] * PixelToHexMatrix[grid_type.value][1][1]
    return Hexagon(round(q), round(r), -round(q) - round(r))


def get_neighbors(hexagon: Hexagon) -> list[Hexagon]:
    result = []
    neighbors_pos = [[1, -1, 0], [1, 0, -1], [0, 1, -1], [-1, 1, 0], [-1, 0, 1], [0, -1, 1]]
    for i in neighbors_pos:
        result.append(hexagon + Hexagon(*i))
    return result


def get_path(obstacles: list[Hexagon], start: Hexagon, end: Hexagon) -> list[Hexagon]:
    frontier = Queue()
    frontier.put(start)
    came_from = dict()
    came_from[start] = None

    while not frontier.empty():
        current = frontier.get()

        if current == end:
            break

        for next in get_neighbors(current):
            if next in obstacles:
                continue
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    q = []
    e = end
    while e is not None:
        q.append(e)
        e = came_from[e]
    return q


if __name__ == '__main__':
    q = Hexagon(0, 0, 0)
    print(get_neighbors(q))
    obstacles = [Hexagon(1, -1, 0), Hexagon(2, -1, -1), Hexagon(2, 0, -2), Hexagon(1, 1, -2), Hexagon(1, 1, -2), Hexagon(0, 2, -2)]
    start = Hexagon(0, 0, 0)
    end = Hexagon(3, 0, -3)
    get_path(obstacles, start, end)
