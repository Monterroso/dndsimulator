from enum import Enum, auto

class LogTypes(Enum):
    ROUND_START = auto()
    ACTION_ADDED = auto()
    ACTION_PERFORMED = auto()
    GAME_START = auto()
    GAME_END = auto()
    ENTITY_MOVED = auto()
