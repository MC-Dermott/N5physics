import streamlit as st

from core.ui.feedback_ui import check_answer, render_feedback, render_working
from core.ui.scaffold_ui import render_scaffold
from core.db.tracker import save_practice_attempt


def _render_notes(question):
    if question.notes:
        with st.expander("📚 Notes"):
            st.markdown(question.notes)


_UNIT_HINT = "Use `/` for per and `^2` for squared — e.g. `m/s`, `m/s^2`. Units are not case sensitive."


def _render_answer_input(question, suffix=""):
    if question.unit:
        col1, col2 = st.columns([3, 2])
        with col1:
            answer = st.text_input("Your answer:", key=f"ans_{question.qid}_{suffix}")
        with col2:
            unit_input = st.text_input("Units:", key=f"unit_{question.qid}_{suffix}",
                                       placeholder="e.g. m/s")
        st.caption(_UNIT_HINT)
    else:
        answer = st.text_input("Your answer:", key=f"ans_{question.qid}_{suffix}")
        unit_input = None
    return answer, unit_input


# =========================================================
# Single question (non-scenario)
# =========================================================

def _check_classification(selected, question):
    if selected == question.correct_answer:
        return "correct", None
    for d in question.distractors:
        if d["value"] == selected:
            return "distractor", d
    return "incorrect", None


def _render_single(question, user_id, qualification):
    submitted_key = f"sub_{question.qid}"

    st.markdown(question.question_text)
    st.write("")

    is_classification = question.metadata.get("type") == "classification"

    if not st.session_state.get(submitted_key):
        _render_notes(question)
        render_scaffold(question)

        if is_classification:
            options = question.metadata.get(
                "options",
                [question.correct_answer] + [d["value"] for d in question.distractors],
            )
            selected = st.radio("Select your answer:", options,
                                key=f"radio_{question.qid}", index=None)
            if st.button("Submit Answer", key=f"submit_{question.qid}", type="primary"):
                if selected is not None:
                    st.session_state[submitted_key] = selected
                    result, distractor = _check_classification(selected, question)
                    st.session_state[f"result_{question.qid}"] = (result, distractor)
                    if user_id:
                        save_practice_attempt(user_id, qualification, question.topic,
                                              question.question_type, result == "correct")
                    st.rerun()
                else:
                    st.warning("Please select an answer before submitting.")
        else:
            answer, unit_input = _render_answer_input(question)
            if st.button("Submit Answer", key=f"submit_{question.qid}", type="primary"):
                if answer.strip():
                    st.session_state[submitted_key] = answer
                    result, distractor = check_answer(answer, question, unit_input=unit_input)
                    st.session_state[f"result_{question.qid}"] = (result, distractor)
                    if user_id:
                        save_practice_attempt(user_id, qualification, question.topic,
                                              question.question_type, result == "correct")
                    st.rerun()
                else:
                    st.warning("Please enter an answer before submitting.")
    else:
        result, distractor = st.session_state.get(f"result_{question.qid}", ("incorrect", None))
        render_feedback(result, distractor, question, show_working=True)


# =========================================================
# Scenario (multi-part)
# =========================================================

def _render_explain_part(question, part_idx, submitted_key):
    if st.button("Show Expected Answer", key=f"reveal_{question.qid}_part{part_idx}", type="primary"):
        st.session_state[submitted_key] = "revealed"
        st.rerun()


def _render_scenario(question, user_id, qualification):
    if question.scenario_context:
        st.info(question.scenario_context)

    for i, part in enumerate(question.parts):
        part_submitted_key = f"sub_{question.qid}_part{i}"
        is_explain = part.metadata.get("type") == "explain"
        st.markdown(f"**Part {i + 1}:** {part.question_text}")

        if not st.session_state.get(part_submitted_key):
            if i == 0 or st.session_state.get(f"sub_{question.qid}_part{i - 1}"):
                if is_explain:
                    _render_explain_part(question, i, part_submitted_key)
                else:
                    _render_notes(part)
                    render_scaffold(part, suffix=f"part{i}")
                    answer, unit_input = _render_answer_input(part, suffix=f"part{i}")
                    if st.button(f"Submit Part {i + 1}", key=f"submit_{question.qid}_part{i}", type="primary"):
                        if answer.strip():
                            st.session_state[part_submitted_key] = answer
                            result, distractor = check_answer(answer, part, unit_input=unit_input)
                            st.session_state[f"result_{question.qid}_part{i}"] = (result, distractor)
                            if user_id:
                                save_practice_attempt(user_id, qualification, part.topic,
                                                      part.question_type, result == "correct")
                            st.rerun()
                        else:
                            st.warning("Please enter an answer before submitting.")
        else:
            if is_explain:
                st.info(part.metadata.get("explain_text", ""))
            else:
                result, distractor = st.session_state.get(
                    f"result_{question.qid}_part{i}", ("incorrect", None))
                render_feedback(result, distractor, part, show_working=True)

        if i < len(question.parts) - 1:
            st.divider()


# =========================================================
# Public entry point
# =========================================================

def render_practice(topic, question_type, qualification, generate_fn, user_id=None):
    quiz = st.session_state.quiz

    if st.button("Generate Question", type="primary"):
        q = generate_fn()
        quiz["current_question"] = q
        # clear any previous submission state for this slot
        for key in list(st.session_state.keys()):
            if key.startswith("sub_") or key.startswith("result_") or key.startswith("ans_") or key.startswith("scaf_"):
                del st.session_state[key]
        st.rerun()

    question = quiz.get("current_question")
    if not question:
        st.caption("Press **Generate Question** to begin.")
        return

    if question.is_scenario:
        _render_scenario(question, user_id, qualification)
    else:
        _render_single(question, user_id, qualification)
