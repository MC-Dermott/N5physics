"""Part-finished assignment tests, so a pupil can leave and Continue later (or Start over).

The test session dict is stored as JSON in `assignment_progress`, one row per pupil per assignment item
(migration 2026-10-26). A test keeps each question's response in test["responses"] until it ends, so that is
what is saved: the questions as generated, the pupil's response to every question already left, and the position.
Each response refers to a question (or one part of a scenario) by position, so it is rebuilt from the questions.
Everything is best-effort: if the table is missing the test still works, it just can't be resumed."""
from datetime import datetime, timezone

from core.db.client import get_supabase
from core.db.reviews import _decode, _encode, question_from_json, question_to_json

TABLE = "assignment_progress"


def _scored_parts(question):
    return [p for p in question.parts if p.metadata.get("type") != "explain"]


def _targets(question):
    """What each saved response belongs to: the question itself, or each scored part of a scenario."""
    return _scored_parts(question) if question.is_scenario else [question]


def progress_to_json(test):
    return {"questions": [question_to_json(q) for q in test["questions"]], "index": test["index"],
            "responses": {str(i): [[display, result, _encode(distractor), _encode(raw)]
                                   for display, result, distractor, _q, raw in rs]
                          for i, rs in test["responses"].items()}}


def progress_from_json(payload):
    """A test session dict ready for st.session_state."""
    questions = [question_from_json(q) for q in payload["questions"]]
    responses = {}
    for key, rs in payload["responses"].items():
        i = int(key)
        if i < len(questions):
            responses[i] = [(display, result, _decode(distractor), target, _decode(raw))
                            for (display, result, distractor, raw), target in zip(rs, _targets(questions[i]))]
    return {"questions": questions, "index": min(payload.get("index", 0), len(questions) - 1), "answers": [],
            "results": [], "feedback": [], "responses": responses, "complete": False, "saved": False}


def answered_count(test):
    return len(test.get("responses") or {})


def save_progress(user_id, item_id, test):
    try:
        get_supabase().table(TABLE).upsert(
            {"user_id": user_id, "assignment_item_id": item_id, "q_index": test["index"],
             "q_total": len(test["questions"]), "payload": progress_to_json(test),
             "updated_at": datetime.now(timezone.utc).isoformat()}, on_conflict="user_id,assignment_item_id").execute()
        return True
    except Exception:
        return False


def load_progress(user_id, item_id):
    """A test session dict, or None."""
    try:
        rows = (get_supabase().table(TABLE).select("payload").eq("user_id", user_id)
                .eq("assignment_item_id", item_id).execute().data or [])
        return progress_from_json(rows[0]["payload"]) if rows else None
    except Exception:
        return None


def delete_progress(user_id, item_id):
    try:
        get_supabase().table(TABLE).delete().eq("user_id", user_id).eq("assignment_item_id", item_id).execute()
    except Exception:
        pass


def progress_summaries(user_id):
    """{assignment_item_id: {"index", "total"}} for the pupil's My Assignments page."""
    try:
        rows = (get_supabase().table(TABLE).select("assignment_item_id,q_index,q_total")
                .eq("user_id", user_id).execute().data or [])
    except Exception:
        return {}
    return {r["assignment_item_id"]: {"index": r["q_index"], "total": r["q_total"]} for r in rows}
