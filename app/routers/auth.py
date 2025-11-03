
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel import select, Session
from ..db import get_session
from ..models import User
from ..security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(payload: RegisterIn, session: Session = Depends(get_session)):
    exists = session.exec(select(User).where(User.email == payload.email)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    u = User(full_name=payload.full_name, email=payload.email, password_hash=hash_password(payload.password), role="EMPLOYEE")
    session.add(u); session.commit()
    return {"ok": True}

@router.post("/login")
def login(payload: LoginIn, session: Session = Depends(get_session)):
    u = session.exec(select(User).where(User.email == payload.email)).first()
    if not u or not verify_password(payload.password, u.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(str(u.id))
    return {"access_token": token, "token_type": "bearer", "user": {"name": u.full_name, "role": u.role}}
