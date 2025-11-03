
from passlib.hash import argon2
from datetime import datetime, timedelta
from jose import jwt
from .settings import get_settings

settings = get_settings()

def hash_password(p: str) -> str:
    return argon2.hash(p)

def verify_password(p: str, h: str) -> bool:
    try:
        return argon2.verify(p, h)
    except Exception:
        return False

def create_access_token(sub: str, expires_minutes: int = 60) -> str:
    payload = {
        "sub": sub,
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes),
        "type": "access",
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.settings import get_settings
from app.models import User
from app.db import Session, engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            raise credentials_exception
        return user
