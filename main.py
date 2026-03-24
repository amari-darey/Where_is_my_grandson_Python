from functools import partial
from src.map_manager import Map
from src.world import World
from src.game import Game
from src.entity_fabric import EntityFabric
from src.components import *
from config.game import SCREEN_SIZE
from config.entities.player import *
from config.entities.zombie import *


def setup_game(world: World, map_manager: Map) -> None:
    EntityFabric.create_player(world, map_manager, PLAYER_POS)
    EntityFabric.create_zombie(world, map_manager, ZOMBIE_POS)

def setup_event(world: World, game: Game):
    dialog_id = game.dialog.add_dialog(
        world, 
        game.player_id, 
        ("Упс... В говно наступил...", "Ну что за день такой")
        )
    dialog2_id = game.dialog.add_dialog(
        world, 
        game.player_id, 
        ("Похоже тут должен был быть мой дом...", "Но его пока не нарисовали")
        )
    game.trigger.create_touch_trigger(
        (2, 2), 
        (0.2, 0.2), 
        partial(lambda: game.dialog.run_dialog(dialog_id)), 
        (ComponentPlayer, ), 
        False
        )
    game.trigger.create_touch_trigger(
        (1, 14), 
        (5, 5), 
        partial(lambda: game.dialog.run_dialog(dialog2_id)), 
        (ComponentPlayer, ), 
        False
        )
    game.trigger.create_touch_trigger(
        (3, 3), 
        (0.5, 0.5), 
        partial(lambda: [EntityFabric.create_zombie(world, game.level_manager.map_manager, (x, 4)) for x in range(5)]), 
        (ComponentPlayer, ), 
        False
        )


if __name__ == "__main__":
    world = World()
    game = Game(world, SCREEN_SIZE, 60)
    setup_game(world, game.level_manager.map_manager)
    game.identify_player()
    setup_event(world, game)
    game.run()
