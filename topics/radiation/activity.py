import random
from utils.make_question import make_question
from utils.notes import NOTES


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def fmt_activity(a):
    a = float(a)
    if abs(a) >= 1_000_000:
        return f"{a / 1_000_000:g} MBq"
    if abs(a) >= 1000:
        return f"{a / 1000:g} kBq"
    return f"{a:g} Bq"


_SOURCES = [
    "A radioactive source",
    "A sample of a radioactive isotope",
    "A radioactive material",
    "A radioisotope",
]


def _pick_a_and_t():
    A_si = random.choice([10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000])
    mode = random.choice(["s", "s", "minutes"])
    if mode == "minutes":
        t_min = random.choice([1, 2, 3, 5, 10, 15, 20])
        return A_si, t_min, "minutes", t_min * 60
    t_si = random.choice([5, 10, 20, 25, 30, 40, 50, 60, 100, 120, 200])
    return A_si, t_si, "s", t_si


def gen_act_find_a(level="N5"):
    A_si, t_disp, t_unit, t_si = _pick_a_and_t()
    N = A_si * t_si
    correct = float(A_si)

    multiplied = round_sf(N * t_si)
    inverted   = round_sf(t_si / N)

    if t_unit != "s":
        prefix_err = round_sf(N / t_disp)
        prefix_msg = (
            f"You used t = {t_disp} without converting from {t_unit} to seconds. "
            f"{t_disp} {t_unit} = {t_si} s."
        )
    else:
        prefix_err = round_sf(N * t_si)
        prefix_msg = "You multiplied N × t instead of dividing. A = N ÷ t."

    steps = [
        {"type": "text", "content": "Use the equation:"},
        {"type": "latex", "content": r"A = \frac{N}{t}"},
    ]
    if t_unit != "s":
        steps.append({"type": "latex", "content": rf"t = {t_disp}\ \mathrm{{{t_unit}}} = {t_si}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"A = \frac{{{N}}}{{{t_si}}}"},
        {"type": "latex", "content": rf"A = {fmt_activity(correct)}"},
    ]

    src = random.choice(_SOURCES)
    question = f"{src} produces {N} nuclear decays in {t_disp} {t_unit}.\n\nCalculate the activity."
    options_data = [
        {"value": correct,    "display": fmt_activity(correct),    "summary": "Correct!",   "mistake": None,       "working": steps},
        {"value": multiplied, "display": fmt_activity(multiplied), "summary": "Incorrect.", "mistake": "You multiplied N × t instead of dividing. A = N ÷ t.",   "working": steps},
        {"value": inverted,   "display": fmt_activity(inverted),   "summary": "Incorrect.", "mistake": "You divided t by N instead of N by t. A = N ÷ t.",       "working": steps},
        {"value": prefix_err, "display": fmt_activity(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg, "working": steps},
    ]
    return make_question(question, correct, options_data, "Bq", notes=NOTES["radiation_activity"],
                         topic="Radiation", question_type="Activity", level=level)


def gen_act_find_n(level="N5"):
    A_si, t_disp, t_unit, t_si = _pick_a_and_t()
    N = A_si * t_si
    correct = float(N)

    divided  = round_sf(A_si / t_si)
    inverted = round_sf(t_si / A_si)

    if t_unit != "s":
        prefix_err = round_sf(A_si * t_disp)
        prefix_msg = (
            f"You used t = {t_disp} without converting from {t_unit} to seconds. "
            f"{t_disp} {t_unit} = {t_si} s."
        )
    else:
        prefix_err = round_sf(A_si / t_si)
        prefix_msg = "You divided A by t instead of multiplying. N = A × t."

    steps = [
        {"type": "text", "content": "Rearrange A = N/t to find N:"},
        {"type": "latex", "content": r"N = At"},
    ]
    if t_unit != "s":
        steps.append({"type": "latex", "content": rf"t = {t_disp}\ \mathrm{{{t_unit}}} = {t_si}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"N = {A_si} \times {t_si}"},
        {"type": "latex", "content": rf"N = {int(correct)}\ \mathrm{{decays}}"},
    ]

    src = random.choice(_SOURCES)
    question = f"{src} has an activity of {fmt_activity(A_si)} and is observed for {t_disp} {t_unit}.\n\nCalculate the number of nuclear decays."
    options_data = [
        {"value": correct,    "display": f"{int(correct)}",        "summary": "Correct!",   "mistake": None,       "working": steps},
        {"value": divided,    "display": f"{round_sf(divided)}",   "summary": "Incorrect.", "mistake": "You divided A by t instead of multiplying. N = A × t.", "working": steps},
        {"value": inverted,   "display": f"{round_sf(inverted)}",  "summary": "Incorrect.", "mistake": "You divided t by A. N = A × t.",                        "working": steps},
        {"value": prefix_err, "display": f"{round_sf(prefix_err)}","summary": "Incorrect.", "mistake": prefix_msg, "working": steps},
    ]
    return make_question(question, correct, options_data, "decays", notes=NOTES["radiation_activity"],
                         topic="Radiation", question_type="Activity", level=level)


def gen_act_find_t(level="N5"):
    A_si = random.choice([10, 20, 50, 100, 200, 500, 1000, 2000, 5000])
    t_si = random.choice([5, 10, 20, 25, 30, 40, 50, 60, 100, 120, 200])
    N = A_si * t_si
    correct = float(t_si)

    multiplied = round_sf(N * A_si)
    inverted   = round_sf(A_si / N)
    prefix_err = round_sf(N * A_si / 1000)

    steps = [
        {"type": "text", "content": "Rearrange A = N/t to find t:"},
        {"type": "latex", "content": r"t = \frac{N}{A}"},
        {"type": "latex", "content": rf"t = \frac{{{N}}}{{{A_si}}}"},
        {"type": "latex", "content": rf"t = {correct}\ \mathrm{{s}}"},
    ]

    src = random.choice(_SOURCES)
    question = f"{src} has an activity of {fmt_activity(A_si)} and produces {N} nuclear decays.\n\nCalculate the time over which the decays occurred."
    options_data = [
        {"value": correct,    "display": f"{correct} s",    "summary": "Correct!",   "mistake": None,
         "working": steps},
        {"value": multiplied, "display": f"{multiplied} s", "summary": "Incorrect.", "mistake": "You multiplied N × A instead of dividing. t = N ÷ A.", "working": steps},
        {"value": inverted,   "display": f"{inverted} s",   "summary": "Incorrect.", "mistake": "You divided A by N instead of N by A. t = N ÷ A.",     "working": steps},
        {"value": prefix_err, "display": f"{prefix_err} s", "summary": "Incorrect.", "mistake": "Check your rearrangement — t = N ÷ A.",                "working": steps},
    ]
    return make_question(question, correct, options_data, "s", notes=NOTES["radiation_activity"],
                         topic="Radiation", question_type="Activity", level=level)


_ALL_GENS = [gen_act_find_a, gen_act_find_n, gen_act_find_t]


def generate_activity(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
