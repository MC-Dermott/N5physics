import random
import math
from core.models.question_model import PhysicsQuestion

g = 9.8  # m/s²

_NOTES_L1 = """
## Projectile Motion — Angled Launch (Level 1)

An object launched at speed **v** at angle **θ** above the horizontal on flat ground.

**Step 1 — Resolve into components:**
$$v_H = v \\cos\\theta \\qquad v_V = v \\sin\\theta$$

**Step 2 — Vertical motion** (decelerates at g = 9.8 m/s²):

At maximum height, vertical velocity = 0. Using $v = u + at$ with final $v = 0$:
$$t_{\\text{up}} = \\frac{v_V}{g}$$

Since launch and landing heights are equal, descent = ascent:
$$t_{\\text{total}} = 2 \\times t_{\\text{up}}$$

Maximum height:
$$h_{\\text{max}} = \\frac{v_V^2}{2g}$$

**Step 3 — Horizontal motion** (constant velocity, no air resistance):
$$R = v_H \\times t_{\\text{total}}$$

| Symbol | Quantity | Unit |
|---|---|---|
| v | Initial speed | m/s |
| θ | Launch angle | ° |
| v_H | Horizontal component | m/s |
| v_V | Vertical component | m/s |
| t_total | Total time of flight | s |
| R | Horizontal range | m |

> ⚠️ **Most common mistake:** using $t_{\\text{up}}$ (time to reach the top) instead of $t_{\\text{total}} = 2t_{\\text{up}}$ when calculating the range.
"""

_NOTES_L2 = """
## Projectile Motion — Horizontal Launch from Height (Level 2)

An object launched **horizontally** at speed $v_H$ from height $h$.

**Vertical motion** (starts from rest, $u_V = 0$, accelerates at $g = 9.8$ m/s²):
$$h = \\frac{1}{2}g t^2 \\quad\\Rightarrow\\quad t = \\sqrt{\\frac{2h}{g}}$$

Vertical velocity at impact:
$$v_y = g t$$

**Horizontal motion** (constant — no horizontal force):
$$R = v_H \\times t$$

**Resultant speed at impact** (horizontal ⊥ vertical, so use Pythagoras):
$$v = \\sqrt{v_H^2 + v_y^2}$$

| Symbol | Quantity | Unit |
|---|---|---|
| h | Launch height | m |
| v_H | Horizontal velocity (constant) | m/s |
| t | Time of flight | s |
| v_y | Vertical velocity at impact | m/s |
| v | Resultant speed at impact | m/s |

> ⚠️ **Common mistake 1:** using $h = gt^2$ (forgetting the $\\frac{1}{2}$) gives $t = \\sqrt{h/g}$, which is too small by a factor of $\\sqrt{2}$.
>
> ⚠️ **Common mistake 2:** adding $v_H + v_y$ instead of using Pythagoras for resultant speed.
"""

# 45° excluded — at 45° sin θ = cos θ so the sin/cos swap distractors would equal the correct answer
_ANGLES = [25, 30, 35, 40, 50, 55, 60, 65]
_SPEEDS = [10, 12, 15, 18, 20, 22, 25, 28, 30]

# Heights that avoid h ≈ 2g = 19.6 m, where t = h/g coincidentally equals √(2h/g)
_HEIGHTS  = [5, 10, 15, 25, 30, 40, 45, 50, 60, 80]
_H_SPEEDS = [5, 8, 10, 12, 15, 18, 20, 25]

_CONTEXTS_L1 = [
    "A ball is kicked from flat ground at **{v} m/s** at **{theta}°** above the horizontal.",
    "A golf ball is struck at **{v} m/s** at an angle of **{theta}°** to the horizontal on a flat course.",
    "A stone is thrown from flat ground at **{v} m/s** at **{theta}°** to the horizontal, landing at the same level.",
    "A ball is projected at **{v} m/s** at **{theta}°** above the horizontal and lands on the same flat surface.",
    "A javelin is thrown at **{v} m/s** at an angle of **{theta}°** to the horizontal, landing on flat ground.",
]

_CONTEXTS_L2 = [
    "A ball rolls off the edge of a table **{h} m** above the floor with a horizontal velocity of **{v_H} m/s**.",
    "A ball is kicked horizontally from the top of a cliff **{h} m** above the sea at **{v_H} m/s**.",
    "An object leaves the edge of a platform **{h} m** above the ground with a horizontal velocity of **{v_H} m/s**.",
    "A ball slides off a bench **{h} m** above the ground and leaves horizontally at **{v_H} m/s**.",
]


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
        notes=_NOTES_L1,
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
        notes=_NOTES_L1,
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
        notes=_NOTES_L1,
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
        notes=_NOTES_L1,
    )

    return PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part_a, part_b, part_c, part_d],
    )


# ── Level 2 — Horizontal launch from height (asymmetric) ─────────────────────

def generate_projectile_l2(level="Higher"):
    h   = random.choice(_HEIGHTS)
    v_H = random.choice(_H_SPEEDS)

    t        = _r3(math.sqrt(2 * h / g))
    R        = _r2(v_H * t)
    v_y      = _r2(g * t)
    v_result = _r2(math.sqrt(v_H ** 2 + v_y ** 2))

    # ── Distractors ──────────────────────────────────────────────────────────
    t_no_half = _r3(math.sqrt(h / g))   # forgot ½: used h = gt²
    t_linear  = _r3(h / g)              # used h = gt (wrong equation entirely)

    context = random.choice(_CONTEXTS_L2).format(h=h, v_H=v_H)

    # ── Part (a): time of flight ──────────────────────────────────────────────
    two_h_over_g = _r3(2 * h / g)
    working_t = [
        {"type": "text",  "content": "Vertical motion starts from rest (initial vertical velocity = 0):"},
        {"type": "latex", "content": r"s = \frac{1}{2}g t^2"},
        {"type": "latex", "content": rf"{h} = \frac{{1}}{{2}} \times 9.8 \times t^2"},
        {"type": "latex", "content": rf"t^2 = \frac{{2 \times {h}}}{{9.8}} = {two_h_over_g}\ \mathrm{{s^2}}"},
        {"type": "latex", "content": rf"t = \sqrt{{{two_h_over_g}}} = {t}\ \mathrm{{s}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the time taken for the projectile to reach the ground.",
        correct_answer=t,
        unit="s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": t_no_half,
                "mistake": (
                    f"You appear to have used h = gt² without the ½. "
                    f"The correct equation is **h = ½gt²**, so "
                    f"t = √(2h/g) = √(2×{h}/9.8) = {t} s."
                ),
                "working": working_t,
            },
            {
                "value": t_linear,
                "mistake": (
                    f"Use **h = ½gt²**, not h = gt. "
                    f"Rearranging: t = √(2h/g) = √(2×{h}/9.8) = {t} s."
                ),
                "working": working_t,
            },
        ],
        working=working_t,
        notes=_NOTES_L2,
    )

    # ── Part (b): horizontal range ────────────────────────────────────────────
    working_R = [
        {"type": "text",  "content": "Horizontal velocity is constant (no horizontal force acts on the projectile):"},
        {"type": "latex", "content": r"R = v_H \times t"},
        {"type": "latex", "content": rf"R = {v_H} \times {t}"},
        {"type": "latex", "content": rf"R = {R}\ \mathrm{{m}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the horizontal distance travelled.",
        correct_answer=R,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(v_H * t_no_half),
                "mistake": (
                    f"You appear to have used t = {t_no_half} s (from h = gt²). "
                    f"Correct time is t = √(2h/g) = {t} s, giving R = {v_H} × {t} = {R} m."
                ),
                "working": working_R,
            },
            {
                "value": _r2(v_H * t_linear),
                "mistake": (
                    f"Check the time calculation — use h = ½gt²: "
                    f"t = √(2×{h}/9.8) = {t} s. Then R = {v_H} × {t} = {R} m."
                ),
                "working": working_R,
            },
        ],
        working=working_R,
        notes=_NOTES_L2,
    )

    # ── Part (c): vertical velocity at impact ─────────────────────────────────
    working_vy = [
        {"type": "text",  "content": "Vertical velocity starts at zero and increases under gravity:"},
        {"type": "latex", "content": r"v_y = u_y + gt"},
        {"type": "latex", "content": rf"v_y = 0 + 9.8 \times {t}"},
        {"type": "latex", "content": rf"v_y = {v_y}\ \mathrm{{m/s}}"},
    ]
    vy_wrong_t = _r2(g * t_no_half)    # used wrong time from the ½ mistake

    part_c = PhysicsQuestion(
        question_text="Calculate the vertical velocity of the projectile just before it hits the ground.",
        correct_answer=v_y,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": float(v_H),
                "mistake": (
                    f"This is the horizontal velocity. Horizontal and vertical motions are independent. "
                    f"v_y = g × t = 9.8 × {t} = {v_y} m/s."
                ),
                "working": working_vy,
            },
            {
                "value": vy_wrong_t,
                "mistake": (
                    f"You appear to have used t = {t_no_half} s (from h = gt² without the ½). "
                    f"Correct time is t = √(2h/g) = {t} s, giving v_y = 9.8 × {t} = {v_y} m/s."
                ),
                "working": working_vy,
            },
        ],
        working=working_vy,
        notes=_NOTES_L2,
    )

    # ── Part (d): resultant speed at impact ───────────────────────────────────
    vH2pvy2 = _r2(v_H ** 2 + v_y ** 2)
    working_v = [
        {"type": "text",  "content": "At impact, the projectile has both horizontal and vertical velocity components (perpendicular). Use Pythagoras:"},
        {"type": "latex", "content": r"v = \sqrt{v_H^2 + v_y^2}"},
        {"type": "latex", "content": rf"v = \sqrt{{{v_H}^2 + {v_y}^2}}"},
        {"type": "latex", "content": rf"v = \sqrt{{{vH2pvy2}}}"},
        {"type": "latex", "content": rf"v = {v_result}\ \mathrm{{m/s}}"},
    ]
    part_d = PhysicsQuestion(
        question_text="Calculate the resultant speed of the projectile just before it hits the ground.",
        correct_answer=v_result,
        unit="m/s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(v_H + v_y),
                "mistake": (
                    f"You cannot add perpendicular velocities directly. "
                    f"Use Pythagoras: v = √(v_H² + v_y²) = √({v_H}² + {v_y}²) = {v_result} m/s."
                ),
                "working": working_v,
            },
            {
                "value": v_y,
                "mistake": (
                    f"This is only the vertical component. At impact the projectile still has "
                    f"horizontal velocity {v_H} m/s. "
                    f"v = √({v_H}² + {v_y}²) = {v_result} m/s."
                ),
                "working": working_v,
            },
        ],
        working=working_v,
        notes=_NOTES_L2,
    )

    return PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part_a, part_b, part_c, part_d],
    )
