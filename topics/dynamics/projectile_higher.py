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

$$v_H = v\\cos\\theta$$
$$v_V = v\\sin\\theta$$

#### Equations of motion

Vertical:
$$v = u + at$$
$$s = ut + \\tfrac{1}{2}at^2$$

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

# (context, min speed, max speed) — a human throw is only used when the chosen
# speed is realistic for it (no 30 m/s shot puts).
_CONTEXTS_L2_HUMAN = [
    ("A shot putter releases the shot at **{v} m/s** at **{theta}°** above the horizontal, from a height of **{h} m**.", 10, 14),
    ("A javelin thrower releases the javelin at **{v} m/s** at **{theta}°** above the horizontal, from a height of **{h} m**.", 18, 30),
    ("A basketball player shoots at **{v} m/s** at **{theta}°** above the horizontal, releasing the ball from a height of **{h} m**.", 7, 10),
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


# ── Shared: resolving the launch velocity into components (parts a, b) ───────

def _l2_elevated_context(v, theta_deg):
    """A launch from a height above the ground (never flat ground)."""
    human = [c for c, lo, hi in _CONTEXTS_L2_HUMAN if lo <= v <= hi]
    if human and random.random() < 0.5:
        h = random.choice(_L2_HUMAN_HEIGHTS)
        context = random.choice(human)
    else:
        h = random.choice(_L2_ELEVATED_HEIGHTS)
        context = random.choice(_CONTEXTS_L2_ELEVATED)
    return h, context.format(v=v, theta=theta_deg, h=h)


def _l2_parts_ab(v, theta_deg, theta, v_H, v_V, level):
    vH_sin = _r2(v * math.sin(theta))  # sin/cos swapped
    vV_cos = _r2(v * math.cos(theta))  # sin/cos swapped

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

    return part_a, part_b


def _l2_part_time_to_peak(v, v_H, v_V, t_up, theta_deg, level):
    t_full_v = _r2(v / g)  # used full speed instead of v_V
    working_tup = [
        {"type": "text",  "content": f"Vertically, up to the highest point: u = {v_V} m/s, v = 0, a = −9.8 m/s²."},
        {"type": "latex", "content": r"v = u + at"},
        {"type": "latex", "content": rf"0 = {v_V} + (-9.8) \times t_{{\text{{up}}}}"},
        {"type": "latex", "content": rf"t_{{\text{{up}}}} = \frac{{{v_V}}}{{9.8}} = {t_up}\ \mathrm{{s}}"},
    ]
    return PhysicsQuestion(
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


# ══ Skill drills — worksheet Sections 1–6 ═══════════════════════════════════
# One generator per step of the worksheet's progression (fired straight up →
# simple horizontal motion → components → time to / from the highest point →
# vertical displacement → horizontal motion of an angled launch). The
# exam-style patterns A–F further down are Section 7. Upwards is positive
# throughout, so a = −9.8 m/s² vertically.

_TOPIC = "Our Dynamic Universe"


def _scenario(context, parts, level):
    return _with_projectile_widget(PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic=_TOPIC,
        question_type="Projectile Motion",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=parts,
    ))


def _distinct(answer, distractors):
    """Drop any distractor within 3% of the answer or of an earlier distractor —
    at some launch angles two different mistakes land on (nearly) the same value."""
    kept, seen = [], [answer]
    for d in distractors:
        if all(abs(d["value"] - x) > 0.03 * max(abs(x), 1e-9) for x in seen):
            kept.append(d)
            seen.append(d["value"])
    return kept


def _part(text, answer, unit, working, distractors, level, scaffold=None):
    distractors = _distinct(answer, distractors)
    return PhysicsQuestion(
        question_text=text,
        correct_answer=answer,
        unit=unit,
        topic=_TOPIC,
        question_type="Projectile Motion",
        level=level,
        distractors=[dict(d, working=working) for d in distractors],
        working=working,
        notes=_NOTES_PROJECTILE,
        scaffold=scaffold or [],
    )


def _parts_ab(v, theta_deg, theta, v_H, v_V, level):
    """_l2_parts_ab with near-duplicate distractors removed (at small angles
    v_H ≈ v, so the 'used the full speed' option would match the answer)."""
    parts = _l2_parts_ab(v, theta_deg, theta, v_H, v_V, level)
    for p in parts:
        p.distractors = _distinct(p.correct_answer, p.distractors)
    return parts


def _launch(flat):
    """Tied launch: speed, angle, context text and launch height above the
    ground/sea (0 for flat ground)."""
    theta_deg = random.choice(_ANGLES)
    v = random.choice(_SPEEDS)
    if flat:
        return v, theta_deg, 0, random.choice(_CONTEXTS_L1).format(v=v, theta=theta_deg)
    h, context = _l2_elevated_context(v, theta_deg)
    return v, theta_deg, h, context


def _components(v, theta_deg):
    theta = math.radians(theta_deg)
    return theta, _r2(v * math.cos(theta)), _r2(v * math.sin(theta))


def _t_fall_part(drop, text, level, alt_drop=None):
    """Fall from the highest point (vertical u = 0) through a vertical distance `drop`."""
    t = _r2(math.sqrt(2 * drop / g))
    working = [
        {"type": "text",  "content": f"From the highest point the vertical velocity is zero: u = 0, s = −{drop} m, a = −9.8 m/s²."},
        {"type": "latex", "content": r"s = ut + \tfrac{1}{2}at^2"},
        {"type": "latex", "content": rf"-{drop} = (0 \times t) + \tfrac{{1}}{{2}} \times (-9.8) \times t^2"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    return _part(text, t, "s", working, [
        {"value": _r2(math.sqrt(drop / g)),
         "mistake": f"You appear to have left out the ½. −{drop} = ½ × (−9.8) × t² gives t = {t} s."},
        {"value": _r2(2 * drop / g),
         "mistake": f"You haven't square-rooted: t² = 2 × {drop} ÷ 9.8, so t = {t} s."},
    ] + ([{"value": _r2(math.sqrt(2 * alt_drop / g)),
           "mistake": f"The projectile only falls {drop} m from its highest point to this level, so s = −{drop} m: t = {t} s."}]
         if alt_drop else []), level), t


# Section 1 — fired straight upwards (no horizontal motion)
_CONTEXTS_VERTICAL_SAME = [
    # (text, min speed, max speed)
    ("A ball is thrown straight upwards at **{v} m/s** and caught at the same height it was thrown from.", 5, 15),
    ("A tennis ball is hit straight upwards at **{v} m/s** and falls back to the height it was hit from.", 8, 18),
    ("A distress flare is fired straight upwards at **{v} m/s** from the deck of a lifeboat and falls back to deck level.", 30, 50),
]


def generate_projectile_s1_vertical_same_height(level="Higher"):
    text, lo, hi = random.choice(_CONTEXTS_VERTICAL_SAME)
    u = random.randint(lo, hi)
    t_up = _r2(u / g)
    t_total = _r2(2 * t_up)
    working_a = [
        {"type": "text",  "content": f"Launched vertically, so u = {u} m/s. At the highest point v = 0; a = −9.8 m/s²."},
        {"type": "latex", "content": r"v = u + at"},
        {"type": "latex", "content": rf"0 = {u} + (-9.8) \times t"},
        {"type": "latex", "content": rf"t = {t_up}\ \mathrm{{s}}"},
    ]
    part_a = _part("Calculate the time taken to reach the highest point.", t_up, "s", working_a, [
        {"value": _r2(u * g), "mistake": f"Rearrange 0 = {u} − 9.8t for t: t = {u} ÷ 9.8 = {t_up} s."},
        {"value": t_total, "mistake": f"That is the time up and back down. The time to the highest point is {u} ÷ 9.8 = {t_up} s."},
    ], level)
    working_b = [
        {"type": "text",  "content": "It returns to the height it was launched from, so the fall takes as long as the rise:"},
        {"type": "latex", "content": rf"t_{{\text{{total}}}} = 2 \times {t_up} = {t_total}\ \mathrm{{s}}"},
    ]
    part_b = _part("Calculate the total time of flight.", t_total, "s", working_b, [
        {"value": t_up, "mistake": f"That is only the rise. The fall takes as long again: 2 × {t_up} = {t_total} s."},
        {"value": _r2(4 * t_up), "mistake": f"Double the time to the highest point once: 2 × {t_up} = {t_total} s."},
    ], level, scaffold=[
        {"prompt": "What is the time to reach the highest point?", "answer": t_up},
        {"prompt": "What is the total time of flight?", "answer": t_total},
    ])
    return _scenario(text.format(v=u), [part_a, part_b], level)


_CONTEXTS_VERTICAL_DIFF = [
    # (text, speeds, launch-height choices above the landing level)
    ("A stone is thrown straight upwards at **{v} m/s** from the edge of a sea cliff **{h} m** high, and falls past "
     "the edge into the sea.", range(5, 16), [15, 20, 25, 30, 40]),
    ("A pupil throws a ball straight upwards at **{v} m/s**, releasing it **{h} m** above the ground, and lets it "
     "land on the ground.", range(4, 11), [1.4, 1.5, 1.6, 1.7, 1.8]),
    ("A distress flare is fired straight upwards at **{v} m/s** from a cliff top **{h} m** above the sea, and falls "
     "past the cliff into the sea.", range(30, 51, 5), [20, 30, 40, 50]),
]


def generate_projectile_s1_vertical_from_highest_point(level="Higher"):
    text, speeds, heights = random.choice(_CONTEXTS_VERTICAL_DIFF)
    u, h = random.choice(list(speeds)), random.choice(heights)
    t_up = _r2(u / g)
    H_top = _r2(h + u ** 2 / (2 * g))
    context = text.format(v=u, h=f"{h:g}")
    where = "the sea" if "sea" in text else "the ground"
    working_a = [
        {"type": "text",  "content": f"Launched vertically, so u = {u} m/s. At the highest point v = 0; a = −9.8 m/s²."},
        {"type": "latex", "content": r"v = u + at"},
        {"type": "latex", "content": rf"0 = {u} + (-9.8) \times t"},
        {"type": "latex", "content": rf"t = {t_up}\ \mathrm{{s}}"},
    ]
    part_a = _part("Calculate the time taken to reach the highest point.", t_up, "s", working_a, [
        {"value": _r2(u * g), "mistake": f"Rearrange 0 = {u} − 9.8t for t: t = {u} ÷ 9.8 = {t_up} s."},
        {"value": _r2(2 * t_up), "mistake": f"That doubles the time. To the highest point only: t = {u} ÷ 9.8 = {t_up} s."},
    ], level)
    part_b, t_down = _t_fall_part(
        H_top,
        f"The highest point is {H_top} m above {where}. Calculate the time taken to fall from the highest point to {where}.",
        level, alt_drop=_r2(H_top - h))
    t_total = _r2(t_up + t_down)
    working_c = [
        {"type": "latex", "content": rf"t = t_{{\text{{up}}}} + t_{{\text{{down}}}} = {t_up} + {t_down} = {t_total}\ \mathrm{{s}}"},
    ]
    part_c = _part("Calculate the total time of flight.", t_total, "s", working_c, [
        {"value": _r2(2 * t_up), "mistake": f"It lands below its launch point, so the fall takes longer than the rise: {t_up} + {t_down} = {t_total} s."},
        {"value": t_down, "mistake": f"That is only the fall. Add the rise: {t_up} + {t_down} = {t_total} s."},
    ], level, scaffold=[
        {"prompt": "What is the time to reach the highest point?", "answer": t_up},
        {"prompt": "What is the time to fall from the highest point?", "answer": t_down},
        {"prompt": "What is the total time of flight?", "answer": t_total},
    ])
    return _scenario(context, [part_a, part_b, part_c], level)


def generate_projectile_s1_vertical_height_at_time(level="Higher"):
    """Straight-up launch, given a time measured from launch or from the highest
    point: s = ut + ½at², then add to that point's height above the ground/sea."""
    text, speeds, heights = random.choice(_CONTEXTS_VERTICAL_DIFF)
    u, h = random.choice(list(speeds)), random.choice(heights)
    context = text.format(v=u, h=f"{h:g}")
    where = "the sea" if "sea" in text else "the ground"
    t_up = u / g
    H_top = _r2(h + u ** 2 / (2 * g))
    t_land = t_up + math.sqrt(2 * H_top / g)
    if random.random() < 0.5:
        t = round(random.uniform(0.2, 0.85) * t_land, 2)
        s = _r2(u * t - 0.5 * g * t ** 2)
        working_a = [
            {"type": "text",  "content": f"Vertically, from launch: u = {u} m/s, t = {t} s, a = −9.8 m/s²."},
            {"type": "latex", "content": r"s = ut + \tfrac{1}{2}at^2"},
            {"type": "latex", "content": rf"s = ({u} \times {t}) + \tfrac{{1}}{{2}} \times (-9.8) \times {t}^2"},
            {"type": "latex", "content": rf"s = {s}\ \mathrm{{m}}"},
        ]
        part_a = _part(f"Calculate the displacement from the launch point {t} s after launch "
                       f"(a negative answer means below the launch point).", s, "m", working_a, [
            {"value": _r2(u * t + 0.5 * g * t ** 2), "mistake": f"Sign error — upwards is positive, so a = −9.8 m/s²: s = {s} m."},
            {"value": _r2(u * t - g * t ** 2), "mistake": f"You appear to have left out the ½: s = {s} m."},
            {"value": _r2(u * t), "mistake": f"You have left out gravity: s = ut + ½at² = {s} m."},
        ], level)
        base, base_text = h, f"{h:g}"
    else:
        t = round(random.uniform(0.3, 0.9) * math.sqrt(2 * H_top / g), 2)
        s = _r2(-0.5 * g * t ** 2)
        context += f" Its highest point is **{H_top} m** above {where}."
        working_a = [
            {"type": "text",  "content": f"From the highest point: u = 0, t = {t} s, a = −9.8 m/s²."},
            {"type": "latex", "content": r"s = ut + \tfrac{1}{2}at^2"},
            {"type": "latex", "content": rf"s = (0 \times {t}) + \tfrac{{1}}{{2}} \times (-9.8) \times {t}^2"},
            {"type": "latex", "content": rf"s = {s}\ \mathrm{{m}}"},
        ]
        part_a = _part(f"Calculate the displacement from the highest point {t} s after passing it "
                       f"(negative = below the highest point).", s, "m", working_a, [
            {"value": _r2(-s), "mistake": f"Below the highest point, so the displacement is negative: s = {s} m."},
            {"value": _r2(-g * t ** 2), "mistake": f"You appear to have left out the ½: s = ½ × (−9.8) × {t}² = {s} m."},
            {"value": _r2(u * t - 0.5 * g * t ** 2), "mistake": f"At the highest point u = 0, not the launch speed: s = {s} m."},
        ], level)
        base, base_text = H_top, f"{H_top}"
    H = _r2(base + s)
    working_b = [{"type": "latex", "content": rf"h = {base_text} + ({s}) = {H}\ \mathrm{{m}}"}]
    part_b = _part(f"Calculate the height above {where} at this time.", H, "m", working_b, [
        {"value": s, "mistake": f"That is the displacement. Add it to the starting height: {base_text} + ({s}) = {H} m."},
        {"value": _r2(base - s), "mistake": f"Add the displacement with its sign: {base_text} + ({s}) = {H} m."},
    ], level, scaffold=[
        {"prompt": "What is the displacement s?", "answer": s},
        {"prompt": f"What is the height above {where}?", "answer": H},
    ])
    return _scenario(context, [part_a, part_b], level)


# Section 2 — simple horizontal motion (constant horizontal velocity, s = vt)
_CONTEXTS_HORIZONTAL = [
    # (object phrase, what happens, v range, t range)
    ("An ice hockey puck slides across smooth ice", "for", (3.0, 10.0), (1.0, 4.0)),
    ("A marble rolls off a table", "and hits the floor", (1.0, 3.0), (0.35, 0.50)),
    ("A stone is thrown horizontally from a cliff top", "and lands in the sea", (5.0, 15.0), (1.8, 3.2)),
    ("A ball rolls horizontally off a harbour wall", "and lands in the water", (1.5, 4.0), (0.6, 1.1)),
]


def generate_projectile_s2_horizontal_motion(level="Higher"):
    obj, event, (v_lo, v_hi), (t_lo, t_hi) = random.choice(_CONTEXTS_HORIZONTAL)
    v = round(random.uniform(v_lo, v_hi), 1)
    t = round(random.uniform(t_lo, t_hi), 2)
    s = _r2(v * t)
    later = "" if event == "for" else " later"
    find = random.choice(["distance", "time", "velocity"])
    if find == "distance":
        text = f"{obj} at **{v} m/s** {event} **{t} s**{later}. Calculate the horizontal distance travelled."
        answer, unit = s, "m"
        working = [{"type": "latex", "content": r"s = vt"},
                   {"type": "latex", "content": rf"s = {v} \times {t} = {s}\ \mathrm{{m}}"}]
        distractors = [{"value": _r2(v / t), "mistake": f"Multiply, don't divide: s = vt = {v} × {t} = {s} m."},
                       {"value": _r2(v * t / 2), "mistake": f"The horizontal velocity is constant, so no halving: s = {v} × {t} = {s} m."}]
    elif find == "time":
        text = f"{obj} at **{v} m/s** and travels **{s} m** horizontally. Calculate the time taken."
        answer, unit = _r2(s / v), "s"
        working = [{"type": "latex", "content": r"s = vt"},
                   {"type": "latex", "content": rf"{s} = {v} \times t"},
                   {"type": "latex", "content": rf"t = {answer}\ \mathrm{{s}}"}]
        distractors = [{"value": _r2(v / s), "mistake": f"Rearrange s = vt for t: t = s ÷ v = {s} ÷ {v} = {answer} s."},
                       {"value": _r2(s * v), "mistake": f"Rearrange s = vt for t: t = s ÷ v = {answer} s."}]
    else:
        text = f"{obj} and travels **{s} m** horizontally in **{t} s**. Calculate its horizontal velocity."
        answer, unit = _r2(s / t), "m/s"
        working = [{"type": "latex", "content": r"s = vt"},
                   {"type": "latex", "content": rf"{s} = v \times {t}"},
                   {"type": "latex", "content": rf"v = {answer}\ \mathrm{{m/s}}"}]
        distractors = [{"value": _r2(t / s), "mistake": f"Rearrange s = vt for v: v = s ÷ t = {s} ÷ {t} = {answer} m/s."},
                       {"value": _r2(s * t), "mistake": f"Rearrange s = vt for v: v = s ÷ t = {answer} m/s."}]
    working.insert(0, {"type": "text", "content": "No horizontal force acts, so the horizontal velocity is constant."})
    return _with_projectile_widget(_part(text, answer, unit, working, distractors, level))


def generate_projectile_s3_components(level="Higher"):
    v, theta_deg, h, context = _launch(flat=random.random() < 0.5)
    theta, v_H, v_V = _components(v, theta_deg)
    part_a, part_b = _parts_ab(v, theta_deg, theta, v_H, v_V, level)
    return _scenario(context, [part_a, part_b], level)


def generate_projectile_s4_time_same_height(level="Higher"):
    v, theta_deg, _, context = _launch(flat=True)
    theta, v_H, v_V = _components(v, theta_deg)
    t_up = _r2(v_V / g)
    t_total = _r2(2 * t_up)
    _, part_a = _parts_ab(v, theta_deg, theta, v_H, v_V, level)
    part_b = _l2_part_time_to_peak(v, v_H, v_V, t_up, theta_deg, level)
    working = [
        {"type": "text",  "content": "It lands at the height it was launched from, so the fall from the highest point takes as long as the rise:"},
        {"type": "latex", "content": rf"t_{{\text{{total}}}} = 2 \times {t_up} = {t_total}\ \mathrm{{s}}"},
    ]
    part_c = _part("Calculate the total time of flight.", t_total, "s", working, [
        {"value": t_up, "mistake": f"That is only the time to the highest point. The fall back down takes as long again: 2 × {t_up} = {t_total} s."},
        {"value": _r2(2 * v / g), "mistake": f"Use the vertical component ({v_V} m/s), not the launch speed: 2 × {v_V} ÷ 9.8 = {t_total} s."},
    ], level, scaffold=[
        {"prompt": "What is the time to reach the highest point?", "answer": t_up},
        {"prompt": "What is the total time of flight?", "answer": t_total},
    ])
    return _scenario(context, [part_a, part_b, part_c], level)


_HOOP_HEIGHT = 3.05


def generate_projectile_s4_time_from_highest_point(level="Higher"):
    if random.random() < 0.3:
        # Basketball dropping through a hoop above its release point.
        v = random.choice([8, 9, 10])
        theta_deg = random.choice([50, 55, 60])
        h = random.choice([1.9, 2.0, 2.1, 2.2])
        target, level_name = _HOOP_HEIGHT, "the hoop"
        context = (f"A basketball is thrown at **{v} m/s** at **{theta_deg}°** above the horizontal, released "
                   f"**{h} m** above the floor. It drops through the hoop, **{_HOOP_HEIGHT} m** above the floor, on its way down.")
    else:
        v, theta_deg, h, context = _launch(flat=False)
        target, level_name = 0, "the ground"
    theta, v_H, v_V = _components(v, theta_deg)
    t_up = _r2(v_V / g)
    H_top = _r2(h + v_V ** 2 / (2 * g))
    drop = _r2(H_top - target)

    _, part_a = _parts_ab(v, theta_deg, theta, v_H, v_V, level)
    part_b = _l2_part_time_to_peak(v, v_H, v_V, t_up, theta_deg, level)
    where = "the floor" if target else "the ground"
    part_c, t_down = _t_fall_part(
        drop,
        f"The highest point of the flight is {H_top} m above {where}. Calculate the time taken to fall "
        f"from the highest point to {level_name}.",
        level, alt_drop=_r2(H_top - h) if not target else H_top)
    if target:
        part_c.scaffold = [
            {"prompt": "What vertical distance does the ball fall from its highest point to the hoop?", "answer": drop},
            {"prompt": "What is the time taken to fall this distance?", "answer": t_down},
        ]
    t_total = _r2(t_up + t_down)
    working = [
        {"type": "latex", "content": rf"t = t_{{\text{{up}}}} + t_{{\text{{down}}}} = {t_up} + {t_down} = {t_total}\ \mathrm{{s}}"},
    ]
    part_d = _part(f"Calculate the total time from launch to reaching {level_name}.", t_total, "s", working, [
        {"value": _r2(2 * t_up), "mistake": f"The launch and landing heights are different, so the fall does not take as long as the rise. t = {t_up} + {t_down} = {t_total} s."},
        {"value": t_down, "mistake": f"That is only the fall. Add the time to rise: {t_up} + {t_down} = {t_total} s."},
    ], level, scaffold=[
        {"prompt": "What is the time to reach the highest point?", "answer": t_up},
        {"prompt": "What is the time to fall from the highest point?", "answer": t_down},
        {"prompt": "What is the total time?", "answer": t_total},
    ])
    return _scenario(context, [part_a, part_b, part_c, part_d], level)


def generate_projectile_s5_max_height(level="Higher"):
    v, theta_deg, h, context = _launch(flat=random.random() < 0.4)
    theta, v_H, v_V = _components(v, theta_deg)
    s = _r2(v_V ** 2 / (2 * g))
    _, part_a = _parts_ab(v, theta_deg, theta, v_H, v_V, level)
    working = [
        {"type": "text",  "content": f"Vertically, to the highest point: u = {v_V} m/s, v = 0, a = −9.8 m/s²."},
        {"type": "latex", "content": r"v^2 = u^2 + 2as"},
        {"type": "latex", "content": rf"0^2 = {v_V}^2 + 2 \times (-9.8) \times s"},
        {"type": "latex", "content": rf"s = {s}\ \mathrm{{m}}"},
    ]
    part_b = _part("Calculate the maximum height reached above the launch point.", s, "m", working, [
        {"value": _r2(v_V ** 2 / g), "mistake": f"You appear to have left out the 2 in 2as: s = {v_V}² ÷ (2 × 9.8) = {s} m."},
        {"value": _r2(v ** 2 / (2 * g)), "mistake": f"Use the vertical component ({v_V} m/s), not the launch speed: s = {s} m."},
    ], level)
    parts = [part_a, part_b]
    if h:
        H = _r2(h + s)
        working_c = [{"type": "latex", "content": rf"h = {h:g} + {s} = {H}\ \mathrm{{m}}"}]
        parts.append(_part("Calculate the maximum height above the ground (or sea).", H, "m", working_c, [
            {"value": s, "mistake": f"That is the height above the launch point. Add the launch height: {h:g} + {s} = {H} m."},
            {"value": _r2(abs(s - h)), "mistake": f"The launch point is above the ground, so add its height: {h:g} + {s} = {H} m."},
        ], level, scaffold=[
            {"prompt": "What is the maximum height above the launch point?", "answer": s},
            {"prompt": "What is the maximum height above the ground?", "answer": H},
        ]))
    return _scenario(context, parts, level)


def generate_projectile_s5_displacement_from_launch(level="Higher"):
    flat = random.random() < 0.4
    v, theta_deg, h, context = _launch(flat=flat)
    theta, v_H, v_V = _components(v, theta_deg)
    # Time of landing on the ground/sea below (h = 0 gives the flat-ground flight time).
    t_land = (v_V + math.sqrt(v_V ** 2 + 2 * g * h)) / g
    t = round(random.uniform(0.2, 0.9) * t_land, 2)
    s = _r2(v_V * t - 0.5 * g * t ** 2)
    _, part_a = _parts_ab(v, theta_deg, theta, v_H, v_V, level)
    working = [
        {"type": "text",  "content": f"Vertically, from launch: u = {v_V} m/s, t = {t} s, a = −9.8 m/s²."},
        {"type": "latex", "content": r"s = ut + \tfrac{1}{2}at^2"},
        {"type": "latex", "content": rf"s = ({v_V} \times {t}) + \tfrac{{1}}{{2}} \times (-9.8) \times {t}^2"},
        {"type": "latex", "content": rf"s = {s}\ \mathrm{{m}}"},
    ]
    if s < 0:
        working.append({"type": "text", "content": "Negative: the projectile is below its launch point."})
    part_b = _part(f"Calculate the vertical displacement from the launch point {t} s after launch "
                   f"(a negative answer means below the launch point).", s, "m", working, [
        {"value": _r2(v_V * t + 0.5 * g * t ** 2), "mistake": f"Sign error — with upwards positive, a = −9.8 m/s², so the ½at² term is subtracted: s = {s} m."},
        {"value": _r2(v_V * t - g * t ** 2), "mistake": f"You appear to have left out the ½: s = {v_V} × {t} − ½ × 9.8 × {t}² = {s} m."},
        {"value": _r2(v_V * t), "mistake": f"You have left out gravity. s = ut + ½at² = {s} m."},
    ], level)
    parts = [part_a, part_b]
    if h:
        H = _r2(h + s)
        working_c = [{"type": "latex", "content": rf"h = {h:g} + ({s}) = {H}\ \mathrm{{m}}"}]
        parts.append(_part("Calculate the height above the ground (or sea) at this time.", H, "m", working_c, [
            {"value": s, "mistake": f"That is the displacement from the launch point. Add the launch height: {h:g} + ({s}) = {H} m."},
            {"value": _r2(h - s), "mistake": f"Add the displacement (with its sign) to the launch height: {h:g} + ({s}) = {H} m."},
            {"value": _r2(h + v_V * t), "mistake": f"You have left out gravity when finding s. s = ut + ½at² = {s} m, so h = {H} m."},
        ], level, scaffold=[
            {"prompt": "What is the vertical displacement from the launch point?", "answer": s},
            {"prompt": "What is the height above the ground at this time?", "answer": H},
        ]))
    return _scenario(context, parts, level)


_CONTEXTS_FROM_TOP = [
    ("A ball kicked from the top of a sea cliff reaches its highest point **{H} m** above the sea.", "the sea", 8, 60),
    ("A shot reaches its highest point **{H} m** above the ground.", "the ground", 3.5, 6),
    ("A football kicked from the pitch reaches its highest point **{H} m** above the ground.", "the ground", 3, 15),
    ("A basketball reaches its highest point **{H} m** above the floor.", "the floor", 3.5, 6),
]


def generate_projectile_s5_displacement_from_highest_point(level="Higher"):
    text, where, lo, hi = random.choice(_CONTEXTS_FROM_TOP)
    H = round(random.uniform(lo, hi), 1)
    t = round(random.uniform(0.3, 0.85) * math.sqrt(2 * H / g), 2)
    s = _r2(-0.5 * g * t ** 2)
    h = _r2(H + s)
    working = [
        {"type": "text",  "content": f"From the highest point: u = 0, t = {t} s, a = −9.8 m/s²."},
        {"type": "latex", "content": r"s = ut + \tfrac{1}{2}at^2"},
        {"type": "latex", "content": rf"s = (0 \times {t}) + \tfrac{{1}}{{2}} \times (-9.8) \times {t}^2 = {s}\ \mathrm{{m}}"},
        {"type": "latex", "content": rf"h = {H:g} + ({s}) = {h}\ \mathrm{{m}}"},
    ]
    q = _part(
        text.format(H=f"{H:g}") + f" Calculate its height above {where} **{t} s** after it passes its highest point.",
        h, "m", working, [
            {"value": _r2(-s), "mistake": f"That is the distance fallen from the highest point. Its height is {H:g} + ({s}) = {h} m."},
            {"value": _r2(H - g * t ** 2), "mistake": f"You appear to have left out the ½: s = ½ × (−9.8) × {t}² = {s} m, so h = {h} m."},
            {"value": _r2(H - 0.5 * g * t), "mistake": f"Square the time: s = ½ × (−9.8) × {t}² = {s} m, so h = {h} m."},
        ], level, scaffold=[
            {"prompt": "What is the vertical displacement from the highest point (negative = below)?", "answer": s},
            {"prompt": f"What is the height above {where}?", "answer": h},
        ])
    return _with_projectile_widget(q)


def _horizontal_s_part(v, v_H, t, text, level):
    s = _r2(v_H * t)
    working = [
        {"type": "text",  "content": f"Horizontal velocity is constant: v = v_H = {v_H} m/s, t = {t} s."},
        {"type": "latex", "content": r"s = vt"},
        {"type": "latex", "content": rf"s = {v_H} \times {t} = {s}\ \mathrm{{m}}"},
    ]
    return _part(text, s, "m", working, [
        {"value": _r2(v_H * t / 2), "mistake": f"Use the whole time given ({t} s): s = {v_H} × {t} = {s} m."},
        {"value": _r2(0.5 * g * t ** 2), "mistake": f"Horizontally there is no acceleration — use s = vt with v_H: s = {s} m."},
        {"value": _r2(v * t), "mistake": f"Use the horizontal component ({v_H} m/s), not the launch speed: s = {v_H} × {t} = {s} m."},
    ], level)


def generate_projectile_s6_horizontal_distance(level="Higher"):
    v, theta_deg, h, context = _launch(flat=random.random() < 0.6)
    theta, v_H, v_V = _components(v, theta_deg)
    part_a, _ = _parts_ab(v, theta_deg, theta, v_H, v_V, level)
    t_up = _r2(v_V / g)
    if random.random() < 0.3:
        part_b = _horizontal_s_part(
            v, v_H, t_up,
            f"The projectile takes {t_up} s to reach its highest point. Calculate its horizontal "
            f"distance from the launch point at that moment.", level)
    else:
        T = _r2((v_V + math.sqrt(v_V ** 2 + 2 * g * h)) / g)
        part_b = _horizontal_s_part(
            v, v_H, T,
            f"The total time of flight is {T} s. Calculate the horizontal distance travelled before landing.",
            level)
    return _scenario(context, [part_a, part_b], level)


_CONTEXTS_TO_TARGET = [
    # (text, speeds, angles, fraction of range at which the target sits)
    ("A player kicks a ball from the ground at **{v} m/s** at **{theta}°** above the horizontal, "
     "towards a crossbar **{x} m** away.", [15, 18, 20, 22, 25], [25, 30, 35, 40], (0.4, 0.85)),
    ("An archer fires an arrow at **{v} m/s** at **{theta}°** above the horizontal towards a target "
     "**{x} m** away.", [40, 45, 50, 55, 60], [3, 4, 5, 6, 8], (0.4, 0.9)),
    ("A golfer chips a ball at **{v} m/s** at **{theta}°** above the horizontal towards a flag "
     "**{x} m** away.", [10, 12, 14, 16], [40, 50, 55, 60], (0.5, 0.95)),
]


def generate_projectile_s6_time_to_distance(level="Higher"):
    text, speeds, angles, (f_lo, f_hi) = random.choice(_CONTEXTS_TO_TARGET)
    v, theta_deg = random.choice(speeds), random.choice(angles)
    theta, v_H, v_V = _components(v, theta_deg)
    R = v_H * 2 * v_V / g
    x = round(random.uniform(f_lo, f_hi) * R, 1)
    x = int(x) if x >= 10 else x
    context = text.format(v=v, theta=theta_deg, x=x)
    part_a, _ = _parts_ab(v, theta_deg, theta, v_H, v_V, level)
    t = _r3(x / v_H)
    working = [
        {"type": "text",  "content": f"Horizontal velocity is constant: s = {x} m, v = v_H = {v_H} m/s."},
        {"type": "latex", "content": r"s = vt"},
        {"type": "latex", "content": rf"{x} = {v_H} \times t"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    part_b = _part(f"Calculate the time taken to travel the {x} m horizontally.", t, "s", working, [
        {"value": _r3(x / v), "mistake": f"Use the horizontal component ({v_H} m/s), not the launch speed: t = {x} ÷ {v_H} = {t} s."},
        {"value": _r3(x / v_V), "mistake": f"Horizontal distance is covered at the horizontal velocity: t = {x} ÷ {v_H} = {t} s."},
        {"value": _r3(x / v_H / 2), "mistake": f"No halving is needed — s = vt applies to the whole {x} m: t = {x} ÷ {v_H} = {t} s."},
    ], level)
    return _scenario(context, [part_a, part_b], level)


_CONTEXTS_HORIZ_V = [
    # (text, s range, T range)
    ("A long jumper is in the air for **{T} s** and lands **{s} m** from the take-off board, at the same height as take-off.",
     (5.5, 8.0), (0.6, 0.9)),
    ("A football kicked from flat ground lands **{s} m** away, on the same flat ground, **{T} s** after it was kicked.",
     (15, 40), (1.5, 3.0)),
    ("A golf ball chipped from a flat green lands **{s} m** away, on the same level, **{T} s** after it was struck.",
     (10, 30), (1.5, 3.0)),
]


def generate_projectile_s6_horizontal_velocity(level="Higher"):
    text, (s_lo, s_hi), (t_lo, t_hi) = random.choice(_CONTEXTS_HORIZ_V)
    s = round(random.uniform(s_lo, s_hi), 1)
    T = round(random.uniform(t_lo, t_hi), 2)
    context = text.format(s=f"{s:g}", T=f"{T:.2f}")
    v_H = _r2(s / T)
    working_a = [
        {"type": "text",  "content": f"Horizontal velocity is constant: s = {s:g} m, t = {T} s."},
        {"type": "latex", "content": r"s = vt"},
        {"type": "latex", "content": rf"{s:g} = v \times {T}"},
        {"type": "latex", "content": rf"v_H = {v_H}\ \mathrm{{m/s}}"},
    ]
    part_a = _part("Calculate the horizontal component of the initial velocity.", v_H, "m/s", working_a, [
        {"value": _r2(s / (T / 2)), "mistake": f"Use the whole time in the air ({T} s): v = {s:g} ÷ {T} = {v_H} m/s."},
        {"value": _r2(s * T), "mistake": f"Rearrange s = vt for v: v = s ÷ t = {v_H} m/s."},
    ], level)
    t_up = _r2(T / 2)
    v_V = _r2(g * t_up)
    working_b = [
        {"type": "text",  "content": f"Same launch and landing height, so the time to the highest point is {T} ÷ 2 = {t_up} s. There, v = 0."},
        {"type": "latex", "content": r"v = u + at"},
        {"type": "latex", "content": rf"0 = u + (-9.8) \times {t_up}"},
        {"type": "latex", "content": rf"u = v_V = {v_V}\ \mathrm{{m/s}}"},
    ]
    part_b = _part("Calculate the vertical component of the initial velocity.", v_V, "m/s", working_b, [
        {"value": _r2(g * T), "mistake": f"At {T} s the projectile is back at launch height, not at its highest point. Use t = {T} ÷ 2 = {t_up} s: u = {v_V} m/s."},
        {"value": v_H, "mistake": f"That is the horizontal component. For the vertical component use v = u + at to the highest point: u = {v_V} m/s."},
        {"value": _r2(g * t_up / 2), "mistake": f"v = u + at gives u = −at directly — no extra halving: u = 9.8 × {t_up} = {v_V} m/s."},
    ], level, scaffold=[
        {"prompt": "What is the time to reach the highest point?", "answer": t_up},
        {"prompt": "What is the vertical component of the initial velocity?", "answer": v_V},
    ])
    return _scenario(context, [part_a, part_b], level)


# ── Pattern A — Same height: symmetric total time, then range ────────────────
# Source: 2015 Paper 2 Q1 (long jump)

def generate_projectile_a_same_height(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)
    context   = random.choice(_CONTEXTS_L1).format(v=v, theta=theta_deg)

    v_H     = _r2(v * math.cos(theta))
    v_V     = _r2(v * math.sin(theta))
    t_up    = _r2(v_V / g)
    t_total = _r2(2 * t_up)
    R       = _r2(v_H * t_total)

    part_a, part_b = _l2_parts_ab(v, theta_deg, theta, v_H, v_V, level)

    working_t = [
        {"type": "text",  "content": (
            "The projectile lands at the same height it was launched, so it takes equally "
            f"long to rise as to fall. Vertically, up to the highest point: u = {v_V} m/s, "
            f"v = 0, a = −9.8 m/s²."
        )},
        {"type": "latex", "content": r"v = u + at"},
        {"type": "latex", "content": rf"0 = {v_V} + (-9.8) \times t_{{\text{{up}}}}"},
        {"type": "latex", "content": rf"t_{{\text{{up}}}} = \frac{{{v_V}}}{{9.8}} = {t_up}\ \mathrm{{s}}"},
        {"type": "latex", "content": r"t_{\text{total}} = 2 \times t_{\text{up}}"},
        {"type": "latex", "content": rf"t_{{\text{{total}}}} = 2 \times {t_up} = {t_total}\ \mathrm{{s}}"},
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
                    f"This is only the time to reach maximum height ({t_up} s). Since the "
                    f"projectile returns to the **same height**, descent takes equally long. "
                    f"t_total = 2 × {t_up} = {t_total} s."
                ),
                "working": working_t,
            },
            {
                "value": _r2(2 * v / g),
                "mistake": (
                    f"Use the **vertical component** of velocity, not the full initial speed. "
                    f"t_up = v_V ÷ g = {v_V} ÷ 9.8 = {t_up} s, so t_total = 2 × {t_up} = {t_total} s."
                ),
                "working": working_t,
            },
        ],
        working=working_t,
        notes=_NOTES_PROJECTILE,
    )

    working_R = [
        {"type": "text",  "content": "Horizontal velocity is constant throughout. Use the total time:"},
        {"type": "latex", "content": r"s = vt"},
        {"type": "latex", "content": rf"s = {v_H} \times {t_total}"},
        {"type": "latex", "content": rf"s = {R}\ \mathrm{{m}}"},
    ]
    part_d = PhysicsQuestion(
        question_text="Calculate the range.",
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
        scaffold=[
            {"prompt": "What is the total time of flight, t_total?", "answer": t_total},
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
        parts=[part_a, part_b, part_c, part_d],
    ))


# ── Pattern B — Given max height & time to peak, find total time, then range ─
# Source: 2015 Paper 2 Q1 (shot put)

def generate_projectile_b_given_height_time(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)
    h, context = _l2_elevated_context(v, theta_deg)

    v_H   = _r2(v * math.cos(theta))
    v_V   = _r2(v * math.sin(theta))
    h_max = _r2(v_V ** 2 / (2 * g))
    t_up  = _r2(v_V / g)                # given, not asked
    H_top = _r2(h + h_max)              # given, not asked
    t_down  = _r2(math.sqrt(2 * H_top / g))
    t_total = _r2(t_up + t_down)
    R       = _r2(v_H * t_total)

    part_a, part_b = _l2_parts_ab(v, theta_deg, theta, v_H, v_V, level)

    working_t = [
        {"type": "text",  "content": (
            f"The projectile falls {H_top} m from the top to the ground. From the highest "
            f"point the vertical velocity is zero: u = 0, s = −{H_top} m, a = −9.8 m/s²."
        )},
        {"type": "latex", "content": r"s = ut + \tfrac{1}{2}at^2"},
        {"type": "latex", "content": rf"-{H_top} = (0 \times t_{{\text{{down}}}}) + \tfrac{{1}}{{2}} \times (-9.8) \times t_{{\text{{down}}}}^2"},
        {"type": "latex", "content": rf"t_{{\text{{down}}}} = \sqrt{{\frac{{2 \times {H_top}}}{{9.8}}}} = {t_down}\ \mathrm{{s}}"},
        {"type": "text",  "content": "Add the given time already spent rising to the maximum height:"},
        {"type": "latex", "content": r"t_{\text{total}} = t_{\text{up}} + t_{\text{down}}"},
        {"type": "latex", "content": rf"t_{{\text{{total}}}} = {t_up} + {t_down} = {t_total}\ \mathrm{{s}}"},
    ]
    part_c = PhysicsQuestion(
        question_text=(
            f"The maximum height reached by the projectile is {H_top} m above the ground. "
            f"The time between launch and reaching this height is {t_up} s. "
            f"Calculate the total time between the projectile being launched and hitting the ground."
        ),
        correct_answer=t_total,
        unit="s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": t_down,
                "mistake": (
                    f"This is only the time falling from the maximum height. Add the given time "
                    f"already spent rising: t_total = t_up + t_down = {t_up} + {t_down} = {t_total} s."
                ),
                "working": working_t,
            },
            {
                "value": _r2(t_up + math.sqrt(H_top / g)),
                "mistake": (
                    f"You appear to have left out the factor of 2 under the square root. "
                    f"t_down = √(2 × H_top ÷ g) = √(2 × {H_top} ÷ 9.8) = {t_down} s, "
                    f"so t_total = {t_up} + {t_down} = {t_total} s."
                ),
                "working": working_t,
            },
        ],
        working=working_t,
        notes=_NOTES_PROJECTILE,
    )

    working_R = [
        {"type": "text",  "content": "Horizontal velocity is constant throughout. Use the total time:"},
        {"type": "latex", "content": r"s = vt"},
        {"type": "latex", "content": rf"s = {v_H} \times {t_total}"},
        {"type": "latex", "content": rf"s = {R}\ \mathrm{{m}}"},
    ]
    part_d = PhysicsQuestion(
        question_text="Calculate the range of the projectile for this throw.",
        correct_answer=R,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(v_H * t_up),
                "mistake": (
                    f"You appear to have used only the given time to reach maximum height. "
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
        scaffold=[
            {"prompt": "What is the total time of flight, t_total?", "answer": t_total},
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
        parts=[part_a, part_b, part_c, part_d],
    ))


# ── Pattern C — Time to peak (calculated), given further time, then range ────
# Source: skier off a ramp

def generate_projectile_c_time_then_range(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)
    h, context = _l2_elevated_context(v, theta_deg)

    v_H  = _r2(v * math.cos(theta))
    v_V  = _r2(v * math.sin(theta))
    t_up = _r2(v_V / g)

    part_a, part_b = _l2_parts_ab(v, theta_deg, theta, v_H, v_V, level)
    part_c = _l2_part_time_to_peak(v, v_H, v_V, t_up, theta_deg, level)

    t2      = round(random.uniform(0.5, 2.0) * t_up, 2)
    t_total = _r2(t_up + t2)
    R       = _r2(v_H * t_total)

    working_R = [
        {"type": "text",  "content": "Add the given time falling from the top to the time already spent rising:"},
        {"type": "latex", "content": r"t_{\text{total}} = t_{\text{up}} + t_2"},
        {"type": "latex", "content": rf"t_{{\text{{total}}}} = {t_up} + {t2} = {t_total}\ \mathrm{{s}}"},
        {"type": "text",  "content": "Horizontal velocity is constant throughout, so:"},
        {"type": "latex", "content": r"s = vt"},
        {"type": "latex", "content": rf"s = {v_H} \times {t_total} = {R}\ \mathrm{{m}}"},
    ]
    part_d = PhysicsQuestion(
        question_text=(
            f"The projectile takes a further {t2} s to travel from its maximum height to the "
            f"ground. Calculate the horizontal distance the projectile travels from launch "
            f"until landing."
        ),
        correct_answer=R,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(v_H * t2),
                "mistake": (
                    f"You appear to have only used the further time ({t2} s), forgetting the "
                    f"time already spent rising to maximum height. t_total = t_up + t₂ = "
                    f"{t_up} + {t2} = {t_total} s, so R = {v_H} × {t_total} = {R} m."
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
        scaffold=[
            {"prompt": "What is the total time of flight, t_up + t₂?", "answer": t_total},
            {"prompt": "What is the horizontal distance travelled, R?", "answer": R},
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


# ── Pattern D — Time to peak (calculated), given further time, then height ───
# Source: wet sponge thrown at a teacher

def generate_projectile_d_time_then_height(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)
    h, context = _l2_elevated_context(v, theta_deg)

    v_H   = _r2(v * math.cos(theta))
    v_V   = _r2(v * math.sin(theta))
    t_up  = _r2(v_V / g)
    h_max = _r2(v_V ** 2 / (2 * g))
    H_top = _r2(h + h_max)
    t_down_full = _r2(math.sqrt(2 * H_top / g))

    part_a, part_b = _l2_parts_ab(v, theta_deg, theta, v_H, v_V, level)
    part_c = _l2_part_time_to_peak(v, v_H, v_V, t_up, theta_deg, level)

    t2 = round(random.uniform(0.25, 0.85) * t_down_full, 2)
    s  = _r2(0.5 * g * t2 ** 2)
    h_final = _r2(H_top - s)

    working_d = [
        {"type": "text",  "content": (
            f"At maximum height, the projectile is {H_top} m above the ground. "
            f"From there, vertically: u = 0, t = {t2} s, a = −9.8 m/s²."
        )},
        {"type": "latex", "content": r"s = ut + \tfrac{1}{2}at^2"},
        {"type": "latex", "content": rf"s = (0 \times {t2}) + \tfrac{{1}}{{2}} \times (-9.8) \times {t2}^2 = -{s}\ \mathrm{{m}}"},
        {"type": "text",  "content": "So its height above the ground at this time is:"},
        {"type": "latex", "content": rf"h = {H_top} + (-{s}) = {h_final}\ \mathrm{{m}}"},
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

    part_d.distractors = _distinct(h_final, part_d.distractors)

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


# ── Pattern E — Horizontal distance to a target: find time, then height ──────
# Source: crossbar challenge

_CONTEXTS_E = [
    "A footballer kicks a ball from flat ground at **{v} m/s** at **{theta}°** above the "
    "horizontal, towards a crossbar **{x_target:g} m** away.",
    "A player strikes a ball from flat ground at **{v} m/s** at **{theta}°** to the "
    "horizontal, towards a crossbar **{x_target:g} m** away.",
]


def generate_projectile_e_horizontal_backwards(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice(_SPEEDS)
    theta     = math.radians(theta_deg)

    v_H = _r2(v * math.cos(theta))
    v_V = _r2(v * math.sin(theta))
    t_total_flight = _r2(2 * v_V / g)
    R_total  = _r2(v_H * t_total_flight)
    x_target = round(R_total * random.uniform(0.25, 0.85), 1)
    t = _r3(x_target / v_H)
    h_final = _r2(v_V * t - 0.5 * g * t ** 2)

    context = random.choice(_CONTEXTS_E).format(v=v, theta=theta_deg, x_target=x_target)

    part_a, part_b = _l2_parts_ab(v, theta_deg, theta, v_H, v_V, level)

    working_t = [
        {"type": "text",  "content": "Horizontal velocity is constant, so the time to travel this horizontal distance is:"},
        {"type": "latex", "content": r"s = vt"},
        {"type": "latex", "content": rf"{x_target:g} = {v_H} \times t"},
        {"type": "latex", "content": rf"t = \frac{{{x_target:g}}}{{{v_H}}} = {t}\ \mathrm{{s}}"},
    ]
    part_c = PhysicsQuestion(
        question_text=f"Calculate the time taken for the ball to reach the crossbar, {x_target:g} m away.",
        correct_answer=t,
        unit="s",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r3(x_target / v),
                "mistake": (
                    f"Use the **horizontal component** v_H = {v_H} m/s, not the full initial "
                    f"speed. t = x ÷ v_H = {x_target:g} ÷ {v_H} = {t} s."
                ),
                "working": working_t,
            },
            {
                "value": _r3(x_target / v_V),
                "mistake": (
                    f"Horizontal distance is covered at the **horizontal** velocity, not the "
                    f"vertical component. t = x ÷ v_H = {x_target:g} ÷ {v_H} = {t} s."
                ),
                "working": working_t,
            },
        ],
        working=working_t,
        notes=_NOTES_PROJECTILE,
    )

    working_h = [
        {"type": "text",  "content": f"Vertically, from launch (taking upward as positive): u = {v_V} m/s, t = {t} s, a = −9.8 m/s²."},
        {"type": "latex", "content": r"s = ut + \tfrac{1}{2}at^2"},
        {"type": "latex", "content": rf"s = ({v_V} \times {t}) + \tfrac{{1}}{{2}} \times (-9.8) \times {t}^2"},
        {"type": "latex", "content": rf"s = {h_final}\ \mathrm{{m}}"},
    ]
    part_d = PhysicsQuestion(
        question_text="Calculate the height above the ground at which the ball reaches the crossbar.",
        correct_answer=h_final,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(v_V * t),
                "mistake": (
                    f"You left out the effect of gravity. Use s = v_V t − ½gt² = "
                    f"{v_V} × {t} − ½ × 9.8 × {t}² = {h_final} m."
                ),
                "working": working_h,
            },
            {
                "value": _r2(v_V * t + 0.5 * g * t ** 2),
                "mistake": (
                    f"Sign error — gravity decelerates the upward motion, so the term is "
                    f"subtracted, not added: s = v_V t − ½gt² = {h_final} m."
                ),
                "working": working_h,
            },
        ],
        working=working_h,
        notes=_NOTES_PROJECTILE,
        scaffold=[
            {"prompt": "What is the time taken to reach the crossbar, t?", "answer": t},
            {"prompt": "What is the height above the ground at this time?", "answer": h_final},
        ],
    )

    correct = (
        f"No, the ball would pass under the crossbar (or fall short of it) — at the same "
        f"angle, a lower speed means the ball is lower at every horizontal distance than "
        f"before, so it does not reach the crossbar's height by the time it gets there."
    )
    distractors_e = [
        {
            "value": (
                "The ball would pass over the crossbar, since a lower speed means the ball "
                "spends longer in the air and so gains more height."
            ),
            "mistake": (
                "A lower speed (same angle) gives a smaller v_H **and** a smaller v_V — the "
                "ball reaches less height at any given horizontal distance, not more."
            ),
            "working": working_h,
        },
        {
            "value": (
                "The ball would still hit the crossbar in the same place, since the angle "
                "hasn't changed."
            ),
            "mistake": (
                "The angle only fixes the **shape** of the path (the ratio of v_H to v_V) — "
                "the actual height reached at a given horizontal distance still depends on "
                "the speed."
            ),
            "working": working_h,
        },
    ]
    options = [correct] + [d["value"] for d in distractors_e]
    random.shuffle(options)
    part_e = PhysicsQuestion(
        question_text=(
            "The player takes another attempt, using the same angle but a lower initial "
            "speed. State whether the ball would hit the crossbar, pass over it, or pass "
            "under it. Justify your answer."
        ),
        correct_answer=correct,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=distractors_e,
        working=working_h,
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


# ── Pattern F — Given total flight time, then a clearance height ─────────────
# Source: Doppler ball

_CONTEXTS_F = [
    "A student throws a ball to a friend at **{v} m/s** at **{theta}°** above the horizontal, "
    "releasing it from a height of **{h} m**. The ball passes over the friend's head before landing.",
    "A player throws a ball towards a teammate at **{v} m/s** at **{theta}°** above the "
    "horizontal, from a height of **{h} m**. The ball passes over the teammate's head before landing.",
]


def generate_projectile_f_given_time_clearance(level="Higher"):
    theta_deg = random.choice(_ANGLES)
    v         = random.choice([s for s in _SPEEDS if s <= 20])  # a casual throw, not a kick
    theta     = math.radians(theta_deg)
    h = random.choice(_L2_HUMAN_HEIGHTS)
    context = random.choice(_CONTEXTS_F).format(v=v, theta=theta_deg, h=h)

    v_H   = _r2(v * math.cos(theta))
    v_V   = _r2(v * math.sin(theta))
    h_max = _r2(v_V ** 2 / (2 * g))
    t_up  = _r2(v_V / g)
    H_top = _r2(h + h_max)
    t_down = _r2(math.sqrt(2 * H_top / g))
    T = _r2(t_up + t_down)   # given directly to the student, not derived
    R = _r2(v_H * T)

    part_a, part_b = _l2_parts_ab(v, theta_deg, theta, v_H, v_V, level)

    working_R = [
        {"type": "text",  "content": "Horizontal velocity is constant, so:"},
        {"type": "latex", "content": r"s = vt"},
        {"type": "latex", "content": rf"s = {v_H} \times {T} = {R}\ \mathrm{{m}}"},
    ]
    part_c = PhysicsQuestion(
        question_text=(
            f"The ball takes {T} s to travel from being released to landing. "
            f"Calculate the horizontal distance travelled by the ball."
        ),
        correct_answer=R,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": _r2(v * T),
                "mistake": (
                    f"Use the **horizontal component** (v_H = {v_H} m/s), "
                    f"not the full initial speed ({v} m/s). R = {v_H} × {T} = {R} m."
                ),
                "working": working_R,
            },
            {
                "value": _r2(v_V * T),
                "mistake": (
                    f"That's the **vertical** component. Horizontal distance uses the "
                    f"horizontal component: R = v_H × T = {v_H} × {T} = {R} m."
                ),
                "working": working_R,
            },
        ],
        working=working_R,
        notes=_NOTES_PROJECTILE,
    )

    # Sample near the peak, where the ball is comfortably above head height.
    t3 = round(t_up * random.uniform(0.7, 1.0), 2)
    ball_h = _r2(h + v_V * t3 - 0.5 * g * t3 ** 2)
    reach_height = round(min(2.3, max(1.5, ball_h * random.uniform(0.5, 0.8))), 2)
    gap = _r2(ball_h - reach_height)

    working_d = [
        {"type": "text",  "content": f"Vertically, from launch (taking upward as positive): u = {v_V} m/s, t = {t3} s, a = −9.8 m/s²."},
        {"type": "latex", "content": r"s = ut + \tfrac{1}{2}at^2"},
        {"type": "latex", "content": rf"s = ({v_V} \times {t3}) + \tfrac{{1}}{{2}} \times (-9.8) \times {t3}^2 = {_r2(ball_h - h)}\ \mathrm{{m}}"},
        {"type": "text",  "content": f"It was released {h:g} m above the ground, so its height at this time is:"},
        {"type": "latex", "content": rf"h = {h:g} + ({_r2(ball_h - h)}) = {ball_h}\ \mathrm{{m}}"},
        {"type": "text",  "content": f"The friend's maximum reach is {reach_height} m, so the gap above their reach is:"},
        {"type": "latex", "content": rf"\text{{gap}} = {ball_h} - {reach_height} = {gap}\ \mathrm{{m}}"},
    ]
    part_d = PhysicsQuestion(
        question_text=(
            f"The ball is directly above the friend {t3} s after it was released. "
            f"The friend has a maximum reach of {reach_height} m. "
            f"Determine the height h between the friend's reach and the ball."
        ),
        correct_answer=gap,
        unit="m",
        topic="Our Dynamic Universe",
        question_type="Projectile Motion",
        level=level,
        distractors=[
            {
                "value": ball_h,
                "mistake": (
                    f"This is the ball's height above the **ground**, not above the friend's "
                    f"reach. Subtract the reach height: h = {ball_h} − {reach_height} = {gap} m."
                ),
                "working": working_d,
            },
            {
                "value": _r2(h + v_V * t3 + 0.5 * g * t3 ** 2 - reach_height),
                "mistake": (
                    f"Sign error — gravity decelerates the ball's rise, so the term is "
                    f"subtracted, not added: s = h + v_V t − ½gt² = {ball_h} m, "
                    f"so h = {ball_h} − {reach_height} = {gap} m."
                ),
                "working": working_d,
            },
        ],
        working=working_d,
        notes=_NOTES_PROJECTILE,
        scaffold=[
            {"prompt": "What is the ball's height above the ground at this time?", "answer": ball_h},
            {"prompt": "What is the height h between the friend's reach and the ball?", "answer": gap},
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
