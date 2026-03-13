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
        if entity_id not in self.__assets: self.__assets[entity_id] = {}
        self.__assets[entity_id][state] = deque(asset)
        

    def get_asset(self, entity_id: UUID, state: Enum) -> tuple[pygame.Surface]:
        return self.__assets[entity_id][state]

