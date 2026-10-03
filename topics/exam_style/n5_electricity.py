"""N5 Electricity — exam-style questions that cut across the unit's topics, like SQA paper questions.

Recognised wrong answers follow the N5 marking instructions and course reports: mA/minutes/kΩ not
converted, series and parallel rules swapped, 1/R_T left uninverted, the supply voltage used across
one component, the wrong form of the power relationship, and a fuse rated below the working current.
"""
import math
import random

from topics.exam_style.base import Exam, T, fmt, graph, ltx, pick, sig

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


def _ex(level):
    return Exam(UNIT, level, NOTES)


def _par(*rs):
    return 1 / sum(1 / r for r in rs)


# ════════════════ Kitchen appliance: current → fuse → resistance → energy → charge ════════════════

def kitchen_appliance(level="N5"):
    ex = _ex(level)
    name, P = random.choice([("toaster", 1100), ("kettle", 2200), ("microwave", 800), ("food mixer", 400), ("iron", 1800)])
    I = P / 230
    ex.on("Electrical Power").num("Calculate the current in the appliance when it is operating.", I, "A",
        wrong=[(P * 230, "I = P ÷ V."), (230 / P, "I = P ÷ V.")],
        working=[r"P = IV \Rightarrow I = \frac{P}{V}", rf"I = \frac{{{P}}}{{230}} = {ltx(I)}\ \text{{A}}"])
    fuse = "3 A" if I < 3 else "13 A"
    ex.on("Power and Fuses").choice("Which fuse should be fitted in the plug?", fuse,
        [("13 A" if fuse == "3 A" else "3 A", "Choose the rating just ABOVE the normal current."),
         ("30 A", "Too high — the flex could overheat without the fuse melting."), ("1 A", "That would melt in normal use.")])
    R = 230 / sig(I)
    ex.on("Ohm's Law").num("Calculate the resistance of the appliance when it is operating.", R, "Ω",
        wrong=[(sig(I) / 230, "R = V ÷ I."), (230 * sig(I), "R = V ÷ I.")],
        working=[rf"R = \frac{{V}}{{I}} = \frac{{230}}{{{ltx(I)}}} = {ltx(R)}\ \Omega"])
    mins = pick(2, 3, 4, 5)
    E = P * mins * 60
    ex.on("Electrical Power").num(f"The {name} is used for {mins} minutes. Calculate the energy it uses.", E, "J",
        wrong=[(P * mins, "Convert minutes to seconds."), (P / (mins * 60), "E = P × t.")],
        working=[rf"E = Pt = {P} \times ({mins} \times 60) = {ltx(E)}\ \text{{J}}"])
    Q = sig(I) * mins * 60
    ex.on("Current").num("Calculate the charge that flows through the appliance in this time.", Q, "C",
        wrong=[(sig(I) * mins, "Convert minutes to seconds."), (sig(I) / (mins * 60), "Q = I × t.")],
        working=[rf"Q = It = {ltx(I)} \times {mins * 60} = {ltx(Q)}\ \text{{C}}"])
    ex.on("Power and Fuses").choice("What is the purpose of the fuse?",
        "To protect the flex — it melts and breaks the circuit if the current becomes too large.",
        [("To protect the user from every electric shock.", "The fuse protects the flex (cable)."),
         ("To reduce the power of the appliance.", "A fuse doesn't change the power."),
         ("To keep the voltage at 230 V.", "It breaks the circuit when the current is too high.")])
    return ex.build(f"A {name} is rated at {P} W and is connected to the 230 V mains.")


# ════════════════ Charging a phone: Q = It → electrons → Ew = QV → P = IV ════════════════

def phone_charger(level="N5"):
    ex = _ex(level)
    I_mA, hrs, V = pick(500, 750, 1000, 1500), pick(1.5, 2, 2.5), 5.0
    I = I_mA / 1000
    Q = I * hrs * 3600
    ex.on("Current").num(f"The charger supplies {I_mA} mA for {hrs:g} hours. Calculate the charge that flows.", Q, "C",
        wrong=[(I_mA * hrs * 3600, "Convert mA to A."), (I * hrs, "Convert hours to seconds."), (I_mA * hrs, "Convert to A and s.")],
        working=[rf"Q = It = {I:g} \times ({hrs:g} \times 3600) = {ltx(Q)}\ \text{{C}}"],
        scaffold=[("Current in A?", I, "A"), ("Time in s?", hrs * 3600, "s")])
    N = sig(Q) / 1.6e-19
    ex.on("Charge Carriers").num("Calculate the number of electrons that flow (charge on an electron = 1.6 × 10⁻¹⁹ C).", N, "",
        wrong=[(sig(Q) * 1.6e-19, "Divide by the charge on one electron.")],
        working=[rf"N = \frac{{Q}}{{e}} = \frac{{{ltx(Q)}}}{{1.6\times10^{{-19}}}} = {ltx(N)}"])
    E = sig(Q) * V
    ex.on("Potential Difference").num(f"The charger's output is {V:g} V. Calculate the energy transferred to the phone.", E, "J",
        wrong=[(sig(Q) / V, "Ew = Q × V."), (I * V, "That's the power — Ew = QV.")],
        working=[rf"E_w = QV = {ltx(Q)} \times {V:g} = {ltx(E)}\ \text{{J}}"])
    ex.on("Electrical Power").num("Calculate the power output of the charger.", I * V, "W",
        wrong=[(I_mA * V, "Convert mA to A."), (V / I, "That's the resistance; P = IV.")],
        working=[rf"P = IV = {I:g} \times {V:g} = {ltx(I * V)}\ \text{{W}}"])
    ex.on("Charge Carriers").choice("The charger changes the a.c. mains into d.c. What is the difference between a.c. and d.c.?",
        "In d.c. charges flow in one direction only; in a.c. the direction of flow changes regularly.",
        [("a.c. is always a bigger current than d.c.", "The difference is the direction of flow."),
         ("In a.c. charges flow one way; in d.c. the direction changes.", "The other way round."),
         ("d.c. can only be produced by batteries.", "It's about the direction of flow.")])
    return ex.build("A mobile phone is charged from a USB charger.")


# ════════════════ Night light: LDR divider → transistor → LED resistor ════════════════

def night_light(level="N5"):
    ex = _ex(level)
    Vs, Rf = pick(5, 6, 9), pick(2200, 4700, 10000)
    Rldr = pick(1000, 1500, 25000, 40000)
    V_ldr = Rldr / (Rf + Rldr) * Vs
    ex.on("Potential Divider").num(f"In the current light level the LDR's resistance is {Rldr} Ω. Calculate the voltage across the LDR.", V_ldr, "V",
        wrong=[(Rf / (Rf + Rldr) * Vs, "That's the voltage across the fixed resistor."), (Rldr / Rf * Vs, "Use R_LDR ÷ (R_LDR + R_fixed).")],
        working=[rf"V_{{LDR}} = \frac{{R_{{LDR}}}}{{R_{{LDR}} + R_f}} \times V_s = \frac{{{Rldr}}}{{{Rldr} + {Rf}}} \times {Vs} = {ltx(V_ldr)}\ \text{{V}}"])
    on = V_ldr >= 0.7
    ex.on("LEDs and Transistor Switches").choice("The transistor switches on when the voltage across the LDR reaches 0.7 V. Is the LED on or off?",
        "On" if on else "Off", [("Off" if on else "On", f"The LDR voltage is {fmt(V_ldr)} V — {'above' if on else 'below'} 0.7 V.")])
    ex.on("LEDs and Transistor Switches").choice("Explain how the circuit switches the LED on as it gets dark.",
        "As it gets darker the LDR's resistance increases, so the voltage across it increases; at 0.7 V the transistor switches on.",
        [("As it gets darker the LDR's resistance decreases, so the transistor switches on.", "An LDR's resistance INCREASES in the dark."),
         ("The LDR produces a voltage in the dark that lights the LED.", "The LDR controls the divider voltage."),
         ("The transistor senses the darkness.", "The LDR senses light; the transistor is the switch.")])
    VL, I_mA = pick(1.8, 2.0, 2.2), pick(10, 15, 20)
    VR = Vs - VL
    ex.on("LEDs and Transistor Switches").num(f"The LED operates at {VL:g} V and {I_mA} mA from the {Vs} V supply. Calculate the resistance of its series resistor.",
        VR / (I_mA / 1000), "Ω",
        wrong=[(Vs / (I_mA / 1000), "Use the voltage across the RESISTOR: V_s − V_LED."), (VR / I_mA, "Convert mA to A.")],
        working=[rf"V_R = {Vs} - {VL:g} = {ltx(VR)}\ \text{{V}}", rf"R = \frac{{V_R}}{{I}} = \frac{{{ltx(VR)}}}{{{I_mA / 1000:g}}} = {ltx(VR / (I_mA / 1000))}\ \Omega"],
        scaffold=[("Voltage across the resistor, in V?", VR, "V")])
    return ex.build(f"A night light uses an LDR and a {Rf} Ω resistor as a potential divider across a {Vs} V supply. A transistor "
                    f"connected across the LDR switches on an LED.")


# ════════════════ Car lights: parallel circuit → resistance → power ════════════════

def car_lights(level="N5"):
    ex = _ex(level)
    Vs = 12
    P1, P2 = random.choice([(48, 24), (60, 36), (55, 21), (48, 12)])
    I1, I2 = P1 / Vs, P2 / Vs
    ex.on("Electrical Power").num(f"Calculate the current in the {P1} W headlamp.", I1, "A",
        wrong=[(P1 * Vs, "I = P ÷ V."), (Vs / P1, "I = P ÷ V.")],
        working=[rf"I = \frac{{P}}{{V}} = \frac{{{P1}}}{{12}} = {ltx(I1)}\ \text{{A}}"])
    ex.on("Circuit Rules").num(f"The {P2} W lamp is connected in parallel with the headlamp. Calculate the current from the battery.", I1 + I2, "A",
        wrong=[(I1, "In parallel, the branch currents ADD."), ((P1 + P2) / (2 * Vs), "Each lamp has the full 12 V.")],
        working=[rf"I_2 = \frac{{{P2}}}{{12}} = {ltx(I2)}\ \text{{A}}", rf"I_s = {ltx(I1)} + {ltx(I2)} = {ltx(I1 + I2)}\ \text{{A}}"])
    R1, R2 = Vs / I1, Vs / I2
    ex.on("Ohm's Law").num("Calculate the resistance of the headlamp.", R1, "Ω",
        wrong=[(I1 / Vs, "R = V ÷ I.")], working=[rf"R = \frac{{V}}{{I}} = \frac{{12}}{{{ltx(I1)}}} = {ltx(R1)}\ \Omega"])
    Rt = _par(R1, R2)
    ex.on("Resistors").num("Calculate the total resistance of the two lamps in parallel.", Rt, "Ω",
        wrong=[(R1 + R2, "In parallel: 1/R_T = 1/R₁ + 1/R₂."), (1 / R1 + 1 / R2, "Invert at the end.")],
        working=[rf"\frac{{1}}{{R_T}} = \frac{{1}}{{{ltx(R1)}}} + \frac{{1}}{{{ltx(R2)}}}", rf"R_T = {ltx(Rt)}\ \Omega"])
    ex.on("Circuits").choice("The smaller lamp fails. What happens to the headlamp?",
        "It stays lit at the same brightness — it still has the full 12 V across it.",
        [("It goes out.", "In parallel each lamp has its own path."), ("It gets brighter.", "Its voltage is unchanged."),
         ("It gets dimmer.", "Its voltage is unchanged.")])
    return ex.build(f"A car's {P1} W headlamp and a {P2} W lamp are connected in parallel to the 12 V battery.")


# ════════════════ Thermostat: thermistor divider → current → heater power ════════════════

def thermostat(level="N5"):
    ex = _ex(level)
    Rf, Rt, Vs = pick(1000, 2200, 4700), pick(1500, 2000, 3000, 5600), pick(6, 9, 12)
    Vout = Rf / (Rf + Rt) * Vs
    ex.on("Resistors").num(f"At 20 °C the thermistor's resistance is {Rt} Ω. Calculate the total resistance of the divider.", Rf + Rt, "Ω",
        wrong=[(_par(Rf, Rt), "They are in SERIES — add them.")], working=[rf"R_T = {Rf} + {Rt} = {Rf + Rt}\ \Omega"])
    I = Vs / (Rf + Rt)
    ex.on("Ohm's Law").num("Calculate the current in the divider.", I, "A",
        wrong=[(Vs / Rf, "Use the TOTAL resistance."), ((Rf + Rt) / Vs, "I = V ÷ R.")],
        working=[rf"I = \frac{{{Vs}}}{{{Rf + Rt}}} = {ltx(I)}\ \text{{A}}"])
    ex.on("Potential Divider").num("Calculate the voltage across the fixed resistor.", Vout, "V",
        wrong=[(Rt / (Rf + Rt) * Vs, "That's across the thermistor."), (Vs / 2, "The voltage divides in the ratio of the resistances.")],
        working=[rf"V = \frac{{{Rf}}}{{{Rf} + {Rt}}} \times {Vs} = {ltx(Vout)}\ \text{{V}}"])
    ex.on("Potential Divider").choice("The temperature rises. What happens to the voltage across the fixed resistor?",
        "It increases — the thermistor's resistance decreases, so the fixed resistor gets a bigger share of the voltage.",
        [("It decreases — the thermistor's resistance increases.", "A thermistor's resistance DECREASES as temperature rises."),
         ("It stays the same.", "Its share depends on the thermistor's resistance."),
         ("It decreases — the current decreases.", "The current increases.")])
    R, Ih = pick(20, 24, 30), pick(4, 5, 6)
    P = Ih ** 2 * R
    ex.on("Power and Fuses").num(f"The heater switched by the thermostat has a {R} Ω element with a current of {Ih} A. Calculate its power.", P, "W",
        wrong=[(Ih * R, "That's the voltage. P = I²R."), (Ih * R ** 2, "Square the current, not R.")],
        working=[rf"P = I^2R = {Ih}^2 \times {R} = {ltx(P)}\ \text{{W}}"])
    return ex.build(f"A thermostat uses a thermistor in series with a {Rf} Ω resistor across a {Vs} V supply.")


# ════════════════ Investigating a series circuit ════════════════

def series_investigation(level="N5"):
    ex = _ex(level)
    R1, R2 = random.sample([10, 15, 20, 22, 33, 47], 2)
    Vs = pick(6, 9, 12)
    RT = R1 + R2
    I = Vs / RT
    ex.on("Resistors").num("Calculate the total resistance of the circuit.", RT, "Ω",
        wrong=[(_par(R1, R2), "In SERIES, just add the resistances.")], working=[rf"R_T = {R1} + {R2} = {RT}\ \Omega"])
    ex.on("Ohm's Law").num("Calculate the current in the circuit.", I, "A",
        wrong=[(Vs / R1, "Use the total resistance."), (RT / Vs, "I = V ÷ R.")],
        working=[rf"I = \frac{{V}}{{R_T}} = \frac{{{Vs}}}{{{RT}}} = {ltx(I)}\ \text{{A}}"])
    V2 = sig(I) * R2
    ex.on("Circuit Rules").num(f"Calculate the voltage across the {R2} Ω resistor.", V2, "V",
        wrong=[(Vs, "In series the supply voltage is shared."), (Vs / 2, "It divides in the ratio of the resistances.")],
        working=[rf"V = IR = {ltx(I)} \times {R2} = {ltx(V2)}\ \text{{V}}"])
    ex.on("Circuits").choice("How should a voltmeter be connected to measure this voltage?", f"In parallel with the {R2} Ω resistor.",
        [(f"In series with the {R2} Ω resistor.", "Ammeters go in series; voltmeters in parallel."),
         ("In series with the battery.", "Connect it across the component."),
         ("Anywhere — voltage is the same everywhere in series.", "In series the voltage is shared.")])
    ex.on("Potential Difference").choice(f"What does a supply voltage of {Vs} V mean?", f"{Vs} J of energy is given to each coulomb of charge.",
        [(f"{Vs} C of charge flows each second.", "That would be a current."), (f"{Vs} J of energy is transferred each second.", "That would be a power."),
         (f"The battery has {Vs} Ω of resistance.", "Voltage is energy per unit charge.")])
    return ex.build(f"A pupil connects a {R1} Ω resistor and a {R2} Ω resistor in series with a {Vs} V battery.")


SCENARIOS = {
    "Kitchen Appliance":     kitchen_appliance,
    "Charging a Phone":      phone_charger,
    "Night Light":           night_light,
    "Car Lights":            car_lights,
    "Thermostat":            thermostat,
    "Series Circuit Investigation": series_investigation,
}
