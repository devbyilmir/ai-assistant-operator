from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.conversation import Conversation
from ..schemas.conversation import ConversationCreate


class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ConversationCreate):
        conversation = Conversation(
            customer_id=data.customer_id,
            operator_id=data.operator_id,
        )
        self.session.add(conversation)
        await self.session.flush()

        return conversation

    async def get_by_id(self, conversation_id: UUID) -> Conversation | None:
        # stmt = select(Conversation).where(Conversation.id == conversation_id)
        stmt = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_status(
        self, conversation_id: UUID, status: str
    ) -> Conversation | None:
        stmt = (
            update(Conversation)
            .where(Conversation.id == conversation_id)
            .values(status=status)
            .returning(Conversation)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
