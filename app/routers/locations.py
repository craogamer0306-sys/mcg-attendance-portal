from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from typing import List
from uuid import UUID
from sqlmodel import Session, select
from ..db import get_session
from ..models import OfficeLocation

router = APIRouter(prefix="/locations", tags=["locations"])

class LocationIn(BaseModel):
    name: str
    latitude: float
    longitude: float
    radius_m: int = 300
    is_active: bool = True

class LocationOut(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    radius_m: int
    is_active: bool

@router.get("", response_model=List[LocationOut])
def list_locations(session: Session = Depends(get_session)):
    locs = session.exec(select(OfficeLocation).order_by(OfficeLocation.created_at)).all()
    return [
        {
            "id": str(l.id),
            "name": l.name,
            "latitude": float(l.latitude),
            "longitude": float(l.longitude),
            "radius_m": l.radius_m or 300,
            "is_active": bool(l.is_active),
        } for l in locs
    ]

@router.post("", response_model=LocationOut)
def create_location(payload: LocationIn, session: Session = Depends(get_session)):
    loc = OfficeLocation(
        name=payload.name,
        latitude=payload.latitude,
        longitude=payload.longitude,
        radius_m=payload.radius_m,
        is_active=payload.is_active,
    )
    session.add(loc); session.commit(); session.refresh(loc)
    return {
        "id": str(loc.id),
        "name": loc.name,
        "latitude": float(loc.latitude),
        "longitude": float(loc.longitude),
        "radius_m": loc.radius_m or 300,
        "is_active": bool(loc.is_active),
    }

@router.delete("/{location_id}")
def delete_location(
    location_id: str = Path(..., description="UUID of the location to delete"),
    session: Session = Depends(get_session),
):
    try:
        loc_uuid = UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    loc = session.get(OfficeLocation, loc_uuid)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    session.delete(loc)
    session.commit()
    return {"ok": True}

@router.post("/{location_id}/deactivate")
def deactivate_location(
    location_id: str = Path(..., description="UUID of the location to deactivate"),
    session: Session = Depends(get_session),
):
    try:
        loc_uuid = UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    loc = session.get(OfficeLocation, loc_uuid)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    loc.is_active = False
    session.add(loc); session.commit()
    return {"ok": True, "id": str(loc.id), "is_active": False}
