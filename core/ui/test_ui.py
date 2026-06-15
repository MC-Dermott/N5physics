import streamlit as st

from core.engine.session_manager import reset_test
from core.ui.feedback_ui import check_answer, render_feedback, render_working

_NUM_QUESTIONS = 5


def render_test(topic, question_type, qualification, generate_fn, user_id=None):
    from core.db.tracker import save_test_result, save_test_question_attempt

    test = st.session_state.test

    # --- Start screen ---
    if not test["questions"]:
        if user_id:
            from core.ui.reports_ui import render_student_insight
            render_student_insight(user_id, qualification, topic, question_type)

        st.markdown(
            f"You will be given **{_NUM_QUESTIONS} questions** on *{question_type}*. "
            "Each question is marked automatically. A summary with feedback is shown at the end."
        )
        if st.button("Start Test", type="primary"):
            reset_test()
            st.session_state.test["questions"] = [generate_fn() for _ in range(_NUM_QUESTIONS)]
            st.rerun()
        return

    # --- Summary screen ---
    if test["complete"]:
        if not test.get("saved") and user_id:
            total = len(test["results"])
            save_test_result(user_id, qualification, topic, question_type,
                             sum(test["results"]), total)
            # Save per-question results with mistake text
            for result_type, distractor, q in test["feedback"]:
                correct = result_type == "correct"
                mistake = None
                if result_type == "distractor" and distractor:
                    mistake = distractor.get("mistake")
                save_test_question_attempt(
                    user_id, qualification, q.topic, q.question_type, correct, mistake
                )
            test["saved"] = True
        _render_summary(test)
        if st.button("Start New Test", type="primary"):
            reset_test()
            st.rerun()
        return

    # --- Active question ---
    idx = test["index"]
    question = test["questions"][idx]

    st.progress((idx + 1) / _NUM_QUESTIONS, text=f"Question {idx + 1} of {_NUM_QUESTIONS}")

    if question.is_scenario:
        _render_scenario_test(test, idx, question)
    else:
        _render_single_test(test, idx, question)


def _render_single_test(test, idx, question):
    st.markdown(question.question_text)
    st.write("")

    col1, col2 = st.columns([4, 1])
    with col1:
        answer = st.text_input("Your answer:", key=f"test_ans_{idx}")
    with col2:
        st.markdown(f"<br><b>{question.unit}</b>", unsafe_allow_html=True)

    if st.button("Submit", key=f"test_submit_{idx}", type="primary"):
        result, distractor = check_answer(answer, question)
        test["answers"].append(answer)
        test["results"].append(result == "correct")
        test["feedback"].append((result, distractor, question))
        test["index"] += 1
        if test["index"] >= _NUM_QUESTIONS:
            test["complete"] = True
        st.rerun()


def _render_scenario_test(test, idx, question):
    """Treat each scored scenario part as a separate test question. Explain parts are skipped."""
    scored_parts = [p for p in question.parts if p.metadata.get("type") != "explain"]

    part_idx_key = f"scenario_part_idx_{idx}"
    part_answers_key = f"scenario_part_answers_{idx}"

    if part_idx_key not in st.session_state:
        st.session_state[part_idx_key] = 0
        st.session_state[part_answers_key] = []

    part_idx = st.session_state[part_idx_key]

    if question.scenario_context:
        st.info(question.scenario_context)

    part = scored_parts[part_idx]
    st.markdown(f"**Part {part_idx + 1} of {len(scored_parts)}:** {part.question_text}")
    st.write("")

    col1, col2 = st.columns([4, 1])
    with col1:
        answer = st.text_input("Your answer:", key=f"test_ans_{idx}_p{part_idx}")
    with col2:
        st.markdown(f"<br><b>{part.unit}</b>", unsafe_allow_html=True)

    if st.button("Submit", key=f"test_submit_{idx}_p{part_idx}", type="primary"):
        result, distractor = check_answer(answer, part)
        st.session_state[part_answers_key].append((answer, result, distractor, part))

        if part_idx + 1 < len(scored_parts):
            st.session_state[part_idx_key] += 1
            st.rerun()
        else:
            for ans, res, dist, p in st.session_state[part_answers_key]:
                test["answers"].append(ans)
                test["results"].append(res == "correct")
                test["feedback"].append((res, dist, p))
            test["index"] += 1
            if test["index"] >= _NUM_QUESTIONS:
                test["complete"] = True
            del st.session_state[part_idx_key]
            del st.session_state[part_answers_key]
            st.rerun()


def _render_summary(test):
    score = sum(test["results"])
    total = len(test["results"])

    st.markdown(f"## Result: {score} / {total}")
    if score == total:
        st.success("Perfect score! Excellent work!")
    elif score >= total * 0.6:
        st.info(f"Good effort — {score} out of {total} correct.")
    else:
        st.warning(f"{score} out of {total} correct. Keep practising!")

    st.markdown("---")
    st.markdown("### Question Review")

    for q_num, (result_type, distractor, q_ref) in enumerate(test["feedback"], start=1):
        answer = test["answers"][q_num - 1]
        correct = test["results"][q_num - 1]

        if correct:
            st.success(f"**Q{q_num}:** {q_ref.question_text}  \nYour answer: **{answer}** ✅")
        else:
            with st.container(border=True):
                st.error(
                    f"**Q{q_num}:** {q_ref.question_text}  \n"
                    f"Your answer: **{answer or '(blank)'}** ❌  \n"
                    f"Correct answer: **{q_ref.correct_answer} {q_ref.unit}**"
                )
                if result_type == "distractor" and distractor and distractor.get("mistake"):
                    st.warning(f"Common mistake: {distractor['mistake']}")
                working = (distractor or {}).get("working") or q_ref.working
                if working:
                    with st.expander("📖 Worked Solution"):
                        render_working(working)

    st.markdown("---")
