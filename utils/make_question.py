from core.models.question_model import PhysicsQuestion


def make_question(question, correct_val, options_data, unit,
                  scaffold=None, notes=None, topic="", question_type="", level="N5"):
    """
    Drop-in replacement for format_mcq() — returns a PhysicsQuestion instead of an MCQ dict.

    options_data: list of dicts with keys:
        value    – numeric answer
        mistake  – str or None (None for the correct option)
        working  – list of {type, content} steps
        summary  – ignored (kept for compatibility)
        display  – optional display string (stored in metadata)
    """
    correct_float = round(float(correct_val), 6)

    correct_working = []
    distractors = []

    for opt in options_data:
        val = round(float(opt["value"]), 6)
        if val == correct_float:
            correct_working = opt.get("working", [])
        else:
            distractors.append({
                "value": float(opt["value"]),
                "display": opt.get("display", f"{opt['value']} {unit}"),
                "mistake": opt.get("mistake") or "",
                "working": opt.get("working", []),
            })

    return PhysicsQuestion(
        question_text=question,
        correct_answer=float(correct_val),
        unit=unit,
        distractors=distractors,
        working=correct_working,
        scaffold=[
            {"prompt": s["question"], "answer": s["answer"]}
            for s in (scaffold or [])
            if s.get("answer") is not None
        ],
        notes=notes or "",
        topic=topic,
        question_type=question_type,
        level=level,
    )
