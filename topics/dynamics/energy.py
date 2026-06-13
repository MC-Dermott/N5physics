import random
from utils.make_question import make_question
from utils.notes import NOTES


def round_sf(value, sf=3):
    return float(f"{value:.{sf}g}")


def fmt_J(j):
    j = float(j)
    if abs(j) >= 1_000_000:
        return f"{j / 1_000_000:g} MJ"
    if abs(j) >= 1000:
        return f"{j / 1000:g} kJ"
    return f"{j:g} J"


def _g_table(g):
    return f"| Constant | Value |\n|---|---|\n| g | {g} N/kg |"


def _mass_and_text():
    if random.choice([True, False]):
        m = random.choice(range(5, 105, 5))
        return m, m, False, f"{m} kg"
    g = random.choice(range(100, 1000, 100))
    return g, g / 1000, True, f"{g}g"


# =========================================================
# GPE — Ep = mgh
# =========================================================

def gen_gpe(level="N5"):
    disp_m, mass_kg, is_g, mass_text = _mass_and_text()
    gravity = random.choice([9.8, 10])
    height  = random.randint(2, 50)
    correct = round_sf(mass_kg * gravity * height)
    grams_err = round_sf(disp_m * gravity * height) if is_g else round_sf(mass_kg + gravity + height)

    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"E_p = {round_sf(mass_kg)} \times {gravity} \times {height}"},
        {"type": "latex", "content": rf"E_p = {fmt_J(correct)}"},
    ]
    question = f"What is the gravitational potential energy of a {mass_text} object raised {height} m?\n\n{_g_table(gravity)}"
    options_data = [
        {"value": correct,                           "display": fmt_J(correct),                           "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(mass_kg / (gravity*height)), "display": fmt_J(round_sf(mass_kg / (gravity*height))), "summary": "Incorrect.", "mistake": "You rearranged the equation incorrectly. Ep = mgh.", "working": working},
        {"value": grams_err,                         "display": fmt_J(grams_err),                         "summary": "Incorrect.", "mistake": "You did not convert grams into kilograms.", "working": working},
        {"value": round_sf(mass_kg * gravity + height), "display": fmt_J(round_sf(mass_kg * gravity + height)), "summary": "Incorrect.", "mistake": "You used the equation incorrectly. Ep = m × g × h.", "working": working},
    ]
    return make_question(question, correct, options_data, "J", notes=NOTES["energy_gpe"],
                         topic="Dynamics", question_type="Energy", level=level)


def gen_gpe_mass(level="N5"):
    gravity = random.choice([9.8, 10])
    height  = random.randint(2, 50)
    energy  = random.choice(range(50, 5001, 50))
    correct = round_sf(energy / (gravity * height))

    working = [
        {"type": "text",  "content": "Rearrange the equation:"},
        {"type": "latex", "content": r"m = \frac{E_p}{gh}"},
        {"type": "latex", "content": rf"m = \frac{{{fmt_J(energy)}}}{{{gravity} \times {height}}}"},
        {"type": "latex", "content": rf"m = {correct}\ \mathrm{{kg}}"},
    ]
    question = f"What is the mass of an object with gravitational potential energy {fmt_J(energy)} raised {height} m?\n\n{_g_table(gravity)}"
    options_data = [
        {"value": correct,                              "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(energy * gravity * height),  "summary": "Incorrect.", "mistake": "You rearranged the equation incorrectly. m = Ep ÷ (g × h).", "working": working},
        {"value": round_sf(correct * 1000),             "summary": "Incorrect.", "mistake": "You gave the answer in grams, not kilograms.", "working": working},
        {"value": round_sf(energy / gravity),           "summary": "Incorrect.", "mistake": "You forgot to divide by h as well as g.", "working": working},
    ]
    return make_question(question, correct, options_data, "kg", notes=NOTES["energy_gpe"],
                         topic="Dynamics", question_type="Energy", level=level)


def gen_gpe_height(level="N5"):
    disp_m, mass_kg, is_g, mass_text = _mass_and_text()
    gravity = random.choice([9.8, 10])
    energy  = random.choice(range(50, 5001, 50))
    correct = round_sf(energy / (mass_kg * gravity))
    grams_err = round_sf(energy / (disp_m * gravity)) if is_g else round_sf(correct + gravity)

    working = [
        {"type": "text",  "content": "Rearrange the equation:"},
        {"type": "latex", "content": r"h = \frac{E_p}{mg}"},
        {"type": "latex", "content": rf"h = \frac{{{fmt_J(energy)}}}{{{round_sf(mass_kg)} \times {gravity}}}"},
        {"type": "latex", "content": rf"h = {correct}\ \mathrm{{m}}"},
    ]
    question = f"An object with mass {mass_text} has gravitational potential energy {fmt_J(energy)}. What height was it raised?\n\n{_g_table(gravity)}"
    options_data = [
        {"value": correct,                             "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(energy * mass_kg * gravity),"summary": "Incorrect.", "mistake": "You rearranged the equation incorrectly. h = Ep ÷ (m × g).", "working": working},
        {"value": grams_err,                           "summary": "Incorrect.", "mistake": "You did not convert grams into kilograms.", "working": working},
        {"value": round_sf(energy / mass_kg),          "summary": "Incorrect.", "mistake": "You forgot to divide by g as well.", "working": working},
    ]
    return make_question(question, correct, options_data, "m", notes=NOTES["energy_gpe"],
                         topic="Dynamics", question_type="Energy", level=level)


# =========================================================
# KE — Ek = ½mv²
# =========================================================

def gen_ke(level="N5"):
    disp_m, mass_kg, is_g, mass_text = _mass_and_text()
    v = random.randint(2, 30)
    correct = round_sf(0.5 * mass_kg * v**2)
    grams_err = round_sf(0.5 * disp_m * v**2) if is_g else round_sf(mass_kg + v)

    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"E_k = \frac{1}{2}mv^2"},
        {"type": "latex", "content": rf"E_k = \frac{{1}}{{2}} \times {round_sf(mass_kg)} \times {v}^2"},
        {"type": "latex", "content": rf"E_k = {fmt_J(correct)}"},
    ]
    question = f"What is the kinetic energy of a {mass_text} object moving at {v} m/s?"
    options_data = [
        {"value": correct,                   "display": fmt_J(correct),   "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(mass_kg * v**2),  "display": fmt_J(round_sf(mass_kg * v**2)),  "summary": "Incorrect.", "mistake": "You forgot the ½ in the equation. Ek = ½mv².", "working": working},
        {"value": grams_err,                 "display": fmt_J(grams_err), "summary": "Incorrect.", "mistake": "You did not convert grams into kilograms.", "working": working},
        {"value": round_sf((2*correct)/v**2),"display": fmt_J(round_sf((2*correct)/v**2)), "summary": "Incorrect.", "mistake": "You rearranged the equation incorrectly.", "working": working},
    ]
    return make_question(question, correct, options_data, "J", notes=NOTES["energy_ke"],
                         topic="Dynamics", question_type="Energy", level=level)


def gen_ke_mass(level="N5"):
    v = random.randint(2, 30)
    energy = random.choice(range(50, 5001, 50))
    correct = round_sf((2 * energy) / v**2)

    working = [
        {"type": "text",  "content": "Rearrange the equation:"},
        {"type": "latex", "content": r"m = \frac{2E_k}{v^2}"},
        {"type": "latex", "content": rf"m = \frac{{2 \times {fmt_J(energy)}}}{{{v}^2}}"},
        {"type": "latex", "content": rf"m = {correct}\ \mathrm{{kg}}"},
    ]
    question = f"What is the mass of an object with kinetic energy {fmt_J(energy)} moving at {v} m/s?"
    options_data = [
        {"value": correct,                         "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf((energy * v**2) / 2),   "summary": "Incorrect.", "mistake": "You rearranged the equation incorrectly. m = 2Ek ÷ v².", "working": working},
        {"value": round_sf(correct * 1000),        "summary": "Incorrect.", "mistake": "You gave the answer in grams, not kilograms.", "working": working},
        {"value": round_sf(energy / v**2),         "summary": "Incorrect.", "mistake": "You forgot to multiply by 2. m = 2Ek ÷ v².", "working": working},
    ]
    return make_question(question, correct, options_data, "kg", notes=NOTES["energy_ke"],
                         topic="Dynamics", question_type="Energy", level=level)


def gen_ke_velocity(level="N5"):
    disp_m, mass_kg, is_g, mass_text = _mass_and_text()
    energy = random.choice(range(50, 5001, 50))
    correct = round_sf(((2 * energy) / mass_kg) ** 0.5)
    grams_err = round_sf(((2 * energy) / disp_m) ** 0.5) if is_g else round_sf(correct + mass_kg)

    working = [
        {"type": "text",  "content": "Rearrange the equation:"},
        {"type": "latex", "content": r"v = \sqrt{\frac{2E_k}{m}}"},
        {"type": "latex", "content": rf"v = \sqrt{{\frac{{2 \times {fmt_J(energy)}}}{{{round_sf(mass_kg)}}}}}"},
        {"type": "latex", "content": rf"v = {correct}\ \mathrm{{m/s}}"},
    ]
    question = f"An object with mass {mass_text} has kinetic energy {fmt_J(energy)}. What is its velocity?"
    options_data = [
        {"value": correct,                           "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(energy / (0.5 * mass_kg)),"summary": "Incorrect.", "mistake": "You forgot to take the square root. v = √(2Ek ÷ m).", "working": working},
        {"value": grams_err,                         "summary": "Incorrect.", "mistake": "You did not convert grams into kilograms.", "working": working},
        {"value": round_sf((energy / mass_kg) ** 0.5),"summary": "Incorrect.", "mistake": "You forgot to multiply by 2 before square rooting. v = √(2Ek ÷ m).", "working": working},
    ]
    return make_question(question, correct, options_data, "m/s", notes=NOTES["energy_ke"],
                         topic="Dynamics", question_type="Energy", level=level)


# =========================================================
# Work Done — W = Fd
# =========================================================

def gen_workdone(level="N5"):
    force    = random.choice(range(5, 105, 5))
    distance = random.randint(2, 50)
    correct  = round_sf(force * distance)

    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"W = Fd"},
        {"type": "latex", "content": rf"W = {force} \times {distance}"},
        {"type": "latex", "content": rf"W = {fmt_J(correct)}"},
    ]
    question = f"What is the work done when a force of {force} N moves an object {distance} m?"
    options_data = [
        {"value": correct,              "display": fmt_J(correct),              "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(force/distance), "display": fmt_J(round_sf(force/distance)), "summary": "Incorrect.", "mistake": "You divided instead of multiplying. W = F × d.", "working": working},
        {"value": round_sf(force+distance), "display": fmt_J(round_sf(force+distance)), "summary": "Incorrect.", "mistake": "You added instead of multiplying. W = F × d.", "working": working},
        {"value": round_sf(distance/force), "display": fmt_J(round_sf(distance/force)), "summary": "Incorrect.", "mistake": "You divided the wrong way around.", "working": working},
    ]
    return make_question(question, correct, options_data, "J", notes=NOTES["energy_work"],
                         topic="Dynamics", question_type="Energy", level=level)


def gen_work_force(level="N5"):
    workdone = random.choice(range(50, 5001, 50))
    distance = random.randint(2, 50)
    correct  = round_sf(workdone / distance)

    working = [
        {"type": "text",  "content": "Rearrange the equation:"},
        {"type": "latex", "content": r"F = \frac{W}{d}"},
        {"type": "latex", "content": rf"F = \frac{{{fmt_J(workdone)}}}{{{distance}}}"},
        {"type": "latex", "content": rf"F = {correct}\ \mathrm{{N}}"},
    ]
    question = f"What force is needed to do {fmt_J(workdone)} of work over a distance of {distance} m?"
    options_data = [
        {"value": correct,                     "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(workdone * distance),"summary": "Incorrect.", "mistake": "You multiplied W × d instead of dividing. F = W ÷ d.", "working": working},
        {"value": round_sf(workdone + distance),"summary": "Incorrect.", "mistake": "You added instead of dividing. F = W ÷ d.", "working": working},
        {"value": round_sf(distance / workdone),"summary": "Incorrect.", "mistake": "You divided the wrong way around.", "working": working},
    ]
    return make_question(question, correct, options_data, "N", notes=NOTES["energy_work"],
                         topic="Dynamics", question_type="Energy", level=level)


def gen_work_distance(level="N5"):
    workdone = random.choice(range(50, 5001, 50))
    force    = random.choice(range(5, 105, 5))
    correct  = round_sf(workdone / force)

    working = [
        {"type": "text",  "content": "Rearrange the equation:"},
        {"type": "latex", "content": r"d = \frac{W}{F}"},
        {"type": "latex", "content": rf"d = \frac{{{fmt_J(workdone)}}}{{{force}}}"},
        {"type": "latex", "content": rf"d = {correct}\ \mathrm{{m}}"},
    ]
    question = f"How far does an object move if {fmt_J(workdone)} of work is done using a force of {force} N?"
    options_data = [
        {"value": correct,                     "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(workdone * force),  "summary": "Incorrect.", "mistake": "You multiplied W × F instead of dividing. d = W ÷ F.", "working": working},
        {"value": round_sf(workdone + force),  "summary": "Incorrect.", "mistake": "You added instead of dividing. d = W ÷ F.", "working": working},
        {"value": round_sf(force / workdone),  "summary": "Incorrect.", "mistake": "You divided the wrong way around.", "working": working},
    ]
    return make_question(question, correct, options_data, "m", notes=NOTES["energy_work"],
                         topic="Dynamics", question_type="Energy", level=level)


_GPE_GENS    = [gen_gpe, gen_gpe_mass, gen_gpe_height]
_KE_GENS     = [gen_ke, gen_ke_mass, gen_ke_velocity]
_WORK_GENS   = [gen_workdone, gen_work_force, gen_work_distance]
_ALL_GENS    = _GPE_GENS + _KE_GENS + _WORK_GENS


def generate_energy(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
