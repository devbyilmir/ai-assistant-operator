from uuid import UUID
from fastapi import APIRouter, Depends

from ..dependencies import get_conversation_service
from app.services.conversation import ConversationService
from app.schemas.conversation import ConversationRead, ConversationCreate

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)


@router.get("/{conversation_id}", response_model=ConversationRead)
async def get_conversation(
    conversation_id: UUID,
    service: ConversationService = Depends(get_conversation_service),
):
    return await service.get_conversation(conversation_id)


@router.patch("/{conversation_id}/close", response_model=ConversationRead)
async def update_conversation(
    conversation_id: UUID,
    service: ConversationService = Depends(get_conversation_service),
):
    return await service.close_conversation(conversation_id)


@router.post("/", response_model=ConversationRead, status_code=201)
async def create_conversation(
    data: ConversationCreate,
    service: ConversationService = Depends(get_conversation_service),
):
    return await service.create_conversation(data)
