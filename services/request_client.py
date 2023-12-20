import json
import logging
from urllib.error import HTTPError

import backoff
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import InvalidJSONError, JSONDecodeError
from starlette import status

from settings.config import settings

chatbot_logger = logging.getLogger(__name__)


class ChatBotWebhookAdapter:
    GOOD_STATUSES = [status.HTTP_200_OK, status.HTTP_201_CREATED]
    adapter = HTTPAdapter()
    requests.adapters.DEFAULT_RETRIES = 5
    client = requests.Session()
    client.mount("https://", adapter)
    client.mount("http://", adapter)

    @staticmethod
    @backoff.on_exception(
        backoff.expo,
        (requests.RequestException, requests.JSONDecodeError, HTTPError),
        max_tries=4,
        max_time=300,
        on_giveup=chatbot_logger.error("Max retries exceeded"),
    )
    def _make_request(
        url: str, method: str, task_id: str, data: dict | None = None
    ) -> tuple[bool, dict]:
        response = None
        try:
            response = ChatBotWebhookAdapter.client.request(
                method=method,
                url=url,
                headers={"Content-Type": "application/json", "X-Celery-ID": task_id},
                data=json.dumps(data) if data else {},
            )
            response.raise_for_status()
            data = response.json()
        except (
            requests.RequestException,
            InvalidJSONError,
            JSONDecodeError,
            HTTPError,
        ) as exc:
            chatbot_logger.error(
                f"[ChatBotWebhookAdapter] Ошибка при запросе {exc}",
                extra={
                    "error": response.text  # type: ignore
                    if hasattr(response, "text")
                    else "Отсутствует text у response объекта"
                },
                exc_info=True,
            )
            return False, {}
        if response.status_code in ChatBotWebhookAdapter.GOOD_STATUSES:
            chatbot_logger.info(
                "[ChatBotWebhookAdapter] Ответ от сервера чатбота 200",
                extra={"result": response.text},
            )
            return True, data
        else:
            chatbot_logger.info(
                "[ChatBotWebhookAdapter] HTTP запрос завершился ошибкой",
                extra={"status": response.status_code, "data": data},
                exc_info=True,
            )
        return False, {}

    @staticmethod
    def send_data_to_chatbot(data: dict, task_id: str) -> bool:
        is_successful_response, data = ChatBotWebhookAdapter._make_request(
            url=settings.CHAT_BOT_WEBHOOK_URL, method="POST", data=data, task_id=task_id
        )
        return is_successful_response
