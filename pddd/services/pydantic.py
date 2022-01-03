from typing import (
    Type,
    List,
)

from pydantic import (
    BaseModel as PydanticModel,
)

from pddd.entities import (
    Entity,
)
from pddd.repositories import (
    Repository,
    CreateRepository,
    ReadRepository,
    UpdateRepository,
    DeleteRepository,
    CrudRepository,
)
from pddd.services import (
    Service,
)


class PydanticBaseService(Service):
    repository: Repository


class PydanticCreateMixin(object):
    repository: CreateRepository
    model_create: Type[PydanticModel]

    async def create(self, inputs: dict) -> dict:
        model: PydanticModel = self.model_create(**inputs)
        entity: Entity = self.repository.entity(**model.dict())

        return dict(await self.repository.create(entity))


class PydanticReadMixin(object):
    repository: ReadRepository
    model_read: Type[PydanticModel]

    async def read(self, filters: dict) -> List[dict]:
        model: PydanticModel = self.model_read(**filters)
        entities: list = await self.repository.read(**model.dict())

        return list(
            map(
                dict,
                entities,
            )
        )


class PydanticUpdateMixin(object):
    repository: UpdateRepository
    model_update: Type[PydanticModel]

    async def update(self, id_: str, inputs: dict) -> dict:
        model: PydanticModel = self.model_update(id=id_, **inputs)
        entity: Entity = self.repository.entity(**model.dict())

        return dict(await self.repository.update(entity))


class PydanticDeleteMixin(object):
    repository: DeleteRepository
    model_delete: Type[PydanticModel]

    async def remove(self, id_: str) -> None:
        model: PydanticModel = self.model_delete(id=id_)
        entity: Entity = self.repository.entity(**model.dict())

        await self.repository.delete(entity)


class PydanticService(
    PydanticBaseService,
    PydanticCreateMixin,
    PydanticReadMixin,
    PydanticUpdateMixin,
    PydanticDeleteMixin,
):
    repository: CrudRepository
