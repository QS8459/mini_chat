from sqlalchemy.orm import Session
from src.db.model import Messages
from datetime import datetime

def get_message(db: Session, message_id: int):
    return db.query(Messages).filter(Messages.id == message_id).first()

def get_messages(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Messages).offset(skip).limit(limit).all()

def create_message(db: Session, message: Messages):
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def update_message(db: Session, message_id: int, msg: str):
    message = db.query(Messages).filter(Messages.id == message_id).first()
    if message:
        message.msg = msg
        message.created_at = datetime.utcnow()
        db.commit()
        db.refresh(message)
    return message

def delete_message(db: Session, message_id: int):
    message = db.query(Messages).filter(Messages.id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
    return message
