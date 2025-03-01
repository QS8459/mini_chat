from pydantic import BaseModel

# Schemas for Chat
class ChatBase(BaseModel):
    chat_name: str
    owner1_id: int
    owner2_id: int

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int

    class Config:
        from_attributes = True
