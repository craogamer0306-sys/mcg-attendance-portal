
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from sqlmodel import Session, select
from ..db import get_session
from ..models import DailyTask, User
from ..integrations_notion import push_task

router = APIRouter(prefix="/tasks", tags=["tasks"])

class TaskIn(BaseModel):
    date: date
    title: Optional[str] = None
    notes: Optional[str] = None
    hours_spent: Optional[float] = Field(default=None, ge=0)

@router.post("")
def create_task(payload: TaskIn, session: Session = Depends(get_session)):
    # For MVP, we'll attach task to the first user (admin). In real app, use auth identity.
    user = session.exec(select(User).order_by(User.created_at)).first()
    if not user:
        raise HTTPException(status_code=400, detail="No users found; register or seed admin first.")
    t = DailyTask(user_id=user.id, date=payload.date, title=payload.title, notes=payload.notes, hours_spent=payload.hours_spent)
    session.add(t); session.commit(); session.refresh(t)
    # Try pushing to Notion (if configured)
    try:
        push_task({
            "title": t.title,
            "date": t.date.isoformat(),
            "employee": user.full_name,
            "notes": t.notes or "",
            "hours_spent": t.hours_spent,
        })
    except Exception as e:
        # Non-fatal
        pass
    return {"ok": True, "task_id": str(t.id)}

@router.get("")
def list_tasks(session: Session = Depends(get_session)) -> list[dict]:
    tasks = session.exec(select(DailyTask).order_by(DailyTask.created_at.desc())).all()
    return [{
        "id": str(t.id), "date": t.date.isoformat(), "title": t.title, "notes": t.notes, "hours_spent": t.hours_spent
    } for t in tasks]
