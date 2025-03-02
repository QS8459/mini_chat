from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ChatBaseSchema(BaseModel):
    user2_id: UUID

    class Config:
        from_attributes = True


class ChatAddSchema(ChatBaseSchema):
    pass


class ChatResponseSchema(ChatBaseSchema):
    user1_id: UUID
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID | None
