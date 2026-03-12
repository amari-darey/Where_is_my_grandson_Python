import os
from src.world import World
from src.game import Game
from src.utils import Utils
from src.entity_fabric import EntityFabric
from src.assests_manager import AnimationAssets


def setup_game(world: World) -> None:
    EntityFabric.get_player(world)


if __name__ == "__main__":
    game_map = Utils.load_map(os.path.join(os.getcwd(), "tests/test_map.txt"))

    world = World()
    assets = AnimationAssets()
    setup_game(world)
    game = Game(world, assets, (5*128, 6*128), 60, game_map)
    game.run()