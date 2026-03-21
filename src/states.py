from enum import Enum, auto


class AppState(Enum):
    RUN = auto()
    CLOSE = auto()


class GameState(Enum):
    RUN = auto()
    PAUSE = auto()
    DIALOG = auto()


class StatePlayer(Enum):
    IDLE_LEFT = auto()
    IDLE_RIGHT = auto()
    WALK_LEFT = auto()
    WALK_RIGHT = auto()


class StateZombie(Enum):
    IDLE_LEFT = auto()
    IDLE_RIGHT = auto()
    WALK_LEFT = auto()
    WALK_RIGHT = auto()
    CHAISE_LEFT = auto()
    CHAISE_RIGHT = auto()
