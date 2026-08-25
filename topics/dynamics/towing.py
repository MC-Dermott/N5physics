import random
from core.models.question_model import PhysicsQuestion

_NOTES = """
## Towing — Connected Objects

**Definitions:**
- The driving force is the force produced by the towing vehicle's engine.
- The tension in a tow bar is the force it exerts to pull whatever is connected behind it.

**Whole system** — to find the acceleration, apply Newton's second law to everything that
moves together (vehicle + all trailers):
$$a = \\frac{F_{\\text{driving}} - F_{\\text{friction (total)}}}{m_{\\text{total}}}$$

**Part of the system** — to find the tension in a tow bar, apply Newton's second law to
*only* the object(s) behind that tow bar (the tow bar is the only horizontal force pulling
them forward, opposed by their own friction if any):
$$T = m_{\\text{behind}} \\times a + F_{\\text{friction (behind)}}$$

| Symbol | Quantity | Unit |
|---|---|---|
| $F_{\\text{driving}}$ | Driving force | N |
| $F_{\\text{friction}}$ | Friction force | N |
| $m_{\\text{total}}$ | Total mass of vehicle + all trailers | kg |
| a | Acceleration | m/s² |
| T | Tension in a tow bar | N |

> **Important:** The acceleration is always the same for every part of the system (they move
> together). But the tension in each tow bar is different — it only has to accelerate the
> mass **behind** it, not the whole system.

**Worked Example:** A 1000 kg car tows a single 250 kg trailer with a driving force of 2500 N
and no friction.
$$a = \\frac{F}{m_{\\text{total}}} = \\frac{2500}{1000 + 250} = 2\\ \\mathrm{m/s^2}$$
Considering the trailer alone (only the tension T acts on it):
$$T = m_{\\text{trailer}} \\times a = 250 \\times 2 = 500\\ \\mathrm{N}$$
"""

_CONTEXTS = ["car", "jeep", "tractor", "van", "4x4"]


def _ctx():
    return random.choice(_CONTEXTS)


# ── Level 1 — one trailer, no friction ──────────────────────────────────────────

def _l1_scenario(level="Higher"):
    obj = _ctx()
    m_c = random.randint(700, 1500)
    m_t = random.randint(200, 800)
    F = random.randint(1500, 4000)
    total = m_c + m_t
    a = round(F / total, 2)
    T = round(m_t * a, 2)

    context = (
        f"A {obj} of mass {m_c} kg tows a single trailer of mass {m_t} kg along a straight, "
        f"level road. The driving force produced by the {obj}'s engine is {F} N. "
        f"There is no friction acting on the {obj} or the trailer."
    )

    working_a = [
        {"type": "text",  "content": "Apply Newton's second law to the whole system (vehicle + trailer):"},
        {"type": "latex", "content": r"F = (m_c + m_t)\,a"},
        {"type": "latex", "content": rf"a = \frac{{F}}{{m_c + m_t}} = \frac{{{F}}}{{{m_c} + {m_t}}}"},
        {"type": "latex", "content": rf"a = {a}\ \mathrm{{m/s^2}}"},
    ]
    part_a = PhysicsQuestion(
        question_text=f"Calculate the acceleration of the {obj} and trailer.",
        correct_answer=a, unit="m/s²",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        working=working_a,
        distractors=[
            {"value": round(F / m_c, 2),
             "mistake": f"You used only the mass of the {obj}. The driving force accelerates "
                        f"the whole system — use the total mass (vehicle + trailer).",
             "working": working_a},
            {"value": round(F / m_t, 2),
             "mistake": "You used only the trailer's mass. Use the total mass of the vehicle "
                        "and trailer together.",
             "working": working_a},
            {"value": round(F * total, 2),
             "mistake": "You multiplied instead of dividing. a = F ÷ (total mass).",
             "working": working_a},
        ],
        notes=_NOTES,
    )

    working_b = [
        {"type": "text",  "content": "Consider the trailer on its own. The only horizontal "
                                     "force acting on it is the tension T in the tow bar "
                                     "(there is no friction):"},
        {"type": "latex", "content": r"T = m_t\,a"},
        {"type": "latex", "content": rf"T = {m_t} \times {a}"},
        {"type": "latex", "content": rf"T = {T}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the tension in the tow bar connecting the "
                      f"{obj} and the trailer.",
        correct_answer=T, unit="N",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        working=working_b,
        distractors=[
            {"value": round(total * a, 2),
             "mistake": "That's the force needed to accelerate the whole system (equal to the "
                        "driving force), not just the trailer. Consider the trailer alone: "
                        "T = m_trailer × a.",
             "working": working_b},
            {"value": round(m_c * a, 2),
             "mistake": f"You used the {obj}'s mass instead of the trailer's mass. Isolate the "
                        "trailer: T = m_trailer × a.",
             "working": working_b},
            {"value": float(F),
             "mistake": f"The tension is not the same as the driving force — some of the "
                        f"driving force also accelerates the {obj} itself. Consider the "
                        "trailer alone: T = m_trailer × a.",
             "working": working_b},
        ],
        notes=_NOTES,
    )

    meta = {"obj": obj, "a": a, "is_multi": False}
    return context, part_a, part_b, meta


def gen_l1_one_trailer_no_friction(level="Higher"):
    context, part_a, part_b, _meta = _l1_scenario(level)
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 2 — one trailer, with friction ────────────────────────────────────────

def _l2_scenario(level="Higher"):
    obj = _ctx()
    m_c = random.randint(700, 1500)
    m_t = random.randint(200, 800)
    F = random.randint(2500, 5000)
    f_c = random.randint(100, 400)
    f_t = random.randint(50, 200)
    total = m_c + m_t
    net = F - f_c - f_t
    a = round(net / total, 2)
    T = round(m_t * a + f_t, 2)

    context = (
        f"A {obj} of mass {m_c} kg tows a single trailer of mass {m_t} kg along a straight, "
        f"level road. The driving force produced by the {obj}'s engine is {F} N. "
        f"Friction acts on the {obj} with a force of {f_c} N, and on the trailer with a "
        f"force of {f_t} N."
    )

    working_a = [
        {"type": "text",  "content": "Apply Newton's second law to the whole system. The "
                                     "unbalanced force is the driving force minus the total friction:"},
        {"type": "latex", "content": r"F_{\text{unbalanced}} = F - f_c - f_t"},
        {"type": "latex", "content": rf"F_{{\text{{unbalanced}}}} = {F} - {f_c} - {f_t} = {net}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"a = \frac{{F_{{\text{{unbalanced}}}}}}{{m_c + m_t}} = \frac{{{net}}}{{{total}}} = {a}\ \mathrm{{m/s^2}}"},
    ]
    part_a = PhysicsQuestion(
        question_text=f"Calculate the acceleration of the {obj} and trailer.",
        correct_answer=a, unit="m/s²",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        working=working_a,
        distractors=[
            {"value": round(F / total, 2),
             "mistake": "You forgot to subtract friction from the driving force. Use the "
                        "*unbalanced* force: F − f_vehicle − f_trailer.",
             "working": working_a},
            {"value": round((F - f_c) / total, 2),
             "mistake": f"You only subtracted the {obj}'s friction. Subtract the trailer's "
                        "friction too.",
             "working": working_a},
            {"value": round((F - f_t) / total, 2),
             "mistake": f"You only subtracted the trailer's friction. Subtract the {obj}'s "
                        "friction too.",
             "working": working_a},
        ],
        notes=_NOTES,
    )

    working_b = [
        {"type": "text",  "content": "Consider the trailer on its own. Two horizontal forces "
                                     "act on it: the tension T (forward) and friction f_t (backward):"},
        {"type": "latex", "content": r"T - f_t = m_t\,a"},
        {"type": "latex", "content": r"T = m_t\,a + f_t"},
        {"type": "latex", "content": rf"T = ({m_t} \times {a}) + {f_t} = {T}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the tension in the tow bar connecting the "
                      f"{obj} and the trailer.",
        correct_answer=T, unit="N",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        working=working_b,
        distractors=[
            {"value": round(m_t * a, 2),
             "mistake": "You forgot to add the trailer's friction. T = (m_trailer × a) + f_trailer.",
             "working": working_b},
            {"value": round(m_t * a - f_t, 2),
             "mistake": "Friction opposes the tension, so it should be added, not subtracted: "
                        "T = (m_trailer × a) + f_trailer.",
             "working": working_b},
            {"value": round(total * a + f_c + f_t, 2),
             "mistake": "That uses the whole system, not just the trailer. Isolate the "
                        "trailer alone: T = (m_trailer × a) + f_trailer.",
             "working": working_b},
        ],
        notes=_NOTES,
    )

    meta = {"obj": obj, "a": a, "is_multi": False}
    return context, part_a, part_b, meta


def gen_l2_one_trailer_friction(level="Higher"):
    context, part_a, part_b, _meta = _l2_scenario(level)
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 3 — multiple trailers, no friction ────────────────────────────────────

def _l3_scenario(level="Higher"):
    obj = _ctx()
    m_c = random.randint(800, 1500)
    m_t1 = random.randint(200, 600)
    m_t2 = random.randint(150, 500)
    F = random.randint(2500, 5500)
    total = m_c + m_t1 + m_t2
    a = round(F / total, 2)
    T1 = round((m_t1 + m_t2) * a, 2)

    context = (
        f"A {obj} of mass {m_c} kg tows two trailers along a straight, level road: "
        f"trailer 1 (mass {m_t1} kg) is attached directly to the {obj}, and trailer 2 "
        f"(mass {m_t2} kg) is attached behind trailer 1. The driving force produced by the "
        f"{obj}'s engine is {F} N. There is no friction."
    )

    working_a = [
        {"type": "text",  "content": "Apply Newton's second law to the whole system "
                                     "(vehicle + both trailers):"},
        {"type": "latex", "content": r"F = (m_c + m_{t1} + m_{t2})\,a"},
        {"type": "latex", "content": rf"a = \frac{{F}}{{m_c + m_{{t1}} + m_{{t2}}}} = \frac{{{F}}}{{{total}}}"},
        {"type": "latex", "content": rf"a = {a}\ \mathrm{{m/s^2}}"},
    ]
    part_a = PhysicsQuestion(
        question_text=f"Calculate the acceleration of the {obj} and trailers.",
        correct_answer=a, unit="m/s²",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        working=working_a,
        distractors=[
            {"value": round(F / (m_c + m_t1), 2),
             "mistake": "You left out the mass of trailer 2. Use the total mass of the "
                        "vehicle and both trailers.",
             "working": working_a},
            {"value": round(F / m_c, 2),
             "mistake": f"You used only the {obj}'s mass. Use the total mass of the vehicle "
                        "and both trailers.",
             "working": working_a},
            {"value": round(F * total, 2),
             "mistake": "You multiplied instead of dividing. a = F ÷ (total mass).",
             "working": working_a},
        ],
        notes=_NOTES,
    )

    working_b = [
        {"type": "text",  "content": "Consider the towed vehicles — trailer 1 AND trailer 2 "
                                     "together — as a single group. The only horizontal force "
                                     "on this group is the tension T in the tow bar pulling them:"},
        {"type": "latex", "content": r"T = (m_{t1} + m_{t2})\,a"},
        {"type": "latex", "content": rf"T = ({m_t1} + {m_t2}) \times {a}"},
        {"type": "latex", "content": rf"T = {T1}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text=f"Calculate the tension in the tow bar connecting the {obj} to the trailers.",
        correct_answer=T1, unit="N",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        working=working_b,
        distractors=[
            {"value": round(m_t1 * a, 2),
             "mistake": "This tow bar has to pull BOTH trailers, not just trailer 1. Use the "
                        "combined mass of trailer 1 and trailer 2.",
             "working": working_b},
            {"value": round(m_t2 * a, 2),
             "mistake": "This tow bar has to pull BOTH trailers, not just trailer 2. Use the "
                        "combined mass of trailer 1 and trailer 2.",
             "working": working_b},
            {"value": round(total * a, 2),
             "mistake": "That's the force needed for the whole system (equal to the driving "
                        "force), not just the towed vehicles behind this tow bar.",
             "working": working_b},
        ],
        notes=_NOTES,
    )

    meta = {"obj": obj, "a": a, "is_multi": True}
    return context, part_a, part_b, meta


def gen_l3_multi_trailer_no_friction(level="Higher"):
    context, part_a, part_b, _meta = _l3_scenario(level)
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 4 — multiple trailers, with friction ──────────────────────────────────

def _l4_scenario(level="Higher"):
    obj = _ctx()
    m_c = random.randint(800, 1500)
    m_t1 = random.randint(200, 600)
    m_t2 = random.randint(150, 500)
    F = random.randint(4000, 7000)
    f_c = random.randint(100, 400)
    f_t1 = random.randint(50, 200)
    f_t2 = random.randint(50, 200)
    total = m_c + m_t1 + m_t2
    net = F - f_c - f_t1 - f_t2
    a = round(net / total, 2)
    T1 = round((m_t1 + m_t2) * a + f_t1 + f_t2, 2)

    context = (
        f"A {obj} of mass {m_c} kg tows two trailers along a straight, level road: "
        f"trailer 1 (mass {m_t1} kg) is attached directly to the {obj}, and trailer 2 "
        f"(mass {m_t2} kg) is attached behind trailer 1. The driving force produced by the "
        f"{obj}'s engine is {F} N. Friction acts on the {obj} with a force of {f_c} N, on "
        f"trailer 1 with a force of {f_t1} N, and on trailer 2 with a force of {f_t2} N."
    )

    working_a = [
        {"type": "text",  "content": "Apply Newton's second law to the whole system. The "
                                     "unbalanced force is the driving force minus the total friction:"},
        {"type": "latex", "content": r"F_{\text{unbalanced}} = F - f_c - f_{t1} - f_{t2}"},
        {"type": "latex", "content": rf"F_{{\text{{unbalanced}}}} = {F} - {f_c} - {f_t1} - {f_t2} = {net}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"a = \frac{{F_{{\text{{unbalanced}}}}}}{{m_c + m_{{t1}} + m_{{t2}}}} = \frac{{{net}}}{{{total}}} = {a}\ \mathrm{{m/s^2}}"},
    ]
    part_a = PhysicsQuestion(
        question_text=f"Calculate the acceleration of the {obj} and trailers.",
        correct_answer=a, unit="m/s²",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        working=working_a,
        distractors=[
            {"value": round(F / total, 2),
             "mistake": "You forgot to subtract the friction forces from the driving force.",
             "working": working_a},
            {"value": round((F - f_c) / total, 2),
             "mistake": f"You only subtracted the {obj}'s friction. Both trailers also have "
                        "friction acting on them — subtract all three.",
             "working": working_a},
            {"value": round(net / (m_c + m_t1), 2),
             "mistake": "You left out the mass of trailer 2. Use the total mass of the "
                        "vehicle and both trailers.",
             "working": working_a},
        ],
        notes=_NOTES,
    )

    working_b = [
        {"type": "text",  "content": "Consider the towed vehicles — trailer 1 AND trailer 2 "
                                     "together — as a single group. Two forces act on this "
                                     "group: the tension T (forward) and both trailers' "
                                     "friction (backward):"},
        {"type": "latex", "content": r"T - f_{t1} - f_{t2} = (m_{t1} + m_{t2})\,a"},
        {"type": "latex", "content": r"T = (m_{t1} + m_{t2})\,a + f_{t1} + f_{t2}"},
        {"type": "latex", "content": rf"T = (({m_t1} + {m_t2}) \times {a}) + {f_t1} + {f_t2} = {T1}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text=f"Calculate the tension in the tow bar connecting the {obj} to the trailers.",
        correct_answer=T1, unit="N",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        working=working_b,
        distractors=[
            {"value": round((m_t1 + m_t2) * a, 2),
             "mistake": "You forgot to add the friction acting on the two trailers: "
                        "T = (m_t1 + m_t2) × a + f_t1 + f_t2.",
             "working": working_b},
            {"value": round((m_t1 + m_t2) * a + f_t1, 2),
             "mistake": "You only added trailer 1's friction — trailer 2's friction also acts "
                        "on this combined mass.",
             "working": working_b},
            {"value": round(total * a + f_c + f_t1 + f_t2, 2),
             "mistake": "That uses the whole system including the vehicle, not just the "
                        "towed vehicles behind this tow bar.",
             "working": working_b},
        ],
        notes=_NOTES,
    )

    meta = {"obj": obj, "a": a, "is_multi": True}
    return context, part_a, part_b, meta


def gen_l4_multi_trailer_friction(level="Higher"):
    context, part_a, part_b, _meta = _l4_scenario(level)
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 5 — exam style (calculation parts + justify) ──────────────────────────

_SCENARIO_BUILDERS = [_l1_scenario, _l2_scenario, _l3_scenario, _l4_scenario]


def gen_exam_style(level="Higher"):
    builder = random.choice(_SCENARIO_BUILDERS)
    context, part_a, part_b, meta = builder(level)
    obj = meta["obj"]
    a = meta["a"]
    is_multi = meta["is_multi"]

    trailer_noun = "trailers" if is_multi else "trailer"
    trailer_the = f"the {trailer_noun}"
    trailer_desc = "the trailers together" if is_multi else "the trailer alone"
    friction_desc = "both trailers'" if is_multi else "the trailer's"

    justify_question = (
        f"As the speed of the {obj} and {trailer_noun} increases, the friction forces on "
        f"both the {obj} and the {trailer_noun} increase.\n\n"
        f"The acceleration of the {obj} and {trailer_noun} remains {a} m/s².\n\n"
        f"Which statement correctly describes what happens to the tension in the tow bar, "
        f"and why?"
    )

    correct = (
        f"Increases — considering {trailer_desc}, T − F_friction = m × a. Since the "
        f"acceleration stays constant, the extra friction must be balanced by extra tension."
    )
    working = [
        {"type": "text", "content": f"Consider {trailer_desc}. The forces on it are the "
                                    "tension T (forward) and friction (backward):"},
        {"type": "latex", "content": r"T - F_{\text{friction}} = m\,a"},
        {"type": "text", "content": f"The acceleration a is fixed at {a} m/s² and the mass "
                                    "doesn't change, so the right-hand side (m × a) stays "
                                    f"constant. If {friction_desc} friction increases, T must "
                                    "increase by the same amount to keep the equation balanced."},
    ]

    distractors = [
        {"value": (f"Decreases — the extra friction on {trailer_the} means less tension is "
                    "needed to keep it moving."),
         "mistake": "Friction opposes the tension, so if friction increases, the tow bar "
                    "must pull *harder*, not softer, to maintain the same acceleration.",
         "working": working},
        {"value": ("Stays the same — since the acceleration doesn't change, none of the "
                    "individual forces need to change either."),
         "mistake": "Constant acceleration only means the *resultant* (unbalanced) force on "
                    f"{trailer_the} stays the same. If friction changes, the tension must "
                    "also change to keep that resultant constant.",
         "working": working},
        {"value": ("Increases — because the driving force from the vehicle's engine must "
                    "increase to maintain the same acceleration."),
         "mistake": "That's true of the driving force, but the question asks about the "
                    f"tension in the tow bar specifically. Consider {trailer_desc}: "
                    "T − F_friction = m × a.",
         "working": working},
    ]

    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)

    part_c = PhysicsQuestion(
        question_text=justify_question,
        correct_answer=correct,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Towing",
        level=level,
        distractors=distractors,
        working=working,
        metadata={"type": "classification", "options": options},
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Towing", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b, part_c],
    )
