from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from .message import MessageRead


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    operator_id: UUID | None
    status: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageRead] = Field(default_factory=list)


class ConversationCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: UUID
    operator_id: UUID | None = None
