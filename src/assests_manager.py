import pygame
from uuid import UUID
from enum import Enum
from collections import deque


class AnimationAssets:
    instance = None
    __assets = {}
    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def add_asset(self, entity_id: UUID, state: Enum, asset: tuple[pygame.Surface]) -> None:
        """Добавление ассета

        Args:
            entity_id (UUID): id сущности которой будет принадлежать ассет
            state (Enum): состояние к которому привязан ассет
            asset (tuple[pygame.Surface]): кортеж из surface которые представляют собой анимацию
        """
        if entity_id not in self.__assets: self.__assets[entity_id] = {}
        self.__assets[entity_id][state] = deque(asset)
        

    def get_asset(self, entity_id: UUID, state: Enum) -> deque[pygame.Surface]:
        """Получить ассет

        Args:
            entity_id (UUID): id сущности к которой привязан ассет
            state (Enum): состояние для которого нужен ассет

        Returns:
            deque[pygame.Surface]: Очередь из surface
        """
        return self.__assets[entity_id][state]

