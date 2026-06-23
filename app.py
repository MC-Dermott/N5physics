import streamlit as st

from core.engine.session_manager import initialise_session, reset_test, reset_assessment
from core.engine.question_factory import generate_question, get_topics, get_question_types, get_sub_types
from core.ui.auth_ui import render_auth, render_change_password
from core.ui.practice_ui import render_practice
from core.ui.test_ui import render_test
from core.ui.assessment_ui import render_assessment
from core.ui.reports_ui import render_teacher_report
from core.ui.student_dashboard_ui import render_student_dashboard
from core.data.backgrounds import get_background_videos

st.set_page_config(page_title="Physics Practice", layout="centered")

initialise_session()


def _do_logout():
    for key in ["user", "qualification", "last_qualification",
                "last_topic", "last_question_type", "show_change_password",
                "show_dashboard", "show_student_dashboard"]:
        st.session_state.pop(key, None)
    reset_test()
    reset_assessment()
    st.session_state.quiz = {"current_question": None}


def _auth_button():
    user = st.session_state.get("user")
    if user:
        st.caption(f"**{user['username']}**")
        if st.button("Log out", key="logout_corner"):
            _do_logout()
            st.rerun()
        if st.button("Change password", key="change_pw_corner"):
            st.session_state.show_change_password = True
            st.rerun()


user = st.session_state.get("user")

# ── Login gate ────────────────────────────────────────────────────────────────

if not user:
    render_auth()
    st.stop()

# ── Change password page ──────────────────────────────────────────────────────

if st.session_state.get("show_change_password"):
    if st.button("← Back"):
        st.session_state.pop("show_change_password", None)
        st.rerun()
    render_change_password(user)
    st.stop()

# ── Teacher dashboard page ────────────────────────────────────────────────────

if st.session_state.get("show_dashboard"):
    st.title("Physics Practice")
    col_back, col_corner = st.columns([5, 1])
    with col_back:
        if st.button("← Back"):
            st.session_state.pop("show_dashboard", None)
            st.rerun()
    with col_corner:
        _auth_button()
    render_teacher_report(st.session_state.get("qualification", "National 5"))
    st.stop()

# ── Student progress page ─────────────────────────────────────────────────────

if st.session_state.get("show_student_dashboard"):
    st.title("Physics Practice")
    col_back, col_corner = st.columns([5, 1])
    with col_back:
        if st.button("← Back"):
            st.session_state.pop("show_student_dashboard", None)
            st.rerun()
    with col_corner:
        _auth_button()
    render_student_dashboard(user)
    st.stop()

# ── Homepage: level selection ─────────────────────────────────────────────────

if "qualification" not in st.session_state:
    st.title("Physics Practice")
    col_title, col_corner = st.columns([5, 1])
    with col_corner:
        _auth_button()

    if user and user.get("role") == "teacher":
        if st.button("📊 Teacher Dashboard", use_container_width=True):
            st.session_state.show_dashboard = True
            st.rerun()
        st.write("")

    if user:
        if st.button("📈 My Progress", use_container_width=True):
            st.session_state.show_student_dashboard = True
            st.rerun()
        st.write("")

    st.write("Choose your level to get started.")
    st.write("")

    col1, col2, col3, col4 = st.columns(4)
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
    with col4:
        if st.button("Crash Higher", use_container_width=True):
            st.session_state.qualification = "Crash Higher"
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
    reset_assessment()
    st.session_state.quiz = {"current_question": None}
    st.rerun()

# Reset state when level changes
if st.session_state.get("last_qualification") != qualification:
    st.session_state.last_qualification = qualification
    reset_test()
    reset_assessment()
    st.session_state.quiz = {"current_question": None}

st.divider()

# ── Mode, topic, question type ────────────────────────────────────────────────

if qualification == "National 4":
    mode_options = ["Practice", "Test", "Practice Assessment"]
else:
    mode_options = ["Practice", "Test"]

mode = st.radio("Mode", mode_options, horizontal=True)

if st.session_state.get("mode") != mode:
    st.session_state.mode = mode
    reset_test()
    reset_assessment()
    st.session_state.quiz = {"current_question": None}

topic_label = "Unit" if qualification == "National 4" else "Topic"
topics = get_topics(qualification)
topic  = st.selectbox(topic_label, topics)

if st.session_state.get("last_topic") != topic:
    st.session_state.last_topic = topic
    reset_test()
    reset_assessment()
    st.session_state.quiz = {"current_question": None}

user_id = user["id"] if user else None

# ── Practice Assessment (N4 only) ─────────────────────────────────────────────

if mode == "Practice Assessment":
    st.divider()
    render_assessment(topic, qualification, user_id=user_id)
    st.stop()

# ── Question type selection ───────────────────────────────────────────────────

question_types = get_question_types(qualification, topic)

if not question_types:
    st.info("No questions available for this topic yet — check back soon!")
    st.stop()

question_type  = st.selectbox("Question Type", question_types)

if st.session_state.get("last_question_type") != question_type:
    st.session_state.last_question_type = question_type
    st.session_state.pop("last_sub_type", None)
    reset_test()
    st.session_state.quiz = {"current_question": None}

sub_types = get_sub_types(qualification, topic, question_type)
if sub_types:
    sub_type = st.selectbox("Question Style", sub_types)
    if st.session_state.get("last_sub_type") != sub_type:
        st.session_state.last_sub_type = sub_type
        reset_test()
        st.session_state.quiz = {"current_question": None}
else:
    sub_type = None
    st.session_state.pop("last_sub_type", None)

# ── Background videos (N5 only) ───────────────────────────────────────────────

if qualification in ("National 5", "Crash Higher"):
    videos = get_background_videos(topic, question_type, qualification=qualification)
    with st.expander("📺 Background"):
        if videos:
            for v in videos:
                st.markdown(f"- [{v['title']}]({v['url']})")
        else:
            st.caption("No background videos added yet for this topic.")

st.divider()

# ── Route to practice or test ─────────────────────────────────────────────────

generate_fn = lambda: generate_question(qualification, topic, question_type, sub_type=sub_type)

if mode == "Test":
    render_test(topic, question_type, qualification, generate_fn, user_id=user_id)
else:
    render_practice(topic, question_type, qualification, generate_fn, user_id=user_id)
