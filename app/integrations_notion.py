
import os, requests
from .settings import get_settings

settings = get_settings()
BASE = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {settings.NOTION_TOKEN}" if settings.NOTION_TOKEN else "",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def push_task(task: dict) -> str | None:
    """Creates/updates a page for a DailyTask. Returns page_id or None if not configured."""
    if not (settings.NOTION_TOKEN and settings.NOTION_DB_ID):
        return None
    properties = {
        "Title": {"title": [{"text": {"content": task.get("title") or f"Daily tasks – {task['date']}"}}]},
        "Date": {"date": {"start": task["date"]}},
        "Employee": {"rich_text": [{"text": {"content": task.get("employee","")}}]},
        "Notes": {"rich_text": [{"text": {"content": (task.get("notes") or "")[:1800]}}]},
        "Hours": {"number": float(task.get("hours_spent")) if task.get("hours_spent") else None},
    }
    payload = {"parent": {"database_id": settings.NOTION_DB_ID}, "properties": properties}
    r = requests.post(f"{BASE}/pages", headers=HEADERS, json=payload, timeout=30)
    r.raise_for_status()
    return r.json().get("id")
