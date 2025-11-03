from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime, time, date
from sqlmodel import Session, select
from app.db import get_session
from app.models import AttendanceLog, OfficeLocation, User
from app.utils_geo import haversine_m
from app.integrations_notion import push_attendance_checkin

router = APIRouter(prefix='/attendance', tags=['attendance'])

# IST window
ON_START   = time(9, 20)
GRACE_END  = time(9, 50)

class CheckInIn(BaseModel):
    lat: float
    lng: float
    resync: bool = False

def compute_status(now: datetime) -> str:
    return "ON TIME" if ON_START <= now.time() <= GRACE_END else "LATE"

def nearest_office(session: Session, lat: float, lng: float):
    offices = session.exec(select(OfficeLocation).where(OfficeLocation.is_active == True)).all()
    nearest = None; dist = None; inside = False
    if offices:
        pairs = []
        for o in offices:
            try:
                d = haversine_m(lat, lng, float(o.latitude), float(o.longitude))
                pairs.append((o, d))
            except Exception:
                pass
        if pairs:
            nearest, dist = min(pairs, key=lambda x: x[1])
            inside = dist <= (nearest.radius_m or 300)
    return nearest, dist, inside

@router.post('/check-in')
def check_in(payload: CheckInIn, session: Session = Depends(get_session)):
    user = session.exec(select(User).order_by(User.created_at)).first()
    if not user:
        raise HTTPException(status_code=400, detail='No user found')

    today = date.today()
    log = session.exec(select(AttendanceLog).where(
        AttendanceLog.user_id == user.id, AttendanceLog.date == today
    )).first()

    office, _, inside = nearest_office(session, payload.lat, payload.lng)
    office_name = office.name if office else None
    now = datetime.now()
    status = compute_status(now)

    created = False
    if not log:
        log = AttendanceLog(user_id=user.id, date=today)
        created = True
    if created or not log.check_in_at or payload.resync:
        log.check_in_at = now
        log.check_in_lat = payload.lat
        log.check_in_lng = payload.lng
        session.add(log); session.commit()

    ok, page_id, err = push_attendance_checkin(
        employee_name=user.full_name,
        employee_id='',
        date_iso=today.isoformat(),
        time_hms=now.strftime('%H:%M:%S'),
        status=status,
        office_name=office_name,
        inside_office=inside,
    )

    return {
        'ok': True,
        'created_log': created,
        'inside_office': inside,
        'office_name': office_name,
        'status': status,
        'notion_sync': ok,
        'notion_error': err if not ok else None,
        'notion_page_id': page_id if ok else None
    }

@router.delete('/today')
def delete_today_log(session: Session = Depends(get_session)):
    user = session.exec(select(User).order_by(User.created_at)).first()
    if not user:
        raise HTTPException(status_code=400, detail='No user found')
    today = date.today()
    log = session.exec(select(AttendanceLog).where(
        AttendanceLog.user_id == user.id, AttendanceLog.date == today
    )).first()
    if not log:
        return {'ok': True, 'deleted': False}
    session.delete(log); session.commit()
    return {'ok': True, 'deleted': True}
