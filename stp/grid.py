from enum import Enum


class HexagonGridTypes(Enum):
    flat_top: "Flat top"
    pointy_top: "Pointy top"


class Hexagon:
    def __init__(self, q, r, s=None):
        if not s:
            s = -q-r
        self.q = q
        self.r = r
        self.s = s

    def __add__(self, other: 'Hexagon'):
        return Hexagon(self.q + other.q, self.r + other.r, self.s + other.s)

    def __iadd__(self, other):
        self.q += other.q
        self.r += other.r
        self.s += other.s
        return self

    def __sub__(self, other):
        return Hexagon(self.q - other.q, self.r - other.r, self.s - other.s)

    def __isub__(self, other):
        self.q -= other.q
        self.r -= other.r
        self.s -= other.s
        return self

    def __mul__(self, other: int):
        return Hexagon(self.q * other, self.r * other, self.s * other)

    def __imul__(self, other: int):
        self.q *= other
        self.r *= other
        self.s *= other
        return self

    def __eq__(self, other: 'Hexagon'):
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __str__(self):
        return f'Hex(q={self.q}, r={self.r}, s={self.s})'


class HexagonGrid:
    def __init__(self, grid_size: int, grid_type: HexagonGridTypes, hexagon_size: int):
        self.size = grid_size
        self.type = grid_type
        self.hexagon_size = hexagon_size
