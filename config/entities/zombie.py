import os
from config import paths
from src.states import StateZombie


ZOMBIE_POS = (1, 0)
ZOMBIE_SIZE = (128, 128)
ZOMBIE_IDLE_IMG = os.path.join(paths.BASE_PATH, r"tests\zombie_idle.png")
ZOMBIE_IDLE_TILESET_SIZE = (6, 1)
ZOMBIE_ANIMATION_FRAME_RATE = 100
ZOMBIE_SPEED = 200
ZOMBIE_START_STATE = StateZombie.IDLE_LEFT
ZOMBIE_STATES = (
    (StateZombie.IDLE_LEFT, "tests\zombie_idle.png", ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE, False),
    (StateZombie.IDLE_RIGHT, "tests\zombie_idle.png", ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE, True),
)