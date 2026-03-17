import os
from src.states import *


BASE_PATH = os.getcwd()
LEVELS_PATH = os.path.join(BASE_PATH, "levels")

SCREEN_SIZE = (128*10, 128*7)

TILES = {
    "0": "tests/test_tile_0.png",
    "1": "tests/test_tile_1.png",
    "2": "tests/test_tile_2.png",
    "3": "tests/test_tile_3.png",
    "4": "tests/test_tile_4.png",
    "5": "tests/test_tile_5.png",
    "5.1": "tests/test_tile_5.1.png",
    "5.2": "tests/test_tile_5.2.png",
    "5.3": "tests/test_tile_5.3.png",
    "5.4": "tests/test_tile_5.4.png",
    "6": "tests/test_tile_6.png",
    "11": "tests/test_tile_11.png",
    "11.1": "tests/test_tile_11.1.png",
    "11.2": "tests/test_tile_11.2.png",
    "11.3": "tests/test_tile_11.3.png",
    "11.4": "tests/test_tile_11.4.png",
    "12": "tests/test_tile_12.png"
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

ZOMBIE_POS = (1, 0)
ZOMBIE_SIZE = (128, 128)
ZOMBIE_IDLE_IMG = r"D:\currentProject\nothingNameGame\tests\zombie_idle.png"
ZOMBIE_IDLE_TILESET_SIZE = (6, 1)
ZOMBIE_ANIMATION_FRAME_RATE = 100
ZOMBIE_SPEED = 200
ZOMBIE_START_STATE = StateZombie.IDLE_LEFT
ZOMBIE_STATES = (
    (StateZombie.IDLE_LEFT, "tests\zombie_idle.png", ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE, False),
    (StateZombie.IDLE_RIGHT, "tests\zombie_idle.png", ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE, True),
)