import pygame

from uuid import UUID


from src.utils import Utils
from src.world import World
from src.camera import Camera
from src.systems import Systems
from src.assests_manager import AnimationAssets


class Game:
    def __init__(
            self, world: World, assets: AnimationAssets, 
            screen_size: tuple[int, int], tick_rate: int, 
            game_map: tuple[tuple], player_id: UUID
            ):
        self.world = world
        self.assets = assets
        self.__screen_size = screen_size
        self.__tick_rate = tick_rate

        self.window = None
        self.timer = None

        self.map = game_map
        self.camera = Camera(0, 0, *self.__screen_size)
        self.dt = 0

        self.player_id = player_id

        self.game = True
        self.pause = False

        self.pygame_setup()

    def pygame_setup(self) -> None:
        pygame.init()
        self.window = pygame.display.set_mode(self.__screen_size, pygame.RESIZABLE)
        self.timer = pygame.time.Clock()

    def run(self) -> None:
        while self.game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game = False
            if not self.pause:
                keys = pygame.key.get_pressed()
                self.camera.update(self.world, self.player_id, self.map)
                Systems.system_map_draw(self.map, self.window, self.camera)
                Systems.system_draw_entities(self.world, self.window, self.camera)
                Systems.system_animation_update(self.world, self.assets, self.dt)
                Systems.system_player_movement(self.world, keys, self.dt)
            pygame.display.update()
            self.dt = self.timer.tick(self.__tick_rate)