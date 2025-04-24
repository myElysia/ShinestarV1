from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from tortoise import Tortoise


class DBCleanupMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        finally:
            # 每次请求结束后检查空闲连接
            conn = Tortoise.get_connection()