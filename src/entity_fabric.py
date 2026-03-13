from uuid import UUID
from collections import deque

from src.world import World
from src.utils import Utils
from src.assests_manager import AnimationAssets
from src.components import *
from src.constants import *


class EntityFabric:
    @staticmethod
    def get_player(world: World, player_pos: tuple[int, int]) -> UUID:
        """Создание игрока

        Components entered:
            ComponentPlayer
            ComponentTransform
            ComponentControl
            ComponentSpeed
            ComponentImage
            ComponentAnimation

        Args:
            world (World): Экземпляр класса World
            player_pos (tuple[int, int]): Позиция игрока в тайлах

        Returns:
            UUID: id игрока
        """
        entity = world.create_entity()
        entity_animation = Utils.load_tile_set_with_scale(PLAYER_IDLE_IMG, PLAYER_IDLE_TILESET_SIZE, PLAYER_SIZE)
        world.add_component(
            entity,
            ComponentPlayer(),
            ComponentTransform(*PLAYER_POS, *PLAYER_SIZE),
            ComponentControl(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE),
            ComponentSpeed(PLAYER_SPEED),
            ComponentImage(entity_animation[0]),
            ComponentAnimation(PLAYER_ANIMATION_FRAME_RATE, 0),
            ComponentState(PLAYER_START_STATE, None, type(PLAYER_START_STATE))
        )

        for state in PLAYER_STATES:
            Utils.load_animations(entity, state)

        return entity

    