from fastapi import APIRouter

from app.api.routes.conversations import router as conversations_router
from app.api.routes.messages import router as messages_router

api_router = APIRouter()

api_router.include_router(conversations_router)
api_router.include_router(messages_router)