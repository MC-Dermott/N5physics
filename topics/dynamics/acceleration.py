import random
from utils.make_question import make_question
from utils.notes import NOTES


def _working_a(force, mass, answer):
    return [
        {"type": "text",  "content": "Use Newton's Second Law:"},
        {"type": "latex", "content": r"a = \frac{F}{m}"},
        {"type": "latex", "content": rf"a = \frac{{{force}}}{{{mass}}}"},
        {"type": "latex", "content": rf"a = {answer}\ \mathrm{{m/s^2}}"},
    ]


def _working_m(force, accel, answer):
    return [
        {"type": "text",  "content": "Rearrange Newton's Second Law:"},
        {"type": "latex", "content": r"m = \frac{F}{a}"},
        {"type": "latex", "content": rf"m = \frac{{{force}}}{{{accel}}}"},
        {"type": "latex", "content": rf"m = {answer}\ \mathrm{{kg}}"},
    ]


def _working_f(mass, accel, answer):
    return [
        {"type": "text",  "content": "Use Newton's Second Law:"},
        {"type": "latex", "content": r"F = ma"},
        {"type": "latex", "content": rf"F = {mass} \times {accel}"},
        {"type": "latex", "content": rf"F = {answer}\ \mathrm{{N}}"},
    ]


# ── unit-conversion helpers ──────────────────────────────────────────────
# Worksheet Section 2 always converts exactly one given quantity (mass in g
# or tonnes, or force in kN) into SI units before F = ma is used — never
# both at once. These helpers reproduce that pattern and feed a matching
# "forgot to convert" distractor.

def _mass_choice():
    """Returns (mass_kg, display_str, raw_display_value_or_None_if_plain)."""
    r = random.random()
    if r < 0.35:
        g = random.randint(200, 950)
        return g / 1000, f"{g} g", g
    elif r < 0.75:
        kg = random.randint(2, 10)
        return float(kg), f"{kg} kg", None
    else:
        t = round(random.uniform(1.0, 3.5), 1)
        label = f"{t} tonne" + ("" if t == 1 else "s")
        return t * 1000, label, t


def _force_choice_kN_or_N(lo_n=2000, hi_n=8000):
    """Returns (force_N, display_str, raw_display_value_or_None_if_plain)."""
    if random.random() < 0.5:
        kN = round(random.uniform(lo_n / 1000, hi_n / 1000), 1)
        return kN * 1000, f"{kN} kN", kN
    else:
        n = random.randint(lo_n, hi_n)
        return float(n), f"{n} N", None


def gen_find_a(level="N5"):
    mass_kg, mass_str, raw_mass = _mass_choice()
    force_n = float(random.randint(2, 10) if mass_kg < 1.5 else
                     random.randint(2000, 8000) if mass_kg > 500 else
                     random.randint(10, 50))
    force_str = f"{force_n:g} N"
    correct = round(force_n / mass_kg, 2)

    working = _working_a(f"{force_n:g}", f"{mass_kg:g}", correct)
    question = f"What is the acceleration of a {mass_str} object if a single force of {force_str} is applied?"
    options_data = [
        {"value": correct,       "mistake": None, "working": working},
        {"value": round(force_n * mass_kg, 2), "mistake": "You multiplied F × m instead of dividing. a = F ÷ m.", "working": working},
        {"value": round(force_n + mass_kg, 2), "mistake": "You used the formula incorrectly. a = F ÷ m.", "working": working},
        {"value": round(mass_kg / force_n, 2), "mistake": "You divided m by F instead of F by m. a = F ÷ m.", "working": working},
    ]
    scaffold = None
    if raw_mass is not None:
        options_data.append({
            "value": round(force_n / raw_mass, 2),
            "mistake": f"You used {mass_str} directly without converting it to kg first — always convert to SI units before substituting.",
            "working": working,
        })
        scaffold = [
            {"question": "What is the mass in kilograms?", "answer": round(mass_kg, 3)},
            {"question": "What is the acceleration?", "answer": correct},
        ]
    return make_question(question, correct, options_data, "m/s²", scaffold=scaffold,
                         notes=NOTES["dynamics_newton"], topic="Dynamics", question_type="Acceleration", level=level)


def gen_find_m(level="N5"):
    accel = random.randint(2, 5)
    force_n, force_str, raw_force = _force_choice_kN_or_N()
    correct = round(force_n / accel, 2)
    working = _working_m(f"{force_n:g}", accel, correct)
    question = f"What is the mass of an object accelerating at {accel} m/s² if a single force of {force_str} is applied?"
    options_data = [
        {"value": correct,       "mistake": None, "working": working},
        {"value": round(force_n * accel, 2), "mistake": "You multiplied F × a instead of dividing. m = F ÷ a.", "working": working},
        {"value": round(force_n + accel, 2), "mistake": "You used F = ma incorrectly. m = F ÷ a.", "working": working},
        {"value": round(accel / force_n, 2), "mistake": "You divided a by F. m = F ÷ a.", "working": working},
    ]
    scaffold = None
    if raw_force is not None:
        options_data.append({
            "value": round(raw_force / accel, 2),
            "mistake": f"You used {force_str} directly without converting it to N first — always convert to SI units before substituting.",
            "working": working,
        })
        scaffold = [
            {"question": "What is the force in newtons?", "answer": round(force_n, 1)},
            {"question": "What is the mass?", "answer": correct},
        ]
    return make_question(question, correct, options_data, "kg", scaffold=scaffold,
                         notes=NOTES["dynamics_newton"], topic="Dynamics", question_type="Acceleration", level=level)


def gen_find_f(level="N5"):
    mass_kg, mass_str, raw_mass = _mass_choice()
    accel = round(random.uniform(5, 20), 1) if mass_kg < 1.5 else \
            round(random.uniform(0.5, 3), 2) if mass_kg > 500 else \
            random.randint(2, 5)
    correct = round(mass_kg * accel, 2)
    working = _working_f(f"{mass_kg:g}", accel, correct)
    question = f"What is the force on a {mass_str} object accelerating at {accel} m/s²?"
    options_data = [
        {"value": correct,      "mistake": None, "working": working},
        {"value": round(mass_kg + accel, 2), "mistake": "You added m and a instead of multiplying. F = m × a.", "working": working},
        {"value": round(mass_kg * (accel + 1), 2), "mistake": "You used the equation incorrectly. F = m × a.", "working": working},
        {"value": round(mass_kg / accel, 2), "mistake": "You divided m by a instead of multiplying. F = m × a.", "working": working},
    ]
    scaffold = None
    if raw_mass is not None:
        options_data.append({
            "value": round(raw_mass * accel, 2),
            "mistake": f"You used {mass_str} directly without converting it to kg first — always convert to SI units before substituting.",
            "working": working,
        })
        scaffold = [
            {"question": "What is the mass in kilograms?", "answer": round(mass_kg, 3)},
            {"question": "What is the force?", "answer": correct},
        ]
    return make_question(question, correct, options_data, "N", scaffold=scaffold,
                         notes=NOTES["dynamics_newton"], topic="Dynamics", question_type="Acceleration", level=level)


_N4_GENS  = [gen_find_a]
_ALL_GENS = [gen_find_a, gen_find_m, gen_find_f]


def generate_acceleration(level="N5"):
    gens = _N4_GENS if level == "N4" else _ALL_GENS
    return random.choice(gens)(level=level)
