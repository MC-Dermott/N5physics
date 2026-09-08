import math
import random
import plotly.graph_objects as go
from utils.make_question import make_question
from core.models.question_model import PhysicsQuestion
from utils.notes import NOTES

_CONTEXTS = ["trolley", "cyclist", "car", "runner", "go-kart", "toy car"]

_LINE_COLOR = "#1f4e8c"
_AXIS_COLOR = "#555555"
_GRID_COLOR = "rgba(0,0,0,0.12)"
_POINT_COLOR = "#c0392b"
_COMPARE_COLORS = ["#1f4e8c", "#c0392b", "#2e8b57"]


def _dedup(options_data, correct):
    seen = {round(float(correct), 4)}
    cleaned = []
    for opt in options_data:
        key = round(float(opt["value"]), 4)
        if key not in seen:
            seen.add(key)
            cleaned.append(opt)
        elif opt["mistake"] is None:
            cleaned.insert(0, opt)
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


# ── Graph rendering ──────────────────────────────────────────────────────────

def _make_figure(points):
    """points: list of (t, v, label) in order along the line. Straight segments
    between consecutive points, red dots + grey labels at each vertex."""
    ts = [p[0] for p in points]
    vs = [p[1] for p in points]

    fig = go.Figure(go.Scatter(
        x=ts, y=vs, mode="lines", line=dict(color=_LINE_COLOR, width=3),
    ))
    fig.add_trace(go.Scatter(
        x=ts, y=vs, mode="markers+text",
        text=[label for _, _, label in points],
        textposition="top center",
        textfont=dict(size=14, color=_AXIS_COLOR),
        marker=dict(color=_POINT_COLOR, size=9),
        showlegend=False,
    ))

    t_max = max(ts) * 1.15 if max(ts) > 0 else 1
    v_max = max(vs) * 1.25 if max(vs) > 0 else 1
    fig.update_xaxes(title_text="Time (s)", range=[0, t_max], zeroline=True,
                     zerolinecolor=_AXIS_COLOR, gridcolor=_GRID_COLOR, linecolor=_AXIS_COLOR)
    fig.update_yaxes(title_text="Speed (m/s)", range=[0, v_max], zeroline=True,
                     zerolinecolor=_AXIS_COLOR, gridcolor=_GRID_COLOR, linecolor=_AXIS_COLOR)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=45, r=15, t=25, b=35), height=320, showlegend=False,
        font=dict(size=11),
    )
    return fig


def _compare_figure(lines):
    """lines: list of (t_end, v_end, label, color), all sharing a common start
    point (0, v_start). No axis tick numbers — this question tests reading
    steepness by eye, not by value, matching the worksheet's own graphs."""
    fig = go.Figure()
    for t_end, v_start, v_end, label, color in lines:
        fig.add_trace(go.Scatter(
            x=[0, t_end], y=[v_start, v_end], mode="lines",
            line=dict(color=color, width=3), showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=[t_end], y=[v_end], mode="markers+text", text=[label],
            textposition="middle right", textfont=dict(size=15, color=color),
            marker=dict(color=color, size=7), showlegend=False,
        ))

    all_t = [0] + [l[0] for l in lines]
    all_v = [l[1] for l in lines] + [l[2] for l in lines]
    fig.update_xaxes(title_text="Time", range=[0, max(all_t) * 1.25], showticklabels=False,
                     zeroline=True, zerolinecolor=_AXIS_COLOR, linecolor=_AXIS_COLOR)
    fig.update_yaxes(title_text="Speed", range=[0, max(all_v) * 1.15], showticklabels=False,
                     zeroline=True, zerolinecolor=_AXIS_COLOR, linecolor=_AXIS_COLOR)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=35, r=35, t=25, b=35), height=300, showlegend=False,
        font=dict(size=11),
    )
    return fig


def _with_graph(question, points):
    question.metadata["main_figure"] = _make_figure(points)
    return question


# ── Section A — comparing acceleration from steepness (qualitative) ─────────

def gen_accel_graph_compare(level="S3"):
    labels = ["A", "B", "C"]
    direction = random.choice(["up", "down"])
    accels = random.sample([1, 2, 3, 4, 5, 6], 3)
    colors = random.sample(_COMPARE_COLORS, 3)
    order = list(range(3))
    random.shuffle(order)
    accels = [accels[i] for i in order]

    T = random.choice([5, 6, 7])
    lines = []
    if direction == "up":
        v_start = 0
        for accel, label, color in zip(accels, labels, colors):
            v_end = accel * T
            lines.append((T, v_start, v_end, label, color))
        best_idx = accels.index(max(accels))
        desc = "speeding up"
        steep_word = "rises the most steeply"
    else:
        v_start = max(accels) * T
        for accel, label, color in zip(accels, labels, colors):
            t_end = round(v_start / accel, 2)
            lines.append((t_end, v_start, 0, label, color))
        best_idx = accels.index(max(accels))
        desc = "slowing down"
        steep_word = "falls the most steeply (reaches zero speed soonest)"

    correct_label = labels[best_idx]

    working = [
        {"type": "text", "content": f"The steeper the line, the greater the size of the "
                                     f"acceleration — the line for {correct_label} {steep_word}."},
    ]
    distractors = []
    for label in labels:
        if label == correct_label:
            continue
        distractors.append({
            "value": label,
            "mistake": f"Object {label}'s line is less steep than {correct_label}'s — a gentler "
                       f"gradient means a smaller change in speed each second, so a smaller "
                       f"acceleration.",
            "working": working,
        })

    question_text = (
        f"The speed-time graphs for three objects, {labels[0]}, {labels[1]} and {labels[2]}, are "
        f"shown below, all {desc}.\n\nWhich object has the greatest acceleration?"
    )

    part = PhysicsQuestion(
        question_text=question_text, correct_answer=correct_label, unit="",
        topic="Dynamics", question_type="V-T Graphs", level=level,
        distractors=distractors, working=working,
        metadata={"type": "classification", "options": labels,
                  "main_figure": _compare_figure(lines)},
        notes=NOTES["vt_graph_acceleration_s3"],
    )
    return part


# ── Section B — calculating acceleration from a simple two-point graph ──────

def gen_accel_graph_basic(level="S3"):
    ctx = random.choice(_CONTEXTS)
    t = random.choice([4, 5, 6, 7, 8])
    accel_true = random.choice([2, 2.5, 3, 3.5, 4, 5, -2, -2.5, -3, -3.5, -4, -5])
    if accel_true >= 0:
        u = random.choice([0, 0, 0, 2, 4, 6])
    else:
        u = random.randint(math.ceil(abs(accel_true) * t), math.ceil(abs(accel_true) * t) + 15)
    v = round(u + accel_true * t, 2)
    delta_v = round(v - u, 2)
    correct = round(delta_v / t, 2)

    points = [(0, u, "A"), (t, v, "B")]
    working = [
        {"type": "text", "content": f"Points: A(0, {u}), B({t}, {v})"},
        {"type": "latex", "content": r"a = \frac{\Delta v}{t} = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"a = \frac{{{v} - {u}}}{{{t}}}"},
        {"type": "latex", "content": rf"a = {correct}\ \mathrm{{m/s^2}}"},
    ]
    question = (
        f"The speed-time graph below shows a {ctx}'s motion between point A and point B.\n\n"
        f"Calculate the acceleration between A and B."
    )
    distractors = [
        {"value": -correct,
         "mistake": "You calculated (u − v) ÷ t instead of (v − u) ÷ t — check which point comes "
                    "first on the graph.",
         "working": working},
        {"value": delta_v,
         "mistake": "That's the change in speed (Δv), not the acceleration — you still need to "
                    "divide by the time, t.",
         "working": working},
        {"value": round(v / t, 2) if t else 0,
         "mistake": "Use a = (v − u) ÷ t — divide the *change* in speed by time, not the final "
                    "speed alone.",
         "working": working},
    ]
    options_data = [{"value": correct, "mistake": None, "working": working}] + distractors
    options_data = _dedup(options_data, correct)
    scaffold = [
        {"question": "What is the change in speed (Δv = v − u) between A and B, read from the graph?",
         "answer": float(delta_v)},
    ]
    q = make_question(question, correct, options_data, "m/s²", scaffold=scaffold,
                      notes=NOTES["vt_graph_acceleration_s3"], topic="Dynamics",
                      question_type="V-T Graphs", level=level)
    return _with_graph(q, points)


# ── Section C — compound (multi-segment) graphs ──────────────────────────────

def gen_accel_graph_compound(level="S3"):
    ctx = random.choice(_CONTEXTS)
    pattern = random.choice(["up_flat_down", "down_flat_up"])

    t1 = random.choice([3, 4, 5])
    flat_dur = random.choice([3, 4, 5])
    t2 = t1 + flat_dur
    t3_dur = random.choice([3, 4, 5])
    t3 = t2 + t3_dur
    v_peak = random.choice([12, 15, 16, 18, 20])

    if pattern == "up_flat_down":
        points = [(0, 0, "A"), (t1, v_peak, "B"), (t2, v_peak, "C"), (t3, 0, "D")]
        desc = "speeding up, travelling at a constant speed, and then slowing down"
    else:
        points = [(0, v_peak, "A"), (t1, 0, "B"), (t2, 0, "C"), (t3, v_peak, "D")]
        desc = "slowing down to a stop, remaining stationary, and then speeding up again"

    segment_labels = ["A to B", "B to C", "C to D"]
    seg_idx = random.randrange(3)
    (t0, v0, l0), (t1_, v1_, l1_) = points[seg_idx], points[seg_idx + 1]
    delta_v = round(v1_ - v0, 2)
    duration = t1_ - t0
    correct = round(delta_v / duration, 2)

    points_desc = ", ".join(f"{lbl}({t}, {v})" for t, v, lbl in points)
    working = [
        {"type": "text", "content": f"Points: {points_desc}"},
        {"type": "latex", "content": r"a = \frac{\Delta v}{t} = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"a = \frac{{{v1_} - {v0}}}{{{duration}}}"},
        {"type": "latex", "content": rf"a = {correct}\ \mathrm{{m/s^2}}"},
    ]
    question = (
        f"The speed-time graph below shows a {ctx} {desc}.\n\n"
        f"Calculate the acceleration for section {segment_labels[seg_idx]} of the graph."
    )

    other_segments = [i for i in range(3) if i != seg_idx]
    distractors = []
    for i in other_segments:
        (ot0, ov0, _), (ot1, ov1, _) = points[i], points[i + 1]
        wrong = round((ov1 - ov0) / (ot1 - ot0), 2)
        distractors.append({
            "value": wrong,
            "mistake": f"That's the acceleration for section {segment_labels[i]}, not "
                       f"{segment_labels[seg_idx]} — make sure you're reading the right two points "
                       f"off the graph.",
            "working": working,
        })
    distractors.append({
        "value": round(delta_v / t3, 2),
        "mistake": f"You divided by the total time (0 to {t3} s) instead of just the time for "
                   f"this section ({duration} s).",
        "working": working,
    })

    options_data = [{"value": correct, "mistake": None, "working": working}] + distractors
    options_data = _dedup(options_data, correct)
    scaffold = [
        {"question": f"What is the change in speed (Δv) for section {segment_labels[seg_idx]}?",
         "answer": float(delta_v)},
    ]
    q = make_question(question, correct, options_data, "m/s²", scaffold=scaffold,
                      notes=NOTES["vt_graph_acceleration_s3"], topic="Dynamics",
                      question_type="V-T Graphs", level=level)
    return _with_graph(q, points)


def generate_vt_graph_acceleration(level="S3"):
    return random.choice(
        [gen_accel_graph_compare, gen_accel_graph_basic, gen_accel_graph_compound]
    )(level=level)
