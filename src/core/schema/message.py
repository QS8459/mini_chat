from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    msg: str
    chat_id: int
    owner_id: int

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
