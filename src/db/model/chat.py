from sqlalchemy import Table, Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.orm import relationship
from src.db.engine import Base
from datetime import datetime


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    chat_name = Column(String, nullable=False)
    owner1_id = Column(Integer, ForeignKey('account.id'))
    owner2_id = Column(Integer, ForeignKey('account.id'))
    created_at = Column(DATETIME, default=datetime.utcnow())

    owner1 = relationship('Account', foreign_keys=[owner1_id])
    owner2 = relationship('Account', foreign_keys=[owner2_id])

__all__ = 'Chat'