import streamlit as st

from core.engine.session_manager import reset_test
from core.ui.feedback_ui import check_answer, render_feedback, render_working

_NUM_QUESTIONS = 5


def render_test(topic, question_type, qualification, generate_fn, user_id=None):
    from core.db.tracker import save_test_result

    test = st.session_state.test

    # --- Start screen ---
    if not test["questions"]:
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
        test["feedback"].append((result, distractor))
        test["index"] += 1
        if test["index"] >= _NUM_QUESTIONS:
            test["complete"] = True
        st.rerun()


def _render_scenario_test(test, idx, question):
    """Treat each scenario part as a separate test question."""
    part_idx_key = f"scenario_part_idx_{idx}"
    part_answers_key = f"scenario_part_answers_{idx}"

    if part_idx_key not in st.session_state:
        st.session_state[part_idx_key] = 0
        st.session_state[part_answers_key] = []

    part_idx = st.session_state[part_idx_key]
    parts = question.parts

    if question.scenario_context:
        st.info(question.scenario_context)

    part = parts[part_idx]
    st.markdown(f"**Part {part_idx + 1} of {len(parts)}:** {part.question_text}")
    st.write("")

    col1, col2 = st.columns([4, 1])
    with col1:
        answer = st.text_input("Your answer:", key=f"test_ans_{idx}_p{part_idx}")
    with col2:
        st.markdown(f"<br><b>{part.unit}</b>", unsafe_allow_html=True)

    if st.button("Submit", key=f"test_submit_{idx}_p{part_idx}", type="primary"):
        result, distractor = check_answer(answer, part)
        st.session_state[part_answers_key].append((answer, result, distractor, part))

        if part_idx + 1 < len(parts):
            st.session_state[part_idx_key] += 1
            st.rerun()
        else:
            # All parts done — record as one entry per part
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

    q_num = 1
    result_idx = 0
    for question in test["questions"]:
        parts = question.parts if question.is_scenario else [question]
        for part in parts:
            if result_idx >= len(test["results"]):
                break
            correct = test["results"][result_idx]
            answer  = test["answers"][result_idx]
            fb      = test["feedback"][result_idx]
            # fb may be (result, distractor) for single or (result, distractor, part_q) for scenario parts
            result  = fb[0]
            distractor = fb[1]
            q_ref   = fb[2] if len(fb) > 2 else part

            if correct:
                st.success(f"**Q{q_num}:** {q_ref.question_text}  \nYour answer: **{answer}** ✅")
            else:
                with st.container(border=True):
                    st.error(
                        f"**Q{q_num}:** {q_ref.question_text}  \n"
                        f"Your answer: **{answer or '(blank)'}** ❌  \n"
                        f"Correct answer: **{q_ref.correct_answer} {q_ref.unit}**"
                    )
                    if result == "distractor" and distractor and distractor.get("mistake"):
                        st.warning(f"Common mistake: {distractor['mistake']}")
                    working = (distractor or {}).get("working") or q_ref.working
                    if working:
                        with st.expander("📖 Worked Solution"):
                            render_working(working)

            q_num += 1
            result_idx += 1

    st.markdown("---")
