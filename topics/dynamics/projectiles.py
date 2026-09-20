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
        {"type": "latex", "content": r"a = \dfrac{v - u}{t}"},
        {"type": "latex", "content": rf"9.8 = \dfrac{{v - 0}}{{{t}}}"},
        {"type": "latex", "content": rf"v = 9.8 \times {t} = {correct}\ \mathrm{{m/s}}"},
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
        {"value": float(G),               "display": f"{G} m/s",                "summary": "Incorrect.", "mistake": "This is the acceleration due to gravity, not the final vertical velocity. Use a = (v − u) ÷ t, rearranged to v = a × t.", "working": working},
        {"value": float(s["range"]),      "display": f"{s['range']} m/s",       "summary": "Incorrect.", "mistake": "This is the horizontal range, not the vertical velocity. Use a = (v − u) ÷ t for vertical motion.", "working": working},
    ]
    return _with_projectile_widget(make_question(question, float(correct), options_data, "m/s",
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level))


def gen_find_height(level="N5"):
    s = _pick()
    v_h, t, correct = s["v_h"], s["t"], s["height"]
    v_y = s["v_y"]

    working = [
        {"type": "text",  "content": "First find the vertical velocity, then use the v-t graph to find the height."},
        {"type": "latex", "content": r"a = \dfrac{v - u}{t} \;\Rightarrow\; v = 9.8 \times t = " + f"{v_y}" + r"\ \mathrm{m/s}"},
        {"type": "text",  "content": "The height fallen is the area under the v-t graph (a triangle)."},
        {"type": "latex", "content": rf"\text{{height}} = \tfrac{{1}}{{2}} \times {t} \times {v_y} = {correct}\ \mathrm{{m}}"},
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
    forgot_half = round(v_y * t, 2)
    options_data = [
        {"value": float(correct),    "display": f"{correct} m",    "summary": "Correct!", "mistake": None, "working": working},
        {"value": forgot_half,       "display": f"{forgot_half} m", "summary": "Incorrect.", "mistake": "You forgot the ½ factor. The area of the triangle on the v-t graph is ½ × base × height = ½ × t × v.", "working": working},
        {"value": float(s["range"]), "display": f"{s['range']} m", "summary": "Incorrect.", "mistake": "This is the horizontal range. The height comes from the vertical motion — sketch the v-t graph and find the area under it.", "working": working},
        {"value": float(v_y),        "display": f"{v_y} m",         "summary": "Incorrect.", "mistake": "That's the vertical velocity, not the height. Use it as the graph height and find the triangle's area.", "working": working},
    ]
    return _with_projectile_widget(make_question(question, float(correct), options_data, "m", scaffold=scaffold,
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level))


def gen_find_time_from_range(level="N5"):
    s = _pick()
    v_h, t, correct = s["v_h"], s["v_h"], s["t"]
    correct = s["t"]
    rng = s["range"]

    working = [
        {"type": "text",  "content": "Horizontal motion: velocity is constant, so rearrange s_H = v_H t for t."},
        {"type": "latex", "content": r"s_H = v_H t \;\Rightarrow\; t = \dfrac{s_H}{v_H}"},
        {"type": "latex", "content": rf"t = \dfrac{{{rng}}}{{{s['v_h']}}} = {correct}\ \mathrm{{s}}"},
    ]
    question = (
        f"A projectile is fired horizontally at {s['v_h']} m/s. "
        f"It lands a horizontal distance of {rng} m from its launch point.\n\n"
        f"Calculate the time taken for the projectile to hit the ground."
    )
    options_data = [
        {"value": float(correct),           "display": f"{correct} s",           "summary": "Correct!", "mistake": None, "working": working},
        {"value": round(rng * s["v_h"], 2), "display": f"{round(rng * s['v_h'], 2)} s", "summary": "Incorrect.", "mistake": "You multiplied the range and horizontal velocity instead of dividing. t = s_H ÷ v_H.", "working": working},
        {"value": float(rng),               "display": f"{rng} s",               "summary": "Incorrect.", "mistake": "That's the range, not the time. Rearrange s_H = v_H t for t.", "working": working},
        {"value": float(s["v_h"]),          "display": f"{s['v_h']} s",          "summary": "Incorrect.", "mistake": "That's the horizontal velocity, not the time. t = s_H ÷ v_H.", "working": working},
    ]
    return _with_projectile_widget(make_question(question, float(correct), options_data, "s",
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level))


def gen_projectile_harder(level="N5"):
    """A more demanding combined question: height and range are given, and the
    horizontal velocity must be found — the reverse direction of gen_find_time_from_range
    and gen_find_height combined, mirroring the worksheet's hardest Section 2 question."""
    height = random.choice([x for x in range(20, 100, 2)])
    t = round(math.sqrt(2 * height / G), 2)
    v_y = round(G * t, 2)
    rng = random.randint(10, 40) * 5
    correct = round(rng / t, 2)

    working = [
        {"type": "text",  "content": "Step 1: find the time of fall from the height, using the v-t graph."},
        {"type": "latex", "content": r"\text{height} = \tfrac{1}{2} a t^2 \;\Rightarrow\; t = \sqrt{\dfrac{2 \times \text{height}}{a}}"},
        {"type": "latex", "content": rf"t = \sqrt{{\dfrac{{2 \times {height}}}{{9.8}}}} = {t}\ \mathrm{{s}}"},
        {"type": "text",  "content": "Step 2: use the time and the range to find the horizontal velocity."},
        {"type": "latex", "content": r"s_H = v_H t \;\Rightarrow\; v_H = \dfrac{s_H}{t}"},
        {"type": "latex", "content": rf"v_H = \dfrac{{{rng}}}{{{t}}} = {correct}\ \mathrm{{m/s}}"},
    ]
    scaffold = [
        {"question": "Calculate the time taken to fall.", "answer": float(t), "unit": "s"},
        {"question": "Calculate the horizontal velocity.", "answer": float(correct), "unit": "m/s"},
    ]
    question = (
        f"A cannonball is fired horizontally from a cliff-top. It falls a height of {height} m before "
        f"landing in the sea, at a horizontal distance of {rng} m from the base of the cliff.\n\n"
        f"Calculate the horizontal velocity at which the cannonball was fired."
    )
    options_data = [
        {"value": float(correct),        "display": f"{correct} m/s",        "summary": "Correct!", "mistake": None, "working": working},
        {"value": round(rng * t, 2),     "display": f"{round(rng * t, 2)} m/s", "summary": "Incorrect.", "mistake": "You multiplied the range and the time instead of dividing. v_H = s_H ÷ t.", "working": working},
        {"value": float(v_y),            "display": f"{v_y} m/s",            "summary": "Incorrect.", "mistake": "That's the vertical velocity, not the horizontal velocity. First find t from the height, then use v_H = s_H ÷ t.", "working": working},
        {"value": round(rng / v_y, 2),   "display": f"{round(rng / v_y, 2)} m/s", "summary": "Incorrect.", "mistake": "You divided the range by the vertical velocity instead of the time of fall. Find t first, then v_H = s_H ÷ t.", "working": working},
    ]
    return _with_projectile_widget(make_question(question, float(correct), options_data, "m/s", scaffold=scaffold,
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level))


_ALL_GENS = [gen_find_range, gen_find_vertical_velocity, gen_find_height, gen_find_time_from_range, gen_projectile_harder]


def generate_projectiles(level="N5"):
    return random.choice(_ALL_GENS)(level=level)


# ── Vertical motion: free fall from rest, no horizontal component ───────────
# A simpler precursor to full projectile motion — same relationships as above
# (a = (v − u) ÷ t for velocity, v-t graph area for height fallen), but with
# nothing launched sideways. Covers both directions the worksheet drills:
# time given -> velocity/height, and height/velocity given -> the other one.

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
        {"type": "latex", "content": r"a = \dfrac{v - u}{t}"},
        {"type": "latex", "content": rf"9.8 = \dfrac{{v - 0}}{{{t}}}"},
        {"type": "latex", "content": rf"v = 9.8 \times {t} = {correct}\ \mathrm{{m/s}}"},
    ]
    question = f"{context} It takes {t} s to reach the ground.\n\nCalculate its velocity just before it hits the ground."
    options_data = [
        {"value": float(correct),  "display": f"{correct} m/s",       "mistake": None, "working": working},
        {"value": float(t),        "display": f"{t} m/s",             "mistake": "That's just the time of fall — you still need to multiply by g. Use a = (v − u) ÷ t.", "working": working},
        {"value": round(t / G, 3), "display": f"{round(t / G, 3)} m/s", "mistake": "You divided by g instead of multiplying. Rearrange a = (v − u) ÷ t to v = a × t.", "working": working},
        {"value": round(0.5 * G * t ** 2, 2), "display": f"{round(0.5 * G * t ** 2, 2)} m/s",
         "mistake": "That's the height fallen (the area under the v-t graph), not the velocity. Use a = (v − u) ÷ t for the final velocity.", "working": working},
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
        {"type": "text",  "content": "Step 1: find the time of fall from the height, using the v-t graph."},
        {"type": "latex", "content": r"\text{height} = \tfrac{1}{2} a t^2 \;\Rightarrow\; t = \sqrt{\dfrac{2 \times \text{height}}{a}}"},
        {"type": "latex", "content": rf"t = \sqrt{{\dfrac{{2 \times {height}}}{{9.8}}}} = {t}\ \mathrm{{s}}"},
        {"type": "text",  "content": "Step 2: use a = (v − u) ÷ t to find the final velocity."},
        {"type": "latex", "content": rf"v = 9.8 \times {t} = {correct}\ \mathrm{{m/s}}"},
    ]
    question = f"{context} It falls a height of {height} m.\n\nCalculate its velocity just before it hits the ground."
    forgot_sqrt = round(G * (2 * height / G), 2)
    options_data = [
        {"value": float(correct),   "display": f"{correct} m/s",   "mistake": None, "working": working},
        {"value": float(height),    "display": f"{height} m/s",    "mistake": "That's just the height fallen, not the velocity — first find the time of fall, then use a = (v − u) ÷ t.", "working": working},
        {"value": float(t),         "display": f"{t} m/s",         "mistake": "That's the time of fall, not the velocity — you still need a = (v − u) ÷ t.", "working": working},
        {"value": round(forgot_sqrt, 2), "display": f"{round(forgot_sqrt, 2)} m/s",
         "mistake": "Check your rearrangement — you need to take the square root to find t before using a = (v − u) ÷ t.", "working": working},
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


def gen_free_fall_height_from_time(level="N5"):
    context = random.choice(_FREEFALL_CONTEXTS)
    t_mult = random.choice([x for x in range(2, 21) if x != 10])
    t = round(t_mult * 0.1, 1)
    v = round(G * t, 2)
    correct = round(0.5 * t * v, 3)

    working = [
        {"type": "text",  "content": "Falling from rest, so the initial velocity is 0."},
        {"type": "latex", "content": rf"a = \dfrac{{v - u}}{{t}} \;\Rightarrow\; v = 9.8 \times {t} = {v}\ \mathrm{{m/s}}"},
        {"type": "text",  "content": "The height fallen is the area under the v-t graph (a triangle)."},
        {"type": "latex", "content": rf"\text{{height}} = \tfrac{{1}}{{2}} \times {t} \times {v} = {correct}\ \mathrm{{m}}"},
    ]
    scaffold = [
        {"question": "Calculate the final velocity.", "answer": float(v), "unit": "m/s"},
        {"question": "Use the v-t graph (triangle area) to find the height fallen.", "answer": float(correct), "unit": "m"},
    ]
    question = f"{context} It takes {t} s to reach the ground.\n\nCalculate the height from which it fell."
    forgot_half = round(t * v, 3)
    options_data = [
        {"value": float(correct),   "display": f"{correct} m", "mistake": None, "working": working},
        {"value": forgot_half,      "display": f"{forgot_half} m", "mistake": "You forgot the ½ factor. The area of the triangle on the v-t graph is ½ × base × height = ½ × t × v.", "working": working},
        {"value": float(v),         "display": f"{v} m",       "mistake": "That's the velocity, not the height. Use it as the graph height and find the triangle's area.", "working": working},
        {"value": float(t),         "display": f"{t} m",       "mistake": "That's the time of fall, not the height. Sketch the v-t graph and find the area under it.", "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return make_question(question, float(correct), options_data, "m", scaffold=scaffold,
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level)


def gen_free_fall_height_from_velocity(level="N5"):
    context = random.choice(_FREEFALL_CONTEXTS)
    t_mult = random.choice([x for x in range(5, 41) if x != 10])
    t = round(t_mult * 0.1, 1)
    v = round(G * t, 2)
    correct = round(0.5 * t * v, 3)

    working = [
        {"type": "text",  "content": "Use a = (v − u) ÷ t to find the time of fall first."},
        {"type": "latex", "content": rf"t = \dfrac{{v - u}}{{a}} = \dfrac{{{v}}}{{9.8}} = {t}\ \mathrm{{s}}"},
        {"type": "text",  "content": "The height fallen is the area under the v-t graph (a triangle)."},
        {"type": "latex", "content": rf"\text{{height}} = \tfrac{{1}}{{2}} \times {t} \times {v} = {correct}\ \mathrm{{m}}"},
    ]
    scaffold = [
        {"question": "Calculate the time of fall.", "answer": float(t), "unit": "s"},
        {"question": "Use the v-t graph (triangle area) to find the height fallen.", "answer": float(correct), "unit": "m"},
    ]
    question = f"{context} It hits the ground with a velocity of {v} m/s.\n\nCalculate the height from which it fell."
    forgot_half = round(t * v, 3)
    options_data = [
        {"value": float(correct),   "display": f"{correct} m", "mistake": None, "working": working},
        {"value": forgot_half,      "display": f"{forgot_half} m", "mistake": "You forgot the ½ factor. The area of the triangle on the v-t graph is ½ × base × height = ½ × t × v.", "working": working},
        {"value": float(v),         "display": f"{v} m",       "mistake": "That's the velocity, not the height. First find the time of fall using a = (v − u) ÷ t.", "working": working},
        {"value": float(t),         "display": f"{t} m",       "mistake": "That's the time of fall, not the height. Sketch the v-t graph and find the area under it.", "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return make_question(question, float(correct), options_data, "m", scaffold=scaffold,
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level)


def gen_free_fall_height(level="N5"):
    return random.choice([gen_free_fall_height_from_time, gen_free_fall_height_from_velocity])(level=level)


# ── Explaining projectile motion (qualitative, no calculation) ──────────────

_MASS_TIME_CASES = [
    ("increased",  "stay the same",
     "The acceleration due to gravity does not depend on mass, so a heavier and a lighter object fall at "
     "the same rate from the same height (ignoring air resistance)."),
]

_HORIZ_TIME_CASES = [
    ("increased",  "stay the same",
     "The horizontal and vertical motions are independent, so the time to fall depends only on the height "
     "and g, not on the horizontal velocity."),
]


def gen_projectile_time_explain(level="N5"):
    """Matches worksheet Section 3: does changing mass, or horizontal velocity,
    change the time a projectile takes to hit the ground? (It never does — the
    two motions are independent and g doesn't depend on mass.)"""
    kind = random.choice(["mass", "horizontal_velocity"])
    if kind == "mass":
        change, answer_key, reason = random.choice(_MASS_TIME_CASES)
        question_text = (
            "A projectile is launched horizontally. If the mass of the projectile were "
            f"{change}, with everything else unchanged, what would happen to the time it "
            "takes to hit the ground?"
        )
    else:
        change, answer_key, reason = random.choice(_HORIZ_TIME_CASES)
        question_text = (
            "A projectile is launched horizontally. If its horizontal velocity were "
            f"{change}, with the height of launch unchanged, what would happen to the time "
            "it takes to hit the ground?"
        )

    working = [{"type": "text", "content": reason}]
    correct = "Stay the same"
    distractor_texts = ["Increase", "Decrease"]

    options = [correct] + distractor_texts
    random.shuffle(options)

    from core.models.question_model import PhysicsQuestion
    distractors = [
        {"value": text, "mistake": reason, "working": working}
        for text in distractor_texts
    ]

    return PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        distractors=distractors,
        working=working,
        notes=NOTES["projectiles"],
        topic="Dynamics",
        question_type="Projectile Motion",
        level=level,
        metadata={"type": "classification", "options": options},
    )
