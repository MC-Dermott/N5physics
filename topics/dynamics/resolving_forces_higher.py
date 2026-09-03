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

If the object is sliding **down** the slope, friction acts up the slope, opposing the
motion, so the resultant force down the slope is $W_{\\parallel} - \\text{friction}$. If
the object is sliding **up** the slope (e.g. after being pushed), friction still opposes
the motion — so it now acts down the slope, in the same direction as $W_{\\parallel}$ —
and the two add together: resultant $= W_{\\parallel} + \\text{friction}$, decelerating
the object.

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
        f"A force of F = {F} N acts at an angle of {theta_deg}° above the horizontal."
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
        scaffold=[
            {"prompt": f"What is cos {theta_deg}°, to 3 decimal places?", "answer": round(math.cos(theta), 3)},
            {"prompt": "What is the horizontal component Fx?", "answer": Fx},
        ],
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
        scaffold=[
            {"prompt": f"What is sin {theta_deg}°, to 3 decimal places?", "answer": round(math.sin(theta), 3)},
            {"prompt": "What is the vertical component Fy?", "answer": Fy},
        ],
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
        scaffold=[
            {"prompt": f"What is cos {theta_deg}°, to 3 decimal places?", "answer": round(math.cos(theta), 3)},
            {"prompt": "What is the tension T in Rope B?", "answer": T},
        ],
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
        scaffold=[
            {"prompt": f"What is sin {theta_deg}°, to 3 decimal places?", "answer": round(math.sin(theta), 3)},
            {"prompt": "What is the vertical component of the tension?", "answer": Ty},
        ],
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 3 — Force from Acceleration ────────────────────────────────────────

def _l3_horizontal_find_F(level):
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


def _l3_horizontal_find_a(level):
    m = random.randint(50, 400)
    F = random.randint(60, 500)
    a = _r1(F / m)

    question = (
        f"A trailer of mass {m} kg is pulled across level ground by a horizontal force of "
        f"{F} N. Calculate the acceleration of the trailer."
    )
    working = [
        {"type": "text",  "content": "Rearrange Newton's second law for acceleration:"},
        {"type": "latex", "content": r"F = ma \;\Rightarrow\; a = \dfrac{F}{m}"},
        {"type": "latex", "content": rf"a = \dfrac{{{F}}}{{{m}}} = {a}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": a, "mistake": None, "working": working},
        {"value": _r1(m / F),
         "mistake": "You divided the wrong way round. a = F ÷ m, not m ÷ F.",
         "working": working},
        {"value": float(F),
         "mistake": "This is the force, not the acceleration. a = F ÷ m.",
         "working": working},
    ]
    return make_question(question, a, options_data, "m/s²",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level)


def _l3_vertical_given_a(level):
    m = random.randint(5, 40)
    a = random.choice([0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
    W = _r1(m * G)
    mode = random.choice(["up", "down", "constant"])
    obj = _obj()

    if mode == "up":
        T = _r1(W + m * a)
        context = f"A {obj} of mass {m} kg is lifted vertically by a crane, accelerating upwards at {a} m/s²."
        rule_text = "Since the object accelerates upward, the tension must overcome its weight AND provide the extra force for the acceleration:"
        eq_latex = r"T = W + ma"
        sub_latex = rf"T = {W} + ({m} \times {a}) = {T}\ \mathrm{{N}}"
        wrong_T = _r1(W - m * a)
        wrong_mistake = f"Since the object accelerates upward, ma must be added to the weight, not subtracted. T = W + ma = {T} N."
    elif mode == "down":
        T = _r1(W - m * a)
        context = f"A {obj} of mass {m} kg is lowered vertically by a winch, accelerating downwards at {a} m/s² (less than g, since the cable is still under tension)."
        rule_text = "Since the object accelerates downward (more slowly than free fall), the tension must be less than the weight, but still positive:"
        eq_latex = r"T = W - ma"
        sub_latex = rf"T = {W} - ({m} \times {a}) = {T}\ \mathrm{{N}}"
        wrong_T = _r1(W + m * a)
        wrong_mistake = f"Since the object accelerates downward, ma must be subtracted from the weight, not added. T = W − ma = {T} N."
    else:
        T = W
        context = f"A {obj} of mass {m} kg is raised at a constant speed by a winch cable."
        rule_text = "At constant speed the object is in equilibrium, so the tension simply equals the weight:"
        eq_latex = r"T = W"
        sub_latex = rf"T = {W}\ \mathrm{{N}}"
        wrong_T = _r1(W * 1.1)
        wrong_mistake = f"At constant speed there is no acceleration, so the tension equals the weight exactly: T = W = {T} N."

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
        {"type": "text",  "content": rule_text},
        {"type": "latex", "content": eq_latex},
        {"type": "latex", "content": sub_latex},
    ]
    distractors_T = [
        {"value": wrong_T, "mistake": wrong_mistake, "working": working_T},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the tension in the cable.",
        correct_answer=T, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_T,
        distractors=distractors_T,
        notes=_NOTES,
        scaffold=None if mode == "constant" else [
            {"prompt": "What is ma (the extra force needed for the acceleration)?", "answer": round(m * a, 2)},
            {"prompt": "What is the tension T?", "answer": T},
        ],
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


def _l3_vertical_inverse(level):
    m = random.randint(5, 40)
    W = _r1(m * G)
    mode = random.choice(["find_a", "find_m"])

    if mode == "find_a":
        a = random.choice([0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
        T = _r1(W + m * a)
        question = (
            f"A {_obj()} of mass {m} kg is lifted by a cable with a tension of {T} N. "
            f"Calculate the acceleration of the object."
        )
        working = [
            {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
            {"type": "text",  "content": "Rearrange T = W + ma for acceleration:"},
            {"type": "latex", "content": r"a = \dfrac{T - W}{m}"},
            {"type": "latex", "content": rf"a = \dfrac{{{T} - {W}}}{{{m}}} = {_r1((T - W) / m)}\ \mathrm{{m/s^2}}"},
        ]
        answer = _r1((T - W) / m)
        options_data = [
            {"value": answer, "mistake": None, "working": working},
            {"value": _r1((T + W) / m),
             "mistake": "The weight should be subtracted from the tension, not added. a = (T − W) ÷ m.",
             "working": working},
            {"value": _r1(T / m),
             "mistake": "You forgot to subtract the weight first. a = (T − W) ÷ m.",
             "working": working},
        ]
        scaffold = [
            {"question": "What is the weight W (= mg)?", "answer": W},
            {"question": "What is the acceleration a?", "answer": answer},
        ]
        return make_question(question, answer, options_data, "m/s²",
                             notes=_NOTES, topic="Our Dynamic Universe",
                             question_type="Components of Vectors", level=level, scaffold=scaffold)
    else:
        a = random.choice([0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
        mass_true = random.randint(10, 60)
        T = round(mass_true * (G - a), 1)
        answer = _r1(T / (G - a))
        question = (
            f"A winch lowers a box, accelerating downwards at {a} m/s² (less than g, since "
            f"the cable is still under tension). The tension in the cable is {T} N. "
            f"Calculate the mass of the box."
        )
        working = [
            {"type": "latex", "content": r"T = W - ma = mg - ma = m(g - a)"},
            {"type": "latex", "content": rf"m = \dfrac{{T}}{{g - a}} = \dfrac{{{T}}}{{9.8 - {a}}} = {answer}\ \mathrm{{kg}}"},
        ]
        options_data = [
            {"value": answer, "mistake": None, "working": working},
            {"value": _r1(T / (G + a)),
             "mistake": "Since the object accelerates downward (slower than free fall), the denominator is (g − a), not (g + a).",
             "working": working},
            {"value": _r1(T / G),
             "mistake": "You forgot to account for the acceleration — this ignores the fact that the box isn't in free fall or stationary.",
             "working": working},
        ]
        return make_question(question, answer, options_data, "kg",
                             notes=_NOTES, topic="Our Dynamic Universe",
                             question_type="Components of Vectors", level=level)


def _l3_force_from_accel(level="Higher"):
    return random.choice([_l3_horizontal_find_F, _l3_horizontal_find_a,
                           _l3_vertical_given_a, _l3_vertical_inverse])(level)


def gen_rf_l2_balancing_and_accel(level="Higher"):
    """Section 2 — balancing forces, and force from acceleration (horizontal/vertical)."""
    return random.choice([gen_rf_l2_balancing, _l3_force_from_accel])(level)


# ── Level 3 — Weight on a Slope ───────────────────────────────────────────────

def gen_rf_l3_weight_on_slope(level="Higher"):
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
        scaffold=[
            {"prompt": f"What is sin {theta_deg}°, to 3 decimal places?", "answer": round(math.sin(theta), 3)},
            {"prompt": "What is the component of weight parallel to the slope?", "answer": W_par},
        ],
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Level 5 — Acceleration on a Slope, With Friction (sliding down) ──────────

def gen_rf_l5_acceleration_with_friction(level="Higher"):
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


# ── Level 6 — Finding an Unknown Force (Friction) on a Slope ─────────────────

def gen_rf_l6_unknown_force(level="Higher"):
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


# ── Level 7 — Finding the Angle of a Slope ────────────────────────────────────

def _l7_direct(level):
    W = random.randint(150, 600)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    W_par = round(W * math.sin(theta), 1)
    sin_theta = round(W_par / W, 3)
    theta_calc = _r1(math.degrees(math.asin(sin_theta)))

    question = (
        f"A crate of weight {W} N rests on a slope. The component of the crate's weight "
        f"acting parallel to the slope is {W_par} N. Calculate the angle of the slope."
    )
    working = [
        {"type": "latex", "content": r"\sin\theta = \dfrac{W_{\parallel}}{W}"},
        {"type": "latex", "content": rf"\sin\theta = \dfrac{{{W_par}}}{{{W}}} = {sin_theta}"},
        {"type": "latex", "content": rf"\theta = \sin^{{-1}}({sin_theta}) = {theta_calc}°"},
    ]
    options_data = [
        {"value": theta_calc, "mistake": None, "working": working},
        {"value": _r1(math.degrees(math.acos(sin_theta))),
         "mistake": "W∥ = W sin θ, so θ must be found using sin⁻¹, not cos⁻¹.",
         "working": working},
        {"value": _r1(W_par / W * 100),
         "mistake": "The angle isn't simply the ratio expressed as a number — you need sin⁻¹ of that ratio.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is sin θ (= W∥ ÷ W)?", "answer": sin_theta},
        {"question": "What is the angle θ?", "answer": theta_calc},
    ]
    return make_question(question, theta_calc, options_data, "°",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


def _l7_dynamic(level):
    m = random.randint(10, 45)
    friction = random.randint(15, 60)
    constant_speed = random.random() < 0.35
    W = _r1(m * G)

    if constant_speed:
        W_par = float(friction)
        a_text = "the block slides down at a constant speed"
    else:
        a = random.choice([0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
        ma = m * a
        W_par = round(ma + friction, 1)
        a_text = f"accelerating at {a} m/s²"

    sin_theta = round(W_par / W, 3)
    if sin_theta >= 1:
        return _l7_dynamic(level)
    theta_calc = _r1(math.degrees(math.asin(sin_theta)))

    obj = _obj()
    question = (
        f"A {obj} of mass {m} kg slides down a slope, {a_text}. The friction force "
        f"acting on the {obj} is {friction} N. Calculate the angle of the slope."
    )
    if constant_speed:
        rule = "Constant speed means the forces along the slope are balanced, so W∥ = friction:"
        wpar_latex = rf"W_{{\parallel}} = \text{{friction}} = {friction}\ \mathrm{{N}}"
    else:
        rule = "Rearranging Resultant = W∥ − friction, with resultant = ma, gives the parallel component of weight:"
        wpar_latex = rf"W_{{\parallel}} = ma + \text{{friction}} = {W_par}\ \mathrm{{N}}"

    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "text",  "content": rule},
        {"type": "latex", "content": wpar_latex},
        {"type": "latex", "content": rf"\sin\theta = \dfrac{{W_{{\parallel}}}}{{W}} = \dfrac{{{W_par}}}{{{W}}} = {sin_theta}"},
        {"type": "latex", "content": rf"\theta = \sin^{{-1}}({sin_theta}) = {theta_calc}°"},
    ]
    options_data = [
        {"value": theta_calc, "mistake": None, "working": working},
        {"value": _r1(math.degrees(math.acos(sin_theta))),
         "mistake": "W∥ = W sin θ, so θ must be found using sin⁻¹, not cos⁻¹.",
         "working": working},
        {"value": _r1(math.degrees(math.asin(min(friction / W, 0.999)))),
         "mistake": "This uses only the friction force. First find W∥, the parallel component of weight, then use sin θ = W∥ ÷ W.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is W∥, the component of weight parallel to the slope?", "answer": W_par},
        {"question": "What is the angle θ?", "answer": theta_calc},
    ]
    return make_question(question, theta_calc, options_data, "°",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


def _l7_find_mass(level):
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    friction = random.randint(40, 250)
    W_par = float(friction)
    W = round(W_par / math.sin(theta), 1)
    mass = _r1(W / G)

    question = (
        f"A creel box sits stationary on a slipway inclined at {theta_deg}°, held in place "
        f"by friction alone. The friction force acting up the slope is {friction} N. "
        f"Calculate the component of the box's weight acting parallel to the slope, and "
        f"hence calculate its weight and mass."
    )
    working_par = [
        {"type": "text",  "content": "Held in place by friction alone, so the forces along the slope balance:"},
        {"type": "latex", "content": r"W_{\parallel} = \text{friction}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = {friction}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the component of the box's weight acting parallel to the slope.",
        correct_answer=W_par, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_par,
        distractors=[
            {"value": _r1(friction * math.sin(theta)),
             "mistake": f"When stationary and held by friction alone, W∥ equals the friction force exactly — no further resolving is needed: W∥ = {friction} N.",
             "working": working_par},
        ],
        notes=_NOTES,
    )

    working_mass = [
        {"type": "latex", "content": r"W_{\parallel} = W\sin\theta \;\Rightarrow\; W = \dfrac{W_{\parallel}}{\sin\theta}"},
        {"type": "latex", "content": rf"W = \dfrac{{{W_par}}}{{\sin {theta_deg}°}} = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"m = \dfrac{{W}}{{g}} = \dfrac{{{W}}}{{9.8}} = {mass}\ \mathrm{{kg}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Hence calculate the weight and mass of the box.",
        correct_answer=mass, unit="kg",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_mass,
        distractors=[
            {"value": W,
             "mistake": f"That is the weight in newtons, not the mass. Divide by g: m = W ÷ g = {mass} kg.",
             "working": working_mass},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": "What is the weight W?", "answer": W},
            {"prompt": "What is the mass m?", "answer": mass},
        ],
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=question, parts=[part_a, part_b],
    )


def _l7_find_angle(level="Higher"):
    return random.choice([_l7_direct, _l7_dynamic, _l7_dynamic, _l7_find_mass])(level)


def gen_rf_l4_slope_dynamics(level="Higher"):
    """Section 4 — acceleration, friction (unknown force), or angle on a slope (sliding down)."""
    return random.choice([
        gen_rf_l5_acceleration_with_friction,
        gen_rf_l6_unknown_force,
        _l7_find_angle,
    ])(level)


# ── Level 5 — Sliding Up a Slope With Friction ────────────────────────────────

def gen_rf_l8_up_slope_deceleration(level="Higher"):
    m = random.randint(10, 45)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    friction = random.randint(10, 60)
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    resultant = _r1(W_par + friction)
    a = _r1(resultant / m)

    obj = _obj()
    context = (
        f"A {obj} of mass {m} kg is given a push and slides up a slope inclined at "
        f"{theta_deg}°. As it slides up, a friction force of {friction} N acts on the "
        f"{obj}, opposing the motion."
    )

    working_res = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Moving up the slope, both W∥ and friction act down the slope, opposing the motion, so they add together:"},
        {"type": "latex", "content": rf"\text{{Resultant}} = W_{{\parallel}} + \text{{friction}} = {_r1(W_par)} + {friction} = {resultant}\ \mathrm{{N}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the resultant force acting on it along the slope.",
        correct_answer=resultant, unit="N",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_res,
        distractors=[
            {"value": _r1(W_par - friction),
             "mistake": f"While moving up the slope, friction and W∥ both act down the slope and so must be added, not subtracted. Resultant = W∥ + friction = {resultant} N.",
             "working": working_res},
        ],
        notes=_NOTES,
    )

    working_a = [
        {"type": "latex", "content": r"a = \dfrac{\text{Resultant}}{m}"},
        {"type": "latex", "content": rf"a = \dfrac{{{resultant}}}{{{m}}} = {a}\ \mathrm{{m/s^2}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the deceleration of the object.",
        correct_answer=a, unit="m/s²",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        working=working_a,
        distractors=[
            {"value": _r1(W_par / m),
             "mistake": f"This uses W∥ only, ignoring friction. a = Resultant ÷ m = {a} m/s².",
             "working": working_a},
        ],
        notes=_NOTES,
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


def gen_rf_l8_up_slope_find_friction(level="Higher"):
    m = random.randint(10, 45)
    theta_deg = random.choice(_ANGLES)
    theta = math.radians(theta_deg)
    dec = random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5])
    W = _r1(m * G)
    W_par = W * math.sin(theta)
    ma = m * dec
    friction = _r1(ma - W_par)
    if friction <= 0:
        return gen_rf_l8_up_slope_find_friction(level)

    obj = _obj()
    question = (
        f"A {obj} of mass {m} kg is pushed up a ramp inclined at {theta_deg}° to the "
        f"horizontal. As it slides up, it decelerates at {dec} m/s². Calculate the "
        f"friction force acting on the {obj}."
    )
    working = [
        {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"W_{{\parallel}} = W\sin\theta = {W} \times \sin {theta_deg}° = {_r1(W_par)}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"ma = {m} \times {dec} = {_r1(ma)}\ \mathrm{{N}}"},
        {"type": "text",  "content": "Moving up and decelerating, so both weight component and friction act down the slope:"},
        {"type": "latex", "content": r"ma = W_{\parallel} + \text{friction}"},
        {"type": "latex", "content": rf"\text{{Friction}} = ma - W_{{\parallel}} = {_r1(ma)} - {_r1(W_par)} = {friction}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": friction, "mistake": None, "working": working},
        {"value": _r1(ma + W_par),
         "mistake": "Friction and W∥ combine to produce ma while the object moves up the slope, so friction = ma − W∥, not ma + W∥.",
         "working": working},
        {"value": _r1(W_par - ma),
         "mistake": "This gives a negative or mismatched value — while moving up, ma is the larger quantity. friction = ma − W∥.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is W∥ (= W sinθ)?", "answer": _r1(W_par)},
        {"question": "What is the friction force?", "answer": friction},
    ]
    return make_question(question, friction, options_data, "N",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Components of Vectors", level=level, scaffold=scaffold)


def gen_rf_l8_up_slope_find_angle_or_mass(level="Higher"):
    friction = random.randint(20, 70)
    dec = random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])

    if random.random() < 0.5:
        m = random.randint(10, 45)
        W = _r1(m * G)
        ma = m * dec
        W_par = round(ma - friction, 1)
        if W_par <= 0 or W_par >= W:
            return gen_rf_l8_up_slope_find_angle_or_mass(level)
        sin_theta = round(W_par / W, 3)
        theta_calc = _r1(math.degrees(math.asin(sin_theta)))

        obj = _obj()
        question = (
            f"A {obj} is pushed up a ramp. A friction force of {friction} N acts on the "
            f"{obj} as it decelerates at {dec} m/s². The {obj} has a mass of {m} kg. "
            f"Calculate the angle of the ramp."
        )
        working = [
            {"type": "latex", "content": rf"W = mg = {m} \times 9.8 = {W}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"ma = {m} \times {dec} = {_r1(ma)}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"W_{{\parallel}} = ma - \text{{friction}} = {_r1(ma)} - {friction} = {W_par}\ \mathrm{{N}}"},
            {"type": "latex", "content": rf"\sin\theta = \dfrac{{W_{{\parallel}}}}{{W}} = \dfrac{{{W_par}}}{{{W}}} = {sin_theta}"},
            {"type": "latex", "content": rf"\theta = \sin^{{-1}}({sin_theta}) = {theta_calc}°"},
        ]
        options_data = [
            {"value": theta_calc, "mistake": None, "working": working},
            {"value": _r1(math.degrees(math.acos(sin_theta))),
             "mistake": "W∥ = W sin θ, so θ is found with sin⁻¹, not cos⁻¹.",
             "working": working},
        ]
        scaffold = [
            {"question": "What is W∥ (= ma − friction)?", "answer": W_par},
            {"question": "What is the angle θ?", "answer": theta_calc},
        ]
        return make_question(question, theta_calc, options_data, "°",
                             notes=_NOTES, topic="Our Dynamic Universe",
                             question_type="Components of Vectors", level=level, scaffold=scaffold)
    else:
        theta_deg = random.choice(_ANGLES)
        theta = math.radians(theta_deg)
        sin_theta = math.sin(theta)
        denom = dec - G * sin_theta
        if denom <= 0.3:
            return gen_rf_l8_up_slope_find_angle_or_mass(level)
        mass = _r1(friction / denom)
        if not (5 <= mass <= 80):
            return gen_rf_l8_up_slope_find_angle_or_mass(level)

        obj = _obj()
        question = (
            f"A {obj} is pushed up a slipway inclined at {theta_deg}°. A friction force "
            f"of {friction} N acts on the {obj} as it decelerates at {dec} m/s². "
            f"Calculate the mass of the {obj}."
        )
        working = [
            {"type": "latex", "content": r"ma = W_{\parallel} + \text{friction} = mg\sin\theta + \text{friction}"},
            {"type": "latex", "content": r"m(a - g\sin\theta) = \text{friction}"},
            {"type": "latex", "content": rf"m = \dfrac{{\text{{friction}}}}{{a - g\sin\theta}} = \dfrac{{{friction}}}{{{dec} - 9.8\times\sin{theta_deg}°}} = {mass}\ \mathrm{{kg}}"},
        ]
        options_data = [
            {"value": mass, "mistake": None, "working": working},
            {"value": _r1(friction / (dec + G * sin_theta)),
             "mistake": "While moving up the slope, W∥ adds to friction to produce ma, so the denominator is (a − g sin θ), not (a + g sin θ).",
             "working": working},
        ]
        return make_question(question, mass, options_data, "kg",
                             notes=_NOTES, topic="Our Dynamic Universe",
                             question_type="Components of Vectors", level=level)


def gen_rf_l5_up_slope(level="Higher"):
    """Section 5 — object sliding up a slope with friction (deceleration, friction, or angle/mass)."""
    return random.choice([
        gen_rf_l8_up_slope_deceleration,
        gen_rf_l8_up_slope_find_friction,
        gen_rf_l8_up_slope_find_angle_or_mass,
    ])(level)


# ── Level 6 — Explain: Effect of Angle ────────────────────────────────────────

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


def _explain_wpar_increases(level):
    obj = _obj()
    context = (
        f"A {obj} rests on a ramp used to load a ferry. The angle of the ramp is then "
        f"increased, while the mass of the {obj} stays the same."
    )
    question_text = "What happens to the component of the crate's weight acting parallel to the ramp, and why?"
    correct = (
        "It increases, because W∥ = W sin θ, and sin θ increases as the angle increases "
        "(up to 90°)."
    )
    working = [
        {"type": "text", "content": (
            "W∥ = W sin θ. The weight W itself doesn't change, but as θ increases, sin θ "
            "increases, so the component of weight acting down the slope increases."
        )},
    ]
    distractors = [
        {"value": "It decreases, because less of the weight acts along a steeper ramp.",
         "mistake": "It's the opposite — a steeper ramp means *more* of the weight acts along it. sin θ increases as θ increases, so W∥ increases.",
         "working": working},
        {"value": "It stays the same, because the weight of the crate doesn't change.",
         "mistake": "The weight itself doesn't change, but its *component* along the ramp does — W∥ = W sin θ depends on angle as well as weight.",
         "working": working},
        {"value": "It increases initially, then decreases once the ramp is steep enough.",
         "mistake": "sin θ increases continuously as θ increases from 0° to 90°, so W∥ keeps increasing throughout this range.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def _explain_vertical_tension(level):
    context = (
        "A tractor tows a sledge using a rope of constant tension. The angle the rope "
        "makes with the ground is then increased."
    )
    question_text = "What happens to the vertical component of the tension, and why?"
    correct = (
        "It increases, because Fy = T sin θ, and sin θ increases as the angle increases, "
        "even though the tension T itself is unchanged."
    )
    working = [
        {"type": "text", "content": (
            "Fy = T sin θ. Since T is constant, Fy depends only on sin θ. As θ increases "
            "(up to 90°), sin θ increases, so the vertical component increases."
        )},
    ]
    distractors = [
        {"value": "It decreases, because the horizontal component takes up more of the tension at a steeper angle.",
         "mistake": "The horizontal component (T cos θ) does decrease, but the vertical component (T sin θ) increases — they don't trade off in the way suggested.",
         "working": working},
        {"value": "It stays the same, because the tension in the rope hasn't changed.",
         "mistake": "The tension T is unchanged, but its *vertical component* Fy = T sin θ still depends on the angle, which has increased.",
         "working": working},
        {"value": "It cannot be determined without knowing the mass of the sledge.",
         "mistake": "The vertical component of a given tension depends only on the tension and the angle — Fy = T sin θ — not on the sledge's mass.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def _explain_accel_decreases(level):
    obj = _obj()
    context = (
        f"A {obj} slides down a slope with a constant friction force acting on it. The "
        f"angle of the slope is then decreased."
    )
    question_text = "What happens to the acceleration of the block, and why?"
    correct = (
        "It decreases, because the resultant force along the slope is W∥ − friction = "
        "mg sin θ − friction, and as θ decreases, sin θ decreases so W∥ decreases while "
        "friction stays the same, reducing the resultant force and hence the acceleration."
    )
    working = [
        {"type": "text", "content": (
            "a = (mg sin θ − friction) ÷ m. As θ decreases, sin θ decreases, so W∥ = mg sin θ "
            "decreases. Since friction is unchanged, the resultant force W∥ − friction gets "
            "smaller, so the acceleration decreases."
        )},
    ]
    distractors = [
        {"value": "It increases, because the friction force has more effect on a gentler slope.",
         "mistake": "Friction stays the same regardless of angle here — it's W∥ that shrinks as the slope becomes gentler, reducing the resultant force and the acceleration.",
         "working": working},
        {"value": "It stays the same, because friction is constant.",
         "mistake": "Friction being constant doesn't mean the resultant force is constant — W∥ = mg sin θ still changes with angle, and it's the resultant of W∥ and friction that sets the acceleration.",
         "working": working},
        {"value": "It decreases to zero immediately, since a smaller angle means no motion is possible.",
         "mistake": "A smaller angle reduces the acceleration, but doesn't necessarily make it zero — that only happens if W∥ becomes exactly equal to (or less than) the friction force.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def _explain_weight_constant(level):
    obj = _obj()
    context = f"A {obj} of fixed mass is placed on ramps of different angles, one after another."
    question_text = "What happens to the crate's weight as the ramp angle changes, and why?"
    correct = (
        "It stays the same, because weight is W = mg, which depends only on mass and g — "
        "not on the angle of the ramp."
    )
    working = [
        {"type": "text", "content": (
            "Weight W = mg depends only on mass and the gravitational field strength g, "
            "neither of which changes when the ramp's angle changes. Changing the angle "
            "changes how the weight is *resolved* into components, but not the weight itself."
        )},
    ]
    distractors = [
        {"value": "It increases as the ramp angle increases, since more of the crate's weight is needed to hold it in place.",
         "mistake": "This confuses weight with the parallel component of weight (W∥ = W sin θ), which does change with angle — the weight itself, W = mg, does not.",
         "working": working},
        {"value": "It decreases as the ramp angle increases, because the normal force supports more of it.",
         "mistake": "The normal force (W cos θ) does decrease with angle, but that doesn't change the crate's actual weight — W = mg is fixed.",
         "working": working},
        {"value": "It depends on the angle, because weight is a component of the resolved force system.",
         "mistake": "Weight is the original force being resolved, not one of its components — W = mg is independent of how it's later split into W∥ and W⊥.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def gen_rf_l6_explain_angle(level="Higher"):
    builder = random.choice([
        _explain_tension, _explain_mass_parallel, _explain_wpar_increases,
        _explain_vertical_tension, _explain_accel_decreases, _explain_weight_constant,
    ])
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
        notes=_NOTES,
        metadata={"type": "classification", "options": options},
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Components of Vectors", level=level,
        is_scenario=True, scenario_context=context, parts=[part],
    )
