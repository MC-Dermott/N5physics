"""Higher ODU — Newton's Law of Gravitation.

Mirrors Hphys_Newtons_Law_of_Gravitation_Worksheet.docx, one generator per worksheet type:
  1  Calculating the force, a mass or a distance (mixed)
  2  Units and centre-to-centre distances (mixed)
  3  Using the force to find g at a height        (reuses gravitation.generate_orbital_gravitation)
  4  How does the force change? (state and justify)

Every distractor is one of the common errors seen in SQA marking instructions / course reports:
r not squared, no square root when finding r, r² dropped when rearranging, g used instead of G,
height used instead of centre-to-centre distance, km/tonnes/g not converted, and treating F as
inversely proportional to r rather than r².
"""
import math
import random

from utils.make_question import make_question
from topics.dynamics.gravitation import generate_orbital_gravitation

G = 6.67e-11
TOPIC = "Our Dynamic Universe"
QTYPE = "Gravitation"

_NOTES = r"""
## Newton's Law of Gravitation

**Relationship (as on the relationships sheet):**
$$F = \frac{Gm_1m_2}{r^2}$$

$G = 6.67 \times 10^{-11}\ \mathrm{m^3\,kg^{-1}\,s^{-2}}$ (data sheet). **r is the distance between
the centres of the two masses.**

**Method:** list the knowns and the unknown → write the equation exactly as above → substitute →
rearrange (if needed) and solve, with units.

**Common errors (from SQA marking instructions and course reports):**
- Using the **height above the surface** as r — add the planet's radius (r = R + h), and for two
  spheres add both radii to the gap between them. Watch for a *diameter* being given.
- Not converting **km → m, tonnes → kg, g → kg** before substituting.
- Not squaring r — or squaring only the power of ten on the calculator. Put brackets round r.
- Stopping at **r²** when asked for r — the last step is a square root.
- Dropping the r² when rearranging for a mass.
- Using **g (9.8)** instead of **G (6.67 × 10⁻¹¹)**.
- At a height, g is **not** 9.8 N kg⁻¹ — use W = mg with W equal to the gravitational force.
- **Inverse square:** doubling the distance gives **¼** of the force, not ½. State the answer first
  ("the force is 4/9 of…", not "decreases by 4/9"), then justify each change.
"""

_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _sig(x, sf=3):
    return float(f"{x:.{sf}g}")


def _ltx(x, sf=3):
    """LaTeX value: plain for 0.01 ≤ |x| < 10 000, otherwise a × 10^n."""
    x = _sig(x, sf)
    if 0.01 <= abs(x) < 1e4:
        return f"{x:g}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    return rf"{coeff} \times 10^{{{int(exp)}}}"


def _txt(x, sf=3):
    """Plain-text value for question text, never Python's 1e+07 style."""
    x = _sig(x, sf)
    if 0.01 <= abs(x) < 1e4:
        return f"{x:g}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    return f"{coeff} × 10{str(int(exp)).translate(_SUP)}"


def _pick(lo, hi, sf=2):
    """Log-uniform value between lo and hi, rounded to sf significant figures."""
    return _sig(10 ** random.uniform(math.log10(lo), math.log10(hi)), sf)


def _the(desc):
    """'a planet' -> 'the planet', 'one of its moons' -> 'the moon'."""
    if desc.startswith("one of its "):
        return "the " + desc[len("one of its "):].rstrip("s")
    if desc.startswith("an "):
        return "the " + desc[3:]
    if desc.startswith("a "):
        return "the " + desc[2:]
    return desc


def _F(m1, m2, r):
    return G * m1 * m2 / r ** 2


def _eq():
    return {"type": "latex", "content": r"F = \frac{Gm_1m_2}{r^2}"}


def _sub_F(m1, m2, r, F_side="F"):
    return {"type": "latex",
            "content": rf"{F_side} = 6.67 \times 10^{{-11}} \times \frac{{{_ltx(m1)} \times {_ltx(m2)}}}{{({_ltx(r)})^2}}"}


def _q(text, answer, unit, options, scaffold):
    return make_question(text, answer, options, unit, scaffold=scaffold, notes=_NOTES,
                         topic=TOPIC, question_type=QTYPE, level="Higher")


# ── Type 1: force, mass or distance ─────────────────────────────────────────
# (m1 description, m1 lo, m1 hi, m2 description, m2 lo, m2 hi, r lo, r hi, r phrase)
_PAIRS = [
    ("the Earth", 5.97e24, 5.97e24, "the Moon", 7.35e22, 7.35e22, 3.6e8, 4.1e8,
     "the distance between their centres"),
    ("a star", 1.0e30, 4.0e30, "a planet", 3.0e23, 2.0e27, 5.0e10, 8.0e11, "its orbital radius"),
    ("a planet", 1.0e25, 2.0e27, "one of its moons", 1.0e19, 1.5e23, 1.0e8, 2.0e9, "the moon's orbital radius"),
    ("one star in a binary system", 1.0e30, 4.0e30, "the other star", 1.0e30, 4.0e30, 1.0e11, 5.0e12,
     "the distance between their centres"),
    ("an asteroid", 1.0e11, 5.0e12, "a smaller asteroid", 1.0e9, 5.0e10, 1.0e3, 5.0e4,
     "the distance between their centres"),
    ("a large lead sphere", 50, 200, "a small lead sphere", 0.5, 2.0, 0.10, 0.40,
     "the distance between their centres"),
    ("the Earth", 5.97e24, 5.97e24, "a satellite", 400, 5000, 6.8e6, 4.3e7,
     "the distance between the satellite and the centre of the Earth"),
]


def _pair_values():
    d1, a1, b1, d2, a2, b2, rlo, rhi, rphr = random.choice(_PAIRS)
    m1 = a1 if a1 == b1 else _pick(a1, b1)
    m2 = a2 if a2 == b2 else _pick(a2, b2)
    r = _pick(rlo, rhi)
    return d1, m1, d2, m2, r, rphr


def _t1_force():
    d1, m1, d2, m2, r, rphr = _pair_values()
    F = _sig(_F(m1, m2, r))
    text = (f"The mass of {d1} is {_txt(m1)} kg and the mass of {d2} is {_txt(m2)} kg. "
            f"{rphr[0].upper() + rphr[1:]} is {_txt(r)} m. "
            f"Calculate the gravitational force between them.")
    work = [_eq(), _sub_F(m1, m2, r), {"type": "latex", "content": rf"F = {_ltx(F)}\ \mathrm{{N}}"}]
    opts = [
        {"value": F, "mistake": None, "working": work},
        {"value": _sig(G * m1 * m2 / r), "mistake": "You didn't square r — the equation has r² on the bottom.", "working": work},
        {"value": _sig(9.8 * m1 * m2 / r ** 2), "mistake": "You used g (9.8) instead of G (6.67 × 10⁻¹¹) from the data sheet.", "working": work},
        {"value": _sig(m1 * m2 / r ** 2), "mistake": "You left out G — multiply by 6.67 × 10⁻¹¹.", "working": work},
    ]
    scaffold = [{"question": "What is r², in m²?", "answer": _sig(r ** 2)},
                {"question": "What is m₁ × m₂?", "answer": _sig(m1 * m2)},
                {"question": "What is the gravitational force F, in N?", "answer": F}]
    return _q(text, F, "N", opts, scaffold)


def _t1_mass():
    d1, m1, d2, m2, r, rphr = _pair_values()
    F = _sig(_F(m1, m2, r), 2)
    m2_ans = _sig(F * r ** 2 / (G * m1))
    text = (f"The gravitational force between {d1} (mass {_txt(m1)} kg) and {d2} is {_txt(F, 2)} N. "
            f"{rphr[0].upper() + rphr[1:]} is {_txt(r)} m. Calculate the mass of {_the(d2)}.")
    work = [_eq(),
            {"type": "latex", "content": rf"{_ltx(F, 2)} = 6.67 \times 10^{{-11}} \times \frac{{{_ltx(m1)} \times m_2}}{{({_ltx(r)})^2}}"},
            {"type": "latex", "content": rf"m_2 = \frac{{{_ltx(F, 2)} \times ({_ltx(r)})^2}}{{6.67 \times 10^{{-11}} \times {_ltx(m1)}}}"},
            {"type": "latex", "content": rf"m_2 = {_ltx(m2_ans)}\ \mathrm{{kg}}"}]
    opts = [
        {"value": m2_ans, "mistake": None, "working": work},
        {"value": _sig(F / (G * m1)), "mistake": "You dropped the r² when rearranging — multiply F by r² before dividing by G and m₁.", "working": work},
        {"value": _sig(F * r / (G * m1)), "mistake": "You multiplied by r instead of r².", "working": work},
        {"value": _sig(F * r ** 2 / m1), "mistake": "You left out G when rearranging.", "working": work},
    ]
    scaffold = [{"question": "What is F × r²?", "answer": _sig(F * r ** 2)},
                {"question": "What is G × m₁?", "answer": _sig(G * m1)},
                {"question": "What is the mass m₂, in kg?", "answer": m2_ans}]
    return _q(text, m2_ans, "kg", opts, scaffold)


def _t1_radius():
    d1, m1, d2, m2, r, rphr = _pair_values()
    F = _sig(_F(m1, m2, r), 2)
    r2 = G * m1 * m2 / F
    r_ans = _sig(math.sqrt(r2))
    text = (f"The mass of {d1} is {_txt(m1)} kg and the mass of {d2} is {_txt(m2)} kg. "
            f"The gravitational force between them is {_txt(F, 2)} N. "
            f"Calculate the distance between their centres.")
    work = [_eq(),
            {"type": "latex", "content": rf"{_ltx(F, 2)} = 6.67 \times 10^{{-11}} \times \frac{{{_ltx(m1)} \times {_ltx(m2)}}}{{r^2}}"},
            {"type": "latex", "content": rf"r^2 = {_ltx(r2)}\ \mathrm{{m^2}}"},
            {"type": "latex", "content": rf"r = \sqrt{{{_ltx(r2)}}} = {_ltx(r_ans)}\ \mathrm{{m}}"}]
    opts = [
        {"value": r_ans, "mistake": None, "working": work},
        {"value": _sig(r2), "mistake": "That's r², not r — the last step is a square root.", "working": work},
        {"value": _sig(math.sqrt(m1 * m2 / F)), "mistake": "You left out G when rearranging.", "working": work},
        {"value": _sig(math.sqrt(9.8 * m1 * m2 / F)), "mistake": "You used g (9.8) instead of G (6.67 × 10⁻¹¹).", "working": work},
    ]
    scaffold = [{"question": "What is r², in m²?", "answer": _sig(r2)},
                {"question": "What is the distance r, in m?", "answer": r_ans}]
    return _q(text, r_ans, "m", opts, scaffold)


def gen_grav_force_mass_distance(level="Higher"):
    return random.choice([_t1_force, _t1_mass, _t1_radius])()


# ── Type 2: units and centre-to-centre distances ────────────────────────────
# (name, mass kg, radius m) — radius is used for r = R + h
_BODIES = [("the Earth", 5.97e24, 6.37e6), ("Mars", 6.42e23, 3.39e6), ("Venus", 4.87e24, 6.05e6),
           ("the Moon", 7.35e22, 1.74e6)]
# (object, mass lo kg, mass hi kg, height lo km, height hi km)
_ORBITERS = [("A satellite", 500, 5000, 300, 36000), ("A space probe", 400, 3000, 100, 5000),
             ("A space station", 2.0e5, 4.5e5, 300, 500)]


def _t2_height():
    body, M, R = random.choice(_BODIES)
    obj, mlo, mhi, hlo, hhi = random.choice(_ORBITERS)
    if body == "the Moon":
        hlo, hhi = 50, 500
    m = _pick(mlo, mhi)
    h_km = int(_pick(hlo, hhi))
    use_diameter = random.random() < 0.3
    h = h_km * 1000
    r = R + h
    F = _sig(_F(M, m, r))
    size = (f"a diameter of {_txt(2 * R)} m" if use_diameter else f"a radius of {_txt(R)} m")
    text = (f"{obj} of mass {_txt(m)} kg orbits at a height of {h_km:,} km above the surface of {body}. "
            f"{body[0].upper() + body[1:]} has a mass of {_txt(M)} kg and {size}. "
            f"Calculate the gravitational force on {_the(obj.lower())}.")
    work = []
    if use_diameter:
        work.append({"type": "latex", "content": rf"R = \frac{{{_ltx(2 * R)}}}{{2}} = {_ltx(R)}\ \mathrm{{m}}"})
    work += [{"type": "latex", "content": rf"r = R + h = {_ltx(R)} + {_ltx(h)} = {_ltx(r)}\ \mathrm{{m}}"},
             _eq(), _sub_F(M, m, r), {"type": "latex", "content": rf"F = {_ltx(F)}\ \mathrm{{N}}"}]
    opts = [
        {"value": F, "mistake": None, "working": work},
        {"value": _sig(_F(M, m, h)), "mistake": "You used the height above the surface as r. r is measured from the centre: r = R + h.", "working": work},
        {"value": _sig(_F(M, m, R / 1000 + h_km)), "mistake": "You didn't convert to metres before substituting — 1 km = 1000 m.", "working": work},
    ]
    if use_diameter:
        opts.append({"value": _sig(_F(M, m, 2 * R + h)), "mistake": "You used the diameter instead of the radius — halve it first.", "working": work})
    scaffold = [{"question": "What is the height in metres?", "answer": float(h)},
                {"question": "What is r, the distance from the centre, in m?", "answer": _sig(r)},
                {"question": "What is the gravitational force F, in N?", "answer": F}]
    return _q(text, F, "N", opts, scaffold)


def _t2_spheres():
    m = _pick(20, 200)
    d = round(random.choice([0.10, 0.12, 0.15, 0.20, 0.25, 0.30]), 2)
    gap = round(random.choice([0.02, 0.03, 0.05, 0.08, 0.10]), 2)
    r = d + gap
    F = _sig(_F(m, m, r))
    text = (f"Two identical lead spheres each have a mass of {_txt(m)} kg and a diameter of {d:.2f} m. "
            f"The gap between their surfaces is {gap:.2f} m. Calculate the gravitational force between them.")
    work = [{"type": "text", "content": "r = radius + gap + radius"},
            {"type": "latex", "content": rf"r = {d / 2:g} + {gap:g} + {d / 2:g} = {r:g}\ \mathrm{{m}}"},
            _eq(), _sub_F(m, m, r), {"type": "latex", "content": rf"F = {_ltx(F)}\ \mathrm{{N}}"}]
    opts = [
        {"value": F, "mistake": None, "working": work},
        {"value": _sig(_F(m, m, gap)), "mistake": "You used the gap between the surfaces as r — r is centre to centre, so add both radii.", "working": work},
        {"value": _sig(_F(m, m, gap + d / 2)), "mistake": "You only added one radius — add the radius of each sphere to the gap.", "working": work},
    ]
    scaffold = [{"question": "What is r, the distance between the centres, in m?", "answer": _sig(r)},
                {"question": "What is the gravitational force F, in N?", "answer": F}]
    return _q(text, F, "N", opts, scaffold)


def _t2_units():
    kind = random.choice(["asteroids_km", "station_tonnes", "balls_grams"])
    if kind == "asteroids_km":
        m1, m2 = _pick(1e11, 5e12), _pick(1e10, 1e11)
        r_given, r_unit, r = _sig(random.uniform(1.2, 9.5), 2), "km", None
        r = r_given * 1000
        text = (f"Two asteroids of masses {_txt(m1)} kg and {_txt(m2)} kg have centres {r_given:g} km apart. "
                f"Calculate the gravitational force between them.")
        conv = f"r = {r_given:g} km = {_txt(r)} m"
        wrong = _sig(_F(m1, m2, r_given))
        wrong_msg = "You didn't convert km to m — 1 km = 1000 m."
    elif kind == "station_tonnes":
        m1 = 5.97e24
        t = int(_pick(200, 450))
        m2 = t * 1000
        r_km = int(_pick(6700, 6900))
        r = r_km * 1000
        text = (f"A space station of mass {t} tonnes orbits at a distance of {r_km:,} km from the centre of the Earth. "
                f"The mass of the Earth is {_txt(m1)} kg. Calculate the gravitational force on the space station.")
        conv = f"m = {t} tonnes = {_txt(m2)} kg,  r = {r_km:,} km = {_txt(r)} m"
        wrong = _sig(_F(m1, t, r))
        wrong_msg = "You didn't convert tonnes to kg — 1 tonne = 1000 kg."
    else:
        g1, g2 = int(_pick(200, 1500)), int(_pick(10, 60))
        m1, m2 = g1 / 1000, g2 / 1000
        r_cm = round(random.uniform(3, 12), 1)
        r = r_cm / 100
        text = (f"Two small lead balls of masses {g1} g and {g2} g are placed with their centres {r_cm:g} cm apart. "
                f"Calculate the gravitational force between them.")
        conv = f"m₁ = {m1:g} kg,  m₂ = {m2:g} kg,  r = {r:g} m"
        wrong = _sig(G * g1 * g2 / r_cm ** 2)
        wrong_msg = "You didn't convert g → kg and cm → m before substituting."
    F = _sig(_F(m1, m2, r))
    work = [{"type": "text", "content": conv}, _eq(), _sub_F(m1, m2, r),
            {"type": "latex", "content": rf"F = {_ltx(F)}\ \mathrm{{N}}"}]
    opts = [
        {"value": F, "mistake": None, "working": work},
        {"value": wrong, "mistake": wrong_msg, "working": work},
        {"value": _sig(G * m1 * m2 / r), "mistake": "You didn't square r.", "working": work},
    ]
    scaffold = [{"question": "What is r in metres?", "answer": _sig(r)},
                {"question": "What is the gravitational force F, in N?", "answer": F}]
    return _q(text, F, "N", opts, scaffold)


def gen_grav_units_centre_distance(level="Higher"):
    return random.choice([_t2_height, _t2_height, _t2_spheres, _t2_units])()


# ── Type 3: g at a height ───────────────────────────────────────────────────

def gen_grav_field_at_height(level="Higher"):
    return generate_orbital_gravitation(level=level)


# ── Type 4: how does the force change? ──────────────────────────────────────
_MASS_FACTORS = [(0.25, "a quarter of"), (1 / 3, "a third of"), (0.5, "half"), (2, "twice"),
                 (3, "three times"), (4, "four times"), (5, "five times")]
_DIST_FACTORS = [(0.5, "half"), (1 / 3, "a third of"), (2, "twice"), (3, "three times"), (4, "four times")]
_SYSTEMS = [("satellite", "the first satellite", "the centre of the Earth"),
            ("moon", "the first moon", "the centre of the planet"),
            ("planet", "the first planet", "the centre of the star")]


def gen_grav_force_change(level="Higher"):
    obj, first, centre = random.choice(_SYSTEMS)
    k, kw = random.choice(_MASS_FACTORS)
    d, dw = random.choice(_DIST_FACTORS)
    ratio = _sig(k / d ** 2)
    text = (f"A second {obj} has {kw} the mass of {first}. Its distance from {centre} is {dw} "
            f"that of {first}. How many times the gravitational force on {first} is the force on the second {obj}? "
            f"(Give F₂ ÷ F₁.)")
    work = [_eq(),
            {"type": "latex", "content": rf"F_2 = \frac{{G \times m_1 \times ({k:.3g}\,m_2)}}{{({d:.3g}\,r)^2}} = \frac{{{k:.3g}}}{{{d ** 2:.3g}}} \times \frac{{Gm_1m_2}}{{r^2}}"},
            {"type": "text", "content": f"Mass × {k:.3g} → force × {k:.3g}.   Distance × {d:.3g} → force ÷ {d ** 2:.3g} (inverse square)."},
            {"type": "latex", "content": rf"\frac{{F_2}}{{F_1}} = {ratio:g}"}]
    opts = [
        {"value": ratio, "mistake": None, "working": work},
        {"value": _sig(k / d), "mistake": "You treated the force as inversely proportional to r — it's r², so square the distance factor.", "working": work},
        {"value": _sig(k * d ** 2), "mistake": "Increasing the distance decreases the force — divide by the distance factor squared, don't multiply.", "working": work},
        {"value": _sig(d ** 2 / k), "mistake": "You've got the ratio upside down — more mass means more force.", "working": work},
    ]
    opts = [o for i, o in enumerate(opts) if i == 0 or abs(o["value"] - ratio) > 1e-9]
    scaffold = [{"question": "By what factor does the change in mass multiply the force?", "answer": _sig(k)},
                {"question": "By what factor does the change in distance multiply the force (1 ÷ factor²)?", "answer": _sig(1 / d ** 2)},
                {"question": "What is F₂ ÷ F₁?", "answer": ratio}]
    return _q(text, ratio, "", opts, scaffold)
