import streamlit as st


def render_main_graph(question, key_suffix=""):
    fig = question.metadata.get("main_figure")
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True, key=f"vt_graph_{question.qid}{key_suffix}")


def render_option_grid(question, key_prefix):
    labels = question.metadata.get("options", [])
    figures = question.metadata.get("option_figures", {})
    for row_start in range(0, len(labels), 3):
        row_labels = labels[row_start:row_start + 3]
        cols = st.columns(len(row_labels))
        for col, label in zip(cols, row_labels):
            with col:
                st.markdown(f"**{label}**")
                fig = figures.get(label)
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_opt_{label}")


def render_correct_option(question, key_suffix=""):
    label = question.correct_answer
    fig = question.metadata.get("option_figures", {}).get(label)
    if fig is not None:
        st.markdown(f"**Correct combination: {label}**")
        st.plotly_chart(fig, use_container_width=True, key=f"correct_opt_{question.qid}{key_suffix}")
