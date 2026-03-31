from functools import partial
from src.map_manager import Map
from src.world import World
from src.game import Game
from src.entity_fabric import EntityFabric
from src.components import *
from config.game import SCREEN_SIZE
from config.entities.player import *
from config.entities.zombie import *


def setup_game(world: World) -> None:
    EntityFabric.create_player(world, PLAYER_POS)
    EntityFabric.create_zombie(world, ZOMBIE_POS)

if __name__ == "__main__":
    world = World()
    setup_game(world)
    game = Game(world, SCREEN_SIZE, 120)
    game.run()
