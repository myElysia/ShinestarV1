from fastapi import APIRouter
from http import HTTPStatus
from enum import Enum


class ErrorResponse(Enum):
    HTTPStatus.BAD_REQUEST = {"description": "Bad request"}
    HTTPStatus.NOT_FOUND = {"description": "Not found"}
    HTTPStatus.INTERNAL_SERVER_ERROR = {"description": "Server error"}
    HTTPStatus.BAD_GATEWAY = {"description": "Bad gateway"}


class Response:
    def __init__(self, code, data=None):
        if code in ErrorResponse.__members__ and not data:
            self.response = ErrorResponse.__getitem__(code)
        else:
            self.response = data

    def __call__(self, *args, **kwargs):
        return self.response


router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
    responses=Response(HTTPStatus.NOT_FOUND)(),
)


def register_router(router: APIRouter):
    router.include_router(router)
