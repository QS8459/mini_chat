from sqlalchemy import Table, Column, Integer, String, DATETIME
from src.db.engine import Base
from datetime import datetime


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DATETIME, default=datetime.utcnow())

__all__ = 'Account'