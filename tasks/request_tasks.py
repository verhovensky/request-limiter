import asyncio
import functools
from logging import getLogger

from celery import Task

from services.limiter import LimiterService
from services.request_client import ChatBotWebhookAdapter
from worker import celery

task_logger = getLogger(__name__)


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return wrapper


@celery.task(name="process_incoming_request", bind=True)
@sync
async def process_incoming_request(self: Task, *args, **kwargs) -> bool:
    """Обработать запрос, проверить дубликаты через LimiterService,
    отправить запрос с ID таски на сервер чатбота при помощи ChatBotWebhookAdapter
    И НЕ ЗАБЫТЬ DECREASE сделать у ключа таски"""
    task_logger.info(f"[process_incoming_request] Таска запущена с {kwargs}")
    result: dict | bool = await LimiterService.process_request(request_data=kwargs)
    if result is False:
        task_logger.info(
            f"[Task process_incoming_request] Запрос дублирован, прерываем таску {self.request.id}",
            extra={"task_id": self.request.id},
        )
        return result
    is_able_to_sent = False
    # Если запрос все же уникальный - проверяем кол-во запросов
    while not is_able_to_sent:
        is_able_to_sent = await LimiterService.check_rate_limit()
        # Возможно это не нужно
        await asyncio.sleep(1.01)
    # Увеличиваем/создаем каунтер в ключе Redis по секунде
    await LimiterService.increase_rate_limit()
    # Отправляем запрос на эндпоинт чатбота
    is_response_ok = ChatBotWebhookAdapter.send_data_to_chatbot(
        data=result, task_id=self.request.id
    )
    # Убавляем каунтер в ключе Redis по секунде, если есть
    await LimiterService.decrease_rate_limit()
    return is_response_ok
