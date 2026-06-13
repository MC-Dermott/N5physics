import random
from utils.make_question import make_question
from utils.notes import NOTES

_VOLUME_UNITS = ["cm³", "mm³", "mL", "L"]


def _c_to_k(c):
    return c + 273


def _random_volume():
    unit = random.choice(_VOLUME_UNITS)
    if unit == "L":
        value = random.randint(1, 50)
    elif unit in ("mL", "cm³"):
        value = random.randint(50, 500)
    else:
        value = random.randint(100, 500)
    return value, unit


def gen_boyles(level="N5"):
    while True:
        p1 = random.randint(50, 180)
        multiplier = random.choice([2, 3, 4])
        p2 = p1 * multiplier
        if p2 <= 200:
            v1, unit = _random_volume()
            v2 = int((p1 * v1) / p2)
            if 1 <= v2 <= 500:
                break

    wrong_flip = int(v1 * p2 / p1)

    working = [
        {"type": "latex", "content": r"P_1V_1=P_2V_2"},
        {"type": "latex", "content": rf"{p1} \times {v1} = {p2} \times V_2"},
        {"type": "latex", "content": rf"V_2 = \frac{{{p1} \times {v1}}}{{{p2}}}"},
        {"type": "latex", "content": rf"V_2 = {v2}\ \mathrm{{{unit}}}"},
    ]
    question = (
        f"A gas has a volume of {v1} {unit} at a pressure of {p1} kPa. "
        f"The pressure changes to {p2} kPa at constant temperature.\n\n"
        f"Calculate the new volume."
    )
    options_data = [
        {"value": float(v2),      "display": f"{v2} {unit}",      "summary": "Correct!",   "mistake": None, "working": working},
        {"value": float(wrong_flip), "display": f"{wrong_flip} {unit}", "summary": "Incorrect.", "mistake": "You rearranged Boyle's Law incorrectly — when pressure increases, volume decreases. V₂ = P₁V₁ ÷ P₂.", "working": working},
        {"value": float(p1),      "display": f"{p1} kPa",         "summary": "Incorrect.", "mistake": "You gave the original pressure, not the new volume. Use P₁V₁ = P₂V₂ and solve for V₂.", "working": working},
        {"value": float(v1),      "display": f"{v1} {unit}",      "summary": "Incorrect.", "mistake": "The volume changes when pressure changes. Apply P₁V₁ = P₂V₂ to find the new volume.", "working": working},
    ]
    return make_question(question, float(v2), options_data, unit,
                         notes=NOTES["gas_laws"], topic="Properties", question_type="Gas Laws", level=level)


def gen_charles(level="N5"):
    while True:
        v1, unit = _random_volume()
        t1_c = random.randint(0, 50)
        t2_c = random.randint(60, 200)
        t1_k = _c_to_k(t1_c)
        t2_k = _c_to_k(t2_c)
        v2 = int(v1 * t2_k / t1_k)
        if 1 <= v2 <= 500:
            break

    wrong_no_kelvin = int(v1 * t2_c / t1_c) if t1_c != 0 else v2 + 50
    wrong_subtract  = abs(int(v1 * (t2_c - 273) / (t1_c - 273)))
    wrong_rearrange = int(v1 * t1_k / t2_k)

    working = [
        {"type": "text",  "content": "Convert temperatures to kelvin first."},
        {"type": "latex", "content": rf"T_1 = {t1_c} + 273 = {t1_k}\ \mathrm{{K}}"},
        {"type": "latex", "content": rf"T_2 = {t2_c} + 273 = {t2_k}\ \mathrm{{K}}"},
        {"type": "latex", "content": r"\frac{V_1}{T_1}=\frac{V_2}{T_2}"},
        {"type": "latex", "content": rf"\frac{{{v1}}}{{{t1_k}}}=\frac{{V_2}}{{{t2_k}}}"},
        {"type": "latex", "content": rf"V_2 = {v2}\ \mathrm{{{unit}}}"},
    ]
    scaffold = [
        {"question": f"Convert T₁ = {t1_c} °C to kelvin.", "answer": float(t1_k), "unit": "K"},
        {"question": f"Convert T₂ = {t2_c} °C to kelvin.", "answer": float(t2_k), "unit": "K"},
        {"question": "Calculate the new volume.", "answer": float(v2), "unit": unit},
    ]
    question = (
        f"A gas occupies {v1} {unit} at {t1_c} °C. "
        f"The temperature increases to {t2_c} °C at constant pressure.\n\n"
        f"Calculate the new volume."
    )
    options_data = [
        {"value": float(v2),             "display": f"{v2} {unit}",             "summary": "Correct!",   "mistake": None, "working": working},
        {"value": float(wrong_no_kelvin), "display": f"{wrong_no_kelvin} {unit}", "summary": "Incorrect.", "mistake": f"You used Celsius temperatures directly. Convert to kelvin first: T = °C + 273.", "working": working},
        {"value": float(wrong_subtract),  "display": f"{wrong_subtract} {unit}", "summary": "Incorrect.", "mistake": "You subtracted 273 instead of adding it. T(K) = T(°C) + 273.", "working": working},
        {"value": float(wrong_rearrange), "display": f"{wrong_rearrange} {unit}", "summary": "Incorrect.", "mistake": "You rearranged Charles' Law incorrectly. V₂ = V₁ × T₂ ÷ T₁.", "working": working},
    ]
    return make_question(question, float(v2), options_data, unit, scaffold=scaffold,
                         notes=NOTES["gas_laws"], topic="Properties", question_type="Gas Laws", level=level)


def gen_gaylussac(level="N5"):
    while True:
        p1 = random.randint(50, 150)
        t1_c = random.randint(0, 50)
        t2_c = random.randint(60, 200)
        t1_k = _c_to_k(t1_c)
        t2_k = _c_to_k(t2_c)
        p2 = int(p1 * t2_k / t1_k)
        if 1 <= p2 <= 200:
            break

    wrong_no_kelvin = int(p1 * t2_c / t1_c) if t1_c != 0 else p2 + 20
    wrong_subtract  = abs(int(p1 * (t2_c - 273) / (t1_c - 273)))
    wrong_rearrange = int(p1 * t1_k / t2_k)

    working = [
        {"type": "text",  "content": "Convert temperatures to kelvin first."},
        {"type": "latex", "content": rf"T_1 = {t1_c} + 273 = {t1_k}\ \mathrm{{K}}"},
        {"type": "latex", "content": rf"T_2 = {t2_c} + 273 = {t2_k}\ \mathrm{{K}}"},
        {"type": "latex", "content": r"\frac{P_1}{T_1}=\frac{P_2}{T_2}"},
        {"type": "latex", "content": rf"\frac{{{p1}}}{{{t1_k}}}=\frac{{P_2}}{{{t2_k}}}"},
        {"type": "latex", "content": rf"P_2 = {p2}\ \mathrm{{kPa}}"},
    ]
    scaffold = [
        {"question": f"Convert T₁ = {t1_c} °C to kelvin.", "answer": float(t1_k), "unit": "K"},
        {"question": f"Convert T₂ = {t2_c} °C to kelvin.", "answer": float(t2_k), "unit": "K"},
        {"question": "Calculate the new pressure.", "answer": float(p2), "unit": "kPa"},
    ]
    question = (
        f"A gas is at a pressure of {p1} kPa at {t1_c} °C. "
        f"The temperature increases to {t2_c} °C at constant volume.\n\n"
        f"Calculate the new pressure."
    )
    options_data = [
        {"value": float(p2),             "display": f"{p2} kPa",             "summary": "Correct!",   "mistake": None, "working": working},
        {"value": float(wrong_no_kelvin), "display": f"{wrong_no_kelvin} kPa", "summary": "Incorrect.", "mistake": "You used Celsius temperatures directly. Convert to kelvin first: T = °C + 273.", "working": working},
        {"value": float(wrong_subtract),  "display": f"{wrong_subtract} kPa", "summary": "Incorrect.", "mistake": "You subtracted 273 instead of adding it. T(K) = T(°C) + 273.", "working": working},
        {"value": float(wrong_rearrange), "display": f"{wrong_rearrange} kPa", "summary": "Incorrect.", "mistake": "You rearranged Gay-Lussac's Law incorrectly. P₂ = P₁ × T₂ ÷ T₁.", "working": working},
    ]
    return make_question(question, float(p2), options_data, "kPa", scaffold=scaffold,
                         notes=NOTES["gas_laws"], topic="Properties", question_type="Gas Laws", level=level)


_ALL_GENS = [gen_boyles, gen_charles, gen_gaylussac]


def generate_gas_laws(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
