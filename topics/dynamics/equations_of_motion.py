import random
import math
from utils.make_question import make_question

_NOTES = """
## Equations of Motion

$$v = u + at$$
$$v^2 = u^2 + 2as$$
$$s = ut + \\frac{1}{2}at^2$$
$$s = \\frac{1}{2}(u + v)t$$

| Symbol | Quantity | Unit |
|---|---|---|
| u | Initial velocity | m/s |
| v | Final velocity | m/s |
| a | Acceleration | m/s² |
| t | Time | s |
| s | Displacement | m |

> **Important:** These equations only apply when acceleration is **uniform** (constant).
> A negative acceleration means the object is decelerating (slowing down).
"""

_CONTEXTS = [
    ("A car", "a straight road"),
    ("A train", "a straight track"),
    ("A cyclist", "a straight road"),
    ("A motorbike", "a straight road"),
    ("A sprinter", "a running track"),
]


def _ctx():
    obj, loc = random.choice(_CONTEXTS)
    return obj, loc


# ── v = u + at ────────────────────────────────────────────────────────────────

def _working_v_from_uat(u, a, t, v):
    return [
        {"type": "text",  "content": "Identify the equation connecting u, a, t and v:"},
        {"type": "latex", "content": r"v = u + at"},
        {"type": "latex", "content": rf"v = {u} + ({a}) \times {t}"},
        {"type": "latex", "content": rf"v = {v}\ \mathrm{{m/s}}"},
    ]


def gen_v_from_uat(level="Higher"):
    u = random.randint(5, 20)
    a = random.choice([-1, -2, -3, 1, 2, 3])
    t = random.randint(3, 8)
    v = round(u + a * t, 2)
    # ensure v is positive and different from u
    while v <= 0 or v == u:
        u = random.randint(5, 20)
        a = random.choice([-1, -2, -3, 1, 2, 3])
        t = random.randint(3, 8)
        v = round(u + a * t, 2)
    obj, loc = _ctx()
    a_desc = f"{abs(a)} m/s²"
    accel_word = "decelerates uniformly" if a < 0 else "accelerates uniformly"
    question = (
        f"{obj} is travelling at {u} m/s along {loc}. "
        f"It {accel_word} at {a_desc} for {t} s. "
        f"What is its final velocity?"
    )
    working = _working_v_from_uat(u, a, t, v)
    options_data = [
        {"value": v,               "mistake": None,    "working": working},
        {"value": u + abs(a) * t,  "mistake": "Check the sign of the acceleration — decelerating means a is negative.", "working": working},
        {"value": u * a * t,       "mistake": "You should add at to u, not multiply all three together.", "working": working},
        {"value": abs(a) * t,      "mistake": "You forgot to include the initial velocity u.", "working": working},
    ]
    # remove duplicates
    options_data = _dedup(options_data, v)
    return make_question(question, v, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


def gen_u_from_vat(level="Higher"):
    v = random.randint(5, 25)
    a = random.choice([-1, -2, -3, 1, 2, 3])
    t = random.randint(3, 8)
    u = round(v - a * t, 2)
    while u <= 0 or u == v:
        v = random.randint(5, 25)
        a = random.choice([-1, -2, -3, 1, 2, 3])
        t = random.randint(3, 8)
        u = round(v - a * t, 2)
    obj, loc = _ctx()
    accel_word = "decelerating" if a < 0 else "accelerating"
    question = (
        f"{obj} is {accel_word} uniformly at {abs(a)} m/s² along {loc}. "
        f"After {t} s its velocity is {v} m/s. "
        f"What was its initial velocity?"
    )
    working = [
        {"type": "text",  "content": "Rearrange v = u + at for u:"},
        {"type": "latex", "content": r"u = v - at"},
        {"type": "latex", "content": rf"u = {v} - ({a}) \times {t}"},
        {"type": "latex", "content": rf"u = {u}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": u,               "mistake": None, "working": working},
        {"value": v + a * t,       "mistake": "Check the rearrangement — u = v − at, not v + at.", "working": working},
        {"value": v + abs(a) * t,  "mistake": "Check both the rearrangement and the sign of a.", "working": working},
        {"value": v / t,           "mistake": "You divided v by t — use v = u + at and rearrange for u.", "working": working},
    ]
    options_data = _dedup(options_data, u)
    return make_question(question, u, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


def gen_a_from_vut(level="Higher"):
    u = random.randint(5, 20)
    t = random.randint(3, 8)
    delta_v = random.choice([-2, -3, -4, -6, 2, 3, 4, 6]) * t
    v = u + delta_v
    while v <= 0 or v == u:
        u = random.randint(5, 20)
        t = random.randint(3, 8)
        delta_v = random.choice([-2, -3, -4, -6, 2, 3, 4, 6]) * t
        v = u + delta_v
    a = round((v - u) / t, 2)
    obj, loc = _ctx()
    question = (
        f"{obj} is travelling along {loc}. "
        f"Its velocity changes from {u} m/s to {v} m/s in {t} s. "
        f"Calculate its acceleration."
    )
    working = [
        {"type": "text",  "content": "Rearrange v = u + at for a:"},
        {"type": "latex", "content": r"a = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"a = \frac{{{v} - {u}}}{{{t}}}"},
        {"type": "latex", "content": rf"a = {a}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": a,                       "mistake": None, "working": working},
        {"value": round((v + u) / t, 2),   "mistake": "Subtract u from v (don't add) when finding the change in velocity.", "working": working},
        {"value": round((v - u) * t, 2),   "mistake": "Divide (v − u) by t — don't multiply.", "working": working},
        {"value": round(v / t, 2),          "mistake": "Use a = (v − u)/t — you must subtract the initial velocity.", "working": working},
    ]
    options_data = _dedup(options_data, a)
    return make_question(question, a, options_data, "m/s²",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


def gen_t_from_vua(level="Higher"):
    u = random.randint(5, 20)
    a = random.choice([-1, -2, -3, 1, 2, 3])
    t = random.randint(3, 8)
    v = round(u + a * t, 2)
    while v <= 0 or v == u:
        u = random.randint(5, 20)
        a = random.choice([-1, -2, -3, 1, 2, 3])
        t = random.randint(3, 8)
        v = round(u + a * t, 2)
    obj, loc = _ctx()
    accel_word = "decelerates" if a < 0 else "accelerates"
    question = (
        f"{obj} is travelling at {u} m/s along {loc}. "
        f"It {accel_word} uniformly at {abs(a)} m/s² until its velocity is {v} m/s. "
        f"How long does this take?"
    )
    working = [
        {"type": "text",  "content": "Rearrange v = u + at for t:"},
        {"type": "latex", "content": r"t = \frac{v - u}{a}"},
        {"type": "latex", "content": rf"t = \frac{{{v} - {u}}}{{{a}}}"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t,                        "mistake": None, "working": working},
        {"value": round((v + u) / a, 2),    "mistake": "Subtract u from v (don't add) to find the change in velocity.", "working": working},
        {"value": round((v - u) * a, 2),    "mistake": "Divide (v − u) by a — don't multiply.", "working": working},
        {"value": round(v / a, 2),          "mistake": "Use t = (v − u)/a — you must subtract u.", "working": working},
    ]
    options_data = _dedup(options_data, t)
    return make_question(question, t, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


# ── v² = u² + 2as ─────────────────────────────────────────────────────────────

def gen_v_from_uas(level="Higher"):
    u = random.randint(5, 15)
    a = random.choice([1, 2, 3])
    s = random.choice([20, 30, 40, 50, 60, 80, 100])
    v2 = u * u + 2 * a * s
    v = round(math.sqrt(v2), 2)
    obj, loc = _ctx()
    question = (
        f"{obj} is travelling at {u} m/s along {loc}. "
        f"It accelerates uniformly at {a} m/s² over a distance of {s} m. "
        f"What is its final velocity?"
    )
    working = [
        {"type": "text",  "content": "Use v² = u² + 2as:"},
        {"type": "latex", "content": r"v^2 = u^2 + 2as"},
        {"type": "latex", "content": rf"v^2 = {u}^2 + 2 \times {a} \times {s}"},
        {"type": "latex", "content": rf"v^2 = {u*u} + {2*a*s} = {v2}"},
        {"type": "latex", "content": rf"v = \sqrt{{{v2}}} = {v}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v,                              "mistake": None, "working": working},
        {"value": round(math.sqrt(u*u + a*s), 2), "mistake": "Don't forget the factor of 2 in 2as.", "working": working},
        {"value": round(math.sqrt(u + 2*a*s), 2), "mistake": "Remember to square u: v² = u² + 2as, not v² = u + 2as.", "working": working},
        {"value": u + 2*a*s,                      "mistake": "You must take the square root of (u² + 2as) to find v.", "working": working},
    ]
    options_data = _dedup(options_data, v)
    return make_question(question, v, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


def gen_s_from_vua_sq(level="Higher"):
    u = random.randint(5, 20)
    a = random.choice([-1, -2, -3, 1, 2, 3])
    t = random.randint(3, 8)
    v = round(u + a * t, 2)
    while v <= 0 or v == u:
        u = random.randint(5, 20)
        a = random.choice([-1, -2, -3, 1, 2, 3])
        t = random.randint(3, 8)
        v = round(u + a * t, 2)
    s = round((v*v - u*u) / (2*a), 2)
    obj, loc = _ctx()
    accel_word = "decelerating" if a < 0 else "accelerating"
    question = (
        f"{obj} is {accel_word} uniformly at {abs(a)} m/s² along {loc}. "
        f"Its velocity changes from {u} m/s to {v} m/s. "
        f"Calculate the distance travelled."
    )
    working = [
        {"type": "text",  "content": "Rearrange v² = u² + 2as for s:"},
        {"type": "latex", "content": r"s = \frac{v^2 - u^2}{2a}"},
        {"type": "latex", "content": rf"s = \frac{{{v}^2 - {u}^2}}{{2 \times ({a})}}"},
        {"type": "latex", "content": rf"s = \frac{{{round(v*v,2)} - {u*u}}}{{{2*a}}}"},
        {"type": "latex", "content": rf"s = {s}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": s,                              "mistake": None, "working": working},
        {"value": round((v - u) / (2*a), 2),      "mistake": "Square v and u first: use (v² − u²), not (v − u).", "working": working},
        {"value": round((v*v - u*u) / a, 2),      "mistake": "Don't forget the factor of 2 in 2as — use s = (v² − u²) / (2a).", "working": working},
        {"value": round((v*v + u*u) / (2*a), 2),  "mistake": "Subtract u² from v² — don't add them.", "working": working},
    ]
    options_data = _dedup(options_data, s)
    return make_question(question, s, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


def gen_a_from_vus(level="Higher"):
    u = random.randint(5, 15)
    a = random.choice([1, 2, 3])
    s = random.choice([20, 30, 40, 50, 60, 80])
    v2 = u*u + 2*a*s
    v = round(math.sqrt(v2), 2)
    obj, loc = _ctx()
    question = (
        f"{obj} accelerates uniformly along {loc}, "
        f"covering {s} m while its velocity increases from {u} m/s to {v} m/s. "
        f"Calculate the acceleration."
    )
    working = [
        {"type": "text",  "content": "Rearrange v² = u² + 2as for a:"},
        {"type": "latex", "content": r"a = \frac{v^2 - u^2}{2s}"},
        {"type": "latex", "content": rf"a = \frac{{{v}^2 - {u}^2}}{{2 \times {s}}}"},
        {"type": "latex", "content": rf"a = \frac{{{v2} - {u*u}}}{{{2*s}}}"},
        {"type": "latex", "content": rf"a = {a}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": a,                               "mistake": None, "working": working},
        {"value": round((v - u) / (2*s), 2),       "mistake": "Square v and u first: use (v² − u²), not (v − u).", "working": working},
        {"value": round((v2 - u*u) / s, 2),        "mistake": "Don't forget the factor of 2: use a = (v² − u²) / (2s).", "working": working},
        {"value": round((v2 + u*u) / (2*s), 2),    "mistake": "Subtract u² from v² — don't add them.", "working": working},
    ]
    options_data = _dedup(options_data, a)
    return make_question(question, a, options_data, "m/s²",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


# ── s = ut + ½at² ─────────────────────────────────────────────────────────────

def gen_s_from_uat_sq(level="Higher"):
    u = random.randint(5, 20)
    a = random.choice([-1, -2, -3, 1, 2, 3])
    t = random.randint(3, 8)
    s = round(u*t + 0.5*a*t*t, 2)
    while s <= 0:
        u = random.randint(5, 20)
        a = random.choice([-1, -2, -3, 1, 2, 3])
        t = random.randint(3, 8)
        s = round(u*t + 0.5*a*t*t, 2)
    obj, loc = _ctx()
    accel_word = "decelerates uniformly" if a < 0 else "accelerates uniformly"
    a_desc = f"{abs(a)} m/s²"
    question = (
        f"{obj} is travelling at {u} m/s along {loc}. "
        f"It {accel_word} at {a_desc} for {t} s. "
        f"Calculate the distance travelled."
    )
    wrong_sign = round(u*t - 0.5*a*t*t, 2)   # used wrong sign for a
    forgot_half = round(u*t + a*t*t, 2)        # forgot the ½
    forgot_accel = round(u*t, 2)               # forgot ½at² entirely
    working = [
        {"type": "text",  "content": "Use s = ut + ½at²:"},
        {"type": "latex", "content": r"s = ut + \frac{1}{2}at^2"},
        {"type": "latex", "content": rf"s = {u} \times {t} + \frac{{1}}{{2}} \times ({a}) \times {t}^2"},
        {"type": "latex", "content": rf"s = {round(u*t,2)} + {round(0.5*a*t*t,2)}"},
        {"type": "latex", "content": rf"s = {s}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": s,           "mistake": None, "working": working},
        {"value": wrong_sign,  "mistake": "Check the sign of the acceleration — decelerating means a is negative in the equation.", "working": working},
        {"value": forgot_half, "mistake": "Don't forget the ½ in ½at².", "working": working},
        {"value": forgot_accel,"mistake": "You only used ut — don't forget the ½at² term.", "working": working},
    ]
    options_data = _dedup(options_data, s)
    return make_question(question, s, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


def gen_a_from_sut_sq(level="Higher"):
    u = random.randint(2, 10)
    a = random.choice([1, 2, 3, 4])
    t = random.randint(3, 7)
    s = round(u*t + 0.5*a*t*t, 2)
    obj, loc = _ctx()
    question = (
        f"{obj} starts from {u} m/s and travels {s} m along {loc} in {t} s under uniform acceleration. "
        f"Calculate the acceleration."
    )
    working = [
        {"type": "text",  "content": "Rearrange s = ut + ½at² for a:"},
        {"type": "latex", "content": r"a = \frac{2(s - ut)}{t^2}"},
        {"type": "latex", "content": rf"a = \frac{{2({s} - {u} \times {t})}}{{{t}^2}}"},
        {"type": "latex", "content": rf"a = \frac{{2 \times {round(s - u*t, 2)}}}{{{t*t}}}"},
        {"type": "latex", "content": rf"a = {a}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": a,                               "mistake": None, "working": working},
        {"value": round(2*s / (t*t), 2),           "mistake": "Subtract the ut term first: a = 2(s − ut) / t².", "working": working},
        {"value": round((s - u*t) / (t*t), 2),     "mistake": "Don't forget the factor of 2: a = 2(s − ut) / t².", "working": working},
        {"value": round(2*(s - u*t) / t, 2),       "mistake": "Divide by t² (not just t): a = 2(s − ut) / t².", "working": working},
    ]
    options_data = _dedup(options_data, a)
    return make_question(question, a, options_data, "m/s²",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


def gen_u_from_sat_sq(level="Higher"):
    u = random.randint(3, 12)
    a = random.choice([1, 2, 3])
    t = random.randint(3, 7)
    s = round(u*t + 0.5*a*t*t, 2)
    obj, loc = _ctx()
    question = (
        f"{obj} accelerates uniformly at {a} m/s² along {loc} for {t} s, "
        f"covering {s} m. "
        f"What was its initial velocity?"
    )
    working = [
        {"type": "text",  "content": "Rearrange s = ut + ½at² for u:"},
        {"type": "latex", "content": r"u = \frac{s - \frac{1}{2}at^2}{t}"},
        {"type": "latex", "content": rf"u = \frac{{{s} - \frac{{1}}{{2}} \times {a} \times {t}^2}}{{{t}}}"},
        {"type": "latex", "content": rf"u = \frac{{{s} - {round(0.5*a*t*t,2)}}}{{{t}}}"},
        {"type": "latex", "content": rf"u = {u}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": u,                               "mistake": None, "working": working},
        {"value": round(s / t, 2),                 "mistake": "Subtract the ½at² term before dividing: u = (s − ½at²) / t.", "working": working},
        {"value": round((s - a*t*t) / t, 2),       "mistake": "Don't forget the ½ in ½at²: u = (s − ½at²) / t.", "working": working},
        {"value": round((s + 0.5*a*t*t) / t, 2),  "mistake": "Subtract ½at² from s — don't add it.", "working": working},
    ]
    options_data = _dedup(options_data, u)
    return make_question(question, u, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


# ── s = ½(u + v)t ─────────────────────────────────────────────────────────────

def gen_s_from_uvt(level="Higher"):
    u = random.randint(2, 15)
    v = random.randint(2, 25)
    while v == u:
        v = random.randint(2, 25)
    t = random.randint(3, 10)
    s = round(0.5*(u+v)*t, 2)
    obj, loc = _ctx()
    accel_word = "decelerates" if v < u else "accelerates"
    question = (
        f"{obj} {accel_word} uniformly along {loc} from {u} m/s to {v} m/s in {t} s. "
        f"Calculate the distance travelled."
    )
    working = [
        {"type": "text",  "content": "Use s = ½(u + v)t:"},
        {"type": "latex", "content": r"s = \frac{1}{2}(u + v)t"},
        {"type": "latex", "content": rf"s = \frac{{1}}{{2}} \times ({u} + {v}) \times {t}"},
        {"type": "latex", "content": rf"s = \frac{{1}}{{2}} \times {u+v} \times {t}"},
        {"type": "latex", "content": rf"s = {s}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": s,                   "mistake": None, "working": working},
        {"value": (u+v)*t,             "mistake": "Don't forget the ½ in s = ½(u + v)t.", "working": working},
        {"value": round(0.5*u*t, 2),   "mistake": "You need both u and v: s = ½(u + v)t, not just ½ut.", "working": working},
        {"value": round(0.5*v*t, 2),   "mistake": "You need both u and v: s = ½(u + v)t, not just ½vt.", "working": working},
    ]
    options_data = _dedup(options_data, s)
    return make_question(question, s, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


def gen_t_from_uvs(level="Higher"):
    u = random.randint(2, 15)
    v = random.randint(2, 25)
    while v == u:
        v = random.randint(2, 25)
    t = random.randint(3, 10)
    s = round(0.5*(u+v)*t, 2)
    obj, loc = _ctx()
    accel_word = "decelerates" if v < u else "accelerates"
    question = (
        f"{obj} {accel_word} uniformly from {u} m/s to {v} m/s along {loc}, "
        f"covering {s} m. "
        f"How long does this take?"
    )
    working = [
        {"type": "text",  "content": "Rearrange s = ½(u + v)t for t:"},
        {"type": "latex", "content": r"t = \frac{2s}{u + v}"},
        {"type": "latex", "content": rf"t = \frac{{2 \times {s}}}{{{u} + {v}}}"},
        {"type": "latex", "content": rf"t = \frac{{{2*s}}}{{{u+v}}}"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t,                        "mistake": None, "working": working},
        {"value": round(s / (u+v), 2),      "mistake": "Don't forget the factor of 2: t = 2s / (u + v).", "working": working},
        {"value": round(2*s / u, 2),        "mistake": "Divide by (u + v), not just u.", "working": working},
        {"value": round(2*s / (u*v), 2),    "mistake": "Add u and v (don't multiply): t = 2s / (u + v).", "working": working},
    ]
    options_data = _dedup(options_data, t)
    return make_question(question, t, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


def gen_u_from_svt(level="Higher"):
    v = random.randint(5, 25)
    t = random.randint(3, 10)
    u = random.randint(2, v - 1) if v > 2 else random.randint(v + 1, 20)
    s = round(0.5*(u+v)*t, 2)
    obj, loc = _ctx()
    question = (
        f"{obj} decelerates uniformly from its initial velocity to {v} m/s along {loc}, "
        f"taking {t} s and covering {s} m. "
        f"What was its initial velocity?"
    )
    working = [
        {"type": "text",  "content": "Rearrange s = ½(u + v)t for u:"},
        {"type": "latex", "content": r"u = \frac{2s}{t} - v"},
        {"type": "latex", "content": rf"u = \frac{{2 \times {s}}}{{{t}}} - {v}"},
        {"type": "latex", "content": rf"u = {round(2*s/t, 2)} - {v}"},
        {"type": "latex", "content": rf"u = {u}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": u,                          "mistake": None, "working": working},
        {"value": round(2*s/t + v, 2),        "mistake": "Subtract v (don't add it): u = 2s/t − v.", "working": working},
        {"value": round(s/t - v, 2),          "mistake": "Don't forget the factor of 2: u = 2s/t − v.", "working": working},
        {"value": round(2*s / (t + v), 2),    "mistake": "Rearrange correctly: multiply both sides by 2/t first, then subtract v.", "working": working},
    ]
    options_data = _dedup(options_data, u)
    return make_question(question, u, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Equations of Motion", level=level)


# ── helpers ───────────────────────────────────────────────────────────────────

def _dedup(options_data, correct):
    """Remove distractor entries whose value equals the correct answer or another distractor."""
    seen = {round(float(correct), 4)}
    cleaned = []
    for opt in options_data:
        key = round(float(opt["value"]), 4)
        if key not in seen:
            seen.add(key)
            cleaned.append(opt)
        elif opt["mistake"] is None:
            cleaned.insert(0, opt)  # always keep correct
    # ensure correct is present
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


_ALL_GENS = [
    gen_v_from_uat,
    gen_u_from_vat,
    gen_a_from_vut,
    gen_t_from_vua,
    gen_v_from_uas,
    gen_s_from_vua_sq,
    gen_a_from_vus,
    gen_s_from_uat_sq,
    gen_a_from_sut_sq,
    gen_u_from_sat_sq,
    gen_s_from_uvt,
    gen_t_from_uvs,
    gen_u_from_svt,
]


def generate_equations_of_motion(level="Higher"):
    return random.choice(_ALL_GENS)(level=level)
