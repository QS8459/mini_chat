from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.db.model.base import BaseModel
from passlib.hash import pbkdf2_sha256 as sha256
from typing import List


class Account(BaseModel):
    __tablename__ = 'account'
    # __table_args__ = {"schema": "public"}

    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(500), nullable=False)

    chats_as_user1: Mapped[List['Chat']] = relationship('Chat', foreign_keys='Chat.user1_id', back_populates="user1")
    chats_as_user2: Mapped[List['Chat']] = relationship('Chat', foreign_keys='Chat.user2_id', back_populates="user2")

    def set_pwd(self, password: str) -> None:
        self.password = sha256.hash(password)
        return None

    def ver_pwd(self, password: str) -> bool:
        return sha256.verify(password, self.password)


__all__ = ["Account"]
