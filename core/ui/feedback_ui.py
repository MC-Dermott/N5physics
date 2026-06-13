import streamlit as st


def _within_tolerance(user_val, target, tolerance=0.02):
    try:
        target = float(target)
        if abs(target) < 1e-9:
            return abs(user_val) < 0.01
        return abs(user_val - target) / abs(target) <= tolerance
    except (ValueError, TypeError):
        return False


def check_answer(user_input, question, tolerance=0.02):
    """
    Returns ("correct", None), ("distractor", d), or ("incorrect", None).
    d is the matching distractor dict.
    """
    try:
        user_val = float(str(user_input).replace(",", "").strip())
    except (ValueError, TypeError):
        return "incorrect", None

    if _within_tolerance(user_val, question.correct_answer, tolerance):
        return "correct", None

    for d in question.distractors:
        if _within_tolerance(user_val, d["value"], tolerance):
            return "distractor", d

    return "incorrect", None


def render_working(working):
    """Render a list of {type, content} working steps."""
    for step in working:
        if step["type"] == "latex":
            st.latex(step["content"])
        else:
            st.write(step["content"])


def render_feedback(result, distractor, question, show_working=True):
    """Render feedback after an answer is submitted."""
    if result == "correct":
        st.success("✅ Correct!")
    elif result == "distractor":
        st.error("❌ Not quite.")
        if distractor.get("mistake"):
            st.warning(f"Common mistake: {distractor['mistake']}")
    else:
        st.error(f"❌ Incorrect. The correct answer is **{question.correct_answer} {question.unit}**.")

    if show_working and result != "correct":
        working = (distractor or {}).get("working") or question.working
        if working:
            with st.expander("📖 Worked Solution"):
                render_working(working)
    elif show_working and result == "correct":
        if question.working:
            with st.expander("📖 Worked Solution"):
                render_working(question.working)
