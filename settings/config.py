from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # TTL in seconds
    CELERY_TASK_ID_TTL: int = 3600
    # URL для передачи запроса его в первозданном виде
    CHAT_BOT_WEBHOOK_URL: str = "https://chatbot.com/webhook"
    # Запросы должны троттлиться до 8 RPS
    THROTTLING_LIMIT: int = 8

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
