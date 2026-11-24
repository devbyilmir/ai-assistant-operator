from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.repositories.conversation import ConversationRepository
from app.services.conversation import ConversationService
from app.repositories.message import MessageRepository
from app.services.message import MessageService


def get_conversation_service(
    session: AsyncSession = Depends(get_session),
) -> ConversationService:
    repository = ConversationRepository(session)

    return ConversationService(repository=repository, session=session)


def get_message_service(
    session: AsyncSession = Depends(get_session),
) -> MessageService:

    conversation_repository = ConversationRepository(session)
    message_repository = MessageRepository(session)

    return MessageService(
        session=session,
        conversation_repository=conversation_repository,
        message_repository=message_repository,
    )
