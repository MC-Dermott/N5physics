import random
import math
import pathlib
from core.models.question_model import PhysicsQuestion

g = 9.8  # m/s²

_PROJECTILE_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "projectile_higher_widget.html"
).read_text(encoding="utf-8")


def _with_projectile_widget(question):
    question.metadata["widget_html"] = _PROJECTILE_WIDGET_HTML
    question.metadata["widget_height"] = 950
    return question

_NOTES_PROJECTILE = """
## Projectile Motion — Key Facts (Higher)

- Horizontal and vertical motion are **independent** of each other — analyse them separately.
- Horizontal velocity is constant throughout the flight:
$$v_H = v\\cos\\theta$$
- Vertical velocity changes under gravity, starting from:
$$v_V = v\\sin\\theta$$
- Vertical acceleration is constant, $a = -9.8\\ \\mathrm{m/s^2}$ (taking upward as positive);
  horizontal acceleration = 0.
- At the highest point of the flight, vertical velocity = 0.

**Equations of motion:**

Vertical (constant acceleration, $a = \\pm 9.8\\ \\mathrm{m/s^2}$):
$$v = u + at \\qquad s = ut + \\tfrac{1}{2}at^2$$

Horizontal (constant velocity, $a = 0$):
$$s = vt$$
"""

# 45° excluded — at 45° sin θ = cos θ so the sin/cos swap distractors would equal the correct answer
_ANGLES = [25, 30, 35, 40, 50, 55, 60, 65]
_SPEEDS = [10, 12, 15, 18, 20, 22, 25, 28, 30]

_CONTEXTS_L1 = [
    "A ball is kicked from flat ground at **{v} m/s** at **{theta}°** above the horizontal.",
    "A golf ball is struck at **{v} m/s** at an angle of **{theta}°** to the horizontal on a flat course.",
    "A stone is thrown from flat ground at **{v} m/s** at **{theta}°** to the horizontal, landing at the same level.",
    "A ball is projected at **{v} m/s** at **{theta}°** above the horizontal and lands on the same flat surface.",
    "A javelin is thrown at **{v} m/s** at an angle of **{theta}°** to the horizontal, landing on flat ground.",
]

_CONTEXTS_L2_HUMAN = [
    "A shot putter releases the shot at **{v} m/s** at **{theta}°** above the horizontal, from a height of **{h} m**.",
    "A javelin thrower releases the javelin at **{v} m/s** at **{theta}°** above the horizontal, from a height of **{h} m**.",
    "A basketball player shoots at **{v} m/s** at **{theta}°** above the horizontal, releasing the ball from a height of **{h} m**.",
]

_CONTEXTS_L2_ELEVATED = [
    "A ball is kicked at **{v} m/s** at **{theta}°** above the horizontal from the top of a cliff **{h} m** above the sea.",
    "A stone is thrown at **{v} m/s** at **{theta}°** above the horizontal from a platform **{h} m** above the ground.",
    "A ball is thrown at **{v} m/s** at **{theta}°** above the horizontal from the top of a building **{h} m** high.",
]

_L2_HUMAN_HEIGHTS = [1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2]
_L2_ELEVATED_HEIGHTS = [10, 15, 20, 25, 30, 40, 50, 60]


def _r2(val):
    return round(float(val), 2)


def _r3(val):
    return round(float(val), 3)


# ── Level 1 — Angled launch, lands at same height ────────────────────────────

def generate_projectile_l1(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)

    v_H     = _r2(v * math.cos(theta))
    v_V     = _r2(v * math.sin(theta))
    t_up    = _r2(v_V / g)
    t_total = _r2(2 * t_up)
    R       = _r2(v_H * t_total)

    vH_sin  = _r2(v * math.sin(theta))  # sin/cos swapped for part (a)
    vV_cos  = _r2(v * math.cos(theta))  # sin/cos swapped for part (b)
    t_d2    = _r2(2 * v / g)            # used full speed instead of v_V for time

    context = random.choice(_CONTEXTS_L1).format(v=v, theta=theta_deg)

    # ── Part (a): horizontal component ───────────────────────────────────────
    working_vH = [
        {"type": "text",  "content": "Resolve the initial velocity into components:"},
        {"type": "latex", "content": r"v_H = v \cos\theta"},
        {"type": "latex", "content": rf"v_H = {v} \times \cos {theta_deg}°"},
        {"type": "latex", "content": rf"v_H = {v_H}\ \mathrm{{m/s}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the horizontal component of the initial velocity.",
        correct_answer=v_H,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": vH_sin,
                "mistake": (
                    f"The **horizontal** component uses cos θ, not sin θ. "
                    f"v_H = v × cos {theta_deg}° = {v} × {round(math.cos(theta), 3)} = {v_H} m/s."
                ),
                "working": working_vH,
            },
            {
                "value": float(v),
                "mistake": (
                    f"This is the full initial speed. "
                    f"The horizontal component is v_H = v × cos {theta_deg}° = {v_H} m/s."
                ),
                "working": working_vH,
            },
        ],
        working=working_vH,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (b): vertical component ─────────────────────────────────────────
    working_vV = [
        {"type": "text",  "content": "The vertical component:"},
        {"type": "latex", "content": r"v_V = v \sin\theta"},
        {"type": "latex", "content": rf"v_V = {v} \times \sin {theta_deg}°"},
        {"type": "latex", "content": rf"v_V = {v_V}\ \mathrm{{m/s}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the vertical component of the initial velocity.",
        correct_answer=v_V,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": vV_cos,
                "mistake": (
                    f"The **vertical** component uses sin θ, not cos θ. "
                    f"v_V = v × sin {theta_deg}° = {v} × {round(math.sin(theta), 3)} = {v_V} m/s."
                ),
                "working": working_vV,
            },
            {
                "value": float(v),
                "mistake": (
                    f"This is the initial speed. "
                    f"The vertical component is v_V = v × sin {theta_deg}° = {v_V} m/s."
                ),
                "working": working_vV,
            },
        ],
        working=working_vV,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (c): total time of flight ────────────────────────────────────────
    working_t = [
        {"type": "text",  "content": "At maximum height, vertical velocity = 0. Find time to the top:"},
        {"type": "latex", "content": r"v = u + at \;\Rightarrow\; 0 = v_V - g\,t_{\text{up}}"},
        {"type": "latex", "content": rf"t_{{\text{{up}}}} = \frac{{v_V}}{{g}} = \frac{{{v_V}}}{{9.8}} = {t_up}\ \mathrm{{s}}"},
        {"type": "text",  "content": "The projectile lands at the same height as it was launched, so the descent takes the same time:"},
        {"type": "latex", "content": rf"t_{{\text{{total}}}} = 2 \times t_{{\text{{up}}}} = 2 \times {t_up} = {t_total}\ \mathrm{{s}}"},
    ]
    part_c = PhysicsQuestion(
        question_text="Calculate the total time of flight.",
        correct_answer=t_total,
        unit="s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": t_up,
                "mistake": (
                    f"This is only the time to reach maximum height ({t_up} s). "
                    f"Since the projectile returns to the **same height**, descent takes equally long. "
                    f"t_total = 2 × {t_up} = {t_total} s."
                ),
                "working": working_t,
            },
            {
                "value": t_d2,
                "mistake": (
                    f"Use the **vertical component** of velocity, not the full initial speed. "
                    f"t_up = v_V / g = {v_V} / 9.8 = {t_up} s, "
                    f"so t_total = 2 × {t_up} = {t_total} s."
                ),
                "working": working_t,
            },
        ],
        working=working_t,
        notes=_NOTES_PROJECTILE,
        scaffold=[
            {"prompt": "What is the time to reach maximum height, t_up?", "answer": t_up},
            {"prompt": "What is the total time of flight, t_total?", "answer": t_total},
        ],
    )

    # ── Part (d): horizontal range ────────────────────────────────────────────
    working_R = [
        {"type": "text",  "content": "Horizontal velocity is constant throughout. Use the total time:"},
        {"type": "latex", "content": r"R = v_H \times t_{\text{total}}"},
        {"type": "latex", "content": rf"R = {v_H} \times {t_total}"},
        {"type": "latex", "content": rf"R = {R}\ \mathrm{{m}}"},
    ]
    part_d = PhysicsQuestion(
        question_text="Calculate the horizontal range.",
        correct_answer=R,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(v_H * t_up),
                "mistake": (
                    f"You appear to have used t = {t_up} s (time to reach the top). "
                    f"Use the **total** flight time: R = v_H × t_total = {v_H} × {t_total} = {R} m."
                ),
                "working": working_R,
            },
            {
                "value": _r2(v * t_total),
                "mistake": (
                    f"Use the **horizontal component** (v_H = {v_H} m/s), "
                    f"not the full initial speed ({v} m/s). "
                    f"R = {v_H} × {t_total} = {R} m."
                ),
                "working": working_R,
            },
        ],
        working=working_R,
        notes=_NOTES_PROJECTILE,
    )

    return _with_projectile_widget(PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part_a, part_b, part_c, part_d],
    ))


# ── Level 2 — Angled launch from a height (asymmetric) ───────────────────────

def generate_projectile_l2(level="Higher"):
    if random.random() < 0.5:
        return _generate_projectile_l2_time(level)
    return _generate_projectile_l2_maxheight(level)


def _generate_projectile_l2_time(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)

    is_human = random.random() < 0.5
    if is_human:
        h = random.choice(_L2_HUMAN_HEIGHTS)
        context = random.choice(_CONTEXTS_L2_HUMAN)
    else:
        h = random.choice(_L2_ELEVATED_HEIGHTS)
        context = random.choice(_CONTEXTS_L2_ELEVATED)
    context = context.format(v=v, theta=theta_deg, h=h)

    v_H  = _r2(v * math.cos(theta))
    v_V  = _r2(v * math.sin(theta))
    v_y  = _r2(math.sqrt(v_V ** 2 + 2 * g * h))
    t    = _r3((v_y + v_V) / g)
    R    = _r2(v_H * t)

    vH_sin = _r2(v * math.sin(theta))  # sin/cos swapped
    vV_cos = _r2(v * math.cos(theta))  # sin/cos swapped

    # ── Part (a): horizontal component ───────────────────────────────────────
    working_vH = [
        {"type": "text",  "content": "Resolve the initial velocity into components:"},
        {"type": "latex", "content": r"v_H = v \cos\theta"},
        {"type": "latex", "content": rf"v_H = {v} \times \cos {theta_deg}°"},
        {"type": "latex", "content": rf"v_H = {v_H}\ \mathrm{{m/s}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the horizontal component of the initial velocity.",
        correct_answer=v_H,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": vH_sin,
                "mistake": (
                    f"The **horizontal** component uses cos θ, not sin θ. "
                    f"v_H = v × cos {theta_deg}° = {v} × {round(math.cos(theta), 3)} = {v_H} m/s."
                ),
                "working": working_vH,
            },
            {
                "value": float(v),
                "mistake": (
                    f"This is the full initial speed. "
                    f"The horizontal component is v_H = v × cos {theta_deg}° = {v_H} m/s."
                ),
                "working": working_vH,
            },
        ],
        working=working_vH,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (b): vertical component ─────────────────────────────────────────
    working_vV = [
        {"type": "text",  "content": "The vertical component:"},
        {"type": "latex", "content": r"v_V = v \sin\theta"},
        {"type": "latex", "content": rf"v_V = {v} \times \sin {theta_deg}°"},
        {"type": "latex", "content": rf"v_V = {v_V}\ \mathrm{{m/s}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the vertical component of the initial velocity.",
        correct_answer=v_V,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": vV_cos,
                "mistake": (
                    f"The **vertical** component uses sin θ, not cos θ. "
                    f"v_V = v × sin {theta_deg}° = {v} × {round(math.sin(theta), 3)} = {v_V} m/s."
                ),
                "working": working_vV,
            },
            {
                "value": float(v),
                "mistake": (
                    f"This is the initial speed. "
                    f"The vertical component is v_V = v × sin {theta_deg}° = {v_V} m/s."
                ),
                "working": working_vV,
            },
        ],
        working=working_vV,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (c): vertical velocity just before landing ──────────────────────
    vV2p2gh = _r2(v_V ** 2 + 2 * g * h)
    working_vy = [
        {"type": "text",  "content": (
            f"Unlike a launch on flat ground, this lands {h:g} m **below** the launch point, "
            f"so the final vertical speed is larger than v_V. Use v² = u² + 2gh:"
        )},
        {"type": "latex", "content": r"v_y = \sqrt{v_V^2 + 2gh}"},
        {"type": "latex", "content": rf"v_y = \sqrt{{{v_V}^2 + 2 \times 9.8 \times {h:g}}}"},
        {"type": "latex", "content": rf"v_y = \sqrt{{{vV2p2gh}}}"},
        {"type": "latex", "content": rf"v_y = {v_y}\ \mathrm{{m/s}}"},
    ]
    part_c = PhysicsQuestion(
        question_text="Calculate the vertical velocity of the projectile just before it lands.",
        correct_answer=v_y,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": v_V,
                "mistake": (
                    f"This is just the initial vertical component, v_V. Since the projectile falls "
                    f"an extra {h:g} m below the launch point, it lands faster than it was launched. "
                    f"v_y = √(v_V² + 2gh) = {v_y} m/s."
                ),
                "working": working_vy,
            },
            {
                "value": _r2(math.sqrt(v_V ** 2 + g * h)),
                "mistake": (
                    f"You appear to have left out the factor of 2. "
                    f"Use v_y = √(v_V² + 2gh) = √({v_V}² + 2×9.8×{h:g}) = {v_y} m/s."
                ),
                "working": working_vy,
            },
        ],
        working=working_vy,
        notes=_NOTES_PROJECTILE,
        scaffold=[
            {"prompt": "What is v_V² + 2gh?", "answer": vV2p2gh},
            {"prompt": "What is the vertical velocity just before landing, v_y?", "answer": v_y},
        ],
    )

    # ── Part (d): time of flight ──────────────────────────────────────────────
    working_t = [
        {"type": "text",  "content": "Use v = u + gt, rearranged for t (vertical motion, taking down as positive):"},
        {"type": "latex", "content": r"t = \frac{v_y + v_V}{g}"},
        {"type": "latex", "content": rf"t = \frac{{{v_y} + {v_V}}}{{9.8}}"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    part_d = PhysicsQuestion(
        question_text="Calculate the total time of flight.",
        correct_answer=t,
        unit="s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r3(v_y / g),
                "mistake": (
                    f"You left out v_V — the projectile was already moving upward at "
                    f"{v_V} m/s when it launched. t = (v_y + v_V) ÷ g = {t} s."
                ),
                "working": working_t,
            },
            {
                "value": _r3(2 * v_V / g),
                "mistake": (
                    f"That formula (t = 2v_V/g) only works when the landing height equals the "
                    f"launch height. Here it lands lower, so use t = (v_y + v_V) ÷ g = {t} s."
                ),
                "working": working_t,
            },
        ],
        working=working_t,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (e): horizontal range ────────────────────────────────────────────
    working_R = [
        {"type": "text",  "content": "Horizontal velocity is constant throughout. Use the total time:"},
        {"type": "latex", "content": r"R = v_H \times t"},
        {"type": "latex", "content": rf"R = {v_H} \times {t}"},
        {"type": "latex", "content": rf"R = {R}\ \mathrm{{m}}"},
    ]
    part_e = PhysicsQuestion(
        question_text="Calculate the range.",
        correct_answer=R,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(v * t),
                "mistake": (
                    f"Use the **horizontal component** (v_H = {v_H} m/s), "
                    f"not the full initial speed ({v} m/s). "
                    f"R = {v_H} × {t} = {R} m."
                ),
                "working": working_R,
            },
            {
                "value": _r2(v_H * v_V / g),
                "mistake": (
                    f"Check your time of flight — use t = (v_y + v_V) ÷ g = {t} s, "
                    f"then R = v_H × t = {v_H} × {t} = {R} m."
                ),
                "working": working_R,
            },
        ],
        working=working_R,
        notes=_NOTES_PROJECTILE,
        scaffold=[
            {"prompt": "What is the total time of flight, t?", "answer": t},
            {"prompt": "What is the range, R?", "answer": R},
        ],
    )

    return _with_projectile_widget(PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part_a, part_b, part_c, part_d, part_e],
    ))


def _generate_projectile_l2_maxheight(level="Higher", include_range=False):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)

    is_human = random.random() < 0.5
    if is_human:
        h = random.choice(_L2_HUMAN_HEIGHTS)
        context = random.choice(_CONTEXTS_L2_HUMAN)
    else:
        h = random.choice(_L2_ELEVATED_HEIGHTS)
        context = random.choice(_CONTEXTS_L2_ELEVATED)
    context = context.format(v=v, theta=theta_deg, h=h)

    v_H  = _r2(v * math.cos(theta))
    v_V  = _r2(v * math.sin(theta))
    t_up = _r2(v_V / g)
    h_max = _r2(v_V ** 2 / (2 * g))
    H_top = _r2(h + h_max)

    t_fall_full = math.sqrt(2 * H_top / g)
    t2 = round(random.uniform(0.35, 0.75) * t_fall_full, 2)
    s = _r2(0.5 * g * t2 ** 2)
    h_final = _r2(H_top - s)

    vH_sin = _r2(v * math.sin(theta))  # sin/cos swapped
    vV_cos = _r2(v * math.cos(theta))  # sin/cos swapped
    t_full_v = _r2(v / g)              # used full speed instead of v_V

    # ── Part (a): horizontal component ───────────────────────────────────────
    working_vH = [
        {"type": "text",  "content": "Resolve the initial velocity into components:"},
        {"type": "latex", "content": r"v_H = v \cos\theta"},
        {"type": "latex", "content": rf"v_H = {v} \times \cos {theta_deg}°"},
        {"type": "latex", "content": rf"v_H = {v_H}\ \mathrm{{m/s}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the horizontal component of the initial velocity.",
        correct_answer=v_H,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": vH_sin,
                "mistake": (
                    f"The **horizontal** component uses cos θ, not sin θ. "
                    f"v_H = v × cos {theta_deg}° = {v} × {round(math.cos(theta), 3)} = {v_H} m/s."
                ),
                "working": working_vH,
            },
            {
                "value": float(v),
                "mistake": (
                    f"This is the full initial speed. "
                    f"The horizontal component is v_H = v × cos {theta_deg}° = {v_H} m/s."
                ),
                "working": working_vH,
            },
        ],
        working=working_vH,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (b): vertical component ─────────────────────────────────────────
    working_vV = [
        {"type": "text",  "content": "The vertical component:"},
        {"type": "latex", "content": r"v_V = v \sin\theta"},
        {"type": "latex", "content": rf"v_V = {v} \times \sin {theta_deg}°"},
        {"type": "latex", "content": rf"v_V = {v_V}\ \mathrm{{m/s}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the vertical component of the initial velocity.",
        correct_answer=v_V,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": vV_cos,
                "mistake": (
                    f"The **vertical** component uses sin θ, not cos θ. "
                    f"v_V = v × sin {theta_deg}° = {v} × {round(math.sin(theta), 3)} = {v_V} m/s."
                ),
                "working": working_vV,
            },
            {
                "value": float(v),
                "mistake": (
                    f"This is the initial speed. "
                    f"The vertical component is v_V = v × sin {theta_deg}° = {v_V} m/s."
                ),
                "working": working_vV,
            },
        ],
        working=working_vV,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (c): time to reach maximum height ────────────────────────────────
    working_t = [
        {"type": "text",  "content": "At maximum height, vertical velocity = 0:"},
        {"type": "latex", "content": r"v = u + at \;\Rightarrow\; 0 = v_V - g\,t_{\text{up}}"},
        {"type": "latex", "content": rf"t_{{\text{{up}}}} = \frac{{v_V}}{{g}} = \frac{{{v_V}}}{{9.8}} = {t_up}\ \mathrm{{s}}"},
    ]
    part_c = PhysicsQuestion(
        question_text="Calculate the time taken for the projectile to reach its maximum height.",
        correct_answer=t_up,
        unit="s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": t_full_v,
                "mistake": (
                    f"Use the **vertical component** of the launch velocity, not the full speed. "
                    f"v_V = v sin {theta_deg}° = {v_V} m/s, so t_up = v_V ÷ g = {t_up} s."
                ),
                "working": working_t,
            },
            {
                "value": _r2(v_H / g),
                "mistake": (
                    f"That uses the horizontal component. Only the **vertical** component "
                    f"decreases to zero at maximum height: t_up = v_V ÷ g = {v_V} ÷ 9.8 = {t_up} s."
                ),
                "working": working_t,
            },
        ],
        working=working_t,
        notes=_NOTES_PROJECTILE,
        scaffold=[
            {"prompt": "What is v_V (the vertical component of the launch velocity)?", "answer": v_V},
            {"prompt": "What is the time to reach maximum height, t_up?", "answer": t_up},
        ],
    )

    # ── Part (d): height above ground a further time after maximum height ────
    working_h = [
        {"type": "text",  "content": (
            f"The projectile rises {h_max} m above its launch point, "
            f"so its height above the **ground** at maximum height is:"
        )},
        {"type": "latex", "content": r"H_{\text{top}} = h + \frac{v_V^2}{2g}"},
        {"type": "latex", "content": rf"H_{{\text{{top}}}} = {h:g} + \frac{{{v_V}^2}}{{2 \times 9.8}} = {H_top}\ \mathrm{{m}}"},
        {"type": "text",  "content": (
            f"A further {t2} s after reaching maximum height, the projectile has fallen "
            f"(from rest, vertically):"
        )},
        {"type": "latex", "content": r"s = \tfrac{1}{2} g t_2^2"},
        {"type": "latex", "content": rf"s = \tfrac{{1}}{{2}} \times 9.8 \times {t2}^2 = {s}\ \mathrm{{m}}"},
        {"type": "text",  "content": "So its height above the ground is:"},
        {"type": "latex", "content": r"h = H_{\text{top}} - s"},
        {"type": "latex", "content": rf"h = {H_top} - {s} = {h_final}\ \mathrm{{m}}"},
    ]
    part_d = PhysicsQuestion(
        question_text=(
            f"The projectile takes a further {t2} s to fall from its maximum height. "
            f"Calculate its height above the ground at this time."
        ),
        correct_answer=h_final,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(h_max - s),
                "mistake": (
                    f"You appear to have forgotten to add the launch height h. The height above "
                    f"the ground at maximum height is H_top = h + v_V²/2g = {H_top} m, "
                    f"so h = {H_top} − {s} = {h_final} m."
                ),
                "working": working_h,
            },
            {
                "value": _r2(H_top - g * t2 ** 2),
                "mistake": (
                    f"You appear to have left out the factor of ½ when finding the distance "
                    f"fallen. Use s = ½ g t₂² = {s} m, so h = {H_top} − {s} = {h_final} m."
                ),
                "working": working_h,
            },
        ],
        working=working_h,
        notes=_NOTES_PROJECTILE,
        scaffold=[
            {"prompt": "What is the height above the ground at maximum height, H_top?", "answer": H_top},
            {"prompt": f"What distance does the projectile fall in the further {t2} s, s?", "answer": s},
            {"prompt": "What is the height above the ground when it hits, h?", "answer": h_final},
        ],
    )

    parts = [part_a, part_b, part_c, part_d]

    if include_range:
        # ── Part (e): horizontal distance travelled by the time it hits ───────
        t_total_flight = _r2(t_up + t2)
        R = _r2(v_H * t_total_flight)
        working_R = [
            {"type": "text",  "content": (
                f"The projectile has been in flight for t_up + t_2 since it launched:"
            )},
            {"type": "latex", "content": r"t_{\text{total}} = t_{\text{up}} + t_2"},
            {"type": "latex", "content": rf"t_{{\text{{total}}}} = {t_up} + {t2} = {t_total_flight}\ \mathrm{{s}}"},
            {"type": "text",  "content": "Horizontal velocity is constant throughout, so:"},
            {"type": "latex", "content": r"R = v_H \times t_{\text{total}}"},
            {"type": "latex", "content": rf"R = {v_H} \times {t_total_flight} = {R}\ \mathrm{{m}}"},
        ]
        part_e = PhysicsQuestion(
            question_text="Calculate the horizontal distance travelled by the projectile by the time it reaches this height.",
            correct_answer=R,
            unit="m",
            topic="Our Dynamic Universe",
            question_type="Projectile Motion",
            level=level,
            distractors=[
                {
                    "value": _r2(v_H * t2),
                    "mistake": (
                        f"You appear to have only used the further time t₂ = {t2} s, forgetting "
                        f"the time already spent rising to maximum height. "
                        f"t_total = t_up + t₂ = {t_up} + {t2} = {t_total_flight} s, "
                        f"so R = {v_H} × {t_total_flight} = {R} m."
                    ),
                    "working": working_R,
                },
                {
                    "value": _r2(v * t_total_flight),
                    "mistake": (
                        f"Use the **horizontal component** (v_H = {v_H} m/s), not the full "
                        f"initial speed ({v} m/s). R = {v_H} × {t_total_flight} = {R} m."
                    ),
                    "working": working_R,
                },
            ],
            working=working_R,
            notes=_NOTES_PROJECTILE,
            scaffold=[
                {"prompt": "What is the total time of flight, t_up + t_2?", "answer": t_total_flight},
                {"prompt": "What is the horizontal distance travelled, R?", "answer": R},
            ],
        )
        parts.append(part_e)

    return _with_projectile_widget(PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=parts,
    ))


# ── Exam Style — working backwards from the horizontal direction ────────────

def _generate_projectile_exam_backwards(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)

    v_H       = _r2(v * math.cos(theta))
    v_V_true  = _r2(v * math.sin(theta))
    t_up_true = _r2(v_V_true / g)
    t_total   = _r2(2 * t_up_true)
    R         = _r2(v_H * t_total)

    # Backward chain — what a student actually derives from the given R and v_H.
    # Recomputed rather than reusing v_V_true/t_up_true above, so every number shown
    # in the workings is self-consistent with the stored answer key.
    t_up  = _r2(t_total / 2)
    v_V   = _r2(g * t_up)
    h_max = _r2(v_V ** 2 / (2 * g))

    vH_sin        = _r2(v * math.sin(theta))  # sin/cos swapped
    vV_wrong_half = _r2(g * t_total)          # forgot to halve t_total before finding v_V

    base_context = random.choice(_CONTEXTS_L1).format(v=v, theta=theta_deg)
    context = f"{base_context} The projectile lands {R:g} m from the launch point."

    # ── Part (a): horizontal component ───────────────────────────────────────
    working_vH = [
        {"type": "text",  "content": "Resolve the initial velocity into components:"},
        {"type": "latex", "content": r"v_H = v \cos\theta"},
        {"type": "latex", "content": rf"v_H = {v} \times \cos {theta_deg}°"},
        {"type": "latex", "content": rf"v_H = {v_H}\ \mathrm{{m/s}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the horizontal component of the initial velocity.",
        correct_answer=v_H,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": vH_sin,
                "mistake": (
                    f"The **horizontal** component uses cos θ, not sin θ. "
                    f"v_H = v × cos {theta_deg}° = {v} × {round(math.cos(theta), 3)} = {v_H} m/s."
                ),
                "working": working_vH,
            },
            {
                "value": float(v),
                "mistake": (
                    f"This is the full initial speed. "
                    f"The horizontal component is v_H = v × cos {theta_deg}° = {v_H} m/s."
                ),
                "working": working_vH,
            },
        ],
        working=working_vH,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (b): total time of flight, worked from the horizontal direction ──
    working_t = [
        {"type": "text",  "content": "Horizontal velocity is constant, so the range and time of flight are related by:"},
        {"type": "latex", "content": r"R = v_H \times t_{\text{total}}"},
        {"type": "latex", "content": rf"t_{{\text{{total}}}} = \frac{{R}}{{v_H}} = \frac{{{R:g}}}{{{v_H}}} = {t_total}\ \mathrm{{s}}"},
    ]
    part_b = PhysicsQuestion(
        question_text=(
            f"The projectile lands {R:g} m from the launch point. "
            f"Calculate the total time of flight."
        ),
        correct_answer=t_total,
        unit="s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(R / v),
                "mistake": (
                    f"Use the **horizontal component** v_H = {v_H} m/s, not the full initial "
                    f"speed. t_total = R ÷ v_H = {R:g} ÷ {v_H} = {t_total} s."
                ),
                "working": working_t,
            },
            {
                "value": t_up,
                "mistake": (
                    f"This is only the time to reach maximum height. Use the full range: "
                    f"t_total = R ÷ v_H = {R:g} ÷ {v_H} = {t_total} s."
                ),
                "working": working_t,
            },
        ],
        working=working_t,
        notes=_NOTES_PROJECTILE,
        scaffold=[
            {"prompt": "What is the horizontal component v_H?", "answer": v_H},
            {"prompt": "What is the total time of flight, t_total?", "answer": t_total},
        ],
    )

    # ── Part (c): vertical component of the launch velocity, from t_total ────
    working_vV = [
        {"type": "text",  "content": (
            "The projectile lands at the same height it was launched, so it takes equally "
            "long to rise as to fall — the time to reach maximum height is half the total:"
        )},
        {"type": "latex", "content": r"t_{\text{up}} = \frac{t_{\text{total}}}{2}"},
        {"type": "latex", "content": rf"t_{{\text{{up}}}} = \frac{{{t_total}}}{{2}} = {t_up}\ \mathrm{{s}}"},
        {"type": "text",  "content": "At maximum height, vertical velocity = 0, so from v = u + at:"},
        {"type": "latex", "content": r"v_V = g \times t_{\text{up}}"},
        {"type": "latex", "content": rf"v_V = 9.8 \times {t_up} = {v_V}\ \mathrm{{m/s}}"},
    ]
    part_c = PhysicsQuestion(
        question_text="Using this time, calculate the vertical component of the launch velocity.",
        correct_answer=v_V,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": vV_wrong_half,
                "mistake": (
                    f"You appear to have used the **total** time of flight instead of halving "
                    f"it first. t_up = t_total ÷ 2 = {t_up} s, so v_V = g × t_up = {v_V} m/s."
                ),
                "working": working_vV,
            },
            {
                "value": v_H,
                "mistake": (
                    f"That's the horizontal component. The vertical component is found from "
                    f"v_V = g × t_up = 9.8 × {t_up} = {v_V} m/s."
                ),
                "working": working_vV,
            },
        ],
        working=working_vV,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (d): maximum height reached ──────────────────────────────────────
    working_h = [
        {"type": "text",  "content": "Using the vertical component of the launch velocity:"},
        {"type": "latex", "content": r"h_{\text{max}} = \frac{v_V^2}{2g}"},
        {"type": "latex", "content": rf"h_{{\text{{max}}}} = \frac{{{v_V}^2}}{{2 \times 9.8}} = {h_max}\ \mathrm{{m}}"},
    ]
    part_d = PhysicsQuestion(
        question_text="Calculate the maximum height reached by the projectile.",
        correct_answer=h_max,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(v_V ** 2 / g),
                "mistake": (
                    f"You appear to have left out the factor of 2 in the denominator. "
                    f"h_max = v_V² ÷ (2g) = {v_V}² ÷ 19.6 = {h_max} m."
                ),
                "working": working_h,
            },
            {
                "value": _r2(v ** 2 / (2 * g)),
                "mistake": (
                    f"Use the **vertical component** v_V = {v_V} m/s, not the full launch speed. "
                    f"h_max = v_V² ÷ (2g) = {h_max} m."
                ),
                "working": working_h,
            },
        ],
        working=working_h,
        notes=_NOTES_PROJECTILE,
    )

    return _with_projectile_widget(PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part_a, part_b, part_c, part_d],
    ))


# ── Exam Style — does it clear the target? ───────────────────────────────────

_CONTEXTS_TARGET = [
    "A ball is kicked from flat ground at **{v} m/s** at **{theta}°** above the horizontal, towards a wall **{y_target:g} m** high, standing **{x_target:g} m** away.",
    "A javelin is thrown from flat ground at **{v} m/s** at **{theta}°** to the horizontal, towards a fence **{y_target:g} m** high, positioned **{x_target:g} m** from the thrower.",
    "A rugby ball is kicked from flat ground at **{v} m/s** at **{theta}°** above the horizontal, towards a crossbar **{y_target:g} m** high, **{x_target:g} m** from the kicker.",
]


def _generate_projectile_exam_target(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)

    v_H            = _r2(v * math.cos(theta))
    v_V            = _r2(v * math.sin(theta))
    t_total_flight = _r2(2 * v_V / g)
    R_total        = _r2(v_H * t_total_flight)
    h_max          = _r2(v_V ** 2 / (2 * g))

    x_target = round(R_total * random.uniform(0.25, 0.85), 1)
    t_reach  = _r3(x_target / v_H)
    y_actual = _r2(v_V * t_reach - 0.5 * g * t_reach ** 2)

    y_target = round(random.uniform(0.5, max(1.5, h_max * 1.4)), 1)
    clears   = y_actual > y_target

    context = random.choice(_CONTEXTS_TARGET).format(
        v=v, theta=theta_deg, x_target=x_target, y_target=y_target
    )

    vH_sin = _r2(v * math.sin(theta))  # sin/cos swapped
    vV_cos = _r2(v * math.cos(theta))  # sin/cos swapped

    # ── Part (a): horizontal component ───────────────────────────────────────
    working_vH = [
        {"type": "text",  "content": "Resolve the initial velocity into components:"},
        {"type": "latex", "content": r"v_H = v \cos\theta"},
        {"type": "latex", "content": rf"v_H = {v} \times \cos {theta_deg}°"},
        {"type": "latex", "content": rf"v_H = {v_H}\ \mathrm{{m/s}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the horizontal component of the initial velocity.",
        correct_answer=v_H,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": vH_sin,
                "mistake": (
                    f"The **horizontal** component uses cos θ, not sin θ. "
                    f"v_H = v × cos {theta_deg}° = {v} × {round(math.cos(theta), 3)} = {v_H} m/s."
                ),
                "working": working_vH,
            },
            {
                "value": float(v),
                "mistake": (
                    f"This is the full initial speed. "
                    f"The horizontal component is v_H = v × cos {theta_deg}° = {v_H} m/s."
                ),
                "working": working_vH,
            },
        ],
        working=working_vH,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (b): vertical component ─────────────────────────────────────────
    working_vV = [
        {"type": "text",  "content": "The vertical component:"},
        {"type": "latex", "content": r"v_V = v \sin\theta"},
        {"type": "latex", "content": rf"v_V = {v} \times \sin {theta_deg}°"},
        {"type": "latex", "content": rf"v_V = {v_V}\ \mathrm{{m/s}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the vertical component of the initial velocity.",
        correct_answer=v_V,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": vV_cos,
                "mistake": (
                    f"The **vertical** component uses sin θ, not cos θ. "
                    f"v_V = v × sin {theta_deg}° = {v} × {round(math.sin(theta), 3)} = {v_V} m/s."
                ),
                "working": working_vV,
            },
            {
                "value": float(v),
                "mistake": (
                    f"This is the initial speed. "
                    f"The vertical component is v_V = v × sin {theta_deg}° = {v_V} m/s."
                ),
                "working": working_vV,
            },
        ],
        working=working_vV,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (c): time to reach the target's horizontal position ─────────────
    working_t = [
        {"type": "text",  "content": "Horizontal velocity is constant, so the time to travel this horizontal distance is:"},
        {"type": "latex", "content": r"t = \frac{x}{v_H}"},
        {"type": "latex", "content": rf"t = \frac{{{x_target:g}}}{{{v_H}}} = {t_reach}\ \mathrm{{s}}"},
    ]
    part_c = PhysicsQuestion(
        question_text=f"Calculate the time taken for the projectile to reach the target, {x_target:g} m away.",
        correct_answer=t_reach,
        unit="s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r3(x_target / v),
                "mistake": (
                    f"Use the **horizontal component** v_H = {v_H} m/s, not the full initial "
                    f"speed. t = x ÷ v_H = {x_target:g} ÷ {v_H} = {t_reach} s."
                ),
                "working": working_t,
            },
            {
                "value": _r3(x_target / v_V),
                "mistake": (
                    f"Horizontal distance is covered at the **horizontal** velocity, not the "
                    f"vertical component. t = x ÷ v_H = {x_target:g} ÷ {v_H} = {t_reach} s."
                ),
                "working": working_t,
            },
        ],
        working=working_t,
        notes=_NOTES_PROJECTILE,
    )

    # ── Part (d): height above the ground at that time ────────────────────────
    working_y = [
        {"type": "text",  "content": "Use the vertical equation of motion (taking upward as positive):"},
        {"type": "latex", "content": r"s = v_V t - \tfrac{1}{2} g t^2"},
        {"type": "latex", "content": rf"s = {v_V} \times {t_reach} - \tfrac{{1}}{{2}} \times 9.8 \times {t_reach}^2"},
        {"type": "latex", "content": rf"s = {y_actual}\ \mathrm{{m}}"},
    ]
    part_d = PhysicsQuestion(
        question_text="Calculate the height of the projectile above the ground at this time.",
        correct_answer=y_actual,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(v_V * t_reach),
                "mistake": (
                    f"You left out the effect of gravity. Use s = v_V t − ½gt² = "
                    f"{v_V} × {t_reach} − ½ × 9.8 × {t_reach}² = {y_actual} m."
                ),
                "working": working_y,
            },
            {
                "value": _r2(v_V * t_reach + 0.5 * g * t_reach ** 2),
                "mistake": (
                    f"Sign error — gravity decelerates the upward motion, so the term is "
                    f"subtracted, not added: s = v_V t − ½gt² = {y_actual} m."
                ),
                "working": working_y,
            },
        ],
        working=working_y,
        notes=_NOTES_PROJECTILE,
        scaffold=[
            {"prompt": "What is the time taken to reach the target, t?", "answer": t_reach},
            {"prompt": "What is the height of the projectile at this time?", "answer": y_actual},
        ],
    )

    # ── Part (e): does the projectile clear the target? ───────────────────────
    if clears:
        correct = (
            f"Yes, it clears the target — at the target's horizontal position the projectile "
            f"is {y_actual} m above the ground, which is higher than the target's height of "
            f"{y_target:g} m."
        )
        wrong_conclusion = (
            f"No, it hits the target — the projectile's height at the target's position is "
            f"lower than the target's height."
        )
    else:
        correct = (
            f"No, it hits the target — at the target's horizontal position the projectile is "
            f"only {y_actual} m above the ground, which is lower than the target's height of "
            f"{y_target:g} m."
        )
        wrong_conclusion = (
            f"Yes, it clears the target — the projectile's height at the target's position is "
            f"higher than the target's height."
        )

    working_e = working_y + [
        {"type": "text", "content": (
            f"Compare this height to the target's height of {y_target:g} m to decide whether "
            f"the projectile clears it or hits it."
        )},
    ]
    distractors_e = [
        {
            "value": wrong_conclusion,
            "mistake": (
                f"Check the comparison again: the projectile's height at the target's position "
                f"is {y_actual} m, and the target is {y_target:g} m high."
            ),
            "working": working_e,
        },
        {
            "value": "It cannot be determined without knowing the total range of the flight.",
            "mistake": (
                "You already have everything needed — the projectile's height exactly at the "
                "target's horizontal position, found from the time taken to reach it."
            ),
            "working": working_e,
        },
    ]
    options = [correct] + [d["value"] for d in distractors_e]
    random.shuffle(options)
    part_e = PhysicsQuestion(
        question_text=f"The target is {y_target:g} m high. Does the projectile clear it?",
        correct_answer=correct,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=distractors_e,
        working=working_e,
        metadata={"type": "classification", "options": options},
        notes=_NOTES_PROJECTILE,
    )

    return _with_projectile_widget(PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part_a, part_b, part_c, part_d, part_e],
    ))


# ── Exam Style — mix of same-height and different-height calculations ───────

def generate_projectile_exam_style(level="Higher"):
    variant = random.choice([
        "same_height",
        "diff_height_time",
        "diff_height_maxheight",
        "backwards_horizontal",
        "target",
    ])
    if variant == "same_height":
        return generate_projectile_l1(level)
    if variant == "diff_height_time":
        return _generate_projectile_l2_time(level)
    if variant == "diff_height_maxheight":
        return _generate_projectile_l2_maxheight(level, include_range=True)
    if variant == "backwards_horizontal":
        return _generate_projectile_exam_backwards(level)
    return _generate_projectile_exam_target(level)


# ── Explain — Conceptual Questions ───────────────────────────────────────────

def _exam_angle_symmetry(level="Higher"):
    theta_deg = random.choice([20, 25, 30, 35, 40])
    other_deg = 90 - theta_deg
    v = random.choice(_SPEEDS)

    context = (
        f"Two identical balls are launched from the same point on flat ground, both at "
        f"{v} m/s: one at {theta_deg}° above the horizontal, the other at {other_deg}° "
        f"above the horizontal. Both land at the same height from which they were launched."
    )
    question_text = (
        "Which statement correctly explains why both balls land the same horizontal "
        "distance from the launch point, despite being launched at different angles?"
    )
    correct = (
        f"Because {theta_deg}° and {other_deg}° are complementary angles, the horizontal "
        f"and vertical components of the two launches are swapped between them — this "
        f"leaves the range R = v_H × t_total unchanged."
    )
    working = [
        {"type": "text", "content": (
            f"For a launch at angle θ, v_H = v cos θ and v_V = v sin θ. For the complementary "
            f"angle (90° − θ), these components swap: v_H becomes v sin θ and v_V becomes "
            f"v cos θ."
        )},
        {"type": "latex", "content": r"R = v_H \times t_{\text{total}} = v_H \times \frac{2v_V}{g}"},
        {"type": "text", "content": (
            "Swapping v_H and v_V swaps the two factors being multiplied together, so the "
            "product — and therefore the range — is unchanged."
        )},
    ]
    distractors = [
        {"value": ("Because both balls have the same initial speed, they must land at the "
                    "same range regardless of angle."),
         "mistake": "Initial speed alone doesn't determine range — angle matters too. "
                    "A ball launched at 10° and one at 80° have the same speed but very "
                    "different ranges. It is specifically the complementary angles that "
                    "cause this pair to match.",
         "working": working},
        {"value": ("Because the time of flight is the same for both launches, so the range "
                    "must also be the same."),
         "mistake": f"The times of flight are actually different for {theta_deg}° and "
                    f"{other_deg}° — only their combination with the horizontal velocity "
                    "gives the same product.",
         "working": working},
        {"value": ("Because the vertical components of the two launches are equal, so both "
                    "balls reach the same maximum height and therefore the same range."),
         "mistake": "The vertical components are not equal (unless θ = 45°) — the two "
                    "balls actually reach different maximum heights. It is the swap of "
                    "v_H and v_V between the two angles that keeps the range the same.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def _exam_air_resistance(level="Higher"):
    v = random.choice(_SPEEDS)
    theta_deg = random.choice(_ANGLES)
    context = (
        f"A ball is launched at {v} m/s at {theta_deg}° above the horizontal. The range "
        f"and maximum height are first calculated assuming no air resistance."
    )
    question_text = (
        "A student says that if air resistance were included instead, the ball would "
        "travel further and higher than the calculated values. Which statement correctly "
        "explains the effect of air resistance?"
    )
    correct = (
        "Air resistance acts opposite to the ball's motion, reducing both its horizontal "
        "velocity and the speed of its vertical motion — so the real range and maximum "
        "height are both smaller than the calculated (no air resistance) values."
    )
    working = [
        {"type": "text", "content": (
            "Air resistance is a friction-like force that always opposes the direction "
            "of motion. It has a horizontal component that continuously slows the "
            "horizontal velocity (which is otherwise constant), reducing the range. It "
            "also acts against the vertical motion — reducing the height reached going "
            "up, and reducing the speed gained coming back down."
        )},
    ]
    distractors = [
        {"value": ("The student is correct — air resistance pushes the ball forward and "
                    "upward, increasing both the range and the maximum height."),
         "mistake": "Air resistance always opposes motion — it cannot push the ball "
                    "forward or upward. It reduces both the range and the maximum "
                    "height compared with the idealised (no air resistance) case.",
         "working": working},
        {"value": ("Air resistance only affects the vertical motion, so the maximum height "
                    "decreases but the horizontal range stays the same."),
         "mistake": "Air resistance has a component opposing the horizontal motion too "
                    "(since the ball is moving both horizontally and vertically), so the "
                    "horizontal velocity — and therefore the range — is reduced as well.",
         "working": working},
        {"value": ("Air resistance only affects the horizontal motion, so the range "
                    "decreases but the maximum height stays the same."),
         "mistake": "Air resistance opposes the ball's actual direction of travel, which "
                    "has a vertical component throughout the flight, so the maximum "
                    "height is reduced too, not just the range.",
         "working": working},
    ]
    return context, question_text, correct, distractors


def generate_projectile_explain(level="Higher"):
    builder = random.choice([_exam_angle_symmetry, _exam_air_resistance])
    context, question_text, correct, distractors = builder(level)

    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)

    part = PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=distractors,
        working=distractors[0]["working"],
        metadata={"type": "classification", "options": options},
        notes=_NOTES_PROJECTILE,
    )

    return _with_projectile_widget(PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part],
    ))
