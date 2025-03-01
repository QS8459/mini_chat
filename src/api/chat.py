from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.db.engine import Session
from src.core.service.chat import chat as crud
from src.core.schema import chat as schemas
from src.db.model import chat as models

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Chat)
def create_chat(chat: schemas.ChatCreate, db: Session = Depends(get_db)):
    try:
        db_chat = models.Chat(
            chat_name=chat.chat_name,
            owner1_id=chat.owner1_id,
            owner2_id=chat.owner2_id
        )
        return crud.create_chat(db=db, chat=db_chat)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{chat_id}", response_model=schemas.Chat)
def read_chat(chat_id: int, db: Session = Depends(get_db)):
    try:
        db_chat = crud.get_chat(db=db, chat_id=chat_id)
        if db_chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        return db_chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.Chat])
def read_chats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud.get_chats(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{chat_id}", response_model=schemas.Chat)
def update_chat(chat_id: int, chat_name: str, owner1_id: int, owner2_id: int, db: Session = Depends(get_db)):
    try:
        updated_chat = crud.update_chat(db=db, chat_id=chat_id, chat_name=chat_name, owner1_id=owner1_id, owner2_id=owner2_id)
        if updated_chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        return updated_chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{chat_id}", response_model=schemas.Chat)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    try:
        deleted_chat = crud.delete_chat(db=db, chat_id=chat_id)
        if deleted_chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        return deleted_chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
