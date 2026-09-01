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

**Worked Example (conservation of energy):** A skateboarder of mass 55 kg starts from rest
at the top of a ramp of height 2.0 m. She reaches 5.5 m/s at the bottom, having travelled
8.0 m along the ramp. Calculate the average frictional force acting on her.
$$E_p = mgh = 55 \\times 9.8 \\times 2.0 = 1078\\ \\mathrm{J} \\qquad E_k = \\tfrac{1}{2}mv^2 = \\tfrac{1}{2} \\times 55 \\times 5.5^2 = 832\\ \\mathrm{J}$$
$$\\text{energy lost} = 1078 - 832 = 246\\ \\mathrm{J} \\qquad E_W = Fd \\implies 246 = F \\times 8.0 \\implies F = 31\\ \\mathrm{N}$$

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

# (context, mass_lo_kg, mass_hi_kg, height_lo_m, height_hi_m) — mass and height are
# tied to the context so a generated question never pairs (e.g.) a "weightlifter"
# with a 400 m lift.
_HEIGHT_KINDS = [
    ("weightlifter", 5, 250, 1.0, 2.5),
    ("crane", 100, 5000, 5, 60),
    ("hoist", 20, 500, 2, 15),
    ("hiker", 50, 100, 50, 900),
    ("chairlift", 60, 300, 100, 900),
]

# (context, mass_lo_kg, mass_hi_kg, speed_lo_ms, speed_hi_ms, allow_kmh)
_SPEED_KINDS = [
    ("sprinter", 45, 95, 5, 12, False),
    ("cyclist", 60, 95, 4, 15, False),
    ("car", 900, 2000, 8, 36, True),
    ("van", 1200, 3500, 8, 30, True),
    ("delivery drone", 0.5, 5, 3, 20, False),
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
        {"type": "text",  "content": "Rearrange EW = Fd for F:"},
        {"type": "latex", "content": r"F = \frac{E_W}{d}"},
        {"type": "latex", "content": rf"F = \frac{{{ew}}}{{{d}}}"},
        {"type": "latex", "content": rf"F = {F}\ \mathrm{{N}}"},
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
        {"type": "text",  "content": "Rearrange EW = Fd for d:"},
        {"type": "latex", "content": r"d = \frac{E_W}{F}"},
        {"type": "latex", "content": rf"d = \frac{{{ew}}}{{{F}}}"},
        {"type": "latex", "content": rf"d = {d}\ \mathrm{{m}}"},
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


# ── Section 2: Gravitational Potential Energy (Ep = mgh) ────────────────────

def gen_gpe_find_ep(level="Higher"):
    ctx, m_lo, m_hi, h_lo, h_hi = random.choice(_HEIGHT_KINDS)
    disp_m, unit, m_kg, is_g = _pick_mass(m_lo, m_hi)
    h = round(random.uniform(h_lo, h_hi), 1)
    ep = round_sf(m_kg * G * h)

    question = f"A {ctx} raises an object of mass {disp_m:g} {unit} through a height of {h:g} m. Calculate the gain in gravitational potential energy."
    working = []
    if is_g:
        working.append({"type": "text", "content": f"Convert the mass to kg: {disp_m:g} g = {m_kg} kg"})
    working += [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"E_p = {m_kg} \times 9.8 \times {h}"},
        {"type": "latex", "content": rf"E_p = {ep}\ \mathrm{{J}}"},
    ]
    options_data = [
        {"value": ep, "mistake": None, "working": working},
        {"value": round_sf(m_kg * h), "mistake": "You left out g. Ep = mgh, not mh.", "working": working},
        {"value": round_sf((disp_m if is_g else m_kg) * G * h), "mistake": f"You used {disp_m:g} without converting to kg. {disp_m:g} g = {m_kg} kg." if is_g else "Check your substitution.", "working": working},
    ]
    scaffold = [
        {"question": "What is m × g?", "answer": round_sf(m_kg * G)},
        {"question": "What is the gravitational potential energy Ep?", "answer": ep},
    ]
    return make_question(question, ep, options_data, "J", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_gpe_find_h(level="Higher"):
    ctx, m_lo, m_hi, h_lo, h_hi = random.choice(_HEIGHT_KINDS)
    disp_m, unit, m_kg, is_g = _pick_mass(m_lo, m_hi)
    h = round(random.uniform(h_lo, h_hi), 1)
    ep = round_sf(m_kg * G * h)

    question = f"A {ctx} raises an object of mass {disp_m:g} {unit}, giving it {ep} J of gravitational potential energy. Calculate the height risen."
    working = []
    if is_g:
        working.append({"type": "text", "content": f"Convert the mass to kg: {disp_m:g} g = {m_kg} kg"})
    working += [
        {"type": "text",  "content": "Rearrange Ep = mgh for h:"},
        {"type": "latex", "content": r"h = \frac{E_p}{mg}"},
        {"type": "latex", "content": rf"h = \frac{{{ep}}}{{{m_kg} \times 9.8}}"},
        {"type": "latex", "content": rf"h = {h}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": float(h), "mistake": None, "working": working},
        {"value": round_sf(ep / m_kg), "mistake": "You forgot to divide by g as well as m. h = Ep ÷ (mg).", "working": working},
        {"value": round_sf(ep * m_kg * G), "mistake": "You multiplied instead of dividing. h = Ep ÷ (mg).", "working": working},
    ]
    scaffold = [
        {"question": "What is m × g?", "answer": round_sf(m_kg * G)},
        {"question": "What is the height h?", "answer": float(h)},
    ]
    return make_question(question, float(h), options_data, "m", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_gpe_find_m(level="Higher"):
    ctx, m_lo, m_hi, h_lo, h_hi = random.choice(_HEIGHT_KINDS)
    dp = 1 if m_hi < 100 else 0
    m_kg = round(random.uniform(m_lo, m_hi), dp)
    if dp == 0:
        m_kg = int(m_kg)
    h = round(random.uniform(h_lo, h_hi), 1)
    ep = round_sf(m_kg * G * h)

    question = f"A {ctx} raises an object through a height of {h:g} m, giving it {ep} J of gravitational potential energy. Calculate the mass of the object."
    working = [
        {"type": "text",  "content": "Rearrange Ep = mgh for m:"},
        {"type": "latex", "content": r"m = \frac{E_p}{gh}"},
        {"type": "latex", "content": rf"m = \frac{{{ep}}}{{9.8 \times {h}}}"},
        {"type": "latex", "content": rf"m = {m_kg}\ \mathrm{{kg}}"},
    ]
    options_data = [
        {"value": m_kg, "mistake": None, "working": working},
        {"value": round_sf(ep / h), "mistake": "You forgot to divide by g as well as h. m = Ep ÷ (gh).", "working": working},
        {"value": round_sf(ep * G * h), "mistake": "You multiplied instead of dividing. m = Ep ÷ (gh).", "working": working},
    ]
    scaffold = [
        {"question": "What is g × h?", "answer": round_sf(G * h)},
        {"question": "What is the mass m?", "answer": m_kg},
    ]
    return make_question(question, m_kg, options_data, "kg", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def generate_gpe(level="Higher"):
    return random.choice([gen_gpe_find_ep, gen_gpe_find_h, gen_gpe_find_m])(level=level)


# ── Section 3: Kinetic Energy (Ek = ½mv²) ────────────────────────────────────

def gen_ke_find_ek(level="Higher"):
    ctx, m_lo, m_hi, v_lo, v_hi, allow_kmh = random.choice(_SPEED_KINDS)
    disp_m, unit, m_kg, is_g = _pick_mass(m_lo, m_hi)
    speed_kmh = allow_kmh and random.random() < 0.4
    if speed_kmh:
        v_disp = random.randint(int(v_lo * 3.6), int(v_hi * 3.6))
        v = round_sf(v_disp / 3.6)
    else:
        v_disp = v = round(random.uniform(v_lo, v_hi), 1)
    ek = round_sf(0.5 * m_kg * v ** 2)
    v_unit = "km h⁻¹" if speed_kmh else "m s⁻¹"

    question = f"A {ctx} of mass {disp_m:g} {unit} travels at a speed of {v_disp:g} {v_unit}. Calculate the kinetic energy."
    working = []
    if is_g:
        working.append({"type": "text", "content": f"Convert the mass to kg: {disp_m:g} g = {m_kg} kg"})
    if speed_kmh:
        working.append({"type": "text", "content": f"Convert the speed to m/s: {v_disp:g} km h⁻¹ = {v} m s⁻¹"})
    working += [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"E_k = \tfrac{1}{2}mv^2"},
        {"type": "latex", "content": rf"E_k = \tfrac{{1}}{{2}} \times {m_kg} \times {v}^2"},
        {"type": "latex", "content": rf"E_k = {ek}\ \mathrm{{J}}"},
    ]
    options_data = [
        {"value": ek, "mistake": None, "working": working},
        {"value": round_sf(m_kg * v ** 2), "mistake": "You forgot the ½ in Ek = ½mv².", "working": working},
        {"value": round_sf(0.5 * m_kg * v), "mistake": "You must square the velocity. Ek = ½mv², not ½mv.", "working": working},
    ]
    scaffold = [
        {"question": "What is v²?", "answer": round_sf(v ** 2)},
        {"question": "What is the kinetic energy Ek?", "answer": ek},
    ]
    return make_question(question, ek, options_data, "J", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_ke_find_v(level="Higher"):
    ctx, m_lo, m_hi, v_lo, v_hi, _allow_kmh = random.choice(_SPEED_KINDS)
    disp_m, unit, m_kg, is_g = _pick_mass(m_lo, m_hi)
    v = round(random.uniform(v_lo, v_hi), 1)
    ek = round_sf(0.5 * m_kg * v ** 2)

    question = f"A {ctx} of mass {disp_m:g} {unit} has a kinetic energy of {ek} J. Calculate its speed."
    working = []
    if is_g:
        working.append({"type": "text", "content": f"Convert the mass to kg: {disp_m:g} g = {m_kg} kg"})
    working += [
        {"type": "text",  "content": "Rearrange Ek = ½mv² for v:"},
        {"type": "latex", "content": r"v = \sqrt{\frac{2E_k}{m}}"},
        {"type": "latex", "content": rf"v = \sqrt{{\frac{{2 \times {ek}}}{{{m_kg}}}}}"},
        {"type": "latex", "content": rf"v = {v}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v, "mistake": None, "working": working},
        {"value": round_sf(math.sqrt(ek / m_kg)), "mistake": "You forgot to multiply by 2 before square rooting. v = √(2Ek ÷ m).", "working": working},
        {"value": round_sf(2 * ek / m_kg), "mistake": "You forgot to take the square root. v = √(2Ek ÷ m).", "working": working},
    ]
    scaffold = [
        {"question": "What is 2Ek ÷ m?", "answer": round_sf(2 * ek / m_kg)},
        {"question": "What is the speed v?", "answer": v},
    ]
    return make_question(question, v, options_data, "m/s", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_ke_find_m(level="Higher"):
    ctx, m_lo, m_hi, v_lo, v_hi, _allow_kmh = random.choice(_SPEED_KINDS)
    dp = 2 if m_hi < 10 else (1 if m_hi < 100 else 0)
    m_kg = round(random.uniform(m_lo, m_hi), dp)
    if dp == 0:
        m_kg = int(m_kg)
    v = round(random.uniform(v_lo, v_hi), 1)
    ek = round_sf(0.5 * m_kg * v ** 2)

    question = f"A {ctx} has a kinetic energy of {ek} J while travelling at a speed of {v} m/s. Calculate its mass."
    working = [
        {"type": "text",  "content": "Rearrange Ek = ½mv² for m:"},
        {"type": "latex", "content": r"m = \frac{2E_k}{v^2}"},
        {"type": "latex", "content": rf"m = \frac{{2 \times {ek}}}{{{v}^2}}"},
        {"type": "latex", "content": rf"m = {m_kg}\ \mathrm{{kg}}"},
    ]
    options_data = [
        {"value": m_kg, "mistake": None, "working": working},
        {"value": round_sf(2 * ek / v), "mistake": "You must square v before dividing. m = 2Ek ÷ v².", "working": working},
        {"value": round_sf(ek / v ** 2), "mistake": "You forgot to multiply by 2. m = 2Ek ÷ v².", "working": working},
    ]
    scaffold = [
        {"question": "What is v²?", "answer": round_sf(v ** 2)},
        {"question": "What is the mass m?", "answer": m_kg},
    ]
    return make_question(question, m_kg, options_data, "kg", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def generate_ke(level="Higher"):
    return random.choice([gen_ke_find_ek, gen_ke_find_v, gen_ke_find_m])(level=level)


# ── Section 4: Power (P = E/t) ────────────────────────────────────────────────

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
        {"type": "text",  "content": "Rearrange P = E/t for E:"},
        {"type": "latex", "content": r"E = Pt"},
        {"type": "latex", "content": rf"E = {P:g} \times {t_s}"},
        {"type": "latex", "content": rf"E = {E}\ \mathrm{{J}}"},
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
        {"type": "text",  "content": "Rearrange P = E/t for t:"},
        {"type": "latex", "content": r"t = \frac{E}{P}"},
        {"type": "latex", "content": rf"t = \frac{{{E:g}}}{{{P:g}}}"},
        {"type": "latex", "content": rf"t = {t_s}\ \mathrm{{s}}"},
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


# ── Section 5: Conservation of Energy ────────────────────────────────────────

def gen_energy_freefall_speed(level="Higher"):
    m_kg = round(random.uniform(0.1, 5), 2)
    h = round(random.uniform(1.5, 30), 1)
    v2 = round_sf(2 * G * h)
    v = round_sf(math.sqrt(v2))

    question = (
        f"An object of mass {m_kg} kg is dropped from a height of {h} m. Assuming no "
        f"energy is lost to air resistance, calculate the speed of the object just before "
        f"it hits the ground."
    )
    working = [
        {"type": "text",  "content": "All Ep converts to Ek (no air resistance):"},
        {"type": "latex", "content": r"mgh = \tfrac{1}{2}mv^2 \;\Rightarrow\; v = \sqrt{2gh}"},
        {"type": "latex", "content": rf"v = \sqrt{{2 \times 9.8 \times {h}}}"},
        {"type": "latex", "content": rf"v = {v}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v, "mistake": None, "working": working},
        {"value": round_sf(math.sqrt(G * h)), "mistake": "You forgot the factor of 2. v = √(2gh).", "working": working},
        {"value": round_sf(G * h), "mistake": "You must take the square root of 2gh to find v.", "working": working},
    ]
    scaffold = [
        {"question": "What is v² (= 2gh)?", "answer": v2},
        {"question": "What is the speed v?", "answer": v},
    ]
    return make_question(question, v, options_data, "m/s", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_energy_max_height(level="Higher"):
    v = round(random.uniform(5, 30), 1)
    h = round_sf(v ** 2 / (2 * G))

    question = (
        f"A ball is thrown vertically upwards with an initial speed of {v} m/s. Assuming no "
        f"energy is lost to air resistance, calculate the maximum height reached by the ball."
    )
    working = [
        {"type": "text",  "content": "All Ek converts to Ep at maximum height:"},
        {"type": "latex", "content": r"\tfrac{1}{2}mv^2 = mgh \;\Rightarrow\; h = \frac{v^2}{2g}"},
        {"type": "latex", "content": rf"h = \frac{{{v}^2}}{{2 \times 9.8}}"},
        {"type": "latex", "content": rf"h = {h}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": h, "mistake": None, "working": working},
        {"value": round_sf(v ** 2 / G), "mistake": "You forgot the factor of 2. h = v² ÷ (2g).", "working": working},
        {"value": round_sf(v / (2 * G)), "mistake": "You must square v before dividing. h = v² ÷ (2g).", "working": working},
    ]
    scaffold = [
        {"question": "What is v²?", "answer": round_sf(v ** 2)},
        {"question": "What is the maximum height h?", "answer": h},
    ]
    return make_question(question, h, options_data, "m", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


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


def gen_energy_lift_power(level="Higher"):
    m_kg = round(random.uniform(40, 120), 0)
    h = round(random.uniform(2.0, 10.0), 1)
    t = round(random.uniform(8, 25), 0)
    ep = round_sf(m_kg * G * h)
    P = round_sf(ep / t)

    ctx = random.choice(["goods lift", "escalator", "chairlift", "hoist"])
    question = (
        f"A {ctx} carries a load of mass {m_kg:g} kg through a vertical height of {h} m in "
        f"a time of {t:g} s, moving at constant speed. Calculate the useful power developed."
    )
    working = [
        {"type": "text",  "content": "At constant speed, useful power = Ep gained ÷ time:"},
        {"type": "latex", "content": rf"E_p = mgh = {m_kg:g} \times 9.8 \times {h} = {ep}\ \mathrm{{J}}"},
        {"type": "latex", "content": r"P = \frac{E_p}{t}"},
        {"type": "latex", "content": rf"P = \frac{{{ep}}}{{{t:g}}}"},
        {"type": "latex", "content": rf"P = {P}\ \mathrm{{W}}"},
    ]
    options_data = [
        {"value": P, "mistake": None, "working": working},
        {"value": round_sf(ep * t), "mistake": "You multiplied Ep by t instead of dividing. P = Ep ÷ t.", "working": working},
        {"value": round_sf(m_kg * G / t), "mistake": "You left out the height h when calculating Ep. Ep = mgh.", "working": working},
    ]
    scaffold = [
        {"question": "What is the gravitational potential energy gained, Ep?", "answer": ep},
        {"question": "What is the useful power P?", "answer": P},
    ]
    return make_question(question, P, options_data, "W", scaffold=scaffold,
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def gen_energy_engine_power(level="Higher"):
    F = random.randint(400, 2500)
    v = round(random.uniform(8, 35), 1)
    P = round_sf(F * v)

    ctx = random.choice(["delivery van", "lorry", "car", "tractor"])
    question = (
        f"A {ctx}'s engine produces a driving force of {F} N while travelling at a "
        f"constant speed of {v} m/s along a level road. Calculate the power developed by "
        f"the engine."
    )
    working = [
        {"type": "text",  "content": "At constant speed, EW = Fd = F(vt), so P = EW ÷ t = Fv:"},
        {"type": "latex", "content": r"P = Fv"},
        {"type": "latex", "content": rf"P = {F} \times {v}"},
        {"type": "latex", "content": rf"P = {P}\ \mathrm{{W}}"},
    ]
    options_data = [
        {"value": P, "mistake": None, "working": working},
        {"value": round_sf(F / v), "mistake": "You divided F by v instead of multiplying. P = Fv.", "working": working},
    ]
    return make_question(question, P, options_data, "W",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Energy, Work and Power", level=level)


def generate_energy_conservation(level="Higher"):
    return random.choice([
        gen_energy_freefall_speed, gen_energy_max_height,
        gen_energy_friction_force, gen_energy_lift_power, gen_energy_engine_power,
    ])(level=level)


_ALL_GENS = [
    gen_work_find_ew, gen_work_find_f, gen_work_find_d,
    gen_gpe_find_ep, gen_gpe_find_h, gen_gpe_find_m,
    gen_ke_find_ek, gen_ke_find_v, gen_ke_find_m,
    gen_power_find_p, gen_power_find_e, gen_power_find_t,
    gen_energy_freefall_speed, gen_energy_max_height,
    gen_energy_friction_force, gen_energy_lift_power, gen_energy_engine_power,
]


def generate_energy_work_power(level="Higher"):
    return random.choice(_ALL_GENS)(level=level)
