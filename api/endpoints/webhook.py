from logging import getLogger
from typing import Union

from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from schemas.requests import (ConversationRequestSchema, MessageRequestSchema,
                              WebhookRequestSchema)
from schemas.responses import (ConversationResponseSchema,
                               MessageResponseSchema, WebhookResponseSchema)

router = APIRouter()
requests_logger = getLogger(__name__)


@router.post(
    "/accept_viber",
    response_model=Union[
        ConversationResponseSchema, MessageResponseSchema, WebhookResponseSchema
    ],
)
async def accept_viber_requests(
    data: WebhookRequestSchema | ConversationResponseSchema | MessageRequestSchema,
):
    """Единый эндпоинт для принятия сообщений от Viber"""

    if isinstance(data, WebhookRequestSchema):
        return JSONResponse(status_code=status.HTTP_200_OK, content={})
    elif isinstance(data, MessageRequestSchema):
        requests_logger.info("[accept_viber] Получен event=message")
    elif isinstance(data, ConversationRequestSchema):
        requests_logger.info("[accept_viber] Получен event=conversation_started")
