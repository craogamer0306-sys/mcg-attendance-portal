from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models import User
from app.security import verify_password, hash_password
from app.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/change-password")
def change_password(old_password: str, new_password: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    user = session.get(User, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Old password incorrect")
    user.password_hash = hash_password(new_password)
    session.add(user)
    session.commit()
    return {"ok": True, "message": "Password changed successfully"}
