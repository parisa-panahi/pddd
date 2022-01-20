from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
)

from pddd.repositories import (
    CreateRepository,
    ReadRepository,
    UpdateRepository,
    DeleteRepository,
    CrudRepository,
)


class Service(ABC):
    ...


class CreateService(Service, ABC):
    @property
    @abstractmethod
    def repository(self) -> CreateRepository:
        raise NotImplementedError()

    @abstractmethod
    async def create(self, inputs: dict) -> dict:
        raise NotImplementedError()


class ReadService(Service, ABC):
    @property
    @abstractmethod
    def repository(self) -> ReadRepository:
        raise NotImplementedError()

    @abstractmethod
    async def read(self, filters: dict) -> List[dict]:
        raise NotImplementedError()


class UpdateService(Service, ABC):
    @property
    @abstractmethod
    def repository(self) -> UpdateRepository:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, id_: str, inputs: dict) -> dict:
        raise NotImplementedError()


class DeleteService(Service, ABC):
    @property
    @abstractmethod
    def repository(self) -> DeleteRepository:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id_: str) -> None:
        raise NotImplementedError()


class CrudService(
    CreateService,
    ReadService,
    UpdateService,
    DeleteService,
    ABC,
):
    repository: CrudRepository
