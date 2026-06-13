import random
from utils.make_question import make_question
from utils.notes import NOTES


def round_sf(value, sf=3):
    return float(f"{value:.{sf}g}")


GRAVITY_LOCATIONS = {
    "Mercury": 3.70, "Venus": 8.87, "Earth": 9.81, "Moon": 1.62,
    "Mars": 3.71, "Jupiter": 24.8, "Saturn": 10.4, "Uranus": 8.69, "Neptune": 11.2,
}


def _choose_location():
    loc = random.choice(list(GRAVITY_LOCATIONS.keys()))
    return loc, GRAVITY_LOCATIONS[loc]


def _choose_wrong_g(correct_loc):
    wrong = random.choice([l for l in GRAVITY_LOCATIONS if l != correct_loc])
    return wrong, GRAVITY_LOCATIONS[wrong]


def _generate_mass():
    if random.choice([True, False]):
        m = random.choice(range(10, 151, 10))
        return m, m, False
    g = random.choice(range(100, 5100, 100))
    return g, g / 1000, True


def gen_weight(level="N5"):
    disp_mass, mass_kg, is_g = _generate_mass()
    loc, gravity = _choose_location()
    correct = round_sf(mass_kg * gravity)
    wrong_loc, wrong_g = _choose_wrong_g(loc)

    mass_text = f"{disp_mass}g" if is_g else f"{disp_mass} kg"
    grams_error = round_sf(disp_mass * gravity) if is_g else round_sf(disp_mass + gravity)

    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"W = mg"},
        {"type": "latex", "content": rf"W = {round_sf(mass_kg)} \times {round_sf(gravity)}"},
        {"type": "latex", "content": rf"W = {correct}\ \mathrm{{N}}"},
    ]
    question = f"What is the weight of a {mass_text} object on {loc}?"
    options_data = [
        {"value": correct,                           "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(mass_kg * wrong_g),       "summary": "Incorrect.", "mistake": f"You used the gravitational field strength for {wrong_loc}.", "working": working},
        {"value": round_sf(mass_kg / gravity),       "summary": "Incorrect.", "mistake": "You divided by g instead of multiplying. W = m × g.", "working": working},
        {"value": grams_error,                       "summary": "Incorrect.", "mistake": "You did not convert grams into kilograms before calculating.", "working": working},
    ]
    return make_question(question, correct, options_data, "N",
                         notes=NOTES["dynamics_weight"], topic="Dynamics", question_type="Weight", level=level)


def gen_mass(level="N5"):
    weight = random.choice(range(10, 501, 10))
    loc, gravity = _choose_location()
    correct = round_sf(weight / gravity)
    wrong_loc, wrong_g = _choose_wrong_g(loc)

    working = [
        {"type": "text",  "content": "Rearrange the equation:"},
        {"type": "latex", "content": r"m = \frac{W}{g}"},
        {"type": "latex", "content": rf"m = \frac{{{weight}}}{{{round_sf(gravity)}}}"},
        {"type": "latex", "content": rf"m = {correct}\ \mathrm{{kg}}"},
    ]
    question = f"What is the mass of an object with weight {weight} N on {loc}?"
    options_data = [
        {"value": correct,                    "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(weight / wrong_g), "summary": "Incorrect.", "mistake": f"You used the gravitational field strength for {wrong_loc}.", "working": working},
        {"value": round_sf(weight * gravity), "summary": "Incorrect.", "mistake": "You multiplied instead of dividing. m = W ÷ g.", "working": working},
        {"value": round_sf(correct * 1000),   "summary": "Incorrect.", "mistake": "You gave the answer in grams, not kilograms.", "working": working},
    ]
    return make_question(question, correct, options_data, "kg",
                         notes=NOTES["dynamics_weight"], topic="Dynamics", question_type="Weight", level=level)


def gen_gravity(level="N5"):
    disp_mass, mass_kg, is_g = _generate_mass()
    weight = random.choice(range(10, 501, 10))
    correct = round_sf(weight / mass_kg)
    _, wrong_g = _choose_wrong_g("")

    mass_text = f"{disp_mass}g" if is_g else f"{disp_mass} kg"
    grams_error = round_sf(weight / disp_mass) if is_g else wrong_g

    working = [
        {"type": "text",  "content": "Rearrange the equation:"},
        {"type": "latex", "content": r"g = \frac{W}{m}"},
        {"type": "latex", "content": rf"g = \frac{{{weight}}}{{{round_sf(mass_kg)}}}"},
        {"type": "latex", "content": rf"g = {correct}\ \mathrm{{N/kg}}"},
    ]
    question = f"What is the gravitational field strength for an object with weight {weight} N and mass {mass_text}?"
    options_data = [
        {"value": correct,                        "summary": "Correct!", "mistake": None, "working": working},
        {"value": round_sf(weight * mass_kg),     "summary": "Incorrect.", "mistake": "You multiplied W × m instead of dividing. g = W ÷ m.", "working": working},
        {"value": grams_error,                    "summary": "Incorrect.", "mistake": "You did not convert grams into kilograms before calculating.", "working": working},
        {"value": wrong_g,                        "summary": "Incorrect.", "mistake": "You selected a g value from memory rather than calculating it.", "working": working},
    ]
    return make_question(question, correct, options_data, "N/kg",
                         notes=NOTES["dynamics_weight"], topic="Dynamics", question_type="Weight", level=level)


_N4_GENS  = [gen_weight]
_ALL_GENS = [gen_weight, gen_mass, gen_gravity]


def generate_weight(level="N5"):
    gens = _N4_GENS if level == "N4" else _ALL_GENS
    return random.choice(gens)(level=level)
