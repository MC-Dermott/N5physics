import random
import pathlib
from utils.make_question import make_question
from utils.notes import NOTES
from topics.dynamics.forces import generate_forces

_FBD_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "free_body_diagram_widget.html"
).read_text(encoding="utf-8")


def _with_fbd_widget(question):
    question.metadata["widget_html"] = _FBD_WIDGET_HTML
    return question

G = 9.8


def gen_horizontal_unbalanced_force(level="S3"):
    """Reuses forces.py's driving-vs-friction generators (same F_unbalanced = F_driving -
    F_friction / F = ma family the worksheet's Q1/Q4 test), just relabelled so the
    recorded question_type matches this S3 topic instead of forces.py's own "Forces"."""
    q = generate_forces(level=level)
    q.question_type = "Unbalanced Forces"
    return q

# (label, mass_lo, mass_hi, applied_lo, applied_hi) — applied force is checked
# against weight below to guarantee a positive (upward) unbalanced force.
_SCENARIOS = [
    ("rocket", "the rocket's engines produce a thrust of", 500, 3000, 8000, 40000),
    ("hot air balloon", "its burner produces a lift force of", 200, 800, 3000, 10000),
    ("crane-lifted mass", "the crane's cable pulls upward with a force of", 5, 50, 100, 700),
    ("drone", "its rotors produce an upward force of", 1, 5, 20, 80),
]


def _draw_scenario():
    label, phrase, m_lo, m_hi, f_lo, f_hi = random.choice(_SCENARIOS)
    for _ in range(20):
        mass = random.randint(m_lo, m_hi)
        applied = random.randint(f_lo, f_hi)
        weight = round(mass * G, 2)
        if applied > weight * 1.15:  # comfortably positive unbalanced force
            break
    return label, phrase, mass, applied, weight


def _round3(x):
    return float(f"{x:.3g}")


def _dedup(options_data, correct):
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


def gen_vertical_unbalanced_force(level="S3"):
    label, phrase, mass, applied, weight = _draw_scenario()
    unbalanced = _round3(applied - weight)
    accel = _round3(unbalanced / mass)

    working = [
        {"type": "text",  "content": "First find the weight, then subtract it from the applied force:"},
        {"type": "latex", "content": r"W = mg"},
        {"type": "latex", "content": rf"W = {mass} \times {G} = {weight}\ \mathrm{{N}}"},
        {"type": "latex", "content": r"F_{\text{unbalanced}} = F_{\text{applied}} - W"},
        {"type": "latex", "content": rf"F_{{unbalanced}} = {applied} - {weight}"},
        {"type": "latex", "content": rf"F_{{unbalanced}} = {unbalanced}\ \mathrm{{N}}"},
    ]
    question = (
        f"A {label} of mass {mass} kg is launching vertically — {phrase} {applied} N.\n\n"
        f"Calculate the unbalanced force acting on the {label}."
    )
    forgot_weight = float(applied)
    swapped = _round3(weight - applied)
    options_data = [
        {"value": unbalanced, "mistake": None, "working": working},
        {"value": forgot_weight,
         "mistake": "That's just the applied force — you need to subtract the weight to find the "
                    "unbalanced force.",
         "working": working},
        {"value": swapped,
         "mistake": "You calculated weight − applied force instead of applied force − weight.",
         "working": working},
    ]
    options_data = _dedup(options_data, unbalanced)
    scaffold = [
        {"question": "What is the weight of the object?", "answer": weight},
        {"question": "What is the unbalanced force?", "answer": unbalanced},
    ]
    return _with_fbd_widget(make_question(question, unbalanced, options_data, "N", scaffold=scaffold,
                         notes=NOTES["unbalanced_forces_s3"], topic="Dynamics",
                         question_type="Unbalanced Forces", level=level))


def gen_vertical_acceleration(level="S3"):
    label, phrase, mass, applied, weight = _draw_scenario()
    unbalanced = round(applied - weight, 2)
    accel = _round3(unbalanced / mass)

    working = [
        {"type": "text",  "content": "Find the weight, then the unbalanced force, then the acceleration:"},
        {"type": "latex", "content": rf"W = mg = {mass} \times {G} = {weight}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"F_{{unbalanced}} = {applied} - {weight} = {unbalanced}\ \mathrm{{N}}"},
        {"type": "latex", "content": r"a = \frac{F_{\text{unbalanced}}}{m}"},
        {"type": "latex", "content": rf"a = \frac{{{unbalanced}}}{{{mass}}}"},
        {"type": "latex", "content": rf"a = {accel}\ \mathrm{{m/s^2}}"},
    ]
    question = (
        f"A {label} of mass {mass} kg is launching vertically — {phrase} {applied} N.\n\n"
        f"Calculate the {label}'s acceleration."
    )
    forgot_weight_accel = _round3(applied / mass)
    options_data = [
        {"value": accel, "mistake": None, "working": working},
        {"value": forgot_weight_accel,
         "mistake": "You divided the applied force straight by mass — first subtract the weight to "
                    "get the unbalanced force, then divide that by mass.",
         "working": working},
    ]
    options_data = _dedup(options_data, accel)
    scaffold = [
        {"question": "What is the weight of the object?", "answer": weight},
        {"question": "What is the unbalanced force?", "answer": unbalanced},
        {"question": "What is the acceleration?", "answer": accel},
    ]
    return _with_fbd_widget(make_question(question, accel, options_data, "m/s²", scaffold=scaffold,
                         notes=NOTES["unbalanced_forces_s3"], topic="Dynamics",
                         question_type="Unbalanced Forces", level=level))


def generate_unbalanced_forces_s3(level="S3"):
    return random.choice([gen_vertical_unbalanced_force, gen_vertical_acceleration])(level=level)
