from typing import List, Optional, Set
import random
from Directions import Direction
from KnowledgeBase import KnowledgeBase
from Position import Position
from WumpusWorld import WumpusWorld

class Agent:
    def __init__(self, world: WumpusWorld):
        self.world = world
        self.knowledge_base = KnowledgeBase(world.size)
        self.visited_positions: Set[Position] = set()
        self.path_history: List[Position] = []

    def perceive_current_location(self):
        current_cell = self.world.grid[self.world.agent_pos.x][self.world.agent_pos.y]
        perceptions = current_cell.entities
        self.knowledge_base.update_knowledge(self.world.agent_pos, perceptions)
        current_cell.visited = True
        self.visited_positions.add(self.world.agent_pos)

    def make_move(self) -> Optional[Direction]:
        # Get safe unvisited positions
        safe_moves = self.knowledge_base.get_safe_unvisited_adjacent(self.world.agent_pos)
        
        if safe_moves:
            # Choose the move to the least visited cell
            least_visited_move = min(safe_moves, key=lambda pos: self.knowledge_base.visit_count(pos))
            self.path_history.append(self.world.agent_pos)
            self.knowledge_base.increment_visit_count(least_visited_move)
            return least_visited_move
        
        # If no safe moves are available, try to backtrack
        if self.path_history:
            previous_pos = self.path_history[-1]
            # Calculate the direction to move back
            dx = previous_pos.x - self.world.agent_pos.x
            dy = previous_pos.y - self.world.agent_pos.y
            for direction in Direction:
                if direction.value.x == dx and direction.value.y == dy:
                    return direction
        
        return None