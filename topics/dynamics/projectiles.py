import random
import math
import pathlib
from utils.make_question import make_question
from utils.notes import NOTES

G = 9.8

_N5_PROJECTILE_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "projectile_n5_widget.html"
).read_text(encoding="utf-8")


def _with_projectile_widget(question):
    question.metadata["widget_html"] = _N5_PROJECTILE_WIDGET_HTML
    question.metadata["widget_height"] = 950
    return question


def _pick():
    v = random.randint(2, 15)
    t_mult = random.choice([x for x in range(1, 16) if x != 10])
    t = round(t_mult * 0.1, 1)
    return {
        "v_h": v,
        "t":   t,
        "range":  round(v * t, 2),
        "v_y":    round(G * t, 2),
        "height": round(0.5 * G * t ** 2, 2),
    }


def gen_find_range(level="N5"):
    s = _pick()
    v, t, correct = s["v_h"], s["t"], s["range"]

    working = [
        {"type": "text",  "content": "Horizontal motion: velocity is constant."},
        {"type": "latex", "content": r"s_H = v_H t"},
        {"type": "latex", "content": rf"s_H = {v} \times {t}"},
        {"type": "latex", "content": rf"s_H = {correct}\ \mathrm{{m}}"},
    ]
    question = (
        f"A projectile is fired horizontally at {v} m/s. "
        f"It takes {t} s to hit the ground.\n\n"
        f"Calculate the horizontal range."
    )
    options_data = [
        {"value": float(correct),          "display": f"{correct} m",        "summary": "Correct!", "mistake": None, "working": working},
        {"value": round(v * G, 2),         "display": f"{round(v * G, 2)} m", "summary": "Incorrect.", "mistake": "You multiplied the horizontal velocity by g. Use the time of flight: s_H = v_H × t.", "working": working},
        {"value": float(t),                "display": f"{t} m",              "summary": "Incorrect.", "mistake": "This is the time of flight, not the horizontal distance. Use s_H = v_H × t.", "working": working},
        {"value": round(v + t, 2),         "display": f"{round(v + t, 2)} m", "summary": "Incorrect.", "mistake": "You added velocity and time instead of multiplying. Range = v_H × t.", "working": working},
    ]
    return _with_projectile_widget(make_question(question, float(correct), options_data, "m",
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level))


def gen_find_vertical_velocity(level="N5"):
    s = _pick()
    v_h, t, correct = s["v_h"], s["t"], s["v_y"]

    working = [
        {"type": "text",  "content": "Vertical motion starts from rest (initial vertical velocity = 0)."},
        {"type": "latex", "content": r"v_v = u_v + a_v t"},
        {"type": "latex", "content": rf"v_v = 0 + 9.8 \times {t}"},
        {"type": "latex", "content": rf"v_v = {correct}\ \mathrm{{m/s}}"},
    ]
    question = (
        f"A projectile is fired horizontally at {v_h} m/s. "
        f"It falls for {t} s.\n\n"
        f"Calculate the vertical velocity just before it hits the ground."
    )
    wrong_with_horiz = round(v_h + G * t, 2)
    options_data = [
        {"value": float(correct),         "display": f"{correct} m/s",          "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(wrong_with_horiz), "display": f"{wrong_with_horiz} m/s", "summary": "Incorrect.", "mistake": f"You added the horizontal velocity ({v_h} m/s) to the vertical component. The horizontal and vertical motions are independent — the initial vertical velocity is 0.", "working": working},
        {"value": float(G),               "display": f"{G} m/s",                "summary": "Incorrect.", "mistake": "This is the acceleration due to gravity, not the final vertical velocity. Use v_v = g × t.", "working": working},
        {"value": float(s["range"]),      "display": f"{s['range']} m/s",       "summary": "Incorrect.", "mistake": "This is the horizontal range, not the vertical velocity. Use v_v = g × t for vertical motion.", "working": working},
    ]
    return _with_projectile_widget(make_question(question, float(correct), options_data, "m/s",
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level))


def gen_find_height(level="N5"):
    s = _pick()
    v_h, t, correct = s["v_h"], s["t"], s["height"]
    v_y = s["v_y"]

    working = [
        {"type": "text",  "content": "The area under the vertical v-t graph gives the height fallen."},
        {"type": "latex", "content": r"s = \frac{1}{2} g t^2"},
        {"type": "latex", "content": rf"s = \frac{{1}}{{2}} \times 9.8 \times {t}^2"},
        {"type": "latex", "content": rf"s = {correct}\ \mathrm{{m}}"},
    ]
    scaffold = [
        {"question": "Calculate the final vertical velocity.", "answer": float(v_y), "unit": "m/s"},
        {"question": "Use the v-t graph (triangle area) to find the height fallen.", "answer": float(correct), "unit": "m"},
    ]
    question = (
        f"A projectile is fired horizontally at {v_h} m/s. "
        f"It takes {t} s to hit the ground.\n\n"
        f"Calculate the height from which it was fired."
    )
    forgot_half = round(G * t ** 2, 2)
    options_data = [
        {"value": float(correct),    "display": f"{correct} m",    "summary": "Correct!", "mistake": None, "working": working},
        {"value": round(v_y * t, 2), "display": f"{round(v_y * t, 2)} m", "summary": "Incorrect.", "mistake": "You forgot the ½ factor. The area of the triangle on the v-t graph is ½ × base × height = ½ × t × v_y.", "working": working},
        {"value": float(s["range"]), "display": f"{s['range']} m", "summary": "Incorrect.", "mistake": "This is the horizontal range. Height comes from vertical motion: s = ½gt².", "working": working},
        {"value": float(forgot_half), "display": f"{forgot_half} m", "summary": "Incorrect.", "mistake": "You forgot the ½ factor. Use s = ½ × g × t².", "working": working},
    ]
    return _with_projectile_widget(make_question(question, float(correct), options_data, "m", scaffold=scaffold,
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level))


_ALL_GENS = [gen_find_range, gen_find_vertical_velocity, gen_find_height]


def generate_projectiles(level="N5"):
    return random.choice(_ALL_GENS)(level=level)


# ── Vertical motion: free fall from rest, no horizontal component ───────────
# A simpler precursor to full projectile motion — same v = gt and s = ½gt²
# relationships, but with nothing launched sideways. Mainly asks for the
# final velocity, either straight from a given fall time or (the harder
# variant) worked back from a given drop height via the time of fall.

_FREEFALL_CONTEXTS = [
    "A stone is dropped from rest from the top of a cliff.",
    "A ball is dropped from rest from a high window.",
    "A rock breaks loose and falls from rest from a ledge.",
    "An acorn falls from rest from a tree branch.",
]


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
            cleaned.insert(0, opt)
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


def gen_free_fall_velocity_from_time(level="N5"):
    context = random.choice(_FREEFALL_CONTEXTS)
    t_mult = random.choice([x for x in range(2, 21) if x != 10])
    t = round(t_mult * 0.1, 1)
    correct = round(G * t, 2)

    working = [
        {"type": "text",  "content": "Falling from rest, so the initial velocity is 0."},
        {"type": "latex", "content": r"v = u + gt"},
        {"type": "latex", "content": rf"v = 0 + 9.8 \times {t}"},
        {"type": "latex", "content": rf"v = {correct}\ \mathrm{{m/s}}"},
    ]
    question = f"{context} It takes {t} s to reach the ground.\n\nCalculate its velocity just before it hits the ground."
    options_data = [
        {"value": float(correct),  "display": f"{correct} m/s",       "mistake": None, "working": working},
        {"value": float(t),        "display": f"{t} m/s",             "mistake": "That's just the time of fall — you still need to multiply by g. v = gt.", "working": working},
        {"value": round(t / G, 3), "display": f"{round(t / G, 3)} m/s", "mistake": "You divided by g instead of multiplying. v = gt.", "working": working},
        {"value": round(0.5 * G * t ** 2, 2), "display": f"{round(0.5 * G * t ** 2, 2)} m/s",
         "mistake": "That's the height fallen (s = ½gt²), not the velocity. Use v = gt for the final velocity.", "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return make_question(question, float(correct), options_data, "m/s",
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level)


def gen_free_fall_velocity_from_height(level="N5"):
    context = random.choice(_FREEFALL_CONTEXTS)
    height = random.randint(5, 80)
    t = round(math.sqrt(2 * height / G), 2)
    correct = round(G * t, 2)

    working = [
        {"type": "text",  "content": "Step 1: Find the time of fall from the height, using s = ½gt²"},
        {"type": "latex", "content": r"t = \sqrt{\dfrac{2s}{g}}"},
        {"type": "latex", "content": rf"t = \sqrt{{\dfrac{{2 \times {height}}}{{9.8}}}} = {t}\ \mathrm{{s}}"},
        {"type": "text",  "content": "Step 2: Use the time to find the final velocity"},
        {"type": "latex", "content": r"v = gt"},
        {"type": "latex", "content": rf"v = 9.8 \times {t} = {correct}\ \mathrm{{m/s}}"},
    ]
    question = f"{context} It falls a height of {height} m.\n\nCalculate its velocity just before it hits the ground."
    forgot_sqrt = round(G * (2 * height / G), 2)
    options_data = [
        {"value": float(correct),   "display": f"{correct} m/s",   "mistake": None, "working": working},
        {"value": float(height),    "display": f"{height} m/s",    "mistake": "That's just the height fallen, not the velocity — first find the time of fall, then use v = gt.", "working": working},
        {"value": float(t),         "display": f"{t} m/s",         "mistake": "That's the time of fall, not the velocity — you still need to multiply by g. v = gt.", "working": working},
        {"value": round(forgot_sqrt, 2), "display": f"{round(forgot_sqrt, 2)} m/s",
         "mistake": "Check your rearrangement of s = ½gt² — you need to take the square root to find t, not skip straight to v = g × (2s/g).", "working": working},
    ]
    options_data = _dedup(options_data, correct)
    scaffold = [
        {"question": "What is the time of fall?", "answer": t, "unit": "s"},
        {"question": "What is the final velocity?", "answer": correct, "unit": "m/s"},
    ]
    return make_question(question, float(correct), options_data, "m/s", scaffold=scaffold,
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level)


def gen_free_fall_velocity(level="N5"):
    return random.choice([gen_free_fall_velocity_from_time, gen_free_fall_velocity_from_height])(level=level)
