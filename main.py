import os
from src.world import World
from src.game import Game
from src.utils import Utils
from src.entity_fabric import EntityFabric
from src.assests_manager import AnimationAssets
from src.constants import *


def setup_game(world: World) -> None:
    player_pos = LEVEL.get("player_stat_pos", PLAYER_POS)
    EntityFabric.get_player(world, player_pos)

    layers = LEVEL["layers"]
    map = Utils.create_map(layers)

    return map


if __name__ == "__main__":
    world = World()
    assets = AnimationAssets()
    map = setup_game(world)
    game = Game(world, assets, (5*128, 6*128), 60, map)
    game.run()