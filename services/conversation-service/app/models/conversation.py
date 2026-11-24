from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4
from sqlalchemy import DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .message import Message


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)

    customer_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)

    operator_id: Mapped[UUID | None] = mapped_column(Uuid, nullable=True)

    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Каждое сообщение ссылается на один диалог через conversation_id
    messages: Mapped[List["Message"]] = relationship(back_populates="conversation")