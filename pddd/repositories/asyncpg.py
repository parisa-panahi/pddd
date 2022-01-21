from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Tuple,
    Optional,
)

from asyncpg import (
    Record,
    connect,
    Connection,
)
from buildpg import (
    render,
)

from pddd.entities import (
    Entity,
)
from pddd.exceptions import (
    RepositoryConnectionError,
    RecordNotFoundError,
    InvalidFilterError,
)
from pddd.repositories import (
    Repository,
    CreateRepository,
    ReadRepository,
    UpdateRepository,
    DeleteRepository,
)


class AsyncpgConnection(object):
    conn: Optional[Connection]
    dsn: str

    def __init__(self, dsn: str):
        self.conn = None
        self.dsn = dsn

    async def connect(self) -> None:
        if self.conn:
            raise RepositoryConnectionError("asyncpg is running")

        self.conn = await connect(dsn=self.dsn)

    async def disconnect(self) -> None:
        if not self.conn:
            raise RepositoryConnectionError("asyncpg is not running")

        await self.conn.close()
        self.conn = None


class AsyncpgRepository(Repository, ABC):
    @property
    @abstractmethod
    def connection(self) -> AsyncpgConnection:
        raise NotImplementedError()


class AsyncpgCreateRepository(AsyncpgRepository, CreateRepository, ABC):
    @property
    @abstractmethod
    def insert_query(self) -> str:
        raise NotImplementedError()

    async def create(self, entity: Entity) -> Entity:
        ctx: dict = entity.__dict__
        query, args = render(
            query_template=self.insert_query,
            **ctx,
        )

        record: Record = await self.connection.conn.fetchrow(
            query,
            *args,
        )

        kwargs = dict(record)
        return self.entity(
            **kwargs  # noqa
        )


class AsyncpgReadRepository(AsyncpgRepository, ReadRepository, ABC):
    _op_map: dict = {
        "lt": "<",
        "lte": "<=",
        "gt": "<",
        "gte": "<=",
    }

    @property
    @abstractmethod
    def select_query(self) -> str:
        raise NotImplementedError()

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
                raise InvalidFilterError("more than one '__' in field name")

            query += f" and {field} {op} :{field}"
            values[field] = v

        return query, values

    async def read(self, filters: dict) -> List[Entity]:
        filter_query, kwargs = await self._filters_to_sql(filters=filters)
        query, args = render(
            query_template=self.select_query + filter_query,
            **kwargs,
        )

        records: list = await self.connection.conn.fetch(
            query,
            *args,
        )

        entities: List[Entity] = []
        for record in records:
            entities.append(self.entity(
                **record  # noqa
            ))

        return entities


class AsyncpgUpdateRepository(AsyncpgRepository, UpdateRepository, ABC):
    @property
    @abstractmethod
    def update_query(self) -> str:
        raise NotImplementedError()

    async def update(self, entity: Entity) -> Entity:
        ctx: dict = entity.__dict__
        query, args = render(
            query_template=self.update_query,
            **ctx,
        )

        record: Record = await self.connection.conn.fetchrow(
            query,
            *args,
        )

        if not record:
            raise RecordNotFoundError("no record found to update")

        kwargs = dict(record)
        return self.entity(
            **kwargs  # noqa
        )


class AsyncpgDeleteRepository(AsyncpgRepository, DeleteRepository, ABC):
    @property
    @abstractmethod
    def delete_query(self) -> str:
        raise NotImplementedError()

    async def delete(self, entity: Entity) -> None:
        ctx: dict = entity.__dict__
        query, args = render(
            query_template=self.delete_query,
            **ctx,
        )

        record: Record = await self.connection.conn.fetchrow(
            query,
            *args,
        )

        if not record:
            raise RecordNotFoundError("no record found to delete")


class AsyncpgCrudRepository(
    AsyncpgCreateRepository,
    AsyncpgReadRepository,
    AsyncpgUpdateRepository,
    AsyncpgDeleteRepository,
    ABC,
):
    ...
