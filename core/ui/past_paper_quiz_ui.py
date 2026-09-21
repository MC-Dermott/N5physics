import random
from pathlib import Path

import streamlit as st

from core.data.past_papers import get_unit_mcqs, canonical_unit
from core.db.tracker import save_test_result, save_test_question_attempt
from core.engine.session_manager import reset_past_paper_quiz

_ASSETS_DIR = Path(__file__).parent.parent / "data" / "past_paper_assets"
_OPTIONS = ["A", "B", "C", "D", "E"]
_NUM_QUESTIONS = 10


def _img_path(entry):
    return str(_ASSETS_DIR / entry["question_images"][0])


def _year_label(entry):
    return "Specimen Paper" if entry["year"] == "SPQ" else entry["year"]


def render_past_paper_quiz(unit, qualification, user_id=None):
    quiz = st.session_state.past_paper_quiz
    pool = get_unit_mcqs(qualification, unit)

    # --- Start screen ---
    if not quiz["questions"]:
        if not pool:
            st.info("No past paper multiple choice questions added yet for this unit.")
            return

        n = min(_NUM_QUESTIONS, len(pool))
        st.markdown(
            f"A **{n}-question multiple choice quiz**, drawn at random from real SQA "
            f"past-paper questions across the whole of this unit. Each question is "
            "marked automatically and your score is tracked."
        )
        if st.button("Start Quiz", type="primary"):
            reset_past_paper_quiz()
            st.session_state.past_paper_quiz["session_id"] = random.randint(100000, 999999)
            st.session_state.past_paper_quiz["questions"] = random.sample(pool, n)
            st.rerun()
        return

    # --- Summary screen ---
    if quiz["complete"]:
        if not quiz["saved"] and user_id:
            total = len(quiz["results"])
            save_test_result(user_id, qualification, canonical_unit(unit), "Past Paper Quiz",
                             sum(quiz["results"]), total)
            for correct, entry in zip(quiz["results"], quiz["questions"]):
                save_test_question_attempt(
                    user_id, qualification, entry["topic"], entry["question_type"], correct
                )
            quiz["saved"] = True
        _render_summary(quiz)
        if st.button("Start New Quiz", type="primary"):
            reset_past_paper_quiz()
            st.rerun()
        return

    # --- Active question ---
    idx = quiz["index"]
    total = len(quiz["questions"])
    entry = quiz["questions"][idx]

    st.progress((idx + 1) / total, text=f"Question {idx + 1} of {total}")
    st.caption(f"**{_year_label(entry)} — Question {entry['qnum']} — {entry['question_type']}**")
    st.image(_img_path(entry))

    radio_key = f"ppq_radio_{quiz['session_id']}_{idx}"
    selected = st.radio("Select your answer:", _OPTIONS, key=radio_key, index=None, horizontal=True)

    if st.button("Submit", key=f"ppq_submit_{quiz['session_id']}_{idx}", type="primary"):
        if selected is not None:
            quiz["answers"].append(selected)
            quiz["results"].append(selected == entry["answer_text"])
            quiz["index"] += 1
            if quiz["index"] >= total:
                quiz["complete"] = True
            st.rerun()
        else:
            st.warning("Please select an answer before submitting.")


def _render_summary(quiz):
    score = sum(quiz["results"])
    total = len(quiz["results"])

    st.markdown(f"## Result: {score} / {total}")
    if score == total:
        st.success("Perfect score! Excellent work!")
    elif score >= total * 0.6:
        st.info(f"Good effort — {score} out of {total} correct.")
    else:
        st.warning(f"{score} out of {total} correct. Keep practising!")

    st.markdown("---")
    st.markdown("### Question Review")

    for i, entry in enumerate(quiz["questions"]):
        answer = quiz["answers"][i]
        correct = quiz["results"][i]
        label = f"**{_year_label(entry)} Q{entry['qnum']} ({entry['question_type']}):**"
        if correct:
            st.success(f"{label} Your answer: **{answer}** ✅")
        else:
            with st.container(border=True):
                st.error(
                    f"{label}  \n"
                    f"Your answer: **{answer or '(blank)'}** ❌  \n"
                    f"Correct answer: **{entry['answer_text']}**"
                )
                st.image(_img_path(entry))

    st.markdown("---")
