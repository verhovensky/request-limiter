import pytest
from fastapi import status
from httpx import AsyncClient

from main import app
from schemas.responses import ConversationResponseSchema


@pytest.mark.asyncio
async def test_webhook_request_ignored(client: AsyncClient):
    response = await client.post(
        app.url_path_for("accept_viber_requests"),
        json={
            "event": "webhook",
            "timestamp": "12345",
            "chat_hostname": "SN-CHAT-01_",
            "message_token": 591683691947794476,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}


@pytest.mark.asyncio
async def test_conversation_replied(client: AsyncClient):
    expected_response: dict = ConversationResponseSchema().model_dump(mode="json")
    response = await client.post(
        app.url_path_for("accept_viber_requests"),
        json={
            "event": "conversation_started",
            "timestamp": "12345",
            "chat_hostname": "SN-563_",
            "message_token": 5916837284433914371,
            "type": "open",
            "user": {
                "id": "12345",
                "name": "Sergey Rùdnev",
                "avatar": "https://media-direct.cdn.viber.com/longlink",
                "language": "en",
                "country": "RU",
                "api_version": 8,
            },
            "subscribed": False,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert expected_response == response.json()


async def test_message_passed(client: AsyncClient):
    response = await client.post(
        app.url_path_for("accept_viber_requests"),
        json={},
    )
    # mymocked_function.assert_called()
    assert response.status_code == status.HTTP_200_OK


async def test_message_duplicated(client: AsyncClient):
    response = await client.post(
        app.url_path_for("accept_viber_requests"),
        json={},
    )
    # mymocked_function.assert_not_called()
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_message_event_invalid(client: AsyncClient):
    response = await client.post(
        app.url_path_for("accept_viber_requests"),
        json={
            "event": "abracadabra",
            "timestamp": "12345",
            "chat_hostname": "SN-CHAT-01_",
            "message_token": 591683691947794476,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
