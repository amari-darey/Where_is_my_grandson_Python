import pygame

from uuid import UUID
from enum import Enum

from src.utils import Utils
from src.world import World
from src.camera import Camera
from src.systems import Systems
from src.assests_manager import AnimationAssets
from src.trigger_manager import TriggerManager
from src.states import AppState, GameState
from src.components import *


class Game:
    def __init__(
            self, world: World, assets: AnimationAssets, 
            screen_size: tuple[int, int], tick_rate: int, 
            game_map: tuple[tuple], player_id: UUID
            ):
        self.world = world
        self.assets = assets
        self.trigger = TriggerManager()
        self.__screen_size = screen_size
        self.__tick_rate = tick_rate

        self.window = None
        self.timer = None

        self.map = game_map
        self.camera = Camera(0, 0, *self.__screen_size)
        self.dt = 0

        self.player_id = player_id

        self.app_state = AppState.RUN
        self.game_state = GameState.RUN

        self.pygame_setup()

    def pygame_setup(self) -> None:
        pygame.init()
        self.window = pygame.display.set_mode(self.__screen_size)
        self.timer = pygame.time.Clock()

    def run(self) -> None:
        while self.app_state == AppState.RUN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app_state = AppState.CLOSE

            if self.game_state not in (GameState.PAUSE, GameState.DIALOG):
                keys = pygame.key.get_pressed()
                self.camera.update(self.world, self.player_id, self.map)
                Systems.system_map_draw(self.map, self.window, self.camera)
                Systems.system_draw_entities(self.world, self.window, self.camera)
                Systems.system_animation_update(self.world, self.assets, self.dt)
                Systems.system_player_movement(self.world, keys, self.dt)
                self.trigger.update(self.world, self.dt)

            pygame.display.update()
            self.dt = self.timer.tick(self.__tick_rate)


