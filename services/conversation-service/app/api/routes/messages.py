from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from ..dependencies import get_message_service
from app.services.message import MessageService
from app.schemas.message import MessageRead, MessageCreate
from app.models.message import Message

router = APIRouter(
    prefix="/conversations",
    tags=["messages"],
)


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageRead,
    status_code=201,
)
async def create_message(
    conversation_id: UUID,
    data: MessageCreate,
    service: MessageService = Depends(get_message_service),
):
    return await service.create_message(conversation_id=conversation_id, data=data)


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageRead],
    # status_code=201,
)
async def get_messages(
    conversation_id: UUID,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: MessageService = Depends(get_message_service),
) -> list[Message]:
    return await service.get_messages(
        conversation_id=conversation_id,
        limit=limit,
        offset=offset,
    )
