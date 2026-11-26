"""Higher Electricity — exam-style questions that each stay within one topic, modelled on SQA paper questions
with changing numbers.

Recognised wrong answers follow the Higher marking instructions: peak and r.m.s. confused, ms left
unconverted, the wrong resistor in a potential divider, the gradient of a V–I graph taken as +r, lost volts
confused with the terminal p.d., the supply p.d. used as the p.d. across R while a capacitor charges, the ½
dropped from E = ½CV², and nm or prefixes left unconverted.
"""
import math

from topics.exam_style.base import fmt, graph, ltx, pick, sig
from topics.exam_style.higher_electricity import AC, C, CAP, CIRC, H, IR, R2, SEMI, _ex


def signal_generator(level="Higher"):
    ex = _ex(level).on(AC)
    div, gain = pick(2.0, 3.0, 3.5), pick(0.50, 2.0, 5.0)
    waves, tb = pick(4, 5, 8), pick(0.50, 2.0, 5.0)
    peak = div * gain
    ex.num("Determine the peak voltage of the output.", peak, "V",
           wrong=[(2 * peak, "Measure from the centre line, not crest to trough."), (gain / div, "Multiply the divisions by the Y-gain.")],
           working=[rf"V_{{peak}} = {div:g} \times {gain:g} = {ltx(peak)}\ \text{{V}}"])
    rms = sig(peak) / R2
    ex.num("Calculate the r.m.s. voltage.", rms, "V",
           wrong=[(sig(peak) * R2, "Divide by √2."), (sig(peak) / 2, "V_rms = V_peak ÷ √2, not ÷ 2.")],
           working=[rf"V_{{rms}} = \frac{{{ltx(peak)}}}{{\sqrt2}} = {ltx(rms)}\ \text{{V}}"])
    T = waves * tb / 1000
    ex.num("Determine the frequency of the output.", 1 / T, "Hz",
           wrong=[(1 / (waves * tb), "Convert ms to s."), (1 / (tb / 1000), "Use the number of divisions for one whole wave."), (T, "f = 1 ÷ T.")],
           working=[rf"T = {waves} \times {tb:g}\times10^{{-3}} = {ltx(T)}\ \text{{s}}", rf"f = \frac1T = {ltx(1 / T)}\ \text{{Hz}}"],
           scaffold=[("Period, in s?", T, "s")])
    R = pick(47, 68, 120, 220)
    ipk = sig(rms) / R * R2
    ex.num(f"A {R} Ω resistor is connected across the output, which stays the same. Calculate the peak current in it.", ipk, "A",
           wrong=[(sig(rms) / R, "That's the r.m.s. current; multiply by √2."), (sig(peak) * R, "I = V ÷ R.")],
           working=[rf"I_{{peak}} = \frac{{V_{{peak}}}}{{R}} = \frac{{{ltx(peak)}}}{{{R}}} = {ltx(ipk)}\ \text{{A}}"])
    ex.choice("The timebase setting is halved, with the signal unchanged. What happens to the trace?",
              "Each wave takes up twice as many divisions, so half as many waves are seen.",
              [("Twice as many waves are seen.", "Less time per division means less time across the screen."),
               ("The trace becomes twice as tall.", "Height is set by the Y-gain."),
               ("The frequency of the signal halves.", "The oscilloscope settings do not change the signal.")])
    ex.choice("State what is meant by an alternating current.", "A current that changes direction and instantaneous value with time.",
              [("A current whose r.m.s. value changes with time.", "The r.m.s. value of a steady a.c. supply is constant."),
               ("A current that flows in one direction but changes size.", "It also changes direction."),
               ("A current that switches on and off.", "It reverses direction.")])
    return ex.build(f"A signal generator is connected to an oscilloscope. The crests of the trace are {div:g} divisions above the centre line, and one complete "
                    f"wave covers {waves} divisions horizontally. The Y-gain is {gain:g} V/div and the timebase is {tb:g} ms/div.")


def sensor_divider(level="Higher"):
    ex = _ex(level).on(CIRC)
    vs = pick(6.0, 9.0, 12.0)
    r1, r2 = pick((2200, 3300), (1500, 4700), (4700, 2200), (1000, 1500))
    total = r1 + r2
    cur = vs / total
    ex.num("Calculate the current in the circuit.", cur, "A",
           wrong=[(vs / r2, "Use the total series resistance."), (vs / (r1 * r2 / total), "The resistors are in SERIES.")],
           working=[rf"I = \frac{{V}}{{R_T}} = \frac{{{vs:g}}}{{{r1} + {r2}}} = {ltx(cur)}\ \text{{A}}"])
    v2 = vs * r2 / total
    ex.num(f"Determine the potential difference across the {r2} Ω resistor.", v2, "V",
           wrong=[(vs * r1 / total, f"That's the p.d. across the {r1} Ω resistor."), (vs * r2 / r1, "V₂ = R₂ ÷ (R₁ + R₂) × V_S.")],
           working=[rf"V_2 = \left(\frac{{{r2}}}{{{r1} + {r2}}}\right) \times {vs:g} = {ltx(v2)}\ \text{{V}}"])
    ex.num(f"Calculate the power dissipated in the {r2} Ω resistor.", sig(v2) ** 2 / r2, "W",
           wrong=[(vs ** 2 / r2, "Use the p.d. across this resistor, not the supply p.d."), (sig(v2) / r2, "That's the current.")],
           working=[rf"P = \frac{{V^2}}{{R}} = \frac{{{ltx(v2)}^2}}{{{r2}}} = {ltx(sig(v2) ** 2 / r2)}\ \text{{W}}"])
    par = r2 / 2
    new = vs * par / (r1 + par)
    ex.num(f"A second {r2} Ω resistor is connected in parallel with the first one. Determine the new p.d. across the pair.", new, "V",
           wrong=[(v2, "The resistance of that part of the circuit has changed."), (vs * 2 * r2 / (r1 + 2 * r2), "Resistors in parallel have a SMALLER combined resistance."),
                  (sig(v2) / 2, "Find the combined resistance, then use the potential divider again.")],
           working=[rf"R_p = {ltx(par)}\ \Omega", rf"V = \left(\frac{{{ltx(par)}}}{{{r1} + {ltx(par)}}}\right) \times {vs:g} = {ltx(new)}\ \text{{V}}"],
           scaffold=[("Combined resistance of the parallel pair, in Ω?", par, "Ω")])
    ex.choice(f"When the second resistor is added, what happens to the p.d. across the {r1} Ω resistor, and why?",
              "It increases: the total resistance falls, so the current from the supply rises.",
              [("It decreases: the current is now shared between two resistors.", f"All the supply current still passes through the {r1} Ω resistor, and it is larger."),
               (f"It stays the same: the {r1} Ω resistor has not changed.", "The current through it has changed."),
               ("It decreases: the total resistance rises.", "Adding a parallel resistor lowers the resistance.")])
    return ex.build(f"A {r1} Ω resistor and a {r2} Ω resistor are connected in series across a {vs:g} V supply of negligible internal resistance.")


def supply_graph(level="Higher"):
    ex = _ex(level).on(IR)
    emf, r = pick((6.0, 8.0), (4.5, 3.0), (9.0, 6.0), (1.5, 2.5))
    imax = float(f"{emf / r * 0.7:.1g}")
    fig = graph([(0, emf), (imax / 2, emf - r * imax / 2), (imax, emf - r * imax)], xlabel="Current (A)", ylabel="Terminal p.d. (V)")
    v_end = emf - r * imax
    ex.choice("Use the graph to find the e.m.f. of the supply.", f"{emf:g} V",
              [(f"{v_end:g} V", "The e.m.f. is the value when the current is zero."), (f"{emf - r * imax / 2:g} V", "Read the intercept on the p.d. axis."),
               ("0 V", "The p.d. is zero on a short circuit; the e.m.f. is read where the CURRENT is zero.")])
    ex.num(f"The graph starts at (0 A, {emf:g} V) and ends at ({imax:g} A, {v_end:g} V). Determine the internal resistance.", r, "Ω",
           wrong=[(-r, "The gradient is −r; the resistance itself is positive."), (v_end / imax, "That's the external resistance at this point."),
                  (imax / (emf - v_end), "r = −gradient = ΔV ÷ ΔI.")],
           working=[rf"\text{{gradient}} = \frac{{{v_end:g} - {emf:g}}}{{{imax:g} - 0}} = -{ltx(r)}", rf"r = {ltx(r)}\ \Omega"])
    isc = emf / r
    ex.num("Calculate the short-circuit current.", isc, "A",
           wrong=[(imax, "On a short circuit the terminal p.d. is zero; the plotted points do not reach that."), (emf * r, "I = E ÷ r.")],
           working=[rf"I = \frac Er = \frac{{{emf:g}}}{{{r:g}}} = {ltx(isc)}\ \text{{A}}"])
    R = pick(10, 12, 18, 22)
    cur = emf / (R + r)
    ex.num(f"A {R} Ω resistor is now connected across the supply. Calculate the terminal potential difference.", cur * R, "V",
           wrong=[(emf, "Some p.d. is lost across the internal resistance."), (cur * r, "That's the lost volts.")],
           working=[rf"I = \frac{{{emf:g}}}{{{R} + {r:g}}} = {ltx(cur)}\ \text{{A}}", rf"V = IR = {ltx(cur * R)}\ \text{{V}}"],
           scaffold=[("Current in the circuit, in A?", cur, "A")])
    ex.choice("A second supply has a smaller e.m.f. and a greater internal resistance. How does its graph compare?",
              "It starts lower on the p.d. axis and is steeper.",
              [("It starts lower on the p.d. axis and is less steep.", "A greater r gives a steeper line."),
               ("It starts higher on the p.d. axis and is steeper.", "A smaller e.m.f. gives a lower intercept."),
               ("It is parallel to the first line but lower.", "Parallel lines have the same internal resistance.")])
    return ex.build("A student varies the current from a power supply and plots its terminal potential difference against the current.", figure=fig)


def cell_and_switch(level="Higher"):
    ex = _ex(level).on(IR)
    emf = pick(1.5, 3.0, 6.0, 9.0)
    r_true, R_true = pick(0.40, 0.60, 1.2), pick(4.0, 5.6, 8.0)
    cur = float(f"{emf / (R_true + r_true):.2g}")
    v = float(f"{emf - cur * r_true:.3g}")
    r = (emf - v) / cur
    ex.num("Calculate the internal resistance of the cell.", r, "Ω",
           wrong=[(v / cur, "That's the external resistance."), (emf / cur, "That's the total resistance."), ((emf - v) * cur, "r = lost volts ÷ current.")],
           working=[r"E = V + Ir", rf"{emf:g} = {v:g} + {cur:g}r", rf"r = {ltx(r)}\ \Omega"], scaffold=[("Lost volts, in V?", emf - v, "V")])
    ex.num("Calculate the resistance of the external resistor.", v / cur, "Ω",
           wrong=[(emf / cur, "Use the terminal p.d., which is the p.d. across the resistor."), ((emf - v) / cur, "That's the internal resistance.")],
           working=[rf"R = \frac VI = \frac{{{v:g}}}{{{cur:g}}} = {ltx(v / cur)}\ \Omega"])
    ex.num("Calculate the power dissipated inside the cell.", cur * (emf - v), "W",
           wrong=[(cur * v, "That's the power in the external resistor."), (cur * emf, "That's the total power supplied.")],
           working=[rf"P = IV_{{lost}} = {cur:g} \times {ltx(emf - v)} = {ltx(cur * (emf - v))}\ \text{{W}}"])
    ex.choice(f"State what is meant by an e.m.f. of {emf:g} V.", f"{emf:g} J of energy is supplied to each coulomb of charge passing through the cell.",
              [(f"The cell can supply {emf:g} J of energy in total.", "It is energy per coulomb."), (f"{emf:g} V is always across the terminals.", "Only with no current."),
               (f"{emf:g} J of energy is lost by each coulomb inside the cell.", "That would describe lost volts.")])
    ex.choice("Why is the voltmeter reading lower with the switch closed than with it open?",
              "There is now a current, so there is a potential difference across the internal resistance.",
              [("The e.m.f. of the cell falls when the switch is closed.", "The e.m.f. is constant."),
               ("The voltmeter takes some of the current.", "An ideal voltmeter takes no current."),
               ("The internal resistance appears only when the voltmeter is connected.", "It is always there; it matters when there is a current.")])
    return ex.build(f"A voltmeter is connected across a cell. With switch S open it reads {emf:g} V. When S is closed, connecting a resistor across the cell, "
                    f"it reads {v:g} V and the current is {cur:g} A.")


def charging_through_resistor(level="Higher"):
    ex = _ex(level).on(CAP)
    vs, R_k, c_uf = pick(6.0, 9.0, 12.0), pick(22, 47, 100, 220), pick(47, 100, 220, 470)
    i0 = vs / (R_k * 1000)
    ex.num("Calculate the initial charging current.", i0, "A",
           wrong=[(vs / R_k, "Convert kΩ to Ω."), (vs * R_k * 1000, "I = V ÷ R.")],
           working=[rf"I = \frac VR = \frac{{{vs:g}}}{{{R_k}\times10^3}} = {ltx(i0)}\ \text{{A}}"])
    frac = pick(0.25, 0.40, 0.60)
    i = float(f"{i0 * frac:.2g}")
    vc = vs - i * R_k * 1000
    ex.num(f"Later the current is {fmt(i)} A. Calculate the p.d. across the capacitor at this instant.", vc, "V",
           wrong=[(i * R_k * 1000, "That's the p.d. across the RESISTOR."), (vs, "The capacitor shares the supply p.d. with the resistor while charging.")],
           working=[rf"V_R = IR = {ltx(i * R_k * 1000)}\ \text{{V}}", rf"V_C = {vs:g} - V_R = {ltx(vc)}\ \text{{V}}"],
           scaffold=[("p.d. across the resistor, in V?", i * R_k * 1000, "V")])
    q = c_uf * 1e-6 * sig(vc)
    ex.num("Calculate the charge on the capacitor at this instant.", q, "C",
           wrong=[(c_uf * 1e-6 * vs, "Use the p.d. across the capacitor at this instant."), (c_uf * sig(vc), "Convert µF to F.")],
           working=[rf"Q = CV = {c_uf}\times10^{{-6}} \times {ltx(vc)} = {ltx(q)}\ \text{{C}}"])
    E = 0.5 * c_uf * 1e-6 * vs ** 2
    ex.num("Calculate the energy stored when the capacitor is fully charged.", E, "J",
           wrong=[(2 * E, "E = ½CV²: include the ½."), (0.5 * c_uf * 1e-6 * vs, "Square the p.d."), (0.5 * c_uf * vs ** 2, "Convert µF to F.")],
           working=[rf"E = \tfrac12CV^2 = \tfrac12 \times {c_uf}\times10^{{-6}} \times {vs:g}^2 = {ltx(E)}\ \text{{J}}"])
    ex.choice("The resistor is replaced by one of greater resistance and the capacitor is charged again from empty. What changes?",
              "The initial current is smaller and charging takes longer; the final p.d. is unchanged.",
              [("The initial current is smaller and the capacitor ends with less charge.", "The final p.d. equals the supply p.d., so the charge is the same."),
               ("The initial current is the same but charging takes longer.", "I = V ÷ R, so it is smaller."),
               ("The capacitor charges faster and stores more energy.", "More resistance means a smaller current.")])
    ex.choice("Why does the charging current decrease as the capacitor charges?",
              "The p.d. across the capacitor increases, so the p.d. across the resistor decreases.",
              [("The resistance of the resistor increases.", "R is constant."),
               ("The e.m.f. of the supply decreases.", "The supply is constant."),
               ("The capacitance decreases as charge builds up.", "C is constant.")])
    return ex.build(f"An uncharged {c_uf} µF capacitor is connected in series with a {R_k} kΩ resistor and a {vs:g} V supply of negligible internal resistance.")


def camera_flash(level="Higher"):
    ex = _ex(level).on(CAP)
    c_uf, v = pick(120, 150, 330), pick(240, 300, 330)
    q = c_uf * 1e-6 * v
    ex.num("Calculate the charge stored on the fully charged capacitor.", q, "C",
           wrong=[(c_uf * v, "Convert µF to F."), (v / (c_uf * 1e-6), "Q = CV.")],
           working=[rf"Q = CV = {c_uf}\times10^{{-6}} \times {v} = {ltx(q)}\ \text{{C}}"])
    E = 0.5 * sig(q) * v
    ex.num("Calculate the energy stored in the capacitor.", E, "J",
           wrong=[(2 * E, "E = ½QV: include the ½."), (0.5 * c_uf * 1e-6 * v, "Square the p.d. in E = ½CV².")],
           working=[rf"E = \tfrac12QV = \tfrac12 \times {ltx(q)} \times {v} = {ltx(E)}\ \text{{J}}"])
    R = pick(1.5, 2.4, 3.0)
    ex.num(f"The flash tube has an effective resistance of {R:g} Ω. Calculate the initial discharge current.", v / R, "A",
           wrong=[(v * R, "I = V ÷ R.")], working=[rf"I = \frac VR = \frac{{{v}}}{{{R:g}}} = {ltx(v / R)}\ \text{{A}}"])
    ms = pick(1.0, 1.5, 2.0)
    ex.num(f"The capacitor releases its energy in {ms:g} ms. Calculate the average power of the flash.", sig(E) / (ms / 1000), "W",
           wrong=[(sig(E) / ms, "Convert ms to s."), (sig(E) * ms / 1000, "P = E ÷ t.")],
           working=[rf"P = \frac Et = \frac{{{ltx(E)}}}{{{ms:g}\times10^{{-3}}}} = {ltx(sig(E) / (ms / 1000))}\ \text{{W}}"])
    ex.choice("A capacitor of smaller capacitance is charged to the same p.d. and used instead. How does the energy released compare, and why?",
              "It is less, because E = ½CV² and the capacitance is smaller.",
              [("It is the same, because the p.d. is the same.", "Energy also depends on the capacitance."),
               ("It is more, because it discharges faster.", "Speed of discharge does not add energy."),
               ("It is less, because the p.d. across it is smaller.", "The p.d. is the same.")])
    ex.choice("Why does the current in the flash tube fall during the discharge?", "The p.d. across the capacitor decreases as it loses charge.",
              [("The capacitor runs out of current.", "Explain in terms of the p.d."), ("The resistance of the tube increases.", "It is taken as constant."),
               ("The capacitance decreases.", "C is fixed.")])
    return ex.build(f"A camera flash uses a {c_uf} µF capacitor that is charged to {v} V and then discharged through a flash tube.")


def led_band_gap(level="Higher"):
    ex = _ex(level).on(SEMI)
    lam, colour = pick((470, "blue"), (525, "green"), (590, "yellow"), (640, "red"))
    gap = float(f"{H * C / (lam * 1e-9):.3g}")
    f = gap / H
    ex.num("Calculate the frequency of the light emitted by the LED.", f, "Hz",
           wrong=[(gap * H, "E = hf, so f = E ÷ h."), (H / gap, "f = E ÷ h.")],
           working=[rf"E = hf \Rightarrow f = \frac{{{ltx(gap)}}}{{6.63\times10^{{-34}}}} = {ltx(f)}\ \text{{Hz}}"])
    wl = C / sig(f) * 1e9
    ex.num("Calculate the wavelength of this light, in nanometres.", wl, "nm",
           wrong=[(wl * 1e-9, "That is in metres; the question asks for nanometres."), (sig(f) / C, "λ = v ÷ f.")],
           working=[rf"v = f\lambda \Rightarrow \lambda = \frac{{3.00\times10^8}}{{{ltx(f)}}} = {ltx(wl * 1e-9)}\ \text{{m}} = {ltx(wl)}\ \text{{nm}}"])
    ex.choice("What colour is the light?", colour.capitalize(),
              [(c.capitalize(), "Compare your wavelength with the visible spectrum.") for c in ("blue", "green", "yellow", "red") if c != colour])
    ex.choice("Using band theory, which describes how the forward-biased LED emits light?",
              "Electrons move from the n-type conduction band towards the p-type conduction band, fall to the valence band and emit photons.",
              [("Electrons absorb photons and move from the valence band to the conduction band.", "That is how a solar cell works."),
               ("Holes and electrons recombine and give out light.", "Use band theory and name the bands."),
               ("Electrons move from the valence band up to the conduction band and emit photons.", "A photon is emitted when an electron FALLS to a lower band.")])
    ex.choice("The LED is replaced by one with a larger band gap. How does the light it emits differ?",
              "Each photon has more energy, so the frequency is higher and the wavelength shorter.",
              [("Each photon has more energy, so the wavelength is longer.", "More energy means a shorter wavelength."),
               ("More photons are emitted each second, with the same frequency.", "The band gap sets the energy of each photon."),
               ("Each photon has less energy, so the frequency is lower.", "A larger gap releases more energy.")])
    ex.choice("A p-n junction can also produce a p.d. when light falls on it. What is this effect called?", "The photovoltaic effect",
              [("The photoelectric effect", "That is the emission of electrons from a surface."), ("Forward biasing", "That is a way of connecting a junction."),
               ("Stimulated emission", "That is the process in a laser.")])
    return ex.build(f"An LED has a band gap of {fmt(gap)} J. It is connected so that it is forward biased and emits light.")


TOPIC_SCENARIOS_ELECTRICITY = {
    "Signal Generator":          signal_generator,
    "Resistors and a Divider":   sensor_divider,
    "Power Supply Graph":        supply_graph,
    "Cell and Switch":           cell_and_switch,
    "Charging Through a Resistor": charging_through_resistor,
    "Camera Flash":              camera_flash,
    "LED Colour":                led_band_gap,
}
