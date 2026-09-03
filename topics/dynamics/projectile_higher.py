import random
import math
from core.models.question_model import PhysicsQuestion

g = 9.8  # m/s²

_NOTES_L1 = """
## Projectile Motion — Angled Launch (Level 1)

**Definitions:**
- Velocity is the speed of an object in a given direction (displacement per unit of time).
- Acceleration is the change in velocity per second.

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

**Worked Example:** An object is launched at 20 m/s at 30° above the horizontal on flat ground. Calculate the range.
$$v_H = 20\\cos30° = 17.3\\ \\mathrm{m/s} \\qquad v_V = 20\\sin30° = 10\\ \\mathrm{m/s}$$
$$t_{\\text{up}} = \\frac{v_V}{g} = \\frac{10}{9.8} = 1.02\\ \\mathrm{s} \\quad\\Rightarrow\\quad t_{\\text{total}} = 2.04\\ \\mathrm{s}$$
$$R = v_H \\times t_{\\text{total}} = 17.3 \\times 2.04 = 35.3\\ \\mathrm{m}$$

> ⚠️ **Most common mistake:** using $t_{\\text{up}}$ (time to reach the top) instead of $t_{\\text{total}} = 2t_{\\text{up}}$ when calculating the range.
"""

_NOTES_L2 = """
## Projectile Motion — Horizontal Launch from Height (Level 2)

**Definitions:**
- Velocity is the speed of an object in a given direction (displacement per unit of time).
- Acceleration is the change in velocity per second.

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

**Worked Example:** An object is launched horizontally at 15 m/s from a height of 20 m. Calculate the resultant speed at impact.
$$t = \\sqrt{\\frac{2h}{g}} = \\sqrt{\\frac{2 \\times 20}{9.8}} = 2.02\\ \\mathrm{s}$$
$$v_y = gt = 9.8 \\times 2.02 = 19.8\\ \\mathrm{m/s}$$
$$v = \\sqrt{v_H^2 + v_y^2} = \\sqrt{15^2 + 19.8^2} = 24.8\\ \\mathrm{m/s}$$

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
        scaffold=[
            {"prompt": "What is 2h/g (t²)?", "answer": two_h_over_g},
            {"prompt": "What is the time of flight t?", "answer": t},
        ],
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
        scaffold=[
            {"prompt": "What is v_H² + v_y²?", "answer": vH2pvy2},
            {"prompt": "What is the resultant speed v?", "answer": v_result},
        ],
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


# ── Time & Height to Maximum Height ──────────────────────────────────────────

_NOTES_MAXH = """
## Projectile Motion — Time and Height to Maximum Height

**Definitions:**
- At the top of its flight, a projectile's vertical velocity is momentarily zero — it has
  stopped rising but not yet started falling.

An object launched at speed **v** at angle **θ** above the horizontal.

**Vertical component of the launch velocity:**
$$v_V = v \\sin\\theta$$

**Time to reach maximum height** (vertical velocity decreases to zero under gravity):
$$v = u + at \;\\Rightarrow\; 0 = v_V - g\\,t_{\\text{up}} \;\\Rightarrow\; t_{\\text{up}} = \\frac{v_V}{g}$$

**Maximum height reached** above the launch point:
$$h_{\\text{max}} = \\frac{v_V^2}{2g}$$

| Symbol | Quantity | Unit |
|---|---|---|
| v | Initial speed | m/s |
| θ | Launch angle | ° |
| v_V | Vertical component of launch velocity | m/s |
| t_up | Time to reach maximum height | s |
| h_max | Maximum height above the launch point | m |

**Worked Example:** An object is launched at 20 m/s at 30° above the horizontal. Calculate the time and height at which it reaches its maximum height.
$$v_V = 20\\sin30° = 10\\ \\mathrm{m/s}$$
$$t_{\\text{up}} = \\frac{v_V}{g} = \\frac{10}{9.8} = 1.02\\ \\mathrm{s}$$
$$h_{\\text{max}} = \\frac{v_V^2}{2g} = \\frac{10^2}{19.6} = 5.1\\ \\mathrm{m}$$

> ⚠️ **Most common mistake:** using the full initial speed v instead of its vertical
> component v_V, or forgetting the factor of 2 in the denominator of h_max = v_V² ÷ 2g.
"""


def generate_projectile_max_height(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)

    v_H  = _r2(v * math.cos(theta))
    v_V  = _r2(v * math.sin(theta))
    t_up = _r2(v_V / g)
    h_max = _r2(v_V ** 2 / (2 * g))

    # distractors
    t_full_v   = _r2(v / g)              # used full speed instead of v_V
    t_vH       = _r2(v_H / g)            # used horizontal component by mistake
    h_no_half  = _r2(v_V ** 2 / g)       # forgot the factor of 2
    h_full_v   = _r2(v ** 2 / (2 * g))   # used full speed instead of v_V

    context = random.choice(_CONTEXTS_L1).format(v=v, theta=theta_deg)

    working_t = [
        {"type": "text",  "content": "First find the vertical component of the launch velocity:"},
        {"type": "latex", "content": rf"v_V = v\sin\theta = {v} \times \sin {theta_deg}° = {v_V}\ \mathrm{{m/s}}"},
        {"type": "text",  "content": "At maximum height, vertical velocity = 0:"},
        {"type": "latex", "content": r"v = u + at \;\Rightarrow\; 0 = v_V - g\,t_{\text{up}}"},
        {"type": "latex", "content": rf"t_{{\text{{up}}}} = \frac{{v_V}}{{g}} = \frac{{{v_V}}}{{9.8}} = {t_up}\ \mathrm{{s}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the time taken to reach maximum height.",
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
                "value": t_vH,
                "mistake": (
                    f"That uses the horizontal component. Only the **vertical** component "
                    f"decreases to zero at maximum height: t_up = v_V ÷ g = {v_V} ÷ 9.8 = {t_up} s."
                ),
                "working": working_t,
            },
        ],
        working=working_t,
        notes=_NOTES_MAXH,
        scaffold=[
            {"prompt": "What is v_V (the vertical component of the launch velocity)?", "answer": v_V},
            {"prompt": "What is the time to reach maximum height, t_up?", "answer": t_up},
        ],
    )

    working_h = [
        {"type": "text",  "content": "Using the vertical component of the launch velocity:"},
        {"type": "latex", "content": r"h_{\text{max}} = \frac{v_V^2}{2g}"},
        {"type": "latex", "content": rf"h_{{\text{{max}}}} = \frac{{{v_V}^2}}{{2 \times 9.8}}"},
        {"type": "latex", "content": rf"h_{{\text{{max}}}} = {h_max}\ \mathrm{{m}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the maximum height reached above the launch point.",
        correct_answer=h_max,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": h_no_half,
                "mistake": (
                    f"You appear to have left out the factor of 2 in the denominator. "
                    f"h_max = v_V² ÷ (2g) = {v_V}² ÷ 19.6 = {h_max} m."
                ),
                "working": working_h,
            },
            {
                "value": h_full_v,
                "mistake": (
                    f"Use the **vertical component** v_V = {v_V} m/s, not the full launch speed. "
                    f"h_max = v_V² ÷ (2g) = {h_max} m."
                ),
                "working": working_h,
            },
        ],
        working=working_h,
        notes=_NOTES_MAXH,
        scaffold=[
            {"prompt": "What is v_V² ?", "answer": round(v_V ** 2, 2)},
            {"prompt": "What is the maximum height h_max?", "answer": h_max},
        ],
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
        parts=[part_a, part_b],
    )


# ── Exam Style — Explain ─────────────────────────────────────────────────────

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


def generate_projectile_exam_style(level="Higher"):
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
        parts=[part],
    )
