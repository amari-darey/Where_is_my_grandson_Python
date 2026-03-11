import pygame
import os


class Utils:
    @staticmethod
    def load_map(path: str) -> list[list]:
        if not os.path.exists(path): return

        game_map = []
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                game_map.append(list(map(int, line.split())))
        
        return game_map

    @staticmethod
    def create_map(game_map: list[list]):
        size = 128
        surface = pygame.Surface((len(game_map[0]) * size, len(game_map)* size))
        tile_1 = Utils.load_image_with_scale("tests/test_tile_4.png", (128, 128))
        tile_2 = Utils.load_image_with_scale("tests/test_tile_3.png", (128, 128))
        x = 0
        y = 0
        for row in game_map:
            for col in row:
                tile = tile_1 if col == 0 else tile_2
                surface.blit(tile, (x, y))
                x += size
            x = 0
            y += size
        return surface


    @staticmethod
    def load_image_with_scale(path: str, size: tuple[int, int], cache={}) -> pygame.Surface:
        if path in cache:
            if size not in cache[path]:
                cache[path][size] = pygame.transform.scale(pygame.image.load(path), size)
        else:
            cache[path] = {}
            cache[path][size] = pygame.transform.scale(pygame.image.load(path), size)
        return cache[path][size]
    
    @staticmethod
    def load_tile_set_with_scale(path: str, tile_set_size: tuple[int, int], image_scaled_size: tuple[int, int], cache={}) -> tuple[pygame.Surface]:
        """Загрузка тайлсета в нужном размере

        Args:
            path (str): Абсолютный путь к тайлсету
            tile_set_size (tuple[int, int]): количество картинок в 1 ряду и количество рядов в тайлсете
            image_scaled_size (tuple[int, int]): Размер итоговой картинки
            cache (dict, optional): кэш. Defaults to {}.

        Returns:
            tuple[pygame.Surface]: Кортеж с картинками
        """
        if not os.path.exists(path): return

        save_flag = False
        need_new_key = False

        if path in cache:
            if image_scaled_size not in cache[path]:
                save_flag = True
        else:
            save_flag = True
            need_new_key = True

        if save_flag:
            images = []
            tileset = pygame.image.load(path)
            tile_width = tileset.get_width() // tile_set_size[0]
            tile_height = tileset.get_height() // tile_set_size[1]
            for height in range(tile_set_size[1]):
                for width in range(tile_set_size[0]):
                    rect = pygame.Rect(width * tile_width, height * tile_height, tile_width, tile_height)
                    tile = tileset.subsurface(rect)
                    images.append(pygame.transform.scale(tile, image_scaled_size))

            if need_new_key:
                cache[path] = {}
            cache[path][image_scaled_size] = tuple(images)

        return cache[path][image_scaled_size]