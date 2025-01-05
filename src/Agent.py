from typing import List, Optional, Set, Deque
from collections import deque
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
        self.exploration_stack: Deque[Position] = deque()
        self.current_path: List[Position] = []
        
    def perceive_current_location(self):
        current_cell = self.world.grid[self.world.agent_pos.x][self.world.agent_pos.y]
        perceptions = current_cell.entities
        self.knowledge_base.update_knowledge(self.world.agent_pos, perceptions)
        current_cell.visited = True
        self.visited_positions.add(self.world.agent_pos)
        
        # Add unvisited safe neighbors to exploration stack
        self._update_exploration_stack()

    def _update_exploration_stack(self):
        # Get all safe unvisited adjacent positions
        for direction in Direction:
            new_pos = self.world.agent_pos + direction.value
            if (self._is_valid_position(new_pos) and 
                new_pos in self.knowledge_base.safe_cells and 
                new_pos not in self.visited_positions and 
                new_pos not in self.exploration_stack):
                self.exploration_stack.append(new_pos)

    def _is_valid_position(self, pos: Position) -> bool:
        return 0 <= pos.x < self.world.size and 0 <= pos.y < self.world.size

    def _get_direction_to(self, target: Position) -> Optional[Direction]:
        dx = target.x - self.world.agent_pos.x
        dy = target.y - self.world.agent_pos.y
        for direction in Direction:
            if direction.value.x == dx and direction.value.y == dy:
                return direction
        return None

    def make_move(self) -> Optional[Direction]:
        # If we have a position to explore in the stack
        if self.exploration_stack:
            target_pos = self.exploration_stack[-1]  # Peek at the next position
            
            # If we can move directly to the target position
            if self._is_adjacent(self.world.agent_pos, target_pos):
                self.exploration_stack.pop()  # Remove it from the stack
                self.path_history.append(self.world.agent_pos)
                return self._get_direction_to(target_pos)
            
            # If we can't move directly, try to find a path to the target
            path = self._find_path_to(target_pos)
            if path and len(path) > 1:  # path[0] is current position
                next_pos = path[1]  # Get the next position in the path
                self.path_history.append(self.world.agent_pos)
                return self._get_direction_to(next_pos)
        
        # If no exploration targets, try to find any unvisited safe cell
        unvisited_safe = self._find_nearest_unvisited_safe()
        if unvisited_safe:
            self.exploration_stack.append(unvisited_safe)
            return self.make_move()  # Recursively try to move to the new target
        
        return None  # No valid moves available

    def _is_adjacent(self, pos1: Position, pos2: Position) -> bool:
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y) == 1

    def _find_path_to(self, target: Position) -> Optional[List[Position]]:
        """Find a path to the target position using BFS through safe cells"""
        if target not in self.knowledge_base.safe_cells:
            return None
            
        queue = deque([(self.world.agent_pos, [self.world.agent_pos])])
        visited = {self.world.agent_pos}
        
        while queue:
            current_pos, path = queue.popleft()
            if current_pos == target:
                return path
                
            for direction in Direction:
                next_pos = current_pos + direction.value
                if (self._is_valid_position(next_pos) and 
                    next_pos in self.knowledge_base.safe_cells and 
                    next_pos not in visited):
                    visited.add(next_pos)
                    new_path = path + [next_pos]
                    queue.append((next_pos, new_path))
        
        return None

    def _find_nearest_unvisited_safe(self) -> Optional[Position]:
        """Find the nearest unvisited safe position using BFS"""
        queue = deque([self.world.agent_pos])
        visited = {self.world.agent_pos}
        
        while queue:
            current_pos = queue.popleft()
            for direction in Direction:
                next_pos = current_pos + direction.value
                if (self._is_valid_position(next_pos) and 
                    next_pos in self.knowledge_base.safe_cells and 
                    next_pos not in visited):
                    if next_pos not in self.visited_positions:
                        return next_pos
                    visited.add(next_pos)
                    queue.append(next_pos)
        
        return None