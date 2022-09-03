# pythonic domain driven design

This project is inspired by Domain-Driven Design (DDD), Hexagonal  (Ports &
Adapters) architecture, Onion Architecture, Clean Architecture, and Explicit
Architecture. It provides a set of toolkits that help you build your
architecture based on any of these architectures or a combination of those. So
it's not supposed to be a framework, guideline, boilerplate, example, or
anything like that.

Some classes and functions help you implement patterns like Command and Query
Responsibility Segregation (CQRS), Create, Read, Update and Delete (CRUD), and
Dependency Injection.

These toolkits are designed to be easily used by other architecture like
Event-driven architecture (EDA), Event Sourcing (ES), Microservices
architecture, and even MVC architecture.

## Bounded Contexts

Represent Bounded Context with different packages, or if microservice
architecture is used, separate Bounded Context into different microservice. But
if we use monolith architecture creating a folder for each bounded context will
be a wise choice.

## Entities / Domain Objects

```python
from dataclasses import dataclass
from pddd.entities import Entity


@dataclass(frozen=True)
class Post(Entity):
    id: int
    title: str
    content: str
```

## Value Objects

```python
class Address(object):
    town: str
    street: str
    number: int
```

## Application Service

```python
from pddd.entities import Entity
from pddd.repositories import CrudRepository
from pddd.services import Service


class PostService(Service):
    repository = CrudRepository()

    async def create(self, entity: Entity) -> None:
        await self.repository.create(entity)

    async def update(self, entity: Entity) -> None:
        await self.repository.update(entity)
```

## Repositories

```python
from pddd.entities import Entity
from pddd.repositories import CreateRepository
from pddd.repositories.asyncpg import AsyncpgConnection

DATABASE_URL: str = "DATABASE_URL"
asyncpg_connection = AsyncpgConnection(dsn=DATABASE_URL)


class PostRepository(CreateRepository):
    entity = Entity
    connection = asyncpg_connection

    async def create(self, entity: Entity) -> None:
        query: str = """
            insert into posts (title, content)
            values ($1, $2)
            returning *
        """

        await self.connection.conn.execute(
            query,
            entity,
        )
```
