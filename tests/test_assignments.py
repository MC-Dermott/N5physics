"""Assignment logic and page smoke tests (no database): python3 -m pytest tests/ or run directly."""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.db import assignments as db

ITEMS = [dict(qualification="Higher", topic="U", question_type="A"),
         dict(qualification="Higher", topic="U", question_type="B")]


def res(qt, score, total=5, **kw):
    return dict(qualification="Higher", topic="U", question_type=qt, score=score, total=total, **kw)


def test_item_status():
    assert db.item_status(ITEMS[0], [], 60)["state"] == db.NOT_STARTED
    assert db.item_status(ITEMS[0], [res("B", 5)], 60)["state"] == db.NOT_STARTED   # other item
    s = db.item_status(ITEMS[0], [res("A", 2)], 60)
    assert s["state"] == db.IN_PROGRESS and s["best"] == 40 and s["attempts"] == 1
    s = db.item_status(ITEMS[0], [res("A", 2), res("A", 3)], 60)                      # best counts, 3/5 = 60 %
    assert s["state"] == db.DONE and s["attempts"] == 2
    assert db.item_status(ITEMS[0], [res("A", 0, total=0)], 60)["state"] == db.NOT_STARTED


def test_assignment_status():
    s = db.assignment_status(ITEMS, [res("A", 5)], 60)
    assert (s["state"], s["done"], s["total"]) == (db.IN_PROGRESS, 1, 2)
    s = db.assignment_status(ITEMS, [res("A", 5), res("B", 4)], 60)
    assert s["state"] == db.DONE
    assert db.assignment_status(ITEMS, [], 60)["state"] == db.NOT_STARTED
    assert db.assignment_status(ITEMS, [res("A", 1)], 60)["state"] == db.IN_PROGRESS


def test_overdue():
    a = {"due_date": "2026-10-01"}
    assert db.is_overdue(a, db.NOT_STARTED, today=date(2026, 10, 8))
    assert not db.is_overdue(a, db.DONE, today=date(2026, 10, 8))
    assert not db.is_overdue({"due_date": None}, db.NOT_STARTED)


def test_recipients():
    students = [dict(id="1", class_code="5A"), dict(id="2", class_code="5b"), dict(id="3", class_code=None)]
    a = {"targets": [dict(class_code="5B"), dict(user_id="3")]}
    assert [s["id"] for s in db.recipients(a, students)] == ["2", "3"]


def test_save_test_result_omits_assignment_id_when_unset():
    from core.db import tracker
    sent = []

    class T:
        def insert(self, row): sent.append(row); return self
        def execute(self): return self
    class C:
        def table(self, _): return T()
    tracker.get_supabase = lambda: C()
    assert tracker.save_test_result("u", "Higher", "U", "A", 3, 5)
    assert "assignment_id" not in sent[0]
    assert tracker.save_test_result("u", "Higher", "U", "A", 3, 5, assignment_id="x")
    assert sent[1]["assignment_id"] == "x"


def test_pages_render():
    from streamlit.testing.v1 import AppTest
    from core.engine.question_factory import QUAL_REGISTRY
    qual = next(iter(QUAL_REGISTRY)); unit = next(iter(QUAL_REGISTRY[qual])); qt = next(iter(QUAL_REGISTRY[qual][unit]))
    item = dict(id="i1", assignment_id="a1", qualification=qual, topic=unit, question_type=qt)
    a = dict(id="a1", title="T", pass_pct=60, due_date="2026-10-01", items=[item], results=[],
             status=db.assignment_status([item], [], 60))
    script = f"""
import streamlit as st
from core.db import assignments as db
db.pupil_assignments = lambda user: [{a!r}]
from core.engine.session_manager import initialise_session
initialise_session()
from core.ui.assignments_ui import render_my_assignments, render_assignment_runner
user = {{"id": "u1", "username": "p", "class_code": "5A"}}
if st.session_state.get("active_assignment"):
    render_assignment_runner(user)
else:
    render_my_assignments(user)
"""
    at = AppTest.from_string(script).run(timeout=30)
    assert not at.exception, at.exception
    assert any("overdue" in e.label for e in at.expander)
    start = next(b for b in at.button if b.label == "Start")
    start.click(); at.run(timeout=30)
    assert not at.exception, at.exception
    assert any("Start Test" in b.label or "Start Unit" in b.label for b in at.button), [b.label for b in at.button]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
