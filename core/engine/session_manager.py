import streamlit as st


def _empty_test():
    return {
        "questions": [],
        "index": 0,
        "answers": [],
        "results": [],
        "feedback": [],
        "complete": False,
        "saved": False,
    }


def _empty_assessment():
    return {
        "questions": [],
        "index": 0,
        "answers": [],
        "results": [],
        "feedback": [],
        "complete": False,
    }


def reset_test():
    st.session_state.test = _empty_test()


def reset_assessment():
    st.session_state.assessment = _empty_assessment()


def initialise_session():
    if "quiz" not in st.session_state:
        st.session_state.quiz = {"current_question": None}
    if "mode" not in st.session_state:
        st.session_state.mode = "Practice"
    if "test" not in st.session_state:
        st.session_state.test = _empty_test()
    if "assessment" not in st.session_state:
        st.session_state.assessment = _empty_assessment()
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "scenario_part" not in st.session_state:
        st.session_state.scenario_part = 0
    if "scenario_submitted" not in st.session_state:
        st.session_state.scenario_submitted = {}
