import requests
from typing import Dict, Any, Optional
from .settings import get_settings

s = get_settings()
BASE = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {s.NOTION_TOKEN}" if s.NOTION_TOKEN else "",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def _get_db(db_id: str) -> Dict[str, Any]:
    r = requests.get(f"{BASE}/databases/{db_id}", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

def _title_prop(db: Dict[str, Any]) -> Optional[str]:
    for k, v in db.get("properties", {}).items():
        if v.get("type") == "title":
            return k
    return None

def _has_prop(db: Dict[str, Any], name: str, types: list[str] | None = None) -> Optional[str]:
    """Return type if property exists (and optionally matches allowed types)."""
    props = db.get("properties", {})
    if name not in props:
        return None
    ptype = props[name].get("type")
    if types and ptype not in types:
        return None
    return ptype

def _status_payload(ptype: str, value: str) -> Dict[str, Any]:
    # Support Notion 'status' or 'select'
    if ptype == "status":
        return {"status": {"name": value}}
    if ptype == "select":
        return {"select": {"name": value}}
    # Fallback: rich_text if schema is unusual
    return {"rich_text": [{"text": {"content": value}}]}

def _post_page(payload: Dict[str, Any]) -> tuple[bool, Optional[str], Optional[str]]:
    r = requests.post(f"{BASE}/pages", headers=HEADERS, json=payload, timeout=30)
    if not r.ok:
        # return ok, page_id, error
        return False, None, r.text
    return True, r.json().get("id"), None

# ---------------- Daily Task ----------------
def push_daily_task(*, date_iso: str, employee_name: str,
                    employee_id: str | None, title: str | None,
                    description: str | None) -> tuple[bool, Optional[str], Optional[str]]:
    db_id = s.NOTION_TASKS_DB_ID
    if not (s.NOTION_TOKEN and db_id):
        return False, None, "Missing NOTION token or TASKS DB ID"

    db = _get_db(db_id)
    title_key = _title_prop(db)
    if not title_key:
        return False, None, "No Title property in Daily Task DB"

    props: Dict[str, Any] = {
        title_key: {"title": [{"text": {"content": employee_name or "Employee"}}]},
    }

    # Add optional props only if present in DB schema
    if _has_prop(db, "Date", ["date"]):
        props["Date"] = {"date": {"start": date_iso}}
    if _has_prop(db, "Task Title", ["rich_text", "title"]):
        # prefer rich_text, but if it's title we still feed title payload
        ptype = _has_prop(db, "Task Title", None)
        if ptype == "title":
            props["Task Title"] = {"title": [{"text": {"content": title or f"Daily tasks – {date_iso}"}}]}
        else:
            props["Task Title"] = {"rich_text": [{"text": {"content": title or f"Daily tasks – {date_iso}"}}]}
    if _has_prop(db, "Task Description", ["rich_text"]):
        props["Task Description"] = {"rich_text": [{"text": {"content": (description or "")[:1800]}}]}
    if employee_id and _has_prop(db, "Employee ID", ["rich_text"]):
        props["Employee ID"] = {"rich_text": [{"text": {"content": employee_id}}]}
    stype = _has_prop(db, "Status", ["status", "select"])
    if stype:
        props["Status"] = _status_payload(stype, "Done")

    payload = {"parent": {"database_id": db_id}, "properties": props}
    return _post_page(payload)

# ---------------- Attendance ----------------
def push_attendance_checkin(*, employee_name: str, employee_id: str | None,
                            date_iso: str, time_hms: str, status: str,
                            office_name: str | None, inside_office: bool
                            ) -> tuple[bool, Optional[str], Optional[str]]:
    db_id = s.NOTION_ATT_DB_ID
    if not (s.NOTION_TOKEN and db_id):
        return False, None, "Missing NOTION token or ATTENDANCE DB ID"

    db = _get_db(db_id)
    title_key = _title_prop(db)
    if not title_key:
        return False, None, "No Title property in Attendance DB"

    props: Dict[str, Any] = {
        title_key: {"title": [{"text": {"content": employee_name or "Employee"}}]},
    }

    if _has_prop(db, "Date", ["date"]):
        props["Date"] = {"date": {"start": date_iso}}
    if _has_prop(db, "Time", ["rich_text"]):
        props["Time"] = {"rich_text": [{"text": {"content": time_hms}}]}
    stype = _has_prop(db, "Status", ["status", "select"])
    if stype:
        props["Status"] = _status_payload(stype, status)
    if _has_prop(db, "Inside Office", ["checkbox"]):
        props["Inside Office"] = {"checkbox": bool(inside_office)}
    if office_name and _has_prop(db, "Office Name", ["rich_text"]):
        props["Office Name"] = {"rich_text": [{"text": {"content": office_name}}]}
    if employee_id and _has_prop(db, "Employee ID", ["rich_text"]):
        props["Employee ID"] = {"rich_text": [{"text": {"content": employee_id}}]}

    payload = {"parent": {"database_id": db_id}, "properties": props}
    return _post_page(payload)
