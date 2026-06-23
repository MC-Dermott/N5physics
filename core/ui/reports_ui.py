import streamlit as st
import pandas as pd
from collections import Counter, defaultdict
from core.db.client import get_supabase
from core.auth.auth import reset_password
from core.ui.student_dashboard_ui import render_progress_heatmaps


def _fetch_all():
    sb = get_supabase()
    users = (
        sb.table("users")
        .select("id,username,role,class_code,created_at")
        .eq("role", "student")
        .order("username")
        .execute().data or []
    )
    attempts = sb.table("question_attempts").select("*").execute().data or []
    tests = sb.table("test_results").select("*").execute().data or []
    return users, attempts, tests


def _fetch_mistakes(user_ids=None):
    try:
        q = get_supabase().table("test_question_attempts").select("*")
        return q.execute().data or []
    except Exception:
        return []


# ── Student insight (shown before a test) ─────────────────────────────────────

def render_student_insight(user_id, qualification, topic, question_type):
    """Show a personalised tip before the test if there is a repeated mistake pattern."""
    try:
        data = (
            get_supabase()
            .table("test_question_attempts")
            .select("*")
            .eq("user_id", user_id)
            .eq("qualification", qualification)
            .eq("topic", topic)
            .eq("question_type", question_type)
            .order("attempted_at", desc=True)
            .limit(30)
            .execute().data or []
        )
    except Exception:
        return

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


# ── Teacher dashboard ──────────────────────────────────────────────────────────

def render_teacher_report(_qualification=None):
    st.header("Teacher Dashboard")

    try:
        all_users, attempts, tests = _fetch_all()
    except Exception as e:
        st.error(f"Could not load data: {e}")
        return

    if not all_users:
        st.info("No students have signed up yet.")
        return

    # ── Class filter ──────────────────────────────────────────────────────────
    class_codes = sorted(c for c in {u.get("class_code") or "" for u in all_users} if c)
    if class_codes:
        selected_class = st.selectbox(
            "Class", ["All classes"] + class_codes,
            label_visibility="collapsed", key="dashboard_class_filter",
        )
        st.caption(f"Showing: **{selected_class}**")
    else:
        selected_class = "All classes"

    users = (
        [u for u in all_users if (u.get("class_code") or "") == selected_class]
        if selected_class != "All classes"
        else all_users
    )
    user_ids = {u["id"] for u in users}
    attempts_f = [a for a in attempts if a["user_id"] in user_ids]
    tests_f    = [t for t in tests    if t["user_id"] in user_ids]

    # ── Overview metrics ──────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("Students", len(users))
    col2.metric("Practice attempts", len(attempts_f))
    col3.metric("Tests taken", len(tests_f))

    st.divider()

    # ── Student overview table ────────────────────────────────────────────────
    st.subheader("Student Overview")
    show_class_col = selected_class == "All classes" and bool(class_codes)
    rows = []
    for u in users:
        uid = u["id"]
        ua = [a for a in attempts_f if a["user_id"] == uid]
        ut = [t for t in tests_f    if t["user_id"] == uid]
        n = len(ua)
        correct = sum(1 for a in ua if a["correct"])
        accuracy = f"{correct / n * 100:.0f}%" if n else "—"
        avg_score = (
            f"{sum(t['score'] for t in ut) / sum(t['total'] for t in ut) * 100:.0f}%"
            if ut else "—"
        )
        row = {"Student": u["username"]}
        if show_class_col:
            row["Class"] = u.get("class_code") or "—"
        row.update({
            "Practice attempts": n,
            "Accuracy": accuracy,
            "Tests taken": len(ut),
            "Avg test score": avg_score,
        })
        rows.append(row)

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()

    # ── Per-student drilldown ─────────────────────────────────────────────────
    st.subheader("Student Detail")
    selected_name = st.selectbox("Select student", [u["username"] for u in users])
    uid = next(u["id"] for u in users if u["username"] == selected_name)

    ua = [a for a in attempts_f if a["user_id"] == uid]
    ut = [t for t in tests_f    if t["user_id"] == uid]

    col_a, col_t = st.columns(2)

    with col_a:
        st.markdown("**Practice attempts**")
        if ua:
            adf = pd.DataFrame(ua)
            summary = (
                adf.groupby(["qualification", "topic", "question_type"])
                .agg(attempts=("correct", "count"), correct=("correct", "sum"))
                .reset_index()
            )
            summary["accuracy"] = (
                (summary["correct"] / summary["attempts"] * 100)
                .round(0).astype(int).astype(str) + "%"
            )
            summary = summary.rename(columns={
                "qualification": "Qual", "topic": "Topic",
                "question_type": "Question type", "attempts": "Attempts",
            }).drop(columns=["correct"])
            st.dataframe(summary, use_container_width=True, hide_index=True)
        else:
            st.info("No practice attempts yet.")

    with col_t:
        st.markdown("**Test results**")
        if ut:
            tdf = pd.DataFrame(ut)
            tdf["Score"] = tdf["score"].astype(str) + " / " + tdf["total"].astype(str)
            tdf["Date"] = pd.to_datetime(tdf["taken_at"]).dt.strftime("%d %b %Y %H:%M")
            tdf = tdf.rename(columns={
                "qualification": "Qual", "topic": "Topic",
                "question_type": "Question type",
            })[["Date", "Qual", "Topic", "Question type", "Score"]]
            st.dataframe(tdf, use_container_width=True, hide_index=True)
        else:
            st.info("No tests taken yet.")

    st.divider()

    # ── Progress heatmap ──────────────────────────────────────────────────────
    st.subheader("Progress Heatmap")
    render_progress_heatmaps(uid)

    st.divider()

    # ── Class-wide mistake analysis ───────────────────────────────────────────
    st.subheader("Common Mistakes (class-wide)")
    st.caption("Drawn from per-question test data. Only wrong answers with a recorded mistake are shown.")

    mistakes = _fetch_mistakes()
    mistakes = [m for m in mistakes if m["user_id"] in user_ids]

    if mistakes:
        mc: dict = defaultdict(lambda: {"times": 0, "students": set()})
        for row in mistakes:
            if not row["correct"] and row.get("mistake"):
                key = (row["topic"], row["question_type"], row["mistake"])
                mc[key]["times"] += 1
                mc[key]["students"].add(row["user_id"])

        if mc:
            mrows = [
                {
                    "Topic": t,
                    "Question Type": qt,
                    "Mistake": m,
                    "Times made": s["times"],
                    "Students affected": len(s["students"]),
                }
                for (t, qt, m), s in mc.items()
            ]
            mrows.sort(key=lambda r: r["Times made"], reverse=True)
            st.dataframe(mrows[:30], use_container_width=True, hide_index=True)
        else:
            st.info("No specific mistake patterns recorded yet.")
    else:
        st.info("No mistake data yet — this populates after students complete tests.")

    st.divider()

    # ── Student Accounts ──────────────────────────────────────────────────────
    st.subheader("Student Accounts")
    account_action = st.radio(
        "Action",
        ["Assign Class Code", "Reset Password"],
        horizontal=True,
        label_visibility="collapsed",
        key="student_accounts_action",
    )

    if account_action == "Assign Class Code":
        assign_name = st.selectbox("Student", [u["username"] for u in all_users], key="assign_select")
        assign_user = next(u for u in all_users if u["username"] == assign_name)
        with st.form("assign_class_form"):
            new_code = st.text_input("Class code", value=assign_user.get("class_code") or "", placeholder="e.g. 5A")
            if st.form_submit_button("Save", type="primary"):
                try:
                    code_to_save = new_code.strip().upper() or None
                    get_supabase().table("users").update({"class_code": code_to_save}).eq("id", assign_user["id"]).execute()
                    st.success(f"Class code for **{assign_name}** updated to **{code_to_save or '(none)'}**.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Update failed: {e}")

    else:
        reset_name = st.selectbox("Student", [u["username"] for u in all_users], key="reset_select")
        with st.form("reset_password_form"):
            new_pw = st.text_input("New password", type="password")
            confirm_pw = st.text_input("Confirm new password", type="password")
            if st.form_submit_button("Reset password", type="primary"):
                if not new_pw:
                    st.error("Please enter a new password.")
                elif new_pw != confirm_pw:
                    st.error("Passwords do not match.")
                elif len(new_pw) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    reset_uid = next(u["id"] for u in all_users if u["username"] == reset_name)
                    err = reset_password(reset_uid, new_pw)
                    if err:
                        st.error(err)
                    else:
                        st.success(f"Password for **{reset_name}** has been reset.")
