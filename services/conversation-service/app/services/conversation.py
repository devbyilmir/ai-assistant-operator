from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.conversation import Conversation
from ..repositories.conversation import ConversationRepository
from ..schemas.conversation import ConversationCreate


class ConversationService:
    def __init__(self, repository: ConversationRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def create_conversation(self, data: ConversationCreate):
        async with self.session.begin():
            return await self.repository.create(data)

    async def get_conversation(self, conversation_id: UUID) -> Conversation | None:
        result = await self.repository.get_by_id(conversation_id)

        if result is None:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return result

    async def close_conversation(self, conversation_id: UUID) -> None:
        async with self.session.begin():
            conversation = await self.repository.get_by_id(conversation_id)

            if conversation is None:
                raise HTTPException(status_code=404, detail="Conversation not found")

            if conversation.status == "closed":
                return conversation

            return await self.repository.update_status(conversation_id, "closed")