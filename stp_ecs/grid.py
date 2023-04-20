from enum import Enum
from typing import Tuple
from math import cos, sin, pi


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

    def __str__(self):
        return f'Hex(q={self.q}, r={self.r}, s={self.s})'

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


class HexagonGrid:
    def __init__(self, grid_type: HexagonGridTypes):
        self.type = grid_type
        self.hexes = []

    @staticmethod
    def generate_hex(grid_size: int) -> list[Hexagon]:
        result = []
        for q in range(-grid_size, grid_size + 1):
            r1 = max(-grid_size, -q - grid_size)
            r2 = min(grid_size, -q + grid_size)
            for r in range(r1, r2 + 1):
                result.append(Hexagon(q, r, -q - r))
        return result

    def hex_to_pixel(self, hexagon: Hexagon, hexagon_size: float) -> Tuple[float, float]:
        x = (hexagon.q * HexToPixelMatrix[self.type.value][0][0] +
             hexagon.r * HexToPixelMatrix[self.type.value][0][1]) * hexagon_size
        y = (hexagon.q * HexToPixelMatrix[self.type.value][1][0] +
             hexagon.r * HexToPixelMatrix[self.type.value][1][1]) * hexagon_size
        return x, y

    def pixel_to_hex(self, pos: Tuple[float, float], hexagon_size: float) -> Hexagon:
        pt = (pos[0] / hexagon_size, pos[1] / hexagon_size)
        q = pt[0] * PixelToHexMatrix[self.type.value][0][0] + pt[1] * PixelToHexMatrix[self.type.value][0][1]
        r = pt[0] * PixelToHexMatrix[self.type.value][1][0] + pt[1] * PixelToHexMatrix[self.type.value][1][1]
        return Hexagon(round(q), round(r), -round(q) - round(r))

    def get_hexagon_edges(self, hexagon: 'Hexagon', hexagon_size: float):
        alpha = pi / 3
        pos = self.hex_to_pixel(hexagon, hexagon_size)
        for i in range(6):
            yield ((pos[0] + hexagon_size * cos(i * alpha + alpha / 2),
                    pos[1] + hexagon_size * sin(i * alpha + alpha / 2)),
                   (pos[0] + hexagon_size * cos((i + 1) * alpha + alpha / 2),
                    pos[1] + hexagon_size * sin((i + 1) * alpha + alpha / 2)))


if __name__ == '__main__':
    g = HexagonGrid(grid_type=HexagonGridTypes.flat_top)
    g.generate_hex(grid_size=12)
    h = g.hexes[0]
    q = g.hex_to_pixel(h, 12)
    w = g.pixel_to_hex(q, 12)
    print(h, q, w)
