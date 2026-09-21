import streamlit as st
import pandas as pd
from core.db.client import get_supabase
from core.engine.question_factory import QUAL_REGISTRY

_GREY = "⚪"
_RED = "🔴"
_YELLOW = "🟡"
_GREEN = "🟢"


def _fetch_tests(user_id):
    return (
        get_supabase()
        .table("test_results")
        .select("*")
        .eq("user_id", user_id)
        .execute()
        .data or []
    )


def _colour_for(pct):
    if pct is None:
        return _GREY
    if pct < 50:
        return _RED
    if pct <= 70:
        return _YELLOW
    return _GREEN


def render_progress_heatmaps(user_id):
    """Render the Unit/Topic progress list for a given user (no page header)."""
    try:
        tests = _fetch_tests(user_id)
    except Exception as e:
        st.error(f"Could not load data: {e}")
        return

    df = pd.DataFrame(tests)
    if not df.empty:
        df["pct"] = df["score"] / df["total"] * 100
        summary = (
            df.groupby(["qualification", "topic", "question_type"])["pct"]
            .agg(pct="mean", attempts="count")
        )
        tested_quals = set(df["qualification"].unique())
    else:
        summary = pd.DataFrame(columns=["pct", "attempts"])
        tested_quals = set()

    qualifications = [q for q in QUAL_REGISTRY if q in tested_quals]
    if not qualifications:
        st.info("No tests taken yet. Complete a test to see your progress here.")
        return

    level = st.selectbox("Level", qualifications, key="progress_level")

    units = list(QUAL_REGISTRY[level].keys())
    unit = st.selectbox("Unit", units, key=f"progress_unit_{level}")

    question_types = QUAL_REGISTRY[level][unit].keys()
    if not question_types:
        st.caption("No topics in this unit yet.")
    for qt in question_types:
        try:
            row = summary.loc[(level, unit, qt)]
            pct, attempts = row["pct"], int(row["attempts"])
        except KeyError:
            pct, attempts = None, 0

        colour = _colour_for(pct)
        if pct is None:
            detail = "No tests yet"
        else:
            detail = f"{pct:.0f}% ({attempts} test{'s' if attempts != 1 else ''})"
        st.markdown(f"{colour} &nbsp; **{qt}** — {detail}")

    st.caption("🟢 > 70%   🟡 50 – 70%   🔴 < 50%   ⚪ No tests taken")


def render_past_paper_quiz_history(user_id):
    """Recent unit-level Past Paper Quiz attempts. Shown separately from the
    heatmap above since a quiz spans a whole unit rather than one curriculum
    topic, so it can't slot into that per-topic grid."""
    try:
        tests = _fetch_tests(user_id)
    except Exception:
        return

    quizzes = [t for t in tests if t["question_type"] == "Past Paper Quiz"]
    if not quizzes:
        return

    quizzes.sort(key=lambda t: t["taken_at"], reverse=True)
    st.subheader("Past Paper Quizzes")
    df = pd.DataFrame(quizzes)
    df["Score"] = df["score"].astype(str) + " / " + df["total"].astype(str)
    df["Date"] = pd.to_datetime(df["taken_at"]).dt.strftime("%d %b %Y %H:%M")
    df = df.rename(columns={"topic": "Unit"})[["Date", "Unit", "Score"]]
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_student_dashboard(user):
    st.header("My Progress")
    render_progress_heatmaps(user["id"])
    render_past_paper_quiz_history(user["id"])
