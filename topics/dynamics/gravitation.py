import random
from core.models.question_model import PhysicsQuestion

G = 6.674e-11  # N m² kg⁻²

_NOTES = """
## Gravitation

**Newton's Law of Universal Gravitation:**
$$F = \\frac{GMm}{r^2}$$

**Gravitational Field Strength:**
$$g = \\frac{GM}{r^2} \\qquad \\text{or equivalently} \\qquad g = \\frac{F}{m}$$

| Symbol | Quantity | Unit |
|---|---|---|
| G | Gravitational constant = 6.67 × 10⁻¹¹ | N m² kg⁻² |
| M | Mass of planet | kg |
| m | Mass of probe / object | kg |
| r | Orbital radius (measured from centre of planet) | m |
| g | Gravitational field strength | N kg⁻¹ |

> ⚠️ **r is NOT the orbital height.** It is measured from the **centre of the planet**:
> $$r = R + h$$
> where R = planet radius and h = orbital height above the surface.

> ⚠️ Always convert distances to **metres** before substituting into formulae.
> 1 km = 1000 m, so multiply km values by 1000.
"""

_PLANETS = [
    {"name": "Mars",     "M": 6.42e23,  "R": 3.39e6},
    {"name": "Venus",    "M": 4.87e24,  "R": 6.05e6},
    {"name": "Jupiter",  "M": 1.90e27,  "R": 7.15e7},
    {"name": "the Moon", "M": 7.35e22,  "R": 1.74e6},
    {"name": "Saturn",   "M": 5.69e26,  "R": 6.03e7},
    {"name": "Earth",    "M": 5.97e24,  "R": 6.37e6},
]

_PROBE_MASSES = [500, 750, 1000, 1200, 1500, 2000, 2500, 3000, 3500, 4000, 5000, 5600, 6000, 7500, 8000]

# Orbital heights in km — given to students in km so they must convert to m
_HEIGHTS_KM = [300, 400, 500, 600, 800, 1000, 1200, 1500, 2000, 2500, 3000, 3500, 3700, 4000, 5000, 6000]


def _r3(val):
    return float(f"{val:.3g}")


def _ltx(val, sf=3):
    """Format value as LaTeX scientific notation, e.g. 4.77 \\times 10^{3}"""
    s = f"{val:.{sf - 1}e}"
    coeff, exp = s.split("e")
    return rf"{coeff} \times 10^{{{int(exp)}}}"


def _disp(val, sf=3):
    """Human-readable scientific notation for markdown, e.g. 4.77 × 10³"""
    s = f"{val:.{sf - 1}e}"
    coeff, exp_s = s.split("e")
    exp_i = int(exp_s)
    sup = str(exp_i).replace("-", "⁻").translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
    return f"{coeff} × 10{sup}"


def generate_orbital_gravitation(level="Higher"):
    planet = random.choice(_PLANETS)
    name = planet["name"]
    M = planet["M"]   # kg
    R = planet["R"]   # m

    probe_mass = random.choice(_PROBE_MASSES)
    h_km = random.choice(_HEIGHTS_KM)
    h_m = h_km * 1000          # correct conversion to metres
    R_km = R / 1000             # planet radius in km (used for wrong-unit distractor)

    # ── Correct orbital radius ─────────────────────────────────────────────────
    r = R + h_m

    F = _r3(G * M * probe_mass / r ** 2)
    g = _r3(G * M / r ** 2)

    # ── Distractor 1: forgot to add planet radius (used h as r) ───────────────
    F_no_R = _r3(G * M * probe_mass / h_m ** 2)
    g_no_R = _r3(G * M / h_m ** 2)

    # ── Distractor 2: didn't convert km → m (used km values as if metres) ─────
    r_km_as_m = R_km + h_km     # e.g. 3390 + 3700 = 7090, wrongly used as 7090 m
    F_no_conv = _r3(G * M * probe_mass / r_km_as_m ** 2)
    g_no_conv = _r3(G * M / r_km_as_m ** 2)

    # ── LaTeX snippets ─────────────────────────────────────────────────────────
    M_ltx  = _ltx(M)
    R_ltx  = _ltx(R)
    hm_ltx = _ltx(h_m)
    r_ltx  = _ltx(r)
    F_ltx  = _ltx(F)
    g_ltx  = _ltx(g)

    # ── Scenario context ───────────────────────────────────────────────────────
    context = (
        f"A space probe of mass **{probe_mass:,} kg** is in orbit at a height of "
        f"**{h_km:,} km** above the surface of **{name}**.\n\n"
        f"The mass of {name} is ${M_ltx}$ kg.  \n"
        f"The radius of {name} is ${R_ltx}$ m."
    )

    # ── Correct working (shared between parts) ─────────────────────────────────
    step_r = [
        {"type": "text",  "content": f"Step 1 — find the orbital radius r (from the centre of {name}):"},
        {"type": "latex", "content": r"r = R + h"},
        {"type": "text",  "content": f"Convert h to metres first: {h_km:,} km × 1000 = {h_m:,} m"},
        {"type": "latex", "content": rf"r = {R_ltx} + {hm_ltx} = {r_ltx}\ \mathrm{{m}}"},
    ]

    working_a = step_r + [
        {"type": "text",  "content": "Step 2 — apply Newton's Law of Gravitation:"},
        {"type": "latex", "content": r"F = \frac{GMm}{r^2}"},
        {"type": "latex", "content": rf"F = \frac{{6.67 \times 10^{{-11}} \times {M_ltx} \times {probe_mass}}}{{{r_ltx}^2}}"},
        {"type": "latex", "content": rf"F = {F_ltx}\ \mathrm{{N}}"},
    ]

    working_b = [
        {"type": "text",  "content": f"Using r = {_disp(r)} m from part (a):"},
        {"type": "latex", "content": r"g = \frac{GM}{r^2}"},
        {"type": "latex", "content": rf"g = \frac{{6.67 \times 10^{{-11}} \times {M_ltx}}}{{{r_ltx}^2}}"},
        {"type": "latex", "content": rf"g = {g_ltx}\ \mathrm{{N\ kg^{{-1}}}}"},
        {"type": "text",  "content": "Or equivalently using the force from part (a):"},
        {"type": "latex", "content": rf"g = \frac{{F}}{{m}} = \frac{{{F_ltx}}}{{{probe_mass}}} = {g_ltx}\ \mathrm{{N\ kg^{{-1}}}}"},
    ]

    # ── Part (a): gravitational force ──────────────────────────────────────────
    part_a = PhysicsQuestion(
        question_text=f"Calculate the gravitational force between the probe and {name}.",
        correct_answer=F,
        unit="N",
        topic="Our Dynamic Universe",
        question_type="Gravitation",
        level=level,
        distractors=[
            {
                "value": F_no_R,
                "mistake": (
                    f"You appear to have used r = h = {h_m:.2e} m instead of r = R + h. "
                    f"The orbital radius is measured from the **centre** of {name}: "
                    f"r = R + h = {R:.2e} + {h_m:.2e} = {r:.2e} m."
                ),
                "working": working_a,
            },
            {
                "value": F_no_conv,
                "mistake": (
                    f"You appear to have used the height in km without converting to metres. "
                    f"{h_km:,} km = {h_m:,} m. "
                    f"Using km values directly gives r ≈ {r_km_as_m:g} m instead of {r:.2e} m — "
                    f"a factor of 1000 error in r, causing a 10⁶ error in F."
                ),
                "working": working_a,
            },
        ],
        working=working_a,
        notes=_NOTES,
    )

    # ── Part (b): gravitational field strength ─────────────────────────────────
    part_b = PhysicsQuestion(
        question_text=f"Calculate the gravitational field strength of {name} at this orbital height.",
        correct_answer=g,
        unit="N/kg",
        topic="Our Dynamic Universe",
        question_type="Gravitation",
        level=level,
        distractors=[
            {
                "value": g_no_R,
                "mistake": (
                    f"You appear to have used r = h = {h_m:.2e} m. "
                    f"Remember r is measured from the centre of {name}: "
                    f"r = R + h = {r:.2e} m."
                ),
                "working": working_b,
            },
            {
                "value": g_no_conv,
                "mistake": (
                    f"The height must be in metres before calculating: "
                    f"{h_km:,} km = {h_m:,} m. "
                    f"Using km directly makes r 1000× too small and g 10⁶× too large."
                ),
                "working": working_b,
            },
        ],
        working=working_b,
        notes=_NOTES,
    )

    return PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic="Our Dynamic Universe",
        question_type="Gravitation",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part_a, part_b],
    )
