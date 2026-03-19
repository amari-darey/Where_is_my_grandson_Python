import pygame
from uuid import UUID

from src.world import World
from src.components import *
from config.camera import CAMERA_SMOOTH


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

    def update(self, world: World, target: UUID, game_map: pygame. Surface, smooth: float = CAMERA_SMOOTH) -> None:
        """Обновляет офсет камеры, относительно target.  
        target остаётся в центре камеры.

        Args:
            world (World): экземпляр класса World
            target (UUID): id сущности
            game_map (pygame.Surface): Карта
            smooth (float): Плавность движения камеры
        """
        target_transform = world.get_component(target, ComponentTransform)
        target_rect = target_transform.rect
        map_width, map_height = game_map.get_size()
        
        target_x = max(0, target_rect.centerx - self.__center_x)
        target_y = max(0, target_rect.centery - self.__center_y)
        target_x = min(target_x, map_width - self.width)
        target_y = min(target_y, map_height - self.height)

        self.ofset_x += (target_x - self.ofset_x) * smooth
        self.ofset_y += (target_y - self.ofset_y) * smooth

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