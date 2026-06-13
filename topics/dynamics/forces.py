import random
from utils.make_question import make_question
from utils.notes import NOTES


def _friction_working(mass, driving_force, accel, answer):
    resultant = mass * accel
    return [
        {"type": "text",  "content": "Step 1: Find the resultant (unbalanced) force using Newton's Second Law"},
        {"type": "latex", "content": r"F_{\text{resultant}} = ma"},
        {"type": "latex", "content": rf"F_{{resultant}} = {mass} \times {accel}"},
        {"type": "latex", "content": rf"F_{{resultant}} = {resultant}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Step 2: Use driving force minus resultant force"},
        {"type": "latex", "content": r"F_{\text{friction}} = F_{\text{driving}} - F_{\text{resultant}}"},
        {"type": "latex", "content": rf"F_{{friction}} = {driving_force} - {resultant}"},
        {"type": "latex", "content": rf"F_{{friction}} = {answer}\ \mathrm{{N}}"},
    ]


def _driving_working(mass, accel, friction_force, answer):
    resultant = mass * accel
    return [
        {"type": "text",  "content": "Step 1: Find resultant force using Newton's Second Law"},
        {"type": "latex", "content": r"F_{\text{resultant}} = ma"},
        {"type": "latex", "content": rf"F_{{resultant}} = {mass} \times {accel}"},
        {"type": "latex", "content": rf"F_{{resultant}} = {resultant}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Step 2: Add friction to get driving force"},
        {"type": "latex", "content": r"F_{\text{driving}} = F_{\text{resultant}} + F_{\text{friction}}"},
        {"type": "latex", "content": rf"F_{{driving}} = {resultant} + {friction_force}"},
        {"type": "latex", "content": rf"F_{{driving}} = {answer}\ \mathrm{{N}}"},
    ]


def _accel_working(mass, driving_force, friction_force, answer):
    resultant = driving_force - friction_force
    return [
        {"type": "text",  "content": "Step 1: Find resultant force"},
        {"type": "latex", "content": r"F_{\text{resultant}} = F_{\text{driving}} - F_{\text{friction}}"},
        {"type": "latex", "content": rf"F_{{resultant}} = {driving_force} - {friction_force}"},
        {"type": "latex", "content": rf"F_{{resultant}} = {resultant}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Step 2: Apply Newton's Second Law"},
        {"type": "latex", "content": r"a = \frac{F}{m}"},
        {"type": "latex", "content": rf"a = \frac{{{resultant}}}{{{mass}}}"},
        {"type": "latex", "content": rf"a = {answer}\ \mathrm{{m/s^2}}"},
    ]


def gen_missing_friction(level="N5"):
    mass          = random.randint(2, 10)
    driving_force = random.randint(10, 50)
    acceleration  = random.randint(2, 5)
    resultant     = mass * acceleration
    correct       = driving_force - resultant

    if correct <= 0:
        return gen_missing_friction(level)

    working = _friction_working(mass, driving_force, acceleration, correct)
    question = (f"What is the frictional force acting on an object of mass {mass} kg "
                f"if the acceleration is {acceleration} m/s² and the driving force is {driving_force} N?")
    options_data = [
        {"value": correct,                       "summary": "Correct!", "mistake": None, "working": working},
        {"value": resultant,                     "summary": "Incorrect.", "mistake": "You've calculated the unbalanced force, not the friction.", "working": working},
        {"value": driving_force + resultant,     "summary": "Incorrect.", "mistake": "You added the unbalanced force and driving force. Friction = driving force − unbalanced force.", "working": working},
        {"value": abs(resultant - driving_force),"summary": "Incorrect.", "mistake": "Check the direction of subtraction. Friction = driving force − unbalanced force.", "working": working},
    ]
    return make_question(question, correct, options_data, "N",
                         scaffold=[
                             {"question": "Calculate the unbalanced force.", "answer": resultant, "unit": "N"},
                             {"question": "Calculate the frictional force.", "answer": correct, "unit": "N"},
                         ],
                         notes=NOTES["dynamics_newton"],
                         topic="Dynamics", question_type="Forces", level=level)


def gen_missing_driving(level="N5"):
    mass          = random.randint(2, 10)
    friction_force = random.randint(2, 50)
    acceleration  = random.randint(2, 5)
    resultant     = mass * acceleration
    correct       = resultant + friction_force

    working = _driving_working(mass, acceleration, friction_force, correct)
    question = (f"What is the driving force acting on an object of mass {mass} kg "
                f"if the acceleration is {acceleration} m/s² and the frictional force is {friction_force} N?")
    options_data = [
        {"value": correct,                      "summary": "Correct!", "mistake": None, "working": working},
        {"value": resultant,                    "summary": "Incorrect.", "mistake": "Remember, driving force = unbalanced force + friction.", "working": working},
        {"value": abs(friction_force - resultant), "summary": "Incorrect.", "mistake": "You subtracted instead of adding. Driving force = unbalanced force + friction.", "working": working},
        {"value": friction_force,               "summary": "Incorrect.", "mistake": "This is only the friction, not the driving force.", "working": working},
    ]
    return make_question(question, correct, options_data, "N",
                         scaffold=[
                             {"question": "Calculate the unbalanced force.", "answer": resultant, "unit": "N"},
                             {"question": "Calculate the driving force.", "answer": correct, "unit": "N"},
                         ],
                         notes=NOTES["dynamics_newton"],
                         topic="Dynamics", question_type="Forces", level=level)


def gen_missing_acceleration(level="N5"):
    mass          = random.randint(2, 10)
    driving_force = random.randint(10, 50)
    friction_force = random.randint(2, driving_force - 1)
    resultant     = driving_force - friction_force
    correct       = round(resultant / mass, 2)

    working = _accel_working(mass, driving_force, friction_force, correct)
    question = (f"What is the acceleration of an object of mass {mass} kg "
                f"with driving force {driving_force} N and friction {friction_force} N?")
    options_data = [
        {"value": correct,                              "summary": "Correct!", "mistake": None, "working": working},
        {"value": round(driving_force / mass, 2),       "summary": "Incorrect.", "mistake": "Remember to work out the unbalanced force first before dividing by mass.", "working": working},
        {"value": round(friction_force / mass, 2),      "summary": "Incorrect.", "mistake": "Remember to work out the unbalanced force first before dividing by mass.", "working": working},
        {"value": round((driving_force + friction_force) / mass, 2), "summary": "Incorrect.", "mistake": "The unbalanced force is the DIFFERENCE between driving force and friction, not the sum.", "working": working},
    ]
    return make_question(question, correct, options_data, "m/s²",
                         scaffold=[
                             {"question": "Calculate the unbalanced force.", "answer": resultant, "unit": "N"},
                             {"question": "Calculate the acceleration.", "answer": correct, "unit": "m/s²"},
                         ],
                         notes=NOTES["dynamics_newton"],
                         topic="Dynamics", question_type="Forces", level=level)


_ALL_GENS = [gen_missing_friction, gen_missing_driving, gen_missing_acceleration]


def generate_forces(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
