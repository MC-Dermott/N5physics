import random
from utils.make_question import make_question
from utils.notes import NOTES

# (setup_sentence, blocker_label, width_name, width_lo_cm, width_hi_cm,
#  release_d_lo_m, release_d_hi_m, total_t_lo_s, total_t_hi_s, gate_t_lo_s, gate_t_hi_s)
_SETUPS = [
    ("A trolley with a {width_cm} cm wide card mounted on it is released from rest and rolls down a ramp, "
     "passing through a light gate.",
     "card", "width", 4.0, 10.0, 0.40, 1.60, 1.5, 3.5, 0.08, 0.20),
    ("A ball bearing of diameter {width_cm} cm is released from rest and rolls down a ramp, passing "
     "through a light gate.",
     "ball bearing", "diameter", 0.8, 2.0, 0.20, 0.60, 1.0, 2.5, 0.015, 0.04),
    ("A coin of diameter {width_cm} cm is dropped from rest and falls through a light gate.",
     "coin", "diameter", 1.8, 2.6, 0.30, 1.00, 0.25, 0.45, 0.010, 0.030),
]


def _draw_scenario():
    sentence, blocker, width_name, w_lo, w_hi, d_lo, d_hi, t_lo, t_hi, g_lo, g_hi = random.choice(_SETUPS)
    width_cm = round(random.uniform(w_lo, w_hi), 1)
    width_m = round(width_cm / 100, 4)
    setup_sentence = sentence.format(width_cm=width_cm)

    for _ in range(20):
        release_d = round(random.uniform(d_lo, d_hi), 2)
        total_t = round(random.uniform(t_lo, t_hi), 1)
        gate_t = round(random.uniform(g_lo, g_hi), 3)
        avg_speed = release_d / total_t
        inst_speed = width_m / gate_t
        if inst_speed > avg_speed * 1.2:  # accelerating from rest: instant speed at the end > average
            break
    return setup_sentence, blocker, width_name, width_cm, width_m, release_d, total_t, gate_t, avg_speed, inst_speed


def _round3(x):
    return float(f"{x:.3g}")


# ── Instantaneous speed at the light gate ───────────────────────────────────────

def gen_instantaneous_speed(level="S3"):
    setup_sentence, blocker, width_name, width_cm, width_m, release_d, total_t, gate_t, avg_speed, inst_speed = _draw_scenario()
    correct = _round3(inst_speed)
    using_average = _round3(avg_speed)
    forgot_conversion = _round3(width_cm / gate_t)  # forgot cm -> m
    swapped = _round3(gate_t / width_m)

    steps = [
        {"type": "text",  "content": f"Use the light gate's {blocker} {width_name} and blocking time, not the total distance/time:"},
        {"type": "latex", "content": r"v = \frac{\mathrm{width}}{\mathrm{light\ gate\ time}}"},
        {"type": "latex", "content": rf"v = \frac{{{width_m}}}{{{gate_t}}}"},
        {"type": "latex", "content": rf"v = {correct}\ \mathrm{{m/s}}"},
    ]

    question = (
        f"{setup_sentence} The release point is {release_d} m from the light gate, and it takes "
        f"{total_t} s to travel this distance. As it passes through the light gate, the {blocker} blocks "
        f"the beam for {gate_t} s.\n\n"
        f"Calculate the instantaneous speed as it passes through the light gate."
    )
    options_data = [
        {"value": correct, "display": f"{correct:g} m/s", "mistake": None, "working": steps},
        {"value": using_average, "display": f"{using_average:g} m/s",
         "mistake": "That's the average speed over the whole run (release point to gate) — it uses the "
                    "total distance and total time, not the light gate's own width and time. Since the "
                    "object accelerates, the instantaneous speed at the gate is different.",
         "working": steps},
        {"value": forgot_conversion, "display": f"{forgot_conversion:g} m/s",
         "mistake": f"You used the {width_name} in cm ({width_cm}) instead of converting it to metres first "
                    f"({width_m} m).",
         "working": steps},
        {"value": swapped, "display": f"{swapped:g} m/s",
         "mistake": f"You divided the light gate time by the {width_name} instead of the {width_name} by the time.",
         "working": steps},
    ]
    scaffold = [
        {"question": f"What is the {blocker} {width_name} in metres?", "answer": width_m},
        {"question": "What is the instantaneous speed at the light gate?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "m/s", scaffold=scaffold,
                         notes=NOTES["instantaneous_speed_s3"], topic="Dynamics",
                         question_type="Instantaneous Speed", level=level)


# ── Average speed over the whole run (for contrast with instantaneous speed) ───

def gen_average_speed_light_gate(level="S3"):
    setup_sentence, blocker, width_name, width_cm, width_m, release_d, total_t, gate_t, avg_speed, inst_speed = _draw_scenario()
    correct = _round3(avg_speed)
    using_gate = _round3(inst_speed)
    swapped = _round3(total_t / release_d)

    steps = [
        {"type": "text",  "content": "Use the total distance and total time for the whole run:"},
        {"type": "latex", "content": r"v = \frac{d}{t}"},
        {"type": "latex", "content": rf"v = \frac{{{release_d}}}{{{total_t}}}"},
        {"type": "latex", "content": rf"v = {correct}\ \mathrm{{m/s}}"},
    ]

    question = (
        f"{setup_sentence} The release point is {release_d} m from the light gate, and it takes "
        f"{total_t} s to travel this distance. As it passes through the light gate, the {blocker} blocks "
        f"the beam for {gate_t} s.\n\n"
        f"Calculate its average speed as it travels from the release point to the light gate."
    )
    options_data = [
        {"value": correct, "display": f"{correct:g} m/s", "mistake": None, "working": steps},
        {"value": using_gate, "display": f"{using_gate:g} m/s",
         "mistake": f"That's the instantaneous speed at the light gate ({width_name} ÷ gate time), not the "
                    "average speed over the whole run — use the total distance and total time instead.",
         "working": steps},
        {"value": swapped, "display": f"{swapped:g} m/s",
         "mistake": "You divided the total time by the total distance instead of distance by time.",
         "working": steps},
    ]
    return make_question(question, correct, options_data, "m/s", scaffold=None,
                         notes=NOTES["instantaneous_speed_s3"], topic="Dynamics",
                         question_type="Instantaneous Speed", level=level)


def generate_instantaneous_speed(level="S3"):
    return random.choice([gen_instantaneous_speed, gen_average_speed_light_gate])(level=level)
