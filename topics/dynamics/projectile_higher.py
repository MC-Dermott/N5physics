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

- Horizontal and vertical motion are **independent** — analyse them separately.
- Horizontal velocity is constant; vertical velocity changes under gravity.
- Acceleration is $-9.8\\ \\mathrm{m/s^2}$ vertically (taking upward as positive) and
  $0$ horizontally.
- At the highest point of the flight, vertical velocity $= 0$.

#### Velocity components

$$v_H = v\\cos\\theta \\qquad\\qquad v_V = v\\sin\\theta$$

#### Equations of motion

Vertical:
$$v = u + at \\qquad\\qquad s = ut + \\tfrac{1}{2}at^2$$

Horizontal:
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


# ── Shared setup: launch scenario + first three parts (v_H, v_V, t_up) ───────

def _l2_random_context(v, theta_deg):
    """Randomly a flat (same-height) launch, or one from a height above the
    ground (split between human-scale and elevated heights)."""
    if random.random() < 0.5:
        h = 0.0
        context = random.choice(_CONTEXTS_L1).format(v=v, theta=theta_deg)
    else:
        if random.random() < 0.5:
            h = random.choice(_L2_HUMAN_HEIGHTS)
            context = random.choice(_CONTEXTS_L2_HUMAN)
        else:
            h = random.choice(_L2_ELEVATED_HEIGHTS)
            context = random.choice(_CONTEXTS_L2_ELEVATED)
        context = context.format(v=v, theta=theta_deg, h=h)
    return h, context


def _l2_parts_abc(v, theta_deg, theta, v_H, v_V, t_up, level):
    vH_sin   = _r2(v * math.sin(theta))  # sin/cos swapped
    vV_cos   = _r2(v * math.cos(theta))  # sin/cos swapped
    t_full_v = _r2(v / g)                # used full speed instead of v_V

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
    working_tup = [
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
                "working": working_tup,
            },
            {
                "value": _r2(v_H / g),
                "mistake": (
                    f"That uses the horizontal component. Only the **vertical** component "
                    f"decreases to zero at maximum height: t_up = v_V ÷ g = {v_V} ÷ 9.8 = {t_up} s."
                ),
                "working": working_tup,
            },
        ],
        working=working_tup,
        notes=_NOTES_PROJECTILE,
        scaffold=[
            {"prompt": "What is v_V (the vertical component of the launch velocity)?", "answer": v_V},
            {"prompt": "What is the time to reach maximum height, t_up?", "answer": t_up},
        ],
    )

    return part_a, part_b, part_c


# ── Height above the ground, a given time after the highest point ────────────

def generate_projectile_height(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)
    h, context = _l2_random_context(v, theta_deg)

    v_H   = _r2(v * math.cos(theta))
    v_V   = _r2(v * math.sin(theta))
    t_up  = _r2(v_V / g)
    h_max = _r2(v_V ** 2 / (2 * g))
    H_top = _r2(h + h_max)
    t_down_full = _r2(math.sqrt(2 * H_top / g))

    part_a, part_b, part_c = _l2_parts_abc(v, theta_deg, theta, v_H, v_V, t_up, level)

    if random.random() < 0.5:
        # Given the full time to fall from the top to the ground, find that height.
        working_d = [
            {"type": "text",  "content": "At the top, vertical velocity = 0, so use s = ½gt² to find the height fallen in this time:"},
            {"type": "latex", "content": r"H_{\text{top}} = \tfrac{1}{2} g t_{\text{down}}^2"},
            {"type": "latex", "content": rf"H_{{\text{{top}}}} = \tfrac{{1}}{{2}} \times 9.8 \times {t_down_full}^2 = {H_top}\ \mathrm{{m}}"},
        ]
        part_d = PhysicsQuestion(
            question_text=(
                f"The projectile takes {t_down_full} s to fall from its maximum height to the "
                f"ground. Calculate the maximum height reached above the ground."
            ),
            correct_answer=H_top,
            unit="m",
            topic="Our Dynamic Universe",
            question_type="Projectile Motion",
            level=level,
            distractors=[
                {
                    "value": _r2(g * t_down_full ** 2),
                    "mistake": (
                        f"You appear to have left out the factor of ½. "
                        f"H_top = ½gt² = ½ × 9.8 × {t_down_full}² = {H_top} m."
                    ),
                    "working": working_d,
                },
                {
                    "value": _r2(0.5 * g * t_down_full),
                    "mistake": (
                        f"You appear to have forgotten to **square** the time. "
                        f"H_top = ½gt² = ½ × 9.8 × {t_down_full}² = {H_top} m, "
                        f"not ½ × 9.8 × {t_down_full}."
                    ),
                    "working": working_d,
                },
            ],
            working=working_d,
            notes=_NOTES_PROJECTILE,
        )
    else:
        # Given an intermediate time after the top, find the height above the ground then.
        t2 = round(random.uniform(0.25, 0.85) * t_down_full, 2)
        s  = _r2(0.5 * g * t2 ** 2)
        h_final = _r2(H_top - s)
        working_d = [
            {"type": "text",  "content": (
                f"At maximum height, the projectile is {H_top} m above the ground. "
                f"A further {t2} s later, it has fallen (from rest, vertically):"
            )},
            {"type": "latex", "content": r"s = \tfrac{1}{2} g t^2"},
            {"type": "latex", "content": rf"s = \tfrac{{1}}{{2}} \times 9.8 \times {t2}^2 = {s}\ \mathrm{{m}}"},
            {"type": "text",  "content": "So its height above the ground at this time is:"},
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
                    "value": _r2(H_top - g * t2 ** 2),
                    "mistake": (
                        f"You appear to have left out the factor of ½ when finding the distance "
                        f"fallen. Use s = ½gt² = {s} m, so h = {H_top} − {s} = {h_final} m."
                    ),
                    "working": working_d,
                },
                {
                    "value": _r2(H_top - 0.5 * g * t_up ** 2),
                    "mistake": (
                        f"You appear to have used the time to **rise** to the top "
                        f"(t_up = {t_up} s) instead of the given further time (t = {t2} s). "
                        f"h = H_top − ½g({t2})² = {H_top} − {s} = {h_final} m."
                    ),
                    "working": working_d,
                },
            ],
            working=working_d,
            notes=_NOTES_PROJECTILE,
            scaffold=[
                {"prompt": "What is the height above the ground at maximum height, H_top?", "answer": H_top},
                {"prompt": f"What distance does the projectile fall in the further {t2} s?", "answer": s},
                {"prompt": "What is the height above the ground at this time?", "answer": h_final},
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
        parts=[part_a, part_b, part_c, part_d],
    ))


# ── Time to fall a given distance from the highest point ─────────────────────

def generate_projectile_time(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)
    h, context = _l2_random_context(v, theta_deg)

    v_H   = _r2(v * math.cos(theta))
    v_V   = _r2(v * math.sin(theta))
    t_up  = _r2(v_V / g)
    h_max = _r2(v_V ** 2 / (2 * g))
    H_top = _r2(h + h_max)

    part_a, part_b, part_c = _l2_parts_abc(v, theta_deg, theta, v_H, v_V, t_up, level)

    if random.random() < 0.5:
        # Given the full height above the ground, find the time to fall all the way down.
        t_down = _r2(math.sqrt(2 * H_top / g))
        working_d = [
            {"type": "text",  "content": "At the top, vertical velocity = 0, so use s = ½gt², rearranged for t:"},
            {"type": "latex", "content": r"t = \sqrt{\frac{2 H_{\text{top}}}{g}}"},
            {"type": "latex", "content": rf"t = \sqrt{{\frac{{2 \times {H_top}}}{{9.8}}}} = {t_down}\ \mathrm{{s}}"},
        ]
        part_d = PhysicsQuestion(
            question_text=(
                f"The projectile reaches a maximum height of {H_top} m above the ground. "
                f"Calculate the time it takes to fall from this height to the ground."
            ),
            correct_answer=t_down,
            unit="s",
            topic="Our Dynamic Universe",
            question_type="Projectile Motion",
            level=level,
            distractors=[
                {
                    "value": _r2(math.sqrt(H_top / g)),
                    "mistake": (
                        f"You appear to have left out the factor of 2. "
                        f"t = √(2H ÷ g) = √(2 × {H_top} ÷ 9.8) = {t_down} s."
                    ),
                    "working": working_d,
                },
                {
                    "value": _r2(H_top / g),
                    "mistake": (
                        f"This isn't a constant-velocity relationship — falling from rest needs "
                        f"s = ½gt², rearranged: t = √(2H ÷ g) = {t_down} s."
                    ),
                    "working": working_d,
                },
            ],
            working=working_d,
            notes=_NOTES_PROJECTILE,
        )
    else:
        # Given an intermediate distance fallen from the top, find the time this takes.
        s2 = round(random.uniform(0.25, 0.85) * H_top, 2)
        t2 = _r2(math.sqrt(2 * s2 / g))
        working_d = [
            {"type": "text",  "content": "At the top, vertical velocity = 0, so use s = ½gt², rearranged for t:"},
            {"type": "latex", "content": r"t = \sqrt{\frac{2s}{g}}"},
            {"type": "latex", "content": rf"t = \sqrt{{\frac{{2 \times {s2}}}{{9.8}}}} = {t2}\ \mathrm{{s}}"},
        ]
        part_d = PhysicsQuestion(
            question_text=(
                f"The projectile falls a distance of {s2} m from its maximum height. "
                f"Calculate the time this takes."
            ),
            correct_answer=t2,
            unit="s",
            topic="Our Dynamic Universe",
            question_type="Projectile Motion",
            level=level,
            distractors=[
                {
                    "value": _r2(math.sqrt(s2 / g)),
                    "mistake": (
                        f"You appear to have left out the factor of 2. "
                        f"t = √(2s ÷ g) = √(2 × {s2} ÷ 9.8) = {t2} s."
                    ),
                    "working": working_d,
                },
                {
                    "value": _r2(s2 / g),
                    "mistake": (
                        f"This isn't a constant-velocity relationship — falling from rest needs "
                        f"s = ½gt², rearranged: t = √(2s ÷ g) = {t2} s."
                    ),
                    "working": working_d,
                },
            ],
            working=working_d,
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
