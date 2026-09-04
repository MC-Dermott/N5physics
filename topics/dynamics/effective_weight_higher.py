import random
import pathlib
from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

_G = 9.8

_LIFT_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "effective_weight_widget.html"
).read_text(encoding="utf-8")


def _with_lift_widget(question):
    question.metadata["widget_html"] = _LIFT_WIDGET_HTML
    question.metadata["widget_height"] = 700
    return question

_NOTES = """
## Effective Weight

**Relationships needed:**
$$F = ma$$
$$W = mg$$

**Key idea:** the reading on a scale (or any supporting force) is not always equal to an
object's true weight — it depends on whether the object is accelerating.

- **Upwards acceleration → increase in effective weight** (reading > weight): \
$$R - mg = ma \\implies R = mg + ma$$
- **Downwards acceleration → decrease in effective weight** (reading < weight): \
$$mg - R = ma \\implies R = mg - ma$$
- **Constant velocity (a = 0) → reading equals true weight:** $$R = mg$$

**Which way does the acceleration act?** Compare the direction of *motion* with whether the
object is *speeding up* or *slowing down*:
- Speeding up while moving up, or slowing down while moving down → acceleration is **upwards**.
- Speeding up while moving down, or slowing down while moving up → acceleration is **downwards**.

**Worked Example:** A person of mass 70 kg stands on bathroom scales inside a lift. The lift
is moving upwards but slowing down at a rate of 1.5 m/s². Calculate the reading R on the
scales.

The lift moves upwards but is slowing down, so its acceleration acts downwards — the reading
R is less than the weight W.
$$mg - R = ma$$
$$(70 \\times 9.8) - R = 70 \\times 1.5$$
$$R = 686 - 105 = 581\\ \\mathrm{N}$$

> **Important:** The same physics applies beyond lifts — a crane cable's tension, a rocket's
> thrust, or the force a drone's platform exerts on a parcel all follow the same F = ma / W = mg
> reasoning. In true free fall, the only force acting is gravity, so a supporting force reads 0 N.
"""

# Each context is tied to its own plausible mass range, so a generated question never pairs
# (e.g.) an "engineer" with a 6 kg mass.
_LIFT_KINDS = [
    ("woman", 45, 70),
    ("man", 65, 95),
    ("passenger", 50, 100),
    ("engineer", 60, 100),
    ("delivery worker", 55, 90),
]

_OBJECT_KINDS = [
    ("suitcase", 5, 40),
    ("toolbox", 5, 30),
    ("crate", 10, 60),
]

# (noun phrase, clause following "of mass X kg", force name, mass_lo, mass_hi, g, note,
#  fixed_direction) — fixed_direction is True/False if the scenario only makes sense moving
# one way (e.g. a crate "lowered" by a cable can't then be "moving upwards"), else None to
# pick randomly. The mass sits right after the noun (e.g. "A crate of mass 45 kg is lowered
# by..."), matching the worksheet's own phrasing rather than tacking "of mass X kg" onto the
# end of a long descriptive clause.
_BEYOND_CONTEXTS = [
    ("A crate", "is lowered by a crane cable", "the tension in the cable", 20, 300, _G, "", False),
    ("An astronaut", "is seated in a rocket during launch",
     "the force exerted on the astronaut by their seat", 60, 100, _G, "", True),
    ("A parcel", "sits on a delivery drone's platform", "the force exerted by the platform on the parcel", 1, 12, _G, "", None),
    ("A lunar lander", "descends towards the surface of the Moon",
     "the thrust force produced by the lander's engines", 800, 3000, 1.6,
     " (the gravitational field strength on the Moon is 1.6 N/kg)", False),
]


def _r1(val):
    return round(float(val), 1)


def _r2(val):
    return round(float(val), 2)


def _cap(s):
    return s[0].upper() + s[1:]


def _a(s):
    return "An" if s[0] in "aeiou" else "A"


def _direction_desc(moving_up, speeding_up):
    motion = "upwards" if moving_up else "downwards"
    change = "speeding up" if speeding_up else "slowing down"
    return motion, change


def _accel_is_up(moving_up, speeding_up):
    return moving_up == speeding_up


# ── Section 1: Lifts — find the reading, given mass and acceleration ────────

def gen_ew_find_reading(level="Higher"):
    name, lo, hi = random.choice(_LIFT_KINDS)
    m = random.randint(lo, hi)
    moving_up = random.choice([True, False])
    speeding_up = random.choice([True, False])
    a = round(random.uniform(0.5, 3.0), 1)
    accel_up = _accel_is_up(moving_up, speeding_up)
    motion, change = _direction_desc(moving_up, speeding_up)

    W = _r1(m * _G)
    F = _r1(m * a)
    R = _r1(W + F) if accel_up else _r1(W - F)

    question = (
        f"{_a(name)} {name} of mass {m} kg stands on bathroom scales inside a lift. "
        f"The lift is moving {motion} and {change} at a rate of {a} m/s². "
        f"Calculate the reading R on the scales."
    )
    working = [
        {"type": "text", "content": f"The resultant force acts {'upwards' if accel_up else 'downwards'}:"},
        {"type": "latex", "content": r"R - mg = ma" if accel_up else r"mg - R = ma"},
        {"type": "latex", "content": r"R = mg + ma" if accel_up else r"R = mg - ma"},
        {"type": "latex", "content": rf"R = ({m} \times {_G}) {'+' if accel_up else '-'} ({m} \times {a})"},
        {"type": "latex", "content": rf"R = {W} {'+' if accel_up else '-'} {F}"},
        {"type": "latex", "content": rf"R = {R}\ \mathrm{{N}}"},
    ]
    wrong_sign = _r1(W - F) if accel_up else _r1(W + F)
    options_data = [
        {"value": R, "mistake": None, "working": working},
        {"value": wrong_sign,
         "mistake": "You used the wrong sign — check whether the resultant force acts upwards or "
                    "downwards for this direction of motion and change in speed.",
         "working": working},
        {"value": F,
         "mistake": "This is just the resultant force (ma) — the scale reading also includes the "
                    "weight: R = mg ± ma.",
         "working": working},
        {"value": W,
         "mistake": "This is just the weight (mg) — it ignores the lift's acceleration: R = mg ± ma.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the person's weight, W = mg?", "answer": W},
        {"question": "What is the size of the resultant force, F = ma?", "answer": F},
        {"question": "What is the reading R on the scales?", "answer": R},
    ]
    return make_question(question, R, options_data, "N", scaffold=scaffold, notes=_NOTES,
                          topic="Our Dynamic Universe", question_type="Effective Weight", level=level)


def gen_ew_find_acceleration(level="Higher"):
    name, lo, hi = random.choice(_LIFT_KINDS)
    m = random.randint(lo, hi)
    moving_up = random.choice([True, False])
    speeding_up = random.choice([True, False])
    a = round(random.uniform(0.3, 2.5), 2)
    accel_up = _accel_is_up(moving_up, speeding_up)
    motion, change = _direction_desc(moving_up, speeding_up)

    W = _r1(m * _G)
    F = _r1(m * a)
    R = _r1(W + F) if accel_up else _r1(W - F)

    question = (
        f"{_a(name)} {name} of mass {m} kg stands on scales in a lift. The lift is moving "
        f"{motion} but {change} at a rate that causes the scales to read {R} N. "
        f"Calculate the rate at which the lift is {change}."
    )
    working = [
        {"type": "text", "content": f"The resultant force acts {'upwards' if accel_up else 'downwards'}:"},
        {"type": "latex", "content": r"R - mg = ma" if accel_up else r"mg - R = ma"},
        {"type": "latex", "content": rf"a = \frac{{R - mg}}{{m}}" if accel_up else rf"a = \frac{{mg - R}}{{m}}"},
        {"type": "latex", "content": rf"a = \frac{{{R} - {W}}}{{{m}}}" if accel_up else rf"a = \frac{{{W} - {R}}}{{{m}}}"},
        {"type": "latex", "content": rf"a = {a}\ \mathrm{{m/s^2}}"},
    ]
    diff = abs(_r1(R - W))
    options_data = [
        {"value": a, "mistake": None, "working": working},
        {"value": diff,
         "mistake": "You found the resultant force but forgot to divide by the mass: a = F ÷ m.",
         "working": working},
        {"value": _r2((R + W) / m),
         "mistake": "Check your equation — R and mg should be subtracted, not added, to find the "
                    "resultant force.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the person's weight, W = mg?", "answer": W},
        {"question": "What is the size of the resultant force (the difference between R and W)?", "answer": diff},
        {"question": "What is the acceleration a?", "answer": a},
    ]
    return make_question(question, a, options_data, "m/s²", scaffold=scaffold, notes=_NOTES,
                          topic="Our Dynamic Universe", question_type="Effective Weight", level=level)


def gen_ew_find_mass(level="Higher"):
    name, lo, hi = random.choice(_OBJECT_KINDS)
    m_true = random.randint(lo, hi)
    moving_up = random.choice([True, False])
    speeding_up = random.choice([True, False])
    a = round(random.uniform(0.5, 3.0), 1)
    accel_up = _accel_is_up(moving_up, speeding_up)
    motion, change = _direction_desc(moving_up, speeding_up)

    W = _r1(m_true * _G)
    F = _r1(m_true * a)
    R = _r1(W + F) if accel_up else _r1(W - F)
    m_calc = _r2(R / (_G + a)) if accel_up else _r2(R / (_G - a))

    question = (
        f"A {name} sits on scales inside a lift. The lift is moving {motion} but {change} "
        f"at a rate of {a} m/s². The scales read {R} N. Calculate the mass of the {name}."
    )
    working = [
        {"type": "text", "content": f"The resultant force acts {'upwards' if accel_up else 'downwards'}:"},
        {"type": "latex", "content": r"R = m(g + a)" if accel_up else r"R = m(g - a)"},
        {"type": "latex", "content": rf"m = \frac{{R}}{{g + a}}" if accel_up else rf"m = \frac{{R}}{{g - a}}"},
        {"type": "latex", "content": rf"m = \frac{{{R}}}{{{_G} + {a}}}" if accel_up else rf"m = \frac{{{R}}}{{{_G} - {a}}}"},
        {"type": "latex", "content": rf"m = {m_calc}\ \mathrm{{kg}}"},
    ]
    options_data = [
        {"value": m_calc, "mistake": None, "working": working},
        {"value": _r2(R / _G),
         "mistake": "You divided by g alone, ignoring the lift's acceleration: m = R ÷ (g ± a).",
         "working": working},
        {"value": _r2(R * (_G + a)) if accel_up else _r2(R * (_G - a)),
         "mistake": "You multiplied instead of dividing: m = R ÷ (g ± a).",
         "working": working},
    ]
    scaffold = [
        {"question": "Is the resultant force acting upwards or downwards here? (type 'up' or 'down')",
         "answer": "up" if accel_up else "down"},
        {"question": "What is the mass of the object?", "answer": m_calc},
    ]
    return make_question(question, m_calc, options_data, "kg", scaffold=scaffold, notes=_NOTES,
                          topic="Our Dynamic Universe", question_type="Effective Weight", level=level)


def gen_ew_uniform_accel_scenario(level="Higher"):
    name, lo, hi = random.choice(_LIFT_KINDS)
    m = random.randint(lo, hi)
    v = round(random.uniform(2.0, 6.0), 1)
    t = round(random.uniform(2.0, 5.0), 1)
    a = _r2(v / t)
    moving_up = random.choice([True, False])
    accel_up = moving_up  # starting from rest and speeding up, so acceleration matches direction of motion
    motion = "upwards" if moving_up else "downwards"

    W = _r1(m * _G)
    F = _r1(m * a)
    R = _r1(W + F) if accel_up else _r1(W - F)

    context = (
        f"A {name} of mass {m} kg stands on a platform in a lift. Starting from rest, the lift "
        f"moves {motion} and speeds up uniformly, reaching a velocity of {v} m/s after {t} s."
    )
    part_a = PhysicsQuestion(
        question_text="Calculate the acceleration of the lift.",
        correct_answer=a, unit="m/s²",
        topic="Our Dynamic Universe", question_type="Effective Weight", level=level,
        working=[
            {"type": "text", "content": "Use the equation of motion (u = 0, starting from rest):"},
            {"type": "latex", "content": r"v = u + at"},
            {"type": "latex", "content": rf"{v} = 0 + a \times {t}"},
            {"type": "latex", "content": rf"a = {a}\ \mathrm{{m/s^2}}"},
        ],
        notes=_NOTES,
    )
    part_b = PhysicsQuestion(
        question_text="Calculate the reading on the platform during this acceleration.",
        correct_answer=R, unit="N",
        topic="Our Dynamic Universe", question_type="Effective Weight", level=level,
        working=[
            {"type": "text", "content": f"The resultant force acts {'upwards' if accel_up else 'downwards'}:"},
            {"type": "latex", "content": r"R = mg + ma" if accel_up else r"R = mg - ma"},
            {"type": "latex", "content": rf"R = ({m} \times {_G}) {'+' if accel_up else '-'} ({m} \times {a})"},
            {"type": "latex", "content": rf"R = {R}\ \mathrm{{N}}"},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": "What is the platform's weight, W = mg?", "answer": W},
            {"prompt": "What is the reading R?", "answer": R},
        ],
    )
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Effective Weight", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


def generate_effective_weight_lifts(level="Higher"):
    return _with_lift_widget(random.choice([
        gen_ew_find_reading, gen_ew_find_acceleration, gen_ew_find_mass, gen_ew_uniform_accel_scenario,
    ])(level=level))


# ── Section 1: Lifts at constant speed ───────────────────────────────────────

def gen_ew_constant_velocity(level="Higher"):
    name, lo, hi = random.choice(_LIFT_KINDS)
    m = random.randint(lo, hi)
    speed = round(random.uniform(0.5, 3.0), 1)
    moving_up = random.choice([True, False])
    motion = "upwards" if moving_up else "downwards"
    W = _r1(m * _G)

    context = f"A lift moves {motion} at a constant speed of {speed} m/s, carrying a passenger of mass {m} kg."
    part_a = PhysicsQuestion(
        question_text="State the acceleration of the lift.",
        correct_answer=0, unit="m/s²",
        topic="Our Dynamic Universe", question_type="Effective Weight", level=level,
        working=[
            {"type": "text", "content": "The lift moves at a constant speed, so its velocity is not changing."},
            {"type": "latex", "content": r"a = 0\ \mathrm{m/s^2}"},
        ],
        notes=_NOTES,
    )
    part_b = PhysicsQuestion(
        question_text="Calculate the reading on scales carried by the passenger.",
        correct_answer=W, unit="N",
        topic="Our Dynamic Universe", question_type="Effective Weight", level=level,
        working=[
            {"type": "text", "content": "With zero acceleration, the resultant force is zero, so the reading equals the true weight:"},
            {"type": "latex", "content": r"R = mg"},
            {"type": "latex", "content": rf"R = {m} \times {_G} = {W}\ \mathrm{{N}}"},
        ],
        notes=_NOTES,
    )
    return _with_lift_widget(PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Effective Weight", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    ))


# ── Section 2: Apparent weight beyond lifts ──────────────────────────────────

def gen_beyond_find_force(level="Higher"):
    noun, clause, force_name, lo, hi, g, note, fixed_dir = random.choice(_BEYOND_CONTEXTS)
    m = random.randint(lo, hi)
    moving_up = fixed_dir if fixed_dir is not None else random.choice([True, False])
    speeding_up = random.choice([True, False])
    a_max = max(0.6, g * 0.75)
    a = round(random.uniform(0.3, a_max), 2)
    accel_up = _accel_is_up(moving_up, speeding_up)
    motion, change = _direction_desc(moving_up, speeding_up)

    W = _r1(m * g)
    F = _r1(m * a)
    force = _r1(W + F) if accel_up else _r1(W - F)

    question = (
        f"{noun} of mass {m} kg {clause}. It is moving {motion} and {change} at a rate of "
        f"{a} m/s²{note}. Calculate {force_name}."
    )
    working = [
        {"type": "text", "content": f"The resultant force acts {'upwards' if accel_up else 'downwards'}:"},
        {"type": "latex", "content": r"F = ma"},
        {"type": "latex", "content": rf"{force_name} = mg {'+' if accel_up else '-'} ma"},
        {"type": "latex", "content": rf"= ({m} \times {g}) {'+' if accel_up else '-'} ({m} \times {a})"},
        {"type": "latex", "content": rf"= {force}\ \mathrm{{N}}"},
    ]
    wrong_sign = _r1(W - F) if accel_up else _r1(W + F)
    options_data = [
        {"value": force, "mistake": None, "working": working},
        {"value": wrong_sign,
         "mistake": "You used the wrong sign — check whether the resultant force acts with or against "
                    "the object's weight here.",
         "working": working},
        {"value": W,
         "mistake": "This is just the weight (mg) — it ignores the acceleration.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the weight, W = mg?", "answer": W},
        {"question": "What is the size of the resultant force, F = ma?", "answer": F},
        {"question": f"What is {force_name}?", "answer": force},
    ]
    return make_question(question, force, options_data, "N", scaffold=scaffold, notes=_NOTES,
                          topic="Our Dynamic Universe", question_type="Effective Weight", level=level)


def gen_beyond_find_accel(level="Higher"):
    noun, clause, force_name, lo, hi, g, note, fixed_dir = random.choice(_BEYOND_CONTEXTS)
    m = random.randint(lo, hi)
    moving_up = fixed_dir if fixed_dir is not None else random.choice([True, False])
    speeding_up = random.choice([True, False])
    a_max = max(0.6, g * 0.75)
    a = round(random.uniform(0.3, a_max), 2)
    accel_up = _accel_is_up(moving_up, speeding_up)
    motion, change = _direction_desc(moving_up, speeding_up)

    W = _r1(m * g)
    F = _r1(m * a)
    force = _r1(W + F) if accel_up else _r1(W - F)

    question = (
        f"{noun} of mass {m} kg {clause}. It is moving {motion} and {change}{note}. "
        f"{_cap(force_name)} is {force} N. Calculate the rate at which it is {change}."
    )
    working = [
        {"type": "text", "content": f"The resultant force acts {'upwards' if accel_up else 'downwards'}:"},
        {"type": "latex", "content": r"a = \frac{F}{m}"},
        {"type": "latex", "content": rf"a = \frac{{{force} - {W}}}{{{m}}}" if accel_up else rf"a = \frac{{{W} - {force}}}{{{m}}}"},
        {"type": "latex", "content": rf"a = {a}\ \mathrm{{m/s^2}}"},
    ]
    diff = abs(_r1(force - W))
    options_data = [
        {"value": a, "mistake": None, "working": working},
        {"value": diff,
         "mistake": "You found the resultant force but forgot to divide by the mass: a = F ÷ m.",
         "working": working},
        {"value": _r2((force + W) / m),
         "mistake": "Check your equation — the two forces should be subtracted, not added, to find "
                    "the resultant force.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the weight, W = mg?", "answer": W},
        {"question": "What is the size of the resultant force?", "answer": diff},
        {"question": "What is the acceleration?", "answer": a},
    ]
    return make_question(question, a, options_data, "m/s²", scaffold=scaffold, notes=_NOTES,
                          topic="Our Dynamic Universe", question_type="Effective Weight", level=level)


def generate_effective_weight_beyond_lifts(level="Higher"):
    return random.choice([gen_beyond_find_force, gen_beyond_find_accel])(level=level)


def gen_ew_explain_freefall(level="Higher"):
    obj = random.choice(["skydiver", "test parachutist", "wingsuit flyer"])
    m = random.randint(55, 95)

    question_text = (
        f"A {obj} of mass {m} kg is falling and speeding up at a rate of 9.8 m/s² (free fall) "
        f"before their parachute opens. A harness sensor recording the force exerted on the "
        f"{obj} by their equipment reads 0 N. Explain, in terms of the forces acting on the "
        f"{obj}, why this reading is 0 N."
    )
    correct = (
        "In free fall, gravity (weight) is the only force acting on the " + obj + " — the "
        "equipment exerts no additional supporting force. Since the resultant force is just the "
        "weight, the acceleration equals g, and the harness sensor, which measures any extra "
        "supporting force, reads 0 N."
    )
    distractors = [
        {"value": "The reading is 0 N because gravity has stopped acting during free fall.",
         "mistake": "Gravity is still acting throughout free fall — it's the only force acting, "
                     "which is exactly why there's no extra supporting force to register a reading.",
         "working": []},
        {"value": "The reading is 0 N because the " + obj + "'s weight and air resistance are perfectly balanced.",
         "mistake": "In true free fall, before terminal speed is reached, air resistance is negligible "
                     "and the " + obj + " is still speeding up — the forces are not balanced.",
         "working": []},
    ]
    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)

    return PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        distractors=distractors,
        working=[],
        notes=_NOTES,
        topic="Our Dynamic Universe",
        question_type="Effective Weight",
        level=level,
        metadata={"type": "classification", "options": options},
    )
