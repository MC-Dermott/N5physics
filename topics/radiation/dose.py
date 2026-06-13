import random
from utils.make_question import make_question
from utils.notes import NOTES

RADIATION_TYPES = [
    {"name": "alpha radiation",  "w_R": 20},
    {"name": "beta radiation",   "w_R": 1},
    {"name": "gamma radiation",  "w_R": 1},
    {"name": "fast neutrons",    "w_R": 20},
    {"name": "slow neutrons",    "w_R": 3},
    {"name": "X-rays",           "w_R": 1},
]

D_OPTIONS    = [2, 4, 5, 8, 10, 20]
TIME_OPTIONS = [2, 4, 5, 10]

W_R_TABLE = (
    "| Type of radiation | Radiation weighting factor (w_R) |\n"
    "|---|---|\n"
    "| Alpha particles | 20 |\n"
    "| Beta particles | 1 |\n"
    "| Gamma rays | 1 |\n"
    "| Fast neutrons | 20 |\n"
    "| Slow neutrons | 3 |\n"
    "| X-rays | 1 |"
)


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def _pick_mass():
    mass_g  = random.choice(range(100, 5100, 100))
    mass_kg = mass_g / 1000
    if mass_g < 1000:
        return mass_g, "g", mass_kg, True, mass_g
    return mass_kg, "kg", mass_kg, False, mass_g


def _pick_values():
    rad = random.choice(RADIATION_TYPES)
    mass_display, mass_unit, mass_kg, is_grams, mass_g = _pick_mass()
    D = random.choice(D_OPTIONS)
    E = D * mass_kg
    t_h = random.choice(TIME_OPTIONS)
    H = D * rad["w_R"]
    dose_rate = H / t_h
    return rad, mass_display, mass_unit, mass_kg, is_grams, mass_g, D, E, t_h, H, dose_rate


def gen_find_D(level="N5"):
    rad, mass_display, mass_unit, mass_kg, is_grams, mass_g, D, E, t_h, H, dose_rate = _pick_values()
    mass_text = f"{mass_display} {mass_unit}"
    correct = round_sf(D)

    working = []
    if is_grams:
        working += [
            {"type": "text",  "content": "First convert the mass to kg:"},
            {"type": "latex", "content": rf"{mass_g}\ \mathrm{{g}} = {mass_kg}\ \mathrm{{kg}}"},
        ]
    working += [
        {"type": "text",  "content": "Use the absorbed dose equation:"},
        {"type": "latex", "content": r"D = \frac{E}{m}"},
        {"type": "latex", "content": rf"D = \frac{{{round_sf(E)}}}{{{mass_kg}}}"},
        {"type": "latex", "content": rf"D = {correct}\ \mathrm{{Gy}}"},
    ]
    question = (
        f"{W_R_TABLE}\n\n"
        f"A patient is exposed to {rad['name']}. "
        f"A mass of {mass_text} of tissue absorbs {round_sf(E)} J of energy.\n\n"
        f"Calculate the absorbed dose."
    )
    mult_err = round_sf(E * mass_kg)
    if is_grams:
        content_val  = round_sf(E / mass_g)
        content_msg  = f"You used the mass in grams ({mass_g} g) without converting to kg. {mass_g} g = {mass_kg} kg."
    else:
        content_val  = mult_err if round_sf(mult_err) != correct else round_sf(correct * 2)
        content_msg  = "You multiplied E × m instead of dividing. D = E ÷ m."

    options_data = [
        {"value": float(correct),      "display": f"{correct} Gy",   "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(H),         "display": f"{round_sf(H)} Sv", "summary": "Incorrect.", "mistake": f"This is the equivalent dose (Sv). Absorbed dose D = E ÷ m (unit: Gray).", "working": working},
        {"value": round_sf(E),         "display": f"{round_sf(E)} J",  "summary": "Incorrect.", "mistake": f"You gave the energy absorbed, not the absorbed dose. D = E ÷ m = {round_sf(E)} ÷ {mass_kg} = {correct} Gy.", "working": working},
        {"value": float(content_val),  "display": f"{content_val} Gy", "summary": "Incorrect.", "mistake": content_msg, "working": working},
    ]
    return make_question(question, float(correct), options_data, "Gy",
                         notes=NOTES["radiation_doses"], topic="Radiation", question_type="Dose", level=level)


def gen_find_H(level="N5"):
    rad, mass_display, mass_unit, mass_kg, is_grams, mass_g, D, E, t_h, H, dose_rate = _pick_values()
    w_R     = rad["w_R"]
    correct = round_sf(H)

    working = [
        {"type": "text",  "content": "Use the equivalent dose equation:"},
        {"type": "latex", "content": r"H = D w_R"},
        {"type": "latex", "content": rf"H = {D} \times {w_R}"},
        {"type": "latex", "content": rf"H = {correct}\ \mathrm{{Sv}}"},
    ]
    question = (
        f"{W_R_TABLE}\n\n"
        f"A patient receives an absorbed dose of {D} Gy from {rad['name']}.\n\n"
        f"Calculate the equivalent dose."
    )
    wrong_wRs = [x for x in [1, 3, 20] if x != w_R]
    wrong_wR_val = round_sf(D * wrong_wRs[0])
    div_err      = round_sf(D / w_R) if w_R != 1 else round_sf(D * 20)

    options_data = [
        {"value": float(correct),   "display": f"{correct} Sv",      "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(D),         "display": f"{D} Sv",            "summary": "Incorrect.", "mistake": f"You gave the absorbed dose (Gy) as the equivalent dose. H = D × w_R = {D} × {w_R} = {correct} Sv.", "working": working},
        {"value": float(div_err),   "display": f"{div_err} Sv",      "summary": "Incorrect.", "mistake": f"You divided D by w_R instead of multiplying. H = D × w_R.", "working": working},
        {"value": float(wrong_wR_val), "display": f"{wrong_wR_val} Sv", "summary": "Incorrect.", "mistake": f"You used the wrong radiation weighting factor. For {rad['name']}, w_R = {w_R}.", "working": working},
    ]
    return make_question(question, float(correct), options_data, "Sv",
                         notes=NOTES["radiation_doses"], topic="Radiation", question_type="Dose", level=level)


def gen_find_dose_rate(level="N5"):
    rad, mass_display, mass_unit, mass_kg, is_grams, mass_g, D, E, t_h, H, dose_rate = _pick_values()
    correct = round_sf(dose_rate)

    working = [
        {"type": "text",  "content": "Use the equivalent dose rate equation:"},
        {"type": "latex", "content": r"\dot{H} = \frac{H}{t}"},
        {"type": "latex", "content": rf"\dot{{H}} = \frac{{{round_sf(H)}}}{{{t_h}}}"},
        {"type": "latex", "content": rf"\dot{{H}} = {correct}\ \mathrm{{Sv/h}}"},
    ]
    question = (
        f"A worker receives an equivalent dose of {round_sf(H)} Sv over {t_h} hour{'s' if t_h > 1 else ''}.\n\n"
        f"Calculate the equivalent dose rate."
    )
    mult_err = round_sf(H * t_h)
    options_data = [
        {"value": float(correct),    "display": f"{correct} Sv/h",   "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(H),       "display": f"{round_sf(H)} Sv", "summary": "Incorrect.", "mistake": "You gave the equivalent dose (Sv), not the dose rate (Sv/h). Divide H by time: Ḣ = H ÷ t.", "working": working},
        {"value": float(mult_err),   "display": f"{mult_err} Sv/h",  "summary": "Incorrect.", "mistake": "You multiplied H × t instead of dividing. Dose rate Ḣ = H ÷ t.", "working": working},
        {"value": round_sf(1/correct) if correct > 0 else 0.0, "display": f"{round_sf(1/correct) if correct > 0 else 0} Sv/h", "summary": "Incorrect.", "mistake": "You inverted the equation. Ḣ = H ÷ t, not t ÷ H.", "working": working},
    ]
    return make_question(question, float(correct), options_data, "Sv/h",
                         notes=NOTES["radiation_doses"], topic="Radiation", question_type="Dose", level=level)


def gen_find_H_from_rate(level="N5"):
    rad, mass_display, mass_unit, mass_kg, is_grams, mass_g, D, E, t_h, H, dose_rate = _pick_values()
    correct = round_sf(H)

    working = [
        {"type": "text",  "content": "Rearrange Ḣ = H/t to find H:"},
        {"type": "latex", "content": r"H = \dot{H} \times t"},
        {"type": "latex", "content": rf"H = {round_sf(dose_rate)} \times {t_h}"},
        {"type": "latex", "content": rf"H = {correct}\ \mathrm{{Sv}}"},
    ]
    question = (
        f"A worker is exposed to radiation at a dose rate of {round_sf(dose_rate)} Sv/h "
        f"for {t_h} hour{'s' if t_h > 1 else ''}.\n\n"
        f"Calculate the equivalent dose received."
    )
    div_err = round_sf(dose_rate / t_h)
    options_data = [
        {"value": float(correct),        "display": f"{correct} Sv",   "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(dose_rate),   "display": f"{round_sf(dose_rate)} Sv", "summary": "Incorrect.", "mistake": "You gave the dose rate (Sv/h), not the total dose. Multiply by time: H = Ḣ × t.", "working": working},
        {"value": float(div_err),        "display": f"{div_err} Sv",   "summary": "Incorrect.", "mistake": "You divided Ḣ by t instead of multiplying. H = Ḣ × t.", "working": working},
        {"value": round_sf(dose_rate * t_h * 2), "display": f"{round_sf(dose_rate * t_h * 2)} Sv", "summary": "Incorrect.", "mistake": "Check your arithmetic — your answer is 2× too large.", "working": working},
    ]
    return make_question(question, float(correct), options_data, "Sv",
                         notes=NOTES["radiation_doses"], topic="Radiation", question_type="Dose", level=level)


def gen_find_D_from_H(level="N5"):
    rad, mass_display, mass_unit, mass_kg, is_grams, mass_g, D, E, t_h, H, dose_rate = _pick_values()
    w_R     = rad["w_R"]
    correct = round_sf(D)

    working = [
        {"type": "text",  "content": "Rearrange H = D × w_R to find D:"},
        {"type": "latex", "content": r"D = \frac{H}{w_R}"},
        {"type": "latex", "content": rf"D = \frac{{{round_sf(H)}}}{{{w_R}}}"},
        {"type": "latex", "content": rf"D = {correct}\ \mathrm{{Gy}}"},
    ]
    question = (
        f"{W_R_TABLE}\n\n"
        f"A patient receives an equivalent dose of {round_sf(H)} Sv from {rad['name']}.\n\n"
        f"Calculate the absorbed dose."
    )
    mult_err    = round_sf(H * w_R)
    wrong_wRs   = [x for x in [1, 3, 20] if x != w_R]
    wrong_D_val = round_sf(H / wrong_wRs[0]) if wrong_wRs else round_sf(H / 2)

    options_data = [
        {"value": float(correct),    "display": f"{correct} Gy",    "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(H),       "display": f"{round_sf(H)} Gy","summary": "Incorrect.", "mistake": f"You gave the equivalent dose (Sv) as the absorbed dose. D = H ÷ w_R = {round_sf(H)} ÷ {w_R} = {correct} Gy.", "working": working},
        {"value": float(mult_err),   "display": f"{mult_err} Gy",   "summary": "Incorrect.", "mistake": "You multiplied H × w_R instead of dividing. D = H ÷ w_R.", "working": working},
        {"value": float(wrong_D_val), "display": f"{wrong_D_val} Gy", "summary": "Incorrect.", "mistake": f"You used the wrong radiation weighting factor. For {rad['name']}, w_R = {w_R}.", "working": working},
    ]
    return make_question(question, float(correct), options_data, "Gy",
                         notes=NOTES["radiation_doses"], topic="Radiation", question_type="Dose", level=level)


def gen_find_E(level="N5"):
    rad, mass_display, mass_unit, mass_kg, is_grams, mass_g, D, E, t_h, H, dose_rate = _pick_values()
    mass_text = f"{mass_display} {mass_unit}"
    correct   = round_sf(E)

    working = []
    if is_grams:
        working += [
            {"type": "text",  "content": "First convert the mass to kg:"},
            {"type": "latex", "content": rf"{mass_g}\ \mathrm{{g}} = {mass_kg}\ \mathrm{{kg}}"},
        ]
    working += [
        {"type": "text",  "content": "Rearrange D = E/m to find E:"},
        {"type": "latex", "content": r"E = D \times m"},
        {"type": "latex", "content": rf"E = {D} \times {mass_kg}"},
        {"type": "latex", "content": rf"E = {correct}\ \mathrm{{J}}"},
    ]
    question = (
        f"A mass of {mass_text} of tissue receives an absorbed dose of {D} Gy.\n\n"
        f"Calculate the energy absorbed by the tissue."
    )
    div_err = round_sf(D / mass_kg)
    if is_grams:
        content_val = round_sf(D * mass_g)
        content_msg = f"You used the mass in grams ({mass_g} g) without converting to kg. {mass_g} g = {mass_kg} kg."
    else:
        content_val = div_err if round_sf(div_err) != correct else round_sf(correct * 3)
        content_msg = "You divided D by m instead of multiplying. E = D × m."

    options_data = [
        {"value": float(correct),     "display": f"{correct} J",    "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(D),           "display": f"{D} Gy",         "summary": "Incorrect.", "mistake": f"You gave the absorbed dose (Gy), not the energy (J). E = D × m.", "working": working},
        {"value": float(div_err),     "display": f"{div_err} J",    "summary": "Incorrect.", "mistake": "You divided D by m instead of multiplying. E = D × m.", "working": working},
        {"value": float(content_val), "display": f"{content_val} J","summary": "Incorrect.", "mistake": content_msg, "working": working},
    ]
    return make_question(question, float(correct), options_data, "J",
                         notes=NOTES["radiation_doses"], topic="Radiation", question_type="Dose", level=level)


_ALL_GENS = [gen_find_D, gen_find_H, gen_find_dose_rate, gen_find_H_from_rate, gen_find_D_from_H, gen_find_E]


def generate_dose(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
