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


class CreateRepository(Repository, ABC):
    conn: Any
    entity: Type[Entity]

    @abstractmethod
    async def create(self, entity: Entity) -> Entity:
        ...


class ReadRepository(Repository, ABC):
    conn: Any
    entity: Type[Entity]

    @abstractmethod
    async def read(self, filters: dict) -> List[Entity]:
        ...


class UpdateRepository(Repository, ABC):
    conn: Any
    entity: Type[Entity]

    @abstractmethod
    async def update(self, entity: Entity) -> Entity:
        ...


class DeleteRepository(Repository, ABC):
    conn: Any
    entity: Type[Entity]

    @abstractmethod
    async def delete(self, entity: Entity) -> None:
        ...


class CrudRepository(
    Repository,
    CreateRepository,
    ReadRepository,
    UpdateRepository,
    DeleteRepository,
    ABC,
):
    pass


class NotFound(Exception):
    pass
