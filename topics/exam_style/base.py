"""Shared builder for exam-style questions — multi-part scenarios in the style of SQA papers.

Like real exam questions, a scenario sets up one context (a car journey, a circuit, a tracer…) and
asks linked parts that cut across the unit's topics, usually building from one calculation to the
next, with state/explain parts asked as multiple choice so that they are marked automatically.
Each part is tagged with the topic it tests, so tests and unit assessments can report by topic.

    def _car(level="N5"):
        ex = Exam("Dynamics", level, NOTES)
        ex.on("Acceleration").num("Calculate the acceleration of the car.", a, "m/s²",
                                  wrong=[(v / t, "Use the CHANGE in speed: v − u.")],
                                  working=[r"a = \\frac{v - u}{t}", ...])
        ex.on("Forces").choice("Why ...?", "Because ...", [("Wrong reason", "Why it's wrong")])
        return ex.build("A car accelerates from rest ...")

    SCENARIOS = {"Car Journey": _car, ...}
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
    """Collects the parts of one exam-style scenario. Call .on(topic) before each part (or run
    of parts) to tag it with the topic it tests."""

    def __init__(self, unit, level, notes=None):
        self.unit, self.level, self.notes = unit, level, notes or {}
        self.topic = None
        self.parts = []

    def on(self, topic):
        self.topic = topic
        return self

    def _part_fields(self):
        assert self.topic, "call .on(topic) before adding a part"
        return dict(topic=self.unit, question_type=self.topic, level=self.level)

    def num(self, text, answer, unit, wrong=(), working=(), scaffold=(), sf=3):
        """A calculation part. wrong: (value, mistake) pairs — values that come from a common
        mistake, recognised when a student enters them. scaffold: (prompt, answer, unit) steps."""
        answer = sig(answer, sf)
        work = _steps(working)
        opts = [{"value": answer, "mistake": None, "working": work}]
        for value, mistake in wrong:
            v = sig(value, sf)
            if not math.isfinite(v) or any(math.isclose(v, o["value"], rel_tol=0.03) for o in opts):
                continue
            opts.append({"value": v, "mistake": mistake, "working": work,
                         "display": f"{fmt(v)} {unit}".strip()})
        steps = [{"question": p, "answer": sig(a, sf), "unit": u} for p, a, u in scaffold]
        fields = self._part_fields()
        q = make_question(text, answer, opts, unit, scaffold=steps, notes=self.notes.get(self.topic, ""),
                          topic=fields["topic"], question_type=fields["question_type"], level=self.level)
        self.parts.append(q)
        return q

    def choice(self, text, correct, wrong, working=()):
        """A multiple-choice part (state / explain / describe). wrong: (option, why) pairs."""
        work = _steps(working)
        options = [correct] + [w for w, _ in wrong]
        random.shuffle(options)
        q = PhysicsQuestion(
            question_text=text, correct_answer=correct, unit="", notes=self.notes.get(self.topic, ""),
            working=work, distractors=[{"value": w, "mistake": why, "working": work} for w, why in wrong],
            metadata={"type": "classification", "options": options}, **self._part_fields(),
        )
        self.parts.append(q)
        return q

    def build(self, context, figure=None, diagram=None):
        for part in self.parts:
            # lets a test's review show each part under the scenario it came from
            part.metadata["scenario_context"] = context
            if diagram:
                part.metadata["scenario_diagram"] = diagram
        covers = list(dict.fromkeys(p.question_type for p in self.parts))
        metadata = {"exam_style": True, "covers": covers}
        if figure is not None:
            metadata["main_figure"] = figure
        if diagram:
            metadata["diagram"] = diagram
        return PhysicsQuestion(
            question_text=context.split("\n\n")[0], correct_answer=0.0, unit="",
            topic=self.unit, question_type=EXAM_STYLE, level=self.level,
            is_scenario=True, scenario_context=context, parts=self.parts, metadata=metadata,
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


