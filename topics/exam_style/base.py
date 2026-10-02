"""Shared builder for exam-style questions — multi-part scenarios in the style of SQA papers.

Each scenario sets up one context (a car, a circuit, a source…) and asks two to four parts on it,
usually building from one calculation to the next and ending with an explain/state part, which is
asked as multiple choice so that it is marked automatically. Every part keeps the topic's name as
its question_type, so tests and unit assessments report results against the topic.

    def _car(level="N5"):
        ex = Exam("Dynamics", "Acceleration", level, NOTES)
        ex.num("Calculate the acceleration of the car.", a, "m/s²",
               wrong=[(v / t, "Use the CHANGE in speed: v − u.")],
               working=[r"a = \\frac{v - u}{t}", ...])
        ex.choice("Why ...?", "Because ...", [("Wrong reason", "Why it's wrong")])
        return ex.build("A car accelerates from rest ...")

    gen_acceleration_exam = exam_style(_car, _bike, _rocket)
"""
import math
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

EXAM_STYLE = "Exam Style"

_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sig(x, sf=3):
    """x rounded to sf significant figures."""
    if x == 0:
        return 0.0
    return float(f"{x:.{sf}g}")


def fmt(x, sf=3):
    """x to sf significant figures as plain text, in scientific notation when very large/small."""
    x = sig(x, sf)
    if x == 0 or 0.001 <= abs(x) < 1e6:
        return f"{x:g}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    coeff = coeff.rstrip("0").rstrip(".")
    return f"{coeff} × 10{str(int(exp)).translate(_SUP)}"


def ltx(x, sf=3):
    """x to sf significant figures as LaTeX."""
    x = sig(x, sf)
    if x == 0 or 0.001 <= abs(x) < 1e6:
        return f"{x:g}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    coeff = coeff.rstrip("0").rstrip(".")
    return rf"{coeff} \times 10^{{{int(exp)}}}"


def L(s):
    return {"type": "latex", "content": s}


def T(s):
    return {"type": "text", "content": s}


def pick(*values):
    return random.choice(values)


def _steps(working):
    """Working given as plain strings is LaTeX; dicts pass through."""
    return [w if isinstance(w, dict) else L(w) for w in working]


class Exam:
    """Collects the parts of one exam-style scenario."""

    def __init__(self, topic, qtype, level, notes=""):
        self.topic, self.qtype, self.level, self.notes = topic, qtype, level, notes
        self.parts = []

    def num(self, text, answer, unit, wrong=(), working=(), scaffold=(), sf=3):
        """A calculation part. wrong: (value, mistake) pairs — values that come from a common
        mistake, recognised when a student enters them. scaffold: (prompt, answer, unit) steps."""
        answer = sig(answer, sf)
        work = _steps(working)
        opts = [{"value": answer, "mistake": None, "working": work}]
        for value, mistake in wrong:
            v = sig(value, sf)
            if not math.isfinite(v) or any(
                    math.isclose(v, o["value"], rel_tol=0.03) for o in opts):
                continue
            opts.append({"value": v, "mistake": mistake, "working": work,
                         "display": f"{fmt(v)} {unit}".strip()})
        steps = [{"question": p, "answer": sig(a, sf), "unit": u} for p, a, u in scaffold]
        q = make_question(text, answer, opts, unit, scaffold=steps, notes=self.notes,
                          topic=self.topic, question_type=self.qtype, level=self.level)
        self.parts.append(q)
        return q

    def choice(self, text, correct, wrong, working=()):
        """A multiple-choice part (state / explain / describe). wrong: (option, why) pairs."""
        work = _steps(working)
        options = [correct] + [w for w, _ in wrong]
        random.shuffle(options)
        q = PhysicsQuestion(
            question_text=text, correct_answer=correct, unit="", topic=self.topic,
            question_type=self.qtype, level=self.level, notes=self.notes, working=work,
            distractors=[{"value": w, "mistake": why, "working": work} for w, why in wrong],
            metadata={"type": "classification", "options": options},
        )
        self.parts.append(q)
        return q

    def build(self, context, figure=None):
        for part in self.parts:
            # lets a test's review show each part under the scenario it came from
            part.metadata["scenario_context"] = context
        metadata = {"exam_style": True}
        if figure is not None:
            metadata["main_figure"] = figure
        return PhysicsQuestion(
            question_text=context.split("\n\n")[0], correct_answer=0.0, unit="",
            topic=self.topic, question_type=self.qtype, level=self.level,
            is_scenario=True, scenario_context=context, parts=self.parts,
            metadata=metadata,
        )


def graph(points, xlabel="Time (s)", ylabel="Velocity (m/s)", labels=None, smooth=False):
    """A line graph for a scenario. points: [(x, y)]; labels: optional text per point
    (e.g. "A", "B"); smooth: draw a curve through many points without markers."""
    import plotly.graph_objects as go

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    fig = go.Figure(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#1f4e8c", width=3)))
    if not smooth:
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="markers+text" if labels else "markers",
            text=labels, textposition="top center", textfont=dict(size=14, color="#555555"),
            marker=dict(color="#c0392b", size=8),
        ))
    y_lo = min(0, min(ys) * 1.2)
    y_hi = max(ys) * 1.2 if max(ys) > 0 else 1
    axis = dict(zeroline=True, zerolinecolor="#555555", gridcolor="rgba(0,0,0,0.12)",
                linecolor="#555555")
    fig.update_xaxes(title_text=xlabel, range=[0, max(xs) * 1.08], **axis)
    fig.update_yaxes(title_text=ylabel, range=[y_lo, y_hi], **axis)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=50, r=15, t=25, b=40), height=320, showlegend=False,
                      font=dict(size=11))
    return fig


def exam_style(*builders):
    """A topic's Exam Style generator: one of its scenarios at random. The scenarios are kept
    on .variants so a test can deal each one before repeating any."""
    def generate(level="N5"):
        return random.choice(builders)(level=level)

    generate.variants = builders
    return generate


def mark_exam_style(q):
    """Tags an existing multi-part generator's question as exam style (for reused generators)."""
    q.metadata["exam_style"] = True
    if q.is_scenario:
        for part in q.parts:
            part.metadata.setdefault("scenario_context", q.scenario_context)
    return q


def reuse(gen, qtype=None):
    """Wraps an existing multi-part generator as an exam-style variant."""
    def build(level="N5"):
        q = gen(level=level)
        if qtype:
            q.question_type = qtype
            for part in q.parts:
                if part.metadata.get("type") != "explain":
                    part.question_type = qtype
        return mark_exam_style(q)

    return build
