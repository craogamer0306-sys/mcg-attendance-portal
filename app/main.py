from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from .settings import get_settings
from .db import init_db, Session, engine
from .models import User
from .security import hash_password
from .routers import auth, tasks, attendance, debug, locations, change_password
from fastapi.staticfiles import StaticFiles

settings = get_settings()
app = FastAPI(title='MCG Attendance Portal (MVP)')

origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(',')]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
def on_startup():
    init_db()
    with Session(engine) as session:
        admin = session.exec(select(User)).first()
        if not admin:
            u = User(
                full_name='Admin',
                email='admin@mcg.local',
                role='ADMIN',
                password_hash=hash_password('admin12345')
            )
            session.add(u)
            session.commit()

@app.get('/health')
def health():
    return {'ok': True}

# Routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(attendance.router)
app.include_router(locations.router)
app.include_router(debug.router)
app.include_router(change_password.router)

# âœ… Serve frontend (React build)
import os

# Serve frontend only in local/dev when web/dist exists.
if os.path.isdir('web/dist'):
    
