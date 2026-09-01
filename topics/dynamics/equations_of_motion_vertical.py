import random
from utils.make_question import make_question

G = 9.8  # m/s²

_NOTES = """
## Equations of Motion — Vertical Motion

**Definitions:**
- An object falling freely, or thrown vertically, accelerates uniformly at g = 9.8 m/s²
  due to gravity (air resistance ignored).
- At the top of its flight, an object thrown upward has a vertical velocity of exactly 0 m/s.

$$v = u + at \\qquad v^2 = u^2 + 2as \\qquad s = ut + \\frac{1}{2}at^2 \\qquad s = \\frac{1}{2}(u+v)t$$

| Symbol | Quantity | Unit |
|---|---|---|
| u | Initial velocity | m/s |
| v | Final velocity | m/s |
| a | Acceleration (g = 9.8 m/s² for free fall) | m/s² |
| t | Time | s |
| s | Height / displacement | m |

**Worked Example:** A stone is dropped from rest from a bridge and takes 3.0 s to reach the water. Calculate the height of the bridge above the water.
$$s = ut + \\frac{1}{2}at^2 = 0 + \\frac{1}{2}\\times 9.8\\times 3.0^2 = 44.1\\ \\mathrm{m}$$

> **Important:** Pick a positive direction and stick to it throughout a calculation. If
> upward is positive, g is −9.8 m/s² for the whole flight — whether the object is rising,
> momentarily at rest, or falling.
"""

_DROP_CONTEXTS = [
    ("A stone", "a bridge", "the water below"),
    ("A ball", "a window", "the ground below"),
    ("A rock", "a cliff", "the sea below"),
    ("A coin", "a tall building", "the pavement below"),
]

_THROW_CONTEXTS = [
    "A ball is thrown vertically upward",
    "A stone is thrown straight up",
    "A ball is hit vertically into the air",
]


def _r2(val):
    return round(float(val), 2)


def _drop_ctx():
    return random.choice(_DROP_CONTEXTS)


# ── Dropped from rest: s = ½gt² ───────────────────────────────────────────────

def gen_drop_time_from_height(level="Higher"):
    obj, start, end = _drop_ctx()
    s = random.choice([20, 30, 45, 60, 80, 100, 122.5, 125])
    t = _r2((2 * s / G) ** 0.5)

    question = f"{obj} is dropped from rest from {start}, {s} m above {end}. Calculate the time taken to fall."
    working = [
        {"type": "text",  "content": "The object starts from rest (u = 0):"},
        {"type": "latex", "content": r"s = ut + \tfrac{1}{2}gt^2 = \tfrac{1}{2}gt^2"},
        {"type": "latex", "content": rf"t = \sqrt{{\dfrac{{2s}}{{g}}}} = \sqrt{{\dfrac{{2\times{s}}}{{9.8}}}}"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t, "mistake": None, "working": working},
        {"value": _r2((s / G) ** 0.5),
         "mistake": "You appear to have used s = gt² without the ½. The correct equation is s = ½gt², so t = √(2s/g).",
         "working": working},
        {"value": _r2(s / G),
         "mistake": "That uses s = gt (constant velocity), but the object is accelerating from rest. Use s = ½gt².",
         "working": working},
        {"value": _r2(2 * (2 * s / G) ** 0.5),
         "mistake": "Check your rearrangement of s = ½gt² for t — don't double the square root itself.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is 2s/g?", "answer": _r2(2 * s / G)},
        {"question": "What is the time taken t?", "answer": t},
    ]
    return make_question(question, t, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level, scaffold=scaffold)


def gen_drop_velocity_from_height(level="Higher"):
    obj, start, end = _drop_ctx()
    s = random.choice([20, 30, 45, 60, 80, 100, 122.5, 125])
    v = _r2((2 * G * s) ** 0.5)

    question = f"{obj} is dropped from rest from {start}, {s} m above {end}. Calculate its velocity just before it reaches {end}."
    working = [
        {"type": "text",  "content": "The object starts from rest (u = 0):"},
        {"type": "latex", "content": r"v^2 = u^2 + 2gs = 2gs"},
        {"type": "latex", "content": rf"v = \sqrt{{2\times9.8\times{s}}}"},
        {"type": "latex", "content": rf"v = {v}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v, "mistake": None, "working": working},
        {"value": _r2(G * s),
         "mistake": "You appear to have used v = gs. The correct equation is v² = 2gs, so v = √(2gs).",
         "working": working},
        {"value": _r2(2 * G * s),
         "mistake": "You forgot to take the square root after computing v² = 2gs.",
         "working": working},
        {"value": _r2((G * s) ** 0.5),
         "mistake": "You appear to have left out the factor of 2. The correct equation is v² = 2gs, so v = √(2gs).",
         "working": working},
    ]
    scaffold = [
        {"question": "What is 2gs (v²)?", "answer": _r2(2 * G * s)},
        {"question": "What is the velocity v?", "answer": v},
    ]
    return make_question(question, v, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level, scaffold=scaffold)


def gen_drop_height_from_time(level="Higher"):
    obj, start, end = _drop_ctx()
    t = random.choice([1.2, 1.5, 2.0, 2.5, 3.0, 3.5])
    s = _r2(0.5 * G * t ** 2)

    question = f"{obj} is dropped from rest from {start} and takes {t} s to reach {end}. Calculate how high above {end} it was dropped from."
    working = [
        {"type": "text",  "content": "The object starts from rest (u = 0):"},
        {"type": "latex", "content": r"s = ut + \tfrac{1}{2}gt^2 = \tfrac{1}{2}gt^2"},
        {"type": "latex", "content": rf"s = \tfrac{{1}}{{2}}\times9.8\times{t}^2"},
        {"type": "latex", "content": rf"s = {s}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": s, "mistake": None, "working": working},
        {"value": _r2(G * t ** 2),
         "mistake": "You appear to have left out the ½ in s = ½gt².",
         "working": working},
        {"value": _r2(G * t),
         "mistake": "That treats velocity as constant (s = gt), but the object is accelerating from rest. Use s = ½gt².",
         "working": working},
        {"value": _r2(0.5 * G * t),
         "mistake": "Check your formula — s = ½gt² needs t squared, not just t.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is t²?", "answer": _r2(t ** 2)},
        {"question": "What is the height s?", "answer": s},
    ]
    return make_question(question, s, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level, scaffold=scaffold)


# ── Thrown upward: v = u − gt, v² = u² − 2gs ─────────────────────────────────

def gen_throw_time_to_top(level="Higher"):
    ctx = random.choice(_THROW_CONTEXTS)
    u = random.choice([10, 12, 14, 15, 16, 18, 20, 22, 24])
    t = _r2(u / G)

    question = f"{ctx} at {u} m/s. Calculate the time taken to reach its maximum height."
    working = [
        {"type": "text",  "content": "At maximum height, the vertical velocity is zero:"},
        {"type": "latex", "content": r"v = u - gt \;\Rightarrow\; 0 = u - gt"},
        {"type": "latex", "content": rf"t = \dfrac{{u}}{{g}} = \dfrac{{{u}}}{{9.8}}"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t, "mistake": None, "working": working},
        {"value": _r2(2 * u / G),
         "mistake": "That is the time for the ball to return to its starting height (up and back down), not just the time to reach the top.",
         "working": working},
        {"value": _r2(u * G),
         "mistake": "You should divide u by g, not multiply. t = u ÷ g.",
         "working": working},
        {"value": _r2(G / u),
         "mistake": "Check which quantity goes on top. t = u ÷ g, not g ÷ u.",
         "working": working},
    ]
    return make_question(question, t, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


def gen_throw_max_height(level="Higher"):
    ctx = random.choice(_THROW_CONTEXTS)
    u = random.choice([10, 12, 14, 15, 16, 18, 20, 22, 24])
    h = _r2(u ** 2 / (2 * G))

    question = f"{ctx} at {u} m/s. Calculate the maximum height reached above its starting point."
    working = [
        {"type": "text",  "content": "At maximum height, the vertical velocity is zero:"},
        {"type": "latex", "content": r"v^2 = u^2 - 2gs \;\Rightarrow\; 0 = u^2 - 2gh"},
        {"type": "latex", "content": rf"h = \dfrac{{u^2}}{{2g}} = \dfrac{{{u}^2}}{{2\times9.8}}"},
        {"type": "latex", "content": rf"h = {h}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": h, "mistake": None, "working": working},
        {"value": _r2(u ** 2 / G),
         "mistake": "You appear to have left out the factor of 2. h = u² ÷ (2g).",
         "working": working},
        {"value": _r2(u / (2 * G)),
         "mistake": "You should square u before dividing. h = u² ÷ (2g).",
         "working": working},
        {"value": _r2((2 * G * u) ** 0.5),
         "mistake": "That rearranges the equation for a velocity, not a height. h = u² ÷ (2g).",
         "working": working},
    ]
    scaffold = [
        {"question": "What is u²?", "answer": u ** 2},
        {"question": "What is the maximum height h?", "answer": h},
    ]
    return make_question(question, h, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level, scaffold=scaffold)


def gen_throw_initial_velocity_from_height(level="Higher"):
    ctx = random.choice(_THROW_CONTEXTS)
    h = random.choice([2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0])
    u = _r2((2 * G * h) ** 0.5)

    question = f"{ctx}, reaching a maximum height of {h} m above its starting point. Calculate its initial velocity."
    working = [
        {"type": "text",  "content": "At maximum height, the vertical velocity is zero:"},
        {"type": "latex", "content": r"v^2 = u^2 - 2gh \;\Rightarrow\; 0 = u^2 - 2gh"},
        {"type": "latex", "content": rf"u = \sqrt{{2gh}} = \sqrt{{2\times9.8\times{h}}}"},
        {"type": "latex", "content": rf"u = {u}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": u, "mistake": None, "working": working},
        {"value": _r2((G * h) ** 0.5),
         "mistake": "You appear to have left out the factor of 2. u = √(2gh).",
         "working": working},
        {"value": _r2(2 * G * h),
         "mistake": "You need to take the square root of 2gh, not just compute 2gh itself.",
         "working": working},
        {"value": _r2(G * h),
         "mistake": "That computes gh, not u. Rearranging v² = u² − 2gh with v = 0 gives u = √(2gh).",
         "working": working},
    ]
    scaffold = [
        {"question": "What is 2gh (u²)?", "answer": _r2(2 * G * h)},
        {"question": "What is the initial velocity u?", "answer": u},
    ]
    return make_question(question, u, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level, scaffold=scaffold)


def gen_throw_initial_velocity_from_total_time(level="Higher"):
    ctx = random.choice(_THROW_CONTEXTS)
    T = random.choice([1.6, 2.0, 2.4, 3.0, 3.2, 3.6, 4.0])
    u = _r2(G * T / 2)

    question = f"{ctx} and returns to its starting height {T} s later. Calculate its initial velocity."
    working = [
        {"type": "text",  "content": "Since it lands at the same height it was launched from, the rise and fall take equal time:"},
        {"type": "latex", "content": r"t_{\text{up}} = \tfrac{T}{2}"},
        {"type": "latex", "content": rf"t_{{\text{{up}}}} = \tfrac{{{T}}}{{2}} = {_r2(T/2)}\ \mathrm{{s}}"},
        {"type": "text",  "content": "At maximum height, vertical velocity = 0:"},
        {"type": "latex", "content": r"v = u - g\,t_{\text{up}} \;\Rightarrow\; 0 = u - g\,t_{\text{up}}"},
        {"type": "latex", "content": rf"u = g\,t_{{\text{{up}}}} = 9.8 \times {_r2(T/2)}"},
        {"type": "latex", "content": rf"u = {u}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": u, "mistake": None, "working": working},
        {"value": _r2(G * T),
         "mistake": f"That uses the *total* flight time ({T} s), not just the time to rise. "
                    f"Halve it first: t_up = T ÷ 2, then u = g × t_up.",
         "working": working},
        {"value": _r2(G * T / 4),
         "mistake": "Check your halving — t_up = T ÷ 2, not T ÷ 4.",
         "working": working},
        {"value": _r2(T / (2 * G)),
         "mistake": "You should multiply by g, not divide. u = g × (T ÷ 2).",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the time to reach maximum height, t_up (= T/2)?", "answer": _r2(T / 2)},
        {"question": "What is the initial velocity u?", "answer": u},
    ]
    return make_question(question, u, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level, scaffold=scaffold)


_ALL_VERTICAL_GENS = [
    gen_drop_time_from_height,
    gen_drop_velocity_from_height,
    gen_drop_height_from_time,
    gen_throw_time_to_top,
    gen_throw_max_height,
    gen_throw_initial_velocity_from_height,
    gen_throw_initial_velocity_from_total_time,
]


def generate_equations_of_motion_vertical(level="Higher"):
    return random.choice(_ALL_VERTICAL_GENS)(level=level)
