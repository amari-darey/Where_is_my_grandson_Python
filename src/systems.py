import pygame

from src.world import World
from src.components import *


class Systems:
    @staticmethod
    def system_draw_entities(world: World, window: pygame.Surface) -> None:
        entities = world.get_entities_with_all(ComponentImage, ComponentTransform)
        for entity in entities:
            transform = world.get_component(entity, ComponentTransform)
            image = world.get_component(entity, ComponentImage)
            window.blit(image.image, (transform.x, transform.y))

    @staticmethod
    def system_animation_update(world: World, dt: int) -> None:
        entities = world.get_entities_with_all(ComponentAnimation)
        for entity in entities:
            animation = world.get_component(entity, ComponentAnimation)
            animation.time_from_last_frame += dt
            if animation.time_from_last_frame >= animation.frame_rate:
                image_component = world.get_component(entity, ComponentImage)
                animation.image.rotate(1)
                animation.time_from_last_frame = 0
                image_component.image = animation.image[0]

    @staticmethod
    def system_player_movement(world: World, key: dict, dt: int) -> None:
        dt = dt / 1000
        entity = world.get_single_entity_with_all(ComponentTransform, ComponentPlayer, ComponentControl)
        control_component = world.get_component(entity, ComponentControl)
        transform_component = world.get_component(entity, ComponentTransform)
        speed_component = world.get_component(entity, ComponentSpeed)

        if key[control_component.up]:
            transform_component.y -= speed_component.speed * dt
        if key[control_component.left]:
            transform_component.x -= speed_component.speed * dt
        if key[control_component.down]:
            transform_component.y += speed_component.speed * dt
        if key[control_component.right]:
            transform_component.x += speed_component.speed * dt

