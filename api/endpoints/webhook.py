from logging import getLogger
from typing import Union

from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from schemas.enums import EventTypesEnum
from schemas.requests import ViberBaseRequest
from schemas.responses import (ConversationResponseSchema,
                               MessageResponseSchema, WebhookResponseSchema)
from tasks.request_tasks import process_incoming_request

router = APIRouter()
endpoints_logger = getLogger(__name__)


@router.post(
    "/accept_viber",
    response_model=Union[
        ConversationResponseSchema, MessageResponseSchema, WebhookResponseSchema
    ],
)
async def accept_viber_requests(
    data: ViberBaseRequest,
):
    """Единый эндпоинт для принятия сообщений от Viber"""

    if data.event == EventTypesEnum.webhook:
        return JSONResponse(status_code=status.HTTP_200_OK, content={})
    elif data.event == EventTypesEnum.conversation_started:
        endpoints_logger.info("[accept_viber] Получен event=conversation_started")
        conversation_response: dict = ConversationResponseSchema().model_dump(
            mode="json"
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=conversation_response
        )
    elif data.event == EventTypesEnum.message:
        to_json_data: dict = data.model_dump(mode="json")
        endpoints_logger.info(
            "[accept_viber] Получен event=message", extra=to_json_data
        )
        process_incoming_request.apply_async(kwargs=to_json_data)
        return JSONResponse(status_code=status.HTTP_200_OK, content={})
