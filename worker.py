from celery import Celery

from settings.config import settings

# TODO: прописать конфиг для очередей, добавить в *.compose,
#  сейчас есть high_priority очередь на всякий случай
celery = Celery(__name__, include=["tasks.request_tasks"])
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
