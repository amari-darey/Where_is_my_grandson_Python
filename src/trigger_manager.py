import pygame
from typing import Callable, Any
from uuid import uuid1, UUID
from functools import partial

from src.world import World
from src.components import *
from config.tiles import *


class TriggerManager:
    """Менеджер триггеров  
    Структура хранения:  
    ``` python
    {
        "touch": {
            UUID: {
                "rect": pygame.Rect, # Рект для сравнения позиция
                "callback": Callable, # Коллбэк для вызова
                "param": tuple[Any], # Кортеж параметров которые будут переданны в коллбэк при вызове
                "allow_entity": tuple[Component], # Кортеж с типами сущностей которые могут вызвать триггер
                "repeat": bool # Удаляется ли триггер после срабатывания
            }
        },
        "time": {
            UUID: {
                "time": int, # колличество миллисекунд с начала игры до срабатывания триггера
                "callback": Callable, # Коллбэк для вызова
                "param": tuple[Any], # Кортеж параметров которые будут переданны в коллбэк при вызове
                "repeat": False # У time триггеров всегда False
            }
        }
    }
    ```
    """
    def __init__(self):
        self.__triggers = {}
        self.__triggers["touch"] = {}
        self.__triggers["time"] = {}
        self.__timer = 0

    def create_touch_trigger(
            self, pos: tuple[int, int], size: tuple[int, int], 
            callback: partial, entity_type: tuple[Component], repeat: bool
            ) -> UUID:
        """Создание триггер зоны

        Args:
            pos (tuple[int, int]): Позиция треггера в тайлах
            size (tuple[int, int]): Размер триггера в тайлах
            callback (partial): Коллбэк, который будет вызван при срабатывании
            entity_type (tuple[Component]): Кортеж с типами сущностей которые могут вызвать триггер
            repeat (bool): Удаляется ли триггер после срабатывания

        Allow entity type:
            ComponentPlayer
            ComponentEnemy
            ComponentZombie

        Returns:
            UUID: id триггера
        """

        trigger_id = uuid1()
        pos_x, pos_y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        size_w, size_h = size[0] * TILE_SIZE, size[1] * TILE_SIZE
        trigger_rect = pygame.Rect(pos_x, pos_y, size_w, size_h)
        self.__triggers["touch"][trigger_id] = {
            "rect": trigger_rect,
            "callback": callback,
            "allow_entity": entity_type,
            "repeat": repeat
        }

        return trigger_id

    def create_time_trigger(self, time: int, callback: partial) -> UUID:
        """Создание триггера по времени

        Args:
            time (int): Время в миллисекундах с начала игры, когда должен сработать триггер
            callback (partial): Коллбэк, который будет вызван при срабатывании

        Returns:
            UUID: id триггера
        """
        trigger_id = uuid1()
        self.__triggers["time"][trigger_id] = {
            "time": time,
            "callback": callback,
            "repeat": False
        }

        return trigger_id
    
    def update(self, world: World, dt: int) -> None:
        """Обновление системы триггеров  
        дабавляет текущий dt к таймеру, что бы отслеживать time триггеры  
        Проверяет срабатывания time и touch триггеров  

        Args:
            world (World): Экземпляр класса World
            dt (int): Время с последнего кадра в миллисекундах
        """
        self.__timer += dt

        triggered = []
        for trigger in self.__triggers["touch"]:
            if self.__check_trigger_rect(trigger, world):
                triggered.append(("touch", trigger))

        for trigger in self.__triggers["time"]:
            if self.__timer >= self.__triggers["time"][trigger]["time"]:
                triggered.append(("time", trigger))

        for trigger in triggered:
            self.__call_trigger(*trigger)

        self.__get_allow_entities(world, (), {})

    def __call_trigger(self, trigger_key: str, id: UUID):
        """Вызов коллбэка триггера

        Args:
            trigger_key (str): Тип триггера touch|time
            id (UUID): id триггера
        """
        if self.__triggers[trigger_key][id]["repeat"]:
            trigger = self.__triggers[trigger_key][id]
        else:
            trigger = self.__triggers[trigger_key].pop(id)
        trigger["callback"]()

    def __check_trigger_rect(self, trigger_id: UUID, world: World) -> bool:
        """Проверка столновения ректа триггера с ректом подходящих сущностей

        Args:
            trigger_id (UUID): id триггера
            world (World): Экземпляра класса World

        Returns:
            bool: Произошло столкновение или нет
        """
        trigger = self.__triggers["touch"][trigger_id]

        targets_id = self.__get_allow_entities(world, trigger["allow_entity"])

        for target in targets_id:
            target_transform = world.get_component(target, ComponentTransform)
            if trigger["rect"].colliderect(target_transform.rect):
                return True
        
        return False

    def __get_allow_entities(self, world: World, components: tuple[Component], cache={}) -> tuple[UUID]:
        """Получение id подходящих сущностей

        Args:
            world (World): Экземпляра класса World
            components (tuple[Component]): Кортеж компонентов для получения подходящих сущностей
            cache (dict, optional): Кэш. Defaults to {}.

        Returns:
            tuple[UUID]: Кортеж с id сущностей имеющих все components
        """
        if not components: return

        if components not in cache:
            cache[components] = world.get_entities_with_all(*components)
        return cache[components]
