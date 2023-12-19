from pydantic import BaseModel, field_validator

from schemas.enums import EventTypesEnum


class ViberBaseRequest(BaseModel):
    event: str
    timestamp: str
    chat_hostname: str
    message_token: int

    @field_validator("event")
    def is_event_processable(cls, value):
        if value not in [event for event in EventTypesEnum]:
            raise ValueError("Not valid event type received!")
        return value

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #             }
    #         ]
    #     }
    # }
