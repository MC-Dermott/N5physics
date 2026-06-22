import streamlit as st


def _within_tolerance(user_val, target, tolerance=0.02):
    try:
        target = float(target)
        if abs(target) < 1e-9:
            return abs(user_val) < 0.01
        return abs(user_val - target) / abs(target) <= tolerance
    except (ValueError, TypeError):
        return False


def _normalize_unit(unit: str) -> str:
    return unit.strip().lower().replace("²", "^2").replace(" ", "")


def check_answer(user_input, question, unit_input=None, tolerance=0.02):
    """
    Returns ("correct", None), ("distractor", d), ("wrong_unit", None), or ("incorrect", None).
    If unit_input is provided and question.unit is non-empty, the unit is also checked.
    """
    try:
        user_val = float(str(user_input).replace(",", "").strip())
    except (ValueError, TypeError):
        return "incorrect", None

    if not _within_tolerance(user_val, question.correct_answer, tolerance):
        for d in question.distractors:
            if _within_tolerance(user_val, d["value"], tolerance):
                return "distractor", d
        return "incorrect", None

    # Number is correct — check unit if one is expected
    if unit_input is not None and question.unit:
        if _normalize_unit(unit_input) != _normalize_unit(question.unit):
            return "wrong_unit", None

    return "correct", None


def render_working(working):
    """Render a list of {type, content} working steps."""
    for step in working:
        if step["type"] == "latex":
            st.latex(step["content"])
        else:
            st.write(step["content"])


def render_feedback(result, distractor, question, show_working=True):
    """Render feedback after an answer is submitted."""
    correct_str = f"{question.correct_answer} {question.unit}".strip()
    is_classification = question.metadata.get("type") == "classification"

    if result == "correct":
        st.success("✅ Correct!")
    elif result == "wrong_unit":
        st.warning(
            f"⚠️ Your value is correct, but the unit is wrong. "
            f"The answer is **{correct_str}**."
        )
    elif result == "distractor":
        st.error("❌ Not quite.")
        if distractor and distractor.get("mistake"):
            st.warning(f"Common mistake: {distractor['mistake']}")
        if is_classification:
            st.info(f"The correct classification is: **{correct_str}**")
    else:
        st.error(f"❌ Incorrect. The correct answer is **{correct_str}**.")

    if show_working and result not in ("correct", "wrong_unit"):
        working = (distractor or {}).get("working") or question.working
        if working:
            with st.expander("📖 Worked Solution"):
                render_working(working)
    elif show_working:
        if question.working:
            with st.expander("📖 Worked Solution"):
                render_working(question.working)
