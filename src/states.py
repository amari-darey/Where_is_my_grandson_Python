from enum import Enum


class StatePlayer(Enum):
    IDLE_LEFT = 0
    IDLE_RIGHT = 1
    WALK_LEFT = 2
    WALK_RIGHT = 3

class StateZombie(Enum):
    IDLE_LEFT = 0
    IDLE_RIGHT = 1
