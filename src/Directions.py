from enum import Enum
from src.Position import Position

class Direction(Enum):
    NORTH = Position(0, 1)
    SOUTH = Position(0, -1)
    EAST = Position(1, 0)
    WEST = Position(-1, 0)