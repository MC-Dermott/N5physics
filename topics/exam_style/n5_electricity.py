"""N5 Electricity — exam-style multi-part questions, one generator per topic.

Recognised wrong answers follow the N5 marking instructions and course reports: mA/minutes/kΩ not
converted, series and parallel rules swapped, 1/R_T left uninverted, the supply voltage used across
one component, the wrong form of the power relationship, and the fuse rating chosen below the
working current.
"""
import math
import random

from topics.exam_style.base import Exam, T, exam_style, fmt, graph, ltx, pick, sig

UNIT = "Electricity"
E_CHARGE = 1.6e-19


def _notes(title, body):
    return f"## {title} — exam technique\n\n{body}"


NOTES = {
    "Current": _notes("Current", r"""
$Q = It$ — current is the **rate of flow of charge** (1 A = 1 C per second). Convert mA → A (÷ 1000) and minutes/hours → s.

In a metal wire the charge carriers are **electrons**.
"""),
    "Ohm's Law": _notes("Ohm's law", r"""
$V = IR$ — convert mA → A and kΩ → Ω.

- A V–I graph that is a straight line through the origin → **constant resistance**; $R$ = gradient = $V/I$.
- A filament lamp's resistance **increases** as its temperature increases.
"""),
    "Resistors": _notes("Resistors", r"""
Series: $R_T = R_1 + R_2 + \dots$ &nbsp;&nbsp; Parallel: $\frac{1}{R_T} = \frac{1}{R_1} + \frac{1}{R_2} + \dots$ — remember to **invert** at the end.

- Adding a resistor in **series** increases $R_T$; adding one in **parallel** decreases $R_T$.
- The total resistance of a parallel combination is smaller than the smallest branch.
"""),
    "Electrical Power": _notes("Electrical power", r"""
$P = IV$ &nbsp; $P = I^2R$ &nbsp; $P = \frac{V^2}{R}$ &nbsp; $E = Pt$ — power is energy **per second** (W = J/s).

Choose the form of the power relationship that uses the quantities you know. Time in **seconds**.
"""),
    "Potential Divider": _notes("Potential dividers", r"""
$\frac{V_1}{V_2} = \frac{R_1}{R_2}$ &nbsp; $V_2 = \left(\frac{R_2}{R_1 + R_2}\right)V_s$

- The larger resistor gets the larger share of the supply voltage.
- Thermistor: resistance **decreases** as temperature increases. LDR: resistance **decreases** as light level increases.
"""),
    "Circuits": _notes("Circuits", r"""
**Series:** same current everywhere; supply voltage = sum of the component voltages.
**Parallel:** same voltage across each branch; supply current = sum of the branch currents.

Ammeters go in **series**; voltmeters go in **parallel** across the component.
"""),
    "Charge Carriers": _notes("Charge carriers", r"""
$Q = It$; charge on one electron $= 1.6 \times 10^{-19}$ C, so number of electrons $= Q \div 1.6\times10^{-19}$.

- d.c. — charges flow in **one direction only**; a.c. — the direction of flow **changes regularly**.
- A charged particle in an electric field experiences a **force**.
"""),
    "Potential Difference": _notes("Potential difference", r"""
$E_w = QV$ — the potential difference (voltage) is the **energy transferred per unit charge** (1 V = 1 J per coulomb).

$R$ = gradient of a V–I graph = $\frac{\Delta V}{\Delta I}$.
"""),
    "Circuit Rules": _notes("Circuit rules", r"""
**Series:** $I_1 = I_2 = I_s$, $V_s = V_1 + V_2$. **Parallel:** $V_1 = V_2 = V_s$, $I_s = I_1 + I_2$.

Adding a lamp in series → greater total resistance → smaller current → lamps dimmer. Adding a lamp in parallel → each lamp still has the full supply voltage.
"""),
    "LEDs and Transistor Switches": _notes("LEDs and transistor switches", r"""
**LED:** a series resistor limits the current. $V_R = V_s - V_{LED}$, then $R = V_R \div I$.

**Transistor switch:** a potential divider (with an LDR or thermistor) sets the voltage across the transistor's input.
When that voltage reaches the switching value (e.g. 0.7 V for an NPN transistor) the transistor switches **on** and the output device operates.
"""),
    "Power and Fuses": _notes("Power and fuses", r"""
$P = IV$ &nbsp; $P = I^2R$ &nbsp; $P = \frac{V^2}{R}$ &nbsp; $E = Pt$. Mains voltage = 230 V.

**Fuse:** choose the rating just **above** the normal operating current (3 A or 13 A). The fuse protects the **flex (cable)** from overheating.
"""),
}


def _ex(qtype, level):
    return Exam(UNIT, qtype, level, NOTES[qtype])


def _par(*rs):
    return 1 / sum(1 / r for r in rs)


# ════════════════ Current ════════════════

def _current_phone(level="N5"):
    ex = _ex("Current", level)
    I_mA, hrs = pick(400, 500, 750, 800, 1200), pick(1.5, 2, 2.5, 3)
    I, t = I_mA / 1000, hrs * 3600
    Q = I * t
    ex.num(f"The charger supplies a current of {I_mA} mA for {hrs:g} hours. Calculate the charge that flows.", Q, "C",
           wrong=[(I_mA * t, "Convert mA to A (÷ 1000)."), (I * hrs, "Convert hours to seconds (× 3600)."),
                  (I_mA * hrs, "Convert to A and s.")],
           working=[r"Q = It", rf"Q = {I:g} \times ({hrs:g} \times 3600)", rf"Q = {ltx(Q)}\ \text{{C}}"],
           scaffold=[("Current in A?", I, "A"), ("Time in s?", t, "s")])
    I2 = pick(1.5, 2.0, 2.4, 3.0)
    t2 = Q / I2
    ex.num(f"A fast charger supplies the same charge with a current of {I2:g} A. Calculate the time taken, in seconds.", t2, "s",
           wrong=[(Q * I2, "t = Q ÷ I."), (I2 / Q, "t = Q ÷ I.")],
           working=[r"t = \frac{Q}{I}", rf"t = \frac{{{ltx(Q)}}}{{{I2:g}}} = {ltx(t2)}\ \text{{s}}"])
    ex.choice("What is meant by an electric current?", "The rate of flow of charge (the charge passing a point each second).",
              [("The energy given to each coulomb of charge.", "That's potential difference (voltage)."),
               ("The opposition to the flow of charge.", "That's resistance."),
               ("The total amount of charge stored in the battery.", "Current is a RATE: charge per second.")])
    return ex.build("A mobile phone battery is charged from a USB charger.")


def _current_lightning(level="N5"):
    ex = _ex("Current", level)
    Q, t_ms = pick(5, 8, 12, 15, 20), pick(0.2, 0.25, 0.4, 0.5)
    t = t_ms / 1000
    I = Q / t
    ex.num(f"A lightning strike transfers {Q} C of charge in {t_ms:g} ms. Calculate the average current.", I, "A",
           wrong=[(Q / t_ms, "Convert ms to s (÷ 1000)."), (Q * t, "I = Q ÷ t.")],
           working=[r"Q = It \Rightarrow I = \frac{Q}{t}", rf"I = \frac{{{Q}}}{{{t:g}}} = {ltx(I)}\ \text{{A}}"])
    N = Q / E_CHARGE
    ex.num("Calculate the number of electrons transferred (charge on an electron = 1.6 × 10⁻¹⁹ C).", N, "",
           wrong=[(Q * E_CHARGE, "Number of electrons = total charge ÷ charge per electron.")],
           working=[r"N = \frac{Q}{e}", rf"N = \frac{{{Q}}}{{1.6 \times 10^{{-19}}}} = {ltx(N)}"])
    ex.choice("What are the charge carriers in a metal wire?", "Electrons",
              [("Protons", "Protons are fixed in the nuclei."), ("Neutrons", "Neutrons have no charge."), ("Atoms", "Free electrons move, not whole atoms.")])
    return ex.build("During a thunderstorm, charge flows between a cloud and the ground.")


gen_current_exam = exam_style(_current_phone, _current_lightning)


# ════════════════ Ohm's Law ════════════════

def _ohm_graph(level="N5"):
    ex = _ex("Ohm's Law", level)
    R = pick(10, 15, 20, 25, 40, 50)
    Imax = pick(0.2, 0.3, 0.4, 0.5)
    pts = [(round(Imax * k / 4, 3), round(R * Imax * k / 4, 3)) for k in range(5)]
    fig = graph(pts, xlabel="Current (A)", ylabel="Voltage (V)")
    Ip, Vp = pts[3]
    ex.num("Use the graph to calculate the resistance of the resistor.", R, "Ω",
           wrong=[(Ip / Vp, "R = V ÷ I."), (Vp * Ip, "R = V ÷ I.")],
           working=[T(f"From the graph, V = {Vp:g} V when I = {Ip:g} A."), r"R = \frac{V}{I}", rf"R = \frac{{{Vp:g}}}{{{Ip:g}}} = {R}\ \Omega"])
    V2 = pick(9, 12, 15, 24)
    I2 = V2 / R
    ex.num(f"The resistor is connected to a {V2} V supply. Calculate the current in it.", I2, "A",
           wrong=[(V2 * R, "I = V ÷ R."), (R / V2, "I = V ÷ R.")],
           working=[r"V = IR \Rightarrow I = \frac{V}{R}", rf"I = \frac{{{V2}}}{{{R}}} = {ltx(I2)}\ \text{{A}}"])
    ex.choice("What does the shape of the graph show about the resistor?",
              "Its resistance is constant — the current is directly proportional to the voltage.",
              [("Its resistance increases as the current increases.", "That would give a curved graph."),
               ("Its resistance is zero.", "The gradient (V/I) is not zero."),
               ("The voltage is inversely proportional to the current.", "A straight line through the origin shows DIRECT proportion.")])
    return ex.build("A pupil measures the voltage across a resistor for different currents. The results are shown in the graph.", figure=fig)


def _ohm_heater(level="N5"):
    ex = _ex("Ohm's Law", level)
    R_k = pick(1.2, 1.5, 2.2, 3.3, 4.7)
    V = pick(6, 9, 12)
    I = V / (R_k * 1000)
    ex.num(f"A {R_k:g} kΩ resistor is connected to a {V} V battery. Calculate the current in the resistor.", I, "A",
           wrong=[(V / R_k, "Convert kΩ to Ω (× 1000)."), (V * R_k * 1000, "I = V ÷ R.")],
           working=[r"I = \frac{V}{R}", rf"I = \frac{{{V}}}{{{R_k:g} \times 10^3}} = {ltx(I)}\ \text{{A}}"])
    Vl, Il = pick(6, 12), pick(0.25, 0.4, 0.5)
    Rl = Vl / Il
    ex.num(f"A lamp operates at {Vl} V with a current of {Il:g} A. Calculate its resistance when lit.", Rl, "Ω",
           wrong=[(Il / Vl, "R = V ÷ I."), (Vl * Il, "That's the power, not the resistance.")],
           working=[r"R = \frac{V}{I}", rf"R = \frac{{{Vl}}}{{{Il:g}}} = {ltx(Rl)}\ \Omega"])
    ex.choice("The resistance of the lamp measured when it is cold is much smaller than this. Why?",
              "The resistance of the filament increases as its temperature increases.",
              [("The resistance decreases as its temperature increases.", "For a metal filament, resistance INCREASES with temperature."),
               ("The ohmmeter adds extra resistance.", "Not the reason — it's the change in temperature."),
               ("Resistance depends only on the supply voltage.", "Resistance depends on the temperature of the filament.")])
    return ex.build("Pupils use V = IR to investigate components.")


gen_ohms_law_exam = exam_style(_ohm_graph, _ohm_heater)


# ════════════════ Resistors ════════════════

def _res_combo(level="N5"):
    ex = _ex("Resistors", level)
    R1 = pick(4, 6, 10, 12, 22)
    R2, R3 = random.choice([(6, 3), (12, 6), (20, 30), (10, 40), (12, 4), (15, 30)])
    Rp = _par(R2, R3)
    RT = R1 + Rp
    Vs = pick(6, 9, 12, 24)
    ex.num(f"Calculate the combined resistance of R₂ and R₃.", Rp, "Ω",
           wrong=[(R2 + R3, "R₂ and R₃ are in PARALLEL — use 1/R_T = 1/R₁ + 1/R₂."), (1 / R2 + 1 / R3, "Invert at the end: R_T = 1 ÷ (1/R₂ + 1/R₃).")],
           working=[r"\frac{1}{R_P} = \frac{1}{R_2} + \frac{1}{R_3}", rf"\frac{{1}}{{R_P}} = \frac{{1}}{{{R2}}} + \frac{{1}}{{{R3}}}", rf"R_P = {ltx(Rp)}\ \Omega"])
    ex.num("Calculate the total resistance of the circuit.", RT, "Ω",
           wrong=[(R1 + R2 + R3, "R₂ and R₃ are in parallel — use their combined resistance."), (_par(R1, R2, R3), "R₁ is in SERIES with the parallel pair.")],
           working=[rf"R_T = R_1 + R_P = {R1} + {ltx(Rp)} = {ltx(RT)}\ \Omega"])
    I = Vs / sig(RT)
    ex.num("Calculate the current from the supply.", I, "A",
           wrong=[(Vs / R1, "Use the TOTAL resistance."), (Vs * sig(RT), "I = V ÷ R.")],
           working=[r"I = \frac{V}{R_T}", rf"I = \frac{{{Vs}}}{{{ltx(RT)}}} = {ltx(I)}\ \text{{A}}"])
    ex.choice("Another resistor is connected in parallel with R₂ and R₃. What happens to the total resistance of the circuit?",
              "It decreases.",
              [("It increases.", "Adding a resistor in PARALLEL gives another path, lowering the resistance."),
               ("It stays the same.", "The parallel combination's resistance decreases, so R_T decreases."),
               ("It becomes zero.", "It decreases, but not to zero.")])
    return ex.build(f"A {R1} Ω resistor R₁ is connected in series with two resistors, R₂ = {R2} Ω and R₃ = {R3} Ω, which are in "
                    f"parallel with each other. The circuit is connected to a {Vs} V supply.")


def _res_series(level="N5"):
    ex = _ex("Resistors", level)
    R1, R2, R3 = random.sample([10, 15, 20, 22, 33, 47, 68], 3)
    Vs = pick(6, 9, 12)
    RT = R1 + R2 + R3
    I = Vs / RT
    V2 = I * R2
    ex.num("Calculate the total resistance of the circuit.", RT, "Ω",
           wrong=[(_par(R1, R2, R3), "The resistors are in SERIES — just add them.")],
           working=[rf"R_T = {R1} + {R2} + {R3} = {RT}\ \Omega"])
    ex.num("Calculate the current in the circuit.", I, "A",
           wrong=[(Vs / R2, "Use the total resistance for the circuit current."), (RT / Vs, "I = V ÷ R.")],
           working=[rf"I = \frac{{V}}{{R_T}} = \frac{{{Vs}}}{{{RT}}} = {ltx(I)}\ \text{{A}}"])
    ex.num(f"Calculate the voltage across the {R2} Ω resistor.", V2, "V",
           wrong=[(Vs, "The supply voltage is shared between the series resistors."), (Vs / 3, "The voltage divides in proportion to the resistances.")],
           working=[rf"V = IR = {ltx(I)} \times {R2} = {ltx(V2)}\ \text{{V}}"])
    return ex.build(f"Resistors of {R1} Ω, {R2} Ω and {R3} Ω are connected in series with a {Vs} V battery.")


gen_resistors_exam = exam_style(_res_combo, _res_series)


# ════════════════ Electrical Power ════════════════

def _power_kettle(level="N5"):
    ex = _ex("Electrical Power", level)
    P = pick(2000, 2200, 2500, 2760, 3000)
    V = 230
    I = P / V
    R = V ** 2 / P
    ex.num("Calculate the current in the kettle when it is operating.", I, "A",
           wrong=[(P * V, "I = P ÷ V."), (V / P, "I = P ÷ V.")],
           working=[r"P = IV", rf"{P} = I \times 230", rf"I = {ltx(I)}\ \text{{A}}"])
    ex.num("Calculate the resistance of the heating element.", R, "Ω",
           wrong=[(P / V ** 2, "R = V² ÷ P."), (V / P, "Use P = V²/R (or R = V/I).")],
           working=[r"P = \frac{V^2}{R}", rf"{P} = \frac{{230^2}}{{R}}", rf"R = {ltx(R)}\ \Omega"])
    mins = pick(2, 3, 4, 5)
    E = P * mins * 60
    ex.num(f"The kettle is switched on for {mins} minutes. Calculate the energy it uses.", E, "J",
           wrong=[(P * mins, "Convert minutes to seconds."), (P / (mins * 60), "E = P × t.")],
           working=[r"E = Pt", rf"E = {P} \times ({mins} \times 60) = {ltx(E)}\ \text{{J}}"])
    return ex.build(f"An electric kettle is rated at {P} W, 230 V.")


def _power_bulbs(level="N5"):
    ex = _ex("Electrical Power", level)
    Pf, Pl = pick(40, 60, 100), pick(5, 6, 8, 10)
    V = 230
    Il = Pl / V
    ex.num(f"Calculate the current in the {Pl} W LED bulb.", Il, "A",
           wrong=[(Pl * V, "I = P ÷ V."), (V / Pl, "I = P ÷ V.")],
           working=[r"I = \frac{P}{V}", rf"I = \frac{{{Pl}}}{{230}} = {ltx(Il)}\ \text{{A}}"])
    hrs = pick(4, 5, 6, 8)
    saved = (Pf - Pl) * hrs * 3600
    ex.num(f"Both bulbs are switched on for {hrs} hours. Calculate how much less energy the LED bulb uses.", saved, "J",
           wrong=[(Pf * hrs * 3600, "Find the DIFFERENCE in energy used."), ((Pf - Pl) * hrs, "Convert hours to seconds.")],
           working=[rf"E_{{fil}} = {Pf} \times {hrs * 3600} = {ltx(Pf * hrs * 3600)}\ \text{{J}}",
                    rf"E_{{LED}} = {Pl} \times {hrs * 3600} = {ltx(Pl * hrs * 3600)}\ \text{{J}}",
                    rf"\Delta E = {ltx(saved)}\ \text{{J}}"])
    ex.choice("Both bulbs give out the same amount of light. Why does the filament bulb need a greater power?",
              "More of its electrical energy is converted to heat rather than light.",
              [("It gives out more light energy.", "Both give the same light — the filament bulb wastes more as heat."),
               ("It has a greater resistance, so it uses less energy.", "It uses MORE energy each second."),
               ("LED bulbs don't need electrical energy.", "They do, but convert more of it to light.")])
    return ex.build(f"A {Pf} W filament bulb and a {Pl} W LED bulb are both designed for the 230 V mains.")


gen_electrical_power_exam = exam_style(_power_kettle, _power_bulbs)


# ════════════════ Potential Divider ════════════════

def _pd_fixed(level="N5"):
    ex = _ex("Potential Divider", level)
    R1, R2 = random.choice([(1000, 2000), (2200, 3300), (4700, 2200), (10000, 5000), (1500, 4500), (3300, 6800)])
    Vs = pick(6, 9, 12)
    V2 = R2 / (R1 + R2) * Vs
    ex.num("Calculate the total resistance of the circuit.", R1 + R2, "Ω", wrong=[(_par(R1, R2), "The resistors are in series.")],
           working=[rf"R_T = {R1} + {R2} = {R1 + R2}\ \Omega"])
    ex.num("Calculate the voltage across R₂.", V2, "V",
           wrong=[(R1 / (R1 + R2) * Vs, "That's the voltage across R₁ — use R₂ on top."), (R2 / R1 * Vs, "Use R₂ ÷ (R₁ + R₂)."),
                  (Vs / 2, "The voltage divides in proportion to the resistances.")],
           working=[r"V_2 = \left(\frac{R_2}{R_1 + R_2}\right)V_s", rf"V_2 = \frac{{{R2}}}{{{R1} + {R2}}} \times {Vs} = {ltx(V2)}\ \text{{V}}"])
    ex.choice("R₂ is replaced by a resistor with a larger resistance. What happens to the voltage across it?",
              "It increases — it now has a larger share of the supply voltage.",
              [("It decreases.", "A larger resistance gets a LARGER share of the supply voltage."),
               ("It stays the same.", "The share depends on the ratio of the resistances."),
               ("It becomes equal to the supply voltage.", "R₁ still takes some of the voltage.")])
    return ex.build(f"A potential divider is made from R₁ = {R1} Ω and R₂ = {R2} Ω connected in series to a {Vs} V supply.")


def _pd_thermistor(level="N5"):
    ex = _ex("Potential Divider", level)
    Rf = pick(1000, 2200, 4700)
    Rt = pick(1500, 2000, 3000, 5600, 8000)
    Vs = pick(5, 6, 9, 12)
    Vout = Rf / (Rf + Rt) * Vs
    ex.num(f"At 20 °C the thermistor has a resistance of {Rt} Ω. Calculate the voltage across the fixed resistor.", Vout, "V",
           wrong=[(Rt / (Rf + Rt) * Vs, "That's the voltage across the thermistor."), (Rf / Rt * Vs, "Use R_fixed ÷ (R_fixed + R_thermistor).")],
           working=[r"V_{out} = \left(\frac{R_{fixed}}{R_{fixed} + R_T}\right)V_s", rf"V_{{out}} = \frac{{{Rf}}}{{{Rf} + {Rt}}} \times {Vs} = {ltx(Vout)}\ \text{{V}}"])
    I = Vs / (Rf + Rt)
    ex.num("Calculate the current in the circuit at 20 °C.", I, "A",
           wrong=[(Vs / Rf, "Use the TOTAL resistance."), (Vs / Rt, "Use the TOTAL resistance.")],
           working=[rf"I = \frac{{V_s}}{{R_T}} = \frac{{{Vs}}}{{{Rf + Rt}}} = {ltx(I)}\ \text{{A}}"])
    ex.choice("The temperature of the thermistor increases. What happens to the voltage across the fixed resistor?",
              "It increases — the thermistor's resistance decreases, so the fixed resistor takes a bigger share of the supply voltage.",
              [("It decreases — the thermistor's resistance increases.", "A (NTC) thermistor's resistance DECREASES as temperature increases."),
               ("It stays the same — the fixed resistor doesn't change.", "Its SHARE of the voltage depends on the thermistor too."),
               ("It decreases — the current decreases.", "The total resistance falls, so the current increases.")])
    return ex.build(f"A thermistor is connected in series with a {Rf} Ω fixed resistor and a {Vs} V supply.")


gen_potential_divider_exam = exam_style(_pd_fixed, _pd_thermistor)


# ════════════════ Circuits ════════════════

def _circ_series(level="N5"):
    ex = _ex("Circuits", level)
    Vs, VL = pick(9, 12), pick(2.5, 3.0, 4.5, 6.0)
    I = pick(0.2, 0.25, 0.3, 0.5)
    VR = Vs - VL
    ex.num(f"The voltmeter across the lamp reads {VL:g} V. Calculate the voltage across the resistor.", VR, "V",
           wrong=[(Vs, "In series the supply voltage is SHARED."), (VL, "V_R = V_s − V_lamp.")],
           working=[rf"V_s = V_L + V_R \Rightarrow V_R = {Vs} - {VL:g} = {VR:g}\ \text{{V}}"])
    R = VR / I
    ex.num(f"The ammeter reads {I:g} A. Calculate the resistance of the resistor.", R, "Ω",
           wrong=[(Vs / I, "Use the voltage across the RESISTOR."), (VR * I, "R = V ÷ I.")],
           working=[rf"R = \frac{{V_R}}{{I}} = \frac{{{VR:g}}}{{{I:g}}} = {ltx(R)}\ \Omega"])
    ex.choice("How should the voltmeter be connected to measure the voltage across the lamp?",
              "In parallel with the lamp.",
              [("In series with the lamp.", "Ammeters go in series; voltmeters go in parallel."),
               ("In series with the battery.", "A voltmeter goes across (in parallel with) the component."),
               ("Anywhere in the circuit — it reads the same everywhere.", "Voltage is shared in series; connect across the lamp.")])
    return ex.build(f"A lamp and a resistor are connected in series with a {Vs} V battery, an ammeter and a voltmeter.")


def _circ_parallel(level="N5"):
    ex = _ex("Circuits", level)
    Vs = pick(6, 9, 12)
    R1, R2 = random.choice([(12, 6), (24, 12), (30, 20), (18, 9), (40, 10)])
    I1, I2 = Vs / R1, Vs / R2
    ex.num(f"Calculate the current in the {R1} Ω lamp.", I1, "A",
           wrong=[(Vs / 2 / R1, "In parallel each branch has the FULL supply voltage.")],
           working=[rf"I_1 = \frac{{V}}{{R_1}} = \frac{{{Vs}}}{{{R1}}} = {ltx(I1)}\ \text{{A}}"])
    ex.num("Calculate the current from the supply.", I1 + I2, "A",
           wrong=[(I1, "Add the branch currents."), (Vs / (R1 + R2), "The lamps are in parallel, not series.")],
           working=[rf"I_2 = \frac{{{Vs}}}{{{R2}}} = {ltx(I2)}\ \text{{A}}", rf"I_s = I_1 + I_2 = {ltx(I1 + I2)}\ \text{{A}}"],
           scaffold=[(f"Current in the {R2} Ω lamp, in A?", I2, "A")])
    ex.choice("One lamp breaks. What happens to the other lamp?",
              "It stays lit at the same brightness — it still has the full supply voltage across it.",
              [("It goes out.", "In PARALLEL, each lamp has its own path."), ("It gets brighter.", "Its voltage (and so current) doesn't change."),
               ("It gets dimmer.", "It still has the full supply voltage.")])
    return ex.build(f"Two lamps, of resistance {R1} Ω and {R2} Ω, are connected in parallel with a {Vs} V supply.")


gen_circuits_exam = exam_style(_circ_series, _circ_parallel)


# ════════════════ Charge Carriers ════════════════

def _cc_vdg(level="N5"):
    ex = _ex("Charge Carriers", level)
    I_uA, t_ms = pick(20, 40, 50, 80), pick(15, 25, 40, 50)
    I, t = I_uA * 1e-6, t_ms / 1000
    Q = I * t
    ex.num(f"A spark from the dome lasts {t_ms} ms with an average current of {I_uA} μA. Calculate the charge transferred.", Q, "C",
           wrong=[(I_uA * t_ms, "Convert μA to A (× 10⁻⁶) and ms to s (÷ 1000)."), (I * t_ms, "Convert ms to s."),
                  (I_uA * 1e-3 * t, "μ means × 10⁻⁶, not × 10⁻³.")],
           working=[r"Q = It", rf"Q = ({I_uA} \times 10^{{-6}}) \times ({t_ms} \times 10^{{-3}})", rf"Q = {ltx(Q)}\ \text{{C}}"])
    N = Q / E_CHARGE
    ex.num("Calculate the number of electrons transferred.", N, "",
           wrong=[(Q * E_CHARGE, "Divide the total charge by the charge on one electron.")],
           working=[rf"N = \frac{{Q}}{{e}} = \frac{{{ltx(Q)}}}{{1.6 \times 10^{{-19}}}} = {ltx(N)}"])
    ex.choice("A small negatively charged sphere is placed in the electric field between the dome and an earthed plate. What happens?",
              "It experiences a force and moves.",
              [("Nothing — electric fields only affect magnets.", "Charged particles in an electric field experience a force."),
               ("It loses its charge immediately.", "It experiences a force in the field."),
               ("It moves at constant speed with no force on it.", "There is a force on it, so it accelerates.")])
    return ex.build("A Van de Graaff generator builds up charge on its dome. Charge on an electron = 1.6 × 10⁻¹⁹ C.")


def _cc_supply(level="N5"):
    ex = _ex("Charge Carriers", level)
    I, mins = pick(0.2, 0.3, 0.5, 1.5), pick(2, 5, 10)
    Q = I * mins * 60
    ex.num(f"The current in a d.c. circuit is {I:g} A for {mins} minutes. Calculate the charge that flows.", Q, "C",
           wrong=[(I * mins, "Convert minutes to seconds."), (I / (mins * 60), "Q = I × t.")],
           working=[rf"Q = It = {I:g} \times ({mins} \times 60) = {ltx(Q)}\ \text{{C}}"])
    ex.num("Calculate how many electrons pass a point in the circuit in this time.", Q / E_CHARGE, "",
           wrong=[(Q * E_CHARGE, "Divide by the charge on one electron.")],
           working=[rf"N = \frac{{{ltx(Q)}}}{{1.6 \times 10^{{-19}}}} = {ltx(Q / E_CHARGE)}"])
    ex.choice("What is the difference between d.c. and a.c.?",
              "In d.c. charges flow in one direction only; in a.c. the direction of flow changes regularly.",
              [("d.c. is always a larger current than a.c.", "The difference is the direction of flow."),
               ("In a.c. charges flow in one direction only; in d.c. the direction changes.", "The other way round."),
               ("a.c. only flows in parallel circuits.", "a.c./d.c. describe the direction of flow, not the circuit.")])
    return ex.build("A pupil investigates the flow of charge in circuits. Charge on an electron = 1.6 × 10⁻¹⁹ C.")


gen_charge_carriers_exam = exam_style(_cc_vdg, _cc_supply)


# ════════════════ Potential Difference ════════════════

def _pdiff_battery(level="N5"):
    ex = _ex("Potential Difference", level)
    V, I, hrs = pick(1.5, 3.7, 6, 9, 12), pick(0.05, 0.1, 0.2, 0.5), pick(2, 4, 5, 10)
    Q = I * hrs * 3600
    E = Q * V
    ex.num(f"The battery supplies {I:g} A for {hrs} hours. Calculate the charge that flows.", Q, "C",
           wrong=[(I * hrs, "Convert hours to seconds (× 3600).")],
           working=[rf"Q = It = {I:g} \times ({hrs} \times 3600) = {ltx(Q)}\ \text{{C}}"])
    ex.num("Calculate the energy transferred by the battery.", E, "J",
           wrong=[(Q / V, "E_w = Q × V."), (I * hrs * V, "Use the charge in coulombs.")],
           working=[r"E_w = QV", rf"E_w = {ltx(Q)} \times {V:g} = {ltx(E)}\ \text{{J}}"])
    ex.choice(f"What does a potential difference of {V:g} V mean?", f"{V:g} J of energy is transferred for each coulomb of charge.",
              [(f"{V:g} C of charge flows each second.", "That's a current of " + f"{V:g} A."),
               (f"{V:g} J of energy is transferred each second.", "That's a power of " + f"{V:g} W."),
               (f"The battery has {V:g} Ω of resistance.", "Voltage is energy per unit charge.")])
    return ex.build(f"A {V:g} V battery powers a device.")


def _pdiff_graph(level="N5"):
    ex = _ex("Potential Difference", level)
    R = pick(5, 8, 12, 20, 30)
    Imax = pick(0.3, 0.5, 0.6, 0.8)
    pts = [(round(Imax * k / 4, 3), round(R * Imax * k / 4, 3)) for k in range(5)]
    fig = graph(pts, xlabel="Current (A)", ylabel="Potential difference (V)")
    I1, V1 = pts[4]
    ex.num("Use the gradient of the graph to find the resistance of the component.", R, "Ω",
           wrong=[(I1 / V1, "Gradient = ΔV ÷ ΔI (rise over run)."), (V1 * I1, "Gradient = ΔV ÷ ΔI.")],
           working=[rf"R = \text{{gradient}} = \frac{{\Delta V}}{{\Delta I}} = \frac{{{V1:g} - 0}}{{{I1:g} - 0}} = {R}\ \Omega"])
    Q = pick(30, 45, 60, 120)
    E = Q * V1
    ex.num(f"When the current is {I1:g} A, {Q} C of charge passes through the component. Calculate the energy transferred.", E, "J",
           wrong=[(Q / V1, "E_w = Q × V."), (Q * I1, f"Use the potential difference ({V1:g} V), not the current.")],
           working=[T(f"At I = {I1:g} A the graph gives V = {V1:g} V."), r"E_w = QV", rf"E_w = {Q} \times {V1:g} = {ltx(E)}\ \text{{J}}"])
    return ex.build("The graph shows how the potential difference across a component varies with the current in it.", figure=fig)


gen_potential_difference_exam = exam_style(_pdiff_battery, _pdiff_graph)


# ════════════════ Circuit Rules ════════════════

def _rules_mixed(level="N5"):
    ex = _ex("Circuit Rules", level)
    n = pick(3, 4, 5)
    Ieach = pick(0.15, 0.2, 0.25, 0.4)
    Vs = pick(6, 12)
    ex.num(f"Each lamp draws {Ieach:g} A. Calculate the current from the supply.", n * Ieach, "A",
           wrong=[(Ieach, "In parallel the branch currents ADD."), (Ieach / n, "Add the branch currents.")],
           working=[rf"I_s = {n} \times {Ieach:g} = {ltx(n * Ieach)}\ \text{{A}}"])
    ex.num("State the voltage across each lamp.", Vs, "V",
           wrong=[(Vs / n, "In PARALLEL each lamp has the full supply voltage.")],
           working=[T(f"Parallel: V across each branch = supply voltage = {Vs} V.")])
    R = Vs / Ieach
    ex.num("Calculate the resistance of one lamp.", R, "Ω",
           wrong=[(Vs / (n * Ieach), "Use the current in ONE lamp."), (Vs / n / Ieach, "Each lamp has the full supply voltage.")],
           working=[rf"R = \frac{{V}}{{I}} = \frac{{{Vs}}}{{{Ieach:g}}} = {ltx(R)}\ \Omega"])
    return ex.build(f"{n} identical lamps are connected in parallel to a {Vs} V supply.")


def _rules_series(level="N5"):
    ex = _ex("Circuit Rules", level)
    Vs = pick(6, 9, 12)
    V1 = sig(Vs * random.uniform(0.25, 0.45), 2)
    V2 = sig(Vs * random.uniform(0.2, 0.35), 2)
    V3 = Vs - V1 - V2
    I = pick(0.1, 0.2, 0.3)
    ex.num(f"The voltages across lamps A and B are {V1:g} V and {V2:g} V. Calculate the voltage across lamp C.", V3, "V",
           wrong=[(Vs, "In series the supply voltage is shared."), (Vs / 3, "The lamps are not identical — subtract the others.")],
           working=[rf"V_C = V_s - V_A - V_B = {Vs} - {V1:g} - {V2:g} = {ltx(V3)}\ \text{{V}}"])
    ex.num(f"The current in lamp A is {I:g} A. State the current in lamp C.", I, "A",
           wrong=[(3 * I, "In SERIES the current is the same everywhere."), (I / 3, "The current is the same everywhere in series.")],
           working=[T(f"Series: the current is the same at all points = {I:g} A.")])
    ex.choice("A fourth lamp is added in series. What happens to the brightness of lamps A, B and C?",
              "They get dimmer — the total resistance increases, so the current decreases.",
              [("They stay the same brightness.", "The supply voltage is now shared between four lamps."),
               ("They get brighter.", "More resistance means less current."),
               ("They go out.", "Current still flows — just less.")])
    return ex.build(f"Three different lamps A, B and C are connected in series with a {Vs} V supply.")


gen_circuit_rules_exam = exam_style(_rules_mixed, _rules_series)


# ════════════════ LEDs and Transistor Switches ════════════════

def _led_resistor(level="N5"):
    ex = _ex("LEDs and Transistor Switches", level)
    Vs, VL, I_mA = pick(5, 6, 9, 12), pick(1.8, 2.0, 2.2, 3.0), pick(10, 15, 20, 25)
    I = I_mA / 1000
    VR = Vs - VL
    R = VR / I
    ex.num("Calculate the voltage across the resistor.", VR, "V",
           wrong=[(Vs, "The LED takes some of the supply voltage."), (VL, "V_R = V_s − V_LED.")],
           working=[rf"V_R = {Vs} - {VL:g} = {ltx(VR)}\ \text{{V}}"])
    ex.num("Calculate the resistance of the resistor.", R, "Ω",
           wrong=[(VR / I_mA, "Convert mA to A."), (Vs / I, "Use the voltage across the RESISTOR only.")],
           working=[rf"R = \frac{{V_R}}{{I}} = \frac{{{ltx(VR)}}}{{{I:g}}} = {ltx(R)}\ \Omega"],
           scaffold=[("Current in A?", I, "A")])
    ex.choice("Why must a resistor be connected in series with the LED?",
              "To limit the current in (and the voltage across) the LED, so it isn't damaged.",
              [("To make the LED brighter.", "The resistor reduces the current."),
               ("To allow current to flow in both directions.", "An LED only conducts in one direction."),
               ("To increase the voltage across the LED.", "It takes some of the supply voltage, reducing the LED's.")])
    return ex.build(f"An LED is connected in series with a resistor and a {Vs} V supply. The LED operates at {VL:g} V with a current of {I_mA} mA.")


def _led_transistor(level="N5"):
    ex = _ex("LEDs and Transistor Switches", level)
    Vs = pick(5, 6, 9)
    Rf = pick(4700, 10000, 2200)
    Rldr = pick(1000, 1500, 25000, 40000)
    V_ldr = Rldr / (Rf + Rldr) * Vs
    ex.num(f"In a certain light level the LDR has a resistance of {Rldr} Ω. Calculate the voltage across the LDR.", V_ldr, "V",
           wrong=[(Rf / (Rf + Rldr) * Vs, "That's the voltage across the fixed resistor."), (Rldr / Rf * Vs, "Use R_LDR ÷ (R_LDR + R_fixed).")],
           working=[rf"V_{{LDR}} = \frac{{R_{{LDR}}}}{{R_{{LDR}} + R_f}} \times V_s = \frac{{{Rldr}}}{{{Rldr} + {Rf}}} \times {Vs} = {ltx(V_ldr)}\ \text{{V}}"])
    on = V_ldr >= 0.7
    ex.choice("The transistor switches on when the voltage across the LDR reaches 0.7 V. Is the lamp on or off at this light level?",
              "On" if on else "Off",
              [("Off" if on else "On", f"The LDR voltage is {fmt(V_ldr)} V, which is {'above' if on else 'below'} 0.7 V.")])
    ex.choice("Explain how the circuit switches the lamp on as it gets dark.",
              "As it gets darker the LDR's resistance increases, so the voltage across it increases; when it reaches 0.7 V the transistor switches on and the lamp lights.",
              [("As it gets darker the LDR's resistance decreases, so the voltage across it increases and the transistor switches on.",
                "An LDR's resistance INCREASES as the light level decreases."),
               ("The LDR produces a voltage in the dark which lights the lamp directly.", "The LDR controls the potential divider voltage, which switches the transistor."),
               ("The transistor detects the darkness and switches on.", "The LDR senses the light; the transistor is the switch.")])
    return ex.build(f"A transistor circuit switches on a lamp when it gets dark. An LDR and a {Rf} Ω resistor form a potential "
                    f"divider across a {Vs} V supply, with the transistor connected across the LDR.")


gen_leds_transistors_exam = exam_style(_led_resistor, _led_transistor)


# ════════════════ Power and Fuses ════════════════

def _fuse_appliance(level="N5"):
    ex = _ex("Power and Fuses", level)
    P = pick(60, 150, 400, 650, 1200, 1800, 2000, 2400)
    I = P / 230
    ex.num(f"Calculate the current in the appliance when it operates normally.", I, "A",
           wrong=[(P * 230, "I = P ÷ V."), (230 / P, "I = P ÷ V.")],
           working=[r"P = IV \Rightarrow I = \frac{P}{V}", rf"I = \frac{{{P}}}{{230}} = {ltx(I)}\ \text{{A}}"])
    fuse = "3 A" if I < 3 else "13 A"
    other = "13 A" if fuse == "3 A" else "3 A"
    ex.choice("Which fuse should be fitted in the plug?", fuse,
              [(other, "Choose the rating just ABOVE the normal current." if fuse == "3 A" else "A 3 A fuse would blow in normal use."),
               ("1 A", "The fuse must be rated above the normal current."), ("30 A", "Too high — the flex could overheat without the fuse blowing.")])
    ex.choice("What is the purpose of the fuse?",
              "To protect the flex (cable) — it melts and breaks the circuit if the current becomes too large.",
              [("To protect the user from all electric shocks.", "That's the earth wire / RCD; the fuse protects the flex."),
               ("To make the appliance use less energy.", "A fuse doesn't change the power."),
               ("To keep the voltage at 230 V.", "The fuse breaks the circuit if the current is too high.")])
    hrs = pick(0.5, 1.5, 2, 3)
    E = P * hrs * 3600
    ex.num(f"The appliance is used for {hrs:g} hours. Calculate the energy it uses.", E, "J",
           wrong=[(P * hrs, "Convert hours to seconds."), (P * hrs * 60, "1 hour = 3600 s.")],
           working=[rf"E = Pt = {P} \times ({hrs:g} \times 3600) = {ltx(E)}\ \text{{J}}"])
    return ex.build(f"A mains appliance is rated at {P} W, 230 V.")


def _fuse_heater(level="N5"):
    ex = _ex("Power and Fuses", level)
    R, I = pick(20, 24, 30, 40), pick(4, 5, 6, 8)
    P = I ** 2 * R
    ex.num(f"The current in the {R} Ω heating element is {I} A. Calculate the power of the heater.", P, "W",
           wrong=[(I * R, "That's the voltage — P = I²R."), (I * R ** 2, "P = I²R: square the current."), (I ** 2 / R, "P = I² × R.")],
           working=[r"P = I^2R", rf"P = {I}^2 \times {R} = {ltx(P)}\ \text{{W}}"])
    V = I * R
    ex.num("Calculate the voltage across the heating element.", V, "V",
           wrong=[(I / R, "V = I × R.")],
           working=[rf"V = IR = {I} \times {R} = {V}\ \text{{V}}"])
    P2 = V ** 2 / (R / 2)
    ex.num(f"The element is replaced by one of resistance {R // 2} Ω, on the same voltage. Calculate the new power.", P2, "W",
           wrong=[(P / 2, "With a fixed voltage, P = V²/R — halving R DOUBLES P."), (I ** 2 * R / 2, "The current changes too — use P = V²/R.")],
           working=[r"P = \frac{V^2}{R}", rf"P = \frac{{{V}^2}}{{{R // 2}}} = {ltx(P2)}\ \text{{W}}"])
    return ex.build("A heater is used to warm a greenhouse.")


gen_power_fuses_exam = exam_style(_fuse_appliance, _fuse_heater)


EXAM = {
    "Current":                      gen_current_exam,
    "Ohm's Law":                    gen_ohms_law_exam,
    "Resistors":                    gen_resistors_exam,
    "Electrical Power":             gen_electrical_power_exam,
    "Potential Divider":            gen_potential_divider_exam,
    "Circuits":                     gen_circuits_exam,
    "Charge Carriers":              gen_charge_carriers_exam,
    "Potential Difference":         gen_potential_difference_exam,
    "Circuit Rules":                gen_circuit_rules_exam,
    "LEDs and Transistor Switches": gen_leds_transistors_exam,
    "Power and Fuses":              gen_power_fuses_exam,
}
