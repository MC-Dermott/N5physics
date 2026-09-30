"""N5 Properties of Matter — exam-style question types from the past-paper/course-report worksheets.

Mirrors N5phys Specific_Heat_Capacity, Specific_Latent_Heat and Gas_Laws_and_the_Kinetic_Model. The
older generators (pressure, gas_laws, heat) drill one-step calculations; these add the styles SQA
sets, with distractors from the N5 course reports 2023–2025 and marking instructions: °C used in
the gas laws, 273 added to a temperature change, mass used for weight / one foot's area, fusion and
vaporisation latent heats swapped, the two heating stages subtracted, the final temperature used as
ΔT, and kinetic-model explanations that talk about particles getting bigger.
"""
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

TOPIC = "Properties"
C_WATER, L_FUS, L_VAP = 4180, 3.34e5, 22.6e5
_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

_NOTES = r"""
## N5 Properties of Matter — exam technique

**Relationships:** $E_h = cm\Delta T$ &nbsp; $E_h = ml$ &nbsp; $P = \frac{E}{t}$ &nbsp; $p = \frac{F}{A}$ &nbsp;
$p_1V_1 = p_2V_2$ &nbsp; $\frac{p_1}{T_1} = \frac{p_2}{T_2}$ &nbsp; $\frac{V_1}{T_1} = \frac{V_2}{T_2}$ &nbsp; $\frac{p_1V_1}{T_1} = \frac{p_2V_2}{T_2}$

Data sheet: $c_{water} = 4180$ J kg⁻¹ °C⁻¹, $l_{fusion}$ (ice) $= 3.34\times10^5$ J kg⁻¹, $l_{vaporisation}$ (water) $= 22.6\times10^5$ J kg⁻¹.

**Common errors (course reports and marking instructions):**
- Gas-law temperatures in **kelvin** (+273). A temperature **change** is the same in K and °C.
- Pressure: use the **weight** (W = mg) and the **total** contact area (two feet, three fins).
- ΔT is the **change** in temperature. Melting/freezing → **fusion**; boiling/condensing → **vaporisation**.
- Heating then boiling: **add** the two energies.
- Kinetic model: particles move faster → hit the walls **more often** and with **more force** → greater pressure. They don't get bigger.
- ‘Heat loss’ on its own isn't accepted — say heat is lost **to the surroundings**.
"""


def _sig(x, sf=3):
    return float(f"{x:.{sf}g}")


def _txt(x, sf=3):
    x = _sig(x, sf)
    if x == 0 or 0.01 <= abs(x) < 1e5:
        return f"{x:g}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    return f"{coeff} × 10{str(int(exp)).translate(_SUP)}"


def _ltx(x, sf=3):
    x = _sig(x, sf)
    if x == 0 or 0.01 <= abs(x) < 1e5:
        return f"{x:g}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    return rf"{coeff} \times 10^{{{int(exp)}}}"


def _L(s):
    return {"type": "latex", "content": s}


def _T(s):
    return {"type": "text", "content": s}


def _q(text, answer, unit, options, qtype, scaffold=None, level="N5"):
    kept = []
    for o in options:
        o.setdefault("display", f"{_txt(o['value'])} {unit}".strip())
        if all(abs(o["value"] - k["value"]) > 0.02 * max(abs(o["value"]), abs(k["value"])) for k in kept):
            kept.append(o)
    return make_question(text, answer, kept, unit, scaffold=scaffold, notes=_NOTES,
                         topic=TOPIC, question_type=qtype, level=level)


def _choice(text, correct, wrong, qtype, level="N5"):
    distractors = [{"value": w, "mistake": why, "working": []} for w, why in wrong]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(question_text=text, correct_answer=correct, unit="", distractors=distractors,
                           working=[], notes=_NOTES, topic=TOPIC, question_type=qtype, level=level,
                           metadata={"type": "classification", "options": options})


# ════════════════ Heat ════════════════
# (context, mass lo, hi (kg), start temp lo, hi (°C))
_WATER = [("a baby bottle", 0.015, 0.030, 4, 10), ("a hot water dispenser", 0.20, 0.30, 15, 22),
          ("a kettle", 0.50, 1.5, 12, 20), ("a pan on a stove", 0.8, 2.0, 12, 20)]


def gen_pm_heat_then_boil(level="N5"):
    ctx, mlo, mhi, tlo, thi = random.choice(_WATER)
    m = round(random.uniform(mlo, mhi), 3 if mhi < 0.1 else 2)
    T0 = random.randint(tlo, thi)
    frac = random.choice([0.2, 0.3, 0.5, 0.7])
    ms = _sig(m * frac, 2)
    E1 = C_WATER * m * (100 - T0)
    E2 = ms * L_VAP
    Et = E1 + E2
    text = (f"Water of mass {m:g} kg in {ctx} is heated from {T0} °C to 100 °C, and then {ms:g} kg of it is changed to steam. "
            f"Calculate the total energy needed.")
    work = [_L(rf"E_h = cm\Delta T = 4180 \times {m:g} \times {100 - T0} = {_ltx(E1)}\ \mathrm{{J}}"),
            _L(rf"E_h = ml = {ms:g} \times 22.6\times10^5 = {_ltx(E2)}\ \mathrm{{J}}"), _L(rf"E_{{total}} = {_ltx(Et)}\ \mathrm{{J}}")]
    opts = [{"value": _sig(Et), "mistake": None, "working": work},
            {"value": _sig(abs(E2 - E1)), "mistake": "Both stages need energy — ADD them (course report 2024).", "working": work},
            {"value": _sig(C_WATER * m * 100 + E2), "mistake": "ΔT is the CHANGE in temperature (100 − start).", "working": work},
            {"value": _sig(E1 + ms * L_FUS), "mistake": "Boiling needs the latent heat of VAPORISATION.", "working": work}]
    scaffold = [{"question": "Energy to heat the water to 100 °C, in J?", "answer": _sig(E1)},
                {"question": "Energy to change the water to steam, in J?", "answer": _sig(E2)},
                {"question": "Total energy, in J?", "answer": _sig(Et)}]
    return _q(text, _sig(Et), "J", opts, "Heat", scaffold, level)


def gen_pm_latent_power(level="N5"):
    freezing = random.random() < 0.5
    if freezing:
        P = random.choice([80, 100, 115, 120, 150])
        m = random.choice([0.10, 0.20, 0.25, 0.38])
        E = m * L_FUS
        t = E / P
        text = f"A {P} W ice maker freezes {m:g} kg of water at 0 °C. Calculate the minimum time this takes."
        work = [_L(rf"E_h = ml = {m:g} \times 3.34\times10^5 = {_ltx(E)}\ \mathrm{{J}}"), _L(rf"t = \frac{{E}}{{P}} = {_ltx(t)}\ \mathrm{{s}}")]
        opts = [{"value": _sig(t), "mistake": None, "working": work},
                {"value": _sig(m * L_VAP / P), "mistake": "Freezing uses the latent heat of FUSION.", "working": work},
                {"value": _sig(E * P), "mistake": "t = E ÷ P.", "working": work}]
    else:
        P = random.choice([750, 1130, 2000, 2500])
        mins = random.choice([2, 3, 4, 5])
        t = mins * 60
        E = P * t
        m = E / L_VAP
        text = f"A {P} W heater keeps water boiling for {mins} minutes. Calculate the maximum mass of water changed to steam."
        work = [_L(rf"E = Pt = {P} \times {t} = {_ltx(E)}\ \mathrm{{J}}"), _L(rf"m = \frac{{E}}{{l}} = {_ltx(m)}\ \mathrm{{kg}}")]
        opts = [{"value": _sig(m), "mistake": None, "working": work},
                {"value": _sig(E / L_FUS), "mistake": "Boiling uses the latent heat of VAPORISATION.", "working": work},
                {"value": _sig(P * mins / L_VAP), "mistake": "The time must be in seconds.", "working": work}]
    scaffold = [{"question": "Energy involved, in J?", "answer": _sig(E)}, {"question": "Final answer?", "answer": opts[0]["value"]}]
    return _q(text, opts[0]["value"], "s" if freezing else "kg", opts, "Heat", scaffold, level)


def gen_pm_heating_curve(level="N5"):
    kind = random.choice(["fusion", "vaporisation", "flat", "state"])
    base = "A solid is heated steadily. Its heating curve rises (P→Q), is flat (Q→R), rises (R→S), is flat (S→T), then rises (T→U)."
    if kind == "fusion":
        return _choice(base + " Which section is used to find the specific latent heat of fusion?", "Q→R",
                       [("S→T", "That's boiling — vaporisation (course report 2024)."), ("R→S", "The temperature is rising — that's heating the liquid."),
                        ("P→Q", "That's heating the solid.")], "Heat", level)
    if kind == "vaporisation":
        return _choice(base + " Which section is used to find the specific latent heat of vaporisation?", "S→T",
                       [("Q→R", "That's melting — fusion (course report 2024)."), ("T→U", "That's heating the gas."), ("R→S", "That's heating the liquid.")], "Heat", level)
    if kind == "flat":
        return _choice("Why does the temperature stay constant while a substance melts, even though energy is still supplied?",
                       "The energy is used to change the state (separate the particles), not to raise the temperature.",
                       [("No energy is being supplied during melting.", "The heater is still on — energy is being supplied."),
                        ("The energy is lost to the surroundings.", "The energy goes into changing the state."),
                        ("The particles stop moving.", "The particles keep moving; the energy breaks the bonds.")], "Heat", level)
    return _choice("Why is a measured value of specific heat capacity usually larger than the data-sheet value?",
                   "Heat is lost to the surroundings, so more energy is supplied than goes into the substance.",
                   [("Because of heat loss.", "Too vague — the marking instructions need you to say heat is lost TO THE SURROUNDINGS."),
                    ("The thermometer is inaccurate.", "That wouldn't consistently make c too large."),
                    ("The substance gains heat from the surroundings.", "When heating, heat is LOST to the surroundings.")], "Heat", level)


# ════════════════ Gas laws and pressure ════════════════
def gen_pm_gas_kelvin(level="N5"):
    kind = random.choice(["pT", "VT", "combined"])
    T1c = random.choice([15, 17, 20, 21, 27])
    T2c = T1c + random.choice([15, 20, 25, 30, 40])
    T1, T2 = T1c + 273, T2c + 273
    if kind == "pT":
        p1 = random.choice([120, 150, 190, 200, 250])
        ans = p1 * T2 / T1
        text = f"A sealed container of gas is at {p1} kPa and {T1c} °C. It is heated to {T2c} °C at constant volume. Calculate the new pressure."
        work = [_L(r"\frac{p_1}{T_1} = \frac{p_2}{T_2}"), _L(rf"\frac{{{p1}}}{{{T1}}} = \frac{{p_2}}{{{T2}}}"), _L(rf"p_2 = {_ltx(ans)}\ \mathrm{{kPa}}")]
        opts = [{"value": _sig(ans), "mistake": None, "working": work},
                {"value": _sig(p1 * T2c / T1c), "mistake": "Temperatures must be in kelvin (course report 2025).", "working": work},
                {"value": _sig(p1 * T1 / T2), "mistake": "Heating at constant volume INCREASES the pressure.", "working": work}]
        unit = "kPa"
    elif kind == "VT":
        V1 = random.choice([0.20, 0.30, 0.45, 2.5])
        ans = V1 * T2 / T1
        text = f"A gas has a volume of {V1:g} m³ at {T1c} °C. It is heated to {T2c} °C at constant pressure. Calculate the new volume."
        work = [_L(r"\frac{V_1}{T_1} = \frac{V_2}{T_2}"), _L(rf"\frac{{{V1:g}}}{{{T1}}} = \frac{{V_2}}{{{T2}}}"), _L(rf"V_2 = {_ltx(ans)}\ \mathrm{{m^3}}")]
        opts = [{"value": _sig(ans), "mistake": None, "working": work},
                {"value": _sig(V1 * T2c / T1c), "mistake": "Temperatures must be in kelvin.", "working": work},
                {"value": _sig(V1 * T1 / T2), "mistake": "Heating at constant pressure INCREASES the volume.", "working": work}]
        unit = "m³"
    else:
        p1 = random.choice([4.0, 5.0, 6.0]) * 1e5
        V1 = random.choice([1.5, 2.2, 2.5])
        p2 = p1 * random.choice([1.1, 1.2, 1.25])
        ans = p1 * V1 / T1 * T2 / p2
        text = (f"A gas at {_txt(p1)} Pa, {T1c} °C and {V1:g} m³ is heated to {T2c} °C and its pressure rises to {_txt(p2)} Pa. "
                f"Calculate the new volume.")
        work = [_L(r"\frac{p_1V_1}{T_1} = \frac{p_2V_2}{T_2}"), _L(rf"\frac{{{_ltx(p1)} \times {V1:g}}}{{{T1}}} = \frac{{{_ltx(p2)} \times V_2}}{{{T2}}}"),
                _L(rf"V_2 = {_ltx(ans)}\ \mathrm{{m^3}}")]
        opts = [{"value": _sig(ans), "mistake": None, "working": work},
                {"value": _sig(p1 * V1 / T1c * T2c / p2), "mistake": "Temperatures must be in kelvin.", "working": work},
                {"value": _sig(p1 * V1 / p2), "mistake": "The temperature also changed — use the combined gas law.", "working": work}]
        unit = "m³"
    scaffold = [{"question": "Initial temperature in kelvin?", "answer": float(T1)}, {"question": "Final temperature in kelvin?", "answer": float(T2)},
                {"question": "Answer?", "answer": _sig(ans)}]
    return _q(text, _sig(ans), unit, opts, "Gas Laws", scaffold, level)


# (object, mass lo, hi, number of contacts, contact name, area each lo, hi (m²))
_PRESSURE = [("A ballet dancer", 45, 60, 2, "shoe platform", 1.4e-3, 1.8e-3), ("A cyclist and bicycle", 65, 90, 2, "tyre", 3.5e-4, 5.0e-4),
             ("A water rocket", 0.8, 1.2, 3, "fin", 1.5e-4, 2.5e-4), ("A camping table", 12, 20, 4, "leg", 2.0e-4, 5.0e-4)]


def gen_pm_pressure_weight(level="N5"):
    obj, mlo, mhi, n, part, alo, ahi = random.choice(_PRESSURE)
    m = round(random.uniform(mlo, mhi), 1 if mhi < 5 else 0)
    a = _sig(random.uniform(alo, ahi), 2)
    W = m * 9.8
    A = n * a
    p = W / A
    text = f"{obj} has a total mass of {m:g} kg and rests on {n} {part}s, each of area {_txt(a, 2)} m². Calculate the pressure exerted on the ground."
    work = [_L(rf"W = mg = {m:g} \times 9.8 = {_ltx(W)}\ \mathrm{{N}}"), _L(rf"A = {n} \times {_ltx(a, 2)} = {_ltx(A)}\ \mathrm{{m^2}}"),
            _L(r"p = \frac{F}{A}"), _L(rf"p = {_ltx(p)}\ \mathrm{{Pa}}")]
    opts = [{"value": _sig(p), "mistake": None, "working": work},
            {"value": _sig(W / a), "mistake": f"There are {n} {part}s — use the TOTAL area (course report 2025).", "working": work},
            {"value": _sig(m / A), "mistake": "Pressure needs the FORCE (weight = mg), not the mass.", "working": work},
            {"value": _sig(W * A), "mistake": "p = F ÷ A.", "working": work}]
    scaffold = [{"question": "Weight, in N?", "answer": _sig(W)}, {"question": "Total area, in m²?", "answer": _sig(A)},
                {"question": "Pressure, in Pa?", "answer": _sig(p)}]
    return _q(text, _sig(p), "Pa", opts, "Pressure", scaffold, level)


def gen_pm_kinetic_model(level="N5"):
    kind = random.choice(["heat", "compress", "cool", "definition", "change"])
    if kind == "heat":
        return _choice("A sealed can of gas is heated. Which is the best kinetic-model explanation of why its pressure increases?",
                       "The particles move faster, so they hit the walls more often and with more force.",
                       [("The particles get bigger, so they push harder on the walls.", "Particles don't expand — they move faster."),
                        ("The particles hit the walls more.", "Too vague — say MORE OFTEN and with MORE FORCE."),
                        ("The particles move slower and stick to the walls.", "Heating gives the particles more kinetic energy.")], "Gas Laws", level)
    if kind == "compress":
        return _choice("A syringe of gas is pushed in slowly at constant temperature. Why does the pressure increase?",
                       "The particles have less space, so they hit the walls more often (at the same speed).",
                       [("The particles move faster.", "At constant temperature the particles' speed doesn't change."),
                        ("The particles hit the walls with less force.", "The force per collision is unchanged; collisions are more frequent."),
                        ("The particles get smaller.", "The particles don't change size.")], "Gas Laws", level)
    if kind == "cool":
        return _choice("A sealed buoy drifts into colder water. Why does the pressure of the air inside fall?",
                       "Pressure is directly proportional to the kelvin temperature — the particles move slower and hit the walls less often and less hard.",
                       [("Pressure is directly proportional to the temperature in degrees Celsius.", "Only in KELVIN."),
                        ("Pressure is inversely proportional to the temperature in kelvin.", "Cooling LOWERS the pressure — direct proportion."),
                        ("The volume of the air decreases.", "The buoy's volume is constant.")], "Gas Laws", level)
    if kind == "definition":
        return _choice("What is meant by pressure?", "The force per unit area.",
                       [("Force over an area.", "Imprecise — PER UNIT area (course report 2023)."), ("Force multiplied by area.", "p = F ÷ A."),
                        ("The force acting on a surface.", "Must include ‘per unit area’.")], "Gas Laws", level)
    a, b = sorted(random.sample([-20, -15, 17, 22, 50, 64, 70], 2))
    return _choice(f"A substance is heated from {a} °C to {b} °C. What is the temperature rise in kelvin?", f"{b - a} K",
                   [(f"{b - a + 273} K", "A temperature CHANGE is the same in K and °C — don't add 273."),
                    (f"{b + 273} K", "That's the final temperature, not the rise."),
                    (f"{abs(b + a)} K" if abs(b + a) != b - a else f"{b - a + 546} K", "Subtract the starting temperature from the final one.")], "Gas Laws", level)
