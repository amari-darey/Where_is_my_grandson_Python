import pygame

from uuid import UUID
from typing import Optional
from heapq import heappush, heappop
from src.utils import Utils
from config.tiles import TILE_SIZE, TILES


class Map:
    def __init__(self):
        self.game_map = None
        self.collision_map = None

    def __create_collision_map(self, game_map: pygame.Surface) -> list[list[str]]:
        """Создание базовой пустой карты

        Args:
            map_size (tuple[int, int]): Размер карты

        Returns:
            list[list[str]]: Карта
        """
        map_size = self.cordinate_to_pos(game_map.get_size())
        owner_map = []
        for _ in range(map_size[0]):
            row = []
            for _ in range(map_size[1]):
                row.append("0")
            owner_map.append(row)
        return owner_map
    
    def __create_map(self, game_map: dict[str, tuple[tuple[str]]]) -> pygame.Surface:
        """Создание карты

        Args:
            game_map (dict[str, tuple[tuple[str]]]): Словарь где ключами выступают названия слоёв 
            а значениями кортеж с кортежами с номерами тайлов

        Returns:
            pygame.Surface: Картинка карты
        """
        map_width = len(game_map["layers"]["base"][0])
        map_height = len(game_map["layers"]["base"])
        surface = pygame.Surface((map_width * TILE_SIZE, map_height* TILE_SIZE))
        for name, layer in game_map["layers"].items():
            x = 0
            y = 0
            for row in layer:
                for col in row:
                    surface.blit(Utils.load_image_with_scale(TILES[col], (TILE_SIZE, TILE_SIZE)), (x, y))
                    x += TILE_SIZE
                x = 0
                y += TILE_SIZE
        return surface
    
    def load_new_map(self, game_map: dict[str, tuple[tuple[str]]]):
        self.game_map = self.__create_map(game_map)
        self.collision_map = self.__create_collision_map(self.game_map)

    def add_to_map(self, position: tuple[int, int], entity_id: Optional[UUID] = None) -> tuple[int, int]|bool:
        """Добавляет объекты на карту  
        Если не был передан entity_id то будет добавлен как статичный объект

        Args:
            position (tuple[int, int]): Позиция в глобальных кординатах
            entity_id (Optional[UUID], optional): id сущности. Defaults to None.

        Returns:
            tuple[int, int]|bool: Позиция на карте, либо False если добавление не возможно
        """

        x, y = self.cordinate_to_pos(position)
        if y < 0 or y >= len(self.collision_map): return False
        if x < 0 or x >= len(self.collision_map[y]): return False

        if self.collision_map[y][x] == "0":
            self.collision_map[y][x] = entity_id if entity_id else "1"
            return True

        return x, y
            
    
    def get_path_to_entity(self, entity_pos: tuple[int, int], target_pos: tuple[int, int]) -> list|bool:
        """Расчитывает путь до сущности  
        Приоретет клеток  
        ____________  
        |8|   1  |2|  
        |—|——————|—|  
        |7|target|3|  
        |—|——————|—|  
        |6|   5  |4|  
        |_|______|_|  

        Args:
            entity_pos (tuple[int, int]): Глобальные кординаты сущности которая ищет путь
            target_pos (tuple[int, int]): Глобальные кординаты сущности до которой путь

        Returns:
            list|bool: Список точек маршрута либо False если путь не найден
        """
        entity_pos = self.cordinate_to_pos(entity_pos)
        target_pos = self.cordinate_to_pos(target_pos)

        points = (
            (target_pos[0], target_pos[1]-1),
            (target_pos[0]+1, target_pos[1]-1),
            (target_pos[0]+1, target_pos[1]),
            (target_pos[0]+1, target_pos[1]+1),
            (target_pos[0], target_pos[1]+1),
            (target_pos[0]-1, target_pos[1]-1),
            (target_pos[0]-1, target_pos[1]),
            (target_pos[0]-1, target_pos[1]+1),
        )
        alavible_point = None
        for x, y in points:
            if self.collision_map[y][x] == "0":
                alavible_point = (x, y)
                break
        return self.__get_path_to_target(entity_pos, alavible_point) if alavible_point else False
    
    def __get_path_to_target(self, entity_pos: tuple[int, int], target_pos: tuple[int, int]) -> list|bool:
        """Поиск пути от точки entity_pos до target_pos по алгоритму A*

        Args:
            entity_pos (tuple[int, int]): Начальня позиция на карте
            target_pos (tuple[int, int]): Конечная позиция на карте

        Returns:
            list|bool: Список точек пути в глобальных кординатах или False если путь не найден
        """
        heuristic = lambda point_a, point_b: abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])
        is_walkable = lambda x, y: self.collision_map[y][x] == "0"

        open_heap = []
        heappush(open_heap, (0, entity_pos))

        closed_set = set()
        came_from = {}
        g_score = {entity_pos: 0}

        while open_heap:
            _, current = heappop(open_heap)
            if current in closed_set:
                continue

            closed_set.add(current)

            if current == target_pos:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(entity_pos)
                path.reverse()
                return [self.pos_to_cordinate(point) for point in path]
            
            x, y = current
            neighbors = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
                (x + 1, y + 1),
                (x - 1, y + 1),
                (x - 1, y - 1),
                (x + 1, y - 1),
            ]

            for new_x, new_y in neighbors:
                if ((not is_walkable(new_x, new_y)) and (new_x, new_y) != target_pos) or ((new_x, new_y) in closed_set):
                    continue

                new_g = g_score[current] + 1

                if (new_x, new_y) not in g_score or new_g < g_score[(new_x, new_y)]:
                    g_score[(new_x, new_y)] = new_g
                    f = new_g + heuristic((new_x, new_y), target_pos)
                    heappush(open_heap, (f, (new_x, new_y)))
                    came_from[(new_x, new_y)] = current
            
        return False

    def get_current_map(self) -> pygame.Surface:
        return self.game_map

    @staticmethod
    def cordinate_to_pos(pos: tuple[int, int]) -> tuple[int, int]:
        """Превращает глобальные кординаты в позицию на карте

        Args:
            pos (tuple[int, int]): Глобальные кординаты

        Example:
            ``` python
                # При TILE_SIZE == 128
                pos = (1432, 567)  
                map_pos = Map.cordinate_to_pos(pos)  
                print(map_pos) #(11, 4)
            ```

        Returns:
            tuple[int, int]: Позиция на карте
        """
        return (int(round(pos[0]/TILE_SIZE, 0)), int(round(pos[1]/TILE_SIZE, 0)))
    
    @staticmethod
    def pos_to_cordinate(pos: tuple[int, int]) -> tuple[int, int]:
        """Превращает позацию на карте в глобальные кординаты

        Args:
            pos (tuple[int, int]): Позиция на карте

        Example:
            ``` python
                # При TILE_SIZE == 128
                pos = (11, 4)  
                map_pos = Map.pos_to_cordinate(pos)  
                print(map_pos) #(1408, 512)
            ```

        Returns:
            tuple[int, int]: Глобальные кординаты
        """
        return (round(pos[0]*TILE_SIZE, 0), round(pos[1]*TILE_SIZE, 0))
    