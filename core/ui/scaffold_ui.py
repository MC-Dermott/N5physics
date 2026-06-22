import streamlit as st
import streamlit.components.v1 as components


def _is_correct(user_input, expected, tolerance=0.02):
    try:
        student = float(str(user_input).replace(",", "").strip())
        exp = float(expected)
        if abs(exp) < 1e-9:
            return abs(student) < 0.01
        return abs(student - exp) / abs(exp) <= tolerance
    except (ValueError, TypeError):
        return str(user_input).strip().lower() == str(expected).strip().lower()


def render_scaffold(question, suffix=""):
    widget_html = question.metadata.get("widget_html")
    if widget_html:
        with st.expander("🎬 Interactive Visualisation"):
            components.html(widget_html, height=520)

    if not question.scaffold:
        return
    with st.expander("🔍 Step-by-step scaffold"):
        for i, step in enumerate(question.scaffold):
            st.markdown(f"**Step {i + 1}:** {step['prompt']}")

            inp_key = f"scaf_{question.qid}_{suffix}_{i}_inp"
            chk_key = f"scaf_{question.qid}_{suffix}_{i}_chk"
            ok_key  = f"scaf_{question.qid}_{suffix}_{i}_ok"

            col1, col2 = st.columns([3, 1])
            with col1:
                user_val = st.text_input("Answer:", key=inp_key, label_visibility="visible")
            with col2:
                st.write("")
                st.write("")
                if st.button("Check", key=f"scaf_{question.qid}_{suffix}_{i}_btn"):
                    st.session_state[chk_key] = True
                    st.session_state[ok_key] = _is_correct(user_val, step["answer"])

            if st.session_state.get(chk_key):
                if st.session_state.get(ok_key):
                    st.success("✓ Correct!")
                else:
                    st.error("✗ Not quite — check your working and try again.")

            if i < len(question.scaffold) - 1:
                st.divider()
