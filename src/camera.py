import pygame
from uuid import UUID

from src.world import World
from src.components import *


class Camera:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.ofset_x = 0
        self.ofset_y = 0

        self.__center_x = width // 2
        self.__center_y = height // 2

    def update(self, world: World, target: UUID, game_map: pygame. Surface) -> None:
        """Обновляет офсет камеры, относительно target.
        target остаётся в центре камеры.

        Args:
            world (World): экземпляр класса World
            target (UUID): id сущности
            game_map (pygame.Surface): Карта
        """
        target_transform = world.get_component(target, ComponentTransform)
        target_rect = target_transform.rect
        map_width, map_height = game_map.get_size()
        
        ofset_x = max(0, target_rect.centerx - self.__center_x)
        ofset_y = max(0, target_rect.centery - self.__center_y)
        self.ofset_x = min(ofset_x, map_width - self.width)
        self.ofset_y = min(ofset_y, map_height - self.height)

    def cordinate_world_to_screen(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Перевод кординат из мировых в кординаты относительно камеры

        Args:
            pos (tuple[int, int]): Текущая позиция в мировых кординатах

        Returns:
            tuple[int, int]: Итоговая позиция
        """
        return pos[0] - self.ofset_x, pos[1] - self.ofset_y

    def cordinate_screen_to_world(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Перевод из кординат камеры в мировые кординаты
        Args:
            pos (tuple[int, int]): Текущая позиция в кординатах камеры

        Returns:
            tuple[int, int]: Итоговая позиция
        """
        return pos[0] + self.ofset_x, pos[1] + self.ofset_y