from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DATETIME, Uuid, ForeignKey
from datetime import datetime
from uuid import uuid4, UUID


class BaseModel(DeclarativeBase):

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), default=uuid4, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DATETIME, onupdate=datetime.utcnow(), nullable=False, default=datetime.utcnow())


class BaseMixin(BaseModel, DeclarativeBase):
    created_by: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey('account.id', ondelete="CASCADE"),
        nullable=False)
