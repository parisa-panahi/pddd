from starlette.endpoints import (
    HTTPEndpoint,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)

from pddd.services import (
    Service,
    CreateService,
    ReadService,
    UpdateService,
    DeleteService,
    CrudService,
)

try:
    from starlette_marshal.json import (
        loads as json_loads,
    )
except ImportError:
    from json import (
        loads as json_loads,
    )

try:
    from starlette_marshal import (
        JSONResponse,
    )
except ImportError:
    from starlette.responses import (
        JSONResponse,
    )


class StarletteEndpoint(HTTPEndpoint):
    service: Service


class StarletteCreateMixin(object):
    service: CreateService

    async def post(self, request: Request) -> Response:
        body: dict = json_loads(s=await request.body())
        data: dict = await self.service.create(inputs=body)

        return JSONResponse(content=data)


class StarletteReadMixin(object):
    service: ReadService

    async def get(self, request: Request) -> Response:
        query_params: dict = dict(request.query_params)
        data: list = await self.service.read(filters=query_params)

        return JSONResponse(content=data)


class StarletteUpdateMixin(object):
    service: UpdateService

    async def patch(self, request: Request) -> Response:
        body: dict = json_loads(s=await request.body())
        id_: str = request.path_params.get("id")
        data: dict = await self.service.update(id_=id_, inputs=body)

        return JSONResponse(content=data)


class StarletteDeleteMixin(object):
    service: DeleteService

    async def delete(self, request: Request) -> Response:
        id_: str = request.path_params.get("id")
        await self.service.delete(id_=id_)

        return Response(status_code=204)


class StarletteCrudEndpoint(
    StarletteEndpoint,
    StarletteCreateMixin,
    StarletteReadMixin,
    StarletteUpdateMixin,
    StarletteDeleteMixin,
):
    service: CrudService
