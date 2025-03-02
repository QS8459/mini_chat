from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Uuid, ForeignKey
from src.db.model.base import BaseModel

from uuid import UUID


class Messages(BaseModel):
    __tablename__ = "messages"
    # __table_ars__ = {"schema": "public"}

    msg: Mapped[str] = mapped_column(String(500), nullable=False)
    chat_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey('chat.id', ondelete="CASCADE"))

    chat: Mapped['Chat'] = relationship("Chat",back_populates='messages')
    owner: Mapped['Account'] = relationship('Account')


__all__ = "Messages"
