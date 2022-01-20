from typing import (
    List,
    Tuple,
    Type,
)

from asyncpg import (
    Connection,
    Record,
)
from buildpg import (
    render,
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
    NotFound,
)


class AsyncpgRepository(Repository):
    conn: Connection
    entity: Type[Entity]


class AsyncpgCreateMixin(CreateRepository):
    conn: Connection
    entity: Type[Entity]
    insert_query: str

    async def create(self, entity: Entity) -> Entity:
        ctx: dict = entity.__dict__
        query, args = render(
            query_template=self.insert_query,
            **ctx,
        )

        record: Record = await self.conn.fetchrow(
            query=query,
            *args,
        )

        kwargs = dict(record)
        return self.entity(
            **kwargs  # noqa
        )


class AsyncpgReadMixin(ReadRepository):
    conn: Connection
    entity: Type[Entity]
    select_query: str
    _op_map: dict = {
        "lt": "<",
        "lte": "<=",
        "gt": "<",
        "gte": "<=",
    }

    async def _filters_to_sql(self, filters: dict) -> Tuple[str, dict]:
        query: str = ""
        values: dict = {}
        for k, v in filters.items():
            if v is None:
                continue

            parts: list = k.split("__")
            len_parts: int = len(parts)

            if len_parts == 1:
                field = parts[0]
                op = "="
            elif len_parts == 2:
                field = parts[0]
                op = self._op_map[parts[1]]
            else:
                raise ValueError("more than one '__' in field name")

            query += f" and {field} {op} :{field}"
            values[field] = v

        return query, values

    async def read(self, filters: dict) -> List[Entity]:
        filter_query, kwargs = await self._filters_to_sql(filters=filters)
        query, args = render(
            query_template=self.select_query + filter_query,
            **kwargs,
        )

        return list(
            map(
                self.entity,
                await self.conn.fetch(
                    query=query,
                    *args,
                ),
            )
        )


class AsyncpgUpdateMixin(UpdateRepository):
    conn: Connection
    entity: Type[Entity]
    update_query: str

    async def update(self, entity: Entity) -> Entity:
        ctx: dict = entity.__dict__
        query, args = render(
            query_template=self.update_query,
            **ctx,
        )

        record: Record = await self.conn.fetchrow(
            query=query,
            *args,
        )

        if not record:
            raise NotFound("no record found to update")

        kwargs = dict(record)
        return self.entity(
            **kwargs  # noqa
        )


class AsyncpgDeleteMixin(DeleteRepository):
    conn: Connection
    entity: Type[Entity]
    delete_query: str

    async def delete(self, entity: Entity) -> None:
        ctx: dict = entity.__dict__
        query, args = render(
            query_template=self.delete_query,
            **ctx,
        )

        record: Record = await self.conn.fetchrow(
            query=query,
            *args,
        )

        if not record:
            raise NotFound("no record found to delete")


class AsyncpgCrudRepository(
    CrudRepository,
    AsyncpgRepository,
    AsyncpgCreateMixin,
    AsyncpgReadMixin,
    AsyncpgUpdateMixin,
    AsyncpgDeleteMixin,
):
    pass
