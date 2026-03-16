import pygame
import json
import os
from src.constants import *


class LevelManager:
    def __init__(self):
        self.__levels = {}

        self.__load_local_levels()

    def __load_local_levels(self) -> None:
        if os.path.exists(LEVELS_PATH):
            for level in os.listdir(LEVELS_PATH):
                with open(os.path.join(LEVELS_PATH, level)) as level:
                    data = json.load(level)
                    if self.__check_level(data):
                        self.__levels[data["name"]] = data

    def __check_level(self, level: dict) -> bool:
        check_list = []
        check_list.append(level.get("name"))
        layers = level.get("layers")
        check_list.append(layers)
        if layers:
            check_list.append(level["layers"].get("base"))
        check_list.append(level.get("player_stat_pos"))
        return all(check_list)
    
    def get_map(self) -> dict:
        return self.__levels["Test"]["layers"]

    def test_print(self):
        for k, v in self.__levels.items():
            print(k)
            print(v)
