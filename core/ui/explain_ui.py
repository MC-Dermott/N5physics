"""Explain questions: the pupil types an answer, then ticks the SQA marking points it includes."""
import streamlit as st


def render_explain(questions, key):
    from core.data.explain_questions import explain_score

    n = st.selectbox("Question", range(len(questions)),
                     format_func=lambda i: f"{i + 1}. {questions[i]['source']}", key=f"explain_pick_{key}")
    q, k = questions[n], f"explain_{key}_{n}"
    marks = len(q["points"])

    st.info(q["context"])
    st.markdown(f"**{q['question']}** ({marks} mark{'s' if marks != 1 else ''})")
    answer = st.text_area("Your answer:", key=f"{k}_answer")

    if st.button("Show marking points", type="primary", key=f"{k}_show"):
        if answer.strip():
            st.session_state[f"{k}_shown"] = True
        else:
            st.warning("Write your answer first.")
    if not st.session_state.get(f"{k}_shown"):
        return

    st.markdown("**Tick each point your answer includes** (one mark each):")
    if q["gate"]:
        st.caption("The first point must be correct, or no marks are awarded.")
    ticked = [st.checkbox(point, key=f"{k}_point{i}") for i, point in enumerate(q["points"])]
    if q["avoid"]:
        st.warning(f"Marking instructions: {q['avoid']}")
    st.markdown(f"### Your mark: {explain_score(q, ticked)} / {marks}")
