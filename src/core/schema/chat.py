from pydantic import BaseModel
from uuid import UUID


class ChatBaseSchema(BaseModel):
    user1_id: UUID
    user2_id: UUID

    class Config:
        from_attributes = True


class ChatAddSchema(ChatBaseSchema):
    pass
