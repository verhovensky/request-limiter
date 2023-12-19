from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # TTL in seconds
    CELERY_TASK_ID_TTL: int = 3600
    # URL для передачи запроса его в первозданном виде
    CHAT_BOT_WEBHOOK_URL: str = "https://chatbot.com/webhook"
    # Запросы должны троттлиться до 8 RPS
    THROTTLING_LIMIT: int = 8
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = []
    # Localhost by default
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
