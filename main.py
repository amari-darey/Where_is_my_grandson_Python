import os
from src.world import World
from src.game import Game
from src.utils import Utils
from src.entity_fabric import EntityFabric
from src.assests_manager import AnimationAssets
from src.level_manager import LevelManager
from config.game import SCREEN_SIZE
from config.entities.player import *
from config.entities.zombie import *


def setup_game(world: World) -> tuple:
    player_id = EntityFabric.create_player(world, PLAYER_POS)
    EntityFabric.create_zombie(world, ZOMBIE_POS)

    level_manager = LevelManager()
    levels = level_manager.get_levels_name()
    game_map = Utils.create_map(level_manager.get_map(levels[0]))

    return player_id, game_map


if __name__ == "__main__":
    world = World()
    assets = AnimationAssets()
    player_id, game_map = setup_game(world)
    game = Game(world, assets, SCREEN_SIZE, 60, game_map, player_id)
    game.run()
