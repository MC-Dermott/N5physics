import random

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from core.models.question_model import PhysicsQuestion

G = 9.8

_NOTES = """
## Graphs of Motion

**Definitions:**
- Velocity is the speed of an object in a given direction (displacement per unit of time).
- Acceleration is the change in velocity per second.
- Displacement is the distance travelled in a straight line, in a given direction, from the
  starting point.

**Key equation** (constant acceleration):
$$s = ut + \\tfrac{1}{2}at^2$$

| Symbol | Quantity | Unit |
|---|---|---|
| s | Displacement | m |
| u | Initial velocity | m/s |
| a | Acceleration | m/s² |
| t | Time | s |

For motion in a straight line with **constant acceleration**:

- The **gradient** of a velocity–time (v–t) graph gives the **acceleration**.
  A straight-line v–t graph means the acceleration is constant; a horizontal
  v–t graph means the acceleration is zero.
- The **area under** a v–t graph gives the **displacement**.
- For constant acceleration, displacement is found by integrating velocity, so a
  displacement–time (s–t) graph is a **curve** (part of a parabola) wherever
  the acceleration is non-zero, and a straight line only where the velocity is constant.
- Because the acceleration is constant within each stage of the motion, the
  acceleration–time (a–t) graph is a **horizontal line** — it only jumps to a new
  horizontal level where the v–t graph's gradient changes.
- The **sign** of the acceleration matches the **sign of the gradient** of the
  v–t graph.

**Worked Example:** A v–t graph rises in a straight line from 0 to 8 m/s over the first 4 s, then
stays constant at 8 m/s for the next 3 s.
- Acceleration in the first 4 s = gradient = $\\frac{8 - 0}{4} = 2\\ \\mathrm{m/s^2}$
- Displacement in the first 4 s = area under the graph (triangle) = $\\frac{1}{2} \\times 4 \\times 8 = 16\\ \\mathrm{m}$
- Acceleration during the constant-speed phase = 0 m/s² (horizontal line)

> **Common exam trap:** don't assume the s–t and a–t graphs look like copies of the
> v–t graph. Only the *gradient* (→ a–t) and *area* (→ s–t) relationships matter —
> always check whether the shape should be straight or curved, and check the sign.
"""

_AXIS_COLOR = "#555"
_GRID_COLOR = "rgba(0,0,0,0.15)"
_V_COLOR = "#1f77b4"
_S_COLOR = "#1f77b4"
_A_COLOR = "#d62728"


# ── Kinematics helpers ───────────────────────────────────────────────────────

def _linspace(a, b, n):
    if n <= 1:
        return [a]
    step = (b - a) / (n - 1)
    return [a + step * i for i in range(n)]


def _integrate(segments, s0=0.0):
    """Add analytic acceleration + start/end displacement to each v–t segment."""
    s = s0
    out = []
    for seg in segments:
        t0, t1, v0, v1 = seg["t0"], seg["t1"], seg["v0"], seg["v1"]
        dt = t1 - t0
        a = (v1 - v0) / dt if dt else 0.0
        s1 = s + v0 * dt + 0.5 * a * dt * dt
        out.append({**seg, "a": a, "s0": s, "s1": s1})
        s = s1
    return out


def _sample_v(segs):
    xs, ys = [segs[0]["t0"]], [segs[0]["v0"]]
    for seg in segs:
        xs.append(seg["t1"])
        ys.append(seg["v1"])
    return xs, ys


def _sample_s(segs, n_per_seg=30):
    xs, ys = [], []
    for seg in segs:
        for t in _linspace(seg["t0"], seg["t1"], n_per_seg):
            dt = t - seg["t0"]
            xs.append(t)
            ys.append(seg["s0"] + seg["v0"] * dt + 0.5 * seg["a"] * dt * dt)
    return xs, ys


def _sample_a_step(segs):
    xs, ys = [], []
    for seg in segs:
        xs += [seg["t0"], seg["t1"], None]
        ys += [seg["a"], seg["a"], None]
    return xs, ys


def _sample_v_shape(segs):
    """The raw (t, v) piecewise-linear shape — reused as a wrong 'copy the v–t shape' trace."""
    xs, ys = [segs[0]["t0"]], [segs[0]["v0"]]
    for seg in segs:
        xs.append(seg["t1"])
        ys.append(seg["v1"])
    return xs, ys


def _mirror_curve(xy):
    """Vertically mirror a sampled curve about the chord joining its first and last points."""
    xs, ys = xy
    x0, y0 = xs[0], ys[0]
    x1, y1 = xs[-1], ys[-1]
    if x1 == x0:
        return xs, ys
    out = []
    for x, y in zip(xs, ys):
        chord_y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        out.append(2 * chord_y - y)
    return xs, out


def _scaled_sloped_mimic(segs):
    """Rescaled v(t) shape used as a wrong, sloped 'acceleration' trace (instead of a constant line)."""
    vxs, vys = _sample_v_shape(segs)
    peak_v = max((abs(v) for v in vys), default=1) or 1
    peak_a = max((abs(seg["a"]) for seg in segs), default=G) or G
    scale = peak_a / peak_v
    return vxs, [v * scale for v in vys]


def _flip_a(segs):
    xs, ys = [], []
    for seg in segs:
        xs += [seg["t0"], seg["t1"], None]
        ys += [-seg["a"], -seg["a"], None]
    return xs, ys


# ── Scenarios (all constant-acceleration, piecewise-linear v–t graphs) ───────

def _scenario_thrown_up():
    u = random.choice([8, 10, 12, 14, 16, 18, 20])
    T = 2 * u / G
    segs = [{"t0": 0.0, "t1": T, "v0": float(u), "v1": float(-u)}]
    desc = (
        f"A ball is thrown vertically upwards with an initial speed of {u} m/s. "
        f"It rises, momentarily comes to rest, and falls back down to be caught at "
        f"the same height {T:.2f} s later. (Take upwards as positive; ignore air "
        f"resistance; g = 9.8 m/s².)"
    )
    return segs, desc


def _scenario_dropped():
    T = random.choice([1.0, 1.5, 2.0, 2.5])
    segs = [{"t0": 0.0, "t1": T, "v0": 0.0, "v1": -G * T}]
    desc = (
        f"A ball is released from rest and falls vertically, hitting the ground "
        f"{T:.2f} s later. (Take upwards as positive; ignore air resistance; "
        f"g = 9.8 m/s².)"
    )
    return segs, desc


def _scenario_uniform_accel():
    v_max = random.choice([10, 12, 15, 18, 20])
    T = random.choice([4, 5, 6, 8])
    segs = [{"t0": 0.0, "t1": float(T), "v0": 0.0, "v1": float(v_max)}]
    desc = f"A car accelerates uniformly from rest, reaching {v_max} m/s after {T} s."
    return segs, desc


def _scenario_uniform_decel():
    v0 = random.choice([10, 12, 15, 18, 20])
    T = random.choice([4, 5, 6, 8])
    segs = [{"t0": 0.0, "t1": float(T), "v0": float(v0), "v1": 0.0}]
    desc = f"A car travelling at {v0} m/s brakes uniformly, coming to rest after {T} s."
    return segs, desc


def _scenario_accel_then_constant():
    v1 = random.choice([8, 10, 12, 15])
    T1 = random.choice([3, 4, 5])
    T2 = random.choice([3, 4, 5])
    segs = [
        {"t0": 0.0, "t1": float(T1), "v0": 0.0, "v1": float(v1)},
        {"t0": float(T1), "t1": float(T1 + T2), "v0": float(v1), "v1": float(v1)},
    ]
    desc = (
        f"A cyclist accelerates uniformly from rest to {v1} m/s over {T1} s, "
        f"then travels at this constant speed for a further {T2} s."
    )
    return segs, desc


def _scenario_constant_then_decel():
    v0 = random.choice([8, 10, 12, 15])
    T1 = random.choice([3, 4, 5])
    T2 = random.choice([3, 4, 5])
    segs = [
        {"t0": 0.0, "t1": float(T1), "v0": float(v0), "v1": float(v0)},
        {"t0": float(T1), "t1": float(T1 + T2), "v0": float(v0), "v1": 0.0},
    ]
    desc = (
        f"A train travels at a constant {v0} m/s for {T1} s, then the brakes are "
        f"applied, bringing it uniformly to rest over a further {T2} s."
    )
    return segs, desc


# Thrown-vertically-up and dropped-vertically are the most commonly occurring examples.
_SCENARIOS = [
    (_scenario_thrown_up, 3),
    (_scenario_dropped, 3),
    (_scenario_uniform_accel, 1),
    (_scenario_uniform_decel, 1),
    (_scenario_accel_then_constant, 1),
    (_scenario_constant_then_decel, 1),
]

_MISTAKE_TEXT = {
    "wrong_s_shape": (
        "The displacement–time graph shouldn't be a straight line here. Since the "
        "velocity is changing at a constant rate, displacement (the area under the "
        "v–t graph) builds up according to s = ut + ½at² — a curve, not a straight "
        "line copying the shape of the v–t graph."
    ),
    "wrong_a_shape": (
        "Because the v–t graph is made of straight-line segments, the acceleration "
        "is constant within each stage. The acceleration–time graph should be a "
        "horizontal line (stepping to a new horizontal level when the v–t gradient "
        "changes) — not a sloped line."
    ),
    "wrong_s_curvature": (
        "The displacement–time graph curves the wrong way. The direction a s–t graph "
        "bends is set by the sign of the acceleration — check whether the v–t "
        "graph's gradient is positive or negative."
    ),
    "wrong_a_sign": (
        "The size of the acceleration is right, but the sign is wrong. The gradient "
        "of the v–t graph gives the acceleration including its sign — check whether "
        "the v–t line slopes upwards or downwards."
    ),
}


# ── Plotting ──────────────────────────────────────────────────────────────────

def _style_axes(fig, row=None, col=None, xtitle=None, ytitle=None):
    kwargs = dict(row=row, col=col) if row is not None else {}
    fig.update_xaxes(title_text=xtitle, zeroline=True, zerolinecolor=_AXIS_COLOR,
                      gridcolor=_GRID_COLOR, linecolor=_AXIS_COLOR, **kwargs)
    fig.update_yaxes(title_text=ytitle, zeroline=True, zerolinecolor=_AXIS_COLOR,
                      gridcolor=_GRID_COLOR, linecolor=_AXIS_COLOR, **kwargs)


def _base_layout(fig, height):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=45, r=15, t=25, b=35),
        height=height,
        showlegend=False,
        font=dict(size=11),
    )


def _main_vt_figure(segs_raw):
    xs, ys = _sample_v(segs_raw)
    fig = go.Figure(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=_V_COLOR, width=3)))
    _style_axes(fig, xtitle="Time (s)", ytitle="Velocity (m/s)")
    _base_layout(fig, height=320)
    return fig


def _option_figure(s_xy, a_xy, y_ranges):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Displacement–time", "Acceleration–time"),
        vertical_spacing=0.22,
    )
    fig.add_trace(go.Scatter(x=s_xy[0], y=s_xy[1], mode="lines",
                              line=dict(color=_S_COLOR, width=2.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=a_xy[0], y=a_xy[1], mode="lines",
                              line=dict(color=_A_COLOR, width=2.5)), row=2, col=1)
    _style_axes(fig, row=1, col=1, ytitle="s (m)")
    _style_axes(fig, row=2, col=1, xtitle="Time (s)", ytitle="a (m/s²)")
    fig.update_yaxes(range=y_ranges["s"], row=1, col=1)
    fig.update_yaxes(range=y_ranges["a"], row=2, col=1)
    _base_layout(fig, height=300)
    fig.update_annotations(font_size=11)
    return fig


def _padded_range(values, pad_frac=0.15, min_pad=0.5):
    lo, hi = min(values), max(values)
    pad = max((hi - lo) * pad_frac, min_pad)
    return [lo - pad, hi + pad]


def _build_combos(segs_raw):
    segs = _integrate(segs_raw)

    s_correct = _sample_s(segs)
    a_correct = _sample_a_step(segs)

    s_wrong_shape = _sample_v_shape(segs)          # straight-line mimic of v(t)
    s_wrong_curvature = _mirror_curve(s_correct)    # correct shape, wrong concavity

    a_wrong_shape = _scaled_sloped_mimic(segs)      # sloped mimic of v(t)
    a_wrong_sign = _flip_a(segs)                    # correct magnitude, wrong sign

    combos = [
        ("correct", s_correct, a_correct),
        ("wrong_s_shape", s_wrong_shape, a_correct),
        ("wrong_a_shape", s_correct, a_wrong_shape),
        ("wrong_s_curvature", s_wrong_curvature, a_correct),
        ("wrong_a_sign", s_correct, a_wrong_sign),
    ]

    all_s_vals = [y for _, s, _ in combos for y in s[1] if y is not None]
    all_a_vals = [y for _, _, a in combos for y in a[1] if y is not None]
    y_ranges = {"s": _padded_range(all_s_vals), "a": _padded_range(all_a_vals)}

    return combos, y_ranges


# ── Public entry point ────────────────────────────────────────────────────────

def generate_graphs_of_motion(level="Higher"):
    scenario_fn = random.choices(
        [fn for fn, _ in _SCENARIOS], weights=[w for _, w in _SCENARIOS], k=1
    )[0]
    segs_raw, desc = scenario_fn()

    combos, y_ranges = _build_combos(segs_raw)
    random.shuffle(combos)

    labels = ["A", "B", "C", "D", "E"]
    option_figures = {}
    label_tag = {}
    correct_label = None
    for label, (tag, s_xy, a_xy) in zip(labels, combos):
        option_figures[label] = _option_figure(s_xy, a_xy, y_ranges)
        label_tag[label] = tag
        if tag == "correct":
            correct_label = label

    main_fig = _main_vt_figure(segs_raw)

    working = [
        {"type": "text", "content": desc},
        {"type": "text", "content": "Gradient of a v–t graph = acceleration; area under a v–t graph = displacement."},
        {"type": "text", "content": "The v–t graph is made of straight-line segments, so the acceleration is "
                                     "constant within each segment — the a–t graph is a horizontal line, stepping "
                                     "to a new level only where the v–t gradient changes."},
        {"type": "text", "content": "Integrating a constant acceleration gives s = ut + ½at², so the s–t graph "
                                     "is a curve (part of a parabola) wherever the acceleration is non-zero."},
        {"type": "text", "content": f"Option {correct_label} is the only one that pairs a correctly curved (or "
                                     f"straight, where appropriate) displacement–time graph with a correctly "
                                     f"constant, correctly signed acceleration–time graph."},
    ]

    distractors = [
        {"value": label, "mistake": _MISTAKE_TEXT[tag], "working": working}
        for label, tag in label_tag.items() if tag != "correct"
    ]

    question_text = (
        f"{desc}\n\nThe velocity–time graph for this motion is shown below. Which combination of "
        f"graphs (A–E) correctly shows the displacement–time and acceleration–time graphs for this motion?"
    )

    return PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct_label,
        unit="",
        distractors=distractors,
        working=working,
        notes=_NOTES,
        topic="Our Dynamic Universe",
        question_type="Graphs of Motion",
        level=level,
        metadata={
            "type": "graph_mcq",
            "main_figure": main_fig,
            "options": labels,
            "option_figures": option_figures,
        },
    )


# ── Numeric velocities from an acceleration–time graph ───────────────────────

from utils.make_question import make_question

_AT_CONTEXTS = [
    "A cyclist", "A car", "A train", "A tractor", "A go-kart",
]


def _at_ctx():
    return random.choice(_AT_CONTEXTS)


def _dedup_at_options(options_data, correct):
    """Remove distractor entries whose value equals the correct answer or another distractor."""
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


def gen_at_final_velocity(level="Higher"):
    obj = _at_ctx()
    u = random.randint(2, 15)
    a = random.choice([-3, -2.5, -2, -1.5, 1.5, 2, 2.5, 3])
    t = random.choice([2, 3, 4, 5, 6, 8])
    v = round(u + a * t, 2)
    while v <= 0:
        u = random.randint(2, 15)
        t = random.choice([2, 3, 4, 5, 6, 8])
        v = round(u + a * t, 2)

    accel_word = "a constant deceleration" if a < 0 else "a constant acceleration"
    question = (
        f"{obj} has an initial velocity of {u} m/s. An acceleration–time graph shows "
        f"{accel_word} of {abs(a)} m/s² for {t} s. Calculate the final velocity."
    )
    working = [
        {"type": "text",  "content": "The change in velocity equals the area under the a-t graph:"},
        {"type": "latex", "content": r"\Delta v = a \times t"},
        {"type": "latex", "content": rf"\Delta v = ({a}) \times {t} = {round(a*t, 2)}\ \mathrm{{m/s}}"},
        {"type": "latex", "content": r"v = u + \Delta v"},
        {"type": "latex", "content": rf"v = {u} + ({round(a*t,2)}) = {v}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v, "mistake": None, "working": working},
        {"value": round(u - a * t, 2),
         "mistake": "Check the sign of the acceleration — a deceleration reduces velocity, an acceleration increases it.",
         "working": working},
        {"value": round(a * t, 2),
         "mistake": "You forgot to add the initial velocity u. v = u + (a × t).",
         "working": working},
        {"value": round(u + a, 2),
         "mistake": "You need the *area* under the a-t graph (a × t), not just a on its own.",
         "working": working},
    ]
    options_data = _dedup_at_options(options_data, v)
    scaffold = [
        {"question": "What is the change in velocity, Δv (= a × t)?", "answer": round(a * t, 2)},
        {"question": "What is the final velocity v?", "answer": v},
    ]
    return make_question(question, v, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Graphs of Motion", level=level, scaffold=scaffold)


def gen_at_initial_velocity(level="Higher"):
    obj = _at_ctx()
    v = random.randint(10, 25)
    a = random.choice([-3, -2.5, -2, -1.5, 1.5, 2, 2.5, 3])
    t = random.choice([2, 3, 4, 5, 6, 8])
    u = round(v - a * t, 2)
    while u <= 0:
        v = random.randint(10, 25)
        t = random.choice([2, 3, 4, 5, 6, 8])
        u = round(v - a * t, 2)

    accel_word = "a constant deceleration" if a < 0 else "a constant acceleration"
    question = (
        f"{obj} undergoes {accel_word} of {abs(a)} m/s² for {t} s, shown on an "
        f"acceleration–time graph, finishing with a velocity of {v} m/s. "
        f"Calculate its initial velocity."
    )
    working = [
        {"type": "text",  "content": "The change in velocity equals the area under the a-t graph:"},
        {"type": "latex", "content": r"\Delta v = a \times t"},
        {"type": "latex", "content": rf"\Delta v = ({a}) \times {t} = {round(a*t, 2)}\ \mathrm{{m/s}}"},
        {"type": "latex", "content": r"u = v - \Delta v"},
        {"type": "latex", "content": rf"u = {v} - ({round(a*t,2)}) = {u}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": u, "mistake": None, "working": working},
        {"value": round(v + a * t, 2),
         "mistake": "Check the sign — you need to subtract the change in velocity from v to get back to u, not add it.",
         "working": working},
        {"value": round(v - a, 2),
         "mistake": "You need the *area* under the a-t graph (a × t), not just a on its own.",
         "working": working},
        {"value": v,
         "mistake": "This is the final velocity — the initial velocity must be different since the object accelerated.",
         "working": working},
    ]
    options_data = _dedup_at_options(options_data, u)
    scaffold = [
        {"question": "What is the change in velocity, Δv (= a × t)?", "answer": round(a * t, 2)},
        {"question": "What is the initial velocity u?", "answer": u},
    ]
    return make_question(question, u, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Graphs of Motion", level=level, scaffold=scaffold)


def gen_at_two_stage_velocity(level="Higher"):
    obj = _at_ctx()
    u = random.randint(0, 6)
    a1 = random.choice([1, 1.5, 2])
    t1 = random.choice([2, 3, 4])
    a2 = random.choice([2, 2.5, 3, 3.5, 4])
    t2 = random.choice([2, 3, 4, 5])
    v_mid = round(u + a1 * t1, 2)
    v_final = round(v_mid + a2 * t2, 2)

    stage1_desc = f"shows a constant {a1} m/s² for the first {t1} s"
    question = (
        f"{obj} starts with a velocity of {u} m/s. An acceleration–time graph "
        f"{stage1_desc}, then steps up to a constant {a2} m/s² for a further {t2} s. "
        f"Calculate the velocity at the end of the {t1 + t2} s shown."
    )
    working = [
        {"type": "text",  "content": "Find the change in velocity from each stage of the a-t graph (its area), and add them in turn:"},
        {"type": "latex", "content": rf"\Delta v_1 = a_1 t_1 = {a1} \times {t1} = {round(a1*t1,2)}\ \mathrm{{m/s}}"},
        {"type": "latex", "content": rf"v_{{\text{{mid}}}} = u + \Delta v_1 = {u} + {round(a1*t1,2)} = {v_mid}\ \mathrm{{m/s}}"},
        {"type": "latex", "content": rf"\Delta v_2 = a_2 t_2 = {a2} \times {t2} = {round(a2*t2,2)}\ \mathrm{{m/s}}"},
        {"type": "latex", "content": rf"v = v_{{\text{{mid}}}} + \Delta v_2 = {v_mid} + {round(a2*t2,2)} = {v_final}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v_final, "mistake": None, "working": working},
        {"value": round(u + a2 * t2, 2),
         "mistake": f"You left out the change in velocity during the first stage. Even though the acceleration "
                    f"there is {a1} m/s², it still lasts {t1} s and contributes {round(a1*t1,2)} m/s.",
         "working": working},
        {"value": round(u + a1 * (t1 + t2), 2),
         "mistake": f"You applied the first stage's acceleration ({a1} m/s²) for the whole {t1+t2} s instead "
                    f"of only the first {t1} s.",
         "working": working},
        {"value": round(v_mid, 2),
         "mistake": f"This is the velocity at the end of the first stage only ({t1} s), not the full "
                    f"{t1 + t2} s shown on the graph.",
         "working": working},
    ]
    options_data = _dedup_at_options(options_data, v_final)
    scaffold = [
        {"question": "What is the velocity at the end of the first stage, v_mid?", "answer": v_mid},
        {"question": "What is the final velocity v?", "answer": v_final},
    ]
    return make_question(question, v_final, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Graphs of Motion", level=level, scaffold=scaffold)


_ALL_AT_GRAPH_GENS = [
    gen_at_final_velocity,
    gen_at_initial_velocity,
    gen_at_two_stage_velocity,
]


def generate_at_graph_velocity(level="Higher"):
    return random.choice(_ALL_AT_GRAPH_GENS)(level=level)
