import random
import math
import pathlib
from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question
from utils.notes import NOTES

_FBD_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "free_body_diagram_widget.html"
).read_text(encoding="utf-8")


def _with_fbd_widget(question):
    question.metadata["widget_html"] = _FBD_WIDGET_HTML
    return question


def _dedup(options_data, correct):
    """Remove distractor entries whose value equals the correct answer or another distractor."""
    seen = {round(float(correct), 4)}
    cleaned = []
    for opt in options_data:
        key = round(float(opt["value"]), 4)
        if key not in seen:
            seen.add(key)
            cleaned.append(opt)
        elif opt["mistake"] is None:
            cleaned.insert(0, opt)
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


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
    options_data = _dedup(options_data, correct)
    return _with_fbd_widget(make_question(question, correct, options_data, "N",
                         scaffold=[
                             {"question": "Calculate the unbalanced force.", "answer": resultant, "unit": "N"},
                             {"question": "Calculate the frictional force.", "answer": correct, "unit": "N"},
                         ],
                         notes=NOTES["dynamics_newton"],
                         topic="Dynamics", question_type="Forces", level=level))


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
    options_data = _dedup(options_data, correct)
    return _with_fbd_widget(make_question(question, correct, options_data, "N",
                         scaffold=[
                             {"question": "Calculate the unbalanced force.", "answer": resultant, "unit": "N"},
                             {"question": "Calculate the driving force.", "answer": correct, "unit": "N"},
                         ],
                         notes=NOTES["dynamics_newton"],
                         topic="Dynamics", question_type="Forces", level=level))


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
    options_data = _dedup(options_data, correct)
    return _with_fbd_widget(make_question(question, correct, options_data, "m/s²",
                         scaffold=[
                             {"question": "Calculate the unbalanced force.", "answer": resultant, "unit": "N"},
                             {"question": "Calculate the acceleration.", "answer": correct, "unit": "m/s²"},
                         ],
                         notes=NOTES["dynamics_newton"],
                         topic="Dynamics", question_type="Forces", level=level))


def _two_forces_working(mass, force_a, force_b, friction, answer):
    combined = force_a + force_b
    resultant = combined - friction
    return [
        {"type": "text",  "content": "Step 1: Add the two forces pulling in the same direction"},
        {"type": "latex", "content": rf"F_{{combined}} = {force_a} + {force_b} = {combined}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Step 2: Subtract friction to find the resultant force"},
        {"type": "latex", "content": rf"F_{{resultant}} = {combined} - {friction} = {resultant}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Step 3: Apply Newton's Second Law"},
        {"type": "latex", "content": r"a = \frac{F}{m}"},
        {"type": "latex", "content": rf"a = \frac{{{resultant}}}{{{mass}}}"},
        {"type": "latex", "content": rf"a = {answer}\ \mathrm{{m/s^2}}"},
    ]


def gen_missing_acceleration_two_forces(level="N5"):
    mass     = random.randint(15, 60)
    force_a  = random.randint(30, 80)
    force_b  = random.randint(20, 60)
    combined = force_a + force_b
    friction = random.randint(10, combined - 5)
    resultant = combined - friction
    correct  = round(resultant / mass, 2)

    working = _two_forces_working(mass, force_a, force_b, friction, correct)
    question = (f"An object of mass {mass} kg is pulled forward by two ropes with forces of "
                f"{force_a} N and {force_b} N. Friction acts backward on the object with a force "
                f"of {friction} N. Calculate the acceleration of the object.")
    options_data = [
        {"value": correct,                                  "summary": "Correct!", "mistake": None, "working": working},
        {"value": round(combined / mass, 2),                "summary": "Incorrect.", "mistake": "You forgot to subtract friction before dividing by mass.", "working": working},
        {"value": round((force_a - friction) / mass, 2),    "summary": "Incorrect.", "mistake": "You only used one of the two forward forces — add both ropes' forces together first.", "working": working},
        {"value": round(resultant / mass + force_b / mass, 2), "summary": "Incorrect.", "mistake": "Check your working — combine the two forward forces, then subtract friction, then divide by mass.", "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return _with_fbd_widget(make_question(question, correct, options_data, "m/s²",
                         scaffold=[
                             {"question": "What is the combined forward force?", "answer": combined, "unit": "N"},
                             {"question": "What is the resultant (unbalanced) force?", "answer": resultant, "unit": "N"},
                             {"question": "What is the acceleration?", "answer": correct, "unit": "m/s²"},
                         ],
                         notes=NOTES["dynamics_newton"],
                         topic="Dynamics", question_type="Forces", level=level))


_ALL_GENS = [gen_missing_friction, gen_missing_driving, gen_missing_acceleration,
             gen_missing_acceleration_two_forces]


def generate_forces(level="N5"):
    return random.choice(_ALL_GENS)(level=level)


def gen_horizontal_forces(level="N5"):
    """Finding acceleration, friction or driving force for horizontal motion."""
    return generate_forces(level=level)


# ── Explain: comparing forward and backward forces during a stage of motion ─

_COMPARE_CASES = [
    ("speeding up", "greater than"),
    ("travelling at a constant, steady speed", "equal to"),
    ("slowing down", "less than"),
]
_COMPARE_SUBJECTS = ["cyclist", "car", "runner", "van", "motorbike", "skateboarder"]


def gen_compare_forces(level="N5"):
    subject = random.choice(_COMPARE_SUBJECTS)
    phase, answer_key = random.choice(_COMPARE_CASES)

    phrasing = {
        "greater than": "greater than",
        "equal to": "equal to",
        "less than": "less than",
    }
    reasoning = {
        "greater than": "unbalanced, acting forward — this speeds the object up",
        "equal to": "balanced — this keeps the object's speed constant",
        "less than": "unbalanced, acting backward — this slows the object down",
    }

    question_text = (
        f"A {subject} is {phase} along a flat, straight road.\n\n"
        f"How does the size of the forward (driving) force compare with the size of the "
        f"backward force (friction and air resistance) acting on the {subject}?"
    )
    working = [
        {"type": "text", "content": f"The {subject} is {phase}, so the forces acting on it must be "
                                     f"{reasoning[answer_key]}."},
        {"type": "text", "content": f"The forward force is {phrasing[answer_key]} the backward force."},
    ]
    correct = f"The forward force is {phrasing[answer_key]} the backward force."
    mistake_text = {
        "greater than": "A forward force bigger than the backward force gives an unbalanced forward force, "
                        "which speeds the object up — that's not this motion.",
        "equal to": "Equal forward and backward forces are balanced, which keeps speed constant — that's not "
                    "this motion.",
        "less than": "A backward force bigger than the forward force gives an unbalanced backward force, "
                     "which slows the object down — that's not this motion.",
    }
    distractors = []
    for key in phrasing:
        if key == answer_key:
            continue
        distractors.append({
            "value": f"The forward force is {phrasing[key]} the backward force.",
            "mistake": mistake_text[key],
            "working": working,
        })

    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)

    return PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        distractors=distractors,
        working=working,
        notes=NOTES["dynamics_newton"],
        topic="Dynamics",
        question_type="Forces",
        level=level,
        metadata={"type": "classification", "options": options},
    )


# ── Resultant of two forces acting at right angles ───────────────────────────

_RESULTANT_FORCE_SCENARIOS = [
    ("cyclist", "pushes forward with a force of", "A crosswind exerts a force of",
     "at right angles to the direction of travel", "the forward force"),
    ("aircraft's engines", "provide a forward thrust of", "A crosswind produces a force of",
     "at right angles to the thrust", "the thrust"),
    ("boat's engine", "provides a forward force of", "A river current pushes on the boat with a force of",
     "at right angles to the engine force", "the engine force"),
    ("go-kart", "is driven forward with a force of", "A gust of wind exerts a force of",
     "at right angles to the direction of travel", "the driving force"),
]


def gen_resultant_force_magnitude(level="N5"):
    subject, verb, perp_phrase, perp_qualifier, ref_name = random.choice(_RESULTANT_FORCE_SCENARIOS)
    f1 = random.randint(150, 600)
    f2 = random.randint(30, max(31, round(f1 * 0.6)))
    magnitude = round(math.sqrt(f1 ** 2 + f2 ** 2), 1)

    question = (f"The {subject} {verb} {f1} N. {perp_phrase} {f2} N {perp_qualifier}.\n\n"
                f"Calculate the magnitude of the resultant force.")
    working = [
        {"type": "text", "content": "The two forces act at right angles, so use Pythagoras' theorem:"},
        {"type": "latex", "content": r"R = \sqrt{F_1^2 + F_2^2}"},
        {"type": "latex", "content": rf"R = \sqrt{{{f1}^2 + {f2}^2}}"},
        {"type": "latex", "content": rf"R = {magnitude}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": magnitude, "mistake": None, "working": working},
        {"value": float(f1 + f2),
         "mistake": "You can't just add the two forces — they act at right angles, so use Pythagoras' theorem.",
         "working": working},
        {"value": float(abs(f1 - f2)),
         "mistake": "You can't just subtract the two forces — they act at right angles, so use Pythagoras' theorem.",
         "working": working},
        {"value": round(f1 ** 2 + f2 ** 2, 1),
         "mistake": "That's R² — remember to take the square root to get the resultant force itself.",
         "working": working},
    ]
    options_data = _dedup(options_data, magnitude)
    scaffold = [
        {"question": "What is R² (F₁² + F₂²)?", "answer": round(f1 ** 2 + f2 ** 2, 1)},
        {"question": "What is the magnitude of the resultant force?", "answer": magnitude},
    ]
    return make_question(question, magnitude, options_data, "N", scaffold=scaffold,
                         notes=NOTES["dynamics_newton"], topic="Dynamics", question_type="Forces", level=level)


def gen_resultant_force_direction(level="N5"):
    subject, verb, perp_phrase, perp_qualifier, ref_name = random.choice(_RESULTANT_FORCE_SCENARIOS)
    f1 = random.randint(150, 600)
    f2 = random.randint(30, max(31, round(f1 * 0.6)))
    angle = round(math.degrees(math.atan(f2 / f1)), 1)
    angle_swapped = round(90 - angle, 1)
    angle_wrong_ratio = round(math.degrees(math.atan(f1 / f2)), 1)

    question = (f"The {subject} {verb} {f1} N. {perp_phrase} {f2} N {perp_qualifier}.\n\n"
                f"Calculate the direction of the resultant force relative to {ref_name}.")
    working = [
        {"type": "text", "content": f"Use trigonometry, measuring the angle from {ref_name}:"},
        {"type": "latex", "content": rf"\tan\theta = \frac{{{f2}}}{{{f1}}}"},
        {"type": "latex", "content": rf"\theta = {angle}°"},
    ]
    options_data = [
        {"value": angle, "display": f"{angle}°", "mistake": None, "working": working},
        {"value": angle_swapped, "display": f"{angle_swapped}°",
         "mistake": f"That's 90° minus the correct angle — θ is measured from {ref_name} itself, not from "
                    f"the perpendicular force.",
         "working": working},
        {"value": angle_wrong_ratio, "display": f"{angle_wrong_ratio}°",
         "mistake": f"Check which force goes on top of the fraction — tan θ = (perpendicular force) ÷ "
                    f"({ref_name}), not the other way round.",
         "working": working},
    ]
    options_data = _dedup(options_data, angle)
    scaffold = [
        {"question": "What is tan θ (perpendicular force ÷ reference force)?", "answer": round(f2 / f1, 3)},
        {"question": "What is θ, the direction of the resultant force?", "answer": angle},
    ]
    return make_question(question, angle, options_data, "°", scaffold=scaffold,
                         notes=NOTES["dynamics_newton"], topic="Dynamics", question_type="Forces", level=level)


def gen_resultant_force(level="N5"):
    return random.choice([gen_resultant_force_magnitude, gen_resultant_force_direction])(level=level)
