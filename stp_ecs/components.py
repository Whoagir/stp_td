from pygame import Surface, Rect
from dataclasses import dataclass as component


@component
class PositionComponent:
    x: float = 0.0
    y: float = 0.0


@component
class RenderComponent:
    image: Surface = None
    rect: Rect = None
