import random
from pathlib import Path

import streamlit as st

from core.data.past_papers import get_past_paper_entries

_ASSETS_DIR = Path(__file__).parent.parent / "data" / "past_paper_assets"


def _img_paths(entry, key):
    return [str(_ASSETS_DIR / p) for p in entry.get(key, [])]


def render_past_papers(topic, question_type):
    entries = get_past_paper_entries(topic, question_type)
    if not entries:
        st.info("No past paper questions added yet for this topic.")
        return

    if st.button("Show a Past Paper Question", type="primary"):
        st.session_state.past_paper_current = random.choice(entries)
        st.session_state.past_paper_revealed = False
        st.rerun()

    entry = st.session_state.get("past_paper_current")
    if not entry:
        st.caption("Press **Show a Past Paper Question** to begin.")
        return

    year_label = "Specimen Paper" if entry["year"] == "SPQ" else entry["year"]
    paper_label = "Paper 1 (Multiple Choice)" if entry["paper"] == "P1" else "Paper 2"
    st.caption(f"**{year_label} — {paper_label} — Question {entry['qnum']}**")

    for img in _img_paths(entry, "question_images"):
        st.image(img)

    reveal_label = "Show Answer" if entry["kind"] == "mcq" else "Show Marking Instructions"
    if st.button(reveal_label):
        st.session_state.past_paper_revealed = True

    if st.session_state.get("past_paper_revealed"):
        answer_text = entry.get("answer_text")
        if answer_text:
            st.success(f"Correct answer: **{answer_text}**")
        for img in _img_paths(entry, "answer_images"):
            st.image(img)
