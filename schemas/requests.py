from pydantic import BaseModel, field_validator

from schemas.enums import EventTypesEnum


class ViberBaseRequest(BaseModel):
    event: str
    timestamp: str
    chat_hostname: str
    message_token: int
    sender: dict | None
    message: dict | None
    silent: bool | None

    @field_validator("event")
    def is_event_processable(cls, value):
        if value not in [event for event in EventTypesEnum]:
            raise ValueError("Not valid event type received!")
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "event": "message",
                    "timestamp": "12345",
                    "chat_hostname": "SN-CALLBACK-21_",
                    "message_token": 5916837654388304302,
                    "sender": {
                        "id": "12345",
                        "name": "Sergey Rùdnev",
                        "avatar": "https://media-direct.cdn.viber.com/download_photo?dlid=MFojMvbS52ZImnxNQUHeU3zomFr47zbnIu6Zj613oDvnQmtgG--p0H_1mI7PPH10Y89AEuUTXTC_7k-j9elWuN6kQ3k1-uJgNEZQ_oJCpt84AB7tGnB4YiFOfeNmFb6bH4sCLw&fltp=jpg&imsz=0000",
                        "language": "en",
                        "country": "RU",
                        "api_version": 8,
                    },
                    "message": {"text": "/start", "type": "text"},
                    "silent": False,
                },
            ]
        }
    }
