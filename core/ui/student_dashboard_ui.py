import re

import streamlit as st
import pandas as pd
from core.db.client import get_supabase
from core.engine.question_factory import QUAL_REGISTRY
from core.engine.units import unit_names

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


def _fetch_wrong_with_mistake(user_id):
    """All of a pupil's wrong test answers, paged because Supabase caps the rows per request."""
    rows = []
    while True:
        batch = (
            get_supabase()
            .table("test_question_attempts")
            .select("*")
            .eq("user_id", user_id)
            .eq("correct", False)
            .order("attempted_at", desc=True)
            .order("id")
            .range(len(rows), len(rows) + 999)
            .execute()
            .data or []
        )
        if not batch:
            return [r for r in rows if r.get("mistake")]
        rows += batch


def common_mistakes(rows, min_times=2, limit=10):
    """Repeated mistakes, most frequent first (ties: most recent first). Messages that differ
    only in their numbers count as the same mistake; the latest wording is the one shown."""
    groups = {}
    for r in sorted(rows, key=lambda r: r["attempted_at"], reverse=True):
        if r.get("correct") or not r.get("mistake"):
            continue
        key = (r["qualification"], r["topic"], r["question_type"],
               re.sub(r"\d+(?:[.,]\d+)*", "#", r["mistake"]))
        if key not in groups:
            groups[key] = {**r, "times": 0}
        groups[key]["times"] += 1
    repeated = [g for g in groups.values() if g["times"] >= min_times]
    # Stable sort, so equal counts stay newest first.
    return sorted(repeated, key=lambda g: g["times"], reverse=True)[:limit]


def render_common_mistakes(user_id):
    st.subheader("My Common Mistakes")
    try:
        rows = _fetch_wrong_with_mistake(user_id)
    except Exception as e:
        st.error(f"Could not load your mistakes: {e}")
        return

    mistakes = common_mistakes(rows)
    if not mistakes:
        st.info("No repeated mistakes yet. A mistake appears here once the app has spotted it "
                "at least twice in your tests.")
        return

    st.caption("Mistakes spotted at least twice in your tests, most frequent first.")
    for m in mistakes:
        last = pd.to_datetime(m["attempted_at"]).strftime("%d %b %Y")
        with st.container(border=True):
            st.markdown(f"**{m['question_type']}** · {m['qualification']} · {m['topic']}")
            st.markdown(m["mistake"])
            st.caption(f"Made {m['times']} times · last on {last}")


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
        tested_quals = set(df["qualification"].unique())
    else:
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
        # includes tests saved under the unit's old name, before it was split
        scores = df.loc[(df["qualification"] == level) & df["topic"].isin(unit_names(level, unit))
                        & (df["question_type"] == qt), "pct"]
        pct, attempts = (scores.mean() if len(scores) else None), len(scores)

        colour = _colour_for(pct)
        if pct is None:
            detail = "No tests yet"
        else:
            detail = f"{pct:.0f}% ({attempts} test{'s' if attempts != 1 else ''})"
        st.markdown(f"{colour} &nbsp; **{qt}** — {detail}")

    st.caption("🟢 > 70%   🟡 50 – 70%   🔴 < 50%   ⚪ No tests taken")


def render_past_paper_quiz_history(user_id, kind="Past Paper Quiz", heading="Past Paper Quizzes"):
    """Recent unit-level attempts (Past Paper Quizzes, Unit Assessments). Shown
    separately from the heatmap above since these span a whole unit rather than
    one curriculum topic, so they can't slot into that per-topic grid."""
    try:
        tests = _fetch_tests(user_id)
    except Exception:
        return

    quizzes = [t for t in tests if t["question_type"] == kind]
    if not quizzes:
        return

    quizzes.sort(key=lambda t: t["taken_at"], reverse=True)
    st.subheader(heading)
    df = pd.DataFrame(quizzes)
    df["Score"] = df["score"].astype(str) + " / " + df["total"].astype(str)
    df["Date"] = pd.to_datetime(df["taken_at"]).dt.strftime("%d %b %Y %H:%M")
    df = df.rename(columns={"topic": "Unit"})[["Date", "Unit", "Score"]]
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_student_dashboard(user):
    st.header("My Progress")
    render_progress_heatmaps(user["id"])
    render_past_paper_quiz_history(user["id"], "Unit Assessment", "Unit Assessments")
    render_past_paper_quiz_history(user["id"])
    render_common_mistakes(user["id"])
