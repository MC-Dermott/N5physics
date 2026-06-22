import random
from utils.make_question import make_question

_NOTES = """
## Electrical Power

$$P = \\frac{E}{t}$$

| Symbol | Quantity | Unit |
|---|---|---|
| P | Power | W (watts) |
| E | Energy | J (joules) |
| t | Time | s (seconds) |

> **Power rating** — the energy transferred per second.
> A 1000 W appliance uses 1000 J of electrical energy every second.

**Rearrangements:**
$$E = P \\times t \\qquad t = \\frac{E}{P}$$
"""

# All powers are multiples of 100 so E = P×t stays a clean integer.
_APPLIANCES = [
    ("electric kettle",   1600),
    ("electric kettle",   2000),
    ("hair dryer",        1200),
    ("hair dryer",        2400),
    ("iron",              1000),
    ("iron",              2000),
    ("toaster",            800),
    ("toaster",           1200),
    ("microwave oven",     800),
    ("microwave oven",    1000),
    ("electric fire",     2000),
    ("electric fire",     3000),
    ("television",         100),
    ("television",         200),
    ("electric shower",   8000),
    ("fan heater",        1500),
    ("fan heater",        2000),
]

_TIMES = [30, 60, 90, 120, 150, 180, 240, 300, 360, 450, 600]


def _dedup(options_data, correct):
    correct_r = round(float(correct), 4)
    seen = {correct_r}
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


def gen_find_energy(level="N4"):
    appliance, P = random.choice(_APPLIANCES)
    t = random.choice(_TIMES)
    E = P * t
    working = [
        {"type": "text",  "content": "Rearrange P = E/t for E:"},
        {"type": "latex", "content": r"E = P \times t"},
        {"type": "latex", "content": rf"E = {P} \times {t}"},
        {"type": "latex", "content": rf"E = {E}\ \mathrm{{J}}"},
    ]
    options_data = [
        {"value": E,               "mistake": None,                                                "working": working},
        {"value": round(P / t, 4), "mistake": "Use E = P × t — do not divide P by t.",            "working": working},
        {"value": P + t,           "mistake": "Multiply P and t — do not add them.",               "working": working},
        {"value": round(t / P, 6), "mistake": "Use E = P × t — power is the larger quantity here.", "working": working},
    ]
    return make_question(
        f"An {appliance} has a power rating of {P} W. "
        f"It is switched on for {t} seconds. "
        f"Calculate how much electrical energy is supplied in this time.",
        E, _dedup(options_data, E), "J",
        notes=_NOTES, topic="Electricity and Energy",
        question_type="Electrical Power", level=level,
    )


def gen_find_power(level="N4"):
    appliance, P = random.choice(_APPLIANCES)
    t = random.choice(_TIMES)
    E = P * t
    working = [
        {"type": "text",  "content": "Use P = E/t:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "latex", "content": rf"P = \frac{{{E}}}{{{t}}}"},
        {"type": "latex", "content": rf"P = {P}\ \mathrm{{W}}"},
    ]
    options_data = [
        {"value": P,               "mistake": None,                                             "working": working},
        {"value": E * t,           "mistake": "Use P = E ÷ t — do not multiply E by t.",       "working": working},
        {"value": round(t / E, 6), "mistake": "Use P = E ÷ t — divide E by t, not t by E.",   "working": working},
        {"value": P * 2,           "mistake": "Check your calculation — P = E ÷ t.",            "working": working},
    ]
    return make_question(
        f"An {appliance} uses {E} J of electrical energy in {t} seconds. "
        f"Calculate the power rating of the {appliance}.",
        P, _dedup(options_data, P), "W",
        notes=_NOTES, topic="Electricity and Energy",
        question_type="Electrical Power", level=level,
    )


def gen_find_time(level="N4"):
    appliance, P = random.choice(_APPLIANCES)
    t = random.choice(_TIMES)
    E = P * t
    working = [
        {"type": "text",  "content": "Rearrange P = E/t for t:"},
        {"type": "latex", "content": r"t = \frac{E}{P}"},
        {"type": "latex", "content": rf"t = \frac{{{E}}}{{{P}}}"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t,               "mistake": None,                                             "working": working},
        {"value": E * P,           "mistake": "Use t = E ÷ P — do not multiply E by P.",       "working": working},
        {"value": round(P / E, 6), "mistake": "Use t = E ÷ P — divide E by P, not P by E.",   "working": working},
        {"value": t * 2,           "mistake": "Check your calculation — t = E ÷ P.",            "working": working},
    ]
    return make_question(
        f"An {appliance} has a power rating of {P} W. "
        f"How long does it take the {appliance} to use {E} J of electrical energy?",
        t, _dedup(options_data, t), "s",
        notes=_NOTES, topic="Electricity and Energy",
        question_type="Electrical Power", level=level,
    )


_ALL_GENS = [gen_find_energy, gen_find_power, gen_find_time]


def generate_electrical_power(level="N4"):
    return random.choice(_ALL_GENS)(level=level)
