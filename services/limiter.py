class LimiterService:
    @staticmethod
    def _make_hash(data: dict):
        """Вычисляет уникальный хеш из всех данных запроса (SHA-256)"""

    @staticmethod
    def check_duplicated_request():
        """Вычисляет хеш всех полей запроса, смотрит в Redis БД
        - если находит такой же хеш, то пишет в лог о дубликате запроса
        (и не вызывает передачу запроса в очеред Rabbit MQ)
        - если не находит такой же хеш, то делает хеш, кладет в Redis с TTL
        (вызывает передачу запроса в очеред Rabbit MQ)"""

    @staticmethod
    def process_request():
        """Сначала делает хеш, проверяет нет ли такого же,
        затем отправляет запрос в очередь Rabbit MQ"""
