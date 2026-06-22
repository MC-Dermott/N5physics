import random
import math
import pathlib
from utils.make_question import make_question

_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "relativity_widget.html"
).read_text(encoding="utf-8")

_NOTES = """
## Special Relativity

**Time dilation** — a moving clock runs slow:
$$t' = \\frac{t}{\\sqrt{1 - \\frac{v^2}{c^2}}}$$

**Length contraction** — a moving object appears shorter:
$$l' = l\\sqrt{1 - \\frac{v^2}{c^2}}$$

| Symbol | Quantity | Unit |
|---|---|---|
| t | Proper time (measured in moving frame) | s |
| t' | Dilated time (measured by stationary observer) | s |
| l | Proper length (measured in rest frame of object) | m |
| l' | Contracted length (measured by stationary observer) | m |
| v | Speed of the moving object | m/s |
| c | Speed of light = 3 × 10⁸ m/s | m/s |

> **Important:** t' > t (stationary observer measures a longer time).
> l' < l (stationary observer measures a shorter length).
> Both formulae use the same factor √(1 − v²/c²).
"""

# (v/c fraction, display string, √(1−v²/c²))
_VELOCITIES = [
    (0.6, "0.6c", 0.8),
    (0.8, "0.8c", 0.6),
]

_SHIP_CONTEXTS = [
    "A spacecraft",
    "A rocket",
    "A probe",
    "A space shuttle",
]


def _ship():
    return random.choice(_SHIP_CONTEXTS)


# ── Time dilation: t' = t / √(1 − v²/c²) ────────────────────────────────────

def gen_t_prime(level="Higher"):
    v_frac, v_str, lor = random.choice(_VELOCITIES)
    # pick t so t' = t/lor is a clean integer
    # lor = 0.8 → t multiples of 4 give clean t'; lor = 0.6 → multiples of 3
    base = 4 if lor == 0.8 else 3
    t = base * random.randint(1, 5)
    t_prime = round(t / lor, 4)
    ship = _ship()
    question = (
        f"{ship} travels at {v_str} relative to an observer on Earth. "
        f"An astronaut on board measures the journey time to be {t} s. "
        f"What journey time does the Earth observer measure?"
    )
    working = [
        {"type": "text",  "content": "Use the time dilation formula:"},
        {"type": "latex", "content": r"t' = \frac{t}{\sqrt{1 - \frac{v^2}{c^2}}}"},
        {"type": "latex", "content": rf"t' = \frac{{{t}}}{{\sqrt{{1 - {v_frac}^2}}}}"},
        {"type": "latex", "content": rf"t' = \frac{{{t}}}{{\sqrt{{1 - {round(v_frac**2,2)}}}}}"},
        {"type": "latex", "content": rf"t' = \frac{{{t}}}{{{lor}}}"},
        {"type": "latex", "content": rf"t' = {t_prime}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t_prime,              "mistake": None, "working": working},
        {"value": round(t * lor, 4),    "mistake": "You multiplied by √(1−v²/c²) instead of dividing — that is the length contraction formula, not time dilation.", "working": working},
        {"value": round(t / lor**2, 4), "mistake": "Divide by √(1−v²/c²), not by (1−v²/c²) — don't forget the square root.", "working": working},
        {"value": t,                    "mistake": "You must apply the time dilation formula — the Earth observer measures a longer time than the astronaut.", "working": working},
    ]
    options_data = _dedup(options_data, t_prime)
    return make_question(question, t_prime, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level)


def gen_t_proper(level="Higher"):
    v_frac, v_str, lor = random.choice(_VELOCITIES)
    base = 4 if lor == 0.8 else 3
    t = base * random.randint(1, 5)
    t_prime = round(t / lor, 4)
    ship = _ship()
    question = (
        f"{ship} travels at {v_str} relative to an observer on Earth. "
        f"The Earth observer measures the journey time to be {t_prime} s. "
        f"What time does the astronaut's clock show for the journey?"
    )
    working = [
        {"type": "text",  "content": "Rearrange t' = t / √(1 − v²/c²) for t:"},
        {"type": "latex", "content": r"t = t'\sqrt{1 - \frac{v^2}{c^2}}"},
        {"type": "latex", "content": rf"t = {t_prime} \times \sqrt{{1 - {v_frac}^2}}"},
        {"type": "latex", "content": rf"t = {t_prime} \times {lor}"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t,                        "mistake": None, "working": working},
        {"value": round(t_prime / lor, 4),  "mistake": "Divide by √(1−v²/c²) only when going from proper time to dilated time — here you need to multiply.", "working": working},
        {"value": round(t_prime * lor**2, 4),"mistake": "Multiply by √(1−v²/c²), not by (1−v²/c²) — don't forget the square root.", "working": working},
        {"value": t_prime,                  "mistake": "The astronaut's clock runs slow — their time is shorter than the Earth observer's time.", "working": working},
    ]
    options_data = _dedup(options_data, t)
    return make_question(question, t, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level)


# ── Length contraction: l' = l × √(1 − v²/c²) ────────────────────────────────

def gen_l_prime(level="Higher"):
    v_frac, v_str, lor = random.choice(_VELOCITIES)
    # pick l so l' = l*lor is a clean integer
    # lor = 0.8 → multiples of 5; lor = 0.6 → multiples of 5
    l = 5 * random.randint(1, 6)
    l_prime = round(l * lor, 4)
    ship = _ship()
    question = (
        f"{ship} is {l} m long when measured at rest. "
        f"It then travels at {v_str} relative to an observer on Earth. "
        f"What length does the Earth observer measure for the spacecraft?"
    )
    working = [
        {"type": "text",  "content": "Use the length contraction formula:"},
        {"type": "latex", "content": r"l' = l\sqrt{1 - \frac{v^2}{c^2}}"},
        {"type": "latex", "content": rf"l' = {l} \times \sqrt{{1 - {v_frac}^2}}"},
        {"type": "latex", "content": rf"l' = {l} \times {lor}"},
        {"type": "latex", "content": rf"l' = {l_prime}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": l_prime,              "mistake": None, "working": working},
        {"value": round(l / lor, 4),    "mistake": "You divided by √(1−v²/c²) instead of multiplying — that is the time dilation rearrangement, not length contraction.", "working": working},
        {"value": round(l * lor**2, 4), "mistake": "Multiply by √(1−v²/c²), not by (1−v²/c²) — don't forget the square root.", "working": working},
        {"value": l,                    "mistake": "You must apply the length contraction formula — the Earth observer measures a shorter length.", "working": working},
    ]
    options_data = _dedup(options_data, l_prime)
    return make_question(question, l_prime, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level)


def gen_l_proper(level="Higher"):
    v_frac, v_str, lor = random.choice(_VELOCITIES)
    l = 5 * random.randint(1, 6)
    l_prime = round(l * lor, 4)
    ship = _ship()
    question = (
        f"{ship} travels at {v_str} relative to an observer on Earth. "
        f"The Earth observer measures the spacecraft to be {l_prime} m long. "
        f"What is the proper length of the spacecraft?"
    )
    working = [
        {"type": "text",  "content": "Rearrange l' = l√(1 − v²/c²) for l:"},
        {"type": "latex", "content": r"l = \frac{l'}{\sqrt{1 - \frac{v^2}{c^2}}}"},
        {"type": "latex", "content": rf"l = \frac{{{l_prime}}}{{\sqrt{{1 - {v_frac}^2}}}}"},
        {"type": "latex", "content": rf"l = \frac{{{l_prime}}}{{{lor}}}"},
        {"type": "latex", "content": rf"l = {l}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": l,                        "mistake": None, "working": working},
        {"value": round(l_prime * lor, 4),  "mistake": "Multiply by √(1−v²/c²) only when going from proper length to contracted length — here you need to divide.", "working": working},
        {"value": round(l_prime / lor**2, 4),"mistake": "Divide by √(1−v²/c²), not by (1−v²/c²) — don't forget the square root.", "working": working},
        {"value": l_prime,                  "mistake": "The proper length is always longer than the contracted length — divide l' by √(1−v²/c²).", "working": working},
    ]
    options_data = _dedup(options_data, l)
    return make_question(question, l, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level)


# ── helpers ───────────────────────────────────────────────────────────────────

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


_ALL_GENS = [
    gen_t_prime,
    gen_t_proper,
    gen_l_prime,
    gen_l_proper,
]


def generate_special_relativity(level="Higher"):
    q = random.choice(_ALL_GENS)(level=level)
    q.metadata["widget_html"] = _WIDGET_HTML
    return q
