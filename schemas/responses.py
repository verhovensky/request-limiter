from pydantic import BaseModel


class ConversationResponseSchema(BaseModel):
    min_api_version: int = (8,)
    type: str = ("text",)
    text: str = (
        "Добро пожаловать! Это сообщение по-умолчанию, обратитесь к менеджерам, чтоб его изменить.",
    )
    sender: dict = {"name": "Автоматический ответ", "avatar": None}


class WebhookResponseSchema(BaseModel):
    data: dict = {}


class MessageResponseSchema(BaseModel):
    data: dict = {}
