"""Higher Electricity — exam-style questions that cut across the unit's topics, like SQA paper questions.

Recognised wrong answers follow the Higher marking instructions and course reports: peak-to-peak read
as the peak, √2 used the wrong way, T left in ms, the current from P = IV taken as the peak, the
internal resistance found as E ÷ I, the gradient of a V–I graph taken as +r, lost volts confused with
the t.p.d., µF not converted, ½ dropped from E = ½CV², the voltmeter across the resistor read as the
capacitor's p.d., parallel resistors given a share of the p.d., and LED/solar-cell explanations that
use the wrong device or no band theory.
"""
import math

from topics.exam_style.base import Exam, fmt, ltx, pick, sig

UNIT = "Electricity"
AC = "Monitoring and Measuring AC"
CIRC = "Current, Potential Difference, Power and Resistance"
IR = "Electrical Sources and Internal Resistance"
CAP = "Capacitors"
SEMI = "Semiconductors and p-n Junctions"
H = 6.63e-34
C = 3.00e8
R2 = math.sqrt(2)


def _notes(title, body):
    return f"## {title} — exam technique\n\n{body}"


NOTES = {
    AC: _notes("Monitoring and measuring AC", r"""
$V_{peak} = \sqrt2 V_{rms}$ &nbsp; $I_{peak} = \sqrt2 I_{rms}$ &nbsp; $T = \frac1f$

- AC: a current that changes **direction and instantaneous value** with time.
- Peak = crest to **centre line** × Y-gain. Period = one whole wave × timebase, in **seconds**.
- In a "show that", show where the period came from (course report 2025).
"""),
    CIRC: _notes("Current, p.d., power and resistance", r"""
$V = IR$ &nbsp; $P = IV = I^2R = \frac{V^2}{R}$ &nbsp; $\frac1{R_T} = \frac1{R_1} + \frac1{R_2}$ &nbsp; $V_1 = \left(\frac{R_1}{R_1+R_2}\right)V_S$

- Invert $1/R_T$. Parallel branches each have the **full** p.d.
- Closing a switch that adds a parallel branch lowers the **total** resistance.
"""),
    IR: _notes("Electrical sources and internal resistance", r"""
$E = V + Ir$ &nbsp; $V = IR$ — lost volts $= Ir$, t.p.d. $= IR$.

- e.m.f. = energy supplied to **each coulomb** of charge.
- V–I graph: intercept $= E$, gradient $= -r$. Short circuit: $I = E/r$.
- R ↑ → I ↓ → lost volts ↓ → t.p.d. ↑.
"""),
    CAP: _notes("Capacitors", r"""
$C = \frac QV$ &nbsp; $Q = It$ &nbsp; $E = \tfrac12QV = \tfrac12CV^2 = \tfrac12\frac{Q^2}{C}$

- µF = 10⁻⁶ F. The supply p.d. is shared: $V_S = V_R + V_C$.
- Larger R → smaller initial current, longer to charge, same energy. Larger C → same initial current, longer.
"""),
    SEMI: _notes("Semiconductors and p-n junctions", r"""
$E = hf$ &nbsp; $v = f\lambda$

- Use **band theory** and name the **valence** and **conduction** bands.
- LED: electrons move from n-type conduction band towards p-type, fall to the valence band, photons emitted.
- Solar cell / photodiode: photons absorbed, electrons raised valence → conduction band, move towards the n-type — the **photovoltaic** effect.
"""),
}


def _ex(level):
    return Exam(UNIT, level, NOTES)


# ════════════════ Lighthouse supply: oscilloscope → r.m.s. → peak current → LEDs on a.c. ════════════════

def lighthouse(level="Higher"):
    ex = _ex(level)
    div, gain = pick(2.0, 2.5, 3.0), pick(2.0, 4.0, 5.0)
    pk = div * gain
    rms = pk / R2
    ex.on(AC).num(f"On an oscilloscope, the crests of the supply trace are {div:g} divisions above the centre line with the Y-gain at {gain:g} V/div. "
                  f"Calculate the r.m.s. voltage of the supply.", rms, "V",
                  wrong=[(2 * pk / R2, "Measure from the centre line — crest to trough is peak-to-peak."), (pk * R2, "Divide by √2 for the r.m.s. value."),
                         (pk, "That's the peak voltage.")],
                  working=[rf"V_{{peak}} = {div:g} \times {gain:g} = {ltx(pk)}\ \text{{V}}", rf"V_{{rms}} = \frac{{{ltx(pk)}}}{{\sqrt2}} = {ltx(rms)}\ \text{{V}}"],
                  scaffold=[("Peak voltage (V)", pk, "V")])
    n, tb = pick(4, 5), pick(2.0, 5.0)
    T = n * tb * 1e-3
    ex.on(AC).num(f"One complete wave occupies {n} divisions with the timebase at {tb:g} ms/div. Calculate the frequency.", 1 / T, "Hz",
                  wrong=[(1 / (n * tb), "Convert ms to s."), (1 / (2 * T), "One whole wave is one period.")],
                  working=[rf"T = {n} \times {tb:g}\times10^{{-3}} = {ltx(T)}\ \text{{s}}", rf"f = \frac1T = {ltx(1 / T)}\ \text{{Hz}}"])
    P = pick(6.0, 12.0, 18.0)
    vr = sig(rms)
    irms = P / vr
    ex.on(AC).num(f"A lamp of power {P:g} W operates from this supply. Calculate the peak current in the lamp.", irms * R2, "A",
                  wrong=[(irms, "P = IV with the r.m.s. voltage gives the r.m.s. current — multiply by √2."), (irms / R2, "The peak is larger: × √2.")],
                  working=[rf"I_{{rms}} = \frac PV = \frac{{{P:g}}}{{{ltx(vr)}}} = {ltx(irms)}\ \text{{A}}", rf"I_{{peak}} = \sqrt2 \times {ltx(irms)} = {ltx(irms * R2)}\ \text{{A}}"],
                  scaffold=[("r.m.s. current (A)", irms, "A")])
    ex.on(SEMI).choice("Red and green LEDs are connected in parallel, facing opposite ways, across this supply. Why do they light alternately?",
                       "Each conducts only when forward biased, and each is forward biased in a different half-cycle.",
                       [("One lights when forward biased, the other when reverse biased.", "An LED never conducts in reverse bias (course report 2023)."),
                        ("The supply switches off between half-cycles.", "It reverses direction."),
                        ("The green LED needs more current.", "It's about bias, not current.")])
    return ex.build("The warning lamps on a model lighthouse are run from a low-voltage a.c. supply, which a student examines with an oscilloscope.")


# ════════════════ Car battery: e.m.f. and internal resistance → headlamps → power in r ════════════════

def car_battery(level="Higher"):
    ex = _ex(level)
    E, r = pick(12.0, 12.6, 12.8), pick(0.05, 0.10, 0.20)
    R = pick(4.0, 4.8, 6.0)
    ex.on(IR).choice(f"State what is meant by an e.m.f. of {E:g} V.", f"{E:g} J of energy is supplied to each coulomb of charge passing through the battery.",
                     [(f"The p.d. across the terminals is always {E:g} V.", "Only on open circuit."), (f"The battery stores {E:g} J.", "Energy per coulomb."),
                      (f"{E:g} V is lost inside the battery.", "That would be lost volts.")])
    I1 = E / (R + r)
    ex.on(IR).num(f"One {R:g} Ω headlamp is switched on. Calculate the current.", I1, "A",
                  wrong=[(E / R, "Include the internal resistance: E = V + Ir.")],
                  working=[r"E = V + Ir", rf"{E:g} = I \times {R:g} + I \times {r:g}", rf"I = {ltx(I1)}\ \text{{A}}"])
    ex.on(IR).num("Calculate the reading on a voltmeter connected across the battery terminals.", I1 * R, "V",
                  wrong=[(E, "The t.p.d. is less than the e.m.f. when there is a current."), (I1 * r, "That's the lost volts.")],
                  working=[rf"V = IR = {ltx(I1)} \times {R:g} = {ltx(I1 * R)}\ \text{{V}}"])
    Rp = R / 2
    I2 = E / (Rp + r)
    ex.on(CIRC).num(f"A second identical headlamp is switched on in parallel. Calculate the total external resistance.", Rp, "Ω",
                    wrong=[(2 * R, "The lamps are in PARALLEL."), (2 / R, "Invert 1/R_T.")],
                    working=[rf"\frac1{{R_T}} = \frac1{{{R:g}}} + \frac1{{{R:g}}},\ R_T = {ltx(Rp)}\ \Omega"])
    ex.on(IR).num("Calculate the power now dissipated in the internal resistance.", I2 ** 2 * r, "W",
                  wrong=[(I1 ** 2 * r, "Recalculate the current with the new external resistance."), (I2 * r, "P = I²r — square the current.")],
                  working=[rf"I = \frac{{{E:g}}}{{{ltx(Rp)} + {r:g}}} = {ltx(I2)}\ \text{{A}}", rf"P = I^2r = {ltx(I2 ** 2 * r)}\ \text{{W}}"],
                  scaffold=[("New current (A)", I2, "A")])
    ex.on(IR).choice("Why are the headlamps slightly dimmer when the second one is switched on?",
                     "The current increases, so the lost volts increase and the t.p.d. decreases.",
                     [("Because of lost volts.", "Explain the chain: R_T ↓ → I ↑ → Ir ↑ → t.p.d. ↓ (course report 2019)."),
                      ("The e.m.f. of the battery falls.", "The e.m.f. is constant."),
                      ("The current is shared between the lamps.", "Each lamp gets the t.p.d.; it's the t.p.d. that falls.")])
    return ex.build(f"A car battery has an e.m.f. of {E:g} V and internal resistance {r:g} Ω. Each headlamp has a resistance of {R:g} Ω.")


# ════════════════ Potato battery: V–I graph → E, r, short circuit → LED band theory ════════════════

def potato_battery(level="Higher"):
    ex = _ex(level)
    E_mv, r_k = pick(800, 900, 950), pick(2.0, 3.0, 4.0)
    I_ua = pick(100, 150, 200)
    V_mv = E_mv - r_k * I_ua
    ex.on(IR).num(f"The t.p.d.–current graph meets the voltage axis at {E_mv} mV and passes through ({I_ua} µA, {V_mv:g} mV). Calculate the internal resistance.",
                  r_k * 1000, "Ω",
                  wrong=[(r_k, "Account for the prefixes on the axes: mV and µA (course report 2018)."), (E_mv * 1e-3 / (I_ua * 1e-6), "E ÷ I is the total resistance.")],
                  working=[r"E = V + Ir", rf"{E_mv}\times10^{{-3}} = {V_mv:g}\times10^{{-3}} + {I_ua}\times10^{{-6}} \times r", rf"r = {ltx(r_k * 1000)}\ \Omega"])
    isc = E_mv * 1e-3 / (r_k * 1000)
    ex.on(IR).num("Calculate the short-circuit current.", isc, "A",
                  wrong=[(I_ua * 1e-6, "The short-circuit current is where V = 0, not the last reading.")],
                  working=[rf"I = \frac Er = \frac{{{E_mv}\times10^{{-3}}}}{{{ltx(r_k * 1000)}}} = {ltx(isc)}\ \text{{A}}"])
    ex.on(IR).choice("How should the e.m.f. be read from the V–I graph?", "It is the intercept on the voltage axis.",
                     [("It is the gradient.", "The gradient is −r."), ("It is the intercept on the current axis.", "That's the short-circuit current."),
                      ("It is the first reading taken.", "Extrapolate to I = 0.")])
    ex.on(SEMI).choice("The battery lights a red LED but not a blue one. Using band theory, why not the blue LED?",
                       "Electrons don't gain enough energy to move into the conduction band of the p-type — the blue LED's band gap is larger.",
                       [("The blue LED is reverse biased.", "Both are forward biased."),
                        ("Holes and electrons don't recombine.", "Use band theory (course report 2018)."),
                        ("Blue light has a longer wavelength.", "Blue light has a SHORTER wavelength.")])
    return ex.build("A student makes a battery from a potato, a copper strip and a magnesium strip, and measures its t.p.d. for different currents.")


# ════════════════ Defibrillator: Q = CV → energy → resistance → discharge curve ════════════════

def defibrillator(level="Higher"):
    ex = _ex(level)
    c_uf, kv = pick(64, 50, 80), pick(2.0, 2.5, 3.0)
    V = kv * 1000
    Q = c_uf * 1e-6 * V
    ex.on(CAP).num(f"The {c_uf} µF capacitor is charged to {kv:g} kV. Calculate the charge stored.", Q, "C",
                   wrong=[(c_uf * kv, "Convert µF → F and kV → V."), (c_uf * 1e-6 * kv, "Convert kV to V.")],
                   working=[r"C = \frac QV", rf"Q = {c_uf}\times10^{{-6}} \times {ltx(V)} = {ltx(Q)}\ \text{{C}}"])
    En = 0.5 * sig(Q) * V
    ex.on(CAP).num("Calculate the maximum energy stored.", En, "J",
                   wrong=[(2 * En, "E = ½QV — include the ½."), (0.5 * sig(Q) * V ** 2, "E = ½QV — don't square V here.")],
                   working=[rf"E = \tfrac12QV = \tfrac12 \times {ltx(Q)} \times {ltx(V)} = {ltx(En)}\ \text{{J}}"])
    I0 = pick(30.0, 35.0, 40.0)
    ex.on(CIRC).num(f"The initial discharge current through the patient is {I0:g} A. Calculate the patient's resistance between the paddles.", V / I0, "Ω",
                    wrong=[(kv / I0, "Convert kV to V.")], working=[r"V = IR", rf"R = \frac{{{ltx(V)}}}{{{I0:g}}} = {ltx(V / I0)}\ \Omega"])
    ex.on(CAP).choice("Why does the current decrease during the discharge?", "The p.d. across the capacitor decreases as it loses charge.",
                      [("The patient's resistance increases.", "The resistance stays the same."),
                       ("The capacitor runs out of current.", "Explain with p.d. (course report 2015)."),
                       ("The capacitance decreases.", "C is fixed.")])
    ex.on(CAP).choice("The defibrillator is used on a patient with a larger resistance. How does the current–time graph change?",
                      "Smaller initial current and it takes longer to fall to zero.",
                      [("Same initial current, takes longer.", "I₀ = V/R is smaller (course report 2015)."),
                       ("Larger initial current, faster.", "Larger R → smaller current."),
                       ("Smaller initial current, faster.", "Takes LONGER.")])
    return ex.build("A defibrillator stores energy in a capacitor and discharges it through a patient's chest using two paddles.")


# ════════════════ Charging experiment: constant current → capacitance → energy → resistor ════════════════

def charging_experiment(level="Higher"):
    ex = _ex(level)
    I_ua, t, Vs = pick(15, 20, 30), pick(25, 28, 40), pick(9.0, 12.0)
    Q = I_ua * 1e-6 * t
    ex.on(CAP).num(f"The capacitor is charged at a constant {I_ua} µA for {t} s. Calculate the charge stored.", Q, "C",
                   wrong=[(I_ua * t, "Convert µA to A.")], working=[r"Q = It", rf"Q = {I_ua}\times10^{{-6}} \times {t} = {ltx(Q)}\ \text{{C}}"])
    Vc = pick(4.0, 5.0, 6.0)
    Cap = sig(Q) / Vc
    ex.on(CAP).num(f"The p.d. across the capacitor is now {Vc:g} V. Calculate its capacitance.", Cap, "F",
                   wrong=[(sig(Q) * Vc, "C = Q ÷ V."), (sig(Q) / Vs, "Use the p.d. across the CAPACITOR.")],
                   working=[r"C = \frac QV", rf"C = \frac{{{ltx(Q)}}}{{{Vc:g}}} = {ltx(Cap)}\ \text{{F}}"])
    VR = Vs - Vc
    ex.on(CIRC).num(f"The supply is {Vs:g} V. Calculate the resistance of the variable resistor at this instant.", VR / (I_ua * 1e-6), "Ω",
                    wrong=[(Vs / (I_ua * 1e-6), "The p.d. across R is the supply minus the capacitor's p.d."), (Vc / (I_ua * 1e-6), "Use the p.d. across R, not across C.")],
                    working=[rf"V_R = {Vs:g} - {Vc:g} = {VR:g}\ \text{{V}}", rf"R = \frac{{V_R}}{{I}} = {ltx(VR / (I_ua * 1e-6))}\ \Omega"],
                    scaffold=[("p.d. across R (V)", VR, "V")])
    ex.on(CAP).choice("Why must the resistance be decreased as the capacitor charges?",
                      "As the capacitor's p.d. rises, the p.d. across R falls, so R must fall to keep the current constant.",
                      [("Because the capacitor's resistance rises.", "Explain using p.d."), ("To increase the current.", "The aim is a CONSTANT current."),
                       ("Because the supply p.d. falls.", "The supply is constant (course report 2025).")])
    En = 0.5 * sig(Cap) * Vs ** 2
    ex.on(CAP).num("Calculate the energy stored when the capacitor is fully charged from this supply.", En, "J",
                   wrong=[(2 * En, "E = ½CV²."), (0.5 * sig(Cap) * Vs, "Square the p.d.")],
                   working=[rf"E = \tfrac12CV^2 = \tfrac12 \times {ltx(Cap)} \times {Vs:g}^2 = {ltx(En)}\ \text{{J}}"])
    return ex.build("A student investigates a capacitor by charging it at a constant current, adjusting a variable resistor in series with it.")


# ════════════════ Garden lights: solar cell → LEDs in parallel → power → photon ════════════════

def garden_lights(level="Higher"):
    ex = _ex(level)
    ex.on(SEMI).choice("The solar cell is a p-n junction. Name the effect by which it produces a p.d.", "The photovoltaic effect.",
                       [("The photoelectric effect.", "That's emission of electrons from a metal surface."),
                        ("Thermionic emission.", "No heating is involved."), ("Forward bias.", "That's a way of connecting a junction.")])
    ex.on(SEMI).choice("Using band theory, explain how the solar cell produces a p.d.",
                       "Electrons absorb photons and move from the valence band to the conduction band; the junction moves them towards the n-type.",
                       [("Electrons fall from the conduction band to the valence band, emitting photons.", "That's an LED (course report 2024)."),
                        ("Holes absorb photons and move up into the conduction band.", "Wrong physics."),
                        ("Light makes the junction warmer so it conducts.", "It is photon absorption.")])
    n, Rb, V = pick(8, 10, 12), pick(220, 330, 470), pick(5.0, 6.0)
    Rt = Rb / n
    ex.on(CIRC).num(f"The array supplies {V:g} V to {n} branches in parallel, each with a combined (LED + resistor) resistance of {Rb} Ω. Calculate the total resistance.",
                    Rt, "Ω", wrong=[(n * Rb, "The branches are in PARALLEL."), (n / Rb, "Invert 1/R_T.")],
                    working=[rf"\frac1{{R_T}} = {n} \times \frac1{{{Rb}}},\ R_T = {ltx(Rt)}\ \Omega"])
    P = V ** 2 / sig(Rt)
    ex.on(CIRC).num("Calculate the total power supplied.", P, "W",
                    wrong=[(V ** 2 / Rb, "Use the total resistance."), (V / sig(Rt), "That's the current.")],
                    working=[rf"P = \frac{{V^2}}{{R}} = \frac{{{V:g}^2}}{{{ltx(Rt)}}} = {ltx(P)}\ \text{{W}}"])
    lam = pick(470, 520, 590, 625)
    Eph = H * C / (lam * 1e-9)
    ex.on(SEMI).num(f"Each LED emits light of wavelength {lam} nm. Calculate the band gap energy.", Eph, "J",
                    wrong=[(H * C / lam, "Convert nm to m."), (H * lam * 1e-9 / C, "f = v ÷ λ.")],
                    working=[rf"f = \frac v\lambda = {ltx(C / (lam * 1e-9))}\ \text{{Hz}}", rf"E = hf = {ltx(Eph)}\ \text{{J}}"])
    return ex.build("A set of garden lights in a Lewis croft is powered by an array of solar cells.")


SCENARIOS = {
    "Lighthouse Supply":   lighthouse,
    "Car Battery":         car_battery,
    "Potato Battery":      potato_battery,
    "Defibrillator":       defibrillator,
    "Charging Experiment": charging_experiment,
    "Garden Lights":       garden_lights,
}
