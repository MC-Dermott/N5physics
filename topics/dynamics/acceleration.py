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


def gen_find_a(level="N5"):
    mass  = random.randint(2, 10)
    force = random.randint(10, 50)
    correct = round(force / mass, 2)
    working = _working_a(force, mass, correct)
    question = f"What is the acceleration of a {mass} kg object if {force} N of force is applied?"
    options_data = [
        {"value": correct,       "summary": "Correct!", "mistake": None, "working": working},
        {"value": force * mass,  "summary": "Incorrect.", "mistake": "You multiplied F × m instead of dividing. a = F ÷ m.", "working": working},
        {"value": force + mass,  "summary": "Incorrect.", "mistake": "You used the formula incorrectly. a = F ÷ m.", "working": working},
        {"value": round(mass / force, 2), "summary": "Incorrect.", "mistake": "You divided m by F instead of F by m. a = F ÷ m.", "working": working},
    ]
    return make_question(question, correct, options_data, "m/s²",
                         notes=NOTES["dynamics_newton"], topic="Dynamics", question_type="Acceleration", level=level)


def gen_find_m(level="N5"):
    accel = random.randint(2, 5)
    force = random.randint(10, 50)
    correct = round(force / accel, 2)
    working = _working_m(force, accel, correct)
    question = f"What is the mass of an object accelerating at {accel} m/s² if {force} N of force is applied?"
    options_data = [
        {"value": correct,       "summary": "Correct!", "mistake": None, "working": working},
        {"value": force * accel, "summary": "Incorrect.", "mistake": "You multiplied F × a instead of dividing. m = F ÷ a.", "working": working},
        {"value": force + accel, "summary": "Incorrect.", "mistake": "You used F = ma incorrectly. m = F ÷ a.", "working": working},
        {"value": round(accel / force, 2), "summary": "Incorrect.", "mistake": "You divided a by F. m = F ÷ a.", "working": working},
    ]
    return make_question(question, correct, options_data, "kg",
                         notes=NOTES["dynamics_newton"], topic="Dynamics", question_type="Acceleration", level=level)


def gen_find_f(level="N5"):
    mass  = random.randint(2, 10)
    accel = random.randint(2, 5)
    correct = mass * accel
    working = _working_f(mass, accel, correct)
    question = f"What is the force on a {mass} kg object accelerating at {accel} m/s²?"
    options_data = [
        {"value": correct,      "summary": "Correct!", "mistake": None, "working": working},
        {"value": mass + accel, "summary": "Incorrect.", "mistake": "You added m and a instead of multiplying. F = m × a.", "working": working},
        {"value": mass * (accel + 1), "summary": "Incorrect.", "mistake": "You used the equation incorrectly. F = m × a.", "working": working},
        {"value": round(mass / accel, 2), "summary": "Incorrect.", "mistake": "You divided m by a instead of multiplying. F = m × a.", "working": working},
    ]
    return make_question(question, correct, options_data, "N",
                         notes=NOTES["dynamics_newton"], topic="Dynamics", question_type="Acceleration", level=level)


_N4_GENS  = [gen_find_a]
_ALL_GENS = [gen_find_a, gen_find_m, gen_find_f]


def generate_acceleration(level="N5"):
    gens = _N4_GENS if level == "N4" else _ALL_GENS
    return random.choice(gens)(level=level)
