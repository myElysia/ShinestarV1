from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from src.config.tortoise import settings
from src.services.healthcheck import HealthCheck


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(config=settings.tortoise_config)

    # 进行健康检查,防止数据库或者Redis崩溃
    await HealthCheck.run_all()
    yield
    await Tortoise.close_connections()


def get_connection():
    """
    获取连接池
    active: conn.pool.get_active_connections()
    idle: conn.pool.get_idle_connections()
    :return:
    """
    conn = Tortoise.get_connection("default")
    return conn
