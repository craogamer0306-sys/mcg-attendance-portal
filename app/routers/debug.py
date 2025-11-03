from fastapi import APIRouter
from datetime import date, datetime
import requests
from app.settings import get_settings

router = APIRouter(prefix="/debug", tags=["debug"])
s = get_settings()

BASE = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {s.NOTION_TOKEN}" if s.NOTION_TOKEN else "",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

@router.post("/notion/tasks")
def debug_notion_tasks():
    if not (s.NOTION_TOKEN and s.NOTION_TASKS_DB_ID):
        return {"ok": False, "msg": "Missing NOTION_TOKEN or NOTION_TASKS_DB_ID in .env"}
    payload = {
        "parent": {"database_id": s.NOTION_TASKS_DB_ID},
        "properties": {
            # Title will be auto-detected in the integration function normally,
            # but here we just test creation with a basic title name 'Name' or 'Employee'.
            "Name": {"title": [{"text": {"content": "Debug Bot"}}]},
        },
    }
    # Try again if 'Name' isn't the title by sending minimal properties only (Notion ignores extras)
    r = requests.post(f"{BASE}/pages", headers=HEADERS, json=payload, timeout=30)
    if not r.ok:
        # Fallback: try 'Employee' as title
        payload["properties"] = {"Employee": {"title": [{"text": {"content": "Debug Bot"}}]}}
        r = requests.post(f"{BASE}/pages", headers=HEADERS, json=payload, timeout=30)
    return {"ok": r.ok, "status": r.status_code, "resp": r.json() if r.content else None}

@router.post("/notion/attendance")
def debug_notion_attendance():
    if not (s.NOTION_TOKEN and s.NOTION_ATT_DB_ID):
        return {"ok": False, "msg": "Missing NOTION_TOKEN or NOTION_ATT_DB_ID in .env"}
    now = datetime.now()
    payload = {
        "parent": {"database_id": s.NOTION_ATT_DB_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": "Debug Bot"}}]},
        },
    }
    r = requests.post(f"{BASE}/pages", headers=HEADERS, json=payload, timeout=30)
    if not r.ok:
        payload["properties"] = {"Employee Name": {"title": [{"text": {"content": "Debug Bot"}}]}}
        r = requests.post(f"{BASE}/pages", headers=HEADERS, json=payload, timeout=30)
    return {"ok": r.ok, "status": r.status_code, "resp": r.json() if r.content else None}

@router.get("/notion/tasks/list")
def list_notion_tasks():
    if not (s.NOTION_TOKEN and s.NOTION_TASKS_DB_ID):
        return {"ok": False, "msg": "Missing NOTION_TOKEN or NOTION_TASKS_DB_ID"}
    q = {"page_size": 5, "sorts": [{"timestamp": "created_time", "direction": "descending"}]}
    r = requests.post(f"{BASE}/databases/{s.NOTION_TASKS_DB_ID}/query", headers=HEADERS, json=q, timeout=30)
    return {"ok": r.ok, "status": r.status_code, "resp": r.json() if r.content else None}

@router.get("/notion/attendance/list")
def list_notion_attendance():
    if not (s.NOTION_TOKEN and s.NOTION_ATT_DB_ID):
        return {"ok": False, "msg": "Missing NOTION_TOKEN or NOTION_ATT_DB_ID"}
    q = {"page_size": 5, "sorts": [{"timestamp": "created_time", "direction": "descending"}]}
    r = requests.post(f"{BASE}/databases/{s.NOTION_ATT_DB_ID}/query", headers=HEADERS, json=q, timeout=30)
    return {"ok": r.ok, "status": r.status_code, "resp": r.json() if r.content else None}
