"""Unit Assessment (N5 and Higher): exam-style questions from across the unit, chosen to cover as
many of its topics as possible, taken like a test, with a per-topic breakdown at the end."""
from collections import OrderedDict

import streamlit as st

from core.engine.question_factory import build_unit_assessment, has_unit_assessment
from core.engine.session_manager import reset_test
from core.ui.test_ui import render_active_question, render_review

UNIT_ASSESSMENT = "Unit Assessment"


def _topic_breakdown(test):
    """(topic, score, total) for each topic, in the order the questions were asked."""
    scores = OrderedDict()
    for correct, (_result, _distractor, part) in zip(test["results"], test["feedback"]):
        got, out_of = scores.get(part.question_type, (0, 0))
        scores[part.question_type] = (got + int(correct), out_of + 1)
    return [(topic, got, out_of) for topic, (got, out_of) in scores.items()]


def _render_summary(unit, test):
    score, total = sum(test["results"]), len(test["results"])
    pct = round(100 * score / total) if total else 0

    st.markdown(f"## {UNIT_ASSESSMENT}: {unit}")
    st.markdown(f"### Score: **{score} / {total}** ({pct}%)")
    if pct >= 70:
        st.success("Excellent — you're well prepared on this unit.")
    elif pct >= 50:
        st.info("A solid pass. Use the breakdown below to target your weaker topics.")
    else:
        st.warning("Keep practising — the breakdown below shows which topics to work on first.")

    st.markdown("### By topic")
    rows = _topic_breakdown(test)
    st.markdown("| Topic | Score | % |\n|---|---|---|\n" + "\n".join(
        f"| {t} | {got} / {out_of} | {round(100 * got / out_of)}% |" for t, got, out_of in rows))
    weakest = [t for t, got, out_of in rows if got / out_of < 0.5]
    if weakest:
        st.caption("Practise next: " + ", ".join(weakest))

    render_review(test)


def render_unit_assessment(unit, qualification, user_id=None):
    from core.db.tracker import save_test_result, save_test_question_attempt

    test = st.session_state.test
    # --- Start screen ---
    if not test["questions"]:
        if not has_unit_assessment(qualification, unit):
            st.info("No exam-style questions for this unit yet — check back soon!")
            return
        st.markdown(f"### {UNIT_ASSESSMENT}: {unit}")
        st.markdown(
            "Exam-style questions from across the whole unit, like a section of an SQA paper — "
            "chosen so that between them they cover the unit's topics. Every part is marked "
            "automatically, and you'll get a breakdown by topic at the end."
        )
        if st.button("Start Unit Assessment", type="primary"):
            reset_test()
            st.session_state.test["questions"] = build_unit_assessment(qualification, unit)
            st.rerun()
        return

    # --- Summary screen ---
    if test["complete"]:
        if not test.get("saved") and user_id:
            save_test_result(user_id, qualification, unit, UNIT_ASSESSMENT,
                             sum(test["results"]), len(test["results"]))
            for result_type, distractor, q in test["feedback"]:
                mistake = distractor.get("mistake") if result_type == "distractor" and distractor else None
                save_test_question_attempt(user_id, qualification, q.topic, q.question_type,
                                           result_type == "correct", mistake)
            test["saved"] = True
        _render_summary(unit, test)
        if st.button("Start New Unit Assessment", type="primary"):
            reset_test()
            st.rerun()
        return

    render_active_question(test)
