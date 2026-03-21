import os
from config import paths
from src.states import StateZombie, StateDirection


ZOMBIE_POS = (1, 0)
ZOMBIE_SIZE = (128, 128)
ZOMBIE_IDLE_IMG = os.path.join(paths.BASE_PATH, r"tests\zombie_idle.png")
ZOMBIE_IDLE_TILESET_SIZE = (6, 1)
ZOMBIE_ANIMATION_FRAME_RATE = 100
ZOMBIE_SPEED = 100
ZOMBIE_CHASE_DISTANCE = 150
ZOMBIE_START_STATE = StateZombie.IDLE
ZOMBIE_STATES = (
    (StateZombie.IDLE, "tests\zombie_idle.png", ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE, StateDirection.LEFT),
    (StateZombie.IDLE, "tests\zombie_idle.png", ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE, StateDirection.RIGHT),
    (StateZombie.CHASE, "tests\zombie_idle.png", ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE, StateDirection.LEFT),
    (StateZombie.CHASE, "tests\zombie_idle.png", ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE, StateDirection.RIGHT),
    (StateZombie.PATROL, "tests\zombie_idle.png", ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE, StateDirection.LEFT),
    (StateZombie.PATROL, "tests\zombie_idle.png", ZOMBIE_IDLE_TILESET_SIZE, ZOMBIE_SIZE, StateDirection.RIGHT),
)