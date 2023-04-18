from pygame import Surface
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
    def __init__(self, image: Surface = Surface([0, 0])):
        self.image = image
