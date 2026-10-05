"""Going back in a test: every test mode (Test, Unit Assessment, Practice Assessment, Past Paper
Quiz) gives each question a ← Previous button, so pupils can change any answer right up until
they submit the last question, which ends the test."""
import streamlit as st

GO_BACK_HINT = "You can go back and change an answer until you submit the last question."


def nav_buttons(key, can_go_back, submit_label="Submit"):
    """The ← Previous / Submit row under a test question. Returns (back, submit)."""
    col_back, col_submit = st.columns([1, 3])
    with col_back:
        back = can_go_back and st.button("← Previous", key=f"{key}_back")
    with col_submit:
        submit = st.button(submit_label, key=f"{key}_submit", type="primary")
    return back, submit


def refill(key, value):
    """Put a saved answer back into a widget before it is drawn, when a pupil returns to a
    question. Leaves a widget that is already on screen (and anything the pupil has typed) alone."""
    if value is not None and key not in st.session_state:
        st.session_state[key] = value


def ensure_slots(state, n):
    """Make state["answers"] / ["results"] / ["feedback"] one slot per question, filled in as
    each is answered (and overwritten if the pupil goes back and changes it)."""
    for k in ("answers", "results", "feedback"):
        if k in state:
            state[k] += [None] * (n - len(state[k]))
