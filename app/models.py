
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
import uuid

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str
    email: str = Field(index=True, unique=True)
    role: str = Field(default="ADMIN")  # ADMIN / EMPLOYEE
    password_hash: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OfficeLocation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    latitude: float
    longitude: float
    radius_m: int = 200
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AttendanceLog(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    date: date
    check_in_at: Optional[datetime] = None
    check_out_at: Optional[datetime] = None
    check_in_lat: Optional[float] = None
    check_in_lng: Optional[float] = None
    check_out_lat: Optional[float] = None
    check_out_lng: Optional[float] = None
    check_in_location_id: Optional[uuid.UUID] = Field(default=None, foreign_key="officelocation.id")
    check_out_location_id: Optional[uuid.UUID] = Field(default=None, foreign_key="officelocation.id")
    source: str = "WEB"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DailyTask(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    date: date
    title: Optional[str] = None
    notes: Optional[str] = None
    hours_spent: Optional[float] = None
    notion_page_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
