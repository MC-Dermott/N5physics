"""Saved attempts, so a pupil can look back over a completed assignment test.

An attempt (the question feedback list, the pupil's answers and which were marked right) is stored as JSON
in `test_result_reviews`, one row per test_results row. Questions are plain dataclasses, so they are
converted to JSON and back; bytes are base64-encoded and tuples are kept."""
import base64
from dataclasses import asdict

from core.db.client import get_supabase
from core.models.question_model import PhysicsQuestion

_BYTES, _TUPLE = "__bytes__", "__tuple__"


def _encode(value):
    if isinstance(value, bytes):
        return {_BYTES: base64.b64encode(value).decode("ascii")}
    if isinstance(value, tuple):
        return {_TUPLE: [_encode(v) for v in value]}
    if isinstance(value, dict):
        return {str(k): _encode(v) for k, v in value.items()}
    if isinstance(value, (list, set)):
        return [_encode(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)                       # anything exotic is shown as text rather than lost


def _decode(value):
    if isinstance(value, dict):
        if set(value) == {_BYTES}:
            return base64.b64decode(value[_BYTES])
        if set(value) == {_TUPLE}:
            return tuple(_decode(v) for v in value[_TUPLE])
        return {k: _decode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_decode(v) for v in value]
    return value


def question_to_json(question):
    return _encode(asdict(question))


def question_from_json(data):
    data = _decode(data)
    data["parts"] = [question_from_json(_encode(p)) if isinstance(p, dict) else p for p in data.get("parts", [])]
    return PhysicsQuestion(**data)


def attempt_to_json(test):
    """test: the finished test's session dict (answers, results, feedback)."""
    return {"answers": _encode(list(test["answers"])), "results": [bool(r) for r in test["results"]],
            "feedback": [[kind, _encode(distractor), question_to_json(q)] for kind, distractor, q in test["feedback"]]}


def attempt_from_json(payload):
    return {"answers": _decode(payload["answers"]), "results": payload["results"],
            "feedback": [(kind, _decode(distractor), question_from_json(q)) for kind, distractor, q in payload["feedback"]]}


def save_review(result_id, test):
    """Best-effort: a pupil's score is already saved, so a failure here must not break the test."""
    try:
        get_supabase().table("test_result_reviews").insert(
            {"test_result_id": result_id, "payload": attempt_to_json(test)}).execute()
        return True
    except Exception:
        return False


def load_review(result_id):
    rows = (get_supabase().table("test_result_reviews").select("payload")
            .eq("test_result_id", result_id).execute().data or [])
    return attempt_from_json(rows[0]["payload"]) if rows else None
