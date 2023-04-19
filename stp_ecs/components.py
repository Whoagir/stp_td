from typing import Tuple
from pygame import Surface, Rect
from dataclasses import dataclass as component


@component
class PositionComponent:
    x: float = 0.0
    y: float = 0.0


@component
class VelocityComponent:
    x: float = 0.0
    y: float = 0.0


class SpriteComponent:
    def __init__(self,
                 image: Surface = Surface([0, 0]),
                 rect: Rect = None,
                 origin: Tuple[float, float] = (0, 0)):
        self.image = image
        self.rect = rect
        self.origin = origin


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
