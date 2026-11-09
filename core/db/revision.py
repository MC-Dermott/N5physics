"""Pupil revision guide rows (table revision_guide, filled by sync_revision_guide.py)."""
from core.db.client import get_supabase

STATUS_ORDER = ["focus", "developing", "secure", "strong", "not_yet"]


def fetch_guide(user_id: str):
    """[(row dict)] for this pupil, weakest first, or None if the table doesn't exist yet."""
    try:
        rows = (get_supabase().table("revision_guide").select("*").eq("user_id", user_id).execute().data or [])
    except Exception:
        return None
    rows.sort(key=lambda r: (r["qualification"], r["rank"]))
    return rows
