import math
import random
from core.models.question_model import PhysicsQuestion
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


def _distinct_options(gen):
    """Re-roll a generator until its distractors are all different from each
    other and from the correct answer (some random values make them coincide)."""
    def wrapped(level="N5"):
        for _ in range(20):
            q = gen(level=level)
            vals = [round(float(d["value"]), 6) for d in q.distractors]
            if len(vals) == 3 and len(set(vals)) == 3:
                break
        return q
    wrapped.__name__ = gen.__name__
    return wrapped


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
    scaffold = [
        {"question": "What is m × g?", "answer": round_sf(mass_kg * gravity)},
        {"question": "What is the gravitational potential energy Ep?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "J", notes=NOTES["energy_gpe"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


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
    scaffold = [
        {"question": "What is g × h?", "answer": round_sf(gravity * height)},
        {"question": "What is the mass m?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "kg", notes=NOTES["energy_gpe"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


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
    scaffold = [
        {"question": "What is m × g?", "answer": round_sf(mass_kg * gravity)},
        {"question": "What is the height h?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "m", notes=NOTES["energy_gpe"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


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
    scaffold = [
        {"question": "What is v² ?", "answer": v ** 2},
        {"question": "What is the kinetic energy Ek?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "J", notes=NOTES["energy_ke"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


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
    scaffold = [
        {"question": "What is v² ?", "answer": v ** 2},
        {"question": "What is the mass m?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "kg", notes=NOTES["energy_ke"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


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
    scaffold = [
        {"question": "What is 2Ek ÷ m?", "answer": round_sf((2 * energy) / mass_kg)},
        {"question": "What is the velocity v?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "m/s", notes=NOTES["energy_ke"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


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


# =========================================================
# Conservation of Energy — Ep ⇄ Ek, energy lost to friction
# =========================================================

_DROP_OBJECTS  = ["stone", "ball", "rock", "box", "bag of sand"]
_THROW_OBJECTS = ["ball", "stone", "bean bag", "tennis ball"]
_SLIDE_OBJECTS = ["sledge", "skateboarder", "go-kart", "toboggan", "trolley"]
_BRAKE_OBJECTS = ["car", "van", "cyclist", "motorbike"]


def gen_cons_falling_speed(level="N5"):
    obj     = random.choice(_DROP_OBJECTS)
    mass_kg = random.choice([0.2, 0.4, 1.5, 2, 2.5, 3, 4, 5])
    gravity = random.choice([9.8, 10])
    height  = random.randint(2, 40)
    ep      = round_sf(mass_kg * gravity * height)
    correct = round_sf(math.sqrt(2 * ep / mass_kg))

    working = [
        {"type": "text",  "content": "Calculate the gravitational potential energy lost:"},
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"E_p = {mass_kg} \times {gravity} \times {height} = {fmt_J(ep)}"},
        {"type": "text",  "content": "No energy is lost, so all the Ep lost becomes Ek gained:"},
        {"type": "latex", "content": rf"E_k = {fmt_J(ep)}"},
        {"type": "latex", "content": r"E_k = \frac{1}{2}mv^2"},
        {"type": "latex", "content": rf"{ep:g} = \frac{{1}}{{2}} \times {mass_kg} \times v^2"},
        {"type": "latex", "content": rf"v = {correct}\ \mathrm{{m/s}}"},
    ]
    question = (f"A {mass_kg} kg {obj} is dropped from a height of {height} m. Assuming no energy "
                f"is lost to air resistance, calculate the speed of the {obj} just before it hits "
                f"the ground.\n\n{_g_table(gravity)}")
    options_data = [
        {"value": correct,                              "mistake": None, "working": working},
        {"value": round_sf(math.sqrt(ep / mass_kg)),    "mistake": "You forgot the ½ in Ek = ½mv². v = √(2Ek ÷ m).", "working": working},
        {"value": round_sf(2 * ep / mass_kg),           "mistake": "You found v² — remember to take the square root.", "working": working},
        {"value": round_sf(math.sqrt(2 * ep)),          "mistake": "You forgot to divide by the mass. v = √(2Ek ÷ m).", "working": working},
    ]
    scaffold = [
        {"question": "What is the gravitational potential energy lost, Ep?", "answer": ep},
        {"question": "What is the kinetic energy gained, Ek?", "answer": ep},
        {"question": "What is the speed v?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "m/s", notes=NOTES["energy_conservation"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


def gen_cons_max_height(level="N5"):
    obj     = random.choice(_THROW_OBJECTS)
    mass_kg = random.choice([0.1, 0.2, 0.25, 0.4, 0.5, 0.6])
    gravity = random.choice([9.8, 10])
    v       = random.randint(4, 25)
    ek      = round_sf(0.5 * mass_kg * v ** 2)
    correct = round_sf(ek / (mass_kg * gravity))

    working = [
        {"type": "text",  "content": "Calculate the kinetic energy at launch:"},
        {"type": "latex", "content": r"E_k = \frac{1}{2}mv^2"},
        {"type": "latex", "content": rf"E_k = \frac{{1}}{{2}} \times {mass_kg} \times {v}^2 = {fmt_J(ek)}"},
        {"type": "text",  "content": "At maximum height all the Ek has become Ep:"},
        {"type": "latex", "content": rf"E_p = {fmt_J(ek)}"},
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"{ek:g} = {mass_kg} \times {gravity} \times h"},
        {"type": "latex", "content": rf"h = {correct}\ \mathrm{{m}}"},
    ]
    question = (f"A {mass_kg} kg {obj} is thrown vertically upwards at {v} m/s. Assuming no energy "
                f"is lost to air resistance, calculate the maximum height reached by the {obj}."
                f"\n\n{_g_table(gravity)}")
    options_data = [
        {"value": correct,                              "mistake": None, "working": working},
        {"value": round_sf(mass_kg * v ** 2 / (mass_kg * gravity)), "mistake": "You forgot the ½ in Ek = ½mv².", "working": working},
        {"value": round_sf(0.5 * mass_kg * v / (mass_kg * gravity)), "mistake": "You forgot to square the speed in Ek = ½mv².", "working": working},
        {"value": round_sf(ek / gravity),               "mistake": "You forgot to divide by the mass. h = Ep ÷ (m × g).", "working": working},
    ]
    scaffold = [
        {"question": "What is the kinetic energy at launch, Ek?", "answer": ek},
        {"question": "What is the gravitational potential energy at maximum height, Ep?", "answer": ek},
        {"question": "What is the maximum height h?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "m", notes=NOTES["energy_conservation"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


def gen_cons_energy_lost(level="N5"):
    obj     = random.choice(_SLIDE_OBJECTS)
    mass_kg = random.choice(range(20, 85, 5))
    gravity = random.choice([9.8, 10])
    height  = random.randint(3, 20)
    v_ideal = math.sqrt(2 * gravity * height)
    v       = round(random.uniform(0.5, 0.85) * v_ideal, 1)
    ep      = round_sf(mass_kg * gravity * height)
    ek      = round_sf(0.5 * mass_kg * v ** 2)
    lost    = round_sf(ep - ek)
    find_force = random.choice([True, False])
    distance   = round(height * random.uniform(2, 5))

    working = [
        {"type": "text",  "content": "Gravitational potential energy lost:"},
        {"type": "latex", "content": rf"E_p = mgh = {mass_kg} \times {gravity} \times {height} = {fmt_J(ep)}"},
        {"type": "text",  "content": "Kinetic energy at the bottom:"},
        {"type": "latex", "content": rf"E_k = \frac{{1}}{{2}}mv^2 = \frac{{1}}{{2}} \times {mass_kg} \times {v}^2 = {fmt_J(ek)}"},
        {"type": "text",  "content": "The difference is the energy lost (as heat) due to friction:"},
        {"type": "latex", "content": rf"E_{{lost}} = {ep:g} - {ek:g} = {fmt_J(lost)}"},
    ]
    question = (f"A {obj} of total mass {mass_kg} kg starts from rest at the top of a slope {height} m high. "
                f"The {obj} travels {distance} m down the slope and reaches a speed of {v} m/s at the bottom.\n\n")

    if find_force:
        correct = round_sf(lost / distance)
        working += [
            {"type": "text",  "content": "This energy equals the work done against friction:"},
            {"type": "latex", "content": r"E_W = Fd"},
            {"type": "latex", "content": rf"{lost:g} = F \times {distance}"},
            {"type": "latex", "content": rf"F = {correct}\ \mathrm{{N}}"},
        ]
        question += f"Calculate the average frictional force acting on the {obj}.\n\n{_g_table(gravity)}"
        options_data = [
            {"value": correct,                    "mistake": None, "working": working},
            {"value": round_sf(ep / distance),    "mistake": "You used all of the Ep. Only the energy lost (Ep − Ek) is work done against friction.", "working": working},
            {"value": round_sf(ek / distance),    "mistake": "You used the Ek at the bottom. The work done against friction is the energy lost (Ep − Ek).", "working": working},
            {"value": round_sf((ep + ek) / distance), "mistake": "You added Ep and Ek. The energy lost is Ep − Ek.", "working": working},
        ]
        scaffold = [
            {"question": "What is the gravitational potential energy lost, Ep?", "answer": ep},
            {"question": "What is the kinetic energy at the bottom, Ek?", "answer": ek},
            {"question": "How much energy is lost due to friction?", "answer": lost},
            {"question": "What is the average frictional force F?", "answer": correct},
        ]
        return make_question(question, correct, options_data, "N", notes=NOTES["energy_conservation"],
                             topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)

    correct = lost
    question += f"Calculate the energy lost due to friction.\n\n{_g_table(gravity)}"
    options_data = [
        {"value": correct,          "display": fmt_J(correct),        "mistake": None, "working": working},
        {"value": round_sf(ep + ek),"display": fmt_J(round_sf(ep + ek)), "mistake": "You added Ep and Ek. The energy lost is Ep − Ek.", "working": working},
        {"value": ek,               "display": fmt_J(ek),             "mistake": "That is the kinetic energy at the bottom. The energy lost is Ep − Ek.", "working": working},
        {"value": round_sf(ep - mass_kg * v ** 2), "display": fmt_J(round_sf(ep - mass_kg * v ** 2)),
         "mistake": "You forgot the ½ in Ek = ½mv².", "working": working},
    ]
    scaffold = [
        {"question": "What is the gravitational potential energy lost, Ep?", "answer": ep},
        {"question": "What is the kinetic energy at the bottom, Ek?", "answer": ek},
        {"question": "How much energy is lost due to friction?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "J", notes=NOTES["energy_conservation"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


def gen_cons_braking(level="N5"):
    obj = random.choice(_BRAKE_OBJECTS)
    if obj == "cyclist":
        mass_kg, v = random.choice(range(60, 105, 5)), random.randint(4, 12)
    elif obj == "motorbike":
        mass_kg, v = random.choice(range(200, 401, 20)), random.randint(10, 25)
    else:
        mass_kg, v = random.choice(range(800, 2001, 100)), random.randint(10, 30)
    distance = random.randint(10, 60) if obj != "cyclist" else random.randint(4, 15)
    ek       = round_sf(0.5 * mass_kg * v ** 2)
    correct  = round_sf(ek / distance)

    working = [
        {"type": "text",  "content": "Kinetic energy before braking:"},
        {"type": "latex", "content": r"E_k = \frac{1}{2}mv^2"},
        {"type": "latex", "content": rf"E_k = \frac{{1}}{{2}} \times {mass_kg} \times {v}^2 = {fmt_J(ek)}"},
        {"type": "text",  "content": "All of this Ek is transferred by the work done by the brakes (as heat):"},
        {"type": "latex", "content": r"E_W = Fd"},
        {"type": "latex", "content": rf"{ek:g} = F \times {distance}"},
        {"type": "latex", "content": rf"F = {correct}\ \mathrm{{N}}"},
    ]
    question = (f"A {obj} of mass {mass_kg} kg is travelling at {v} m/s. The brakes are applied and "
                f"it comes to rest in a distance of {distance} m.\n\n"
                f"Calculate the average braking force.")
    options_data = [
        {"value": correct,                                "mistake": None, "working": working},
        {"value": round_sf(mass_kg * v ** 2 / distance),  "mistake": "You forgot the ½ in Ek = ½mv².", "working": working},
        {"value": round_sf(0.5 * mass_kg * v / distance), "mistake": "You forgot to square the speed in Ek = ½mv².", "working": working},
        {"value": round_sf(ek * distance),                "mistake": "You multiplied by the distance. F = E_W ÷ d.", "working": working},
    ]
    scaffold = [
        {"question": "What is the kinetic energy before braking, Ek?", "answer": ek},
        {"question": "What is the work done by the brakes?", "answer": ek},
        {"question": "What is the average braking force F?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "N", notes=NOTES["energy_conservation"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


# =========================================================
# Explain — effect of friction, mass, speed, height
# =========================================================

_HEAT_LOST = ("Some energy is converted into heat (and sound) due to friction / air resistance, "
              "so not all of the energy is transferred as calculated.")

# (question, correct, distractors, explanation)
_EXPLAIN_CASES = [
    (
        "A {slider} slides down a slope. The speed at the bottom is calculated assuming all the "
        "gravitational potential energy becomes kinetic energy. The actual speed measured is less "
        "than the calculated value. Why?",
        "Some energy is converted into heat due to friction.",
        ["The mass of the {slider} decreases as it moves.",
         "Gravitational field strength decreases as the {slider} moves down the slope.",
         "Kinetic energy is converted into gravitational potential energy on the way down."],
        _HEAT_LOST,
    ),
    (
        "A ball is thrown vertically upwards. The maximum height is calculated assuming all the "
        "kinetic energy becomes gravitational potential energy. The actual height reached is less "
        "than calculated. Why?",
        "Some energy is converted into heat due to air resistance.",
        ["The ball gains mass as it rises.",
         "The ball's kinetic energy is zero when it is thrown.",
         "Gravitational potential energy is converted into kinetic energy as the ball rises."],
        _HEAT_LOST,
    ),
    (
        "A {slider} slides down a slope from rest. If the slope were made rougher, so that the "
        "force of friction increased, what would happen to the speed of the {slider} at the bottom?",
        "Decrease",
        ["Increase", "Stay the same"],
        "More work is done against friction, so more energy is converted into heat. Less of the "
        "gravitational potential energy becomes kinetic energy, so the speed at the bottom is lower.",
    ),
    (
        "A {slider} slides down a slope from rest. How does the gravitational potential energy lost "
        "compare with the kinetic energy gained, when friction acts?",
        "The Ep lost is greater than the Ek gained.",
        ["The Ep lost is equal to the Ek gained.", "The Ep lost is less than the Ek gained."],
        "Some of the Ep lost is converted into heat by friction, so only part of it becomes Ek. "
        "The Ep lost is therefore greater than the Ek gained.",
    ),
    (
        "Two objects are dropped from the same height. One has twice the mass of the other. "
        "Ignoring air resistance, how does the speed of the heavier object just before it hits the "
        "ground compare with the lighter one?",
        "It is the same",
        ["It is double", "It is half"],
        "mgh = ½mv², so the mass cancels: v = √(2gh). The speed only depends on the height fallen "
        "(and g), not on the mass.",
    ),
    (
        "The speed of a {mover} is doubled. What happens to its kinetic energy?",
        "It is four times bigger",
        ["It doubles", "It stays the same", "It halves"],
        "Ek = ½mv². The speed is squared, so doubling v multiplies Ek by 2² = 4.",
    ),
    (
        "An object is lifted to twice the height. What happens to its gain in gravitational "
        "potential energy?",
        "It doubles",
        ["It is four times bigger", "It stays the same", "It halves"],
        "Ep = mgh. Ep is directly proportional to h, so doubling the height doubles Ep.",
    ),
    (
        "A {mover} brakes and comes to a stop. What happens to its kinetic energy?",
        "It is converted into heat in the brakes by friction.",
        ["It is converted into gravitational potential energy.",
         "It is destroyed.",
         "It is converted into chemical energy in the fuel."],
        "The braking force does work against the motion. Energy cannot be destroyed — the kinetic "
        "energy is converted into heat (and sound) by friction in the brakes.",
    ),
    (
        "A roller coaster car is released from rest at the top of the first hill. Why must the "
        "second hill be lower than the first?",
        "Some energy is converted into heat by friction, so the car cannot regain its original height.",
        ["The car gains mass as it travels.",
         "The car has more kinetic energy at the top of the second hill.",
         "Gravitational field strength is weaker at the second hill."],
        "Friction and air resistance convert some energy into heat. The car has less total energy "
        "at the second hill, so it cannot reach the same height (the Ep available is less).",
    ),
    (
        "A ball is thrown vertically upwards. What is its kinetic energy at the maximum height?",
        "Zero",
        ["At its greatest value", "Equal to its kinetic energy at launch"],
        "At the maximum height the ball is momentarily stationary (v = 0), so Ek = ½mv² = 0. "
        "All of its kinetic energy has become gravitational potential energy.",
    ),
]


def gen_energy_explain(level="N5"):
    question_text, correct, distractor_texts, reason = random.choice(_EXPLAIN_CASES)
    fill = {"slider": random.choice(_SLIDE_OBJECTS), "mover": random.choice(_BRAKE_OBJECTS)}
    question_text = question_text.format(**fill)
    correct = correct.format(**fill)
    distractor_texts = [d.format(**fill) for d in distractor_texts]

    working = [{"type": "text", "content": reason}]
    distractors = [{"value": d, "mistake": reason, "working": working} for d in distractor_texts]
    options = [correct] + distractor_texts
    random.shuffle(options)

    return PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        distractors=distractors,
        working=working,
        notes=NOTES["energy_conservation"],
        topic="Dynamics",
        question_type="Energy",
        level=level,
        metadata={"type": "classification", "options": options},
    )


_GPE_GENS    = [_distinct_options(g) for g in (gen_gpe, gen_gpe_mass, gen_gpe_height)]
_KE_GENS     = [_distinct_options(g) for g in (gen_ke, gen_ke_mass, gen_ke_velocity)]
_WORK_GENS   = [_distinct_options(g) for g in (gen_workdone, gen_work_force, gen_work_distance)]
_CONS_GENS   = [_distinct_options(g) for g in (gen_cons_falling_speed, gen_cons_max_height,
                                               gen_cons_energy_lost, gen_cons_braking)]
_ALL_GENS    = _GPE_GENS + _KE_GENS + _WORK_GENS + _CONS_GENS


def generate_energy_gpe(level="N5"):
    return random.choice(_GPE_GENS)(level=level)


def generate_energy_ke(level="N5"):
    return random.choice(_KE_GENS)(level=level)


def generate_energy_work(level="N5"):
    return random.choice(_WORK_GENS)(level=level)


def generate_energy_conservation(level="N5"):
    return random.choice(_CONS_GENS)(level=level)


def generate_energy(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
