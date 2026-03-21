from enum import Enum, auto


class AppState(Enum):
    RUN = auto()
    CLOSE = auto()


class GameState(Enum):
    RUN = auto()
    PAUSE = auto()
    DIALOG = auto()


class StatePlayer(Enum):
    IDLE = auto()
    WALK= auto()

class StateZombie(Enum):
    IDLE = auto()
    WALK = auto()
    CHASE = auto()
    PATROL = auto()

class StateDirection(Enum):
    LEFT = auto()
    RIGHT = auto()