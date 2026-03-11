import pygame
from src.utils import Utils
from src.world import World
from src.systems import Systems


class Game:
    def __init__(self, world: World, screen_size: tuple[int, int], tick_rate: int, game_map: tuple[tuple]):
        self.world = world
        self.__screen_size = screen_size
        self.__tick_rate = tick_rate

        self.window = None
        self.timer = None

        self.map = Utils.create_map(game_map)
        self.dt = 0

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
                self.window.blit(self.map, (0, 0))
                Systems.system_draw_entities(self.world, self.window)
                Systems.system_animation_update(self.world, self.dt)
                Systems.system_player_movement(self.world, keys, self.dt)
            pygame.display.update()
            self.dt = self.timer.tick(self.__tick_rate)