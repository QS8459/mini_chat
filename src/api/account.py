from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.db.engine import Session
from src.crud import account as crud
from src.db.model import account as models
from src.schema import account as schemas
router = APIRouter(
    prefix="/account",
    tags=["account"],
)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    try:
        db_account = models.Account(name=account.name)
        return crud.create_account(db=db, account=db_account)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    try:
        db_account = crud.get_account(db=db, account_id=account_id)
        if db_account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        return db_account
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[schemas.Account])
def read_accounts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud.get_accounts(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{account_id}", response_model=schemas.Account)
def update_account(account_id: int, name: str, db: Session = Depends(get_db)):
    try:
        updated_account = crud.update_account(db=db, account_id=account_id, name=name)
        if updated_account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        return updated_account
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{account_id}", response_model=schemas.Account)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    try:
        deleted_account = crud.delete_account(db=db, account_id=account_id)
        if deleted_account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        return deleted_account
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
