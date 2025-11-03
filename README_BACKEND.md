# Backend (FastAPI) — Quick Start

## 1) Install deps
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 2) Create `.env`
Copy `.env.example` to `.env` and fill NOTION_TOKEN / NOTION_DB_ID later.

If `DATABASE_URL` is empty, the app will auto-fallback to SQLite file `dev.db`.

## 3) Run
```
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs

## Seed login
On first run, the app ensures an admin user:
- email: admin@mcg.local
- password: admin12345
(change immediately via /auth/change-password)
