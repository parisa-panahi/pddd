from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Type,
    List,
)

from pddd.entities import (
    Entity,
)


class Repository(ABC):
    conn: Any
    entity: Type[Entity]

    def __init__(self, conn: Any = None, entity: Type[Entity] = None):
        if not hasattr(self, "conn"):
            self.conn = conn

        if not hasattr(self, "entity"):
            self.entity = entity

    async def read(self, filters: dict) -> List[Entity]:
        ...

    async def create(self, entity: Entity) -> Entity:
        ...

    async def update(self, entity: Entity) -> Entity:
        ...

    async def delete(self, entity: Entity) -> None:
        ...


class NotFound(Exception):
    pass
