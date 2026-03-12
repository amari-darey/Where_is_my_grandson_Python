from src.states import *


TILES = {
    "0": "tests/test_tile_1.png",
    "1": "tests/test_tile_2.png",
}
TILE_SIZE = 128


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