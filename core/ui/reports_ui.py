import streamlit as st
from collections import Counter, defaultdict
from core.db.client import get_supabase


def _fetch(user_id=None, qualification=None, topic=None, question_type=None):
    try:
        q = get_supabase().table("test_question_attempts").select("*")
        if user_id:
            q = q.eq("user_id", user_id)
        if qualification:
            q = q.eq("qualification", qualification)
        if topic:
            q = q.eq("topic", topic)
        if question_type:
            q = q.eq("question_type", question_type)
        return q.order("attempted_at", desc=True).limit(500).execute().data or []
    except Exception:
        return []


def render_student_insight(user_id, qualification, topic, question_type):
    """Show a personalised tip before the test if there is a repeated mistake pattern."""
    data = _fetch(user_id=user_id, qualification=qualification,
                  topic=topic, question_type=question_type)
    if len(data) < 3:
        return

    wrong = [r["mistake"] for r in data if not r["correct"] and r.get("mistake")]
    if not wrong:
        return

    top_mistake, count = Counter(wrong).most_common(1)[0]
    if count < 2:
        return

    total = len(data)
    accuracy = round(sum(1 for r in data if r["correct"]) / total * 100)

    st.info(
        f"**Based on your recent tests on this topic ({accuracy}% correct):**\n\n"
        f"You've made this error **{count} time{'s' if count > 1 else ''}**:\n\n"
        f"*{top_mistake}*\n\n"
        f"Keep it in mind as you answer!"
    )


def render_teacher_report(qualification):
    """Class-wide mistake report for teachers."""
    st.markdown("## Class Report")

    quals = ["National 4", "National 5", "Higher"]
    selected_qual = st.selectbox(
        "Qualification", ["All"] + quals,
        index=(["All"] + quals).index(qualification) if qualification in quals else 0,
    )

    data = _fetch(qualification=selected_qual if selected_qual != "All" else None)

    if not data:
        st.info("No test data yet. Reports will appear once students have completed tests.")
        return

    # ── Topic performance ──────────────────────────────────────────────────────
    st.markdown("### Topic Performance")
    st.caption("Sorted weakest first.")

    topic_stats: dict = defaultdict(lambda: {"attempts": 0, "correct": 0})
    for row in data:
        key = (row["qualification"], row["topic"], row["question_type"])
        topic_stats[key]["attempts"] += 1
        if row["correct"]:
            topic_stats[key]["correct"] += 1

    perf_rows = []
    for (qual, topic, qtype), stats in topic_stats.items():
        pct = round(stats["correct"] / stats["attempts"] * 100)
        perf_rows.append({
            "Qualification": qual,
            "Topic": topic,
            "Question Type": qtype,
            "Attempts": stats["attempts"],
            "% Correct": pct,
        })
    perf_rows.sort(key=lambda r: r["% Correct"])

    # Format % Correct as string for display
    display_rows = [{**r, "% Correct": f"{r['% Correct']}%"} for r in perf_rows]
    st.dataframe(display_rows, use_container_width=True, hide_index=True)

    # ── Most common mistakes ───────────────────────────────────────────────────
    st.markdown("### Most Common Mistakes")
    st.caption("Only wrong answers where a specific mistake was identified.")

    mistake_counts: dict = defaultdict(lambda: {"times": 0, "students": set()})
    for row in data:
        if not row["correct"] and row.get("mistake"):
            key = (row["topic"], row["question_type"], row["mistake"])
            mistake_counts[key]["times"] += 1
            mistake_counts[key]["students"].add(row["user_id"])

    if not mistake_counts:
        st.info("No specific mistake patterns recorded yet.")
        return

    mistake_rows = [
        {
            "Topic": topic,
            "Question Type": qtype,
            "Mistake": mistake,
            "Times Made": stats["times"],
            "Students Affected": len(stats["students"]),
        }
        for (topic, qtype, mistake), stats in mistake_counts.items()
    ]
    mistake_rows.sort(key=lambda r: r["Times Made"], reverse=True)
    st.dataframe(mistake_rows[:30], use_container_width=True, hide_index=True)

    # ── Per-student breakdown ──────────────────────────────────────────────────
    with st.expander("Per-student breakdown"):
        student_stats: dict = defaultdict(lambda: {"attempts": 0, "correct": 0})
        for row in data:
            student_stats[row["user_id"]]["attempts"] += 1
            if row["correct"]:
                student_stats[row["user_id"]]["correct"] += 1

        # Fetch usernames for the user IDs present
        try:
            ids = list(student_stats.keys())
            users = get_supabase().table("users").select("id, username").in_("id", ids).execute().data or []
            id_to_name = {u["id"]: u["username"] for u in users}
        except Exception:
            id_to_name = {}

        student_rows = []
        for uid, stats in student_stats.items():
            pct = round(stats["correct"] / stats["attempts"] * 100)
            student_rows.append({
                "Student": id_to_name.get(uid, uid[:8] + "…"),
                "Attempts": stats["attempts"],
                "% Correct": f"{pct}%",
            })
        student_rows.sort(key=lambda r: int(r["% Correct"].rstrip("%")))
        st.dataframe(student_rows, use_container_width=True, hide_index=True)
