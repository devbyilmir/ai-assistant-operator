from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.message import MessageRepository
from ..repositories.conversation import ConversationRepository
from ..schemas.message import MessageCreate


class MessageService:
    def __init__(
        self,
        session: AsyncSession,
        message_repository: MessageRepository,
        conversation_repository: ConversationRepository,
    ):
        self.session = session
        self.message_repository = message_repository
        self.conversation_repository = conversation_repository

    async def create_message(self, conversation_id: UUID, data: MessageCreate):
        async with self.session.begin():
            conversation = await self.conversation_repository.get_by_id(conversation_id)

            if conversation is None:
                raise HTTPException(status_code=404, detail="The dialogue not found")

            message = await self.message_repository.create_message(
                conversation_id=conversation_id,
                data=data,
            )

            return message

    async def get_messages(
        self, 
        conversation_id: UUID,
        limit: int,
        offset: int,
    ):
        async with self.session.begin():
            conversation = await self.conversation_repository.get_by_id(conversation_id)
            
            if conversation is None:
                raise HTTPException(status_code=404, detail="The dialogue not found")

            messages = await self.message_repository.get_messages(
                conversation_id=conversation_id,
                limit=limit,
                offset=offset,
            )

            return messages