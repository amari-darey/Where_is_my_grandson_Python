import os
from src.world import World
from src.game import Game
from src.utils import Utils
from src.entity_fabric import EntityFabric


def setup_game(world: World) -> None:
    EntityFabric.get_player(world)


if __name__ == "__main__":
    game_map = Utils.load_map(os.path.join(os.getcwd(), "tests/test_map.txt"))

    world = World()
    setup_game(world)
    game = Game(world, (5*128, 6*128), 60, game_map)
    game.run()