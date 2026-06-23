import streamlit as st

from core.engine.assessment_generator import generate_assessment, TOTAL_MARKS, PASS_MARK
from core.engine.session_manager import reset_assessment
from core.ui.feedback_ui import check_answer, render_feedback, render_working

_UNIT_HINT = "Use `/` for per and `^2` for squared — e.g. `m/s`, `m/s^2`. Units are not case sensitive."


def _check_classification(selected, question):
    if selected == question.correct_answer:
        return "correct", None
    for d in question.distractors:
        if d["value"] == selected:
            return "distractor", d
    return "incorrect", None


def _render_question(assessment, idx, question):
    st.progress((idx + 1) / TOTAL_MARKS, text=f"Question {idx + 1} of {TOTAL_MARKS}")
    st.caption(f"*{question.question_type}*")
    st.markdown(question.question_text)
    st.write("")

    is_classification = question.metadata.get("type") == "classification"

    if is_classification:
        options = question.metadata.get(
            "options",
            [question.correct_answer] + [d["value"] for d in question.distractors],
        )
        selected = st.radio("Select your answer:", options,
                            key=f"assess_radio_{idx}", index=None)
        if st.button("Submit", key=f"assess_submit_{idx}", type="primary"):
            if selected is not None:
                result, distractor = _check_classification(selected, question)
                assessment["answers"].append(selected)
                assessment["results"].append(result == "correct")
                assessment["feedback"].append((result, distractor, question))
                assessment["index"] += 1
                if assessment["index"] >= TOTAL_MARKS:
                    assessment["complete"] = True
                st.rerun()
            else:
                st.warning("Please select an answer before submitting.")
    else:
        if question.unit:
            col1, col2 = st.columns([3, 2])
            with col1:
                answer = st.text_input("Your answer:", key=f"assess_ans_{idx}")
            with col2:
                unit_input = st.text_input("Units:", key=f"assess_unit_{idx}",
                                           placeholder="e.g. m/s")
            st.caption(_UNIT_HINT)
        else:
            answer = st.text_input("Your answer:", key=f"assess_ans_{idx}")
            unit_input = None

        if st.button("Submit", key=f"assess_submit_{idx}", type="primary"):
            if answer.strip():
                result, distractor = check_answer(answer, question, unit_input=unit_input)
                display_answer = f"{answer} {unit_input}".strip() if unit_input else answer
                assessment["answers"].append(display_answer)
                assessment["results"].append(result == "correct")
                assessment["feedback"].append((result, distractor, question))
                assessment["index"] += 1
                if assessment["index"] >= TOTAL_MARKS:
                    assessment["complete"] = True
                st.rerun()
            else:
                st.warning("Please enter an answer before submitting.")


def _render_summary(unit, assessment):
    score = sum(assessment["results"])
    total = len(assessment["results"])
    passed = score >= PASS_MARK

    st.markdown(f"## Practice Assessment: {unit}")
    st.markdown(f"### Score: **{score} / {total}** &nbsp;&nbsp; Pass mark: {PASS_MARK}/{TOTAL_MARKS}")

    if passed:
        st.success(f"**Pass** — {score} out of {total}. Well done!")
    else:
        st.error(f"**Not yet passed** — {score} out of {total}. Keep practising!")

    st.markdown("---")
    st.markdown("### Question Review")

    for q_num, (result_type, distractor, q_ref) in enumerate(assessment["feedback"], start=1):
        answer = assessment["answers"][q_num - 1]
        correct = assessment["results"][q_num - 1]
        correct_str = f"{q_ref.correct_answer} {q_ref.unit}".strip()

        if correct:
            st.success(
                f"**Q{q_num} ({q_ref.question_type}):** {q_ref.question_text}  \n"
                f"Your answer: **{answer}** ✅"
            )
        elif result_type == "wrong_unit":
            with st.container(border=True):
                st.warning(
                    f"**Q{q_num} ({q_ref.question_type}):** {q_ref.question_text}  \n"
                    f"Your answer: **{answer}** ⚠️  \n"
                    f"Correct answer: **{correct_str}** — value correct, unit wrong!"
                )
                if q_ref.working:
                    with st.expander("📖 Worked Solution"):
                        render_working(q_ref.working)
        else:
            with st.container(border=True):
                st.error(
                    f"**Q{q_num} ({q_ref.question_type}):** {q_ref.question_text}  \n"
                    f"Your answer: **{answer or '(blank)'}** ❌  \n"
                    f"Correct answer: **{correct_str}**"
                )
                if result_type == "distractor" and distractor and distractor.get("mistake"):
                    st.warning(f"Common mistake: {distractor['mistake']}")
                working = (distractor or {}).get("working") or q_ref.working
                if working:
                    with st.expander("📖 Worked Solution"):
                        render_working(working)

    st.markdown("---")


def render_assessment(unit, qualification, user_id=None):
    assessment = st.session_state.assessment

    if not assessment["questions"]:
        st.markdown(f"### Practice Assessment: {unit}")
        st.markdown(
            f"This assessment covers all topics in the **{unit}** unit.  \n"
            f"**{TOTAL_MARKS} marks** &nbsp;|&nbsp; **Pass mark: {PASS_MARK}/{TOTAL_MARKS}**  \n"
            f"Questions are drawn from across the unit and marked automatically."
        )
        st.write("")
        if st.button("Start Assessment", type="primary"):
            reset_assessment()
            st.session_state.assessment["questions"] = generate_assessment(unit)
            st.rerun()
        return

    if assessment["complete"]:
        _render_summary(unit, assessment)
        if st.button("Start New Assessment", type="primary"):
            reset_assessment()
            st.rerun()
        return

    _render_question(assessment, assessment["index"], assessment["questions"][assessment["index"]])
