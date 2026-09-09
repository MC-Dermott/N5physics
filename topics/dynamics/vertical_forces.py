import random
import pathlib
from utils.make_question import make_question
from utils.notes import NOTES

G = 9.8

_FBD_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "free_body_diagram_widget.html"
).read_text(encoding="utf-8")


def _with_fbd_widget(question):
    question.metadata["widget_html"] = _FBD_WIDGET_HTML
    return question


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


# (label, phrase, mass_lo, mass_hi, excess_factor_lo, excess_factor_hi) — the
# applied force is drawn as a multiple of the object's own weight (not an
# independent N range), so the net force stays a realistic, modest excess
# over weight regardless of the object's scale (matches the worksheet's
# helicopter/balloon/rocket examples, all roughly 1.1-1.4x weight).
_LIFTOFF_SCENARIOS = [
    ("helicopter", "the rotor blades provide an upward lift force of", 1000, 3000, 1.08, 1.25),
    ("weather balloon", "it experiences an upward buoyancy force of", 1, 10, 1.15, 1.45),
    ("rocket", "the engines provide an upward thrust of", 1500, 5000, 1.15, 1.35),
    ("hot air balloon", "its burner provides an upward lift force of", 200, 800, 1.10, 1.30),
]


def _draw_liftoff():
    label, phrase, m_lo, m_hi, x_lo, x_hi = random.choice(_LIFTOFF_SCENARIOS)
    mass = random.randint(m_lo, m_hi)
    weight = round(mass * G, 1)
    factor = random.uniform(x_lo, x_hi)
    applied = round(weight * factor / 10) * 10  # round to nearest 10 N
    if applied <= weight:
        applied = round(weight) + 10
    return label, phrase, mass, applied, weight


def gen_vertical_liftoff_accel(level="N5"):
    label, phrase, mass, applied, weight = _draw_liftoff()
    net = round(applied - weight, 1)
    correct = round(net / mass, 2)

    working = [
        {"type": "text",  "content": "Step 1: Find the weight"},
        {"type": "latex", "content": rf"W = mg = {mass} \times {G} = {weight}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Step 2: Find the net (unbalanced) upward force"},
        {"type": "latex", "content": rf"F_{{net}} = {applied} - {weight} = {net}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Step 3: Apply Newton's Second Law"},
        {"type": "latex", "content": rf"a = \frac{{F_{{net}}}}{{m}} = \frac{{{net}}}{{{mass}}} = {correct}\ \mathrm{{m/s^2}}"},
    ]
    question = (f"A {label} has a mass of {mass} kg. As it takes off vertically, "
                f"{phrase} {applied} N. Calculate its acceleration. (g = {G} N/kg)")
    forgot_weight = round(applied / mass, 2)
    swapped = round(abs(weight - applied) / mass, 2)
    options_data = [
        {"value": correct,        "mistake": None, "working": working},
        {"value": forgot_weight,  "mistake": "You divided the applied force straight by mass — first subtract the weight to find the net force.", "working": working},
        {"value": round(weight / mass, 2), "mistake": "That's g again, not the acceleration — you need the NET force (applied − weight) divided by mass.", "working": working},
    ]
    options_data = _dedup(options_data, correct)
    scaffold = [
        {"question": "What is the weight?", "answer": weight, "unit": "N"},
        {"question": "What is the net (unbalanced) force?", "answer": net, "unit": "N"},
        {"question": "What is the acceleration?", "answer": correct, "unit": "m/s²"},
    ]
    return _with_fbd_widget(make_question(question, correct, options_data, "m/s²", scaffold=scaffold,
                         notes=NOTES["unbalanced_forces_s3"], topic="Dynamics",
                         question_type="Vertical Forces", level=level))


# (label, mass_lo, mass_hi) for the free-falling/parachute-deceleration scenarios.
_SKYDIVE_CONTEXTS = [
    ("skydiver", 55, 95),
    ("parachutist", 60, 100),
]


def gen_freefall_acceleration(level="N5"):
    label, m_lo, m_hi = random.choice(_SKYDIVE_CONTEXTS)
    mass = random.randint(m_lo, m_hi)
    t = random.randint(8, 15)
    a_target = round(random.uniform(3.5, 8.5), 1)
    v = round(a_target * t, 1)
    correct = round(v / t, 2)

    working = [
        {"type": "text",  "content": "The skydiver starts from rest, so u = 0. Use a = (v − u) ÷ t:"},
        {"type": "latex", "content": r"a = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"a = \frac{{{v} - 0}}{{{t}}} = {correct}\ \mathrm{{m/s^2}}"},
    ]
    question = (f"A {label} of mass {mass} kg jumps from a plane. In the first {t} s, before "
                f"reaching a constant speed, their velocity increases from 0 to {v} m/s. "
                f"Calculate their acceleration during this time.")
    options_data = [
        {"value": correct,             "mistake": None, "working": working},
        {"value": round(v * t, 2),     "mistake": "You multiplied v × t instead of dividing. a = (v − u) ÷ t.", "working": working},
        {"value": mass,                "mistake": "That's the mass, not the acceleration — mass isn't needed for a = (v − u) ÷ t.", "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return make_question(question, correct, options_data, "m/s²",
                         notes=NOTES["acceleration_s3"], topic="Dynamics",
                         question_type="Vertical Forces", level=level)


def gen_parachute_deceleration(level="N5"):
    label, m_lo, m_hi = random.choice(_SKYDIVE_CONTEXTS)
    mass = random.randint(m_lo, m_hi)
    v1 = random.randint(40, 58)
    v2 = random.randint(5, 12)
    t = random.randint(3, 8)
    delta_v = v1 - v2
    correct = round(delta_v / t, 2)

    working = [
        {"type": "text",  "content": "Step 1: Find the change in speed"},
        {"type": "latex", "content": rf"\Delta v = v - u = {v2} - {v1} = {-delta_v}\ \mathrm{{m/s}}"},
        {"type": "text",  "content": "Step 2: Divide by the time taken to get the deceleration"},
        {"type": "latex", "content": rf"a = \frac{{\Delta v}}{{t}} = \frac{{{delta_v}}}{{{t}}} = {correct}\ \mathrm{{m/s^2}}"},
    ]
    question = (f"A {label} of mass {mass} kg opens their parachute while falling at {v1} m/s. "
                f"Over the next {t} s, their speed decreases to {v2} m/s. "
                f"Calculate the size of their deceleration.")
    options_data = [
        {"value": correct,                      "mistake": None, "working": working},
        {"value": round((v1 + v2) / t, 2),      "mistake": "You added the two speeds instead of subtracting them. Δv = v₁ − v₂.", "working": working},
        {"value": round(v1 / t, 2),             "mistake": "You ignored the final speed — you need the CHANGE in speed, not just the starting speed.", "working": working},
    ]
    options_data = _dedup(options_data, correct)
    scaffold = [
        {"question": "What is the change in speed (Δv)?", "answer": delta_v, "unit": "m/s"},
        {"question": "What is the deceleration?", "answer": correct, "unit": "m/s²"},
    ]
    return make_question(question, correct, options_data, "m/s²", scaffold=scaffold,
                         notes=NOTES["acceleration_s3"], topic="Dynamics",
                         question_type="Vertical Forces", level=level)


_ALL_GENS = [gen_vertical_liftoff_accel, gen_freefall_acceleration, gen_parachute_deceleration]


def generate_vertical_forces(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
