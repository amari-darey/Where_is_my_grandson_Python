from uuid import UUID
from collections import deque

from src.world import World
from src.utils import Utils
from src.assests_manager import AnimationAssets
from src.components import *
from src.constants import *


class EntityFabric:
    @staticmethod
    def create_player(world: World, pos: tuple[int, int]) -> UUID:
        """Создание игрока

        Components entered:
            ComponentPlayer
            ComponentTransform
            ComponentControl
            ComponentSpeed
            ComponentImage
            ComponentDialog
            ComponentAnimation
            ComponentState

        Args:
            world (World): Экземпляр класса World
            pos (tuple[int, int]): позиция зомби в тайлах

        Returns:
            UUID: id игрока
        """
        if world.get_single_entity_with_all(ComponentPlayer): return

        entity = world.create_entity()
        entyti_pos = Utils.tiles_pos_to_world(pos)
        entity_animation = Utils.load_tile_set_with_scale(PLAYER_IDLE_IMG, PLAYER_IDLE_TILESET_SIZE, PLAYER_SIZE)
        entity_dialog_image = Utils.load_tile_set_with_scale(PLAYER_IDLE_IMG, PLAYER_IDLE_TILESET_SIZE, (800, 800))[0]
        world.add_component(
            entity,
            ComponentPlayer(),
            ComponentTransform(*entyti_pos, *PLAYER_SIZE),
            ComponentControl(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE),
            ComponentSpeed(PLAYER_SPEED),
            ComponentImage(entity_animation[0]),
            ComponentDialog(PLAYER_NAME, entity_dialog_image),
            ComponentAnimation(PLAYER_ANIMATION_FRAME_RATE, 0),
            ComponentState(PLAYER_START_STATE, None, type(PLAYER_START_STATE))
        )

        for state in PLAYER_STATES:
            Utils.load_animations(entity, state)

        return entity
    
    @staticmethod
    def create_zombie(world: World, pos: tuple[int, int]) -> UUID:
        """Создание зомби

        Components entered:
            ComponentEnemy
            ComponentZombie
            ComponentTransform
            ComponentImage
            ComponentAnimation
            ComponentState

        Args:
            world (World): Экземпляр класса World
            pos (tuple[int, int]): позиция зомби в тайлах

        Returns:
            UUID: id зомби
        """
        entity = world.create_entity()
        entyti_pos = Utils.tiles_pos_to_world(pos)
        entity_animation = Utils.load_tile_set_with_scale(ZOMBIE_IDLE_IMG, ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE)
        world.add_component(
            entity,
            ComponentEnemy(),
            ComponentZombie(),
            ComponentTransform(*entyti_pos, *ZOMBIE_SIZE),
            ComponentImage(entity_animation[0]),
            ComponentAnimation(ZOMBIE_ANIMATION_FRAME_RATE, 0),
            ComponentState(ZOMBIE_START_STATE, None, type(ZOMBIE_START_STATE))
        )

        for state in ZOMBIE_STATES:
            Utils.load_animations(entity, state)

        return entity


    