from hashlib import sha256


class LimiterService:
    @staticmethod
    def check_rate_limit():
        """Проверяет текущее количество запущенных тасок.
        Этот ключ лежит в Redis и увеличивается/уменьшается в зависимости от того,
        Выполнена таска или только поступила."""

    @staticmethod
    def _make_hash(data: dict) -> str:
        """Вычисляет уникальный хеш из всех данных запроса (SHA-256)"""
        return sha256(bytes(str(data), "utf-8")).hexdigest()

    @staticmethod
    def check_duplicated_request():
        """Вычисляет хеш всех полей запроса, смотрит в Redis БД
        - если находит такой же хеш, то пишет в лог о дубликате запроса
        (и не вызывает передачу запроса в очеред Rabbit MQ)
        - если не находит такой же хеш, то делает хеш, кладет в Redis с TTL
        (вызывает передачу запроса в очередь)"""

    @staticmethod
    def process_request():
        """Сначала делает хеш, проверяет нет ли такого же,
        затем отправляет запрос в очередь"""
