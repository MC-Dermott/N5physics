import random
import pathlib
from utils.make_question import make_question
from utils.notes import NOTES

_ACCELERATION_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "acceleration_widget.html"
).read_text(encoding="utf-8")


def _with_acceleration_widget(question):
    question.metadata["widget_html"] = _ACCELERATION_WIDGET_HTML
    return question


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
    return _with_acceleration_widget(make_question(question, correct, options_data, "m/s",
                         notes=NOTES["acceleration_s3"], topic="Dynamics",
                         question_type="Acceleration", level=level))


# ── Level 1b — calculating acceleration itself (a = (v - u) / t) ────────────────

def gen_calculate_acceleration(level="S3"):
    obj = random.choice(_CONTEXTS)
    a_true = random.choice(_ACCELS)
    t = random.randint(2, 10)
    if a_true >= 0:
        u = random.randint(1, 15)
    else:
        # keep v = u + a_true*t non-negative: u must be at least |a_true|*t
        u = random.randint(abs(a_true) * t, abs(a_true) * t + 15)
    v = u + a_true * t
    correct = a_true

    question = (
        f"A {obj} changes speed from {u} m/s to {v} m/s in {t} s.\n\n"
        f"Calculate its acceleration."
    )
    working = [
        {"type": "text",  "content": "Use a = (v − u) ÷ t:"},
        {"type": "latex", "content": r"a = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"a = \frac{{{v} - {u}}}{{{t}}}"},
        {"type": "latex", "content": rf"a = {correct}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": -correct,
         "mistake": "You calculated (u − v) ÷ t instead of (v − u) ÷ t — check which speed comes first.",
         "working": working},
        {"value": v - u,
         "mistake": "You found the change in speed (v − u) but forgot to divide by the time.",
         "working": working},
        {"value": round(v / t, 2),
         "mistake": "Use a = (v − u) ÷ t — divide the change in speed by time, not just v by t.",
         "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return _with_acceleration_widget(make_question(question, correct, options_data, "m/s²",
                         notes=NOTES["acceleration_s3"], topic="Dynamics",
                         question_type="Acceleration", level=level))


# ── Level 1c — calculating time from a and Δv (t = Δv / a) ──────────────────────

def gen_calculate_time(level="S3"):
    obj = random.choice(_CONTEXTS)
    a = random.choice([1.5, 2, 2.5, 3, 4, 5, 6])
    t_true = random.randint(2, 10)
    delta_v = round(a * t_true, 2)
    correct = t_true

    question = (
        f"A {obj} accelerates at {a} m/s². Its speed changes by {delta_v} m/s.\n\n"
        f"Calculate how long this takes."
    )
    working = [
        {"type": "text",  "content": "Rearrange a = Δv ÷ t for t:"},
        {"type": "latex", "content": r"t = \frac{\Delta v}{a}"},
        {"type": "latex", "content": rf"t = \frac{{{delta_v}}}{{{a}}}"},
        {"type": "latex", "content": rf"t = {correct}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round(delta_v * a, 2),
         "mistake": "You multiplied Δv by a instead of dividing. t = Δv ÷ a.",
         "working": working},
        {"value": round(a / delta_v, 4) if delta_v else 0,
         "mistake": "You divided a by Δv instead of Δv by a. t = Δv ÷ a.",
         "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return _with_acceleration_widget(make_question(question, correct, options_data, "s",
                         notes=NOTES["acceleration_s3"], topic="Dynamics",
                         question_type="Acceleration", level=level))


# ── Level 2 — initial or final speed (v = u + at) ───────────────────────────────

def gen_initial_final_speed(level="S3"):
    a = random.choice(_ACCELS)
    if a >= 0:
        t = random.randint(2, 10)
        u = random.randint(0, 30)
    else:
        # keep v = u + a*t non-negative: cap t so that even u = 30 can cover it
        t = random.randint(2, max(2, min(10, 30 // abs(a))))
        u = random.randint(abs(a) * t, 30)
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
    return _with_acceleration_widget(make_question(question, correct, options_data, "m/s",
                         notes=NOTES["acceleration_s3"], topic="Dynamics",
                         question_type="Acceleration", level=level))
