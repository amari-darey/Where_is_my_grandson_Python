from uuid import UUID
from collections import deque

from src.world import World
from src.utils import Utils
from src.components import *
from src.constants import *


class EntityFabric:
    @staticmethod
    def get_player(world: World) -> UUID:
        """Создание игрока

        Components entered:
            ComponentPlayer
            ComponentTransform
            ComponentControl
            ComponentSpeed
            ComponentImage
            ComponentAnimation

        Args:
            world (World): экземпляр класса World

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
            ComponentAnimation(deque(entity_animation), PLAYER_ANIMATION_FRAME_RATE, 0)
        )