from typing import Tuple
from esper import World

from sprite_preset import SpritePreset
from components import PositionComponent, SpriteComponent
from config import ASSETS_DIR


def create_sprite_entity(world: World,
                         sprite_preset: SpritePreset,
                         pos: Tuple[float, float] = (0, 0)):
    entity = world.create_entity()
    world.add_component(entity, PositionComponent(x=pos[0], y=pos[1]))
    img = sprite_preset.image
    rect = sprite_preset.image.get_rect()
    world.add_component(entity, SpriteComponent(image=img, rect=rect, origin=sprite_preset.origin))
    return entity


player_preset = SpritePreset(ASSETS_DIR / 'images' / 'hex.png', scale_factor=(1, 1))
empty_floor_preset = SpritePreset(ASSETS_DIR / 'images' / 'empty_floor.png', scale_factor=(1, 1), origin=(0, 0))
red_floor_preset = SpritePreset(ASSETS_DIR / 'images' / 'red_floor.png', scale_factor=(1, 1))
green_floor_preset = SpritePreset(ASSETS_DIR / 'images' / 'green_floor.png', scale_factor=(1, 1))
purpul_floor_preset = SpritePreset(ASSETS_DIR / 'images' / 'purpul_floor.png', scale_factor=(1, 1))
enemy_preset = SpritePreset(ASSETS_DIR / 'images' / 'enemy.png', scale_factor=(1, 1))
