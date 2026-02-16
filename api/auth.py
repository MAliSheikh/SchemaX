from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.dependency import get_db
from schemas.users import UserCreate
from core.security import create_access_token, create_refresh_token, verify_refresh_token
from db import crud

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserCreate)
def register(
    user: UserCreate, 
    db: Session = Depends(get_db),
):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not db_user:
        raise HTTPException(401, "Invalid credentials")

    access_token = create_access_token({"sub": db_user.email, "role": db_user.role})
    refresh_token = create_refresh_token({"sub": db_user.email, "role": db_user.role})

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh_token(data: RefreshRequest):
    try:
        payload = verify_refresh_token(data.refresh_token)
    except Exception:
        raise HTTPException(401, "Invalid refresh token")

    email = payload.get("sub")
    role = payload.get("role")

    if email is None:
        raise HTTPException(401, "Invalid token payload")

    new_access = create_access_token({"sub": email, "role": role})

    return {"access_token": new_access, "token_type": "bearer"}