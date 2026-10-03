import re

import streamlit as st

from utils.answer_format import format_answer
from utils.diagrams import diagram_markdown as question_diagram_markdown
from utils.notes import format_math, split_equations
from utils.vector_diagram import diagram_markdown


def _within_tolerance(user_val, target, tolerance=0.02):
    try:
        target = float(target)
        if target == 0:
            return abs(user_val) < 0.01
        return abs(user_val - target) / abs(target) <= tolerance
    except (ValueError, TypeError):
        return False


def _normalize_unit(unit: str) -> str:
    unit = unit.strip().lower().replace("²", "^2").replace("³", "^3").replace(" ", "")
    return re.sub(r"ohms?", "ω", unit)


_SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
# e.g. 3.2x10^19, 3.2 × 10^-19, 3.2*10^(−19), 3.2 × 10⁻¹⁹
_SCI = re.compile(r"([+-]?(?:\d+\.?\d*|\.\d+))[x×*]10\^?\(?([+-]?\d+)\)?", re.IGNORECASE)


def parse_number(text):
    """A typed answer as a float; accepts scientific notation written as × 10^n."""
    text = str(text).replace(",", "").replace(" ", "").replace("−", "-").translate(_SUPERSCRIPTS)
    m = _SCI.fullmatch(text)
    if m:
        return float(m.group(1)) * 10 ** int(m.group(2))
    return float(text)


def check_answer(user_input, question, unit_input=None, tolerance=0.02):
    """
    Returns ("correct", None), ("distractor", d), ("wrong_unit", None), or ("incorrect", None).
    If unit_input is provided and question.unit is non-empty, the unit is also checked.
    """
    try:
        user_val = parse_number(user_input)
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


def render_diagram(question):
    """The question's diagram (a circuit, a light-gate set-up…), if it has one."""
    svg = question.metadata.get("diagram")
    if svg:
        st.markdown(question_diagram_markdown(svg))


def render_working(working):
    """Render a list of {type, content} working steps."""
    for step in working:
        if step["type"] == "latex":
            # One equation per line: split "A \Rightarrow B" / "A \qquad B" steps.
            for equation in split_equations(step["content"]):
                st.latex(equation)
        elif step["type"] == "diagram":
            st.markdown(diagram_markdown(step["content"]))
        else:
            st.markdown(format_math(step["content"]))


def render_feedback(result, distractor, question, show_working=True):
    """Render feedback after an answer is submitted."""
    correct_str = format_answer(question)
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
