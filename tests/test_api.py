import pytest
from fastapi import status
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_webhook_request_ignored(client: AsyncClient):
    from settings.config import settings

    print(settings)
    response = await client.post(
        app.url_path_for("accept_viber_requests"),
        json={},
    )
    assert response.status_code == status.HTTP_200_OK


async def test_conversation_replied(client: AsyncClient):
    expected_data = {}
    response = await client.post(
        app.url_path_for("accept_viber_requests"),
        json={},
    )
    assert response.status_code == status.HTTP_200_OK
    assert expected_data in response.json()


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
