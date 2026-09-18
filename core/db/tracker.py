from core.db.client import get_supabase


def save_practice_attempt(user_id: str, qualification: str, topic: str, question_type: str, correct: bool):
    try:
        get_supabase().table("question_attempts").insert({
            "user_id": user_id,
            "qualification": qualification,
            "topic": topic,
            "question_type": question_type,
            "correct": correct,
        }).execute()
    except Exception:
        pass  # Don't break the app if tracking fails


def save_test_result(user_id: str, qualification: str, topic: str, score: int, total: int):
    """A test now covers a whole topic (mixing question types), so results are
    recorded at topic level. Per-question-type breakdown still comes from
    save_test_question_attempt below."""
    try:
        get_supabase().table("test_results").insert({
            "user_id": user_id,
            "qualification": qualification,
            "topic": topic,
            "score": score,
            "total": total,
        }).execute()
    except Exception:
        pass


def save_test_question_attempt(user_id: str, qualification: str, topic: str,
                                question_type: str, correct: bool, mistake: str | None = None):
    try:
        get_supabase().table("test_question_attempts").insert({
            "user_id": user_id,
            "qualification": qualification,
            "topic": topic,
            "question_type": question_type,
            "correct": correct,
            "mistake": mistake,
        }).execute()
    except Exception:
        pass
