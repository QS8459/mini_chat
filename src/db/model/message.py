from sqlalchemy import Table, Column, Integer, TEXT, DATETIME, ForeignKey
from sqlalchemy.orm import relationship
from src.db.engine import Base
from datetime import datetime


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    msg = Column(TEXT, nullable=False)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    created_at = Column(DATETIME, default=datetime.utcnow)

    chat = relationship('Chat')
    owner = relationship('Account')


__all__ = "Messages"
