"""N5 Properties of Matter and Skills — exam-style multi-part questions.

Recognised wrong answers follow the N5 marking instructions and course reports: °C used in the gas
laws, mass used instead of weight for pressure, one contact area used instead of the total, the
final temperature used for ΔT, fusion and vaporisation swapped, and prefixes misread.
"""
import random

from topics.exam_style.base import Exam, T, exam_style, fmt, ltx, pick, reuse, sig
from topics.properties.heat import generate_heat_exam_icemachine

G = 9.8
C_WATER, L_FUS, L_VAP = 4180, 3.34e5, 22.6e5

NOTES = {
    "Pressure": r"""## Pressure — exam technique

$p = \frac{F}{A}$ — pressure in pascals (Pa = N/m²).

- The force on the ground is the **weight**: $W = mg$ — not the mass.
- Use the **total** contact area (all feet / wheels / legs). Convert cm² → m² (÷ 10 000).
- Bigger area → smaller pressure (snowshoes, wide tyres); smaller area → bigger pressure (knives, stilettos).
""",
    "Gas Laws": r"""## Gas laws — exam technique

$p_1V_1 = p_2V_2$ &nbsp; $\frac{p_1}{T_1} = \frac{p_2}{T_2}$ &nbsp; $\frac{V_1}{T_1} = \frac{V_2}{T_2}$ &nbsp; $\frac{p_1V_1}{T_1} = \frac{p_2V_2}{T_2}$

- Temperatures in **kelvin**: K = °C + 273.
- Kinetic model: heating → particles move **faster** → hit the walls **more often** and **with more force** → greater pressure.
- Smaller volume (same temperature) → particles hit the walls **more often** → greater pressure.
""",
    "Heat": r"""## Heat — exam technique

$E_h = cm\Delta T$ &nbsp; $E_h = ml$ &nbsp; $P = \frac{E}{t}$ — $c_{water} = 4180$ J/kg°C, $l_{fusion} = 3.34\times10^5$ J/kg, $l_{vaporisation} = 22.6\times10^5$ J/kg.

- ΔT is the **change** in temperature.
- Melting/freezing → **fusion**; boiling/condensing → **vaporisation**.
- Real heating takes longer than calculated: heat is **lost to the surroundings**.
""",
    "Scientific Prefixes": r"""## Prefixes — exam technique

| Prefix | Symbol | × |
|---|---|---|
| giga | G | 10⁹ |
| mega | M | 10⁶ |
| kilo | k | 10³ |
| milli | m | 10⁻³ |
| micro | μ | 10⁻⁶ |
| nano | n | 10⁻⁹ |

Convert every quantity to the base unit **before** substituting into a relationship.
""",
}


def _ex(qtype, level, unit="Properties"):
    return Exam(unit, qtype, level, NOTES[qtype])


# ════════════════ Pressure ════════════════

def _pressure_snow(level="N5"):
    ex = _ex("Pressure", level)
    m = pick(55, 60, 68, 75, 82)
    a_boot = pick(0.025, 0.03, 0.035)
    a_shoe = pick(0.12, 0.15, 0.18)
    W = m * G
    ex.num("Calculate the weight of the walker.", W, "N", wrong=[(m, "Weight = mg."), (m / G, "W = m × g.")],
           working=[rf"W = mg = {m} \times 9.8 = {ltx(W)}\ \text{{N}}"])
    p = W / (2 * a_boot)
    ex.num(f"Standing on both feet, each boot has an area of {a_boot:g} m² in contact with the snow. Calculate the pressure on the snow.",
           p, "Pa",
           wrong=[(W / a_boot, "Use the TOTAL area of both boots."), (m / (2 * a_boot), "Use the weight (N), not the mass."),
                  (W * 2 * a_boot, "p = F ÷ A.")],
           working=[rf"A = 2 \times {a_boot:g} = {ltx(2 * a_boot)}\ \text{{m}}^2", r"p = \frac{F}{A}", rf"p = \frac{{{ltx(W)}}}{{{ltx(2 * a_boot)}}} = {ltx(p)}\ \text{{Pa}}"])
    p2 = W / (2 * a_shoe)
    ex.num(f"The walker puts on snowshoes, each of area {a_shoe:g} m². Calculate the new pressure on the snow.", p2, "Pa",
           wrong=[(W / a_shoe, "Use the TOTAL area of both snowshoes.")],
           working=[rf"p = \frac{{{ltx(W)}}}{{2 \times {a_shoe:g}}} = {ltx(p2)}\ \text{{Pa}}"])
    ex.choice("Why do snowshoes stop the walker sinking into the snow?",
              "They spread the same weight over a larger area, so the pressure on the snow is smaller.",
              [("They reduce the walker's weight.", "The weight is unchanged."), ("They increase the pressure on the snow.", "Larger area → smaller pressure."),
               ("They reduce the walker's mass.", "Mass is unchanged.")])
    return ex.build(f"A walker of mass {m} kg crosses deep snow.")


def _pressure_tyres(level="N5"):
    ex = _ex("Pressure", level)
    p_k = pick(200, 220, 240, 250)
    A_cm2 = pick(120, 150, 160, 180)
    A = A_cm2 / 10000
    F = p_k * 1000 * A
    ex.num(f"Each tyre has a pressure of {p_k} kPa and {A_cm2} cm² in contact with the road. Calculate the force on the road from one tyre.",
           F, "N",
           wrong=[(p_k * A, "Convert kPa to Pa (× 1000)."), (p_k * 1000 * A_cm2, "Convert cm² to m² (÷ 10 000)."),
                  (p_k * 1000 / A, "F = p × A.")],
           working=[rf"A = {A_cm2}\ \text{{cm}}^2 = {A:g}\ \text{{m}}^2", r"p = \frac{F}{A} \Rightarrow F = pA", rf"F = {p_k} \times 10^3 \times {A:g} = {ltx(F)}\ \text{{N}}"],
           scaffold=[("Area in m²?", A, "m²")])
    W = 4 * F
    ex.num("The car has four identical tyres. Calculate the weight of the car.", W, "N", wrong=[(F, "Add the force from all four tyres.")],
           working=[rf"W = 4 \times {ltx(F)} = {ltx(W)}\ \text{{N}}"])
    m = W / G
    ex.num("Calculate the mass of the car.", m, "kg", wrong=[(W * G, "m = W ÷ g.")],
           working=[rf"m = \frac{{W}}{{g}} = \frac{{{ltx(W)}}}{{9.8}} = {ltx(m)}\ \text{{kg}}"])
    return ex.build("A car rests on a level road. The pressure inside each tyre is equal to the pressure the tyre exerts on the road.")


gen_pressure_exam = exam_style(_pressure_snow, _pressure_tyres)


# ════════════════ Gas Laws ════════════════

def _gas_can(level="N5"):
    ex = _ex("Gas Laws", level)
    p1 = pick(100, 120, 150, 200, 250)
    T1c, T2c = pick(15, 17, 20, 27), pick(60, 77, 90, 127)
    T1, T2 = T1c + 273, T2c + 273
    ex.num(f"Convert {T2c} °C to kelvin.", T2, "K", wrong=[(T2c - 273, "Add 273 to convert °C to K.")],
           working=[rf"T = {T2c} + 273 = {T2}\ \text{{K}}"])
    p2 = p1 * T2 / T1
    ex.num(f"The can is heated from {T1c} °C to {T2c} °C. Calculate the new pressure of the gas.", p2, "kPa",
           wrong=[(p1 * T2c / T1c, "Use kelvin temperatures."), (p1 * T1 / T2, "Heating at constant volume INCREASES the pressure.")],
           working=[r"\frac{p_1}{T_1} = \frac{p_2}{T_2}", rf"\frac{{{p1}}}{{{T1}}} = \frac{{p_2}}{{{T2}}}", rf"p_2 = {ltx(p2)}\ \text{{kPa}}"],
           scaffold=[("T₁ in kelvin?", T1, "K")])
    ex.choice("Use the kinetic model to explain why the pressure increases.",
              "The gas particles gain kinetic energy and move faster, so they hit the walls more often and with greater force.",
              [("The gas particles expand and push on the walls.", "Particles don't get bigger."),
               ("There are more gas particles in the can.", "The can is sealed — same number of particles."),
               ("The particles hit the walls less often but harder.", "They hit MORE often and harder.")])
    return ex.build(f"An aerosol can contains gas at a pressure of {p1} kPa at {T1c} °C. The volume of the can is constant.")


def _gas_syringe(level="N5"):
    ex = _ex("Gas Laws", level)
    p1 = pick(100, 101)
    V1, V2 = random.choice([(50, 20), (60, 40), (40, 25), (30, 12), (80, 50)])
    p2 = p1 * V1 / V2
    ex.num(f"The plunger is pushed in slowly until the volume is {V2} cm³. Calculate the new pressure.", p2, "kPa",
           wrong=[(p1 * V2 / V1, "Decreasing the volume INCREASES the pressure: p₂ = p₁V₁ ÷ V₂."), (p1, "The pressure changes.")],
           working=[r"p_1V_1 = p_2V_2", rf"{p1} \times {V1} = p_2 \times {V2}", rf"p_2 = {ltx(p2)}\ \text{{kPa}}"])
    p3 = pick(150, 200, 250)
    V3 = p1 * V1 / p3
    ex.num(f"Calculate the volume when the pressure is {p3} kPa.", V3, "cm³",
           wrong=[(p3 * V1 / p1, "p₁V₁ = p₃V₃ → V₃ = p₁V₁ ÷ p₃.")],
           working=[rf"V_3 = \frac{{p_1V_1}}{{p_3}} = \frac{{{p1} \times {V1}}}{{{p3}}} = {ltx(V3)}\ \text{{cm}}^3"])
    ex.choice("Why must the plunger be pushed in slowly?",
              "So the temperature of the gas stays constant.",
              [("So the mass of the gas increases.", "The syringe is sealed — the mass is constant."),
               ("So the pressure stays constant.", "The pressure is what's being measured as it changes."),
               ("So the particles stop moving.", "The particles keep moving; the temperature must stay constant.")])
    ex.choice("Use the kinetic model to explain why the pressure increases as the volume decreases.",
              "The particles have less space, so they hit the walls more often (with the same force each time).",
              [("The particles move faster.", "At constant temperature their speed is unchanged."),
               ("The particles get smaller.", "Particle size doesn't change."),
               ("The particles hit the walls with less force.", "Same force per collision; more frequent collisions.")])
    return ex.build(f"A sealed syringe contains {V1} cm³ of air at {p1} kPa. The temperature of the air stays constant.")


def _gas_balloon(level="N5"):
    ex = _ex("Gas Laws", level)
    V1 = pick(2.0, 2.4, 3.0, 4.5)
    T1c, T2c = pick(-10, 0, 5), pick(20, 25, 27, 30)
    T1, T2 = T1c + 273, T2c + 273
    V2 = V1 * T2 / T1
    ex.num(f"A balloon has a volume of {V1:g} m³ at {T1c} °C. It is warmed to {T2c} °C at constant pressure. Calculate its new volume.",
           V2, "m³",
           wrong=[(V1 * T1 / T2, "Warming at constant pressure INCREASES the volume.")]
                 + ([(V1 * T2c / T1c, "Use kelvin temperatures.")] if T1c > 0 else []),
           working=[r"\frac{V_1}{T_1} = \frac{V_2}{T_2}", rf"\frac{{{V1:g}}}{{{T1}}} = \frac{{V_2}}{{{T2}}}", rf"V_2 = {ltx(V2)}\ \text{{m}}^3"],
           scaffold=[("T₁ in K?", T1, "K"), ("T₂ in K?", T2, "K")])
    ex.choice("What is absolute zero?",
              "0 K (−273 °C) — the temperature at which the particles have their minimum kinetic energy (stop moving).",
              [("0 °C — the temperature at which water freezes.", "Absolute zero is −273 °C."),
               ("−100 °C — the coldest temperature on Earth.", "Absolute zero is 0 K = −273 °C."),
               ("273 K — the lowest temperature of any gas.", "273 K is 0 °C.")])
    rise = T2c - T1c
    ex.num("State the temperature rise of the air in kelvin.", rise, "K",
           wrong=[(rise + 273, "A temperature CHANGE is the same in K and °C."), (T2, "That's the final temperature.")],
           working=[rf"\Delta T = {T2c} - ({T1c}) = {rise}\ \text{{°C}} = {rise}\ \text{{K}}"])
    return ex.build("Air in a balloon is warmed by the Sun.")


gen_gas_laws_exam = exam_style(_gas_can, _gas_syringe, _gas_balloon)


# ════════════════ Heat ════════════════

def _heat_kettle(level="N5"):
    ex = _ex("Heat", level)
    m, T0 = pick(0.5, 0.8, 1.0, 1.2, 1.5), pick(12, 15, 18, 20)
    P = pick(2000, 2200, 2400, 3000)
    dT = 100 - T0
    E = C_WATER * m * dT
    ex.num(f"Calculate the energy needed to heat the water to 100 °C.", E, "J",
           wrong=[(C_WATER * m * 100, "ΔT is the CHANGE in temperature (100 − start)."), (C_WATER * m * T0, "ΔT = 100 − start temperature."),
                  (m * L_VAP, "This is heating, not boiling — use E = cmΔT.")],
           working=[r"E_h = cm\Delta T", rf"E_h = 4180 \times {m:g} \times ({100} - {T0})", rf"E_h = {ltx(E)}\ \text{{J}}"])
    t = sig(E) / P
    ex.num("Calculate the minimum time for the kettle to heat the water to 100 °C.", t, "s",
           wrong=[(E * P, "t = E ÷ P."), (P / E, "t = E ÷ P.")],
           working=[r"P = \frac{E}{t} \Rightarrow t = \frac{E}{P}", rf"t = \frac{{{ltx(E)}}}{{{P}}} = {ltx(t)}\ \text{{s}}"])
    ex.choice("The kettle actually takes longer than this. Why?",
              "Heat is lost to the surroundings (and used to heat the kettle itself).",
              [("Heat loss.", "Too vague — say heat is lost TO THE SURROUNDINGS."),
               ("The water gains heat from the surroundings.", "The water is hotter than its surroundings — it loses heat."),
               ("The kettle's power increases as the water heats up.", "The power is constant.")])
    return ex.build(f"A {P} W kettle contains {m:g} kg of water at {T0} °C. (c_water = 4180 J/kg°C)")


def _heat_boil(level="N5"):
    ex = _ex("Heat", level)
    m, T0 = pick(0.3, 0.4, 0.5, 0.6), pick(15, 18, 20)
    ms = sig(m * pick(0.1, 0.2, 0.25), 2)
    P = pick(1500, 2000, 2500)
    E1 = C_WATER * m * (100 - T0)
    E2 = ms * L_VAP
    ex.num("Calculate the energy needed to heat the water to its boiling point.", E1, "J",
           wrong=[(C_WATER * m * 100, "ΔT = 100 − start temperature.")],
           working=[rf"E_h = cm\Delta T = 4180 \times {m:g} \times {100 - T0} = {ltx(E1)}\ \text{{J}}"])
    ex.num(f"{ms:g} kg of the water then boils away. Calculate the energy needed for this.", E2, "J",
           wrong=[(ms * L_FUS, "Boiling uses the latent heat of VAPORISATION."), (m * L_VAP, f"Only {ms:g} kg boils away.")],
           working=[rf"E_h = ml = {ms:g} \times 22.6 \times 10^5 = {ltx(E2)}\ \text{{J}}"])
    t = (sig(E1) + sig(E2)) / P
    ex.num("Calculate the total time the heater is switched on.", t, "s",
           wrong=[(sig(E2) / P, "Include the time to heat the water first — add both energies."), (abs(sig(E2) - sig(E1)) / P, "ADD the two energies."),
                  ((sig(E1) + sig(E2)) * P, "t = E ÷ P.")],
           working=[rf"E = {ltx(E1)} + {ltx(E2)} = {ltx(E1 + E2)}\ \text{{J}}", rf"t = \frac{{E}}{{P}} = {ltx(t)}\ \text{{s}}"])
    return ex.build(f"A {P} W heater heats {m:g} kg of water from {T0} °C until some of it boils away. "
                    f"(c_water = 4180 J/kg°C, l_vaporisation = 22.6 × 10⁵ J/kg)")


gen_heat_exam = exam_style(_heat_kettle, _heat_boil, reuse(generate_heat_exam_icemachine, qtype="Heat"))


# ════════════════ Scientific Prefixes (Skills) ════════════════

def _prefix_wifi(level="N5"):
    ex = Exam("Skills", "Scientific Prefixes", level, NOTES["Scientific Prefixes"])
    f_G = pick(2.4, 5.0, 5.8)
    f = f_G * 1e9
    ex.num(f"A Wi-Fi router transmits at {f_G:g} GHz. Write this frequency in hertz.", f, "Hz",
           wrong=[(f_G * 1e6, "giga (G) = 10⁹, not 10⁶."), (f_G * 1e3, "giga (G) = 10⁹.")],
           working=[rf"{f_G:g}\ \text{{GHz}} = {f_G:g} \times 10^9\ \text{{Hz}}"])
    lam = 3e8 / f
    ex.num("Calculate the wavelength of the signal (speed = 3.0 × 10⁸ m/s).", lam, "m",
           wrong=[(3e8 / (f_G * 1e6), "Use 10⁹ for giga."), (3e8 / f_G, "Convert GHz to Hz first.")],
           working=[rf"\lambda = \frac{{v}}{{f}} = \frac{{3 \times 10^8}}{{{f_G:g} \times 10^9}} = {ltx(lam)}\ \text{{m}}"])
    ex.num("Write this wavelength in millimetres.", lam * 1000, "mm",
           wrong=[(lam * 1e6, "1 m = 1000 mm (milli = 10⁻³)."), (lam / 1000, "Multiply by 1000 to go from m to mm.")],
           working=[rf"{ltx(lam)}\ \text{{m}} = {ltx(lam * 1000)}\ \text{{mm}}"])
    return ex.build("Wireless devices use microwaves to send data.")


def _prefix_sensor(level="N5"):
    ex = Exam("Skills", "Scientific Prefixes", level, NOTES["Scientific Prefixes"])
    I_u, t_ms = pick(25, 40, 50, 80), pick(2, 5, 8)
    Q = I_u * 1e-6 * t_ms * 1e-3
    ex.num(f"The sensor draws a current of {I_u} μA. Write this current in amperes.", I_u * 1e-6, "A",
           wrong=[(I_u * 1e-3, "micro (μ) = 10⁻⁶; milli (m) = 10⁻³."), (I_u * 1e-9, "micro = 10⁻⁶, nano = 10⁻⁹.")],
           working=[rf"{I_u}\ \mu\text{{A}} = {I_u} \times 10^{{-6}}\ \text{{A}}"])
    ex.num(f"Each reading takes {t_ms} ms. Calculate the charge used in one reading (Q = It).", Q, "C",
           wrong=[(I_u * t_ms, "Convert μA and ms to A and s first."), (I_u * 1e-6 * t_ms, "Convert ms to s (× 10⁻³).")],
           working=[rf"Q = It = ({I_u} \times 10^{{-6}}) \times ({t_ms} \times 10^{{-3}}) = {ltx(Q)}\ \text{{C}}"])
    ex.choice("Which prefix means × 10⁻⁹?", "nano (n)",
              [("micro (μ)", "micro = 10⁻⁶."), ("milli (m)", "milli = 10⁻³."), ("mega (M)", "mega = 10⁶.")])
    return ex.build("A battery-powered sensor takes readings in a weather station.")


gen_prefixes_exam = exam_style(_prefix_wifi, _prefix_sensor)


EXAM = {
    "Pressure": gen_pressure_exam,
    "Gas Laws": gen_gas_laws_exam,
    "Heat":     gen_heat_exam,
}

SKILLS_EXAM = {
    "Scientific Prefixes": gen_prefixes_exam,
}
