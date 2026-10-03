"""Higher Electricity — question types from the five Hphys Electricity worksheets.

Monitoring and Measuring AC, Current/Potential Difference/Power/Resistance, Electrical Sources and
Internal Resistance, Capacitors, and Semiconductors and p-n Junctions. Equations are written as on
the Higher relationships sheet. Distractors are the errors named in the SQA course reports
2015–2025 and marking instructions: dividing by √2 for the peak (or multiplying for r.m.s.); the
peak-to-peak height read as the peak; T left in ms; the current from P = IV taken as the peak;
reciprocals not inverted; the square root forgotten in P = I²R; the wrong resistor on top of the
divider fraction; parallel resistors given a share of the p.d.; r found as E ÷ I; the gradient of a
V–I graph taken as +r; µF not converted; the ½ dropped from E = ½CV²; the voltmeter across the
resistor read as the capacitor p.d.; and LED explanations without band theory.
"""
import math
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

TOPIC = "Electricity"
AC = "Monitoring and Measuring AC"
CIRC = "Current, Potential Difference, Power and Resistance"
IR = "Electrical Sources and Internal Resistance"
CAP = "Capacitors"
SEMI = "Semiconductors and p-n Junctions"
H = 6.63e-34
C = 3.00e8
E_CHARGE = 1.60e-19
R2 = math.sqrt(2)
_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

_NOTES = r"""
## Higher Electricity

**Relationships (as on the relationships sheet):**
$$V_{peak} = \sqrt2 V_{rms} \quad I_{peak} = \sqrt2 I_{rms} \quad T = \frac1f \quad Q = It \quad V = IR \quad P = IV = I^2R = \frac{V^2}{R}$$
$$R_T = R_1 + R_2 + \dots \quad \frac1{R_T} = \frac1{R_1} + \frac1{R_2} + \dots \quad V_1 = \left(\frac{R_1}{R_1 + R_2}\right)V_S \quad \frac{V_1}{V_2} = \frac{R_1}{R_2}$$
$$E = V + Ir \quad C = \frac QV \quad E = \tfrac12 QV = \tfrac12 CV^2 = \tfrac12\frac{Q^2}{C} \quad E = hf \quad v = f\lambda$$

**Common errors (SQA course reports and marking instructions):**
- AC = a current that changes **direction and instantaneous value** with time. The peak is the **larger** value: $V_{peak} = \sqrt2 V_{rms}$.
- Oscilloscope: peak = crest to **centre line** (not crest to trough) × Y-gain. Period = divisions for **one whole wave** × timebase — in **seconds**.
- $P = IV$ with r.m.s. values gives the **r.m.s.** current; multiply by $\sqrt2$ for the peak.
- Parallel: **invert** $1/R_T$. Parallel branches each have the **full** p.d. — don't use the divider rule on them.
- $P = I^2R$ → take the **square root** for I. Convert kΩ → Ω.
- Potential divider: $R_1$ is the resistor you want the p.d. across. Combine a parallel pair **first**.
- e.m.f. = energy supplied to **each coulomb** of charge. $E \div I$ is the **total** resistance $R + r$, not $r$.
- V–I graph: intercept $= E$, gradient $= -r$; short-circuit current $= E/r$ (where V = 0, not the last data point).
- Capacitors: µF = $10^{-6}$ F. Energy is **½**QV. A voltmeter across the **resistor** reads $V_S - V_C$.
- Larger R → **smaller** initial current, longer to charge; larger C → **same** initial current, longer to charge. Energy stored ½CV² does not depend on R.
- LEDs: explain with **band theory** — electrons move from the n-type conduction band towards the p-type, fall from the conduction band to the valence band and emit a photon. A **larger band gap** → higher-energy photons (blue).
- A solar cell uses the **photovoltaic effect**. A semiconductor's conductivity **increases** with temperature.
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


def _q(text, answer, unit, options, qtype, scaffold=None, level="Higher"):
    kept = []
    for o in options:
        o["value"] = _sig(o["value"])
        o.setdefault("display", f"{_txt(o['value'])} {unit}".strip())
        if all(abs(o["value"] - k["value"]) > 0.02 * max(abs(o["value"]), abs(k["value"])) for k in kept):
            kept.append(o)
    return make_question(text, _sig(answer), kept, unit, scaffold=scaffold, notes=_NOTES,
                         topic=TOPIC, question_type=qtype, level=level)


def _choice(text, correct, wrong, qtype, level="Higher"):
    distractors = [{"value": w, "mistake": why, "working": []} for w, why in wrong]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(question_text=text, correct_answer=correct, unit="", distractors=distractors,
                           working=[], notes=_NOTES, topic=TOPIC, question_type=qtype, level=level,
                           metadata={"type": "classification", "options": options})


def _opts(work, right, *wrong):
    return [{"value": right, "mistake": None, "working": work}] + [{"value": v, "mistake": m, "working": work} for v, m in wrong]


# ════════════════ Monitoring and measuring AC ════════════════
# (context, r.m.s. voltage, power choices (W))
_AC_DEVICES = [("A kettle connected to the 230 V r.m.s. mains", 230, [2300, 2760, 3000]),
               ("A heater connected to the 230 V r.m.s. mains", 230, [1150, 1840, 2070]),
               ("A 12 V r.m.s. lamp in a model lighthouse", 12, [24, 36, 48]),
               ("A 24 V r.m.s. lamp on a CalMac ferry's chart table", 24, [36, 60, 72])]


def gen_he_peak_rms(level="Higher"):
    kind = random.choice(["peak", "rms", "power"])
    if kind == "peak":
        v = random.choice([12, 24, 110, 230, 6.0, 9.0])
        pk = R2 * v
        text = f"An a.c. supply has an r.m.s. voltage of {v:g} V. Calculate its peak voltage."
        work = [_L(r"V_{peak} = \sqrt2 V_{rms}"), _L(rf"V_{{peak}} = \sqrt2 \times {v:g} = {_ltx(pk)}\ \mathrm{{V}}")]
        return _q(text, pk, "V", _opts(work, pk, (v / R2, "The peak is the LARGER value — multiply by √2."),
                                       (2 * v, "Multiply by √2, not 2.")), AC, None, level)
    if kind == "rms":
        i = random.choice([0.85, 1.2, 2.5, 4.0, 13.0])
        rms = i / R2
        text = f"The peak current in a resistor is {i:g} A. Calculate the r.m.s. current."
        work = [_L(r"I_{peak} = \sqrt2 I_{rms}"), _L(rf"{i:g} = \sqrt2 \times I_{{rms}}"), _L(rf"I_{{rms}} = {_ltx(rms)}\ \mathrm{{A}}")]
        return _q(text, rms, "A", _opts(work, rms, (i * R2, "The r.m.s. value is SMALLER than the peak — divide by √2."),
                                        (i / 2, "Divide by √2, not 2.")), AC, None, level)
    name, v, ps = random.choice(_AC_DEVICES)
    P = random.choice(ps)
    irms = P / v
    ipk = R2 * irms
    text = f"{name} has a power of {P:g} W. Calculate the peak current."
    work = [_L(r"P = IV"), _L(rf"{P:g} = I_{{rms}} \times {v:g}"), _L(rf"I_{{rms}} = {_ltx(irms)}\ \mathrm{{A}}"),
            _L(rf"I_{{peak}} = \sqrt2 \times {_ltx(irms)} = {_ltx(ipk)}\ \mathrm{{A}}")]
    scaffold = [{"question": "What is the r.m.s. current, in A?", "answer": _sig(irms)},
                {"question": "What is the peak current, in A?", "answer": _sig(ipk)}]
    return _q(text, ipk, "A", _opts(work, ipk, (irms, "P = IV with the r.m.s. voltage gives the r.m.s. current — now multiply by √2 (2015 Paper 1)."),
                                    (irms / R2, "The peak is LARGER than the r.m.s. — multiply by √2.")), AC, scaffold, level)


def gen_he_scope(level="Higher"):
    kind = random.choice(["vrms", "freq", "timebase"])
    if kind == "vrms":
        div = random.choice([1.5, 2.0, 2.5, 3.0, 3.5])
        gain = random.choice([0.5, 1.0, 2.0, 5.0])
        pk = div * gain
        rms = pk / R2
        text = (f"On an oscilloscope, the crests of a trace are {div:g} divisions above the centre line. "
                f"The Y-gain is {gain:g} V/div. Calculate the r.m.s. voltage.")
        work = [_L(rf"V_{{peak}} = {div:g} \times {gain:g} = {_ltx(pk)}\ \mathrm{{V}}"), _L(r"V_{peak} = \sqrt2 V_{rms}"),
                _L(rf"V_{{rms}} = \frac{{{_ltx(pk)}}}{{\sqrt2}} = {_ltx(rms)}\ \mathrm{{V}}")]
        scaffold = [{"question": "What is the peak voltage, in V?", "answer": _sig(pk)},
                    {"question": "What is the r.m.s. voltage, in V?", "answer": _sig(rms)}]
        return _q(text, rms, "V", _opts(work, rms, (2 * pk / R2, "Crest to trough is the peak-to-peak voltage — measure from the centre line."),
                                        (pk * R2, "Divide by √2 for the r.m.s. value."), (pk, "That's the peak — now find the r.m.s.")), AC, scaffold, level)
    if kind == "freq":
        n = random.choice([2, 2.5, 4, 5, 8])
        tb, unit = random.choice([(0.5, "ms"), (1, "ms"), (2, "ms"), (5, "ms"), (10, "ms"), (30, "ms"), (0.1, "ms")])
        T = n * tb * 1e-3
        f = 1 / T
        text = (f"One complete wave of a trace occupies {n:g} divisions. The timebase is set at {tb:g} {unit}/div. "
                f"Calculate the frequency of the signal.")
        work = [_L(rf"T = {n:g} \times {tb:g}\times10^{{-3}} = {_ltx(T)}\ \mathrm{{s}}"), _L(r"T = \frac1f"),
                _L(rf"f = \frac{{1}}{{{_ltx(T)}}} = {_ltx(f)}\ \mathrm{{Hz}}")]
        scaffold = [{"question": "What is the period, in s?", "answer": _sig(T)}, {"question": "What is the frequency, in Hz?", "answer": _sig(f)}]
        return _q(text, f, "Hz", _opts(work, f, (1 / (n * tb), "Convert ms to s before f = 1/T."),
                                       (1 / (2 * T), "One whole wave = one period — don't double it.")), AC, scaffold, level)
    f = random.choice([50, 100, 250, 500, 1000, 2000])
    n = random.choice([2, 4, 5])
    T = 1 / f
    tb = T / n
    text = f"A {f:g} Hz signal is displayed so that one complete wave occupies {n} divisions. Calculate the timebase setting, in s/div."
    work = [_L(r"T = \frac1f"), _L(rf"T = \frac{{1}}{{{f:g}}} = {_ltx(T)}\ \mathrm{{s}}"),
            _L(rf"\text{{timebase}} = \frac{{{_ltx(T)}}}{{{n}}} = {_ltx(tb)}\ \mathrm{{s/div}}")]
    scaffold = [{"question": "What is the period, in s?", "answer": _sig(T)}, {"question": "What is the timebase, in s/div?", "answer": _sig(tb)}]
    return _q(text, tb, "s/div", _opts(work, tb, (T, "That's the period of one wave — divide by the number of divisions."),
                                       (T * n, "Divide the period by the number of divisions (2024 Paper 2).")), AC, scaffold, level)


def gen_he_ac_explain(level="Higher"):
    kind = random.choice(["define", "same", "led"])
    if kind == "define":
        return _choice("What is meant by an alternating current?", "A current that changes direction and instantaneous value with time.",
                       [("A current that changes direction.", "Incomplete — the instantaneous value must change with time too (course report 2024)."),
                        ("A current whose size changes but direction stays the same.", "That is a varying d.c."),
                        ("A current with a peak value √2 times its r.m.s. value.", "That's a property of a sinusoidal a.c., not its definition.")], AC, level)
    if kind == "same":
        return _choice("The frequency of a signal on an oscilloscope is doubled and the timebase setting is halved. How does the trace change?",
                       "It looks exactly the same.", [("Twice as many waves are shown.", "Halving the time per division cancels the doubled frequency."),
                                                      ("Half as many waves are shown.", "The two changes cancel."),
                                                      ("The waves are twice as tall.", "Neither change affects the height.")], AC, level)
    return _choice("A red LED and a blue LED are connected in parallel, facing opposite ways, across a low-frequency a.c. supply. Why do they light alternately?",
                   "Each LED only conducts when forward biased, and each is forward biased in a different half of every cycle.",
                   [("The red LED lights when forward biased and the blue LED when reverse biased.", "An LED never conducts in reverse bias (course report 2023)."),
                    ("The a.c. supply switches off between half-cycles.", "The supply reverses direction; it doesn't switch off."),
                    ("The blue LED needs a higher frequency.", "Both receive the same frequency — it's the bias that matters.")], AC, level)


# ════════════════ Current, potential difference, power and resistance ════════════════

def _par(*rs):
    return 1 / sum(1 / r for r in rs)


def gen_he_resistance_power(level="Higher"):
    kind = random.choice(["network", "parallel_power", "sqrt"])
    if kind == "network":
        rs = random.choice([2.0, 4.0, 5.0, 9.0, 10.0])
        a, b = random.choice([(8.0, 2.0), (6.0, 3.0), (12.0, 6.0), (6.0, 6.0), (30.0, 20.0), (12.0, 4.0)])
        V = random.choice([3.0, 6.0, 9.0, 12.0])
        rp = _par(a, b)
        rt = rs + rp
        I = V / rt
        text = (f"A {rs:g} Ω resistor is in series with a parallel pair of {a:g} Ω and {b:g} Ω resistors, across a {V:g} V supply of "
                f"negligible internal resistance. Calculate the current from the supply.")
        work = [_L(rf"\frac{{1}}{{R_P}} = \frac{{1}}{{{a:g}}} + \frac{{1}}{{{b:g}}},\ R_P = {_ltx(rp)}\ \Omega"),
                _L(rf"R_T = {rs:g} + {_ltx(rp)} = {_ltx(rt)}\ \Omega"), _L(r"V = IR"), _L(rf"I = \frac{{{V:g}}}{{{_ltx(rt)}}} = {_ltx(I)}\ \mathrm{{A}}")]
        scaffold = [{"question": "What is the resistance of the parallel pair, in Ω?", "answer": _sig(rp)},
                    {"question": "What is the total resistance, in Ω?", "answer": _sig(rt)},
                    {"question": "What is the current, in A?", "answer": _sig(I)}]
        return _q(text, I, "A", _opts(work, I, (V / (rs + 1 / a + 1 / b), "Invert 1/R_P before adding — reciprocals not inverted earn 0 (MI)."),
                                      (V / (rs + a + b), "The pair is in PARALLEL — use 1/R_T = 1/R₁ + 1/R₂."),
                                      (V / rs, "Include the parallel pair in the total resistance.")), CIRC, scaffold, level)
    if kind == "parallel_power":
        V = random.choice([6.0, 9.0, 12.0])
        a, b = random.choice([(3.0, 6.0), (4.0, 12.0), (2.0, 8.0)])
        P = V ** 2 / a
        text = f"A {a:g} Ω resistor and a {b:g} Ω resistor are connected in parallel across a {V:g} V supply of negligible internal resistance. Calculate the power dissipated in the {a:g} Ω resistor."
        work = [_L(rf"V = {V:g}\ \mathrm{{V}}\ \text{{(each parallel branch has the full p.d.)}}"), _L(r"P = \frac{V^2}{R}"),
                _L(rf"P = \frac{{{V:g}^2}}{{{a:g}}} = {_ltx(P)}\ \mathrm{{W}}")]
        share = a / (a + b) * V
        return _q(text, P, "W", _opts(work, P, (share ** 2 / a, "Parallel resistors don't share the p.d. — each has the full supply p.d."),
                                      (V ** 2 / (a + b), "Use this resistor's own resistance."), (V / a, "That's the current — P = V²/R.")), CIRC, None, level)
    R, P, label = random.choice([(120, 4.8, "current"), (50, 2.0, "current"), (33, 0.75, "current"),
                                 (100, 4.0, "pd"), (2200, 0.25, "pd"), (4700, 0.5, "pd")])
    if label == "current":
        I = math.sqrt(P / R)
        text = f"A {R:g} Ω resistor dissipates {P:g} W. Calculate the current in it."
        work = [_L(r"P = I^2R"), _L(rf"{P:g} = I^2 \times {R:g}"), _L(rf"I = \sqrt{{{_ltx(P / R)}}} = {_ltx(I)}\ \mathrm{{A}}")]
        scaffold = [{"question": "What is I², in A²?", "answer": _sig(P / R)}, {"question": "What is I, in A?", "answer": _sig(I)}]
        return _q(text, I, "A", _opts(work, I, (P / R, "That's I² — take the square root."), (P * R, "Rearrange P = I²R for I².")), CIRC, scaffold, level)
    V = math.sqrt(P * R)
    rtxt = f"{R / 1000:g} kΩ" if R >= 1000 else f"{R:g} Ω"
    text = f"A {rtxt} resistor has a power rating of {P:g} W. Calculate the maximum p.d. that can be applied across it."
    work = [_L(r"P = \frac{V^2}{R}"), _L(rf"{P:g} = \frac{{V^2}}{{{R:g}}}"), _L(rf"V = \sqrt{{{_ltx(P * R)}}} = {_ltx(V)}\ \mathrm{{V}}")]
    scaffold = [{"question": "What is V², in V²?", "answer": _sig(P * R)}, {"question": "What is V, in V?", "answer": _sig(V)}]
    wrong = [(P * R, "That's V² — take the square root.")]
    if R >= 1000:
        wrong.append((math.sqrt(P * R / 1000), "Convert kΩ to Ω."))
    return _q(text, V, "V", _opts(work, V, *wrong), CIRC, scaffold, level)


def gen_he_divider(level="Higher"):
    kind = random.choice(["simple", "parallel", "bridge"])
    if kind == "simple":
        r1, r2 = random.choice([(4.0, 2.0), (330, 470), (82, 47), (3.0, 1.0), (2.2, 6.8), (10, 15)])
        Vs = random.choice([5.0, 6.0, 9.0, 12.0])
        V1 = r1 / (r1 + r2) * Vs
        text = f"Resistors of {r1:g} kΩ and {r2:g} kΩ are connected in series across a {Vs:g} V supply. Calculate the p.d. across the {r1:g} kΩ resistor."
        work = [_L(r"V_1 = \left(\frac{R_1}{R_1+R_2}\right)V_S"), _L(rf"V_1 = \left(\frac{{{r1:g}}}{{{r1:g}+{r2:g}}}\right)\times{Vs:g} = {_ltx(V1)}\ \mathrm{{V}}")]
        return _q(text, V1, "V", _opts(work, V1, (r2 / (r1 + r2) * Vs, "R₁ (on top) is the resistor you want the p.d. across."),
                                       (r1 / r2 * Vs, "Divide by the TOTAL resistance R₁ + R₂.")), CIRC, None, level)
    if kind == "parallel":
        rs = random.choice([60, 15, 30, 40])
        a, b = random.choice([(30, 20), (20, 30), (60, 30), (12, 6)])
        Vs = random.choice([6.0, 12.0, 9.0])
        rp = _par(a, b)
        V1 = rs / (rs + rp) * Vs
        text = (f"A {rs:g} Ω resistor is in series with a parallel pair of {a:g} Ω and {b:g} Ω resistors across a {Vs:g} V supply. "
                f"Calculate the p.d. across the {rs:g} Ω resistor.")
        work = [_L(rf"R_P = {_ltx(rp)}\ \Omega"), _L(r"V_1 = \left(\frac{R_1}{R_1+R_2}\right)V_S"),
                _L(rf"V_1 = \left(\frac{{{rs:g}}}{{{rs:g}+{_ltx(rp)}}}\right)\times{Vs:g} = {_ltx(V1)}\ \mathrm{{V}}")]
        scaffold = [{"question": "What is the resistance of the parallel pair, in Ω?", "answer": _sig(rp)},
                    {"question": f"What is the p.d. across the {rs:g} Ω resistor, in V?", "answer": _sig(V1)}]
        return _q(text, V1, "V", _opts(work, V1, (rs / (rs + a) * Vs, "Combine the parallel pair first."),
                                       (rs / (rs + a + b) * Vs, "The pair is in parallel, not series."),
                                       (rp / (rs + rp) * Vs, "That's the p.d. across the parallel pair.")), CIRC, scaffold, level)
    Vs = random.choice([12.0, 15.0, 9.0])
    (a1, b1), (a2, b2) = random.sample([(2.0, 4.0), (1.0, 4.0), (6.0, 3.0), (3.0, 2.0), (4.0, 4.0), (1.0, 2.0)], 2)
    vx = b1 / (a1 + b1) * Vs
    vy = b2 / (a2 + b2) * Vs
    d = abs(vx - vy)
    if d < 0.2:
        return gen_he_divider(level)
    text = (f"Two potential dividers are connected in parallel across a {Vs:g} V supply. Branch 1: {a1:g} kΩ above {b1:g} kΩ, with X between them. "
            f"Branch 2: {a2:g} kΩ above {b2:g} kΩ, with Y between them. Calculate the reading on a voltmeter connected between X and Y.")
    work = [_L(rf"V_X = \left(\frac{{{b1:g}}}{{{a1 + b1:g}}}\right)\times{Vs:g} = {_ltx(vx)}\ \mathrm{{V}}"),
            _L(rf"V_Y = \left(\frac{{{b2:g}}}{{{a2 + b2:g}}}\right)\times{Vs:g} = {_ltx(vy)}\ \mathrm{{V}}"), _L(rf"V_{{XY}} = {_ltx(d)}\ \mathrm{{V}}")]
    scaffold = [{"question": "What is the p.d. across the lower resistor in branch 1, in V?", "answer": _sig(vx)},
                {"question": "What is the p.d. across the lower resistor in branch 2, in V?", "answer": _sig(vy)},
                {"question": "What is the voltmeter reading, in V?", "answer": _sig(d)}]
    return _q(text, d, "V", _opts(work, d, (vx + vy, "Subtract the two potentials — the voltmeter reads the DIFFERENCE."),
                                  (max(vx, vy), "Find both potentials and subtract.")), CIRC, scaffold, level)


def gen_he_circuit_explain(level="Higher"):
    kind = random.choice(["switch", "thermistor", "lamp"])
    if kind == "switch":
        return _choice("Closing a switch connects an extra resistor in parallel with part of a circuit. Why does the supply current increase?",
                       "The total resistance of the circuit decreases.",
                       [("The resistance decreases.", "Say which resistance — the TOTAL resistance of the circuit."),
                        ("The current is shared between more branches.", "Sharing doesn't increase the supply current; the lower total resistance does."),
                        ("The supply voltage increases.", "The supply p.d. is unchanged.")], CIRC, level)
    if kind == "thermistor":
        return _choice("A thermistor (resistance falls as it warms) is in series with a fixed resistor. A voltmeter is across the fixed resistor. The temperature rises. What happens to the reading?",
                       "It increases, because the thermistor takes a smaller share of the supply p.d.",
                       [("It decreases, because the thermistor's resistance falls.", "The thermistor's share falls, so the fixed resistor's share rises."),
                        ("It stays the same, because the supply p.d. is fixed.", "The p.d. is shared in the ratio of the resistances."),
                        ("It increases, because the thermistor's resistance increases.", "A thermistor's resistance falls as it warms.")], CIRC, level)
    return _choice("A lamp (6 Ω) is in series with a 6 V supply and either a 3 Ω resistor, a 6 Ω resistor, or 3 Ω ∥ 6 Ω. Which gives the greatest power in the lamp?",
                   "3 Ω ∥ 6 Ω — it has the smallest resistance (2 Ω), so the lamp gets the largest share of the p.d.",
                   [("6 Ω — the largest resistor protects the lamp.", "More series resistance means LESS p.d. and current for the lamp."),
                    ("3 Ω — it is the smallest single resistor.", "The parallel pair (2 Ω) is smaller than either resistor."),
                    ("All the same — the supply is 6 V in each case.", "The lamp's share of the 6 V depends on the series resistance (2025 Paper 1).")], CIRC, level)


# ════════════════ Electrical sources and internal resistance ════════════════

def gen_he_emf_calc(level="Higher"):
    kind = random.choice(["r", "lost", "tpd", "cells"])
    if kind == "r":
        E = random.choice([1.5, 4.5, 6.0, 9.0, 12.0])
        r = random.choice([0.2, 0.5, 1.0, 2.0])
        R = random.choice([2.0, 3.0, 5.0, 10.0])
        I = E / (R + r)
        V = I * R
        Vs, Is = _sig(V), _sig(I)
        rr = (E - Vs) / Is
        text = f"A battery of e.m.f. {E:g} V supplies {_txt(Is)} A. The t.p.d. is {_txt(Vs)} V. Calculate the internal resistance."
        work = [_L(r"E = V + Ir"), _L(rf"{E:g} = {_ltx(Vs)} + {_ltx(Is)} \times r"), _L(rf"r = {_ltx(rr)}\ \Omega")]
        return _q(text, rr, "Ω", _opts(work, rr, (E / Is, "E ÷ I is the TOTAL resistance (R + r)."), (Vs / Is, "V ÷ I is the external resistance R.")), IR, None, level)
    E = random.choice([6.0, 9.0, 12.0, 4.5])
    r = random.choice([0.5, 1.0, 2.0, 4.0])
    R = random.choice([2.5, 4.0, 6.0, 8.0])
    if kind == "cells":
        n = random.choice([2, 3, 4])
        e1, r1 = random.choice([(1.5, 0.5), (1.5, 0.2), (2.0, 0.25)])
        E, r = n * e1, n * r1
        I = E / (R + r)
        text = f"{n} identical cells, each of e.m.f. {e1:g} V and internal resistance {r1:g} Ω, are connected in series to a {R:g} Ω resistor. Calculate the current."
        work = [_L(rf"E = {n} \times {e1:g} = {E:g}\ \mathrm{{V}},\ r = {n} \times {r1:g} = {_ltx(r)}\ \Omega"), _L(r"E = V + Ir"),
                _L(rf"{E:g} = I \times {R:g} + I \times {_ltx(r)}"), _L(rf"I = {_ltx(I)}\ \mathrm{{A}}")]
        scaffold = [{"question": "What is the total e.m.f., in V?", "answer": E}, {"question": "What is the total internal resistance, in Ω?", "answer": _sig(r)},
                    {"question": "What is the current, in A?", "answer": _sig(I)}]
        return _q(text, I, "A", _opts(work, I, (E / (R + r1), "Add ALL the internal resistances (cells in series)."), (E / R, "Include the internal resistance.")), IR, scaffold, level)
    I = E / (R + r)
    lost, tpd = I * r, I * R
    want = "lost volts" if kind == "lost" else "t.p.d."
    ans = lost if kind == "lost" else tpd
    other = tpd if kind == "lost" else lost
    text = f"A battery of e.m.f. {E:g} V and internal resistance {r:g} Ω is connected to a {R:g} Ω resistor. Calculate the {want}."
    work = [_L(r"E = V + Ir \quad (V = IR)"), _L(rf"{E:g} = I \times {R:g} + I \times {r:g}"), _L(rf"I = {_ltx(I)}\ \mathrm{{A}}"),
            _L(rf"\text{{{want}}} = {_ltx(I)} \times {r if kind == 'lost' else R:g} = {_ltx(ans)}\ \mathrm{{V}}")]
    scaffold = [{"question": "What is the current, in A?", "answer": _sig(I)}, {"question": f"What is the {want}, in V?", "answer": _sig(ans)}]
    return _q(text, ans, "V", _opts(work, ans, (other, f"That's the {'t.p.d.' if kind == 'lost' else 'lost volts'} — check which p.d. is asked for."),
                                    (E / R * (r if kind == "lost" else R), "Include the internal resistance when finding the current.")), IR, scaffold, level)


def gen_he_emf_graph(level="Higher"):
    E = random.choice([1.5, 4.5, 6.0, 9.0, 12.0])
    r = random.choice([0.5, 1.0, 1.5, 2.0, 3.0])
    I2 = random.choice([0.5, 1.0, 1.5, 2.0])
    if E - I2 * r <= 0.2:
        return gen_he_emf_graph(level)
    V2 = E - I2 * r
    kind = random.choice(["r", "isc"])
    pts = f"meets the V axis at {E:g} V and passes through ({I2:g} A, {_txt(V2)} V)"
    if kind == "r":
        text = f"A graph of t.p.d. V against current I for a battery is a straight line that {pts}. Determine the internal resistance."
        work = [_L(r"\text{gradient} = -r"), _L(rf"-r = \frac{{{_ltx(V2)} - {E:g}}}{{{I2:g}}}"), _L(rf"r = {_ltx(r)}\ \Omega")]
        return _q(text, r, "Ω", _opts(work, r, (E / I2, "E ÷ I is not r — use the gradient (or E = V + Ir)."),
                                      (V2 / I2, "V ÷ I gives the external resistance.")), IR, None, level)
    isc = E / r
    text = f"A graph of t.p.d. V against current I for a battery is a straight line that {pts}. Calculate the short-circuit current."
    work = [_L(rf"r = -\text{{gradient}} = {_ltx(r)}\ \Omega"), _L(r"\text{short circuit: } V = 0,\ E = Ir"), _L(rf"I = \frac{{{E:g}}}{{{_ltx(r)}}} = {_ltx(isc)}\ \mathrm{{A}}")]
    scaffold = [{"question": "What is the internal resistance, in Ω?", "answer": _sig(r)}, {"question": "What is the short-circuit current, in A?", "answer": _sig(isc)}]
    return _q(text, isc, "A", _opts(work, isc, (I2, "The short-circuit current is where V = 0 — extrapolate, don't use the last point (course report 2024)."),
                                    (E * r, "I = E ÷ r.")), IR, scaffold, level)


def gen_he_emf_explain(level="Higher"):
    kind = random.choice(["emf", "switch", "Rup", "measure"])
    if kind == "emf":
        return _choice("A cell has an e.m.f. of 1.5 V. What does this mean?", "1.5 J of energy is supplied to each coulomb of charge passing through the cell.",
                       [("The p.d. across the cell's terminals is always 1.5 V.", "Only on open circuit — the t.p.d. falls when there is a current."),
                        ("The cell supplies 1.5 J of energy in total.", "It is energy per COULOMB."),
                        ("1.5 V is lost inside the cell.", "That describes lost volts.")], IR, level)
    if kind == "switch":
        return _choice("A voltmeter across a battery reads 6.0 V. When a lamp is switched on, it reads 5.4 V. Why?",
                       "There is now a current, so there are lost volts across the internal resistance.",
                       [("Because of lost volts.", "Not enough — explain that the current causes lost volts across r (course report 2019)."),
                        ("The lamp uses up some of the e.m.f.", "The e.m.f. doesn't change."),
                        ("The internal resistance increases when there is a current.", "r is constant; the current makes Ir non-zero.")], IR, level)
    if kind == "Rup":
        return _choice("The external resistance connected to a battery is increased. What happens to the t.p.d.?",
                       "It increases: the current decreases, so the lost volts decrease.",
                       [("It decreases: the resistance is bigger.", "Bigger R → smaller I → smaller Ir → larger t.p.d."),
                        ("It stays equal to the e.m.f.", "Only true on open circuit."),
                        ("It increases because the e.m.f. increases.", "The e.m.f. is fixed.")], IR, level)
    return _choice("How is the e.m.f. of a battery found from a graph of t.p.d. against current?",
                   "It is the intercept on the voltage axis (where I = 0).",
                   [("It is the gradient of the line.", "The gradient is −r."),
                    ("It is the intercept on the current axis.", "That's the short-circuit current."),
                    ("It is the largest voltage reading taken.", "Extrapolate to I = 0.")], IR, level)


# ════════════════ Capacitors ════════════════

def gen_he_cap_charge(level="Higher"):
    kind = random.choice(["Q", "C", "It"])
    if kind == "It":
        I_ua = random.choice([15, 25, 30, 50, 100])
        t = random.choice([20, 25, 28, 40, 60])
        V = random.choice([5.0, 6.0, 9.0, 12.0])
        Q = I_ua * 1e-6 * t
        Cf = Q / V
        text = f"A capacitor is charged at a constant current of {I_ua} µA for {t} s, after which the p.d. across it is {V:g} V. Calculate its capacitance."
        work = [_L(r"Q = It"), _L(rf"Q = {I_ua}\times10^{{-6}} \times {t} = {_ltx(Q)}\ \mathrm{{C}}"), _L(r"C = \frac QV"),
                _L(rf"C = \frac{{{_ltx(Q)}}}{{{V:g}}} = {_ltx(Cf)}\ \mathrm{{F}}")]
        scaffold = [{"question": "What is the charge stored, in C?", "answer": _sig(Q)}, {"question": "What is the capacitance, in F?", "answer": _sig(Cf)}]
        return _q(text, Cf, "F", _opts(work, Cf, (I_ua * t / V, "Convert µA to A."), (Q * V, "C = Q ÷ V.")), CAP, scaffold, level)
    c_uf = random.choice([20, 22, 47, 100, 220, 470])
    V = random.choice([6.0, 9.0, 12.0, 25.0])
    Q = c_uf * 1e-6 * V
    if kind == "Q":
        text = f"A {c_uf} µF capacitor is charged to {V:g} V. Calculate the charge stored."
        work = [_L(r"C = \frac QV"), _L(rf"{c_uf}\times10^{{-6}} = \frac{{Q}}{{{V:g}}}"), _L(rf"Q = {_ltx(Q)}\ \mathrm{{C}}")]
        return _q(text, Q, "C", _opts(work, Q, (c_uf * 1e-6 / V, "Rearrange: Q = CV."), (0.5 * Q, "½CV is not an equation — Q = CV."),
                                      (c_uf * V * 1e-3, "µ means 10⁻⁶.")), CAP, None, level)
    Vs = random.choice([9.0, 12.0])
    Vr = random.choice([3.0, 4.0, 7.0, 5.0])
    Vc = Vs - Vr
    Q = c_uf * 1e-6 * Vc
    text = (f"A {c_uf} µF capacitor is charging from a {Vs:g} V battery through a resistor. A voltmeter across the RESISTOR reads {Vr:g} V. "
            f"Calculate the charge on the capacitor at that instant.")
    work = [_L(rf"V_C = {Vs:g} - {Vr:g} = {Vc:g}\ \mathrm{{V}}"), _L(r"C = \frac QV"), _L(rf"Q = {c_uf}\times10^{{-6}} \times {Vc:g} = {_ltx(Q)}\ \mathrm{{C}}")]
    scaffold = [{"question": "What is the p.d. across the capacitor, in V?", "answer": Vc}, {"question": "What is the charge, in C?", "answer": _sig(Q)}]
    return _q(text, Q, "C", _opts(work, Q, (c_uf * 1e-6 * Vr, "The voltmeter is across the RESISTOR — V_C = supply − V_R (2022 Paper 1)."),
                                  (c_uf * 1e-6 * Vs, "The capacitor isn't fully charged yet.")), CAP, scaffold, level)


def gen_he_cap_energy(level="Higher"):
    kind = random.choice(["CV", "QV", "It", "divider"])
    if kind == "CV":
        c_uf = random.choice([47, 100, 220, 470, 4700])
        V = random.choice([6.0, 9.0, 12.0, 16.0])
        En = 0.5 * c_uf * 1e-6 * V ** 2
        text = f"A {c_uf} µF capacitor is charged to {V:g} V. Calculate the energy stored."
        work = [_L(r"E = \tfrac12 CV^2"), _L(rf"E = \tfrac12 \times {c_uf}\times10^{{-6}} \times {V:g}^2 = {_ltx(En)}\ \mathrm{{J}}")]
        return _q(text, En, "J", _opts(work, En, (2 * En, "E = ½CV² — include the ½."), (0.5 * c_uf * 1e-6 * V, "Square the p.d."),
                                       (0.5 * c_uf * V ** 2, "Convert µF to F.")), CAP, None, level)
    if kind == "QV":
        c_uf, kv = random.choice([(64, 2.5), (32, 2.0), (100, 1.5)])
        Q = c_uf * 1e-6 * kv * 1e3
        En = 0.5 * Q * kv * 1e3
        text = f"A defibrillator's {c_uf} µF capacitor is charged to {kv:g} kV. Calculate the energy stored."
        work = [_L(r"C = \frac QV:\ Q = " + _ltx(Q) + r"\ \mathrm{C}"), _L(r"E = \tfrac12 QV"), _L(rf"E = \tfrac12 \times {_ltx(Q)} \times {kv * 1000:g} = {_ltx(En)}\ \mathrm{{J}}")]
        scaffold = [{"question": "What is the charge stored, in C?", "answer": _sig(Q)}, {"question": "What is the energy stored, in J?", "answer": _sig(En)}]
        return _q(text, En, "J", _opts(work, En, (2 * En, "E = ½QV — include the ½."), (En / 1e6, "kV → V is × 1000, so the energy is large.")), CAP, scaffold, level)
    if kind == "It":
        I_ma, t, V = random.choice([(0.10, 20, 12), (0.20, 30, 9.0), (0.50, 10, 6.0)])
        Q = I_ma * 1e-3 * t
        En = 0.5 * Q * V
        text = f"A capacitor is charged at a constant {I_ma:g} mA for {t} s. The p.d. across it is then {V:g} V. Calculate the energy stored."
        work = [_L(rf"Q = It = {I_ma:g}\times10^{{-3}} \times {t} = {_ltx(Q)}\ \mathrm{{C}}"), _L(r"E = \tfrac12 QV"), _L(rf"E = {_ltx(En)}\ \mathrm{{J}}")]
        scaffold = [{"question": "What is the charge stored, in C?", "answer": _sig(Q)}, {"question": "What is the energy stored, in J?", "answer": _sig(En)}]
        return _q(text, En, "J", _opts(work, En, (2 * En, "E = ½QV — include the ½ (2024 Paper 1 Q21)."), (0.5 * Q * V ** 2, "E = ½QV — V is not squared here.")), CAP, scaffold, level)
    r1, r2, Vs = random.choice([(480, 120, 6.0), (1000, 2000, 9.0), (16, 16, 12.0)])
    c_uf = random.choice([20, 30, 100])
    Vc = r2 / (r1 + r2) * Vs
    En = 0.5 * c_uf * 1e-6 * Vc ** 2
    text = f"A {c_uf} µF capacitor is connected across the {r2:g} Ω resistor of a potential divider ({r1:g} Ω and {r2:g} Ω in series across {Vs:g} V). Calculate the maximum energy stored."
    work = [_L(rf"V_C = \left(\frac{{{r2:g}}}{{{r1 + r2:g}}}\right)\times{Vs:g} = {_ltx(Vc)}\ \mathrm{{V}}"), _L(r"E = \tfrac12 CV^2"), _L(rf"E = {_ltx(En)}\ \mathrm{{J}}")]
    scaffold = [{"question": "What is the p.d. across the capacitor, in V?", "answer": _sig(Vc)}, {"question": "What is the energy stored, in J?", "answer": _sig(En)}]
    return _q(text, En, "J", _opts(work, En, (0.5 * c_uf * 1e-6 * Vs ** 2, "The capacitor only gets the p.d. across its resistor (2017 Paper 1 Q18)."),
                                   (c_uf * 1e-6 * Vc ** 2, "Include the ½.")), CAP, scaffold, level)


def gen_he_cap_curves(level="Higher"):
    kind = random.choice(["R", "C", "why", "increase", "constant"])
    if kind == "R":
        return _choice("A capacitor is charged again through a resistor of GREATER resistance. How does the current–time graph change?",
                       "Smaller initial current, and it takes longer to fall to zero.",
                       [("Same initial current, takes longer to fall to zero.", "I₀ = V/R — a bigger R gives a SMALLER initial current (course report 2015)."),
                        ("Larger initial current, falls to zero faster.", "Bigger R → smaller current, slower charging."),
                        ("Smaller initial current, falls to zero faster.", "A smaller current takes LONGER to charge it.")], CAP, level)
    if kind == "C":
        return _choice("A capacitor is replaced by one of GREATER capacitance and charged through the same resistor. How does the current–time graph change?",
                       "Same initial current, but it takes longer to fall to zero.",
                       [("Larger initial current, takes longer.", "The initial current is V/R — it doesn't depend on C (2024 Paper 1 Q22)."),
                        ("Smaller initial current, takes longer.", "Only R changes the initial current."),
                        ("Same initial current, falls to zero faster.", "More charge must flow, so it takes longer.")], CAP, level)
    if kind == "why":
        return _choice("Why does the charging current decrease as a capacitor charges through a resistor?",
                       "The p.d. across the capacitor increases, so the p.d. across the resistor (and the current) decreases.",
                       [("The capacitor gets full.", "Explain in terms of p.d. (course report 2015)."),
                        ("The resistor heats up and its resistance rises.", "The resistance is constant."),
                        ("The supply p.d. decreases.", "The supply p.d. is constant — it is shared differently.")], CAP, level)
    if kind == "increase":
        return _choice("Suggest an alteration to the circuit that would increase the maximum energy stored by THIS 47 µF capacitor.",
                       "Increase the supply voltage.",
                       [("Use a capacitor of greater capacitance.", "The question is about this 47 µF capacitor (course report 2019)."),
                        ("Use a larger resistor.", "R changes the charging time, not the energy ½CV²."),
                        ("Charge it for longer.", "Once fully charged, waiting longer adds nothing.")], CAP, level)
    return _choice("A capacitor is charged at a constant current by adjusting a variable resistor. How must the resistance change as it charges?",
                   "It must be decreased, because the p.d. across the resistor falls as the p.d. across the capacitor rises.",
                   [("It must be increased, because the capacitor's p.d. rises.", "A rising V_C leaves LESS p.d. for R, so R must fall to keep I = V_R/R."),
                    ("It must stay the same, because the current is constant.", "Without adjustment the current would fall (course report 2025)."),
                    ("It must be decreased, because the capacitor's resistance falls.", "Explain using the p.d. across R.")], CAP, level)


# ════════════════ Semiconductors and p-n junctions ════════════════
_LEDS = [("red", 625, 680), ("orange", 600, 615), ("yellow", 585, 595), ("green", 520, 560), ("blue", 450, 475)]


def gen_he_led_photon(level="Higher"):
    colour, lo, hi = random.choice(_LEDS)
    lam = random.randint(lo, hi)
    f = C / (lam * 1e-9)
    En = H * f
    if random.random() < 0.5:
        text = f"A {colour} LED emits light of wavelength {lam} nm. Calculate the band gap energy (the energy of each photon)."
        work = [_L(r"v = f\lambda"), _L(rf"3.00\times10^8 = f \times {lam}\times10^{{-9}},\ f = {_ltx(f)}\ \mathrm{{Hz}}"), _L(r"E = hf"),
                _L(rf"E = 6.63\times10^{{-34}} \times {_ltx(f)} = {_ltx(En)}\ \mathrm{{J}}")]
        scaffold = [{"question": "What is the frequency, in Hz?", "answer": _sig(f)}, {"question": "What is the photon energy, in J?", "answer": _sig(En)}]
        return _q(text, En, "J", _opts(work, En, (H * C / lam, "Convert nm to m."), (H * lam * 1e-9 / C, "f = v ÷ λ, then E = hf.")), SEMI, scaffold, level)
    Es = _sig(En)
    lam_m = H * C / Es
    text = f"The band gap of an LED is {_txt(Es)} J. Calculate the wavelength of the light it emits."
    work = [_L(r"E = hf"), _L(rf"{_ltx(Es)} = 6.63\times10^{{-34}} \times f,\ f = {_ltx(Es / H)}\ \mathrm{{Hz}}"), _L(r"v = f\lambda"),
            _L(rf"\lambda = \frac{{3.00\times10^8}}{{{_ltx(Es / H)}}} = {_ltx(lam_m)}\ \mathrm{{m}}")]
    scaffold = [{"question": "What is the frequency, in Hz?", "answer": _sig(Es / H)}, {"question": "What is the wavelength, in m?", "answer": _sig(lam_m)}]
    return _q(text, lam_m, "m", _opts(work, lam_m, (Es / H, "That's the frequency — use v = fλ for the wavelength."),
                                      (C * Es / H, "λ = v ÷ f.")), SEMI, scaffold, level)


def gen_he_band_explain(level="Higher"):
    kind = random.choice(["semi_rt", "temp", "led", "solar", "redblue", "insulator", "dc_leds"])
    if kind == "semi_rt":
        return _choice("Using band theory, why can a semiconductor conduct at room temperature?",
                       "The band gap is small, so some electrons gain enough energy to move from the valence band into the conduction band.",
                       [("Its conduction band is completely full of electrons.", "A full band can't conduct; conductors have partly filled bands."),
                        ("Electrons jump into the conductive band.", "Name the bands correctly — valence and conduction (MI)."),
                        ("Its valence and conduction bands overlap.", "That describes some metals.")], SEMI, level)
    if kind == "temp":
        return _choice("How does an increase in temperature affect a semiconductor?",
                       "Its conductivity increases, because more electrons reach the conduction band.",
                       [("Its conductivity increases, because the band gap gets smaller.", "The band gap does not change."),
                        ("Its conductivity decreases, like a metal's.", "A semiconductor's conductivity INCREASES (2023 Paper 1 Q23)."),
                        ("No effect on its conductivity.", "More electrons gain enough energy to cross the gap (2024 Paper 1 Q24).")], SEMI, level)
    if kind == "led":
        return _choice("Using band theory, how does a forward-biased LED emit light?",
                       "Electrons move from the n-type conduction band towards the p-type, fall from the conduction band into the valence band, and emit photons.",
                       [("Holes and electrons recombine at the junction and give out light.", "No band theory — 0 marks (course reports 2016, 2018)."),
                        ("Electrons absorb photons and move from the valence band to the conduction band.", "That is how a SOLAR CELL works."),
                        ("Holes move up from the valence band to the conduction band, emitting photons.", "Wrong physics — 0 marks (MI).")], SEMI, level)
    if kind == "solar":
        return _choice("Using band theory, how does a solar cell produce a p.d.?",
                       "Electrons absorb energy from photons and move from the valence band to the conduction band; the junction moves them towards the n-type.",
                       [("Electrons fall from the conduction band to the valence band, emitting photons.", "That's an LED (course reports 2022, 2024)."),
                        ("Photons knock electrons out of the surface of the cell.", "That's the photoelectric effect, not the photovoltaic effect."),
                        ("The light heats the junction, so it conducts.", "It is photon absorption, not heating.")], SEMI, level)
    if kind == "redblue":
        return _choice("What is the difference between red and blue LEDs?",
                       "The blue LED has a larger band gap, so its photons have more energy.",
                       [("The red LED has a larger band gap.", "Red photons have less energy — smaller band gap."),
                        ("The blue LED has a larger p.d. across it, which sets its wavelength.", "The band gap, not the applied p.d., sets the wavelength (2025 Paper 1 Q23)."),
                        ("They have the same band gap but different doping.", "Mention the band gap (course report 2023).")], SEMI, level)
    if kind == "insulator":
        return _choice("Which describes an insulator?", "Full valence band, empty (unfilled) conduction band, large band gap.",
                       [("Unfilled conduction band, bands overlap.", "Overlapping bands = a conductor."),
                        ("Full conduction band, small gap.", "The conduction band is unfilled."),
                        ("Partly filled valence band.", "That describes a metal.")], SEMI, level)
    return _choice("Two LEDs are connected in series with each other, facing opposite ways, across a d.c. supply. What happens?",
                   "Neither lights — one is always reverse biased, so there is no current in the branch.",
                   [("The forward-biased one lights.", "A reverse-biased LED in series blocks the current (2019 Paper 1 Q24)."),
                    ("Both light dimly.", "There is no current at all."),
                    ("They light alternately.", "That needs an a.c. supply and LEDs in parallel.")], SEMI, level)
