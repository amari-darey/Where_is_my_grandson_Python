import pygame
import os
from enum import Enum
from uuid import UUID

from src.assests_manager import AnimationAssets
from src.world import World
from src.camera import Camera
from src.components import ComponentEnemy, ComponentTransform
from src.states import StateDirection
from config.tiles import *


class Utils:
    @staticmethod
    def load_map(path: str) -> list[list]:
        if not os.path.exists(path): return

        game_map = []
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                game_map.append(line.split())
        
        return game_map

    @staticmethod
    def create_map(game_map: dict[str, tuple[tuple[str]]]) -> pygame.Surface:
        """Создание карты

        Args:
            game_map (dict[str, tuple[tuple[str]]]): Словарь где ключами выступают названия слоёв 
            а значениями кортеж с кортежами с номерами тайлов

        Returns:
            pygame.Surface: Картинка карты
        """
        map_width = len(game_map["base"][0])
        map_height = len(game_map["base"])
        surface = pygame.Surface((map_width * TILE_SIZE, map_height* TILE_SIZE))
        for name, layer in game_map.items():
            x = 0
            y = 0
            for row in layer:
                for col in row:
                    surface.blit(Utils.load_image_with_scale(TILES[col], (TILE_SIZE, TILE_SIZE)), (x, y))
                    x += TILE_SIZE
                x = 0
                y += TILE_SIZE
        return surface


    @staticmethod
    def load_image_with_scale(path: str, size: tuple[int, int], cache={}) -> pygame.Surface:
        """Загрузка одного изображения нужного размера

        Args:
            path (str): Путь к изображению
            size (tuple[int, int]): Размер итогового изображения ширина/высота
            cache (dict, optional): кэш. Defaults to {}.

        Returns:
            pygame.Surface: Итоговое изображение
        """
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
    
    @staticmethod
    def mirror_image(path: str, image: pygame.Surface, cache={}) -> pygame.Surface:
        if path not in cache:
            cache[path] = pygame.transform.flip(image, True, False)
        return cache[path]
    
    @staticmethod
    def mirror_images(path: str, images: tuple[pygame.Surface], cache={}) -> tuple[pygame.Surface]:
        if path not in cache:
            result = []
            for image in images:
                result.append(pygame.transform.flip(image, True, False))
            cache[path] = tuple(result)
        return cache[path]
    
    @staticmethod
    def load_animations(entity_id: UUID, states: tuple[tuple[Enum, str, tuple[int, int], tuple[int, int], bool]]) -> None:
        assets = AnimationAssets()
        state, path, tile_size, size, direction = states
        if direction == StateDirection.LEFT:
            images = Utils.load_tile_set_with_scale(path, tile_size, size)
            assets.add_asset(entity_id, state, direction, images)
        if direction == StateDirection.RIGHT:
            images = Utils.load_tile_set_with_scale(path, tile_size, size)
            images = Utils.mirror_images(path, images)
            assets.add_asset(entity_id, state, direction, images)

    @staticmethod
    def tiles_pos_to_world(tile_pos: tuple[int, int]) -> tuple[int, int]:
        """Переводит позицию в тайлах в глобальную позицию

        Args:
            tile_pos (tuple[int, int]): Позиция тайла в формета (ряд, колонка)

        Returns:
            tuple[int, int]: Позиция в глобальных кординатах
        """
        return tile_pos[0] * TILE_SIZE, tile_pos[1] * TILE_SIZE
    
    @staticmethod
    def get_closest_enemy_to_mouse(
        world: World, 
        camera: Camera, 
        mouse_pos: tuple[int, int]|pygame.Vector2, 
        max_distanse: int = 150
        ) -> UUID:
        """Определяет ближайшего к указателю мыши противника

        Args:
            world (World): Экземпляр класса World
            camera (Camera): Экземпляр класса Camera
            mouse_pos (tuple[int, int] | pygame.Vector2): Позиция мыши
            max_distanse (int, optional): Максимальная дистанция для обнаружения. Defaults to 150.

        Returns:
            UUID: id ближайшей сущности
        """
        mouse_pos = mouse_pos if isinstance(mouse_pos, pygame.Vector2) else pygame.Vector2(mouse_pos)
        closest = None
        min_dist = float("inf")
        entities = world.get_entities_with_all(ComponentEnemy, ComponentTransform)
        ofset = pygame.Vector2(camera.ofset_x, camera.ofset_y)
        for entity in entities:
            transform = world.get_component(entity, ComponentTransform)
            entity_pos = pygame.Vector2(transform.rect.center) - ofset
            dist = mouse_pos.distance_to(entity_pos)
            if dist < min_dist and dist < max_distanse:
                min_dist = dist
                closest = entity

        return closest
        