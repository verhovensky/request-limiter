from enum import Enum


class EventTypesEnum(str, Enum):
    conversation_started = "conversation_started"
    webhook = "webhook"
    message = "message"
