import pygame
import json
import os
from config.paths import *


class LevelManager:
    """
    Исправить:
        Уровни все сразу грузятся в память
            Собирать только имена уровней
            Сделать метод загрузки уровня и убирать предыдуший
    """
    def __init__(self):
        self.__levels = {}
        self.__current_level = None

        self.__load_local_levels()

    def __load_local_levels(self) -> None:
        """Загрузка уровней из стандартной папки Path_to_game/levels/
        """
        if os.path.exists(LEVELS_PATH):
            for level in os.listdir(LEVELS_PATH):
                with open(os.path.join(LEVELS_PATH, level)) as level:
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

        check_list.append(level.get("player_start_pos"))
        return all(check_list)
    
    def set_current_level(self, level_name: str):
        if level_name in self.__levels:
            self.__current_level = level_name
    
    def get_current_level_map(self) -> dict:
        return self.__levels[self.__current_level]["layers"]

    def get_map(self, level_name: str) -> dict:
        return self.__levels[level_name]["layers"]
    
    def get_levels_name(self) -> tuple[str]:
        return tuple(self.__levels.keys())
