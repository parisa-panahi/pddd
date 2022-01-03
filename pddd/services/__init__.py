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
    repository: CreateRepository

    @abstractmethod
    async def create(self, inputs: dict) -> dict:
        ...


class ReadService(Service, ABC):
    repository: ReadRepository

    @abstractmethod
    async def read(self, filters: dict) -> List[dict]:
        ...


class UpdateService(Service, ABC):
    repository: UpdateRepository

    @abstractmethod
    async def update(self, id_: str, inputs: dict) -> dict:
        ...


class DeleteService(Service, ABC):
    repository: DeleteRepository

    @abstractmethod
    async def delete(self, id_: str) -> None:
        ...


class CrudService(
    Service,
    CreateService,
    ReadService,
    UpdateService,
    DeleteService,
    ABC,
):
    repository: CrudRepository
