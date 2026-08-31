import random
import plotly.graph_objects as go
from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

_NOTES = """
## Velocity-Time Graphs

**Key ideas:**
- The **area under** a velocity-time graph gives the **distance** travelled. Where the
  graph goes below the time axis, that section still adds to distance, but subtracts
  from **displacement** (since the object is moving the opposite way).
- The **gradient** of a velocity-time graph gives the **acceleration** — this can be found
  using any two points on the same straight-line section, even if that section doesn't
  start at t = 0.
- A ball moving freely under gravity (thrown or dropped) changes direction *smoothly* —
  its velocity passes gradually through zero. A **bouncing** ball changes direction
  *instantly* at each bounce — the graph jumps straight from a negative to a smaller
  positive velocity, without passing smoothly through zero.

**Worked Example (distance & displacement):** A car accelerates from rest to 8 m/s over
4 s, then brakes and reverses, reaching −4 m/s after a further 4 s.
- Stage 1 (triangle) = ½ × 4 × 8 = 16 m
- Stage 2 crosses zero at t = 6.67 s: forward part ≈ ½ × 2.67 × 8 = 10.7 m; reverse part ≈
  ½ × 1.33 × 4 = 2.7 m
- Distance ≈ 16 + 10.7 + 2.7 = 29.3 m          Displacement ≈ 16 + 10.7 − 2.7 = 24.0 m

**Worked Example (acceleration over an interval):** A graph shows a vehicle's velocity
rising steadily from 0 to 20 m/s over the first 10 s. Between t = 2 s and t = 8 s:
at t = 2 s, v = 4 m/s; at t = 8 s, v = 16 m/s.
$$a = \\frac{16 - 4}{8 - 2} = 2\\ \\mathrm{m/s^2}$$

> **Common exam trap:** distance is the *area*, not a single velocity value read off
> the graph — always check whether the shape under the line is a rectangle, triangle,
> or trapezium, and whether any part of it lies below the time axis.
"""

_CONTEXTS = ["car", "cyclist", "train", "ferry", "tractor", "go-kart", "trolley"]


def _dedup(options_data, correct):
    seen = {round(float(correct), 2)}
    cleaned = []
    for opt in options_data:
        key = round(float(opt["value"]), 2)
        if key not in seen:
            seen.add(key)
            cleaned.append(opt)
        elif opt["mistake"] is None:
            cleaned.insert(0, opt)
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


# ── Which velocity-time graph matches this description? ─────────────────────

_SCENARIOS = {
    "thrown_up_caught": {
        "desc": "A ball is thrown vertically upward and caught again at the same height.",
        "t": [0, 4], "v": [10, -10],
    },
    "dropped_caught": {
        "desc": "A ball is dropped from rest and caught at the ground.",
        "t": [0, 3], "v": [0, 12],
    },
    "bounce_once": {
        "desc": "A ball is dropped, bounces once, and is caught at the top of the bounce.",
        "t": [0, 2, 2, 3], "v": [0, 20, -10, 0],
    },
    "thrown_up_lands_below": {
        "desc": "A ball is thrown vertically upward from a height, and lands below the point it was released from.",
        "t": [0, 3.2], "v": [8, -14],
    },
}


def _scenario_figure(key):
    s = _SCENARIOS[key]
    fig = go.Figure(go.Scatter(x=s["t"], y=s["v"], mode="lines", line=dict(color="#1f4e8c", width=3)))
    ymax = max(max(s["v"]), 1) * 1.3
    ymin = min(min(s["v"]), -1) * 1.3
    fig.update_xaxes(title_text="Time (s)", zeroline=True, zerolinecolor="#555",
                      gridcolor="rgba(0,0,0,0.15)", linecolor="#555")
    fig.update_yaxes(title_text="Velocity (m/s)", zeroline=True, zerolinecolor="#555",
                      gridcolor="rgba(0,0,0,0.15)", linecolor="#555", range=[ymin, ymax])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       height=220, showlegend=False, margin=dict(l=45, r=15, t=15, b=35),
                       font=dict(size=11))
    return fig


def gen_which_graph_matches(level="N5"):
    keys = list(_SCENARIOS.keys())
    correct_key = random.choice(keys)
    others = [k for k in keys if k != correct_key]
    random.shuffle(others)
    option_keys = [correct_key] + others[:3]
    random.shuffle(option_keys)

    labels = ["A", "B", "C", "D"]
    option_figures = {label: _scenario_figure(k) for label, k in zip(labels, option_keys)}
    correct_label = labels[option_keys.index(correct_key)]

    working = [
        {"type": "text", "content": _SCENARIOS[correct_key]["desc"]},
        {"type": "text", "content": "A ball moving freely under gravity changes direction smoothly, through "
                                     "v = 0. A bounce shows as a sudden jump instead. Match the shape of each "
                                     "graph to the situation described."},
    ]
    distractor_text = {
        "thrown_up_caught": "shows a smooth, symmetric crossing through zero — that matches a ball thrown "
                             "upward and caught at the same height, not this description.",
        "dropped_caught": "shows a single ramp from zero with no direction change at all — that matches a "
                           "ball simply dropped and caught, not this description.",
        "bounce_once": "shows a sudden jump partway through — that matches a bouncing ball, not this description.",
        "thrown_up_lands_below": "shows a smooth crossing that ends further from zero than it started — that "
                                  "matches a ball thrown upward and landing below its release point, not this description.",
    }
    distractors = []
    for label, key in zip(labels, option_keys):
        if label == correct_label:
            continue
        distractors.append({
            "value": label,
            "mistake": f"Graph {label} " + distractor_text[key],
            "working": working,
        })

    question_text = (
        f"{_SCENARIOS[correct_key]['desc']}\n\n"
        f"Which velocity-time graph (A–D) matches this description?"
    )

    part = PhysicsQuestion(
        question_text=question_text, correct_answer=correct_label, unit="",
        topic="Dynamics", question_type="Speed and Velocity", level=level,
        distractors=distractors, working=working,
        metadata={"type": "graph_mcq", "options": labels, "option_figures": option_figures},
        notes=_NOTES,
    )
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Dynamics", question_type="Speed and Velocity", level=level,
        is_scenario=True, scenario_context="", parts=[part],
    )


# ── Distance and displacement from the area under a v-t graph ───────────────

def gen_distance_displacement(level="N5"):
    ctx = random.choice(_CONTEXTS)
    include_reversal = random.random() < 0.5

    if not include_reversal:
        v1 = random.choice([4, 6, 8, 10, 12, 15])
        t1 = random.choice([3, 4, 5, 6])
        to_rest = random.random() < 0.6
        v2 = 0 if to_rest else v1 + random.choice([3, 4, 5])
        t2 = random.choice([2, 3, 4, 5])

        area1 = v1 * t1
        area2 = 0.5 * (v1 + v2) * t2
        total = round(area1 + area2, 1)
        shape2 = "triangle" if v2 == 0 else "trapezium"
        phase2 = f"decelerates uniformly to rest over the next {t2} s" if v2 == 0 else \
            f"accelerates uniformly to {v2} m/s over the next {t2} s"

        question = (
            f"A {ctx} travels at a constant {v1} m/s for {t1} s, then {phase2}, as shown "
            f"on a velocity-time graph.\n\nCalculate the total distance travelled."
        )
        working = [
            {"type": "text", "content": "Distance travelled = area under the velocity-time graph."},
            {"type": "latex", "content": rf"\text{{Stage 1 (rectangle)}} = {v1} \times {t1} = {area1}\ \mathrm{{m}}"},
            {"type": "latex", "content": rf"\text{{Stage 2 ({shape2})}} = \tfrac{{1}}{{2}} \times ({v1} + {v2}) \times {t2} = {area2}\ \mathrm{{m}}"},
            {"type": "latex", "content": rf"\text{{Total distance}} = {area1} + {area2} = {total}\ \mathrm{{m}}"},
        ]
        options_data = [
            {"value": total, "mistake": None, "working": working},
            {"value": round(v1 * (t1 + t2), 1),
             "mistake": f"You treated the whole {t1 + t2} s as if the {ctx} moved at a constant {v1} m/s the "
                        f"entire time. The second stage's area is a {shape2}, not another rectangle.",
             "working": working},
            {"value": round(area1, 1),
             "mistake": "You only found the distance for the first stage — don't forget to add the second.",
             "working": working},
            {"value": round(area2, 1),
             "mistake": "You only found the distance for the second stage — don't forget to add the first.",
             "working": working},
        ]
        options_data = _dedup(options_data, total)
        return make_question(question, total, options_data, "m",
                             notes=_NOTES, topic="Dynamics", question_type="Speed and Velocity", level=level)

    # --- reversal case: two-part scenario (distance, then displacement) ---
    v0 = random.choice([4, 5, 6, 8])
    v1_mag = random.choice([2, 3, 4, 6])
    T = random.choice([5, 6, 8, 10])
    t_cross = round(v0 * T / (v0 + v1_mag), 3)

    pos_area = 0.5 * t_cross * v0
    neg_area = 0.5 * (T - t_cross) * v1_mag
    distance = round(pos_area + neg_area, 1)
    displacement = round(pos_area - neg_area, 1)

    context = (
        f"A {ctx}'s velocity changes uniformly from {v0} m/s to −{v1_mag} m/s over {T} s "
        f"(taking one direction as positive)."
    )
    working = [
        {"type": "text", "content": f"The graph crosses zero at t = {round(t_cross, 2)} s "
                                     f"(similar triangles: t ÷ {v0} = ({T} − t) ÷ {v1_mag})."},
        {"type": "latex", "content": rf"\text{{Forward area}} = \tfrac12 \times {round(t_cross,2)} \times {v0} = {round(pos_area,2)}\ \mathrm{{m}}"},
        {"type": "latex", "content": rf"\text{{Reverse area}} = \tfrac12 \times {round(T-t_cross,2)} \times {v1_mag} = {round(neg_area,2)}\ \mathrm{{m}}"},
    ]

    working_dist = working + [
        {"type": "latex", "content": rf"\text{{Distance}} = {round(pos_area,2)} + {round(neg_area,2)} = {distance}\ \mathrm{{m}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the total distance travelled.",
        correct_answer=distance, unit="m",
        topic="Dynamics", question_type="Speed and Velocity", level=level,
        working=working_dist,
        distractors=[
            {"value": abs(displacement),
             "mistake": "That's the magnitude of the displacement (the two areas partly cancel). Distance "
                        "adds both areas together regardless of direction.",
             "working": working_dist},
            {"value": round(pos_area, 2),
             "mistake": "That's only the forward part of the journey — the reverse part still adds to the "
                        "total distance travelled.",
             "working": working_dist},
        ],
        notes=_NOTES,
    )

    working_disp = working + [
        {"type": "latex", "content": rf"\text{{Displacement}} = {round(pos_area,2)} - {round(neg_area,2)} = {displacement}\ \mathrm{{m}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the total displacement.",
        correct_answer=displacement, unit="m",
        topic="Dynamics", question_type="Speed and Velocity", level=level,
        working=working_disp,
        distractors=[
            {"value": distance,
             "mistake": "That's the total distance (both areas added). Displacement subtracts the reverse "
                        "part, since it's in the opposite direction.",
             "working": working_disp},
            {"value": -distance,
             "mistake": "The reverse area should be subtracted from the forward area, not used to make the "
                        "whole distance negative.",
             "working": working_disp},
        ],
        notes=_NOTES,
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Dynamics", question_type="Speed and Velocity", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Acceleration from a v-t graph, over an interval not starting at t = 0 ───

def gen_acceleration_interval(level="N5"):
    ctx = random.choice(_CONTEXTS)
    a1 = random.choice([1, 1.5, 2, 2.5, 3])
    t1 = random.choice([6, 8, 10])
    hold = random.choice([3, 4, 5])
    a2 = random.choice([2, 3, 4]) * random.choice([1, -1])
    span2 = random.choice([2, 3, 4])

    v_end1 = a1 * t1

    stage_choice = random.choice(["stage1", "stage3"])
    if stage_choice == "stage1":
        t_start = round(random.uniform(1, t1 - 3), 1)
        t_end = round(t_start + random.uniform(2, min(4, t1 - t_start)), 1)
        v_start = round(a1 * t_start, 2)
        v_end = round(a1 * t_end, 2)
        a_answer = a1
    else:
        t3_start = t1 + hold
        t_start = round(t3_start + random.uniform(0.5, max(0.6, span2 - 1.5)), 1)
        t_end = round(t_start + random.uniform(1, span2 - (t_start - t3_start)), 1)
        v_start = round(v_end1 + a2 * (t_start - t3_start), 2)
        v_end = round(v_end1 + a2 * (t_end - t3_start), 2)
        a_answer = a2

    a_answer = round(a_answer, 2)

    context = (
        f"A {ctx}'s velocity-time graph shows it accelerating uniformly at {a1} m/s\u00b2 from rest "
        f"for the first {t1} s, then travelling at a constant velocity for {hold} s, then "
        f"{'accelerating' if a2 > 0 else 'decelerating'} uniformly at {abs(a2)} m/s\u00b2 for a "
        f"further {span2} s."
    )
    question = (
        f"{context}\n\nUsing the graph, calculate the {ctx}'s acceleration between "
        f"t = {t_start} s and t = {t_end} s."
    )
    working = [
        {"type": "text", "content": f"At t = {t_start} s, v = {v_start} m/s. At t = {t_end} s, v = {v_end} m/s."},
        {"type": "latex", "content": rf"a = \frac{{\Delta v}}{{\Delta t}} = \frac{{{v_end} - {v_start}}}{{{t_end} - {t_start}}}"},
        {"type": "latex", "content": rf"a = {a_answer}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": a_answer, "mistake": None, "working": working},
        {"value": round((v_end - v_start) / t_end, 2),
         "mistake": f"You divided by t = {t_end} s (measured from the origin) instead of the length of the "
                    f"interval itself, {round(t_end - t_start, 2)} s.",
         "working": working},
        {"value": round(v_end, 2),
         "mistake": "That's the velocity at the end of the interval, not the acceleration — you need the "
                    "*change* in velocity divided by the time taken.",
         "working": working},
    ]
    options_data = _dedup(options_data, a_answer)
    return make_question(question, a_answer, options_data, "m/s²",
                         notes=_NOTES, topic="Dynamics", question_type="Speed and Velocity", level=level)


_ALL_GENS = [
    gen_which_graph_matches,
    gen_distance_displacement,
    gen_acceleration_interval,
]


def generate_velocity_time_graphs(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
