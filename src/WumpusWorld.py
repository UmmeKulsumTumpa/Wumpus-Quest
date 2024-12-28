from enum import Enum
from typing import List
import random
from Cell import Cell
from Directions import Direction
from EntityType import EntityType
from Position import Position

class WumpusWorld:
    def __init__(self, size: int = 10):
        self.size = size
        self.grid: List[List[Cell]] = [[Cell() for _ in range(size)] for _ in range(size)]
        self.agent_pos = Position(0, 0)
        self.agent_direction = Direction.EAST
        self.agent_alive = True
        self.has_gold = False
        self.score = 0

    def initialize_random_world(self, num_pits: int = 10, num_wumpus: int = 1):
        # Place pits
        for _ in range(num_pits):
            while True:
                x, y = random.randint(1, self.size-1), random.randint(1, self.size-1)
                if not self.grid[x][y].entities:
                    self.grid[x][y].add_entity(EntityType.PIT)
                    # Add breezes around pit
                    self._add_perception_around(Position(x, y), EntityType.BREEZE)
                    break

        # Place Wumpus
        for _ in range(num_wumpus):
            while True:
                x, y = random.randint(1, self.size-1), random.randint(1, self.size-1)
                if not self.grid[x][y].entities:
                    self.grid[x][y].add_entity(EntityType.WUMPUS)
                    # Add stenches around Wumpus
                    self._add_perception_around(Position(x, y), EntityType.STENCH)
                    break

        # Place gold
        while True:
            x, y = random.randint(1, self.size-1), random.randint(1, self.size-1)
            if not self.grid[x][y].entities:
                self.grid[x][y].add_entity(EntityType.GOLD)
                self.grid[x][y].add_entity(EntityType.GLITTER)
                break

    def _add_perception_around(self, pos: Position, perception: EntityType):
        for direction in Direction:
            new_pos = pos + direction.value
            if self._is_valid_position(new_pos):
                self.grid[new_pos.x][new_pos.y].add_entity(perception)

    def _is_valid_position(self, pos: Position) -> bool:
        return 0 <= pos.x < self.size and 0 <= pos.y < self.size