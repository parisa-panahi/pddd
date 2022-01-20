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
    @property
    @abstractmethod
    def conn(self) -> Any:
        raise NotImplementedError()

    @property
    @abstractmethod
    def entity(self) -> Type[Entity]:
        raise NotImplementedError()


class CreateRepository(Repository):
    @abstractmethod
    async def create(self, entity: Entity) -> Entity:
        raise NotImplementedError()


class ReadRepository(Repository, ABC):
    @abstractmethod
    async def read(self, filters: dict) -> List[Entity]:
        raise NotImplementedError()


class UpdateRepository(Repository, ABC):
    @abstractmethod
    async def update(self, entity: Entity) -> Entity:
        raise NotImplementedError()


class DeleteRepository(Repository, ABC):
    @abstractmethod
    async def delete(self, entity: Entity) -> None:
        raise NotImplementedError()


class CrudRepository(
    CreateRepository,
    ReadRepository,
    UpdateRepository,
    DeleteRepository,
    ABC,
):
    ...


class NotFound(Exception):
    ...
