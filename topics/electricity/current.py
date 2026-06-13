import random
from utils.make_question import make_question
from utils.notes import NOTES


def gen_current(level="N5"):
    charge = random.randint(10, 100)
    use_min = random.choice([True, False]) if level != "N4" else False
    if use_min:
        t_val, t_sec, t_label = random.randint(1, 10), 0, "minutes"
        t_val = random.randint(1, 10)
        t_sec = t_val * 60
    else:
        t_val = random.randint(5, 60)
        t_sec = t_val
        t_label = "seconds"

    correct = round(charge / t_sec, 2)
    conversion_d = round(charge / t_val, 2)

    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"I = \frac{Q}{t}"},
        {"type": "latex", "content": rf"I = \frac{{{charge}}}{{{t_sec}}}"},
        {"type": "latex", "content": rf"I = {correct}\ \mathrm{{A}}"},
    ]
    question = f"What is the current flowing if {charge} C of charge passes in {t_val} {t_label}?"
    options_data = [
        {"value": correct,          "summary": "Correct!", "mistake": None, "working": working},
        {"value": charge * t_sec,   "summary": "Incorrect.", "mistake": "You multiplied Q × t instead of dividing. I = Q ÷ t.", "working": working},
        {"value": round(t_sec / charge, 2), "summary": "Incorrect.", "mistake": "You divided t by Q instead of Q by t. I = Q ÷ t.", "working": working},
        {"value": conversion_d,     "summary": "Incorrect.", "mistake": "You did not convert the time into seconds.", "working": working},
    ]
    return make_question(question, correct, options_data, "A", notes=NOTES["electricity_current"],
                         topic="Electricity", question_type="Current", level=level)


def gen_charge(level="N5"):
    current = random.randint(1, 10)
    use_min = random.choice([True, False]) if level != "N4" else False
    if use_min:
        t_val = random.randint(1, 10)
        t_sec = t_val * 60
        t_label = "minutes"
    else:
        t_val = random.randint(5, 60)
        t_sec = t_val
        t_label = "seconds"

    correct = round(current * t_sec, 2)
    conversion_d = round(current * t_val, 2)

    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"Q = It"},
        {"type": "latex", "content": rf"Q = {current} \times {t_sec}"},
        {"type": "latex", "content": rf"Q = {correct}\ \mathrm{{C}}"},
    ]
    question = f"What is the total charge transferred if a current of {current} A flows for {t_val} {t_label}?"
    options_data = [
        {"value": correct,                     "summary": "Correct!", "mistake": None, "working": working},
        {"value": round(current / t_sec, 2),   "summary": "Incorrect.", "mistake": "You divided I by t instead of multiplying. Q = I × t.", "working": working},
        {"value": round(t_sec / current, 2),   "summary": "Incorrect.", "mistake": "You rearranged Q = It incorrectly.", "working": working},
        {"value": conversion_d,                "summary": "Incorrect.", "mistake": "You forgot to convert time to seconds.", "working": working},
    ]
    return make_question(question, correct, options_data, "C", notes=NOTES["electricity_current"],
                         topic="Electricity", question_type="Current", level=level)


def gen_time(level="N5"):
    charge  = random.randint(10, 100)
    current = random.randint(1, 10)
    correct = round(charge / current, 2)

    working = [
        {"type": "text",  "content": "Rearrange the equation:"},
        {"type": "latex", "content": r"t = \frac{Q}{I}"},
        {"type": "latex", "content": rf"t = \frac{{{charge}}}{{{current}}}"},
        {"type": "latex", "content": rf"t = {correct}\ \mathrm{{s}}"},
    ]
    question = f"For how long must a current of {current} A flow to transfer {charge} C?"
    options_data = [
        {"value": correct,              "summary": "Correct!", "mistake": None, "working": working},
        {"value": charge * current,     "summary": "Incorrect.", "mistake": "You multiplied Q × I instead of dividing. t = Q ÷ I.", "working": working},
        {"value": round(current / charge, 2), "summary": "Incorrect.", "mistake": "You divided I by Q. t = Q ÷ I.", "working": working},
        {"value": round(correct / 60, 2),     "summary": "Incorrect.", "mistake": "You converted to minutes incorrectly — the answer should be in seconds.", "working": working},
    ]
    return make_question(question, correct, options_data, "s", notes=NOTES["electricity_current"],
                         topic="Electricity", question_type="Current", level=level)


_N4_GENS  = [gen_current, gen_charge]
_ALL_GENS = [gen_current, gen_charge, gen_time]


def generate_current(level="N5"):
    gens = _N4_GENS if level == "N4" else _ALL_GENS
    return random.choice(gens)(level=level)
