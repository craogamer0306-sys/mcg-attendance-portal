
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import get_settings
from .db import init_db, Session, engine
from sqlmodel import select
from .models import User
from .security import hash_password
from .routers import auth, tasks

settings = get_settings()
app = FastAPI(title="MCG Attendance Portal (MVP)")

# CORS
origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()
    # seed admin if none
    with Session(engine) as session:
        admin = session.exec(select(User)).first()
        if not admin:
            u = User(full_name="Admin", email="admin@mcg.local", role="ADMIN", password_hash=hash_password("admin12345"))
            session.add(u); session.commit()

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(auth.router)
app.include_router(tasks.router)
