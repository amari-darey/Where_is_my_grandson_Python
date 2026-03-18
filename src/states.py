from enum import Enum


class AppState(Enum):
    RUN = 1
    CLOSE = 0


class GameState(Enum):
    RUN = 1
    PAUSE = 0
    DIALOG = 2


class StatePlayer(Enum):
    IDLE_LEFT = 0
    IDLE_RIGHT = 1
    WALK_LEFT = 2
    WALK_RIGHT = 3


class StateZombie(Enum):
    IDLE_LEFT = 0
    IDLE_RIGHT = 1
