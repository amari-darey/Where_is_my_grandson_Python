import pygame

from src.world import World
from src.assests_manager import AnimationAssets
from src.components import *


class Systems:
    @staticmethod
    def system_draw_entities(world: World, window: pygame.Surface) -> None:
        """Система отрисовки сущностей
        Отрисовывает все сущности содержащие компоненты ComponentImage, ComponentTransform

        Args:
            world (World): экземпляр класса World
            window (pygame.Surface): Surface экрана
        """
        entities = world.get_entities_with_all(ComponentImage, ComponentTransform)
        for entity in entities:
            transform = world.get_component(entity, ComponentTransform)
            image = world.get_component(entity, ComponentImage)
            window.blit(image.image, (transform.x, transform.y))

    @staticmethod
    def system_animation_update(world: World, animation_assets: AnimationAssets, dt: int) -> None:
        """Обновление анимации
        Если время с последней анимации больше чем frame_rate то в ComponentImage записывается новое изображение

        Args:
            world (World): экземпляр класса World
            dt (int): количество миллисекунд с последнего кадра
        """
        entities = world.get_entities_with_all(ComponentAnimation, ComponentImage)
        for entity in entities:
            animation = world.get_component(entity, ComponentAnimation)
            animation.time_from_last_frame += dt
            if animation.time_from_last_frame >= animation.frame_rate:
                image_component = world.get_component(entity, ComponentImage)
                state = world.get_component(entity, ComponentState)
                asset = animation_assets.get_asset(entity, state.current_state)
                asset.rotate(1)
                animation.time_from_last_frame = 0
                image_component.image = asset[0]

    @staticmethod
    def system_player_movement(world: World, key: dict, dt: int) -> None:
        """Передвижение персонажа

        Args:
            world (World): экземпляр класса World
            key (dict): Словарь нажатых клавишь (pygame.key.get_pressed())
            dt (int): количество миллисекунд с последнего кадра
        """
        dt = dt / 1000
        entity = world.get_single_entity_with_all(ComponentTransform, ComponentPlayer, ComponentControl, ComponentState)
        control_component = world.get_component(entity, ComponentControl)
        transform_component = world.get_component(entity, ComponentTransform)
        speed_component = world.get_component(entity, ComponentSpeed)
        state_component = world.get_component(entity, ComponentState)
        dx = dy = 0
        if key[control_component.left]:
            dx -= speed_component.speed * dt
        if key[control_component.right]:
            dx += speed_component.speed * dt
        if key[control_component.up]:
            dy -= speed_component.speed * dt
        if key[control_component.down]:
            dy += speed_component.speed * dt

        transform_component.x += dx
        transform_component.y += dy
        
        if dx != 0:
            state_component.previous_state = state_component.current_state
            if dx > 0:
                state_component.current_state = state_component.all_states.WALK_RIGHT
            else:
                state_component.current_state = state_component.all_states.WALK_LEFT
        if not dx and not dy:
            state_component.previous_state = state_component.current_state
            if state_component.current_state == state_component.all_states.WALK_LEFT:
                state_component.current_state = state_component.all_states.IDLE_LEFT
            elif state_component.current_state == state_component.all_states.WALK_RIGHT:
                state_component.current_state = state_component.all_states.IDLE_RIGHT



