from typing import Dict, Any

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = ''
    REDIS_PORT: int = 6379
    REDIS_PASS: str = ''
    REDIS_DB: int = 0
    REDIS_MAX_CONNECTION: int = 20

    class Config:
        env_file = '.env'
        extra = "ignore"  # 忽略多余的环境变量

    @property
    def connection_pool_kw(self) -> Dict[str, Any]:
        return {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
            "db": self.REDIS_DB,
            "max_connections": self.REDIS_MAX_CONNECTION,
            "password": self.REDIS_PASS,
            "decode_responses": True,
        }
