from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.db.engine import Session
from src.db.model import message as models
from src.crud import message as crud
from src.schema import message as schemas

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Message)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    try:
        db_message = models.Messages(
            msg=message.msg,
            chat_id=message.chat_id,
            owner_id=message.owner_id
        )
        return crud.create_message(db=db, message=db_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{message_id}", response_model=schemas.Message)
def read_message(message_id: int, db: Session = Depends(get_db)):
    try:
        db_message = crud.get_message(db=db, message_id=message_id)
        if db_message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return db_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.Message])
def read_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud.get_messages(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{message_id}", response_model=schemas.Message)
def update_message(message_id: int, msg: str, db: Session = Depends(get_db)):
    try:
        updated_message = crud.update_message(db=db, message_id=message_id, msg=msg)
        if updated_message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return updated_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{message_id}", response_model=schemas.Message)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    try:
        deleted_message = crud.delete_message(db=db, message_id=message_id)
        if deleted_message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return deleted_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
