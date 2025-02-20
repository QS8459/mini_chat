from sqlalchemy.orm import Session
from src.db.model import Account


def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Account).offset(skip).limit(limit).all()


def create_account(db: Session, account: Account):
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def update_account(db: Session, account_id: int, name: str):
    user = db.query(Account).filter(Account.id == account_id).first()
    if user:
        user.name = name
        db.commit()
        db.refresh(user)
    return user


def delete_account(db: Session, account_id: int):
    user = db.query(Account).filter(Account.id == account_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
