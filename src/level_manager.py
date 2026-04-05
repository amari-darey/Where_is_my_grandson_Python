import pygame

from functools import partial
import json
import os

from src.components import ComponentPlayer
from src.map_manager import Map
from config.paths import *
from src.entity_fabric import ENTITYFABRIC_ENTITY


class LevelManager:
    """
    Исправить:
        Уровни все сразу грузятся в память
            Собирать только имена уровней
            Сделать метод загрузки уровня и убирать предыдуший
    """
    def __init__(self, game):
        self.game = game
        self.__levels = {}
        self.__current_level = None

        self.__load_local_levels()

        self.map_manager = Map()

    def __load_local_levels(self) -> None:
        """Загрузка уровней из стандартной папки Path_to_game/levels/
        """
        if os.path.exists(LEVELS_PATH):
            for level in list(filter(lambda path: "tileset" not in path, os.listdir(LEVELS_PATH))):
                with open(os.path.join(LEVELS_PATH, level), "r", encoding="utf-8") as level:
                    data = json.load(level)
                    if self.__check_level(data):
                        self.__levels[data["name"]] = data

    def __check_level(self, level: dict) -> bool:
        """Проверка на соответсвие уровню
        Проверяемые пункты:  
            Уровень имеет ключ name  
            Имя уровня не совпадает с ранее загруженными  
            Уровень имеет ключ layers  
                По ключу layers есть ключ base  
            Размер всех слоёв одинаков
            Уровень имеет ключ player_start_pos  

        Args:
            level (dict): Уровень

        Returns:
            bool: Проходит ли уровень проверку
        """
        check_list = []
        check_list.append(level.get("name"))
        check_list.append(level.get("name") not in self.__levels)
        layers = level.get("layers")
        check_list.append(layers)
        if layers:
            check_list.append(level["layers"].get("base"))
        row_legth = 0
        for layer_name in level["layers"]:
            for index, layer_map in enumerate(level["layers"][layer_name]):
                if row_legth == 0:
                    row_legth = len(layer_map)
                if len(layer_map) == row_legth:
                    check_list.append(True)
                else:
                    check_list.append(False)
                    print(f"[Map Error]\n\t layer {layer_name} имеет {len(layer_map)} элементов вместо {row_legth} на строке {index + 1}")
        check_list.append(level.get("events"))
        check_list.append(level.get("player_start_pos"))
        return all(check_list)
    
    def load_level_by_name(self, level_name: str):
        """Загрузка уровня по его названию

        Args:
            level_name (str): Имя уровня
        """
        if level_name in self.__levels:
            self.map_manager.load_new_map(self.__levels[level_name])
            self.__current_level = level_name
            self.__create_events(self.__levels[level_name]["events"])

    def __create_events(self, events: dict):
        """Создание ивентов при загрузке уровня

        Args:
            events (dict): ивенты из уровня
        """
        for event in events["touch"]:
            if event["type"] == "dialog":
                if event["triggerComponent"]:
                    self.__create_event_dialog(event)
            if event["type"] == "create_entity":
                self.__create_event_create(event)

        for event in  events["time"]:
            if event["type"] == "dialog":
                self.__create_time_event_dialog(event)
            if event["type"] == "create_entity":
                self.__create_time_event_create(event)
    
    def __create_time_event_dialog(self, event):
        """Создание ивента диалога чрез триггер по времени

        Args:
            event (_type_): Ивент
        """
        dialog_id = self.game.dialog.add_dialog(
            self.game.world,
            self.game.player_id,
            event['content']
        )

        self.game.trigger.create_time_trigger(
            event["time"],
            partial(lambda dialog_id=dialog_id: self.game.dialog.run_dialog(dialog_id))
        )

    def __create_time_event_create(self, event):
        """Создание ивента создания сущностей чрез триггер по времени

        Args:
            event (_type_): Ивент
        """
        self.game.trigger.create_time_trigger(
            event["time"],
            partial(lambda: [ENTITYFABRIC_ENTITY[entity_type](self.game.world, entity_pos) for entity_type, entity_pos in event["content"]])
        )

    def __create_event_dialog(self, event):
        """Создание ивента диалога чрез триггер по позиции

        Args:
            event (_type_): Ивент
        """
        dialog_id = self.game.dialog.add_dialog(
            self.game.world,
            self.game.player_id,
            event['content']
        )
        self.game.trigger.create_touch_trigger(
            event["pos"],
            event["size"],
            partial(lambda dialog_id=dialog_id: self.game.dialog.run_dialog(dialog_id)),
            (ComponentPlayer, ),
            event["repeat"]
        )
    
    def __create_event_create(self, event):
        """Создание ивента создания сущностей чрез триггер по позиции

        Args:
            event (_type_): Ивент
        """
        self.game.trigger.create_touch_trigger(
                event["pos"],
                event["size"],
                partial(lambda: [ENTITYFABRIC_ENTITY[entity_type](self.game.world, entity_pos) for entity_type, entity_pos in event["content"]]),
                (ComponentPlayer, ),
                event["repeat"]
            )

    def get_game_map(self) -> pygame.Surface:
        """Получить текущую карту

        Returns:
            _type_: _description_
        """
        return self.map_manager.get_current_map()

    def get_current_level_map(self) -> dict:
        """Получить слои карты текущего уроня 

        Returns:
            dict: Словарь со слоями карты
        """
        return self.__levels[self.__current_level]["layers"]

    def get_map(self, level_name: str) -> dict:
        """Получить слои карты уроня по уровню

        Returns:
            dict: Словарь со слоями карты
        """
        return self.__levels[level_name]["layers"]
    
    def get_levels_name(self) -> tuple[str]:
        """Получить кортеж уровней

        Returns:
            tuple[str]: Кортеж уровней
        """
        return tuple(self.__levels.keys())
