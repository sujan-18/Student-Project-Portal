from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User


def get_current_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user_id")
    return user