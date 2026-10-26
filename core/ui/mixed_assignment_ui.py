"""A mixed-practice assignment: one random exam-style question for each topic, answered as a single attempt
(Previous / Submit like a Test), scored and saved as one result under db.MIXED_KEY, with a breakdown by topic."""
import streamlit as st

from core.db import assignments as db
from core.engine.question_factory import generate_mixed_assignment
from core.engine.session_manager import reset_test
from core.ui.test_ui import render_active_question, render_review
from core.ui.unit_assessment_ui import _topic_breakdown


def render_mixed_assignment(assignment, user_id):
    from core.db.tracker import save_test_result, save_test_question_attempt

    test = st.session_state.test
    items = assignment["items"]

    if not test["questions"]:
        n = len(items)
        st.markdown(f"This assignment has **{n} question{'s' if n != 1 else ''}**, one on each topic below, in the "
                    "style of the exam. Every part is marked automatically and a full review is shown at the end.")
        st.markdown("\n".join(f"- {i['question_type']} · {i['topic']}" for i in items))
        if st.button("Start", type="primary", key="mixed_start"):
            reset_test()
            st.session_state.test["questions"] = generate_mixed_assignment(items)
            st.rerun()
        return

    if test["complete"]:
        if not test.get("saved") and user_id:
            if not save_test_result(user_id, db.MIXED_KEY["qualification"], db.MIXED_KEY["topic"],
                                    db.MIXED_KEY["question_type"], sum(test["results"]), len(test["results"]),
                                    assignment_id=assignment["id"], review_state=test):
                st.error("Your score could not be saved, so it won't count towards the assignment. "
                         "Please tell your teacher.")
            for result_type, distractor, q in test["feedback"]:
                mistake = distractor.get("mistake") if result_type == "distractor" and distractor else None
                save_test_question_attempt(user_id, items[0]["qualification"], q.topic, q.question_type,
                                           result_type == "correct", mistake)
            test["saved"] = True
        score, total = sum(test["results"]), len(test["results"])
        st.markdown(f"## Result: {score} / {total}")
        st.markdown("### By topic")
        st.markdown("| Topic | Score | % |\n|---|---|---|\n" + "\n".join(
            f"| {t} | {got} / {out_of} | {round(100 * got / out_of)}% |" for t, got, out_of in _topic_breakdown(test)))
        render_review(test)
        if st.button("Try again with new questions", type="primary", key="mixed_again"):
            reset_test()
            st.rerun()
        return

    render_active_question(test)
