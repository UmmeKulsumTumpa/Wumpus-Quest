from typing import List, Optional, Set
import random
from src.Directions import Direction
from src.KnowledgeBase import KnowledgeBase
from src.Position import Position
from src.WumpusWorld import WumpusWorld

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
            # Choose the move that leads to the most promising direction
            # (This could be enhanced with more sophisticated heuristics)
            return random.choice(safe_moves)
        
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