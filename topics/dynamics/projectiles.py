import random
from utils.make_question import make_question
from utils.notes import NOTES

G = 9.8


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
    return make_question(question, float(correct), options_data, "m",
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level)


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
    return make_question(question, float(correct), options_data, "m/s",
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level)


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
    return make_question(question, float(correct), options_data, "m", scaffold=scaffold,
                         notes=NOTES["projectiles"], topic="Dynamics", question_type="Projectile Motion", level=level)


_ALL_GENS = [gen_find_range, gen_find_vertical_velocity, gen_find_height]


def generate_projectiles(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
