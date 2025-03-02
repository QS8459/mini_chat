from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class MessageBaseSchema(BaseModel):
    msg: str
    chat_id: UUID


class MessageAddSchema(MessageBaseSchema):
    pass


class MessageResponseSchema(MessageBaseSchema):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
