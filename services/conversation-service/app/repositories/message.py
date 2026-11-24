from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from ..models.message import Message
from ..schemas.message import MessageCreate


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(
        self, conversation_id: UUID, data: MessageCreate
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=data.role,
            content=data.content,
        )

        self.session.add(message)
        await self.session.flush()

        return message

    async def get_messages(
        self,
        conversation_id: UUID,
        limit: int,
        offset: int,
    ):
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at, Message.id)
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()
