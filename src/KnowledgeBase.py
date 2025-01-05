from typing import List, Set
from Directions import Direction
from EntityType import EntityType
from Position import Position

class KnowledgeBase:
    def __init__(self, world_size: int):
        self.world_size = world_size
        self.safe_cells: Set[Position] = set()
        self.unsafe_cells: Set[Position] = set()
        self.wumpus_candidates: Set[Position] = set()
        self.pit_candidates: Set[Position] = set()
        self.visited_positions: Set[Position] = set()
        self.visit_count = lambda pos: len([1 for p in self.visited_positions if p == pos])

    def update_knowledge(self, pos: Position, perceptions: Set[EntityType]):
        self.safe_cells.add(pos)
        
        # If we don't detect any dangers, adjacent cells are safe
        if not (EntityType.BREEZE in perceptions or EntityType.STENCH in perceptions):
            for direction in Direction:
                adj_pos = pos + direction.value
                if self._is_valid_position(adj_pos):
                    self.safe_cells.add(adj_pos)
                    self.unsafe_cells.discard(adj_pos)
                    self.wumpus_candidates.discard(adj_pos)
                    self.pit_candidates.discard(adj_pos)
        
        # Update danger candidates based on perceptions
        if EntityType.BREEZE in perceptions:
            self._update_danger_candidates(pos, EntityType.PIT)
        if EntityType.STENCH in perceptions:
            self._update_danger_candidates(pos, EntityType.WUMPUS)

    def _update_danger_candidates(self, pos: Position, danger_type: EntityType):
        for direction in Direction:
            adj_pos = pos + direction.value
            if self._is_valid_position(adj_pos) and adj_pos not in self.safe_cells:
                if danger_type == EntityType.PIT:
                    self.pit_candidates.add(adj_pos)
                else:
                    self.wumpus_candidates.add(adj_pos)
                self.unsafe_cells.add(adj_pos)

    def get_safe_unvisited_adjacent(self, pos: Position) -> List[Direction]:
        safe_moves = []
        for direction in Direction:
            new_pos = pos + direction.value
            if (self._is_valid_position(new_pos) and 
                new_pos in self.safe_cells and 
                new_pos not in self.visited_positions):
                safe_moves.append(direction)
        return safe_moves

    def _is_valid_position(self, pos: Position) -> bool:
        return 0 <= pos.x < self.world_size and 0 <= pos.y < self.world_size
    
    def increment_visit_count(self, pos: Position):
        self.visited_positions.add(pos)