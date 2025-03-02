from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Uuid, UniqueConstraint
from src.db.model.base import BaseModel
from uuid import UUID


class Chat(BaseModel):

    __tablename__ = "chat"
    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="unique_private_chat"),
        # {"schema": "public"}
    )

    user1_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey('account.id', ondelete="CASCADE"))
    user2_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey('account.id', ondelete="CASCADE"))

    user1: Mapped['Account'] = relationship('Account', foreign_keys=[user1_id])
    user2: Mapped['Account'] = relationship('Account', foreign_keys=[user2_id])
    messages: Mapped['Messages'] = relationship("Messages", back_populates="chat", cascade="all, delete-orphan")


__all__ = ["Chat"]
