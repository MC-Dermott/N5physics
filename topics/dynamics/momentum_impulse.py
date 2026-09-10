import random
import pathlib
from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

_COLLISIONS_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "momentum_collisions_widget.html"
).read_text(encoding="utf-8")

_IMPULSE_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "impulse_widget.html"
).read_text(encoding="utf-8")


def _with_collisions_widget(question, initial_mode):
    question.metadata["widget_html"] = _COLLISIONS_WIDGET_HTML.replace("__INITIAL_MODE__", initial_mode)
    question.metadata["widget_height"] = 900
    return question


def _with_impulse_widget(question):
    question.metadata["widget_html"] = _IMPULSE_WIDGET_HTML
    question.metadata["widget_height"] = 1200
    return question

_NOTES = """
## Momentum and Impulse

**Definitions:**
- Momentum is the product of an object's mass and velocity — it is a vector, so direction
  matters.
- Impulse is the change in momentum produced by a force acting for a certain time; it is
  also equal to the area under a force–time graph.

$$p = mv$$
$$m_1u_1 + m_2u_2 = m_1v_1 + m_2v_2 \\ \\text{(total momentum before = total momentum after)}$$
$$Ft = mv - mu$$
$$E_k = \\frac{1}{2}mv^2$$

| Symbol | Quantity | Unit |
|---|---|---|
| p | Momentum | kg m/s |
| m | Mass | kg |
| v, u | Final / initial velocity | m/s |
| F | Force | N |
| t | Time | s |
| $E_k$ | Kinetic energy | J |

> **Important:** Total momentum before a collision or explosion always equals total
> momentum after, provided no external forces act. Always state which direction is positive
> before substituting — a velocity in the opposite direction must be entered as negative.
> In an explosion, both objects start at rest, so total momentum before is zero. A collision
> is elastic only if total kinetic energy is the same before and after; otherwise it is
> inelastic.
"""

# Each context object is tied to its own plausible mass range, so a generated
# question never pairs (e.g.) a "snooker ball" with a 56 kg mass.
_KINDS = [
    ("trolley", 0.2, 2.5),
    ("curling stone", 15, 25),
    ("ice hockey puck", 0.15, 0.20),
    ("snooker ball", 0.15, 0.20),
    ("car", 900, 2000),
    ("railway wagon", 1500, 4000),
    ("boat", 500, 3000),
]

_SMALL_KINDS = [k for k in _KINDS if k[2] <= 25]
_LARGE_KINDS = [k for k in _KINDS if k[1] >= 500]


def _pick_kind(pool):
    return random.choice(pool)


def _mass_for(kind, dp=2):
    name, lo, hi = kind
    return round(random.uniform(lo, hi), dp)


def _scaled_mass_and_obj():
    """Pick a mass and a context object that plausibly matches its scale."""
    name, lo, hi = random.choice(_KINDS)
    dp = 2 if hi <= 25 else 0
    m = round(random.uniform(lo, hi), dp)
    return (int(m) if dp == 0 else m), name


def _r2(val):
    return round(float(val), 2)


def _round_sf(val, sf=3):
    val = float(val)
    if val == 0:
        return 0.0
    return float(f"{val:.{sf}g}")


def _cap(s):
    return s[0].upper() + s[1:]


def _a(s):
    return "An" if s[0] in "aeiou" else "A"


# ── Type 1: Basic momentum calculations (p = mv) ─────────────────────────────

def gen_p_from_mv(level="Higher"):
    m, obj = _scaled_mass_and_obj()
    v = round(random.uniform(2, 30), 1)
    p = _r2(m * v)

    question = f"{_a(obj)} {obj} of mass {m} kg travels at {v} m/s. Calculate its momentum."
    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"p = mv"},
        {"type": "latex", "content": rf"p = {m} \times {v}"},
        {"type": "latex", "content": rf"p = {p}\ \mathrm{{kg\ m/s}}"},
    ]
    options_data = [
        {"value": p, "mistake": None, "working": working},
        {"value": _r2(m / v), "mistake": "You divided m by v instead of multiplying. p = m × v.", "working": working},
        {"value": _r2(m + v), "mistake": "Momentum is the product of mass and velocity, not their sum. p = m × v.", "working": working},
    ]
    return make_question(question, p, options_data, "kg m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Momentum and Impulse", level=level)


def gen_v_from_pm(level="Higher"):
    m, obj = _scaled_mass_and_obj()
    v = round(random.uniform(2, 30), 1)
    p = _r2(m * v)

    question = f"{_a(obj)} {obj} of mass {m} kg has a momentum of {p} kg m/s. Calculate its velocity."
    working = [
        {"type": "text",  "content": "Rearrange p = mv for v:"},
        {"type": "latex", "content": r"v = \frac{p}{m}"},
        {"type": "latex", "content": rf"v = \frac{{{p}}}{{{m}}}"},
        {"type": "latex", "content": rf"v = {v}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v, "mistake": None, "working": working},
        {"value": _r2(p * m), "mistake": "You multiplied p by m instead of dividing. v = p ÷ m.", "working": working},
        {"value": _r2(m / p), "mistake": "You divided the wrong way round. v = p ÷ m.", "working": working},
    ]
    return make_question(question, v, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Momentum and Impulse", level=level)


def gen_m_from_pv(level="Higher"):
    m, obj = _scaled_mass_and_obj()
    v = round(random.uniform(2, 30), 1)
    p = _r2(m * v)

    question = f"{_a(obj)} {obj} travelling at {v} m/s has a momentum of {p} kg m/s. Calculate its mass."
    working = [
        {"type": "text",  "content": "Rearrange p = mv for m:"},
        {"type": "latex", "content": r"m = \frac{p}{v}"},
        {"type": "latex", "content": rf"m = \frac{{{p}}}{{{v}}}"},
        {"type": "latex", "content": rf"m = {m}\ \mathrm{{kg}}"},
    ]
    options_data = [
        {"value": float(m), "mistake": None, "working": working},
        {"value": _r2(p * v), "mistake": "You multiplied p by v instead of dividing. m = p ÷ v.", "working": working},
        {"value": _r2(v / p), "mistake": "You divided the wrong way round. m = p ÷ v.", "working": working},
    ]
    return make_question(question, float(m), options_data, "kg",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Momentum and Impulse", level=level)


def generate_momentum_basic(level="Higher"):
    return random.choice([gen_p_from_mv, gen_v_from_pm, gen_m_from_pv])(level=level)


# ── Type 2: Collisions where objects stick together ──────────────────────────

def gen_stick_together(level="Higher"):
    small = random.choice([True, False])
    kind = _pick_kind(_SMALL_KINDS if small else _LARGE_KINDS)
    obj1, obj2 = f"{kind[0]} A", f"{kind[0]} B"
    if small:
        m1 = _mass_for(kind)
        m2 = _mass_for(kind)
        u1 = round(random.uniform(1.0, 4.0), 1)
        u2 = round(random.uniform(0.2, 1.5), 1)
    else:
        m1 = int(_mass_for(kind, dp=0))
        m2 = int(_mass_for(kind, dp=0))
        u1 = round(random.uniform(3.0, 12.0), 1)
        u2 = round(random.uniform(1.0, 4.0), 1)
    u2_moving = random.choice([True, False])
    u2 = u2 if u2_moving else 0.0

    total_before = _r2(m1 * u1 + m2 * u2)
    total_mass = _r2(m1 + m2)
    v = _r2(total_before / total_mass)
    moving_desc = f"moving in the same direction at {u2} m/s" if u2_moving else "stationary"
    question = (
        f"{_cap(obj1)} (mass {m1} kg), moving at {u1} m/s, collides with "
        f"{obj2} (mass {m2} kg), {moving_desc}. The two stick together after the "
        f"collision. Calculate their common velocity."
    )
    working = [
        {"type": "text",  "content": "Total momentum before = total momentum after:"},
        {"type": "latex", "content": r"m_1u_1 + m_2u_2 = (m_1 + m_2)v"},
        {"type": "latex", "content": rf"({m1} \times {u1}) + ({m2} \times {u2}) = ({total_mass})v"},
        {"type": "latex", "content": rf"{total_before} = {total_mass}v"},
        {"type": "latex", "content": rf"v = {v}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v, "mistake": None, "working": working},
        {"value": _r2(total_before / m1), "mistake": "You divided by only one mass. Use the combined mass (m1 + m2) after they stick together.", "working": working},
        {"value": _r2((m1 * u1 - m2 * u2) / total_mass), "mistake": "Both objects move in the same direction here, so their momenta should be added, not subtracted.", "working": working},
    ]
    scaffold = [
        {"question": "What is the total momentum before the collision?", "answer": total_before},
        {"question": "What is the common velocity v after the collision?", "answer": v},
    ]
    return _with_collisions_widget(make_question(question, v, options_data, "m/s", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Momentum and Impulse", level=level), "stick")


# ── Type 3: Collisions where objects separate ────────────────────────────────

def gen_separate(level="Higher"):
    small = random.choice([True, False])
    kind = _pick_kind(_SMALL_KINDS if small else _LARGE_KINDS)
    obj1, obj2 = f"{kind[0]} A", f"{kind[0]} B"
    if small:
        m1 = _mass_for(kind)
        m2 = _mass_for(kind)
        u1 = round(random.uniform(1.5, 5.0), 1)
        u2_mag = round(random.uniform(0.5, 3.0), 1)
    else:
        m1 = int(_mass_for(kind, dp=0))
        m2 = int(_mass_for(kind, dp=0))
        u1 = round(random.uniform(6.0, 15.0), 1)
        u2_mag = round(random.uniform(3.0, 10.0), 1)

    opposite = random.choice([True, False])
    u2 = u2_mag * (-1 if opposite else 1)
    v1 = round(random.uniform(0.2, u1 * 0.6), 2) * random.choice([-1, 1])

    total_before = _r2(m1 * u1 + m2 * u2)
    v2 = _r2((total_before - m1 * v1) / m2)
    dir2 = "in the opposite direction" if opposite else "in the same direction"
    v1_dir = "continues forward" if v1 > 0 else "rebounds"
    question = (
        f"{_cap(obj1)} (mass {m1} kg) travelling at {u1} m/s collides with "
        f"{obj2} (mass {m2} kg) travelling at {abs(u2)} m/s {dir2}. After the collision "
        f"{obj1} {v1_dir} at {abs(v1)} m/s. Calculate the velocity of {obj2} immediately "
        f"after the collision (taking {obj1}'s initial direction as positive)."
    )
    working = [
        {"type": "text",  "content": "Total momentum before = total momentum after:"},
        {"type": "latex", "content": r"m_1u_1 + m_2u_2 = m_1v_1 + m_2v_2"},
        {"type": "latex", "content": rf"({m1} \times {u1}) + ({m2} \times {u2}) = ({m1} \times {v1}) + {m2}v_2"},
        {"type": "latex", "content": rf"{total_before} = {_r2(m1*v1)} + {m2}v_2"},
        {"type": "latex", "content": rf"v_2 = {v2}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v2, "mistake": None, "working": working},
        {"value": _r2((m1 * u1 + m2 * u2 + m1 * v1) / m2), "mistake": "Check your rearrangement — m1v1 should be subtracted from the total, not added.", "working": working},
        {"value": _r2((m1 * u1 - m2 * u2 - m1 * v1) / m2), "mistake": "Check the sign of u2 in your substitution — direction matters throughout.", "working": working},
    ]
    scaffold = [
        {"question": "What is the total momentum before the collision?", "answer": total_before},
        {"question": "What is v2, the velocity of the second object?", "answer": v2},
    ]
    return _with_collisions_widget(make_question(question, v2, options_data, "m/s", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Momentum and Impulse", level=level), "separate")


# ── Type 4: Explosions and recoil ────────────────────────────────────────────

def gen_explosion(level="Higher"):
    m1 = round(random.uniform(0.5, 3.0), 2)
    m2 = round(random.uniform(0.5, 3.0), 2)
    v1 = round(random.uniform(2.0, 20.0), 1)
    v2 = _r2(-(m1 * v1) / m2)

    momentum1 = _r2(m1 * v1)
    total_mass = round(m1 + m2, 2)
    question = (
        f"A stationary firework shell of total mass {total_mass} kg explodes into two "
        f"fragments: fragment A (mass {m1} kg) and fragment B (mass {m2} kg). Fragment A "
        f"moves off at {v1} m/s. Calculate the velocity of fragment B immediately after "
        f"the explosion."
    )
    working = [
        {"type": "text",  "content": "Total momentum before the explosion is zero:"},
        {"type": "latex", "content": r"0 = m_1v_1 + m_2v_2"},
        {"type": "latex", "content": rf"0 = ({m1} \times {v1}) + {m2}v_2"},
        {"type": "latex", "content": rf"0 = {momentum1} + {m2}v_2"},
        {"type": "latex", "content": rf"v_2 = {v2}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v2, "mistake": None, "working": working},
        {"value": abs(v2), "mistake": "The two parts must move in opposite directions for total momentum to stay zero — check your sign.", "working": working},
        {"value": _r2(momentum1 / m2), "mistake": "Total momentum before the explosion is zero, so the two final momenta must be equal and opposite — check your sign.", "working": working},
    ]
    scaffold = [
        {"question": "What is the momentum of fragment A (m1 × v1)?", "answer": momentum1},
        {"question": "What is the velocity of fragment B?", "answer": v2},
    ]
    return _with_collisions_widget(make_question(question, v2, options_data, "m/s", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Momentum and Impulse", level=level), "explosion")


# ── Impulse: Ft = mv - mu ─────────────────────────────────────────────────────

def gen_impulse_find_f(level="Higher"):
    m = round(random.uniform(0.05, 0.5), 3)
    u = round(random.uniform(0, 5), 1)
    v = round(random.uniform(u + 2, u + 25), 1)
    t = round(random.uniform(0.005, 0.05), 3)
    delta_p = _r2(m * v - m * u)
    F = _r2(delta_p / t)

    obj = random.choice(["ball", "puck", "shuttlecock"])
    question = (
        f"A {obj} of mass {m} kg, initially moving at {u} m/s, is struck and speeds up to "
        f"{v} m/s. The force acts for {t} s. Calculate the average force exerted on the {obj}."
    )
    working = [
        {"type": "text",  "content": "Use the impulse equation:"},
        {"type": "latex", "content": r"Ft = mv - mu"},
        {"type": "latex", "content": rf"F \times {t} = ({m} \times {v}) - ({m} \times {u})"},
        {"type": "latex", "content": rf"F \times {t} = {delta_p}"},
        {"type": "latex", "content": rf"F = {F}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": F, "mistake": None, "working": working},
        {"value": _r2(delta_p * t), "mistake": "You multiplied by t instead of dividing. F = (mv − mu) ÷ t.", "working": working},
        {"value": _r2((m * v + m * u) / t), "mistake": "You added mv and mu instead of subtracting. F = (mv − mu) ÷ t.", "working": working},
    ]
    scaffold = [
        {"question": "What is the change in momentum (mv − mu)?", "answer": delta_p},
        {"question": "What is the average force F?", "answer": F},
    ]
    return _with_impulse_widget(make_question(question, F, options_data, "N", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Momentum and Impulse", level=level))


def gen_impulse_find_t(level="Higher"):
    m = round(random.uniform(0.05, 0.5), 3)
    u = 0.0
    v = round(random.uniform(5, 40), 1)
    F = round(random.uniform(500, 8000), 0)
    delta_p = _r2(m * v - m * u)
    t = _round_sf(delta_p / F)

    obj = random.choice(["ball", "puck"])
    question = (
        f"A club exerts an average force of {F:g} N on a stationary {obj} of mass {m} kg. "
        f"The {obj} leaves the club at {v} m/s. Calculate the time for which the club is in "
        f"contact with the {obj}."
    )
    working = [
        {"type": "text",  "content": "Use the impulse equation:"},
        {"type": "latex", "content": r"Ft = mv - mu"},
        {"type": "latex", "content": rf"{F:g} \times t = ({m} \times {v}) - 0"},
        {"type": "latex", "content": rf"{F:g} \times t = {delta_p}"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t, "mistake": None, "working": working},
        {"value": _r2(delta_p * F), "mistake": "You multiplied by F instead of dividing. t = (mv − mu) ÷ F.", "working": working},
        {"value": _r2(F / delta_p), "mistake": "You divided the wrong way round. t = (mv − mu) ÷ F.", "working": working},
    ]
    scaffold = [
        {"question": "What is the change in momentum (mv − mu)?", "answer": delta_p},
        {"question": "What is the contact time t?", "answer": t},
    ]
    return _with_impulse_widget(make_question(question, t, options_data, "s", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Momentum and Impulse", level=level))


def generate_impulse_basic(level="Higher"):
    return random.choice([gen_impulse_find_f, gen_impulse_find_t])(level=level)


# ── Impulse from a force-time graph ──────────────────────────────────────────

def gen_impulse_graph(level="Higher"):
    m = round(random.uniform(0.1, 0.6), 2)
    peak_F = random.choice([400, 500, 600, 700, 800, 900, 1000, 1200])
    t_peak = round(random.uniform(0.006, 0.012), 3)
    t_total = round(t_peak * 2, 3)
    impulse = _r2(0.5 * t_total * peak_F)
    v = _r2(impulse / m)

    obj = random.choice(["football", "rugby ball", "hockey ball"])
    context = (
        f"A {obj}, initially at rest, is kicked. The force-time graph for the kick is a "
        f"triangle, rising from 0 to a peak force of {peak_F} N at t = {t_peak} s, then "
        f"falling back to 0 N at t = {t_total} s. The mass of the {obj} is {m} kg."
    )

    working_a = [
        {"type": "text",  "content": "Impulse equals the area under the force-time graph:"},
        {"type": "latex", "content": r"\text{impulse} = \frac{1}{2} \times \text{base} \times \text{height}"},
        {"type": "latex", "content": rf"\text{{impulse}} = \frac{{1}}{{2}} \times {t_total} \times {peak_F}"},
        {"type": "latex", "content": rf"\text{{impulse}} = {impulse}\ \mathrm{{N\ s}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the impulse given to the ball.",
        correct_answer=impulse, unit="N s",
        topic="Our Dynamic Universe", question_type="Momentum and Impulse", level=level,
        working=working_a,
        distractors=[
            {"value": _r2(t_total * peak_F),
             "mistake": "You found the area of a rectangle. For a triangular force-time graph, impulse = ½ × base × height.",
             "working": working_a},
            {"value": float(peak_F),
             "mistake": "This is just the peak force, not the impulse. Impulse is the whole area under the graph.",
             "working": working_a},
        ],
        notes=_NOTES,
        scaffold=[{"prompt": "What is the impulse (area under the graph)?", "answer": impulse}],
    )

    working_b = [
        {"type": "text",  "content": "The ball starts from rest, so impulse equals its final momentum:"},
        {"type": "latex", "content": r"Ft = mv - mu"},
        {"type": "latex", "content": rf"{impulse} = {m}v - 0"},
        {"type": "latex", "content": rf"v = {v}\ \mathrm{{m/s}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the velocity of the ball as it leaves the ground.",
        correct_answer=v, unit="m/s",
        topic="Our Dynamic Universe", question_type="Momentum and Impulse", level=level,
        working=working_b,
        distractors=[
            {"value": _r2(impulse * m),
             "mistake": "You multiplied the impulse by the mass instead of dividing. v = impulse ÷ m.",
             "working": working_b},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": "What is the impulse given to the ball (area under the graph)?", "answer": impulse},
            {"prompt": "What is the velocity of the ball?", "answer": v},
        ],
    )

    return _with_impulse_widget(PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Momentum and Impulse", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    ))


# ── Elastic and inelastic collisions ─────────────────────────────────────────
#
# Covers all the collision "types" the worksheet's Section 3 now works through:
#   - stick together, stationary target      (perfectly inelastic)
#   - stick together, head-on, both moving   (perfectly inelastic)
#   - separate, stationary target, elastic   (kinetic energy conserved)
#   - separate, stationary target, partial   (inelastic, but doesn't stick)

def gen_elastic_inelastic(level="Higher"):
    m1 = round(random.uniform(0.3, 1.5), 2)
    m2 = round(random.uniform(0.3, 1.5), 2)
    u1 = round(random.uniform(2.0, 5.0), 1)

    collision_type = random.choice(["stick_stationary", "stick_moving", "elastic", "partial"])

    if collision_type == "stick_moving":
        opposite = random.choice([True, False])
        u2_mag = round(random.uniform(0.5, 2.5), 1)
        u2 = u2_mag * (-1 if opposite else 1)
    else:
        u2 = 0.0

    total_p = _r2(m1 * u1 + m2 * u2)
    total_mass = round(m1 + m2, 3)
    v_stick = round(total_p / total_mass, 3)

    # Stationary-target elastic solution — used directly for the "elastic" type,
    # and as one endpoint when interpolating a "partial" (separates, but lossy) outcome.
    v1_elastic = round(((m1 - m2) / (m1 + m2)) * u1, 3)
    v2_elastic = round((2 * m1 / (m1 + m2)) * u1, 3)

    if collision_type in ("stick_stationary", "stick_moving"):
        v1 = v2 = v_stick
    elif collision_type == "elastic":
        v1, v2 = v1_elastic, v2_elastic
    else:  # "partial": separates, and loses some — but not all — kinetic energy.
        # Interpolating between the stick solution (minimum possible Ek after,
        # at f=0) and the elastic solution (maximum possible Ek after, at f=1)
        # guarantees a physically valid, genuinely inelastic outcome for any
        # f strictly between 0 and 1.
        f = round(random.uniform(0.25, 0.75), 2)
        v1 = round(v_stick + f * (v1_elastic - v_stick), 3)
        v2 = round((total_p - m1 * v1) / m2, 3)

    ek_before = _r2(0.5 * m1 * u1 ** 2 + 0.5 * m2 * u2 ** 2)
    ek_after = _r2(0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2)
    is_elastic = abs(ek_before - ek_after) < 0.01 * max(ek_before, 0.01)

    kind_name = _pick_kind(_SMALL_KINDS)[0]
    obj1, obj2 = f"{kind_name} A", f"{kind_name} B"
    if u2 == 0:
        setup = f"a stationary {obj2} of mass {m2} kg"
    else:
        dir2 = "in the same direction" if u2 > 0 else "in the opposite direction"
        setup = f"{obj2} (mass {m2} kg), moving at {abs(u2)} m/s {dir2}"
    if v1 == v2:
        outcome = f"the two move off together at {v1} m/s"
    else:
        outcome = f"{obj1} continues at {v1} m/s and {obj2} moves off at {v2} m/s"
    question_text = (
        f"{_cap(obj1)} of mass {m1} kg moving at {u1} m/s collides with {setup}. "
        f"After the collision {outcome}.\n\nDetermine, by calculation, whether the "
        f"collision is elastic or inelastic."
    )
    correct = (
        f"Elastic — Ek(before) = {ek_before} J and Ek(after) = {ek_after} J are equal."
        if is_elastic else
        f"Inelastic — Ek(before) = {ek_before} J is greater than Ek(after) = {ek_after} J."
    )
    before_terms = (
        rf"\tfrac{{1}}{{2}} \times {m1} \times {u1}^2"
        if u2 == 0 else
        rf"(\tfrac{{1}}{{2}} \times {m1} \times {u1}^2) + (\tfrac{{1}}{{2}} \times {m2} \times {u2}^2)"
    )
    working = [
        {"type": "latex", "content": rf"E_k(\text{{before}}) = {before_terms} = {ek_before}\ \mathrm{{J}}"},
        {"type": "latex", "content": rf"E_k(\text{{after}}) = (\tfrac{{1}}{{2}} \times {m1} \times {v1}^2) + (\tfrac{{1}}{{2}} \times {m2} \times {v2}^2) = {ek_after}\ \mathrm{{J}}"},
    ]
    distractors = [
        {"value": "Elastic — momentum is conserved, and momentum is always conserved in a collision." if not is_elastic
                   else "Inelastic — the two objects have different masses, so kinetic energy cannot be conserved.",
         "mistake": "Whether a collision is elastic or inelastic is decided by comparing total kinetic energy "
                    "before and after, not by momentum (which is always conserved) or by whether the masses differ.",
         "working": working},
        {"value": f"Inelastic — Ek(before) = {ek_before} J is greater than Ek(after) = {ek_after} J." if is_elastic
                   else f"Elastic — Ek(before) = {ek_before} J and Ek(after) = {ek_after} J are equal.",
         "mistake": f"Check the kinetic energy calculation: Ek(before) = {ek_before} J, Ek(after) = {ek_after} J.",
         "working": working},
    ]
    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)

    widget_mode = "stick" if collision_type in ("stick_stationary", "stick_moving") else "separate"
    return _with_collisions_widget(PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        distractors=distractors,
        working=working,
        notes=_NOTES,
        topic="Our Dynamic Universe",
        question_type="Momentum and Impulse",
        level=level,
        metadata={"type": "classification", "options": options},
    ), widget_mode)


def gen_ke_lost(level="Higher"):
    """Numeric counterpart to gen_elastic_inelastic's classification questions —
    calculate the actual kinetic energy lost in a sticking collision, rather
    than just identifying elastic/inelastic. Target may be stationary or
    (head-on) already moving, matching both variants on the worksheet."""
    m1 = round(random.uniform(0.3, 2.0), 2)
    m2 = round(random.uniform(0.3, 2.0), 2)
    u1 = round(random.uniform(2.0, 6.0), 1)

    head_on = random.choice([True, False])
    if head_on:
        opposite = random.choice([True, False])
        # keep enough relative speed between the two that the collision has a
        # real (and never rounding-noise-sized) kinetic energy loss
        u2_mag = round(random.uniform(0.5, 3.0), 1)
        while not opposite and abs(u1 - u2_mag) < 1.0:
            u2_mag = round(random.uniform(0.5, 3.0), 1)
        u2 = u2_mag * (-1 if opposite else 1)
    else:
        u2 = 0.0

    kind_name = _pick_kind(_SMALL_KINDS)[0]
    obj1, obj2 = f"{kind_name} A", f"{kind_name} B"

    total_p = _r2(m1 * u1 + m2 * u2)
    total_mass = round(m1 + m2, 3)
    v_exact = total_p / total_mass
    v = _r2(v_exact)

    # Use the unrounded common velocity for the energy comparison so 2-d.p.
    # rounding of v can never flip Ek(after) above Ek(before).
    ek_before = _r2(0.5 * m1 * u1 ** 2 + 0.5 * m2 * u2 ** 2)
    ek_after = _r2(0.5 * total_mass * v_exact ** 2)
    loss = _r2(max(ek_before - ek_after, 0.0))

    if u2 == 0:
        setup = f"a stationary {obj2} of mass {m2} kg"
    else:
        dir2 = "in the same direction" if u2 > 0 else "in the opposite direction"
        setup = f"{obj2} (mass {m2} kg), moving at {abs(u2)} m/s {dir2}"

    question = (
        f"{_cap(obj1)} of mass {m1} kg, moving at {u1} m/s, collides with {setup}. "
        f"The two stick together after the collision. Calculate the kinetic energy "
        f"lost in this collision."
    )
    before_terms = (
        rf"\tfrac{{1}}{{2}} \times {m1} \times {u1}^2"
        if u2 == 0 else
        rf"(\tfrac{{1}}{{2}} \times {m1} \times {u1}^2) + (\tfrac{{1}}{{2}} \times {m2} \times {u2}^2)"
    )
    working = [
        {"type": "text",  "content": "Find the common velocity from conservation of momentum:"},
        {"type": "latex", "content": r"m_1u_1 + m_2u_2 = (m_1 + m_2)v"},
        {"type": "latex", "content": rf"({m1} \times {u1}) + ({m2} \times {u2}) = ({total_mass})v"},
        {"type": "latex", "content": rf"v = {v}\ \mathrm{{m/s}}"},
        {"type": "text",  "content": "Compare kinetic energy before and after:"},
        {"type": "latex", "content": rf"E_k(\text{{before}}) = {before_terms} = {ek_before}\ \mathrm{{J}}"},
        {"type": "latex", "content": rf"E_k(\text{{after}}) = \tfrac{{1}}{{2}} \times {total_mass} \times {v}^2 = {ek_after}\ \mathrm{{J}}"},
        {"type": "latex", "content": rf"\text{{loss}} = {ek_before} - {ek_after} = {loss}\ \mathrm{{J}}"},
    ]
    options_data = [
        {"value": loss, "mistake": None, "working": working},
        {"value": ek_after, "mistake": "This is the kinetic energy remaining after the collision, not the amount lost.", "working": working},
        {"value": ek_before, "mistake": "This is the kinetic energy before the collision — you need to subtract Ek(after) to find the loss.", "working": working},
    ]
    scaffold = [
        {"question": "What is the common velocity v after the collision (m/s)?", "answer": v},
        {"question": "What is Ek before the collision (J)?", "answer": ek_before},
        {"question": "What is Ek after the collision (J)?", "answer": ek_after},
        {"question": "What is the kinetic energy lost (J)?", "answer": loss},
    ]
    return _with_collisions_widget(make_question(question, loss, options_data, "J", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Momentum and Impulse", level=level), "stick")


_ALL_GENS = [
    gen_p_from_mv, gen_v_from_pm, gen_m_from_pv,
    gen_stick_together, gen_separate, gen_explosion,
    gen_impulse_find_f, gen_impulse_find_t, gen_impulse_graph,
    gen_elastic_inelastic, gen_ke_lost,
]


def generate_momentum_impulse(level="Higher"):
    return random.choice(_ALL_GENS)(level=level)
