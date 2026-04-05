import os

import pygame

from pathlib import Path
import json

from config.paths import LEVELS_PATH


class TileManager:
    def __init__(self):
        self.__tiles = {}

    def get_tile(self, tile_name):
        if tile_name in self.__tiles:
            return self.__tiles[tile_name]

    def load_tileset(self, path: str) -> None:
        """Загружает tileset по пути к картинке  
        Необходимо наличие рядом с картинкой json файла с описанием

        Args:
            path (str | Path): Путь к картинке
        """
        path = Path(path)
        tileset = pygame.image.load(path)
        path_to_info_json_file = os.path.join(LEVELS_PATH, path.stem) + ".json"
        with open(path_to_info_json_file, "r", encoding="utf-8") as data:
            data = json.load(data)
            tile_size = data.get("tileSize", (128, 128))
            y = 0
            for line in data.get("tiles", []):
                x = 0
                for col in line:
                    rect = pygame.Rect(
                        x,
                        y,
                        tile_size[0],
                        tile_size[1]
                        )
                    tile = tileset.subsurface(rect)
                    self.__tiles[col] = tile
                    x += tile_size[0]
                y += tile_size[1]
