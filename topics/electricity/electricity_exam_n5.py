"""N5 Electricity — exam-style question types from the past-paper/course-report worksheets.

Mirrors the five N5phys Electricity worksheets (Charge Carriers; Potential Difference and Ohm's Law;
Series and Parallel Circuits; Potential Dividers and Transistor Circuits; Electrical Power). The older
generators in this package (current, ohms_law, resistors, potential_divider, power, circuits) already
drill the basic one-step calculations; these add the question styles SQA actually sets, with
distractors that are the errors named in the N5 course reports 2023–2025 and marking instructions:
time/prefix not converted, the voltage used as the current, multiplying by e instead of dividing,
a.c./d.c. explained without electrons, single-point resistance from a line that misses the origin,
1/R_T not inverted, one branch instead of the whole parallel set, the LED voltage used for its
resistor, transistor circuits explained with currents, and the current not squared in P = I²R.
"""
import math
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

TOPIC = "Electricity"
E_CHARGE = 1.6e-19
_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

_NOTES = r"""
## N5 Electricity — exam technique

**Relationships (as on the relationships sheet):**
$$Q = It \quad E_W = QV \quad V = IR \quad R_T = R_1 + R_2 + \dots \quad \frac{1}{R_T} = \frac{1}{R_1} + \frac{1}{R_2} + \dots$$
$$V_2 = \left(\frac{R_2}{R_1 + R_2}\right)V_s \quad \frac{V_1}{V_2} = \frac{R_1}{R_2} \quad P = \frac{E}{t} \quad P = IV \quad P = I^2R \quad P = \frac{V^2}{R}$$

**Common errors (SQA course reports 2023–2025 and marking instructions):**
- Time must be in **seconds** and prefixes converted (mA, μA, ms, kΩ, kW).
- Number of electrons = charge **÷** 1.6 × 10⁻¹⁹ C.
- a.c. / d.c. must be explained **in terms of electrons**: a.c. — electrons change direction repeatedly; d.c. — electrons flow one way.
- Voltage is the **energy per coulomb** (1 V = 1 J C⁻¹).
- If a V–I line does not go through the origin, find R from the **gradient**, not from one point.
- Parallel: 1/R_T must be **inverted**; adding a branch lowers the **total** resistance so the supply current rises.
- An LED's series resistor has (supply − LED) volts across it.
- Transistor switching circuits are explained with **resistance → voltage → switching voltage → transistor on**, never currents.
- Fuse just above the working current: up to about 720 W → 3 A, above → 13 A.
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
        o.setdefault("display", f"{_txt(o['value'])} {unit}")
        if all(abs(o["value"] - k["value"]) > 0.02 * max(abs(o["value"]), abs(k["value"])) for k in kept):
            kept.append(o)
    return make_question(text, answer, kept, unit, scaffold=scaffold, notes=_NOTES,
                         topic=TOPIC, question_type=qtype, level=level)


def _choice(text, correct, wrong, qtype, level="N5"):
    """wrong: list of (option text, why it's wrong)."""
    distractors = [{"value": w, "mistake": why, "working": []} for w, why in wrong]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(question_text=text, correct_answer=correct, unit="", distractors=distractors,
                           working=[], notes=_NOTES, topic=TOPIC, question_type=qtype, level=level,
                           metadata={"type": "classification", "options": options})


# ════════════════ Charge carriers ════════════════
# (device, supply voltage, current lo, hi (A), time value lo, hi, time unit, seconds per unit)
_Q_CONTEXTS = [
    ("A phone charger", 5, 1.0, 3.0, 1, 3, "hours", 3600),
    ("A lamp", 12, 0.2, 0.8, 2, 10, "minutes", 60),
    ("A hairdryer", 230, 2.0, 8.0, 3, 10, "minutes", 60),
    ("An electric bike battery", 36, 1.0, 5.0, 1, 4, "hours", 3600),
    ("A kettle", 230, 8.0, 12.0, 2, 5, "minutes", 60),
]


def gen_ec_charge(level="N5"):
    dev, V, ilo, ihi, tlo, thi, unit, per = random.choice(_Q_CONTEXTS)
    I = round(random.uniform(ilo, ihi), 1)
    tv = random.randint(tlo, thi)
    t = tv * per
    Q = I * t
    text = (f"{dev} is connected to a {V} V supply. The current in it is {I:g} A. Calculate the charge that "
            f"passes through it in {tv} {unit}.")
    work = [_L(r"Q = It"), _T(f"t = {tv} {unit} = {t} s"), _L(rf"Q = {I:g} \times {t}"), _L(rf"Q = {_ltx(Q)}\ \mathrm{{C}}")]
    opts = [{"value": _sig(Q), "mistake": None, "working": work},
            {"value": _sig(I * tv), "mistake": f"The time must be in seconds — {tv} {unit} = {t} s (course report 2024).", "working": work},
            {"value": _sig(V * t), "mistake": f"You used the {V} V supply voltage as the current — it isn't needed here.", "working": work},
            {"value": _sig(t / I), "mistake": "Q = It — multiply the current by the time.", "working": work}]
    scaffold = [{"question": f"What is the time in seconds?", "answer": float(t)},
                {"question": "What is the charge, in C?", "answer": _sig(Q)}]
    return _q(text, _sig(Q), "C", opts, "Charge Carriers", scaffold, level)


# (event, charge lo, hi, time, time text)
_SPARKS = [("During a lightning strike", 10, 30, 1.5e-3, "1.5 ms"),
           ("During a discharge from a Van de Graaff generator", 1.0e-6, 5.0e-6, 0.80e-3, "0.80 ms"),
           ("In a spark between two electrodes", 2.0e-7, 9.0e-7, 2.0e-6, "2.0 μs")]


def gen_ec_electrons(level="N5"):
    event, qlo, qhi, t, ttxt = random.choice(_SPARKS)
    Q = _sig(random.uniform(qlo, qhi), 2)
    if random.random() < 0.5:
        n = Q / E_CHARGE
        text = f"{event}, {_txt(Q, 2)} C of charge is transferred. Calculate the number of electrons transferred."
        work = [_T("number of electrons = charge ÷ charge on one electron"), _L(rf"n = \frac{{{_ltx(Q, 2)}}}{{1.6 \times 10^{{-19}}}}"),
                _L(rf"n = {_ltx(n)}")]
        opts = [{"value": _sig(n), "mistake": None, "working": work},
                {"value": _sig(Q * E_CHARGE), "mistake": "Divide by 1.6 × 10⁻¹⁹ C — the answer should be a huge number of electrons.", "working": work},
                {"value": _sig(E_CHARGE / Q), "mistake": "The fraction is upside down: n = Q ÷ e.", "working": work}]
        return _q(text, _sig(n), "electrons", opts, "Charge Carriers", None, level)
    I = Q / t
    text = f"{event}, {_txt(Q, 2)} C of charge is transferred in {ttxt}. Calculate the average current."
    unit_s = {"ms": 1e-3, "μs": 1e-6}[ttxt.split()[1]]
    work = [_L(r"Q = It"), _L(rf"{_ltx(Q, 2)} = I \times {_ltx(t, 2)}"), _L(rf"I = {_ltx(I)}\ \mathrm{{A}}")]
    opts = [{"value": _sig(I), "mistake": None, "working": work},
            {"value": _sig(Q / (t / unit_s)), "mistake": f"The prefix on {ttxt} has not been converted to seconds (course report 2025).", "working": work},
            {"value": _sig(Q * t), "mistake": "Q = It rearranges to I = Q ÷ t.", "working": work}]
    scaffold = [{"question": "What is the time in seconds?", "answer": t}, {"question": "What is the current, in A?", "answer": _sig(I)}]
    return _q(text, _sig(I), "A", opts, "Charge Carriers", scaffold, level)


def gen_ec_ac_dc(level="N5"):
    kind = random.choice(["ac", "dc", "field", "straight"])
    if kind == "ac":
        return _choice("Which statement explains alternating current (a.c.) in terms of electron flow?",
                       "The electrons change direction repeatedly (flow back and forth).",
                       [("The current changes direction.", "Correct physics, but it doesn't mention electrons — the question asks for electron flow (course report 2024)."),
                        ("The electrons flow in one direction only.", "That describes d.c."),
                        ("The electrons move faster and slower.", "It is the direction of flow that alternates.")], "Charge Carriers", level)
    if kind == "dc":
        return _choice("Which statement explains direct current (d.c.) in terms of electron flow?",
                       "The electrons flow in one direction only.",
                       [("It is a current that goes one way.", "No mention of electrons — not accepted when ‘electron flow’ is asked for (course report 2024)."),
                        ("The electrons change direction repeatedly.", "That describes a.c."),
                        ("Positive charges flow from + to −.", "In a wire it is electrons that flow.")], "Charge Carriers", level)
    if kind == "field":
        plate = random.choice(["top", "bottom"])
        other = "bottom" if plate == "top" else "top"
        return _choice(f"A positively charged particle passes between two charged plates and curves towards the {plate} plate. What are the charges on the plates?",
                       f"{plate} plate negative, {other} plate positive",
                       [(f"{plate} plate positive, {other} plate negative", "Like charges repel — a positive particle moves away from a positive plate."),
                        ("both plates positive", "Then there would be no field between them to deflect the particle this way."),
                        ("the plates have no charge", "An uncharged field region would not deflect it.")], "Charge Carriers", level)
    return _choice("A particle passes straight through the electric field between two charged plates without being deflected. What is the charge on the particle?",
                   "It has no charge.",
                   [("It is positive.", "A charged particle would experience a force and be deflected."),
                    ("It is negative.", "A charged particle would experience a force and be deflected."),
                    ("It depends on its speed.", "Any charged particle feels a force in an electric field.")], "Charge Carriers", level)


# ════════════════ Potential difference and Ohm's law ════════════════
_EW_CONTEXTS = [("torch battery", 3.0, 0.2, 0.5, 2, 10), ("car headlamp", 12, 3.0, 5.0, 1, 5),
                ("laptop battery", 19, 1.5, 3.5, 5, 20), ("bike light battery", 6.0, 0.3, 0.8, 5, 30)]


def gen_ec_ew_qv(level="N5"):
    dev, V, ilo, ihi, mlo, mhi = random.choice(_EW_CONTEXTS)
    I = round(random.uniform(ilo, ihi), 1)
    mins = random.randint(mlo, mhi)
    t = mins * 60
    Q = I * t
    E = Q * V
    text = f"A {V:g} V {dev} supplies a current of {I:g} A for {mins} minutes. Calculate the energy supplied."
    work = [_L(r"Q = It"), _L(rf"Q = {I:g} \times {t} = {_ltx(Q)}\ \mathrm{{C}}"), _L(r"E_W = QV"),
            _L(rf"E_W = {_ltx(Q)} \times {V:g}"), _L(rf"E_W = {_ltx(E)}\ \mathrm{{J}}")]
    opts = [{"value": _sig(E), "mistake": None, "working": work},
            {"value": _sig(I * V), "mistake": "E_W = QV needs the CHARGE — find Q = It first (you used the current).", "working": work},
            {"value": _sig(I * mins * V), "mistake": "The time must be in seconds.", "working": work},
            {"value": _sig(Q / V), "mistake": "E_W = QV — multiply, don't divide.", "working": work}]
    scaffold = [{"question": "What is the charge Q, in C?", "answer": _sig(Q)}, {"question": "What is the energy, in J?", "answer": _sig(E)}]
    return _q(text, _sig(E), "J", opts, "Potential Difference", scaffold, level)


def gen_ec_gradient(level="N5"):
    R = random.choice([12, 15, 22, 33, 47, 50, 68])
    offset = random.choice([0.2, 0.3, 0.4, 0.5])
    i1, i2 = random.choice([(0.02, 0.06), (0.01, 0.05), (0.03, 0.07)])
    v1, v2 = offset + R * i1, offset + R * i2
    text = (f"A graph of voltage (V) against current (A) for a resistor is a straight line that does NOT pass through the origin. "
            f"Two points on the line are ({i1} A, {v1:.2f} V) and ({i2} A, {v2:.2f} V). Determine the resistance of the resistor.")
    work = [_T("R = gradient of the V–I line"), _L(rf"R = \frac{{{v2:.2f} - {v1:.2f}}}{{{i2} - {i1}}}"), _L(rf"R = {R}\ \Omega")]
    opts = [{"value": float(R), "mistake": None, "working": work},
            {"value": _sig(v2 / i2), "mistake": "One point divided — the line misses the origin, so use the gradient (course report 2025).", "working": work},
            {"value": _sig(v1 / i1), "mistake": "One point divided — the line misses the origin, so use the gradient (course report 2025).", "working": work},
            {"value": _sig((i2 - i1) / (v2 - v1)), "mistake": "Gradient = rise ÷ run = ΔV ÷ ΔI here.", "working": work}]
    scaffold = [{"question": "What is the change in voltage ΔV, in V?", "answer": _sig(v2 - v1)},
                {"question": "What is the change in current ΔI, in A?", "answer": _sig(i2 - i1)},
                {"question": "What is the resistance, in Ω?", "answer": float(R)}]
    return _q(text, float(R), "Ω", opts, "Potential Difference", scaffold, level)


def gen_ec_voltage_meaning(level="N5"):
    V = random.choice([1.5, 3.0, 6.0, 9.0, 12])
    return _choice(f"What does a potential difference of {V:g} V across a battery mean?",
                   f"Each coulomb of charge is given {V:g} J of energy.",
                   [(f"The battery gives {V:g} J of energy in total.", "It is energy PER COULOMB of charge."),
                    (f"{V:g} coulombs of charge pass each second.", "Charge per second is the current."),
                    (f"The battery gives {V:g} W of power.", "Power is energy per second, not per coulomb.")], "Potential Difference", level)


# ════════════════ Series and parallel circuits ════════════════
_E12 = [10, 12, 15, 20, 24, 30, 36, 40, 60, 90, 120]


def gen_ec_series_parallel(level="N5"):
    # pairs whose parallel combination is a tidy value
    pairs = [(a, b) for a in _E12 for b in _E12 if a < b and (a * b) % (a + b) == 0]
    r1, r2 = random.choice(pairs)
    rs = random.choice([5, 10, 15, 20, 25])
    Vs = random.choice([6.0, 9.0, 12.0, 24.0])
    rp = r1 * r2 / (r1 + r2)
    rt = rp + rs
    I = Vs / rt
    text = (f"A {rs} Ω resistor is connected in series with a parallel combination of {r1} Ω and {r2} Ω, across a {Vs:g} V supply. "
            f"Calculate the current from the supply.")
    work = [_L(rf"\frac{{1}}{{R_P}} = \frac{{1}}{{{r1}}} + \frac{{1}}{{{r2}}} \Rightarrow R_P = {rp:g}\ \Omega"),
            _L(rf"R_T = {rp:g} + {rs} = {rt:g}\ \Omega"), _L(r"V = IR"), _L(rf"{Vs:g} = I \times {rt:g}"), _L(rf"I = {_ltx(I)}\ \mathrm{{A}}")]
    opts = [{"value": _sig(I), "mistake": None, "working": work},
            {"value": _sig(Vs / (1 / rp + rs)), "mistake": "1/R_P was not inverted before adding the series resistor.", "working": work},
            {"value": _sig(Vs / (r1 + r2 + rs)), "mistake": "The parallel resistors were added as if they were in series.", "working": work},
            {"value": _sig(Vs / rp), "mistake": "The series resistor has been left out of the total resistance.", "working": work}]
    scaffold = [{"question": "What is the resistance of the parallel pair, in Ω?", "answer": float(rp)},
                {"question": "What is the total resistance, in Ω?", "answer": float(rt)},
                {"question": "What is the supply current, in A?", "answer": _sig(I)}]
    return _q(text, _sig(I), "A", opts, "Circuit Rules", scaffold, level)


# (device, number lo, hi, power each (W), supply V)
_PARALLEL_SETS = [("LED spotlights", 3, 6, 4.8, 12), ("halogen lamps", 2, 5, 20, 12), ("garden lights", 4, 8, 3.0, 12),
                  ("heaters", 2, 3, 1000, 230)]


def gen_ec_parallel_total_current(level="N5"):
    dev, nlo, nhi, P, V = random.choice(_PARALLEL_SETS)
    n = random.randint(nlo, nhi)
    I1 = P / V
    It = n * I1
    text = f"{n} identical {dev}, each rated {P:g} W, are connected in parallel to a {V} V supply. Calculate the current drawn from the supply."
    work = [_L(r"P = IV"), _L(rf"P_{{total}} = {n} \times {P:g} = {n * P:g}\ \mathrm{{W}}"), _L(rf"{n * P:g} = I \times {V}"),
            _L(rf"I = {_ltx(It)}\ \mathrm{{A}}")]
    opts = [{"value": _sig(It), "mistake": None, "working": work},
            {"value": _sig(I1), "mistake": f"That is the current in ONE of them — there are {n} in parallel, and branch currents add (course report 2025).", "working": work},
            {"value": _sig(I1 / n), "mistake": "In parallel the branch currents add; they are not shared out.", "working": work},
            {"value": _sig(V / P * n), "mistake": "P = IV rearranges to I = P ÷ V.", "working": work}]
    scaffold = [{"question": "What is the current in one of them, in A?", "answer": _sig(I1)},
                {"question": "What is the total current, in A?", "answer": _sig(It)}]
    return _q(text, _sig(It), "A", opts, "Circuit Rules", scaffold, level)


def gen_ec_circuit_changes(level="N5"):
    kind = random.choice(["add_branch", "ldr_branch", "advantage"])
    if kind == "add_branch":
        return _choice("A switch is closed that connects another resistor in parallel with the existing one. What happens to the supply current, and why?",
                       "It increases, because the total resistance of the circuit decreases.",
                       [("It increases, because the resistance goes down.", "Must make clear it is the TOTAL resistance of the circuit (course report 2023)."),
                        ("It decreases, because there is more resistance in the circuit.", "Adding a parallel branch lowers the total resistance."),
                        ("It stays the same, because the supply voltage is unchanged.", "The total resistance changes, so the current does.")], "Circuit Rules", level)
    if kind == "ldr_branch":
        return _choice("An LDR is in one branch of a parallel circuit and a fixed resistor is in the other. The light level falls. What happens to the current in the fixed resistor?",
                       "It stays the same, because the voltage across it is unchanged.",
                       [("It increases, because the LDR branch takes less current.", "Parallel branches each have the supply voltage; the resistor's current doesn't change (course report 2024)."),
                        ("It decreases, because the LDR's resistance increases.", "Only the LDR branch current decreases."),
                        ("It becomes zero.", "The resistor still has the supply voltage across it.")], "Circuit Rules", level)
    return _choice("Which is an advantage of connecting spotlights in parallel rather than in series?",
                   "Each spotlight operates at the correct (supply) voltage, and if one fails the others stay on.",
                   [("They all have the same voltage.", "Must say they operate at the CORRECT voltage (course report 2025)."),
                    ("The current is the same in each spotlight.", "That is a property of series circuits."),
                    ("The total resistance is higher, so less current is drawn.", "The total resistance in parallel is lower.")], "Circuit Rules", level)


# ════════════════ Potential dividers, LEDs and transistors ════════════════
# (colour, LED voltage)
_LEDS = [("red", 1.8), ("yellow", 2.0), ("green", 2.2), ("blue", 3.0)]


def gen_ec_led_resistor(level="N5"):
    colour, vled = random.choice(_LEDS)
    n = random.choice([1, 1, 2, 3])
    vs = random.choice([5.0, 6.0, 9.0, 12.0])
    if vs <= n * vled + 0.5:
        vs = 12.0
    i_ma = random.choice([10, 15, 20, 25])
    vr = vs - n * vled
    R = vr / (i_ma / 1000)
    leds = "An LED" if n == 1 else f"{n} identical LEDs connected in series"
    text = (f"{leds} ({colour}, each operating at {vled} V and {i_ma} mA) {'is' if n == 1 else 'are'} connected in series with a resistor to a "
            f"{vs:g} V supply. Calculate the resistance of the resistor.")
    work = [_L(rf"V_R = {vs:g} - {n} \times {vled} = {vr:.1f}\ \mathrm{{V}}"), _L(r"V = IR"),
            _L(rf"{vr:.1f} = {i_ma / 1000:g} \times R"), _L(rf"R = {_ltx(R)}\ \Omega")]
    opts = [{"value": _sig(R), "mistake": None, "working": work},
            {"value": _sig(vled / (i_ma / 1000)), "mistake": "That's the LED's resistance — the resistor has (supply − LED) volts across it (course reports 2023 and 2024).", "working": work},
            {"value": _sig(vs / (i_ma / 1000)), "mistake": "Subtract the LED voltage from the supply first.", "working": work},
            {"value": _sig(vr / i_ma), "mistake": "The current must be in amps: mA ÷ 1000.", "working": work}]
    scaffold = [{"question": "What is the voltage across the resistor, in V?", "answer": _sig(vr)},
                {"question": "What is the resistance, in Ω?", "answer": _sig(R)}]
    return _q(text, _sig(R), "Ω", opts, "LEDs and Transistor Switches", scaffold, level)


# (sensor, what lowers its resistance, condition that raises its voltage)
_SENSORS = [("LDR", "light", "it gets dark", "a lamp"), ("thermistor", "temperature", "it gets cold", "a heater")]


def gen_ec_divider_switch(level="N5"):
    sensor, _, _, _ = random.choice(_SENSORS)
    vs = random.choice([5.0, 6.0, 9.0])
    r1 = random.choice([4.7, 6.8, 10, 12, 16.6])
    r2 = random.choice([1.0, 2.2, 3.4, 4.7, 6.8])
    vsw = random.choice([0.7, 2.4])
    v2 = r2 / (r1 + r2) * vs
    on = "ON" if v2 >= vsw else "OFF"
    text = (f"A {r1:g} kΩ variable resistor (top) and a {sensor} (bottom) form a potential divider across {vs:g} V. A transistor connected across the "
            f"{sensor} switches on at {vsw} V. The {sensor} has a resistance of {r2:g} kΩ. Calculate the voltage across the {sensor} "
            f"(the transistor is {on} at this value).")
    work = [_L(r"V_2 = \left(\frac{R_2}{R_1 + R_2}\right)V_s"), _L(rf"V_2 = \left(\frac{{{r2:g}}}{{{r1:g} + {r2:g}}}\right) \times {vs:g}"),
            _L(rf"V_2 = {_ltx(v2)}\ \mathrm{{V}}"), _T(f"{_txt(v2)} V is {'at least' if on == 'ON' else 'less than'} {vsw} V, so the transistor is {on.lower()}.")]
    opts = [{"value": _sig(v2), "mistake": None, "working": work},
            {"value": _sig(r1 / (r1 + r2) * vs), "mistake": "That's the voltage across the variable resistor — put the sensor's resistance on top.", "working": work},
            {"value": _sig(r2 / r1 * vs), "mistake": "The bottom of the fraction is the TOTAL resistance R₁ + R₂.", "working": work},
            {"value": _sig(r2 / (r1 + r2)), "mistake": "You found the fraction of the supply but didn't multiply by the supply voltage.", "working": work},
            {"value": _sig(vs * r2 / (r1 + r2) + vsw), "mistake": "The switching voltage isn't part of the calculation — it's only compared with your answer.", "working": work}]
    scaffold = [{"question": "What is the total resistance, in kΩ?", "answer": _sig(r1 + r2)},
                {"question": f"What is the voltage across the {sensor}, in V?", "answer": _sig(v2)}]
    return _q(text, _sig(v2), "V", opts, "LEDs and Transistor Switches", scaffold, level)


def gen_ec_transistor_explain(level="N5"):
    sensor, factor, condition, device = random.choice(_SENSORS)
    return _choice(f"A resistor (top) and a {sensor} (bottom) form a potential divider. A MOSFET's gate is connected across the {sensor}, and the MOSFET "
                   f"switches on {device}. Which explanation of how {device} switches on when {condition} is best?",
                   f"The {sensor}'s resistance increases, so the voltage across it increases; when it reaches the switching voltage the MOSFET switches on.",
                   [(f"The {sensor} lets less current through, so more current goes to the MOSFET and it switches on.",
                     "Transistor circuits must be explained in terms of resistance and VOLTAGE, not current (course reports 2024 and 2025)."),
                    (f"The {sensor}'s resistance decreases, so the voltage across it increases and the MOSFET switches on.",
                     f"When {condition}, the {sensor}'s resistance INCREASES."),
                    (f"The {sensor}'s resistance increases, so {device} switches on.",
                     "The link through the VOLTAGE across the sensor reaching the switching voltage is missing.")], "LEDs and Transistor Switches", level)


# ════════════════ Power and fuses ════════════════
# (appliance, power lo, hi (W))
_APPLIANCES = [("television", 80, 250), ("laptop charger", 45, 120), ("lamp", 40, 100), ("kettle", 2000, 3000),
               ("toaster", 900, 1400), ("hairdryer", 1000, 2000), ("games console", 150, 300), ("electric heater", 1500, 2500)]


def gen_ec_fuse(level="N5"):
    dev, plo, phi = random.choice(_APPLIANCES)
    P = random.randrange(plo, phi + 1, 10 if phi < 500 else 100)
    I = P / 230
    fuse = "3 A" if I < 3 else "13 A"
    wrong = "13 A" if fuse == "3 A" else "3 A"
    why = ("A 13 A fuse would not blow until the current was far above the working current, so it wouldn't protect the flex."
           if fuse == "3 A" else f"The working current is {_txt(I, 2)} A — a 3 A fuse would blow as soon as it was switched on.")
    return _choice(f"A {P} W {dev} is connected to the 230 V mains. Which fuse should be fitted in its plug?",
                   f"{fuse} (the current is {_txt(I, 2)} A)",
                   [(f"{wrong} (the current is {_txt(I, 2)} A)", why),
                    (f"{fuse} (the current is {_txt(P * 230, 2)} A)", "P = IV rearranges to I = P ÷ V."),
                    ("5 A (it is always the safest choice)", "Plugs are fitted with the fuse just above the working current: 3 A or 13 A.")],
                   "Power and Fuses", level)


# (element, current lo, hi (A), resistance lo, hi (Ω))
_PIR = [("heating element", 2.0, 6.0, 10, 50), ("wire", 1.0, 3.0, 2, 10), ("lamp filament", 0.2, 0.8, 5, 30), ("resistor", 0.05, 0.5, 20, 200)]


def gen_ec_power_i2r(level="N5"):
    el, ilo, ihi, rlo, rhi = random.choice(_PIR)
    if random.random() < 0.5:
        I = round(random.uniform(ilo, ihi), 2 if ihi < 1 else 1)
        R = random.randint(rlo, rhi)
        P = I * I * R
        text = f"A current of {I:g} A flows in a {R} Ω {el}. Calculate the power developed."
        work = [_L(r"P = I^2R"), _L(rf"P = {I:g}^2 \times {R}"), _L(rf"P = {_ltx(P)}\ \mathrm{{W}}")]
        opts = [{"value": _sig(P), "mistake": None, "working": work},
                {"value": _sig(I * R), "mistake": "The current has not been squared (course report 2024).", "working": work},
                {"value": _sig(I * I / R), "mistake": "P = I²R — multiply by R.", "working": work},
                {"value": _sig(I * R * R), "mistake": "It is the CURRENT that is squared, not the resistance.", "working": work}]
        scaffold = [{"question": "What is I², in A²?", "answer": _sig(I * I)}, {"question": "What is the power, in W?", "answer": _sig(P)}]
        return _q(text, _sig(P), "W", opts, "Power and Fuses", scaffold, level)
    V = random.choice([6.0, 12.0, 24.0, 230.0])
    R = random.randint(rlo, rhi) * (20 if V == 230 else 1)
    P = V * V / R
    text = f"A {V:g} V supply is connected across a {R} Ω {el}. Calculate the power developed."
    work = [_L(r"P = \frac{V^2}{R}"), _L(rf"P = \frac{{{V:g}^2}}{{{R}}}"), _L(rf"P = {_ltx(P)}\ \mathrm{{W}}")]
    opts = [{"value": _sig(P), "mistake": None, "working": work},
            {"value": _sig(V / R), "mistake": "That's the current (V ÷ R) — the voltage must be squared for the power.", "working": work},
            {"value": _sig(V * V * R), "mistake": "P = V² ÷ R — divide by R.", "working": work}]
    return _q(text, _sig(P), "W", opts, "Power and Fuses", None, level)


def gen_ec_energy_time(level="N5"):
    dev, plo, phi = random.choice(_APPLIANCES)
    P = random.randrange(plo, phi + 1, 10 if phi < 500 else 100)
    if random.random() < 0.5 or P < 500:
        mins = random.choice([2, 3, 5, 10, 15, 30])
        t = mins * 60
        E = P * t
        text = f"A {P} W {dev} is switched on for {mins} minutes. Calculate the energy used."
        work = [_L(r"P = \frac{E}{t}"), _L(rf"{P} = \frac{{E}}{{{t}}}"), _L(rf"E = {_ltx(E)}\ \mathrm{{J}}")]
        opts = [{"value": _sig(E), "mistake": None, "working": work},
                {"value": _sig(P * mins), "mistake": "The time must be in seconds.", "working": work},
                {"value": _sig(P / t), "mistake": "P = E ÷ t rearranges to E = P × t.", "working": work}]
        scaffold = [{"question": "What is the time in seconds?", "answer": float(t)}, {"question": "What is the energy, in J?", "answer": _sig(E)}]
        return _q(text, _sig(E), "J", opts, "Power and Fuses", scaffold, level)
    kw = P / 1000
    t = random.choice([60, 90, 120, 150, 180])
    E = P * t
    text = f"A {kw:g} kW {dev} transfers {_txt(E)} J of energy. Calculate how long it is switched on."
    work = [_L(r"P = \frac{E}{t}"), _L(rf"{P} = \frac{{{_ltx(E)}}}{{t}}"), _L(rf"t = {t}\ \mathrm{{s}}")]
    opts = [{"value": float(t), "mistake": None, "working": work},
            {"value": _sig(E / kw), "mistake": "The power must be in watts: 1 kW = 1000 W.", "working": work},
            {"value": _sig(E * P), "mistake": "t = E ÷ P.", "working": work}]
    return _q(text, float(t), "s", opts, "Power and Fuses", None, level)


def gen_ec_toaster_statements(level="N5"):
    P = random.choice([900, 1200, 1500, 2000])
    I = P / 230
    return _choice(f"A {P / 1000:g} kW toaster is connected to the 230 V mains. Which statement is correct?",
                   f"The element transfers {P} J of energy each second.",
                   [(f"The element transfers {P * 10} J of energy each second.", f"{P / 1000:g} kW = {P} W = {P} J each second (course report 2024)."),
                    ("230 C of charge passes through the element each second.", f"Charge per second is the current: {_txt(I, 2)} A, i.e. {_txt(I, 2)} C each second (course report 2024)."),
                    ("The plug should be fitted with a 3 A fuse.", f"The current is {_txt(I, 2)} A, so it needs a 13 A fuse.")], "Power and Fuses", level)
