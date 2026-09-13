from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import LoginRequest, LoginResponse, UserOut
from auth_utils import verify_password
import crud.user as user_crud

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db, credentials.username)

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return user

from schemas.user import UserOut

@router.get("/users", response_model=list[UserOut])
def list_users(role: str = None, db: Session = Depends(get_db)):
    return user_crud.get_users(db, role)