from pydantic import BaseModel

from schemas.enums import EventTypesEnum


class BaseRequest(BaseModel):
    event: str
    timestamp: str
    chat_hostname: str
    message_token: int

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #             }
    #         ]
    #     }
    # }


class WebhookRequestSchema(BaseRequest):
    event: str = EventTypesEnum.webhook


class MessageRequestSchema(BaseRequest):
    event: str = EventTypesEnum.message


class ConversationRequestSchema(BaseRequest):
    event: str = EventTypesEnum.conversation_started
