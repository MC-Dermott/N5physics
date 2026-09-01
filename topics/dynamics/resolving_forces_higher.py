import random
import math
from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

G = 9.8  # m/s²

_NOTES = """
## Components of Vectors — Resolving Forces

**Definitions:**
- A vector can be resolved into two components at right angles to each other — usually
  horizontal and vertical, or parallel and perpendicular to a slope.
- Resolving a vector does not change it; the two components together are exactly
  equivalent to the original vector.

$$F_x = F\\cos\\theta \\qquad F_y = F\\sin\\theta$$

For an object of mass m on a slope inclined at angle θ to the horizontal, with weight
$W = mg$:
$$W_{\\parallel} = W\\sin\\theta \\ \\text{(component down the slope)} \\qquad W_{\\perp} = W\\cos\\theta \\ \\text{(component into the slope)}$$

| Symbol | Quantity | Unit |
|---|---|---|
| F | Size of the force (or W = weight) | N |
| θ | Angle to the horizontal (or to the slope) | ° |
| Fx, W∥ | Component parallel to the reference direction | N |
| Fy, W⊥ | Component perpendicular to the reference direction | N |

**Worked Example:** A force of 50 N acts at 40° above the horizontal. Resolve it into
horizontal and vertical components.
$$F_x = 50\\cos40° = 38.3\\ \\mathrm{N} \\qquad F_y = 50\\sin40° = 32.1\\ \\mathrm{N}$$

> **Important:** Always check which angle is given — the angle to the horizontal, or the
> angle to the slope/vertical — since this decides whether a component uses sin or cos.
"""

_ANGLES = [20, 25, 30, 35, 40, 50, 55, 60, 65, 70]
_OBJ = ["crate", "box", "sledge", "block", "barrel", "trunk"]


def _r1(val):
    return round(float(val), 1)


def _obj():
    return random.choice(_OBJ)


# ── Level 1 — Finding Components ─────────────────────────────────────────────

def gen_rf_l1_components(level="Higher"):
    F = random.randint(20, 200)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)

    Fx = _r1(F * math.cos(theta))
    Fy = _r1(F * math.sin(theta))
    Fx_swap = _r1(F * math.sin(theta))
    Fy_swap = _r1(F * math.cos(theta))

    context = (
        f"A force of {F} N acts at an angle of {theta_deg}° above the horizontal."
    )

    working_x = [
        {"type": "text",  "content": "The horizontal component uses cos θ:"},
        {"type": "latex", "content": r"F_x = F\cos\theta"},
        {"type": "latex", "content": rf"F_x = {F} \times \cos {theta_deg}° = {Fx}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the horizontal component of the force.",
        correct_answer=Fx, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_x,
        distractors=[
            {"value": Fx_swap,
             "mistake": f"The horizontal component uses cos θ, not sin θ. Fx = F cos {theta_deg}° = {Fx} N.",
             "working": working_x},
            {"value": float(F),
             "mistake": "This is the full force. Resolve it using Fx = F cos θ.",
             "working": working_x},
        ],
        notes=_NOTES,
    )

    working_y = [
        {"type": "text",  "content": "The vertical component uses sin θ:"},
        {"type": "latex", "content": r"F_y = F\sin\theta"},
        {"type": "latex", "content": rf"F_y = {F} \times \sin {theta_deg}° = {Fy}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the vertical component of the force.",
        correct_answer=Fy, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_y,
        distractors=[
            {"value": Fy_swap,
             "mistake": f"The vertical component uses sin θ, not cos θ. Fy = F sin {theta_deg}° = {Fy} N.",
             "working": working_y},
            {"value": float(F),
             "mistake": "This is the full force. Resolve it using Fy = F sin θ.",
             "working": working_y},
        ],
        notes=_NOTES,
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 2 — Components of a Balancing Force ────────────────────────────────

def gen_rf_l2_balancing(level="Higher"):
    Fx_known = random.randint(80, 300)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)

    T = _r1(Fx_known / math.cos(theta))
    Ty = _r1(T * math.sin(theta))

    context = (
        f"An object is held in equilibrium by two ropes. Rope A pulls horizontally with a "
        f"force of {Fx_known} N. Rope B is inclined at {theta_deg}° to the horizontal, and "
        f"its horizontal component exactly balances the pull of Rope A."
    )

    working_T = [
        {"type": "text",  "content": "Since the ropes balance, the horizontal component of Rope B's tension equals Rope A's pull:"},
        {"type": "latex", "content": r"F_x = T\cos\theta \;\Rightarrow\; T = \dfrac{F_x}{\cos\theta}"},
        {"type": "latex", "content": rf"T = \dfrac{{{Fx_known}}}{{\cos {theta_deg}°}} = {T}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the tension in Rope B.",
        correct_answer=T, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_T,
        distractors=[
            {"value": _r1(Fx_known * math.cos(theta)),
             "mistake": f"You multiplied by cos θ instead of dividing. Rearranging Fx = T cos θ gives T = Fx ÷ cos θ = {T} N.",
             "working": working_T},
            {"value": float(Fx_known),
             "mistake": f"The tension in Rope B is not equal to Rope A's pull — only its horizontal *component* is. T = {Fx_known} ÷ cos {theta_deg}° = {T} N.",
             "working": working_T},
        ],
        notes=_NOTES,
    )

    working_Ty = [
        {"type": "text",  "content": "Now find the vertical component of this tension:"},
        {"type": "latex", "content": r"F_y = T\sin\theta"},
        {"type": "latex", "content": rf"F_y = {T} \times \sin {theta_deg}° = {Ty}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the vertical component of the tension in Rope B.",
        correct_answer=Ty, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_Ty,
        distractors=[
            {"value": _r1(T * math.cos(theta)),
             "mistake": f"The vertical component uses sin θ, not cos θ — and since T cos θ was already used to find T from Rope A's pull, this just gives back {Fx_known} N. Fy = T sin {theta_deg}° = {Ty} N.",
             "working": working_Ty},
            {"value": T,
             "mistake": f"That is the full tension in Rope B, not its vertical component. Fy = T sin {theta_deg}° = {Ty} N.",
             "working": working_Ty},
        ],
        notes=_NOTES,
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 3 — Force from Acceleration ────────────────────────────────────────

def _l3_horizontal(level):
    m = random.randint(10, 60)
    a = random.choice([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    F = _r1(m * a)

    question = (
        f"A {_obj()} of mass {m} kg accelerates at {a} m/s² across a smooth horizontal "
        f"surface when pushed. Calculate the horizontal component of the force applied."
    )
    working = [
        {"type": "text",  "content": "Apply Newton's second law:"},
        {"type": "latex", "content": r"F = ma"},
        {"type": "latex", "content": rf"F = {m} \times {a} = {F}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": F, "mistake": None, "working": working},
        {"value": _r1(m / a),
         "mistake": "You divided instead of multiplying. F = m × a.",
         "working": working},
        {"value": _r1(m + a),
         "mistake": "Force is the *product* of mass and acceleration, not their sum. F = m × a.",
         "working": working},
    ]
    return make_question(question, F, options_data, "N",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level)


def _l3_vertical(level):
    m = random.randint(5, 40)
    a = random.choice([0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
    W = _r1(m * G)
    T = _r1(W + m * a)

    context = (
        f"A {_obj()} of mass {m} kg is lifted vertically by a crane, accelerating upwards "
        f"at {a} m/s²."
    )

    working_W = [
        {"type": "latex", "content": r"W = mg"},
        {"type": "latex", "content": rf"W = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the weight of the object.",
        correct_answer=W, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_W,
        distractors=[
            {"value": float(m),
             "mistake": "Weight is mass × g, not mass on its own. W = mg.",
             "working": working_W},
        ],
        notes=_NOTES,
    )

    working_T = [
        {"type": "text",  "content": "Since the object accelerates upward, the tension must overcome its weight AND provide the extra force for the acceleration:"},
        {"type": "latex", "content": r"T = W + ma"},
        {"type": "latex", "content": rf"T = {W} + ({m} \times {a}) = {T}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the tension in the lifting cable.",
        correct_answer=T, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_T,
        distractors=[
            {"value": W,
             "mistake": f"That is just the weight. Since the object is accelerating upward, the tension must be larger than the weight: T = W + ma = {T} N.",
             "working": working_T},
            {"value": _r1(W - m * a),
             "mistake": "Since the object accelerates upward, ma must be added to the weight, not subtracted. T = W + ma.",
             "working": working_T},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": "What is ma (the extra force needed for the acceleration)?", "answer": round(m * a, 2)},
            {"prompt": "What is the tension T?", "answer": T},
        ],
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


def gen_rf_l3_force_from_accel(level="Higher"):
    return random.choice([_l3_horizontal, _l3_vertical])(level)


# ── Level 4 — Weight on a Slope ──────────────────────────────────────────────

def gen_rf_l4_weight_on_slope(level="Higher"):
    m = random.randint(5, 50)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)

    W = _r1(m * G)
    W_par = _r1(W * math.sin(theta))
    W_perp = _r1(W * math.cos(theta))

    context = f"A {_obj()} of mass {m} kg rests on a ramp inclined at {theta_deg}° to the horizontal."

    working_W = [
        {"type": "latex", "content": r"W = mg"},
        {"type": "latex", "content": rf"W = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the weight of the object.",
        correct_answer=W, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_W,
        distractors=[
            {"value": float(m), "mistake": "Weight is mass × g, not mass on its own.", "working": working_W},
        ],
        notes=_NOTES,
    )

    working_par = [
        {"type": "text",  "content": "The component of weight acting down the slope (parallel to it):"},
        {"type": "latex", "content": r"W_{\parallel} = W\sin\theta"},
        {"type": "latex", "content": rf"W_{{\parallel}} = {W} \times \sin {theta_deg}° = {W_par}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the component of the weight acting parallel to (down) the slope.",
        correct_answer=W_par, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_par,
        distractors=[
            {"value": W_perp,
             "mistake": f"The component *parallel* to the slope uses sin θ, not cos θ. W∥ = W sin {theta_deg}° = {W_par} N.",
             "working": working_par},
            {"value": W,
             "mistake": "This is the full weight. It must be resolved using W∥ = W sin θ.",
             "working": working_par},
        ],
        notes=_NOTES,
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 5 — Resultant Force Along a Slope, No Friction ─────────────────────

def gen_rf_l5_resultant_no_friction(level="Higher"):
    m = random.randint(5, 40)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    W = _r1(m * G)
    resultant = _r1(W * math.sin(theta))

    question = (
        f"A {_obj()} of mass {m} kg is released from rest on a smooth (frictionless) slope "
        f"inclined at {theta_deg}°. Calculate the resultant force acting on it along the slope."
    )
    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "text",  "content": "With no friction, the resultant force along the slope is simply the parallel component of the weight:"},
        {"type": "latex", "content": r"\text{Resultant} = W\sin\theta"},
        {"type": "latex", "content": rf"\text{{Resultant}} = {W} \times \sin {theta_deg}° = {resultant}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": resultant, "mistake": None, "working": working},
        {"value": _r1(W * math.cos(theta)),
         "mistake": f"The component *along* the slope uses sin θ, not cos θ. Resultant = W sin {theta_deg}° = {resultant} N.",
         "working": working},
        {"value": W,
         "mistake": "This is the full weight, not its component along the slope.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the weight W (= mg)?", "answer": W},
        {"question": "What is the resultant force along the slope?", "answer": resultant},
    ]
    return make_question(question, resultant, options_data, "N",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


# ── Level 6 — Acceleration of a Block on a Slope, With Friction ──────────────

def gen_rf_l6_acceleration_with_friction(level="Higher"):
    m = random.randint(5, 40)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    friction = round(random.uniform(0.2, 0.7) * W_par, 1)
    resultant = _r1(W_par - friction)
    a = _r1(resultant / m)

    obj = _obj()
    question = (
        f"A {obj} of mass {m} kg slides down a slope inclined at {theta_deg}°. Friction "
        f"acts on it with a force of {friction} N, opposing the motion. "
        f"Calculate the acceleration of the {obj}."
    )
    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"\text{{Resultant}} = W_{{\parallel}} - \text{{friction}} = {_r1(W_par)} - {friction} = {resultant}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"a = \dfrac{{\text{{Resultant}}}}{{m}} = \dfrac{{{resultant}}}{{{m}}} = {a}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": a, "mistake": None, "working": working},
        {"value": _r1((W_par + friction) / m),
         "mistake": "Friction opposes the motion down the slope, so it should be subtracted from the parallel weight component, not added.",
         "working": working},
        {"value": _r1(W_par / m),
         "mistake": "You forgot to subtract the friction force before dividing by mass.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the resultant force along the slope (W∥ − friction)?", "answer": resultant},
        {"question": "What is the acceleration a?", "answer": a},
    ]
    return make_question(question, a, options_data, "m/s²",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


# ── Level 7 — Finding an Unknown Force ───────────────────────────────────────

def gen_rf_l7_unknown_force(level="Higher"):
    m = random.randint(5, 40)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    a = random.choice([0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5])
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    ma = m * a
    friction = _r1(W_par - ma)

    question = (
        f"A {_obj()} of mass {m} kg slides down a slope inclined at {theta_deg}°, "
        f"accelerating at {a} m/s². Calculate the friction force acting on it."
    )
    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"ma = {m} \times {a} = {_r1(ma)}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"\text{{Friction}} = W_{{\parallel}} - ma = {_r1(W_par)} - {_r1(ma)} = {friction}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": friction, "mistake": None, "working": working},
        {"value": _r1(W_par + ma),
         "mistake": "Friction opposes the motion, reducing the resultant below the parallel weight component. It should be subtracted, i.e. friction = W∥ − ma.",
         "working": working},
        {"value": _r1(W_par),
         "mistake": "You forgot to subtract ma. friction = W∥ − ma.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is W∥ (= W sinθ)?", "answer": _r1(W_par)},
        {"question": "What is the friction force?", "answer": friction},
    ]
    return make_question(question, friction, options_data, "N",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


# ── Level 8 — Explain: Effect of Angle ────────────────────────────────────────

def _explain_tension(level):
    obj = _obj()
    context = (
        f"A {obj} is held stationary on a smooth (frictionless) slope by a rope running "
        f"parallel to the slope. The angle of the slope is then increased, while the mass "
        f"of the {obj} stays the same."
    )
    question_text = "What happens to the tension in the rope, and why?"
    correct = (
        "The tension increases, because the rope must balance the component of weight "
        "acting down the slope, W sin θ, and sin θ increases as the angle increases."
    )
    working = [
        {"type": "text", "content": (
            f"With no friction, the rope's tension must exactly balance the parallel "
            f"component of the {obj}'s weight: T = W sin θ. As θ increases (up to 90°), "
            "sin θ increases, so T must increase too."
        )},
    ]
    distractors = [
        {"value": "The tension decreases, because less of the weight acts along the slope as the angle increases.",
         "mistake": "It's the opposite — as the slope gets steeper, *more* of the weight acts down the slope (W sin θ increases with θ), so the tension needed increases.",
         "working": working},
        {"value": "The tension stays the same, because the weight of the object doesn't change.",
         "mistake": "The weight itself doesn't change, but the *component* of that weight acting down the slope does — W sin θ depends on the angle, not just on W.",
         "working": working},
        {"value": "The tension increases, because the normal force from the slope increases as the angle increases.",
         "mistake": "The normal force (perpendicular component, W cos θ) actually decreases as the angle increases — it isn't what determines the tension here.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def _explain_mass_parallel(level):
    obj = _obj()
    context = (
        f"Two identical {obj}s are placed on the same slope, at the same angle. One {obj} "
        f"has twice the mass of the other."
    )
    question_text = "How does the component of weight acting parallel to the slope compare for the two objects, and why?"
    correct = (
        "It is twice as large for the heavier object, because W∥ = W sin θ = mg sin θ, and "
        "for a fixed angle this component is directly proportional to mass."
    )
    working = [
        {"type": "text", "content": (
            "The parallel component of weight is W∥ = mg sin θ. For the same angle θ, W∥ "
            "is directly proportional to mass m, so doubling the mass doubles W∥."
        )},
    ]
    distractors = [
        {"value": "It is the same for both objects, because the angle of the slope hasn't changed.",
         "mistake": "The angle being the same doesn't mean W∥ is the same — W∥ = mg sin θ also depends on mass, which has doubled.",
         "working": working},
        {"value": "It is four times as large for the heavier object, since weight depends on mass squared.",
         "mistake": "Weight is W = mg — mass appears only to the first power, not squared. Doubling m doubles W, and so doubles W∥ = W sin θ too.",
         "working": working},
        {"value": "It cannot be compared without knowing the coefficient of friction.",
         "mistake": "Friction doesn't affect the weight component itself — W∥ = mg sin θ depends only on mass and angle.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def gen_rf_l8_explain_angle(level="Higher"):
    builder = random.choice([_explain_tension, _explain_mass_parallel])
    context, question_text, correct, distractors = builder(level)

    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)

    part = PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Components of Vectors",
        level=level,
        distractors=distractors,
        working=distractors[0]["working"],
        metadata={"type": "classification", "options": options},
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part],
    )
