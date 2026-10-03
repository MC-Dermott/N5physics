import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from core.engine.session_manager import reset_test
from core.ui.feedback_ui import check_answer, render_feedback, render_working
from core.ui.graph_mcq_ui import render_main_graph, render_option_grid
from utils.answer_format import format_answer
from utils.notes import format_math

_GAME_HTML_PATH = Path(__file__).parent / "assets" / "geometry_dash.html"
_game_html_cache = None


def _load_game_html():
    global _game_html_cache
    if _game_html_cache is None:
        _game_html_cache = _GAME_HTML_PATH.read_text(encoding="utf-8")
    return _game_html_cache


def render_test(topic, question_type, qualification, generate_fn, user_id=None, example=None,
                num_questions=5, exam_style=False):
    from core.db.tracker import save_test_result, save_test_question_attempt

    test = st.session_state.test

    # --- Start screen ---
    if not test["questions"]:
        if user_id:
            from core.ui.reports_ui import render_student_insight
            render_student_insight(user_id, qualification, topic, question_type)

        if exam_style:
            st.markdown(
                f"You will be given **{num_questions} exam-style questions** from across *{topic}*, "
                "each with several parts that draw on different topics, like an SQA paper. "
                "Every part is marked automatically. "
                "A summary with feedback is shown at the end."
            )
        else:
            st.markdown(
                f"You will be given **{num_questions} questions** on *{question_type}*. "
                "Each question is marked automatically. A summary with feedback is shown at the end."
            )
        if st.button("Start Test", type="primary"):
            reset_test()
            st.session_state.test["questions"] = [generate_fn() for _ in range(num_questions)]
            st.rerun()

        if example:
            with st.expander("💡 Example"):
                st.markdown(format_math(example))
        return

    # --- Summary screen ---
    if test["complete"]:
        if not test.get("saved") and user_id:
            total = len(test["results"])
            save_test_result(user_id, qualification, topic, question_type,
                             sum(test["results"]), total)
            # Save per-question results with mistake text
            for result_type, distractor, q in test["feedback"]:
                correct = result_type == "correct"
                mistake = None
                if result_type == "distractor" and distractor:
                    mistake = distractor.get("mistake")
                save_test_question_attempt(
                    user_id, qualification, q.topic, q.question_type, correct, mistake
                )
            test["saved"] = True
        if test["results"] and all(test["results"]) and "game_unlock_time" not in test:
            test["game_unlock_time"] = time.time()
        _render_summary(test)
        if st.button("Start New Test", type="primary"):
            reset_test()
            st.rerun()
        return

    render_active_question(test)


def render_active_question(test):
    """The current question of a test (or unit assessment) in progress."""
    idx = test["index"]
    question = test["questions"][idx]
    total = len(test["questions"])

    st.progress((idx + 1) / total, text=f"Question {idx + 1} of {total}")

    if question.is_scenario:
        _render_scenario_test(test, idx, question)
    else:
        _render_single_test(test, idx, question)


def _finish_question(test):
    test["index"] += 1
    if test["index"] >= len(test["questions"]):
        test["complete"] = True


_UNIT_HINT = ("Use `/` for per and `^2` for squared — e.g. `m/s`, `m/s^2`. Units are not case sensitive. "
              "Powers of ten can be typed as `3.2x10^-19` or `3.2e-19`.")


def _check_classification(selected, question):
    if selected == question.correct_answer:
        return "correct", None
    for d in question.distractors:
        if d["value"] == selected:
            return "distractor", d
    return "incorrect", None


def _render_single_test(test, idx, question):
    st.markdown(question.question_text)
    st.write("")

    q_type = question.metadata.get("type")
    is_classification = q_type == "classification"
    is_graph_mcq = q_type == "graph_mcq"

    if question.metadata.get("main_figure") is not None:
        render_main_graph(question, key_suffix=f"_test_{idx}")
        st.write("")

    if is_graph_mcq:
        render_option_grid(question, key_prefix=f"test_{idx}")
        labels = question.metadata.get("options", [])
        selected = st.radio("Select your answer:", labels,
                            key=f"test_radio_{idx}", index=None, horizontal=True)
        if st.button("Submit", key=f"test_submit_{idx}", type="primary"):
            if selected is not None:
                result, distractor = _check_classification(selected, question)
                test["answers"].append(selected)
                test["results"].append(result == "correct")
                test["feedback"].append((result, distractor, question))
                _finish_question(test)
                st.rerun()
            else:
                st.warning("Please select an answer before submitting.")
    elif is_classification:
        options = question.metadata.get(
            "options",
            [question.correct_answer] + [d["value"] for d in question.distractors],
        )
        selected = st.radio("Select your answer:", options,
                            key=f"test_radio_{idx}", index=None)
        if st.button("Submit", key=f"test_submit_{idx}", type="primary"):
            if selected is not None:
                result, distractor = _check_classification(selected, question)
                test["answers"].append(selected)
                test["results"].append(result == "correct")
                test["feedback"].append((result, distractor, question))
                _finish_question(test)
                st.rerun()
            else:
                st.warning("Please select an answer before submitting.")
    else:
        if question.unit:
            col1, col2 = st.columns([3, 2])
            with col1:
                answer = st.text_input("Your answer:", key=f"test_ans_{idx}")
            with col2:
                unit_input = st.text_input("Units:", key=f"test_unit_{idx}",
                                           placeholder="e.g. m/s")
            st.caption(_UNIT_HINT)
        else:
            answer = st.text_input("Your answer:", key=f"test_ans_{idx}")
            unit_input = None

        if st.button("Submit", key=f"test_submit_{idx}", type="primary"):
            result, distractor = check_answer(answer, question, unit_input=unit_input)
            display_answer = f"{answer} {unit_input}".strip() if unit_input else answer
            test["answers"].append(display_answer)
            test["results"].append(result == "correct")
            test["feedback"].append((result, distractor, question))
            _finish_question(test)
            st.rerun()


def _render_scenario_test(test, idx, question):
    """Treat each scored scenario part as a separate test question. Explain parts are skipped."""
    scored_parts = [p for p in question.parts if p.metadata.get("type") != "explain"]

    part_idx_key = f"scenario_part_idx_{idx}"
    part_answers_key = f"scenario_part_answers_{idx}"

    if part_idx_key not in st.session_state:
        st.session_state[part_idx_key] = 0
        st.session_state[part_answers_key] = []

    part_idx = st.session_state[part_idx_key]

    if question.metadata.get("exam_style"):
        st.caption("📝 Exam-style question · covers " + ", ".join(question.metadata.get("covers", [])))

    if question.scenario_context:
        st.info(question.scenario_context)

    if question.metadata.get("main_figure") is not None:
        render_main_graph(question, key_suffix=f"_test_{idx}_scenario")
        st.write("")

    part = scored_parts[part_idx]
    st.markdown(f"**Part {part_idx + 1} of {len(scored_parts)}:** {part.question_text}")
    st.write("")

    part_type = part.metadata.get("type")
    is_graph_mcq = part_type == "graph_mcq"
    is_classification = part_type == "classification" or is_graph_mcq

    def _advance(display_answer, result, distractor, part):
        st.session_state[part_answers_key].append((display_answer, result, distractor, part))
        if part_idx + 1 < len(scored_parts):
            st.session_state[part_idx_key] += 1
            st.rerun()
        else:
            for ans, res, dist, p in st.session_state[part_answers_key]:
                test["answers"].append(ans)
                test["results"].append(res == "correct")
                test["feedback"].append((res, dist, p))
            _finish_question(test)
            del st.session_state[part_idx_key]
            del st.session_state[part_answers_key]
            st.rerun()

    if is_classification:
        if is_graph_mcq:
            if part.metadata.get("main_figure") is not None:
                render_main_graph(part, key_suffix=f"_test_{idx}_p{part_idx}")
                st.write("")
            render_option_grid(part, key_prefix=f"test_{idx}_p{part_idx}")
        options = part.metadata.get("options", [])
        selected = st.radio("Select your answer:", options,
                            key=f"test_radio_{idx}_p{part_idx}", index=None,
                            horizontal=is_graph_mcq)
        if st.button("Submit", key=f"test_submit_{idx}_p{part_idx}", type="primary"):
            if selected is not None:
                result, distractor = _check_classification(selected, part)
                _advance(selected, result, distractor, part)
            else:
                st.warning("Please select an answer before submitting.")
    else:
        if part.unit:
            col1, col2 = st.columns([3, 2])
            with col1:
                answer = st.text_input("Your answer:", key=f"test_ans_{idx}_p{part_idx}")
            with col2:
                unit_input = st.text_input("Units:", key=f"test_unit_{idx}_p{part_idx}",
                                           placeholder="e.g. m/s")
            st.caption(_UNIT_HINT)
        else:
            answer = st.text_input("Your answer:", key=f"test_ans_{idx}_p{part_idx}")
            unit_input = None

        if st.button("Submit", key=f"test_submit_{idx}_p{part_idx}", type="primary"):
            result, distractor = check_answer(answer, part, unit_input=unit_input)
            display_answer = f"{answer} {unit_input}".strip() if unit_input else answer
            _advance(display_answer, result, distractor, part)


def _render_game_reward(test):
    """5/5 unlocks a 60-second play of the bespoke Geometry Dash reward game."""
    remaining = max(0, 60 - int(time.time() - test.get("game_unlock_time", time.time())))
    if remaining <= 0:
        st.info("Time's up! Start a new test to keep practising.")
        return

    timer_block = f"""
        <div id="n5-timer-text" style="font-family:sans-serif;text-align:center;color:#eaeaea;margin:6px 0 0;">
            ⏱ Game available for <span id="n5-secs">{remaining}</span> seconds
        </div>
        <script>
        (function() {{
            var s = {remaining};
            var secsEl = document.getElementById('n5-secs');
            var timerText = document.getElementById('n5-timer-text');
            var wrap = document.getElementById('wrap');
            var iv = setInterval(function() {{
                s--;
                if (secsEl) secsEl.textContent = s;
                if (s <= 0) {{
                    clearInterval(iv);
                    if (window.n5StopGame) window.n5StopGame();
                    wrap.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;' +
                        'min-height:380px;background:rgba(10,10,20,0.97);color:#fff;font-family:sans-serif;' +
                        'font-size:1.1em;text-align:center;border-radius:8px;padding:20px;">' +
                        "Time's up! Pick another set of questions to play again." + '</div>';
                    timerText.style.display = 'none';
                }}
            }}, 1000);
        }})();
        </script>
    </body>"""
    game_page = _load_game_html().replace("</body>", timer_block)
    components.html(game_page, height=460, scrolling=False)


def _render_summary(test):
    score = sum(test["results"])
    total = len(test["results"])

    st.markdown(f"## Result: {score} / {total}")
    if score == total:
        st.success("Perfect score! Excellent work!")
        _render_game_reward(test)
    elif score >= total * 0.6:
        st.info(f"Good effort — {score} out of {total} correct.")
    else:
        st.warning(f"{score} out of {total} correct. Keep practising!")

    render_review(test)


def render_review(test):
    """Every answer in a finished test, with feedback. The parts of a multi-part
    question are shown under its scenario."""
    st.markdown("---")
    st.markdown("### Question Review")

    last_context = None
    for q_num, (result_type, distractor, q_ref) in enumerate(test["feedback"], start=1):
        answer = test["answers"][q_num - 1]
        correct = test["results"][q_num - 1]

        context = q_ref.metadata.get("scenario_context")
        if context and context != last_context:
            st.info(context)
        last_context = context

        correct_str = format_answer(q_ref)
        if correct:
            st.success(f"**Q{q_num}:** {q_ref.question_text}  \nYour answer: **{answer}** ✅")
        elif result_type == "wrong_unit":
            with st.container(border=True):
                st.warning(
                    f"**Q{q_num}:** {q_ref.question_text}  \n"
                    f"Your answer: **{answer}** ⚠️  \n"
                    f"Correct answer: **{correct_str}** — value correct, unit wrong!"
                )
                if q_ref.working:
                    with st.expander("📖 Worked Solution"):
                        render_working(q_ref.working)
        else:
            with st.container(border=True):
                st.error(
                    f"**Q{q_num}:** {q_ref.question_text}  \n"
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
