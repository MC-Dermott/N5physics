"""N5 Properties of Matter — exam-style questions that cut across the unit's topics, like SQA paper questions.

Recognised wrong answers follow the N5 marking instructions and course reports: °C used in the gas
laws, mass used instead of weight for pressure, one contact area used instead of the total, the
final temperature used for ΔT, fusion and vaporisation swapped, and the two heating stages not added.
"""
import random

from topics.exam_style.base import Exam, T, fmt, ltx, pick, sig

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
}


NOTES["Definitions"] = ""


def _ex(level):
    return Exam("Properties", level, NOTES)


# ════════════════ Pressure cooker: heating → gas law → force on the lid ════════════════

def pressure_cooker(level="N5"):
    ex = _ex(level)
    m, T0, P = pick(0.5, 0.8, 1.0, 1.2), pick(15, 18, 20), pick(1500, 2000, 2400)
    E = C_WATER * m * (100 - T0)
    ex.on("Heat").num(f"The cooker contains {m:g} kg of water at {T0} °C. Calculate the energy needed to heat it to 100 °C.", E, "J",
        wrong=[(C_WATER * m * 100, "ΔT = 100 − start temperature."), (m * L_VAP, "This is heating, not boiling: E = cmΔT.")],
        working=[rf"E_h = cm\Delta T = 4180 \times {m:g} \times {100 - T0} = {ltx(E)}\ \text{{J}}"])
    ex.on("Heat").num(f"The hob supplies {P} W. Calculate the minimum time to heat the water to 100 °C.", sig(E) / P, "s",
        wrong=[(sig(E) * P, "t = E ÷ P.")], working=[rf"t = \frac{{E}}{{P}} = \frac{{{ltx(E)}}}{{{P}}} = {ltx(sig(E) / P)}\ \text{{s}}"])
    p1, T1c, T2c = pick(100, 101), pick(20, 27), pick(110, 120, 127)
    T1, T2 = T1c + 273, T2c + 273
    p2 = p1 * T2 / T1
    ex.on("Gas Laws").num(f"The sealed lid traps air at {p1} kPa and {T1c} °C. Calculate the pressure of this air when heated to {T2c} °C at constant volume.",
        p2, "kPa", wrong=[(p1 * T2c / T1c, "Use kelvin: K = °C + 273."), (p1 * T1 / T2, "Heating increases the pressure.")],
        working=[r"\frac{p_1}{T_1} = \frac{p_2}{T_2}", rf"p_2 = {p1} \times \frac{{{T2}}}{{{T1}}} = {ltx(p2)}\ \text{{kPa}}"],
        scaffold=[("T₁ in K?", T1, "K"), ("T₂ in K?", T2, "K")])
    A = pick(0.03, 0.04, 0.05)
    F = sig(p2) * 1000 * A
    ex.on("Pressure").num(f"The lid has an area of {A:g} m². Calculate the force on the lid from the air inside.", F, "N",
        wrong=[(sig(p2) * A, "Convert kPa to Pa (× 1000)."), (sig(p2) * 1000 / A, "F = p × A.")],
        working=[rf"F = pA = {ltx(p2)} \times 10^3 \times {A:g} = {ltx(F)}\ \text{{N}}"])
    ex.on("Gas Laws").choice("Use the kinetic model to explain why the pressure of the trapped air increases.",
        "The particles move faster, so they hit the walls more often and with more force.",
        [("The particles expand.", "Particles don't get bigger."), ("There are more particles.", "The cooker is sealed."),
         ("The particles hit the walls less often but harder.", "More often AND harder.")])
    return ex.build("A pressure cooker is used to cook food quickly. (c_water = 4180 J/kg°C)")


# ════════════════ Bicycle tyre: pressure on road → hot day → pumping ════════════════

def bike_tyre(level="N5"):
    ex = _ex(level)
    m, A_cm2 = pick(75, 85, 95), pick(8, 10, 12)
    W = m * G
    A = 2 * A_cm2 / 1e4
    p = sig(W) / A
    ex.on("Pressure").num(f"The cyclist and bike have a total mass of {m} kg. Each of the two tyres has {A_cm2} cm² in contact with the road. "
        f"Calculate the pressure on the road.", p, "Pa",
        wrong=[(sig(W) / (A_cm2 / 1e4), "Use the TOTAL area of both tyres."), (m / A, "Use the weight (mg), not the mass."),
               (sig(W) / (2 * A_cm2), "Convert cm² to m² (÷ 10 000).")],
        working=[rf"W = mg = {m} \times 9.8 = {ltx(W)}\ \text{{N}}", rf"A = 2 \times {A_cm2}\ \text{{cm}}^2 = {A:g}\ \text{{m}}^2",
                 rf"p = \frac{{F}}{{A}} = {ltx(p)}\ \text{{Pa}}"],
        scaffold=[("Weight, in N?", W, "N"), ("Total area, in m²?", A, "m²")])
    p1, T1c, T2c = pick(300, 350, 400), pick(10, 12, 15), pick(30, 35, 40)
    p2 = p1 * (T2c + 273) / (T1c + 273)
    ex.on("Gas Laws").num(f"The tyre pressure is {p1} kPa at {T1c} °C. On a hot day the air inside reaches {T2c} °C. Calculate the new pressure "
        f"(the volume is constant).", p2, "kPa",
        wrong=[(p1 * T2c / T1c, "Use kelvin temperatures."), (p1 * (T1c + 273) / (T2c + 273), "Heating increases the pressure.")],
        working=[rf"p_2 = {p1} \times \frac{{{T2c + 273}}}{{{T1c + 273}}} = {ltx(p2)}\ \text{{kPa}}"])
    V1, V2 = random.choice([(300, 100), (240, 80), (450, 150), (200, 50)])
    ex.on("Gas Laws").num(f"A pump squeezes {V1} cm³ of air at 100 kPa into {V2} cm³ at constant temperature. Calculate the new pressure.",
        100 * V1 / V2, "kPa", wrong=[(100 * V2 / V1, "Smaller volume → HIGHER pressure: p₂ = p₁V₁ ÷ V₂.")],
        working=[rf"p_1V_1 = p_2V_2 \Rightarrow p_2 = \frac{{100 \times {V1}}}{{{V2}}} = {ltx(100 * V1 / V2)}\ \text{{kPa}}"])
    ex.on("Gas Laws").choice("Why does the pressure increase when the air is squeezed into a smaller volume (same temperature)?",
        "The particles hit the walls more often, because they have less space.",
        [("The particles move faster.", "At constant temperature their speed doesn't change."),
         ("The particles get smaller.", "Particle size doesn't change."), ("The particles hit the walls with less force.", "Same force, more often.")])
    return ex.build("A cyclist checks the tyres on their bike.")


# ════════════════ Ice and steam: cooling → freezing → boiling ════════════════

def ice_and_steam(level="N5"):
    ex = _ex(level)
    m, T0, P = pick(0.2, 0.25, 0.4, 0.5), pick(15, 18, 20, 22), pick(80, 100, 120, 150)
    E1 = C_WATER * m * T0
    ex.on("Heat").num(f"An ice maker cools {m:g} kg of water from {T0} °C to 0 °C. Calculate the energy removed.", E1, "J",
        wrong=[(m * L_FUS, "Cooling to 0 °C uses E = cmΔT; freezing comes next."), (C_WATER * m * (T0 + 273), "ΔT is the change: T₀ − 0.")],
        working=[rf"E_h = cm\Delta T = 4180 \times {m:g} \times {T0} = {ltx(E1)}\ \text{{J}}"])
    E2 = m * L_FUS
    ex.on("Heat").num("Calculate the energy removed to freeze the water at 0 °C.", E2, "J",
        wrong=[(m * L_VAP, "Freezing uses the latent heat of FUSION."), (C_WATER * m, "Freezing is a change of state: E = ml.")],
        working=[rf"E_h = ml = {m:g} \times 3.34\times10^5 = {ltx(E2)}\ \text{{J}}"])
    t = (sig(E1) + sig(E2)) / P
    ex.on("Heat").num(f"The ice maker removes energy at {P} W. Calculate the minimum time for the whole process.", t, "s",
        wrong=[(sig(E2) / P, "ADD the energy for cooling and freezing."), ((sig(E1) + sig(E2)) * P, "t = E ÷ P.")],
        working=[rf"E = {ltx(E1)} + {ltx(E2)} = {ltx(sig(E1) + sig(E2))}\ \text{{J}}", rf"t = \frac{{E}}{{P}} = {ltx(t)}\ \text{{s}}"])
    ex.on("Heat").choice("Why does the temperature stay at 0 °C while the water freezes, even though energy is still being removed?",
        "The energy removed comes from the change of state (bonds forming between particles), not from a fall in temperature.",
        [("No energy is removed while it freezes.", "Energy is still removed — that's the latent heat."),
         ("The thermometer stops working at 0 °C.", "It's a real effect: latent heat."),
         ("The particles stop moving.", "They still vibrate; the energy change is in the bonds.")])
    return ex.build("A freezer makes ice from tap water. (c_water = 4180 J/kg°C, l_fusion = 3.34 × 10⁵ J/kg)")


SCENARIOS = {
    "Pressure Cooker": pressure_cooker,
    "Bicycle Tyre":    bike_tyre,
    "Ice and Steam":   ice_and_steam,
}
