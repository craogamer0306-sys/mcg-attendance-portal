
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
