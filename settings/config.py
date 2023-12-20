import sys

import redis.asyncio as redis
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # TTL in seconds
    CELERY_TASK_ID_TTL: int = 3600
    RATE_LIMIT_REDIS_KEY: str = "RPS_LIMIT"
    # URL для передачи запроса его в первозданном виде
    CHAT_BOT_WEBHOOK_URL: str = "https://chatbot.com/webhook"
    # Запросы должны троттлиться до 8 RPS
    THROTTLING_LIMIT: int = 8
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = []
    # Localhost by default
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASS: str | None = None
    REDIS_CLIENT: redis.Redis | None = None

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"

    @field_validator("REDIS_CLIENT")
    def _assemble_redis_client(cls, v: str, values: ValidationInfo) -> redis.Redis:
        try:
            if values.data["REDIS_PASS"] is not None or values.data["REDIS_PASS"] != "":
                return redis.Redis(
                    host=values.data["REDIS_HOST"],
                    port=values.data["REDIS_PORT"],
                    password=values.data["REDIS_PASS"],
                    db=0,
                )
            else:
                return redis.Redis(
                    host=values.data["REDIS_HOST"], port=values.data["REDIS_PORT"], db=0
                )
        except Exception as e:
            sys.stdout.write(f"Redis initialization failed! {e}")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
