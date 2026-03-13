from src.states import *


TILES = {
    "0": "tests/test_tile_0.png",
    "1": "tests/test_tile_1.png",
    "2": "tests/test_tile_2.png",
    "3": "tests/test_tile_3.png",
    "4": "tests/test_tile_4.png",
    "5": "tests/test_tile_5.png",
    "6": "tests/test_tile_6.png",
    "7": "tests/test_tile_7.png",
    "8": "tests/test_tile_8.png",
    "9": "tests/test_tile_9.png",
    "10": "tests/test_tile_10.png",
}
TILE_SIZE = 128


LEVEL = {
    "name": "Test",
    "layers": {
        "base": (
            ("4", "4", "4", "5", "6"),
            ("4", "10", "9", "5", "5"),
            ("4", "7", "8", "5", "5"),
            ("4", "5", "5", "5", "5"),
            ("4", "4", "3", "4", "5"),
            ("2", "2", "4", "4", "5"),
        )
    },
    "player_stat_pos": (3, 3)
}


PLAYER_POS = (0, 0)
PLAYER_SIZE = (128, 128)
PLAYER_IDLE_IMG = r"D:\currentProject\nothingNameGame\tests\player_idle.png"
PLAYER_IDLE_TILESET_SIZE = (6, 1)
PLAYER_ANIMATION_FRAME_RATE = 100
PLAYER_SPEED = 300
PLAYER_START_STATE = StatePlayer.IDLE_LEFT
PLAYER_STATES = (
    (StatePlayer.IDLE_LEFT, "tests\player_idle.png", PLAYER_IDLE_TILESET_SIZE, PLAYER_SIZE, False),
    (StatePlayer.IDLE_RIGHT, "tests\player_idle.png", PLAYER_IDLE_TILESET_SIZE, PLAYER_SIZE, True),
    (StatePlayer.WALK_LEFT, "tests\player_walk.png", PLAYER_IDLE_TILESET_SIZE, PLAYER_SIZE, False),
    (StatePlayer.WALK_RIGHT, "tests\player_walk.png", PLAYER_IDLE_TILESET_SIZE, PLAYER_SIZE, True),
)