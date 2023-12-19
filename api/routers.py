from fastapi import APIRouter

from api.endpoints import webhook

api_router = APIRouter()
api_router.include_router(webhook.router, prefix="/webhook", tags=["viber_webhook"])
