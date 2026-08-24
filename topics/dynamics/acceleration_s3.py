import random
from utils.make_question import make_question
from utils.notes import NOTES

_CONTEXTS = ["car", "cyclist", "runner", "train", "bus", "skateboarder", "motorbike"]

# Acceleration can be positive (speeding up) or negative (slowing down).
_ACCELS = [-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]


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
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


# ── Level 1 — change in speed (Δv = at) ─────────────────────────────────────────

def gen_change_in_speed(level="S3"):
    a = random.choice(_ACCELS)
    t = random.randint(2, 10)
    correct = a * t
    obj = random.choice(_CONTEXTS)

    working = [
        {"type": "text",  "content": "Rearrange the acceleration equation for the change in speed:"},
        {"type": "latex", "content": r"a = \frac{v - u}{t} \quad\Rightarrow\quad v - u = at"},
        {"type": "latex", "content": rf"v - u = ({a}) \times {t}"},
        {"type": "latex", "content": rf"v - u = {correct}\ \mathrm{{m/s}}"},
    ]
    question = (
        f"A {obj} has an acceleration of {a} m/s² for {t} s.\n\n"
        f"Calculate the change in speed."
    )
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": -correct,
         "mistake": "Check the sign of the acceleration — it tells you whether the speed "
                    "increases or decreases.",
         "working": working},
        {"value": a + t,
         "mistake": "You added a and t instead of multiplying. Change in speed = a × t.",
         "working": working},
        {"value": round(a / t, 2),
         "mistake": "You divided a by t instead of multiplying. Change in speed = a × t.",
         "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return make_question(question, correct, options_data, "m/s",
                         notes=NOTES["acceleration_s3"], topic="Dynamics",
                         question_type="Acceleration", level=level)


# ── Level 2 — initial or final speed (v = u + at) ───────────────────────────────

def gen_initial_final_speed(level="S3"):
    a = random.choice(_ACCELS)
    t = random.randint(2, 10)
    u = random.randint(0, 30)
    v = round(u + a * t, 2)
    while v < 0:
        u = random.randint(0, 30)
        v = round(u + a * t, 2)
    obj = random.choice(_CONTEXTS)

    if random.choice([True, False]):
        correct = v
        question = (
            f"A {obj} starts with a speed of {u} m/s and has an acceleration of {a} m/s² for {t} s.\n\n"
            f"Calculate its final speed."
        )
        working = [
            {"type": "text",  "content": "Use v = u + at:"},
            {"type": "latex", "content": r"v = u + at"},
            {"type": "latex", "content": rf"v = {u} + ({a}) \times {t}"},
            {"type": "latex", "content": rf"v = {correct}\ \mathrm{{m/s}}"},
        ]
        options_data = [
            {"value": correct, "mistake": None, "working": working},
            {"value": round(u - a * t, 2),
             "mistake": "Add at to u (don't subtract it) to find the final speed: v = u + at.",
             "working": working},
            {"value": round(a * t, 2),
             "mistake": "You forgot to include the initial speed u: v = u + at.",
             "working": working},
            {"value": round(u / t, 2) if t else 0,
             "mistake": "Use v = u + at — don't divide the initial speed by the time.",
             "working": working},
        ]
    else:
        correct = u
        question = (
            f"A {obj} has an acceleration of {a} m/s² for {t} s and reaches a final speed of {v} m/s.\n\n"
            f"Calculate its initial speed."
        )
        working = [
            {"type": "text",  "content": "Rearrange v = u + at for u:"},
            {"type": "latex", "content": r"u = v - at"},
            {"type": "latex", "content": rf"u = {v} - ({a}) \times {t}"},
            {"type": "latex", "content": rf"u = {correct}\ \mathrm{{m/s}}"},
        ]
        options_data = [
            {"value": correct, "mistake": None, "working": working},
            {"value": round(v + a * t, 2),
             "mistake": "Subtract at from v (don't add it) to find the initial speed: u = v − at.",
             "working": working},
            {"value": round(a * t, 2),
             "mistake": "You forgot to include the final speed v: u = v − at.",
             "working": working},
            {"value": round(v / t, 2) if t else 0,
             "mistake": "Use u = v − at — don't divide the final speed by the time.",
             "working": working},
        ]

    options_data = _dedup(options_data, correct)
    return make_question(question, correct, options_data, "m/s",
                         notes=NOTES["acceleration_s3"], topic="Dynamics",
                         question_type="Acceleration", level=level)
