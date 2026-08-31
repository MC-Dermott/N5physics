import random
from utils.make_question import make_question

_NOTES = """
## Velocity-Time Graphs

**Key ideas:**
- The **area under** a velocity-time graph gives the **distance** (or displacement)
  travelled during that time.
- A straight line that **crosses the time axis** (velocity = 0) shows the moment the
  object **changes direction** — before that instant it moves one way, after it
  moves the opposite way.

**Worked Example (area):** A car travels at a constant 10 m/s for 4 s, then
decelerates uniformly to rest over the next 3 s.
- Stage 1 (rectangle): 10 × 4 = 40 m
- Stage 2 (triangle): ½ × 10 × 3 = 15 m
- Total distance = 40 + 15 = 55 m

**Worked Example (direction change):** A trolley's velocity decreases uniformly
from 8 m/s at t = 0 s to −4 m/s at t = 6 s.
- By similar triangles: t ÷ 8 = (6 − t) ÷ 4, so t = 8 × 6 ÷ (8 + 4) = 4 s
- The trolley changes direction at t = 4 s.

> **Common exam trap:** distance is the *area*, not a single velocity value read off
> the graph — always check whether the shape under the line is a rectangle,
> triangle, or trapezium before calculating.
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


# ── Distance from the area under a v-t graph ─────────────────────────────────

def gen_distance_from_area(level="N5"):
    ctx = random.choice(_CONTEXTS)
    v1 = random.choice([4, 6, 8, 10, 12, 15])
    t1 = random.choice([3, 4, 5, 6])
    to_rest = random.random() < 0.6
    v2 = 0 if to_rest else v1 + random.choice([3, 4, 5])
    t2 = random.choice([2, 3, 4, 5])

    area1 = v1 * t1
    area2 = 0.5 * (v1 + v2) * t2
    total = round(area1 + area2, 1)

    if v2 == 0:
        phase2 = f"decelerates uniformly to rest over the next {t2} s"
        shape2 = "triangle"
    else:
        phase2 = f"accelerates uniformly to {v2} m/s over the next {t2} s"
        shape2 = "trapezium"

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
         "mistake": f"You treated the whole {t1 + t2} s as if the {ctx} moved at a constant {v1} m/s the entire "
                    f"time. The second stage's area is a {shape2}, not another rectangle at {v1} m/s.",
         "working": working},
        {"value": round(area1, 1),
         "mistake": f"You only found the distance for the first {t1} s. Don't forget to add the area of the "
                    f"second stage too.",
         "working": working},
        {"value": round(area2, 1),
         "mistake": f"You only found the distance for the second stage. Don't forget to add the area of the "
                    f"first {t1} s at constant {v1} m/s too.",
         "working": working},
    ]
    options_data = _dedup(options_data, total)
    return make_question(question, total, options_data, "m",
                         notes=_NOTES, topic="Dynamics", question_type="Speed and Velocity", level=level)


# ── Reading a v-t graph: when does the object change direction? ─────────────

def gen_direction_change(level="N5"):
    ctx = random.choice(_CONTEXTS)
    v0 = random.choice([4, 6, 8, 10, 12])
    v1_mag = random.choice([2, 3, 4, 5, 6])
    T = random.choice([4, 6, 8, 10])
    t0 = round(v0 * T / (v0 + v1_mag), 2)

    question = (
        f"A {ctx}'s velocity, as shown on a velocity-time graph, decreases uniformly "
        f"from {v0} m/s at t = 0 s to −{v1_mag} m/s at t = {T} s.\n\n"
        f"Calculate the time at which the {ctx} changes direction."
    )

    working = [
        {"type": "text", "content": "The object changes direction at the instant its velocity is zero — "
                                     "where the line crosses the time axis."},
        {"type": "text", "content": "Using similar triangles on either side of that crossing point:"},
        {"type": "latex", "content": rf"\frac{{t}}{{{v0}}} = \frac{{{T} - t}}{{{v1_mag}}}"},
        {"type": "latex", "content": rf"t = \frac{{{v0} \times {T}}}{{{v0} + {v1_mag}}} = {t0}\ \mathrm{{s}}"},
    ]

    midpoint = round(T / 2, 2)
    options_data = [
        {"value": t0, "mistake": None, "working": working},
        {"value": midpoint,
         "mistake": f"The crossing point isn't necessarily halfway through the {T} s — it depends on how large "
                    f"each velocity is, not just the total time. Use similar triangles with the actual "
                    f"velocity values.",
         "working": working},
        {"value": round(T - t0, 2),
         "mistake": "That's the time remaining *after* the direction change, not the time at which it happens.",
         "working": working},
        {"value": v0,
         "mistake": "That's the initial velocity, not a time. Set up the similar-triangles equation using the "
                    "two velocities and the total time.",
         "working": working},
    ]
    options_data = _dedup(options_data, t0)
    return make_question(question, t0, options_data, "s",
                         notes=_NOTES, topic="Dynamics", question_type="Speed and Velocity", level=level)


_ALL_GENS = [
    gen_distance_from_area,
    gen_direction_change,
]


def generate_velocity_time_graphs(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
