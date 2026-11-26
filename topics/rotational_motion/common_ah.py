"""Shared helpers for the Advanced Higher question generators.

calc() builds a numerical question and explain() a multiple-choice state/explain question.
Constants are the values on the AH data sheet.
"""
import math
import random

from core.models.question_model import PhysicsQuestion
from topics.exam_style.base import L, T, fmt, ltx, sig
from utils.make_question import make_question

__all__ = ["L", "T", "fmt", "ltx", "sig", "calc", "explain", "explain_set", "uni", "pick_sig",
           "UNIT", "LEVEL", "G", "C", "SIGMA", "M_EARTH", "R_EARTH", "M_SUN", "R_SUN",
           "AU", "LIGHT_YEAR", "EXPLAIN_TIP"]

UNIT = "Rotational Motion and Astrophysics"
LEVEL = "AH"

G = 6.67e-11
C = 3.00e8
SIGMA = 5.67e-8
M_EARTH = 6.0e24
R_EARTH = 6.4e6
M_SUN = 2.0e30
R_SUN = 6.955e8
AU = 1.5e11
LIGHT_YEAR = C * 365.25 * 24 * 3600

EXPLAIN_TIP = """
**How to answer an "explain" or "justify" question:** identify the principle first, then write
cause → effect steps, one point for each mark. Say what stays constant, state the relationship,
use the key terms and answer the question that was asked.
"""


def uni(lo, hi, dp=1):
    return round(random.uniform(lo, hi), dp)


def pick_sig(lo, hi, sf=2):
    """A random value between lo and hi to sf significant figures."""
    return sig(random.uniform(lo, hi), sf)


def calc(qtype, text, answer, unit, working, wrong=(), scaffold=(), notes="", sf=3, topic=UNIT):
    """working: LaTeX strings or L()/T() dicts. wrong: (value, mistake) pairs from common errors.
    scaffold: (prompt, answer[, unit]) checkpoints."""
    answer = sig(answer, sf)
    work = [w if isinstance(w, dict) else L(w) for w in working]
    options = [{"value": answer, "mistake": None, "working": work}]
    for value, mistake in wrong:
        value = sig(value, sf)
        if not math.isfinite(value) or any(
                math.isclose(value, o["value"], rel_tol=0.03, abs_tol=1e-300) for o in options):
            continue
        options.append({"value": value, "mistake": mistake, "working": work,
                        "display": f"{fmt(value)} {unit}".strip()})
    steps = [{"question": s[0], "answer": sig(s[1], sf), "unit": s[2] if len(s) > 2 else ""}
             for s in scaffold]
    return make_question(text, answer, options, unit, scaffold=steps, notes=notes,
                         topic=topic, question_type=qtype, level=LEVEL)


def explain(qtype, text, correct, wrong, why, notes="", topic=UNIT):
    """wrong: (option, why it's wrong) pairs. why: the reasoning shown as the worked solution."""
    working = [T(w) for w in ([why] if isinstance(why, str) else why)]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(
        question_text=text, correct_answer=correct, unit="", topic=topic, question_type=qtype,
        level=LEVEL, notes=notes + EXPLAIN_TIP, working=working,
        distractors=[{"value": w, "mistake": m, "working": working} for w, m in wrong],
        metadata={"type": "classification", "options": options},
    )


def explain_set(qtype, bank, notes="", topic=UNIT):
    """A generator that picks one (text, correct, wrong, why) item from a bank."""
    def generate(level=LEVEL):
        return explain(qtype, *random.choice(bank), notes=notes, topic=topic)
    return generate
