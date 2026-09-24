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


# ── number choices ───────────────────────────────────────────────────────
# Small, friendly numbers throughout: F is always built as m × a so every
# answer comes out exact. N4 uses plain kg and N only. Every other level
# gives exactly one quantity with a prefix (mass in g, or force in kN) that
# must be converted to SI units before F = ma is used, with a matching
# "forgot to convert" distractor.

def _fmt(x):
    return f"{round(x, 3):g}"


def _plain():
    """N4: (mass_kg, accel, force_N), all small whole numbers."""
    m = random.randint(2, 20)
    a = random.randint(2, 10)
    return m, a, m * a


def _mass_in_grams():
    """(mass_kg, mass_g, accel, force_N) — a light object, mass given in g."""
    g = random.randrange(100, 950, 50)
    a = random.randint(2, 10)
    m = g / 1000
    return m, g, a, round(m * a, 3)


def _force_in_kN():
    """(mass_kg, accel, force_N, force_kN) — a heavy object, force given in kN."""
    m = random.randrange(100, 1000, 100)
    a = random.randint(1, 5)
    f = m * a
    return m, a, f, f / 1000


def _a_or_an(quantity):
    """Article for a spoken number: "an 8 kg", "an 11 kg", "an 800 g", but "a 2 kg"."""
    digits = quantity.split()[0].split(".")[0]
    vowel_sound = digits.startswith("8") or (len(digits) in (2, 5) and digits[:2] in ("11", "18"))
    return "an" if vowel_sound else "a"


def _finish(question, correct, options_data, unit, convert_step, answer_prompt, level):
    """convert_step: None, or (prompt, answer, unit, wrong_value, given_str, si_unit)."""
    scaffold = None
    if convert_step:
        prompt, conv_answer, conv_unit, wrong_value, given_str, si_unit = convert_step
        options_data.append({
            "value": wrong_value,
            "mistake": f"You used {given_str} directly without converting it to {si_unit} first — "
                       f"always convert to SI units before substituting.",
            "working": options_data[0]["working"],
        })
        scaffold = [
            {"question": prompt, "answer": conv_answer, "unit": conv_unit},
            {"question": answer_prompt, "answer": correct, "unit": unit},
        ]
    return make_question(question, correct, _dedup(options_data, correct), unit, scaffold=scaffold,
                         notes=NOTES["dynamics_newton"], topic="Dynamics", question_type="Acceleration", level=level)


def _dedup(options_data, correct):
    seen, cleaned = {round(float(correct), 4)}, [options_data[0]]
    for opt in options_data[1:]:
        key = round(float(opt["value"]), 4)
        if key not in seen:
            seen.add(key)
            cleaned.append(opt)
    return cleaned


def gen_find_a(level="N5"):
    convert = None
    if level == "N4":
        m, a, f = _plain()
        mass_str, force_str = f"{m} kg", f"{f} N"
    elif random.random() < 0.5:
        m, g, a, f = _mass_in_grams()
        mass_str, force_str = f"{g} g", f"{_fmt(f)} N"
        convert = ("What is the mass in kilograms?", m, "kg", round(f / g, 4), mass_str, "kg")
    else:
        m, a, f, kN = _force_in_kN()
        mass_str, force_str = f"{m} kg", f"{_fmt(kN)} kN"
        convert = ("What is the force in newtons?", f, "N", round(kN / m, 4), force_str, "N")

    correct = a
    working = _working_a(_fmt(f), _fmt(m), correct)
    question = (f"What is the acceleration of {_a_or_an(mass_str)} {mass_str} object "
                f"if a single force of {force_str} is applied?")
    options_data = [
        {"value": correct,             "mistake": None, "working": working},
        {"value": round(f * m, 3),     "mistake": "You multiplied F × m instead of dividing. a = F ÷ m.", "working": working},
        {"value": round(m / f, 4),     "mistake": "You divided m by F instead of F by m. a = F ÷ m.", "working": working},
    ]
    return _finish(question, correct, options_data, "m/s²", convert, "What is the acceleration?", level)


def gen_find_m(level="N5"):
    convert = None
    if level == "N4":
        m, a, f = _plain()
        force_str = f"{f} N"
    else:
        m, a, f, kN = _force_in_kN()
        force_str = f"{_fmt(kN)} kN"
        convert = ("What is the force in newtons?", f, "N", round(kN / a, 4), force_str, "N")

    correct = m
    working = _working_m(_fmt(f), a, correct)
    question = f"What is the mass of an object accelerating at {a} m/s² if a single force of {force_str} is applied?"
    options_data = [
        {"value": correct,             "mistake": None, "working": working},
        {"value": round(f * a, 3),     "mistake": "You multiplied F × a instead of dividing. m = F ÷ a.", "working": working},
        {"value": round(a / f, 4),     "mistake": "You divided a by F. m = F ÷ a.", "working": working},
    ]
    return _finish(question, correct, options_data, "kg", convert, "What is the mass?", level)


def gen_find_f(level="N5"):
    convert = None
    if level == "N4":
        m, a, f = _plain()
        mass_str = f"{m} kg"
    else:
        m, g, a, f = _mass_in_grams()
        mass_str = f"{g} g"
        convert = ("What is the mass in kilograms?", m, "kg", g * a, mass_str, "kg")

    correct = f
    working = _working_f(_fmt(m), a, _fmt(correct))
    question = f"What is the force on {_a_or_an(mass_str)} {mass_str} object accelerating at {a} m/s²?"
    options_data = [
        {"value": correct,             "mistake": None, "working": working},
        {"value": round(m + a, 3),     "mistake": "You added m and a instead of multiplying. F = m × a.", "working": working},
        {"value": round(m / a, 4),     "mistake": "You divided m by a instead of multiplying. F = m × a.", "working": working},
    ]
    return _finish(question, correct, options_data, "N", convert, "What is the force?", level)


_ALL_GENS = [gen_find_a, gen_find_m, gen_find_f]


def generate_acceleration(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
