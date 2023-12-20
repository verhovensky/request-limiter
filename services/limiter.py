from datetime import datetime, timedelta
from hashlib import sha256
from logging import getLogger

from settings.config import settings

limiter_logger = getLogger(__name__)


class LimiterService:
    REDIS_KEY = settings.RATE_LIMIT_REDIS_KEY
    RATE_LIMIT = settings.THROTTLING_LIMIT

    @staticmethod
    async def get_redis_key() -> tuple[str, datetime]:
        """Получает ключ для текущей секунды в UTC в ISO формате + наш ключ
        Используем для кеша запросов в Redis
        прим. 'REDIS_KEY_2023-12-20T11:45:05'"""
        now: datetime = datetime.utcnow()
        current_second: str = now.isoformat(sep="T", timespec="seconds")
        return f"{LimiterService.REDIS_KEY}_{current_second}", now

    @staticmethod
    async def increase_rate_limit(
        is_first_request: bool = False,
    ) -> dict[str, int | bool]:
        """Увеличивает кол-во в ключе redis_minute_key, и инвалидирует ключ через секунду,
        т.к. у нас лимит в секунду. is_first_request возможно нужен для расширения функционала, дебага.
        """
        redis_minute_key, now = await LimiterService.get_redis_key()
        current_count: int = await settings.REDIS_CLIENT.incrby(redis_minute_key)
        # в таске потом проверяем текущее значение по ключу для текущей минуты в UTC
        if current_count == 1:
            await settings.REDIS_CLIENT.expireat(
                name=LimiterService.REDIS_KEY, when=now + timedelta(seconds=1)
            )
            is_first_request = True
        result = {"current_count": current_count, "is_first_request": is_first_request}
        limiter_logger.info(
            f"[LimiterService] Rate Limit увеличен до {current_count}",
            extra={"data": result},
        )
        return result

    @staticmethod
    async def decrease_rate_limit() -> bool:
        """Убавляем каунтер в ключе Redis по секунде, если есть"""
        redis_minute_key, now = await LimiterService.get_redis_key()
        current_count: int = await settings.REDIS_CLIENT.decrby(redis_minute_key)
        return bool(current_count)

    @staticmethod
    async def check_rate_limit() -> bool:
        """Проверяет текущее количество запросов к бекенду чатбота.
        Этот ключ лежит в Redis и увеличивается/уменьшается в зависимости от того,
        Когда совершается непосредственно POST запрос к бекенду чатбота."""

        redis_key, now = await LimiterService.get_redis_key()
        current_count: int | None = await settings.REDIS_CLIENT.get(redis_key)
        if current_count is None:
            return True
        if current_count >= settings.THROTTLING_LIMIT:
            return False
        return True

    @staticmethod
    async def _make_hash(data: dict) -> str:
        """Вычисляет уникальный хеш из всех данных запроса (SHA-256)"""
        return sha256(bytes(str(data), "utf-8")).hexdigest()

    @staticmethod
    async def put_hash_redis(hash: str, ttl: int = settings.CELERY_TASK_ID_TTL) -> bool:
        """Кладет хеш запроса в Redis с TTL"""
        result = await settings.REDIS_CLIENT.setex(
            name=hash, value=1, time=timedelta(seconds=ttl)
        )
        return result

    @staticmethod
    async def check_duplicated_request(hash: str) -> bool:
        """Проверяет хеш, смотрит в Redis БД
        - если находит такой же хеш, то пишет в лог о дубликате запроса"""
        return await settings.REDIS_CLIENT.get(name=hash)

    @staticmethod
    async def process_request(request_data: dict) -> bool | dict:
        """Вычисляет хеш, проверяет нет ли такого же, передает запрос далее"""
        request_hash: str = await LimiterService._make_hash(request_data)
        is_exist = await LimiterService.check_duplicated_request(hash=request_hash)
        if is_exist:
            limiter_logger.info(
                "[LimiterService] Запрос дублируется!", extra={"data": request_data}
            )
            return False
        # Кладем в Redis с TTL
        await LimiterService.put_hash_redis(hash=request_hash)
        limiter_logger.info(
            f"[LimiterService] Получен уникальный запрос, "
            f"хеш запроса отправлен в Redis c TTL {settings.CELERY_TASK_ID_TTL} ",
            extra={"data": request_data},
        )
        return request_data
