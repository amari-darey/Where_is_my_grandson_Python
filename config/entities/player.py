import os
from config import paths
from src.states import StatePlayer, StateDirection


PLAYER_NAME = "Пьяный кузнец"
PLAYER_POS = (0, 0)
PLAYER_SIZE = (128, 128)
PLAYER_IDLE_IMG = os.path.join(paths.BASE_PATH, r"tests\player_idle.png")
PLAYER_IDLE_TILESET_SIZE = (6, 1)
PLAYER_ANIMATION_FRAME_RATE = 100
PLAYER_SPEED = 300
PLAYER_START_STATE = StatePlayer.IDLE
PLAYER_STATES = (
    (StatePlayer.IDLE, "tests\player_idle.png", PLAYER_IDLE_TILESET_SIZE, PLAYER_SIZE, StateDirection.LEFT),
    (StatePlayer.IDLE, "tests\player_idle.png", PLAYER_IDLE_TILESET_SIZE, PLAYER_SIZE, StateDirection.RIGHT),
    (StatePlayer.WALK, "tests\player_walk.png", PLAYER_IDLE_TILESET_SIZE, PLAYER_SIZE, StateDirection.LEFT),
    (StatePlayer.WALK, "tests\player_walk.png", PLAYER_IDLE_TILESET_SIZE, PLAYER_SIZE, StateDirection.RIGHT),
)