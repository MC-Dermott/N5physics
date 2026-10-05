import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from core.engine.session_manager import reset_test
from core.ui.feedback_ui import check_answer, render_diagram, render_feedback, render_working
from core.ui.graph_mcq_ui import render_main_graph, render_option_grid
from utils.answer_format import format_answer
from utils.diagrams import diagram_markdown as question_diagram_markdown
from utils.notes import format_math
from core.ui.test_nav import GO_BACK_HINT, nav_buttons, refill

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
    """The current question of a test (or unit assessment) in progress. Pupils can go back and
    change any answer until they submit the last question — each question's response is kept in
    test["responses"] and only flattened into answers/results/feedback when the test ends."""
    test.setdefault("responses", {})
    idx = test["index"]
    question = test["questions"][idx]
    total = len(test["questions"])

    st.progress((idx + 1) / total, text=f"Question {idx + 1} of {total}")
    st.caption(GO_BACK_HINT)

    if question.is_scenario:
        _render_scenario_test(test, idx, question)
    else:
        _render_single_test(test, idx, question)


def _scored_parts(question):
    return [p for p in question.parts if p.metadata.get("type") != "explain"]


def _scenario_keys(idx):
    return f"scenario_part_idx_{idx}", f"scenario_part_answers_{idx}"


def _move(test, back):
    """Step to the previous or next question, or finish the test after the last one."""
    questions = test["questions"]
    if back:
        test["index"] -= 1
        previous = questions[test["index"]]
        if previous.is_scenario:   # come back in on its last part
            st.session_state[_scenario_keys(test["index"])[0]] = len(_scored_parts(previous)) - 1
    elif test["index"] == len(questions) - 1:
        for i in range(len(questions)):
            for display_answer, result, distractor, part, _raw in test["responses"][i]:
                test["answers"].append(display_answer)
                test["results"].append(result == "correct")
                test["feedback"].append((result, distractor, part))
        test["complete"] = True
    else:
        test["index"] += 1
        st.session_state.pop(_scenario_keys(test["index"])[0], None)
    st.rerun()


_UNIT_HINT = ("Use `/` for per and `^2` for squared — e.g. `m/s`, `m/s^2`. Units are not case sensitive. "
              "Powers of ten can be typed as `3.2x10^-19` or `3.2e-19`.")


def _check_classification(selected, question):
    if selected == question.correct_answer:
        return "correct", None
    for d in question.distractors:
        if d["value"] == selected:
            return "distractor", d
    return "incorrect", None


def _answer_widgets(q, key, saved):
    """The radio, or answer (and units) boxes, for a question or scenario part, refilled with
    the pupil's saved response if they've come back to it. Returns the response
    (display_answer, result_type, distractor, q, raw_inputs), or None if no option is chosen."""
    raw = saved[4] if saved else {}
    q_type = q.metadata.get("type")
    if q_type in ("classification", "graph_mcq"):
        options = q.metadata.get("options", [q.correct_answer] + [d["value"] for d in q.distractors])
        radio_key = f"test_radio_{key}"
        if raw.get("choice") in options:
            refill(radio_key, raw["choice"])
        selected = st.radio("Select your answer:", options, key=radio_key, index=None,
                            horizontal=q_type == "graph_mcq")
        if selected is None:
            return None
        result, distractor = _check_classification(selected, q)
        return selected, result, distractor, q, {"choice": selected}

    refill(f"test_ans_{key}", raw.get("answer"))
    if q.unit:
        refill(f"test_unit_{key}", raw.get("unit"))
        col1, col2 = st.columns([3, 2])
        with col1:
            answer = st.text_input("Your answer:", key=f"test_ans_{key}")
        with col2:
            unit_input = st.text_input("Units:", key=f"test_unit_{key}", placeholder="e.g. m/s")
        st.caption(_UNIT_HINT)
    else:
        answer = st.text_input("Your answer:", key=f"test_ans_{key}")
        unit_input = None
    result, distractor = check_answer(answer, q, unit_input=unit_input)
    display_answer = f"{answer} {unit_input}".strip() if unit_input else answer
    return display_answer, result, distractor, q, {"answer": answer, "unit": unit_input}


def _render_single_test(test, idx, question):
    st.markdown(question.question_text)
    render_diagram(question)
    st.write("")

    if question.metadata.get("main_figure") is not None:
        render_main_graph(question, key_suffix=f"_test_{idx}")
        st.write("")
    if question.metadata.get("type") == "graph_mcq":
        render_option_grid(question, key_prefix=f"test_{idx}")

    saved = test["responses"].get(idx, [None])[0]
    response = _answer_widgets(question, str(idx), saved)
    back, submit = nav_buttons(f"test_{idx}", idx > 0)
    if submit and response is None:
        st.warning("Please select an answer before submitting.")
        return
    if back or submit:
        # going back keeps whatever was entered, but doesn't record a blank as an answer
        if response is not None and (submit or response[0]):
            test["responses"][idx] = [response]
        _move(test, back)


def _render_scenario_test(test, idx, question):
    """Treat each scored scenario part as a separate test question. Explain parts are skipped."""
    scored_parts = _scored_parts(question)
    part_idx_key, part_answers_key = _scenario_keys(idx)
    st.session_state.setdefault(part_idx_key, 0)
    if part_answers_key not in st.session_state:
        st.session_state[part_answers_key] = list(test["responses"].get(idx, [None] * len(scored_parts)))
    answers = st.session_state[part_answers_key]
    part_idx = st.session_state[part_idx_key]

    if question.metadata.get("exam_style"):
        st.caption("📝 Exam-style question · covers " + ", ".join(question.metadata.get("covers", [])))

    if question.scenario_context:
        st.info(question.scenario_context)
    render_diagram(question)

    if question.metadata.get("main_figure") is not None:
        render_main_graph(question, key_suffix=f"_test_{idx}_scenario")
        st.write("")

    part = scored_parts[part_idx]
    st.markdown(f"**Part {part_idx + 1} of {len(scored_parts)}:** {part.question_text}")
    st.write("")

    if part.metadata.get("type") == "graph_mcq":
        if part.metadata.get("main_figure") is not None:
            render_main_graph(part, key_suffix=f"_test_{idx}_p{part_idx}")
            st.write("")
        render_option_grid(part, key_prefix=f"test_{idx}_p{part_idx}")

    response = _answer_widgets(part, f"{idx}_p{part_idx}", answers[part_idx])
    back, submit = nav_buttons(f"test_{idx}_p{part_idx}", idx > 0 or part_idx > 0)
    if submit and response is None:
        st.warning("Please select an answer before submitting.")
        return
    if response is not None and (submit or response[0]):
        answers[part_idx] = response
    if back and part_idx > 0:
        st.session_state[part_idx_key] -= 1
        st.rerun()
    if submit and part_idx + 1 < len(scored_parts):
        st.session_state[part_idx_key] += 1
        st.rerun()
    if back or submit:
        if submit or any(answers):
            test["responses"][idx] = [a or ("", "incorrect", None, p, {})
                                      for a, p in zip(answers, scored_parts)]
        del st.session_state[part_idx_key]
        del st.session_state[part_answers_key]
        _move(test, back)


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
            if q_ref.metadata.get("scenario_diagram"):
                st.markdown(question_diagram_markdown(q_ref.metadata["scenario_diagram"]))
        last_context = context
        if not context:
            render_diagram(q_ref)

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
