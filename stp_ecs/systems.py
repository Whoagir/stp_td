from esper import Processor
import pygame.display

from components import *
from presets import create_sprite_entity, empty_floor_preset


class MovementProcessor(Processor):
    def process(self):
        for ent, (pos, vel) in self.world.get_components(PositionComponent, VelocityComponent):
            pos.x, pos.y = pygame.Vector2(pos.x, pos.y) + pygame.Vector2(vel.x, vel.y)


class RenderProcessor(Processor):
    def __init__(self, surface: Surface, clear_color=(0, 0, 0)):
        self.surface = surface
        self.clear_color = clear_color

    def process(self, *args, **kwargs):
        self.surface.fill(self.clear_color)
        for ent, (sprite, pos) in self.world.get_components(SpriteComponent, PositionComponent):
            if not sprite.rect:
                sprite.rect = sprite.image.get_rect()
            sprite.rect.topleft = (pos.x - sprite.origin[0], pos.y - sprite.origin[1])
            self.surface.blit(sprite.image, sprite.rect)
        pygame.display.flip()


class CollideProcessor(Processor):
    def process(self):
        for ent, (pos, collider) in self.world.get_components(PositionComponent,
                                                              ColliderComponent):
            for enemy_ent, (enemy_pos, enemy_collider) in self.world.get_components(PositionComponent,
                                                                                    ColliderComponent):
                if ent == enemy_ent:
                    continue
                if pygame.Vector2(pos.x, pos.y).distance_to(pygame.Vector2(enemy_pos.x, enemy_pos.y)) < \
                        collider.radius + enemy_collider.radius:
                    self.world.add_component(ent, CollisionComponent(entity=enemy_ent))


class CollisionProcessor(Processor):
    def process(self):
        for ent, (collision,) in self.world.get_components(CollisionComponent):
            print(f'{ent} collide with {collision.entity}')


class MouseClickProcessor(Processor):
    def process(self):
        for ent, (click,) in self.world.get_components(MouseClickComponent):
            self.world.remove_component(ent, MouseClickComponent)
            create_sprite_entity(self.world, empty_floor_preset, (click.x, click.y))


class RenderWithLayerProcessor(Processor):
    def process(self):
        for ent, (layer, sprite, pos) in self.world.get_components(LayerComponent, SpriteComponent, PositionComponent):
            for i in range(5):
                if layer.layer == i:
                    print('render sprite')


class DamageHandlerProcessor(Processor):
    def process(self):
        for ent, (hp, damage) in self.world.get_components(HealthPointsComponent, TakeEnemyDamageComponent):
            hp.hp -= damage.damage


class EffectHandlerProcessor(Processor):
    def process(self):
        pass