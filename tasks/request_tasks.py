import asyncio
import functools
from logging import getLogger

from services.limiter import LimiterService
from worker import celery

task_logger = getLogger(__name__)


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return wrapper


@celery.task(name="process_incoming_request")
@sync
async def process_incoming_request(*args, **kwargs) -> bool:
    """Обработать запрос, проверить дубликаты через LimiterService,
    отправить запрос с ID таски на сервер чатбота при помощи ChatBotWebhookAdapter
    И НЕ ЗАБЫТЬ DECREASE сделать у ключа таски"""
    task_logger.info(f"[process_incoming_request] Таска запущена с {kwargs}")
    result: dict | bool = await LimiterService.process_request(request_data=kwargs)
    if result is False:
        task_logger.info(
            "[Task process_incoming_request] Запрос дублирован, прерываем таску",
        )
        return result
