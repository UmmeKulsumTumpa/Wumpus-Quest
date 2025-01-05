from typing import List, Optional, Set, Deque, Dict
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
        self.frontier: Set[Position] = set()  # Unvisited but accessible safe positions
        self.known_unsafe: Set[Position] = set()  # Positions known to be unsafe
        self.to_explore: Deque[Position] = deque()  # Queue of positions to explore next
        
    def perceive_current_location(self):
        current_pos = self.world.agent_pos
        current_cell = self.world.grid[current_pos.x][current_pos.y]
        perceptions = current_cell.entities
        
        # Update knowledge base with current perceptions
        self.knowledge_base.update_knowledge(current_pos, perceptions)
        current_cell.visited = True
        self.visited_positions.add(current_pos)
        
        # Update frontier with newly discovered safe positions
        self._update_frontier()
        
        # If frontier is empty but there are still unexplored safe cells,
        # we need to find a path to them through visited cells
        if not self.frontier and not self.to_explore:
            self._find_all_reachable_safe_cells()

    def _update_frontier(self):
        """Update the frontier with newly discovered safe positions"""
        current_pos = self.world.agent_pos
        
        # Check all adjacent positions
        for direction in Direction:
            adj_pos = current_pos + direction.value
            if not self._is_valid_position(adj_pos):
                continue
                
            # If it's safe and unvisited, add to frontier
            if adj_pos in self.knowledge_base.safe_cells and adj_pos not in self.visited_positions:
                self.frontier.add(adj_pos)
            
            # If it's unsafe, mark it
            if adj_pos in self.knowledge_base.unsafe_cells:
                self.known_unsafe.add(adj_pos)

    def _find_all_reachable_safe_cells(self):
        """Find all safe cells that can be reached through visited cells"""
        # Start BFS from current position
        queue = deque([self.world.agent_pos])
        visited = {self.world.agent_pos}
        
        while queue:
            current = queue.popleft()
            
            # Check all adjacent positions
            for direction in Direction:
                adj_pos = current + direction.value
                if not self._is_valid_position(adj_pos):
                    continue
                    
                # If position is safe and unvisited
                if adj_pos in self.knowledge_base.safe_cells and adj_pos not in visited:
                    visited.add(adj_pos)
                    queue.append(adj_pos)
                    
                    # If we haven't visited this position yet, add it to exploration queue
                    if adj_pos not in self.visited_positions:
                        self.to_explore.append(adj_pos)

    def make_move(self) -> Optional[Direction]:
        current_pos = self.world.agent_pos
        
        # First priority: explore frontier positions
        if self.frontier:
            target = min(self.frontier, key=lambda p: self._manhattan_distance(current_pos, p))
            self.frontier.remove(target)
            return self._get_direction_to_target(target)
        
        # Second priority: explore positions in the to_explore queue
        if self.to_explore:
            target = self.to_explore[0]
            path = self._find_safe_path(target)
            if path:
                next_pos = path[1]  # First step towards target
                if self._is_adjacent(current_pos, next_pos):
                    self.to_explore.popleft()
                return self._get_direction_to(next_pos)
        
        # If we've exhausted all known safe cells and haven't found the gold,
        # we need to take calculated risks
        if not self.frontier and not self.to_explore:
            safest_risky_move = self._find_safest_risky_move()
            if safest_risky_move:
                return self._get_direction_to_target(safest_risky_move)
        
        return None

    def _manhattan_distance(self, pos1: Position, pos2: Position) -> int:
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

    def _get_direction_to_target(self, target: Position) -> Optional[Direction]:
        """Get the next move towards a target position"""
        path = self._find_safe_path(target)
        if path and len(path) > 1:
            return self._get_direction_to(path[1])
        return None

    def _find_safe_path(self, target: Position) -> Optional[List[Position]]:
        """Find a path through safe cells to the target position"""
        if not self._is_valid_position(target):
            return None
            
        queue = deque([(self.world.agent_pos, [self.world.agent_pos])])
        visited = {self.world.agent_pos}
        
        while queue:
            current, path = queue.popleft()
            if current == target:
                return path
                
            for direction in Direction:
                next_pos = current + direction.value
                if (self._is_valid_position(next_pos) and 
                    next_pos not in visited and
                    (next_pos in self.knowledge_base.safe_cells or next_pos in self.visited_positions)):
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        
        return None

    def _find_safest_risky_move(self) -> Optional[Position]:
        """Find the safest unexplored position when we must take a risk"""
        current_pos = self.world.agent_pos
        candidate_positions = set()
        
        # Get all adjacent unvisited positions that aren't known to be unsafe
        for direction in Direction:
            adj_pos = current_pos + direction.value
            if (self._is_valid_position(adj_pos) and 
                adj_pos not in self.visited_positions and 
                adj_pos not in self.known_unsafe):
                candidate_positions.add(adj_pos)
        
        if not candidate_positions:
            return None
        
        # Score each position based on risk factors
        position_scores = {}
        for pos in candidate_positions:
            score = 0
            # Positions adjacent to visited safe cells are preferred
            for direction in Direction:
                adj_pos = pos + direction.value
                if adj_pos in self.visited_positions:
                    score += 1
            # Fewer adjacent unsafe cells is better
            for direction in Direction:
                adj_pos = pos + direction.value
                if adj_pos in self.known_unsafe:
                    score -= 2
            position_scores[pos] = score
        
        # Return the position with the highest score
        if position_scores:
            return max(position_scores.items(), key=lambda x: x[1])[0]
        return None

    def _is_valid_position(self, pos: Position) -> bool:
        return 0 <= pos.x < self.world.size and 0 <= pos.y < self.world.size

    def _is_adjacent(self, pos1: Position, pos2: Position) -> bool:
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y) == 1

    def _get_direction_to(self, target: Position) -> Optional[Direction]:
        dx = target.x - self.world.agent_pos.x
        dy = target.y - self.world.agent_pos.y
        for direction in Direction:
            if direction.value.x == dx and direction.value.y == dy:
                return direction
        return None