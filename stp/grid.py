from enum import Enum
from typing import Tuple


def lerp(a: float, b: float, t: float):
    if t < 0:
        t = 0
    if t > 1:
        t = 1
    return a + (b-a) * t


class HexagonGridTypes(Enum):
    hex_flat_top = "Hex flat top"
    hex_pointy_top = "Hex pointy top"
    rect = "Rect"


class Hexagon:
    def __init__(self, q: int, r: int, s: int = None):
        if not s:
            s = -q-r
        self.q = q
        self.r = r
        self.s = s

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


class HexagonGrid:
    def __init__(self, grid_size: int, grid_type: HexagonGridTypes, hexagon_size: int, offset: Tuple[float, float] = (0, 0)):
        self.offset = offset
        self.size = grid_size
        self.type = grid_type
        self.hexagon_size = hexagon_size
        self._hexes = []

    def _generate_hex(self):
        for q in range(-self.size, self.size + 1):
            r1 = max(-self.size, -q - self.size)
            r2 = min(self.size, -q + self.size)
            for r in range(r1, r2 + 1):
                self._hexes.append(Hexagon(q, r, -q - r))

    def _generate_rect(self):
        pass

    def local_to_global(self, hexagon: Hexagon):
        pass

    def global_to_local(self, x: float, y: float):
        pass

    def lerp(self, a_hex: Hexagon, b_hex: Hexagon, t: float):
        if t < 0:
            t = 0
        if t > 1:
            t = 1


if __name__ == '__main__':
    pass
