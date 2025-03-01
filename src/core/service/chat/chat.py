from sqlalchemy.orm import Session
from src.db.model import Chat


# CRUD functions for Chat
def get_chat(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()

def get_chats(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Chat).offset(skip).limit(limit).all()

def create_chat(db: Session, chat: Chat):
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def update_chat(db: Session, chat_id: int, chat_name: str, owner1_id: int, owner2_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        chat.chat_name = chat_name
        chat.owner1_id = owner1_id
        chat.owner2_id = owner2_id
        db.commit()
        db.refresh(chat)
    return chat

def delete_chat(db: Session, chat_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        db.delete(chat)
        db.commit()
    return chat
