from typing import Set
from EntityType import EntityType

class Cell:
    def __init__(self):
        self.entities: Set[EntityType] = set()
        self.visited = False
        self.safe = None  # None = unknown, True = safe, False = unsafe

    def add_entity(self, entity: EntityType):
        self.entities.add(entity)

    def remove_entity(self, entity: EntityType):
        self.entities.discard(entity)

    def has_entity(self, entity: EntityType) -> bool:
        return entity in self.entities