import random
import math
from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

G = 9.8

_NOTES = """
## Energy, Work and Power

**Definitions:**
- Work done is the energy transferred when a force moves an object through a distance.
- Power is the rate at which energy is transferred.

$$E_W = Fd$$
$$E_p = mgh$$
$$E_k = \\frac{1}{2}mv^2$$
$$P = \\frac{E}{t}$$

| Symbol | Quantity | Unit |
|---|---|---|
| $E_W$ | Work done | J |
| $E_p$ | Gravitational potential energy | J |
| $E_k$ | Kinetic energy | J |
| P | Power | W |
| F | Force | N |
| d | Distance | m |
| m | Mass | kg |
| g | Gravitational field strength (= 9.8 m/s²) | N/kg |
| h | Height | m |
| v | Velocity | m/s |
| E | Energy transferred | J |
| t | Time | s |

> **Important:** In a conservation-of-energy problem, energy converts from one form to
> another. Any energy that "goes missing" between two points has been lost, usually to
> friction, and that lost energy equals the work done against the resistive force. At
> constant speed, useful power = energy transferred ÷ time; for something moving
> horizontally against a resistive force at constant speed, P = Fv.
"""


def _r2(val):
    return round(float(val), 2)


def round_sf(value, sf=3):
    value = float(value)
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def fmt_num(value):
    """Human-readable number for question text: avoids Python's '1.92e+07' style."""
    value = float(value)
    if abs(value) >= 1e5 or (0 < abs(value) < 1e-3):
        s = f"{value:.3e}"
        mantissa, exp = s.split("e")
        mantissa = mantissa.rstrip("0").rstrip(".")
        exp_i = int(exp)
        return f"{mantissa} × 10{str(exp_i).translate(_SUP)}"
    if value == int(value):
        return f"{int(value)}"
    return f"{value:g}"


_WORK_CONTEXTS = ["porter", "removal worker", "rower", "crane", "tug", "forklift driver"]

# (context, power_lo_W, power_hi_W) — power is tied to a plausible rating for that device.
_POWER_KINDS = [
    ("kettle", 1800, 3000),
    ("immersion heater", 2000, 3500),
    ("motor", 200, 5000),
    ("winch", 500, 4000),
    ("pump", 300, 2500),
    ("television", 60, 200),
]

def _pick_mass(lo_kg, hi_kg, allow_grams=True):
    """Occasionally present the mass in grams, matching the worksheet's own style."""
    if allow_grams and lo_kg < 1 and random.random() < 0.4:
        m_g = random.randint(max(1, int(lo_kg * 1000)), int(hi_kg * 1000))
        return m_g / 1000, "g", m_g, True
    dp = 1 if hi_kg < 100 else 0
    m_kg = round(random.uniform(lo_kg, hi_kg), dp)
    if dp == 0:
        m_kg = int(m_kg)
    return m_kg, "kg", m_kg, False


# ── Section 1: Work Done (EW = Fd) ───────────────────────────────────────────

def gen_work_find_ew(level="Higher"):
    F = random.randint(20, 900)
    d = random.randint(10, 300)
    ew = F * d
    ctx = random.choice(_WORK_CONTEXTS)

    question = f"A {ctx} applies an average force of {F} N over a distance of {d} m. Calculate the work done."
    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"E_W = Fd"},
        {"type": "latex", "content": rf"E_W = {F} \times {d}"},
        {"type": "latex", "content": rf"E_W = {ew}\ \mathrm{{J}}"},
    ]
    options_data = [
        {"value": float(ew), "mistake": None, "working": working},
        {"value": round_sf(F / d), "mistake": "You divided F by d instead of multiplying. EW = Fd.", "working": working},
        {"value": float(F + d), "mistake": "Work done is the product of force and distance, not their sum. EW = Fd.", "working": working},
    ]
    return make_question(question, float(ew), options_data, "J",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_work_find_f(level="Higher"):
    F = random.randint(20, 900)
    d = random.randint(10, 300)
    ew = F * d
    ctx = random.choice(_WORK_CONTEXTS)

    question = f"A {ctx} does {ew} J of work moving an object a distance of {d} m. Calculate the force applied."
    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"E_W = Fd"},
        {"type": "latex", "content": rf"{ew} = F \times {d}"},
        {"type": "latex", "content": rf"F = \frac{{{ew}}}{{{d}}} = {F}\ \mathrm{{N}}"},
    ]
    options_data = [
        {"value": float(F), "mistake": None, "working": working},
        {"value": float(ew * d), "mistake": "You multiplied EW by d instead of dividing. F = EW ÷ d.", "working": working},
        {"value": round_sf(d / ew), "mistake": "You divided the wrong way round. F = EW ÷ d.", "working": working},
    ]
    return make_question(question, float(F), options_data, "N",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_work_find_d(level="Higher"):
    F = random.randint(20, 900)
    d = random.randint(10, 300)
    ew = F * d
    ctx = random.choice(_WORK_CONTEXTS)

    question = f"A {ctx} applies a force of {F} N, doing {ew} J of work. Calculate the distance moved."
    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"E_W = Fd"},
        {"type": "latex", "content": rf"{ew} = {F} \times d"},
        {"type": "latex", "content": rf"d = \frac{{{ew}}}{{{F}}} = {d}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": float(d), "mistake": None, "working": working},
        {"value": float(ew * F), "mistake": "You multiplied EW by F instead of dividing. d = EW ÷ F.", "working": working},
        {"value": round_sf(F / ew), "mistake": "You divided the wrong way round. d = EW ÷ F.", "working": working},
    ]
    return make_question(question, float(d), options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def generate_work_done(level="Higher"):
    return random.choice([gen_work_find_ew, gen_work_find_f, gen_work_find_d])(level=level)


# ── Section 2: Power (P = E/t) ────────────────────────────────────────────────

_TIME_UNITS = [("s", 1), ("minutes", 60), ("hours", 3600)]


def _pick_time():
    unit, factor = random.choices(_TIME_UNITS, weights=[3, 2, 1])[0]
    if unit == "s":
        t_disp = random.randint(10, 300)
    elif unit == "minutes":
        t_disp = random.choice([1, 2, 3, 4, 5, 10, 15, 20, 30])
    else:
        t_disp = random.choice([1, 2, 3])
    return t_disp, unit, t_disp * factor


def gen_power_find_p(level="Higher"):
    ctx, p_lo, p_hi = random.choice(_POWER_KINDS)
    t_disp, unit, t_s = _pick_time()
    P_true = round_sf(random.uniform(p_lo, p_hi))
    E = round_sf(P_true * t_s)
    P = round_sf(E / t_s)

    question = f"A {ctx} transfers {fmt_num(E)} J of energy in {t_disp} {unit}. Calculate the power."
    working = []
    if unit != "s":
        working.append({"type": "text", "content": f"Convert the time to seconds: {t_disp} {unit} = {t_s} s"})
    working += [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "latex", "content": rf"P = \frac{{{fmt_num(E)}}}{{{t_s}}}"},
        {"type": "latex", "content": rf"P = {P}\ \mathrm{{W}}"},
    ]
    options_data = [
        {"value": P, "mistake": None, "working": working},
        {"value": round_sf(E * t_s), "mistake": "You multiplied E by t instead of dividing. P = E ÷ t.", "working": working},
        {"value": round_sf(t_s / E) if E else 0.0, "mistake": "You divided the wrong way round. P = E ÷ t.", "working": working},
    ]
    scaffold = None
    if unit != "s":
        scaffold = [
            {"question": "What is the time in seconds?", "answer": float(t_s)},
            {"question": "What is the power P?", "answer": P},
        ]
    return make_question(question, P, options_data, "W", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_power_find_e(level="Higher"):
    ctx, p_lo, p_hi = random.choice(_POWER_KINDS)
    t_disp, unit, t_s = _pick_time()
    P = round_sf(random.uniform(p_lo, p_hi))
    E = round_sf(P * t_s)

    question = f"A {ctx} has a power rating of {P:g} W. Calculate the energy it transfers in {t_disp} {unit}."
    working = []
    if unit != "s":
        working.append({"type": "text", "content": f"Convert the time to seconds: {t_disp} {unit} = {t_s} s"})
    working += [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "latex", "content": rf"{P:g} = \frac{{E}}{{{t_s}}}"},
        {"type": "latex", "content": rf"E = {P:g} \times {t_s} = {E}\ \mathrm{{J}}"},
    ]
    options_data = [
        {"value": E, "mistake": None, "working": working},
        {"value": round_sf(P / t_s), "mistake": "You divided P by t instead of multiplying. E = Pt.", "working": working},
    ]
    scaffold = None
    if unit != "s":
        scaffold = [
            {"question": "What is the time in seconds?", "answer": float(t_s)},
            {"question": "What is the energy E?", "answer": E},
        ]
    return make_question(question, E, options_data, "J", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_power_find_t(level="Higher"):
    ctx = random.choice(["student climbing a flight of stairs", "hiker climbing a hill", "cyclist climbing a hill"])
    P = round_sf(random.uniform(100, 400))
    E = round_sf(random.uniform(500, 6000))
    t_s = round_sf(E / P)

    question = f"A {ctx} does {E:g} J of work. If they have a power output of {P:g} W, calculate the time taken."
    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "latex", "content": rf"{P:g} = \frac{{{E:g}}}{{t}}"},
        {"type": "latex", "content": rf"t = \frac{{{E:g}}}{{{P:g}}} = {t_s}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t_s, "mistake": None, "working": working},
        {"value": round_sf(E * P), "mistake": "You multiplied E by P instead of dividing. t = E ÷ P.", "working": working},
    ]
    return make_question(question, t_s, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def generate_power(level="Higher"):
    return random.choice([gen_power_find_p, gen_power_find_e, gen_power_find_t])(level=level)


# ── Section 3: Conservation of Energy ────────────────────────────────────────

# (description, lands_on, mass_lo_kg, mass_hi_kg, height_lo_m, height_hi_m)
_FALL_KINDS = [
    ("A stone is dropped from a bridge", "the water", 0.1, 0.9, 5, 40),
    ("A ball is dropped from the top of a building", "the ground", 0.05, 0.6, 5, 30),
    ("A diver steps off a diving board", "the water", 45, 90, 3, 10),
    ("A coconut falls from a palm tree", "the ground", 0.8, 2.5, 5, 20),
]

# (description, mass_lo_kg, mass_hi_kg, speed_lo_ms, speed_hi_ms)
_RISE_KINDS = [
    ("A ball is thrown vertically upwards", 0.05, 0.6, 5, 20),
    ("An arrow is fired vertically upwards", 0.02, 0.08, 20, 60),
    ("A skateboarder rolls up a ramp", 40, 85, 3, 8),
    ("A pendulum bob swings up from its lowest point", 0.1, 2.0, 1, 4),
]


def _conservation_mass(lo_kg, hi_kg):
    """Mass for an Ep ⇄ Ek question: light objects are often given in grams
    (never rounded to zero); heavier ones in kg."""
    if hi_kg < 1:
        m_g = random.randint(int(lo_kg * 1000), int(hi_kg * 1000))
        if random.random() < 0.5:
            return m_g, "g", m_g / 1000
        return m_g / 1000, "kg", m_g / 1000
    m_kg = round(random.uniform(lo_kg, hi_kg), 1 if hi_kg < 10 else 0)
    return m_kg, "kg", m_kg


def _fall_question(level):
    desc, lands_on, m_lo, m_hi, h_lo, h_hi = random.choice(_FALL_KINDS)
    disp_m, unit, m_kg = _conservation_mass(m_lo, m_hi)
    h = round(random.uniform(h_lo, h_hi), 1)
    ep = round_sf(m_kg * G * h)
    v = round_sf(math.sqrt(2 * ep / m_kg))

    question = (
        f"{desc}. Its mass is {disp_m:g} {unit} and it falls through a height of {h} m. "
        f"Assuming no energy is lost to air resistance, calculate its speed just before it "
        f"hits {lands_on}."
    )
    working = []
    if unit == "g":
        working.append({"type": "text", "content": f"Convert the mass: {disp_m:g} g = {m_kg:g} kg"})
    working += [
        {"type": "text",  "content": "Calculate the gravitational potential energy lost:"},
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"E_p = {m_kg:g} \times 9.8 \times {h}"},
        {"type": "latex", "content": rf"E_p = {ep:g}\ \mathrm{{J}}"},
        {"type": "text",  "content": "No energy is lost, so all the Ep lost becomes Ek gained:"},
        {"type": "latex", "content": rf"E_k = {ep:g}\ \mathrm{{J}}"},
        {"type": "latex", "content": r"E_k = \tfrac{1}{2}mv^2"},
        {"type": "latex", "content": rf"{ep:g} = \tfrac{{1}}{{2}} \times {m_kg:g} \times v^2"},
        {"type": "latex", "content": rf"v = {v:g}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v, "mistake": None, "working": working},
        {"value": round_sf(math.sqrt(ep / m_kg)), "mistake": "You forgot the ½ in Ek = ½mv².", "working": working},
        {"value": round_sf(2 * ep / m_kg), "mistake": "You found v² — take the square root to find v.", "working": working},
        {"value": round_sf(math.sqrt(2 * ep)), "mistake": "You forgot to divide by the mass when solving ½mv² = Ek.", "working": working},
    ]
    scaffold = [
        {"question": "What is the gravitational potential energy lost, Ep = mgh?", "answer": ep},
        {"question": "What is the kinetic energy gained, Ek?", "answer": ep},
        {"question": "Use Ek = ½mv² to find the speed v.", "answer": v},
    ]
    return make_question(question, v, options_data, "m/s", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def _rise_question(level):
    desc, m_lo, m_hi, v_lo, v_hi = random.choice(_RISE_KINDS)
    disp_m, unit, m_kg = _conservation_mass(m_lo, m_hi)
    v = round(random.uniform(v_lo, v_hi), 1)
    ek = round_sf(0.5 * m_kg * v ** 2)
    h = round_sf(ek / (m_kg * G))

    question = (
        f"{desc} with a speed of {v} m/s. Its mass is {disp_m:g} {unit}. Assuming no energy "
        f"is lost, calculate the maximum height it rises through."
    )
    working = []
    if unit == "g":
        working.append({"type": "text", "content": f"Convert the mass: {disp_m:g} g = {m_kg:g} kg"})
    working += [
        {"type": "text",  "content": "Calculate the kinetic energy at the start:"},
        {"type": "latex", "content": r"E_k = \tfrac{1}{2}mv^2"},
        {"type": "latex", "content": rf"E_k = \tfrac{{1}}{{2}} \times {m_kg:g} \times {v}^2"},
        {"type": "latex", "content": rf"E_k = {ek:g}\ \mathrm{{J}}"},
        {"type": "text",  "content": "At maximum height all the Ek has become Ep:"},
        {"type": "latex", "content": rf"E_p = {ek:g}\ \mathrm{{J}}"},
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"{ek:g} = {m_kg:g} \times 9.8 \times h"},
        {"type": "latex", "content": rf"h = {h:g}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": h, "mistake": None, "working": working},
        {"value": round_sf(2 * ek / (m_kg * G)), "mistake": "You forgot the ½ in Ek = ½mv².", "working": working},
        {"value": round_sf(0.5 * m_kg * v / (m_kg * G)), "mistake": "You forgot to square the speed in Ek = ½mv².", "working": working},
        {"value": round_sf(ek / G), "mistake": "You forgot to divide by the mass when solving mgh = Ep.", "working": working},
    ]
    scaffold = [
        {"question": "What is the kinetic energy at the start, Ek = ½mv²?", "answer": ek},
        {"question": "What is the gravitational potential energy at maximum height, Ep?", "answer": ek},
        {"question": "Use Ep = mgh to find the height h.", "answer": h},
    ]
    return make_question(question, h, options_data, "m", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_energy_ep_ek(level="Higher"):
    """Ep ⇄ Ek with no losses. A mass is always given: students calculate one
    type of energy, then substitute that value into the other energy equation
    (rather than cancelling m algebraically)."""
    gen = random.choice([_fall_question, _rise_question])
    for _ in range(20):
        q = gen(level)
        vals = [round(float(d["value"]), 6) for d in q.distractors]
        if len(vals) == 3 and len(set(vals)) == 3:
            break
    return q


_SLOPE_OBJECTS = ["go-kart", "sledge", "toboggan", "trolley", "skateboarder"]


def gen_energy_friction_force(level="Higher"):
    m_kg = round(random.uniform(20, 200), 0)
    h = round(random.uniform(2.0, 6.0), 1)
    d = round(random.uniform(15, 35), 0)
    v_max = round_sf(math.sqrt(2 * G * h)) * 0.85
    v = round(random.uniform(max(1.0, v_max * 0.5), v_max), 1)

    ep = round_sf(m_kg * G * h)
    ek = round_sf(0.5 * m_kg * v ** 2)
    energy_lost = round_sf(ep - ek)
    F = round_sf(energy_lost / d)

    obj = random.choice(_SLOPE_OBJECTS)
    context = (
        f"A {obj} of mass {m_kg:g} kg free-wheels down a slope from rest. It starts at a "
        f"height of {h} m above the bottom of the slope and reaches a speed of {v} m/s at "
        f"the bottom, having travelled {d:g} m along the slope."
    )

    working_a = [
        {"type": "latex", "content": rf"E_p = mgh = {m_kg:g} \times 9.8 \times {h} = {ep}\ \mathrm{{J}}"},
        {"type": "latex", "content": rf"E_k = \tfrac{{1}}{{2}}mv^2 = \tfrac{{1}}{{2}} \times {m_kg:g} \times {v}^2 = {ek}\ \mathrm{{J}}"},
        {"type": "latex", "content": rf"\text{{energy lost}} = {ep} - {ek} = {energy_lost}\ \mathrm{{J}}"},
    ]
    part_a = PhysicsQuestion(
        question_text="Calculate the energy lost to friction as it travels down the slope.",
        correct_answer=energy_lost, unit="J",
        topic="Our Dynamic Universe", question_type="Energy, Work and Power", level=level,
        working=working_a,
        distractors=[
            {"value": ep, "mistake": "This is the gravitational potential energy at the top, not the energy lost. Energy lost = Ep − Ek.", "working": working_a},
            {"value": ek, "mistake": "This is the kinetic energy at the bottom, not the energy lost. Energy lost = Ep − Ek.", "working": working_a},
        ],
        notes=_NOTES,
        scaffold=[
            {"prompt": "What is Ep at the top of the slope?", "answer": ep},
            {"prompt": "What is Ek at the bottom of the slope?", "answer": ek},
            {"prompt": "What is the energy lost to friction?", "answer": energy_lost},
        ],
    )

    working_b = [
        {"type": "text",  "content": "The work done against friction equals the energy lost:"},
        {"type": "latex", "content": r"E_W = Fd"},
        {"type": "latex", "content": rf"{energy_lost} = F \times {d:g}"},
        {"type": "latex", "content": rf"F = {F}\ \mathrm{{N}}"},
    ]
    part_b = PhysicsQuestion(
        question_text="Calculate the average frictional force acting on it as it travels down the slope.",
        correct_answer=F, unit="N",
        topic="Our Dynamic Universe", question_type="Energy, Work and Power", level=level,
        working=working_b,
        distractors=[
            {"value": round_sf(energy_lost * d), "mistake": "You multiplied instead of dividing. F = (energy lost) ÷ d.", "working": working_b},
            {"value": round_sf(ep / d), "mistake": "Use the energy lost to friction (Ep − Ek), not Ep alone.", "working": working_b},
        ],
        notes=_NOTES,
    )

    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Energy, Work and Power", level=level,
        is_scenario=True, scenario_context=context, parts=[part_a, part_b],
    )


# ── Section 4: Conservation — Power (P = energy change ÷ time) ──────────────
#
# All of these situations reduce to the same idea — average power is the
# energy transferred divided by the time taken — but WHICH energy change is
# occurring is different every time: a gain in Ep, a gain or loss of Ek, work
# done against friction, or some combination. The scaffold's first step is
# always to identify and calculate that energy change before dividing by time.

_ACCEL_CONTEXTS = ["car", "van", "train", "motorbike"]
_ENGINE_CONTEXTS = ["delivery van", "lorry", "car", "tractor"]
_LIFT_CONTEXTS = ["goods lift", "escalator", "chairlift", "hoist", "crane"]
_SLOPE_VEHICLE_CONTEXTS = ["bus", "lorry", "car", "cyclist", "van"]


def _accel_mass(ctx):
    return random.randint(150, 300) if ctx == "motorbike" else random.randint(800, 5000)


def _power_lift(level):
    ctx = random.choice(_LIFT_CONTEXTS)
    m_kg = round(random.uniform(40, 120), 0)
    h = round(random.uniform(2.0, 10.0), 1)
    t = round(random.uniform(8, 25), 0)
    ep = round_sf(m_kg * G * h)
    P = round_sf(ep / t)

    question = (
        f"A {ctx} carries a load of mass {m_kg:g} kg through a vertical height of {h} m in "
        f"a time of {t:g} s, moving at constant speed. Calculate the useful power developed."
    )
    working = [
        {"type": "text",  "content": "The energy change here is a gain in gravitational potential energy:"},
        {"type": "latex", "content": rf"E_p = mgh = {m_kg:g} \times 9.8 \times {h} = {ep}\ \mathrm{{J}}"},
        {"type": "text",  "content": "Average power = energy change ÷ time:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "latex", "content": rf"P = \frac{{{ep}}}{{{t:g}}}"},
        {"type": "latex", "content": rf"P = {P}\ \mathrm{{W}}"},
    ]
    options_data = [
        {"value": P, "mistake": None, "working": working},
        {"value": round_sf(ep * t), "mistake": "You multiplied Ep by t instead of dividing. P = Ep ÷ t.", "working": working},
        {"value": round_sf(m_kg * G / t), "mistake": "You left out the height h when calculating Ep. Ep = mgh.", "working": working},
    ]
    scaffold = [
        {"question": "The energy change here is a gain in gravitational potential energy. What is Ep?", "answer": ep},
        {"question": "What is the average power, P = (energy change) ÷ time?", "answer": P},
    ]
    return make_question(question, P, options_data, "W", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def _power_engine(level):
    ctx = random.choice(_ENGINE_CONTEXTS)
    F = random.randint(400, 2500)
    d = round(random.uniform(200, 1000), 0)
    t = round(random.uniform(15, 60), 0)
    ew = round_sf(F * d)
    P = round_sf(ew / t)

    question = (
        f"A {ctx}'s engine produces a driving force of {F} N. The {ctx} travels {d:g} m "
        f"along a level road in {t:g} s at a constant speed. Calculate the average power "
        f"developed by the engine."
    )
    working = [
        {"type": "text",  "content": "At constant speed, the energy change here is the work done against the resistive forces:"},
        {"type": "latex", "content": rf"E_W = Fd = {F} \times {d:g} = {ew}\ \mathrm{{J}}"},
        {"type": "text",  "content": "Average power = energy change ÷ time:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "latex", "content": rf"P = \frac{{{ew}}}{{{t:g}}}"},
        {"type": "latex", "content": rf"P = {P}\ \mathrm{{W}}"},
    ]
    options_data = [
        {"value": P, "mistake": None, "working": working},
        {"value": round_sf(ew * t), "mistake": "You multiplied Ew by t instead of dividing. P = Ew ÷ t.", "working": working},
        {"value": round_sf(F / t), "mistake": "You left out the distance d when calculating Ew. Ew = Fd.", "working": working},
    ]
    scaffold = [
        {"question": "At constant speed, the energy change here is the work done against the resistive forces. What is Ew = Fd?", "answer": ew},
        {"question": "What is the average power, P = (energy change) ÷ time?", "answer": P},
    ]
    return make_question(question, P, options_data, "W", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def _power_accelerate(level):
    ctx = random.choice(_ACCEL_CONTEXTS)
    m_kg = _accel_mass(ctx)
    from_rest = random.random() < 0.5
    u = 0.0 if from_rest else round(random.uniform(2, 8), 1)
    v = round(random.uniform(u + 5, u + 25), 1)
    t = round(random.uniform(5, 30), 0)
    ek_i = round_sf(0.5 * m_kg * u ** 2)
    ek_f = round_sf(0.5 * m_kg * v ** 2)
    delta_ek = round_sf(ek_f - ek_i)
    P = round_sf(delta_ek / t)

    if from_rest:
        question = (
            f"A {ctx} of mass {m_kg} kg accelerates from rest to a speed of {v} m/s in "
            f"{t:g} s. Calculate the average power developed by the engine."
        )
    else:
        question = (
            f"A {ctx} of mass {m_kg} kg accelerates from {u} m/s to {v} m/s in {t:g} s. "
            f"Calculate the average power developed by the engine."
        )
    working = [{"type": "text", "content": "The energy change here is a gain in kinetic energy:"}]
    if not from_rest:
        working.append({"type": "latex", "content": rf"E_{{k,i}} = \tfrac{{1}}{{2}}mu^2 = \tfrac{{1}}{{2}} \times {m_kg} \times {u}^2 = {ek_i}\ \mathrm{{J}}"})
    working += [
        {"type": "latex", "content": rf"E_{{k,f}} = \tfrac{{1}}{{2}}mv^2 = \tfrac{{1}}{{2}} \times {m_kg} \times {v}^2 = {ek_f}\ \mathrm{{J}}"},
        {"type": "latex", "content": rf"\Delta E_k = {ek_f} - {ek_i} = {delta_ek}\ \mathrm{{J}}"},
        {"type": "text",  "content": "Average power = energy change ÷ time:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "latex", "content": rf"P = \frac{{{delta_ek}}}{{{t:g}}}"},
        {"type": "latex", "content": rf"P = {P}\ \mathrm{{W}}"},
    ]
    options_data = [
        {"value": P, "mistake": None, "working": working},
        {"value": round_sf(ek_f / t), "mistake": "You used the final kinetic energy only. You must use the change in kinetic energy: P = ΔEk ÷ t.", "working": working},
        {"value": round_sf(delta_ek * t), "mistake": "You multiplied ΔEk by t instead of dividing. P = ΔEk ÷ t.", "working": working},
    ]
    scaffold = [
        {"question": "The energy change here is a gain in kinetic energy. What is ΔEk?", "answer": delta_ek},
        {"question": "What is the average power, P = (energy change) ÷ time?", "answer": P},
    ]
    return make_question(question, P, options_data, "W", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def _power_decelerate(level):
    ctx = random.choice(_ACCEL_CONTEXTS)
    m_kg = _accel_mass(ctx)
    v = round(random.uniform(15, 35), 1)
    stops = random.random() < 0.6
    u = 0.0 if stops else round(random.uniform(2, v - 5), 1)
    t = round(random.uniform(3, 15), 0)
    ek_i = round_sf(0.5 * m_kg * v ** 2)
    ek_f = round_sf(0.5 * m_kg * u ** 2)
    delta_ek = round_sf(ek_i - ek_f)
    P = round_sf(delta_ek / t)

    if stops:
        question = (
            f"A {ctx} of mass {m_kg} kg travelling at {v} m/s brakes to rest in {t:g} s. "
            f"Calculate the average power dissipated by the brakes."
        )
    else:
        question = (
            f"A {ctx} of mass {m_kg} kg decelerates from {v} m/s to {u} m/s in {t:g} s. "
            f"Calculate the average power dissipated by the brakes."
        )
    working = [
        {"type": "text",  "content": "The energy change here is a loss in kinetic energy (dissipated as heat by the brakes):"},
        {"type": "latex", "content": rf"E_{{k,i}} = \tfrac{{1}}{{2}}mv^2 = \tfrac{{1}}{{2}} \times {m_kg} \times {v}^2 = {ek_i}\ \mathrm{{J}}"},
    ]
    if not stops:
        working.append({"type": "latex", "content": rf"E_{{k,f}} = \tfrac{{1}}{{2}}mu^2 = \tfrac{{1}}{{2}} \times {m_kg} \times {u}^2 = {ek_f}\ \mathrm{{J}}"})
    working += [
        {"type": "latex", "content": rf"\Delta E_k = {ek_i} - {ek_f} = {delta_ek}\ \mathrm{{J}}"},
        {"type": "text",  "content": "Average power = energy change ÷ time:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "latex", "content": rf"P = \frac{{{delta_ek}}}{{{t:g}}}"},
        {"type": "latex", "content": rf"P = {P}\ \mathrm{{W}}"},
    ]
    options_data = [
        {"value": P, "mistake": None, "working": working},
        {"value": round_sf(ek_i / t), "mistake": "You used the initial kinetic energy only. You must use the loss in kinetic energy: P = ΔEk ÷ t.", "working": working},
        {"value": round_sf(delta_ek * t), "mistake": "You multiplied ΔEk by t instead of dividing. P = ΔEk ÷ t.", "working": working},
    ]
    scaffold = [
        {"question": "The energy change here is a loss in kinetic energy. What is ΔEk?", "answer": delta_ek},
        {"question": "What is the average power dissipated, P = (energy change) ÷ time?", "answer": P},
    ]
    return make_question(question, P, options_data, "W", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def _power_hydro(level):
    is_dam = random.random() < 0.5
    h = round(random.uniform(15, 300), 0)
    rate_s = round_sf(random.uniform(1e4, 5e8))
    use_minutes = random.random() < 0.5
    unit_label = "minute" if use_minutes else "second"
    rate_disp = round_sf(rate_s * 60) if use_minutes else rate_s
    P = round_sf(rate_s * G * h)

    if is_dam:
        question = (
            f"Water flows through a hydroelectric dam at a rate of {fmt_num(rate_disp)} kg "
            f"per {unit_label}.\nThe water falls through a height of {h:g} m before reaching "
            f"the turbines.\nCalculate the total power delivered by the falling water."
        )
    else:
        question = (
            f"Water flows at a rate of {fmt_num(rate_disp)} kg per {unit_label} over a "
            f"waterfall.\nThe height of the waterfall is {h:g} m.\nCalculate the total power "
            f"delivered by the water in falling through the {h:g} m."
        )

    working = []
    if use_minutes:
        working.append({"type": "text", "content": f"Convert the flow rate to kg/s: {fmt_num(rate_disp)} kg/min ÷ 60 = {fmt_num(rate_s)} kg/s"})
    working += [
        {"type": "text",  "content": "The energy change here is the gravitational potential energy lost by the mass of water falling each second:"},
        {"type": "latex", "content": rf"E_p = mgh = {fmt_num(rate_s)} \times 9.8 \times {h:g} = {fmt_num(P)}\ \mathrm{{J}}"},
        {"type": "text",  "content": "Average power = energy change ÷ time (here, per 1 s):"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "latex", "content": rf"P = \frac{{{fmt_num(P)}}}{{1}} = {fmt_num(P)}\ \mathrm{{W}}"},
    ]
    options_data = [{"value": P, "mistake": None, "working": working}]
    if use_minutes:
        options_data.append({
            "value": round_sf(rate_disp * G * h),
            "mistake": f"You used the flow rate in kg per minute without converting to kg per second. {fmt_num(rate_disp)} kg/min ÷ 60 = {fmt_num(rate_s)} kg/s.",
            "working": working,
        })
    options_data += [
        {"value": round_sf(rate_s * h), "mistake": "You left out g. P = (m/t) × g × h.", "working": working},
        {"value": round_sf(rate_s * G), "mistake": "You left out the height h. P = (m/t) × g × h.", "working": working},
    ]
    scaffold = [
        {"question": "The energy change here is the gravitational potential energy lost by the water falling each second. What is Ep = mgh, using the flow rate in kg per second?", "answer": P},
        {"question": "What is the total power delivered, P = (energy change) ÷ time?", "answer": P},
    ]
    return make_question(question, P, options_data, "W", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def _power_slope(level):
    ctx = random.choice(_SLOPE_VEHICLE_CONTEXTS)
    if ctx == "cyclist":
        m_kg = random.randint(70, 100)
        f_friction = random.randint(20, 80)
        d_km = round(random.uniform(0.3, 1.5), 2)
        h = round(random.uniform(20, 80), 0)
        t_min = round(random.uniform(3, 12), 0)
    else:
        m_kg = random.randint(1000, 12000)
        f_friction = random.randint(400, 2000)
        d_km = round(random.uniform(0.5, 3), 2)
        h = round(random.uniform(80, 400), 0)
        t_min = round(random.uniform(10, 30), 0)

    d_m = round_sf(d_km * 1000)
    t_s = t_min * 60
    ep = round_sf(m_kg * G * h)
    work_friction = round_sf(f_friction * d_m)
    total_work = round_sf(ep + work_friction)
    P = round_sf(total_work / t_s)

    question = (
        f"A {ctx} of mass {m_kg:g} kg climbs a hill on a motorway. Frictional forces of "
        f"{f_friction:g} N act on the {ctx} throughout the climb, which has a length of "
        f"{d_km:g} km. The {ctx} gains a height of {h:g} m during the climb. If the {ctx} "
        f"takes {t_min:g} min to complete the climb, calculate the average power of the "
        f"{ctx}'s engine."
    )
    working = [
        {"type": "text",  "content": f"Convert the distance and time: {d_km:g} km = {d_m:g} m, {t_min:g} min = {t_s:g} s"},
        {"type": "text",  "content": "The energy change here has two parts — a gain in Ep, plus work done against friction:"},
        {"type": "latex", "content": rf"E_p = mgh = {m_kg:g} \times 9.8 \times {h:g} = {ep}\ \mathrm{{J}}"},
        {"type": "latex", "content": rf"E_{{W,friction}} = Fd = {f_friction:g} \times {d_m:g} = {work_friction}\ \mathrm{{J}}"},
        {"type": "latex", "content": rf"E_{{W,total}} = {ep} + {work_friction} = {total_work}\ \mathrm{{J}}"},
        {"type": "text",  "content": "Average power = energy change ÷ time:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "latex", "content": rf"P = \frac{{{total_work}}}{{{t_s:g}}}"},
        {"type": "latex", "content": rf"P = {P}\ \mathrm{{W}}"},
    ]
    options_data = [
        {"value": P, "mistake": None, "working": working},
        {"value": round_sf(ep / t_s), "mistake": "You forgot to include the work done against friction. Total energy change = Ep + Fd.", "working": working},
        {"value": round_sf(work_friction / t_s), "mistake": "You forgot to include the gain in gravitational potential energy. Total energy change = Ep + Fd.", "working": working},
        {"value": round_sf(total_work / t_min), "mistake": f"You did not convert the time to seconds. {t_min:g} min = {t_s:g} s.", "working": working},
    ]
    scaffold = [
        {"question": "The energy change here has two parts. What is the total — the gain in gravitational potential energy, Ep, plus the work done against friction, Fd?", "answer": total_work},
        {"question": "What is the average power of the engine, P = (energy change) ÷ time?", "answer": P},
    ]
    return make_question(question, P, options_data, "W", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_conservation_power(level="Higher"):
    """Every branch computes average power as (change in energy) ÷ time — but
    what that energy change IS (gain in Ep, gain/loss of Ek, work done against
    friction, or a combination) differs with the situation. Identifying and
    calculating that energy change is always the first step."""
    return random.choice([
        _power_lift, _power_engine, _power_accelerate, _power_decelerate,
        _power_hydro, _power_slope,
    ])(level)


def generate_energy_conservation(level="Higher"):
    return random.choice([
        gen_energy_ep_ek, gen_energy_friction_force, gen_conservation_power,
    ])(level=level)


_ALL_GENS = [
    gen_work_find_ew, gen_work_find_f, gen_work_find_d,
    gen_power_find_p, gen_power_find_e, gen_power_find_t,
    gen_energy_ep_ek, gen_energy_friction_force, gen_conservation_power,
]


def generate_energy_work_power(level="Higher"):
    return random.choice(_ALL_GENS)(level=level)
