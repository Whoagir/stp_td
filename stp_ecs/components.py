from typing import Tuple
from pygame import Surface, Rect
from dataclasses import dataclass as component
from dataclasses import field

from grid import Hexagon
from constant import *


@component
class PositionComponent:
    x: float = 0.0
    y: float = 0.0


@component
class VelocityComponent:
    x: float = 0.0
    y: float = 0.0


@component
class SpriteComponent:
    image: Surface = field(default_factory=lambda _: Surface([0, 0]))
    rect: Rect = None
    origin: Tuple[float, float] = (0, 0)


@component
class ColliderComponent:
    radius: float = 0.0


@component
class CollisionComponent:
    entity: int = None


@component
class MouseClickComponent:
    x: float = 0.0
    y: float = 0.0


@component
class LayerComponent:
    layer: int = 0


@component
class HexagonComponent:
    hexagon: Hexagon = None


@component
class EnemyComponent:
    pass


@component
class TowerComponent:
    pass


@component
class FlyEnemyComponent:
    pass


@component
class TakeDamageComponent:
    damage: float = 0.0


@component
class EnemyEffectComponent:
    effect: EnemyEffectType = EnemyEffectType.base


@component
class AlliesEffectComponent:
    effect: AlliesEffectType = AlliesEffectType.base


@component
class HealthPointsComponent:
    value: int = 0


@component
class PathfindingComponent:
    pass
