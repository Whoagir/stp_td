import enum


class EnemyEffectType(enum.Enum):
    base = 0


class AlliesEffectType(enum.Enum):
    base = 0


class DamageType(enum.Enum):
    basic = 0
    chaos = 1
    phisical = 2
    magic = 3
    siege = 4

class ArmorType(enum.Enum):
    basic = 0