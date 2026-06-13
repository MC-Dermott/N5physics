import streamlit as st

from core.engine.session_manager import initialise_session, reset_test
from core.engine.question_factory import generate_question, get_topics, get_question_types
from core.ui.auth_ui import render_auth
from core.ui.practice_ui import render_practice
from core.ui.test_ui import render_test

st.set_page_config(page_title="Physics Practice", layout="centered")

initialise_session()


def _do_logout():
    for key in ["user", "qualification", "last_qualification",
                "last_topic", "last_question_type"]:
        st.session_state.pop(key, None)
    reset_test()
    st.session_state.quiz = {"current_question": None}


def _auth_button():
    user = st.session_state.get("user")
    if user:
        st.caption(f"**{user['username']}**")
        if st.button("Log out", key="logout_corner"):
            _do_logout()
            st.rerun()
    else:
        if st.button("Log in / Sign up", key="login_corner"):
            st.session_state.show_auth = True
            st.rerun()


# ── Auth page ────────────────────────────────────────────────────────────────

if st.session_state.get("show_auth"):
    if st.button("← Back"):
        st.session_state.pop("show_auth", None)
        st.rerun()
    render_auth()
    st.stop()

user = st.session_state.get("user")

# ── Homepage: level selection ─────────────────────────────────────────────────

if "qualification" not in st.session_state:
    st.title("Physics Practice")
    col_title, col_corner = st.columns([5, 1])
    with col_corner:
        _auth_button()

    st.write("Choose your level to get started.")
    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("National 4", use_container_width=True):
            st.session_state.qualification = "National 4"
            st.rerun()
    with col2:
        if st.button("National 5", use_container_width=True):
            st.session_state.qualification = "National 5"
            st.rerun()
    with col3:
        if st.button("Higher", use_container_width=True):
            st.session_state.qualification = "Higher"
            st.rerun()
    st.stop()

# ── Main page ─────────────────────────────────────────────────────────────────

qualification = st.session_state.qualification

st.title("Physics Practice")

col_info, col_corner = st.columns([5, 1])
with col_info:
    label = f"Level: **{qualification}**"
    if user:
        label += f" | **{user['username']}**"
    st.caption(label)
with col_corner:
    _auth_button()

if st.button("← Change Level"):
    st.session_state.pop("qualification", None)
    reset_test()
    st.session_state.quiz = {"current_question": None}
    st.rerun()

# Reset state when level changes
if st.session_state.get("last_qualification") != qualification:
    st.session_state.last_qualification = qualification
    reset_test()
    st.session_state.quiz = {"current_question": None}

st.divider()

# ── Mode, topic, question type ────────────────────────────────────────────────

mode = st.radio("Mode", ["Practice", "Test"], horizontal=True)

if st.session_state.get("mode") != mode:
    st.session_state.mode = mode
    reset_test()
    st.session_state.quiz = {"current_question": None}

topics = get_topics(qualification)
topic  = st.selectbox("Topic", topics)

if st.session_state.get("last_topic") != topic:
    st.session_state.last_topic = topic
    reset_test()
    st.session_state.quiz = {"current_question": None}

question_types = get_question_types(qualification, topic)
question_type  = st.selectbox("Question Type", question_types)

if st.session_state.get("last_question_type") != question_type:
    st.session_state.last_question_type = question_type
    reset_test()
    st.session_state.quiz = {"current_question": None}

st.divider()

# ── Route to practice or test ─────────────────────────────────────────────────

user_id     = user["id"] if user else None
generate_fn = lambda: generate_question(qualification, topic, question_type)

if mode == "Test":
    render_test(topic, question_type, qualification, generate_fn, user_id=user_id)
else:
    render_practice(topic, question_type, qualification, generate_fn, user_id=user_id)
