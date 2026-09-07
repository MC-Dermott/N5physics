import random
from utils.make_question import make_question
from utils.notes import NOTES

_PLANETS = {
    "Mercury": 3.7, "Venus": 8.9, "Earth": 9.8, "Mars": 3.7,
    "Jupiter": 23, "Saturn": 9.0, "Neptune": 11, "Uranus": 8.7,
}

_OBJECTS = ["astronaut", "rover", "lander", "sample container", "supply crate", "probe"]


def _dedup(options_data, correct):
    seen = {round(float(correct), 2)}
    cleaned = []
    for opt in options_data:
        key = round(float(opt["value"]), 2)
        if key not in seen:
            seen.add(key)
            cleaned.append(opt)
        elif opt["mistake"] is None:
            cleaned.insert(0, opt)
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


# ── Forward: W = mg ──────────────────────────────────────────────────────────

def gen_weight_forward(level="S3"):
    planet, g = random.choice(list(_PLANETS.items()))
    mass = random.choice([5, 10, 12, 20, 25, 40, 50, 64, 80, 100, 150])
    obj = random.choice(_OBJECTS)
    correct = round(mass * g, 2)

    working = [
        {"type": "text", "content": f"g on {planet} = {g} N/kg"},
        {"type": "latex", "content": r"W = mg"},
        {"type": "latex", "content": rf"W = {mass} \times {g}"},
        {"type": "latex", "content": rf"W = {correct}\ \mathrm{{N}}"},
    ]
    question = (
        f"A {obj} has a mass of {mass} kg on {planet} (g = {g} N/kg).\n\n"
        f"Calculate its weight."
    )
    swapped = mass + g
    forgotten = mass
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": swapped,
         "mistake": "You added mass and g instead of multiplying. W = mg.", "working": working},
        {"value": forgotten,
         "mistake": "That's just the mass — weight = mass × g, not mass alone.", "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return make_question(question, correct, options_data, "N", scaffold=None,
                         notes=NOTES["weight_calculations_s3"], topic="Dynamics",
                         question_type="Weight Calculations", level=level)


# ── Rearranged: m = W / g ────────────────────────────────────────────────────

def gen_weight_find_mass(level="S3"):
    planet, g = random.choice(list(_PLANETS.items()))
    mass_true = random.choice([5, 10, 12, 20, 25, 40, 50, 64, 80, 100])
    obj = random.choice(_OBJECTS)
    weight = round(mass_true * g, 2)
    correct = mass_true

    working = [
        {"type": "text", "content": f"g on {planet} = {g} N/kg"},
        {"type": "latex", "content": r"m = \frac{W}{g}"},
        {"type": "latex", "content": rf"m = \frac{{{weight}}}{{{g}}}"},
        {"type": "latex", "content": rf"m = {correct}\ \mathrm{{kg}}"},
    ]
    question = (
        f"A {obj} has a weight of {weight} N on {planet} (g = {g} N/kg).\n\n"
        f"Calculate its mass."
    )
    multiplied = round(weight * g, 2)
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": multiplied,
         "mistake": "You multiplied W by g instead of dividing. m = W ÷ g.", "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return make_question(question, correct, options_data, "kg", scaffold=None,
                         notes=NOTES["weight_calculations_s3"], topic="Dynamics",
                         question_type="Weight Calculations", level=level)


# ── Conceptual: mass is invariant across planets ────────────────────────────

def gen_weight_same_mass(level="S3"):
    planet_a, g_a = random.choice(list(_PLANETS.items()))
    remaining = {k: v for k, v in _PLANETS.items() if k != planet_a}
    planet_b, g_b = random.choice(list(remaining.items()))
    mass = random.choice([5, 10, 12, 20, 25, 40, 50, 64, 80, 100])
    obj = random.choice(_OBJECTS)
    correct = mass

    working = [
        {"type": "text", "content": "Mass does not change with location — only weight does."},
        {"type": "latex", "content": rf"m = {mass}\ \mathrm{{kg}}\ \text{{(unchanged)}}"},
    ]
    question = (
        f"A {obj} has a mass of {mass} kg on {planet_a} (g = {g_a} N/kg).\n\n"
        f"State its mass on {planet_b} (g = {g_b} N/kg)."
    )
    wrong_ratio = round(mass * g_b / g_a, 2)
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": wrong_ratio,
         "mistake": f"Mass doesn't scale with g between planets — that's how weight changes, not "
                    f"mass. The mass is still {mass} kg on {planet_b}.",
         "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return make_question(question, correct, options_data, "kg", scaffold=None,
                         notes=NOTES["weight_calculations_s3"], topic="Dynamics",
                         question_type="Weight Calculations", level=level)


def generate_weight_calculations(level="S3"):
    return random.choice([gen_weight_forward, gen_weight_find_mass, gen_weight_same_mass])(level=level)
