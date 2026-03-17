import os
from src.world import World
from src.game import Game
from src.utils import Utils
from src.entity_fabric import EntityFabric
from src.assests_manager import AnimationAssets
from src.level_manager import LevelManager
from src.constants import *


def setup_game(world: World) -> tuple:
    player_id = EntityFabric.create_player(world, PLAYER_POS)
    EntityFabric.create_zombie(world, ZOMBIE_POS)

    layers = LevelManager()
    game_map = Utils.create_map(layers.get_map())

    return player_id, game_map


if __name__ == "__main__":
    world = World()
    assets = AnimationAssets()
    player_id, game_map = setup_game(world)
    game = Game(world, assets, SCREEN_SIZE, 60, game_map, player_id)
    game.run()