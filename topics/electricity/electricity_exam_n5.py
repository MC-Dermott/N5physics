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
from utils.circuit_diagram import comp, divider, loop_circuit, network as net3, par, with_diagram

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


def gen_ec_ohm_experiment(level="N5"):
    """Ohm's law experiment and V–I graphs: meter positions, obtaining a range of readings, graph conclusions."""
    kind = random.choice(["meters", "range", "lamp", "resistor_graph", "warming", "reliable", "anomalous", "zero_error", "better_method",
                          "supply_range", "mean_current", "table_headings", "conclusion"])
    if kind == "supply_range":
        qobj = _choice("A student uses a variable power supply, an ammeter, a voltmeter and a resistor R to find how the current in R depends on the voltage across it. "
                       "How does the student obtain a range of readings?",
                       "Change the voltage of the variable power supply, recording the voltmeter and ammeter readings each time.",
                       [("Change the resistance of R.", "R is the resistor being investigated — it must stay the same."),
                        ("Change the ammeter to a different range.", "Changing the meter range does not change the current or voltage."),
                        ("Change the voltmeter so that it is in series with R.", "The voltmeter must stay in parallel with (across) R.")], "Potential Difference", level)
        return with_diagram(qobj, loop_circuit([comp("ammeter"), comp("resistor", "R", voltmeter="V")], supply="varsupply", supply_label="variable power supply"))
    if kind == "mean_current":
        base = random.choice([0.10, 0.20, 0.30, 0.40, 0.50])
        d = random.choice([0.01, 0.02])
        reads = [round(base - d, 2), round(base, 2), round(base + d, 2)]
        V = random.choice([2.0, 4.0, 6.0, 8.0, 10.0])
        text = (f"A student measures the current in a resistor three times with {V:g} V across it: {reads[0]:g} A, {reads[1]:g} A and {reads[2]:g} A. "
                f"Calculate the mean current.")
        work = [_L(rf"I = \frac{{{reads[0]:g} + {reads[1]:g} + {reads[2]:g}}}{{3}} = {base:g}\ \mathrm{{A}}")]
        opts = [{"value": float(base), "mistake": None, "working": work},
                {"value": _sig(sum(reads)), "mistake": "The readings were added but not divided by 3.", "working": work},
                {"value": _sig(reads[2]), "mistake": "The largest reading was used — the mean uses all three readings.", "working": work},
                {"value": _sig(sum(reads) / 2), "mistake": "Divide by the NUMBER of readings (3), not 2.", "working": work}]
        scaffold = [{"question": "What is the sum of the three readings, in A?", "answer": _sig(sum(reads))}]
        return _q(text, float(base), "A", opts, "Potential Difference", scaffold, level)
    if kind == "table_headings":
        return _choice("A student presents the results of an Ohm's law experiment in a table. Which is the best way to give the units?",
                       "In the column headings only, e.g. ‘Voltage (V)’ and ‘Mean current (A)’.",
                       [("After every reading in the table.", "Units go in the column heading so each reading is just a number."),
                        ("Not at all — the units are obvious.", "Every column heading needs its unit."),
                        ("Only in the first row of the table.", "Put the unit in the heading for the whole column.")], "Potential Difference", level)
    if kind == "conclusion":
        return _choice("The graph of current against voltage for a resistor is a straight line through the origin. Which is the best conclusion?",
                       "The current in the resistor is directly proportional to the voltage across it.",
                       [("The current gets bigger.", "A conclusion must state the relationship between the two quantities."),
                        ("The current is directly proportional to the voltage because the graph is a straight line.", "It must also pass through the origin to show direct proportionality."),
                        ("The current is inversely proportional to the voltage.", "The current increases as the voltage increases.")], "Potential Difference", level)
    if kind == "meters":
        qobj = _choice("A student finds the resistance of resistor R using a battery, a variable resistor, an ammeter and a voltmeter. How should the meters be connected?",
                       "The ammeter in series with R and the voltmeter in parallel with R.",
                       [("The ammeter in parallel with R and the voltmeter in series with R.", "Ammeters go in series; voltmeters go across (in parallel with) the component."),
                        ("Both meters in series with R.", "The voltmeter must be connected across R."),
                        ("Both meters in parallel with R.", "The ammeter must be in series so the current passes through it.")], "Potential Difference", level)
        return with_diagram(qobj, loop_circuit([comp("variable", "variable resistor"), comp("resistor", "R")], supply_label=""))
    if kind == "range":
        qobj = _choice("The student wants a range of values of current and voltage for resistor R. What should be done?",
                       "Change the resistance of the variable resistor.",
                       [("Change the variable resistor.", "Must say it is the RESISTANCE of the variable resistor that is changed (course report 2024)."),
                        ("Change the voltage of the battery.", "The method uses the variable resistor to change the current and voltage."),
                        ("Change the resistance of R.", "R is the resistor being investigated — its resistance must stay the same.")], "Potential Difference", level)
        return with_diagram(qobj, loop_circuit([comp("variable", "variable resistor"), comp("resistor", "R")], supply_label=""))
    if kind == "reliable":
        return _choice("A student repeats an Ohm's law experiment and gets almost identical results each time. What does this show about the results?",
                       "They are reliable (repeatable).",
                       [("They are accurate.", "Close agreement between repeats shows the results are reliable; it does not show they are correct."),
                        ("They are anomalous.", "An anomalous result is one that does NOT fit the pattern."),
                        ("The resistance of the resistor is constant.", "Repeat readings agreeing says nothing about whether the resistance changes.")], "Potential Difference", level)
    if kind == "anomalous":
        return _choice("One pair of readings in an Ohm's law experiment does not fit the pattern of the others. What should the student do?",
                       "Repeat that measurement.",
                       [("Leave it out of the results without checking it.", "Check it by repeating the measurement first."),
                        ("Use it in the calculation as it is.", "An anomalous reading should be repeated, not used unchecked."),
                        ("Change the resistor and start again.", "Only the doubtful reading needs repeating.")], "Potential Difference", level)
    if kind == "zero_error":
        return _choice("The V–I line for a resistor does not pass through the origin. Which is a possible reason?",
                       "One of the meters has a zero error.",
                       [("The resistor has no resistance.", "The line has a gradient, so the resistor has a resistance."),
                        ("The voltage is directly proportional to the current.", "That would give a line through the origin."),
                        ("The ammeter was connected in parallel.", "That would affect the readings but is not the usual explanation for an offset line.")], "Potential Difference", level)
    if kind == "better_method":
        r = random.choice([4.8, 5.0, 10, 12, 22])
        return _choice(f"Student A finds the resistance of a resistor from one pair of readings. Student B plots a graph of five pairs of readings and uses its gradient to get {r:g} Ω. Which statement is correct?",
                       "Student B's method is better, because it uses several readings so one inaccurate reading has less effect.",
                       [("Student A's method is better, because it is quicker.", "Speed does not make a method more accurate."),
                        ("The methods are equally good, because both use V = IR.", "Using several readings reduces the effect of a single inaccurate reading."),
                        ("Student B's method is worse, because a graph needs more readings.", "More readings make the result more reliable, not less.")], "Potential Difference", level)
    if kind == "lamp":
        return _choice("The V–I graph for a filament lamp curves so that the gradient increases as the current increases. Which conclusion is correct?",
                       "The resistance of the lamp increases as the current increases.",
                       [("As the voltage increases, the current increases.", "That describes the graph but says nothing about the RESISTANCE (course report 2025)."),
                        ("The resistance of the lamp stays constant.", "A straight line through the origin means constant resistance; this curve does not."),
                        ("The resistance of the lamp decreases as the current increases.", "A steeper V–I line means a greater resistance.")], "Potential Difference", level)
    if kind == "resistor_graph":
        return _choice("Which V–I graph is correct for a fixed resistor at constant temperature?",
                       "A straight line through the origin.",
                       [("A straight line that does not pass through the origin.", "V is directly proportional to I, so the line goes through the origin."),
                        ("A curve with a gradient that increases.", "That is the shape for a filament lamp."),
                        ("A horizontal straight line.", "The voltage increases as the current increases.")], "Potential Difference", level)
    return _choice("What happens to the resistance of a filament lamp as it warms up after being switched on?",
                   "It increases, so the current decreases.",
                   [("It decreases, so the current increases.", "The resistance of the filament increases with temperature."),
                    ("It stays the same, so the current stays the same.", "The filament is non-ohmic: its resistance changes as it heats."),
                    ("It increases, so the current increases.", "A greater resistance with the same voltage means a smaller current.")], "Potential Difference", level)


def gen_ec_non_ohmic(level="N5"):
    """Direct proportionality, gradient = R, and non-ohmic components (filament lamp and diode)."""
    kind = random.choice(["diode_dir", "diode_threshold", "obey", "gradient_meaning", "proportional", "steeper", "lamp_resistance", "lamp_resistance"])
    if kind == "diode_dir":
        return _choice("Which statement describes how a diode conducts?",
                       "It conducts in one direction only; in the other direction its resistance is very high.",
                       [("It conducts equally well in both directions.", "A diode only allows current in one direction."),
                        ("It conducts in one direction only; in the other direction its resistance is zero.", "In the reverse direction the resistance is very HIGH, so there is no current."),
                        ("Its resistance is constant for all voltages.", "A diode is non-ohmic — its resistance is not constant.")], "Potential Difference", level)
    if kind == "diode_threshold":
        vt = random.choice([0.6, 0.7])
        return _choice(f"The current–voltage graph of a diode is drawn for forward voltages up to 1.0 V. Which statement describes the graph?",
                       f"There is almost no current until the voltage reaches about {vt:g} V, then the current increases rapidly.",
                       [("The current increases steadily from zero in a straight line.", "That is the graph for a resistor — a diode is non-ohmic."),
                        (f"The current is greatest at low voltages and falls above {vt:g} V.", "The current increases once the diode starts to conduct."),
                        ("The current is the same at every voltage.", "The current depends strongly on the voltage.")], "Potential Difference", level)
    if kind == "obey":
        return _choice("Which of these components obeys Ohm's law at constant temperature?",
                       "A fixed resistor.", [("A filament lamp.", "Its resistance increases as the filament gets hotter, so the V–I graph is a curve."),
                                              ("A diode.", "A diode conducts in one direction only and is not a straight line through the origin."),
                                              ("An LED.", "An LED is a diode — it is non-ohmic.")], "Potential Difference", level)
    if kind == "gradient_meaning":
        return _choice("A graph of voltage (y-axis) against current (x-axis) for a resistor is a straight line through the origin. What does the gradient of the line represent?",
                       "The resistance of the resistor.",
                       [("The power of the resistor.", "The gradient is ΔV ÷ ΔI, which is V ÷ I."),
                        ("The charge flowing in the resistor.", "Charge is current × time."),
                        ("The reciprocal of the resistance (1 ÷ R).", "With voltage on the y-axis the gradient is V ÷ I = R.")], "Potential Difference", level)
    if kind == "proportional":
        return _choice("A graph of voltage against current for a component is a straight line through the origin. Which statement is correct?",
                       "The voltage is directly proportional to the current, because the graph is a straight line through the origin.",
                       [("The voltage is directly proportional to the current, because the graph is a straight line.", "The line must ALSO pass through the origin."),
                        ("The voltage is inversely proportional to the current, because the graph is a straight line.", "V rises as I rises, so it is directly proportional."),
                        ("The voltage is not proportional to the current, because the graph goes through the origin.", "A straight line through the origin IS direct proportionality.")], "Potential Difference", level)
    if kind == "steeper":
        a, b = random.sample([10, 20, 30, 40, 50], 2)
        hi, lo = ("A", "B") if a > b else ("B", "A")
        return _choice(f"The V–I graphs (voltage on the y-axis) of resistors A and B are straight lines through the origin. At the same current, the voltage across resistor {hi} is greater than the voltage across resistor {lo}. "
                       f"Which resistor has the greater resistance?",
                       f"Resistor {hi}, because its graph has the steeper gradient.",
                       [(f"Resistor {lo}, because its graph has the steeper gradient.", "It is resistor " + hi + " whose line is steeper."),
                        (f"Resistor {hi}, because it has the smaller gradient.", "A steeper V–I line means a greater resistance."),
                        ("They have the same resistance, because both lines are straight.", "The gradients are different, so the resistances are different.")], "Potential Difference", level)
    i1, v1, i2, v2 = random.choice([(0.20, 2.4, 0.40, 8.0), (0.10, 0.5, 0.30, 4.5), (0.20, 1.0, 0.50, 10.0), (0.10, 0.8, 0.40, 8.0)])
    r1, r2 = v1 / i1, v2 / i2
    text = (f"The voltage across a filament lamp is {v1:g} V when the current is {i1:g} A and {v2:g} V when the current is {i2:g} A. "
            f"Calculate the resistance of the lamp when the current is {i2:g} A.")
    work = [_L(r"V = IR"), _L(rf"{v2:g} = {i2:g} \times R"), _L(rf"R = {_ltx(r2)}\ \Omega")]
    opts = [{"value": _sig(r2), "mistake": None, "working": work},
            {"value": _sig(r1), "mistake": f"That is the resistance at {i1:g} A. The question asks for the resistance at {i2:g} A.", "working": work},
            {"value": _sig((v2 - v1) / (i2 - i1)), "mistake": "The lamp's graph is a curve, so the gradient between two points is not its resistance — use R = V ÷ I at the stated current.", "working": work},
            {"value": _sig(v2 * i2), "mistake": "V = IR — divide the voltage by the current; V × I is power.", "working": work}]
    scaffold = [{"question": f"What is the resistance at {i1:g} A, in Ω?", "answer": _sig(r1)},
                {"question": f"What is the resistance at {i2:g} A, in Ω?", "answer": _sig(r2)}]
    return _q(text, _sig(r2), "Ω", opts, "Potential Difference", scaffold, level)


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
    qobj = _q(text, _sig(I), "A", opts, "Circuit Rules", scaffold, level)
    return with_diagram(qobj, loop_circuit([comp("resistor", f"{rs} Ω"), par([comp("resistor", f"{r1} Ω")], [comp("resistor", f"{r2} Ω")])], supply_label=f"{Vs:g} V"))


_SERIES_R = [20, 30, 40, 50, 60, 80, 100, 120, 150, 180, 220, 270]


def gen_ec_series_current(level="N5"):
    """Current in a circuit of three resistors in series (SQA 4-mark: total resistance, then V = IR)."""
    r1, r2, r3 = random.sample(_SERIES_R, 3)
    Vs = random.choice([6.0, 9.0, 12.0, 15.0, 24.0])
    rt = r1 + r2 + r3
    I = Vs / rt
    text = f"Three resistors of {r1} Ω, {r2} Ω and {r3} Ω are connected in series with a {Vs:g} V supply. Calculate the current in the circuit."
    work = [_L(rf"R_T = {r1} + {r2} + {r3} = {rt}\ \Omega"), _L(r"V = IR"), _L(rf"{Vs:g} = I \times {rt}"), _L(rf"I = {_ltx(I)}\ \mathrm{{A}}")]
    rp = 1 / (1 / r1 + 1 / r2 + 1 / r3)
    opts = [{"value": _sig(I), "mistake": None, "working": work},
            {"value": _sig(Vs / r1), "mistake": f"Only the {r1} Ω resistor was used — the supply voltage goes with the TOTAL resistance of the circuit.", "working": work},
            {"value": _sig(Vs / rp), "mistake": "The resistors were combined as if they were in parallel — in series the resistances add.", "working": work},
            {"value": _sig(Vs * rt), "mistake": "V = IR was not rearranged — I = V ÷ R, not V × R.", "working": work}]
    scaffold = [{"question": "What is the total resistance of the circuit, in Ω?", "answer": float(rt)},
                {"question": "What is the current in the circuit, in A?", "answer": _sig(I)}]
    qobj = _q(text, _sig(I), "A", opts, "Circuit Rules", scaffold, level)
    return with_diagram(qobj, loop_circuit([comp("ammeter"), comp("resistor", f"{r1} Ω"), comp("resistor", f"{r2} Ω"), comp("resistor", f"{r3} Ω")],
                                           supply_label=f"{Vs:g} V"))


def gen_ec_current_then_voltage(level="N5"):
    """Multi-step: find the supply current first, then a voltage (SQA 4-mark style; leads into potential dividers)."""
    kind = random.choice(["series2", "series3", "series_parallel", "find_r"])
    if kind == "series2":
        r1, r2 = random.sample(_SERIES_R, 2)
        Vs = random.choice([6.0, 9.0, 12.0, 15.0, 24.0])
        which = random.choice([1, 2])
        rx, ro = (r1, r2) if which == 1 else (r2, r1)
        rt = r1 + r2
        I = Vs / rt
        Vx = I * rx
        text = f"A {r1} Ω resistor and a {r2} Ω resistor are connected in series with a {Vs:g} V supply. Calculate the voltage across the {rx} Ω resistor."
        work = [_L(rf"R_T = {r1} + {r2} = {rt}\ \Omega"), _L(r"V = IR"), _L(rf"{Vs:g} = I \times {rt} \Rightarrow I = {_ltx(I)}\ \mathrm{{A}}"),
                _L(rf"V = {_ltx(I)} \times {rx} = {_ltx(Vx)}\ \mathrm{{V}}")]
        opts = [{"value": _sig(Vx), "mistake": None, "working": work},
                {"value": _sig(Vs), "mistake": "The supply voltage is shared between the resistors — it is not all across one of them.", "working": work},
                {"value": _sig(I * ro), "mistake": f"That is the voltage across the {ro} Ω resistor.", "working": work},
                {"value": _sig(Vs / rx * 1.0), "mistake": f"The supply voltage was used with only the {rx} Ω resistor — find the current with the TOTAL resistance first.", "working": work}]
        scaffold = [{"question": "What is the total resistance, in Ω?", "answer": float(rt)},
                    {"question": "What is the current in the circuit, in A?", "answer": _sig(I)},
                    {"question": f"What is the voltage across the {rx} Ω resistor, in V?", "answer": _sig(Vx)}]
        qobj = _q(text, _sig(Vx), "V", opts, "Circuit Rules", scaffold, level)
        return with_diagram(qobj, loop_circuit([comp("ammeter"), comp("resistor", f"{r1} Ω"), comp("resistor", f"{r2} Ω")], supply_label=f"{Vs:g} V"))
    if kind == "series3":
        r1, r2, r3 = random.sample(_SERIES_R, 3)
        Vs = random.choice([6.0, 9.0, 12.0, 15.0, 24.0])
        rt = r1 + r2 + r3
        I = Vs / rt
        V2 = I * r2
        text = f"Three resistors of {r1} Ω, {r2} Ω and {r3} Ω are connected in series with a {Vs:g} V supply. Calculate the voltage across the {r2} Ω resistor."
        work = [_L(rf"R_T = {r1} + {r2} + {r3} = {rt}\ \Omega"), _L(r"V = IR"), _L(rf"I = {Vs:g} \div {rt} = {_ltx(I)}\ \mathrm{{A}}"),
                _L(rf"V = {_ltx(I)} \times {r2} = {_ltx(V2)}\ \mathrm{{V}}")]
        opts = [{"value": _sig(V2), "mistake": None, "working": work},
                {"value": _sig(Vs / 3), "mistake": "The voltage is shared in proportion to the resistances, not equally.", "working": work},
                {"value": _sig(Vs * r2 / (r1 + r2)), "mistake": "All three resistors must be included in the total resistance.", "working": work},
                {"value": _sig(I * rt), "mistake": "I × R_T is the supply voltage, not the voltage across one resistor.", "working": work}]
        scaffold = [{"question": "What is the total resistance, in Ω?", "answer": float(rt)},
                    {"question": "What is the current in the circuit, in A?", "answer": _sig(I)},
                    {"question": f"What is the voltage across the {r2} Ω resistor, in V?", "answer": _sig(V2)}]
        qobj = _q(text, _sig(V2), "V", opts, "Circuit Rules", scaffold, level)
        return with_diagram(qobj, loop_circuit([comp("ammeter"), comp("resistor", f"{r1} Ω"), comp("resistor", f"{r2} Ω"), comp("resistor", f"{r3} Ω")], supply_label=f"{Vs:g} V"))
    if kind == "series_parallel":
        pairs = [(a, b) for a in _E12 for b in _E12 if a <= b and (a * b) % (a + b) == 0]
        r1, r2 = random.choice(pairs)
        rs = random.choice([x for x in (10, 20, 30, 40, 50) if x not in (r1, r2)])
        Vs = random.choice([6.0, 9.0, 12.0, 24.0])
        rp = r1 * r2 / (r1 + r2)
        rt = rp + rs
        I = Vs / rt
        Vs_res = I * rs
        text = (f"A {rs} Ω resistor is connected in series with a {r1} Ω resistor and a {r2} Ω resistor in parallel, across a {Vs:g} V supply. "
                f"Calculate the voltage across the {rs} Ω resistor.")
        work = [_L(rf"\frac{{1}}{{R_P}} = \frac{{1}}{{{r1}}} + \frac{{1}}{{{r2}}} \Rightarrow R_P = {rp:g}\ \Omega"), _L(rf"R_T = {rp:g} + {rs} = {rt:g}\ \Omega"),
                _L(rf"I = {Vs:g} \div {rt:g} = {_ltx(I)}\ \mathrm{{A}}"), _L(rf"V = {_ltx(I)} \times {rs} = {_ltx(Vs_res)}\ \mathrm{{V}}")]
        opts = [{"value": _sig(Vs_res), "mistake": None, "working": work},
                {"value": _sig(I * rp), "mistake": f"That is the voltage across the parallel pair, not across the {rs} Ω resistor.", "working": work},
                {"value": _sig(Vs), "mistake": "The supply voltage is shared between the series resistor and the parallel pair.", "working": work},
                {"value": _sig(Vs / (r1 + r2 + rs) * rs), "mistake": "The parallel resistors were added as if they were in series.", "working": work}]
        scaffold = [{"question": "What is the resistance of the parallel pair, in Ω?", "answer": float(rp)},
                    {"question": "What is the total resistance, in Ω?", "answer": float(rt)},
                    {"question": "What is the current from the supply, in A?", "answer": _sig(I)},
                    {"question": f"What is the voltage across the {rs} Ω resistor, in V?", "answer": _sig(Vs_res)}]
        qobj = _q(text, _sig(Vs_res), "V", opts, "Circuit Rules", scaffold, level)
        return with_diagram(qobj, loop_circuit([comp("ammeter"), comp("resistor", f"{rs} Ω"), par([comp("resistor", f"{r1} Ω")], [comp("resistor", f"{r2} Ω")])], supply_label=f"{Vs:g} V"))
    # find_r: potential divider, voltmeter reading across R2 known -> R2
    while True:
        R1 = random.choice([60, 80, 100, 120, 150, 200])
        I = random.choice([0.02, 0.04, 0.05, 0.10])
        V2 = random.choice([2.0, 3.0, 4.0, 5.0, 6.0])
        V1 = round(R1 * I, 2)
        Vs = round(V1 + V2, 2)
        R2 = round(V2 / I, 1)
        if Vs <= 24 and R2 != R1 and abs(R2 - R1) > 0.05 * R1:
            break
    text = (f"A {R1} Ω resistor and a resistor R are connected in series with a {Vs:g} V supply. The voltmeter across R reads {V2:g} V. Calculate the resistance of R.")
    work = [_L(rf"V_1 = {Vs:g} - {V2:g} = {V1:g}\ \mathrm{{V}}"), _L(rf"V = IR \Rightarrow {V1:g} = I \times {R1} \Rightarrow I = {_ltx(I)}\ \mathrm{{A}}"),
            _L(rf"{V2:g} = {_ltx(I)} \times R \Rightarrow R = {_ltx(R2)}\ \Omega")]
    opts = [{"value": _sig(R2), "mistake": None, "working": work},
            {"value": _sig(V2 / (Vs / R1)), "mistake": f"The supply voltage was used with the {R1} Ω resistor alone — the voltage across it is the supply voltage minus the voltmeter reading.", "working": work},
            {"value": _sig(Vs / I), "mistake": "Vs ÷ I is the TOTAL resistance of the circuit, not R.", "working": work},
            {"value": float(R1), "mistake": f"The resistance of the {R1} Ω resistor — the question asks for R.", "working": work}]
    scaffold = [{"question": f"What is the voltage across the {R1} Ω resistor, in V?", "answer": _sig(V1)},
                {"question": "What is the current in the circuit, in A?", "answer": _sig(I)},
                {"question": "What is the resistance of R, in Ω?", "answer": _sig(R2)}]
    qobj = _q(text, _sig(R2), "Ω", opts, "Circuit Rules", scaffold, level)
    return with_diagram(qobj, divider("resistor", f"{R1} Ω", "resistor", "R", supply_label=f"{Vs:g} V", vout_label=f"{V2:g} V"))


def gen_ec_switch_ammeter(level="N5"):
    """2023 Paper 2 Q6 style: S1 closed, then S2 closed adds an equal parallel branch (reading, total resistance, justify)."""
    ra = random.choice([10, 20, 24, 30])
    rb = random.choice([30, 36, 60, 90])
    Vs = random.choice([6.0, 10.0, 12.0, 18.0])
    rp = rb / 2
    r_s1, r_s2 = ra + rb, ra + rp
    diagram = loop_circuit([comp("switch", "S1"), comp("resistor", f"{ra} Ω"), par([comp("resistor", f"{rb} Ω")], [comp("switch", "S2"), comp("resistor", f"{rb} Ω")]),
                            comp("ammeter")], supply_label=f"{Vs:g} V")
    setup = "In the circuit shown both switches S1 and S2 are initially open. "
    kind = random.choice(["reading", "total", "justify"])
    if kind == "reading":
        I = Vs / r_s1
        text = setup + "S1 is closed. Determine the reading on the ammeter."
        work = [_L(rf"R_T = {ra} + {rb} = {r_s1}\ \Omega"), _L(r"V = IR"), _L(rf"{Vs:g} = I \times {r_s1}"), _L(rf"I = {_ltx(I)}\ \mathrm{{A}}")]
        opts = [{"value": _sig(I), "mistake": None, "working": work},
                {"value": _sig(Vs / r_s2), "mistake": "S2 is still open — the lower branch carries no current.", "working": work},
                {"value": _sig(Vs / ra), "mistake": "The resistor in the upper branch of the parallel pair was left out.", "working": work},
                {"value": _sig(Vs / (ra + 2 * rb)), "mistake": "Both parallel branches were added in series.", "working": work}]
        scaffold = [{"question": "What is the total resistance with only S1 closed, in Ω?", "answer": float(r_s1)},
                    {"question": "What is the ammeter reading, in A?", "answer": _sig(I)}]
        return with_diagram(_q(text, _sig(I), "A", opts, "Circuit Rules", scaffold, level), diagram)
    if kind == "total":
        text = setup + "S1 and S2 are both closed. Determine the total resistance of the circuit."
        work = [_L(rf"\frac{{1}}{{R_P}} = \frac{{1}}{{{rb}}} + \frac{{1}}{{{rb}}} \Rightarrow R_P = {rp:g}\ \Omega"), _L(rf"R_T = {ra} + {rp:g} = {r_s2:g}\ \Omega")]
        opts = [{"value": _sig(r_s2), "mistake": None, "working": work},
                {"value": _sig(r_s1), "mistake": "S2 is closed — the second branch is now in parallel with the first.", "working": work},
                {"value": _sig(ra + 2 * rb), "mistake": "The parallel resistors were added as if in series.", "working": work},
                {"value": _sig(rp), "mistake": "The series resistor was left out of the total.", "working": work}]
        scaffold = [{"question": "What is the resistance of the parallel pair, in Ω?", "answer": _sig(rp)},
                    {"question": "What is the total resistance, in Ω?", "answer": _sig(r_s2)}]
        return with_diagram(_q(text, _sig(r_s2), "Ω", opts, "Circuit Rules", scaffold, level), diagram)
    qobj = _choice(setup + "S1 is closed, and then S2 is also closed. What happens to the reading on the ammeter, and why?",
                   "It increases, because the total resistance of the circuit decreases.",
                   [("It increases, because the resistance decreases.", "Must make clear it is the TOTAL resistance of the circuit that decreases (course report 2023)."),
                    ("It decreases, because there is now more resistance in the circuit.", "A second parallel branch lowers the total resistance."),
                    ("It stays the same, because the supply voltage has not changed.", "The total resistance changes, so the current does.")],
                   "Circuit Rules", level)
    return with_diagram(qobj, diagram)


_ARRANGEMENTS = ("series", "parallel", "pair_series", "series_pair")


def gen_ec_three_resistors(level="N5"):
    """Total resistance of three resistors in one of the four possible arrangements (2018/2025 Paper 1 style)."""
    kind = random.choice(_ARRANGEMENTS)
    r = random.choice([6, 12, 15, 30, 60])
    a = f"{r} Ω"
    if kind == "series":
        rt = 3 * r
        text = f"Three {r} Ω resistors are connected in series. Calculate the total resistance."
        work = [_L(rf"R_T = {r} + {r} + {r} = {rt}\ \Omega")]
        wrong = [(r / 3, "The resistors were combined as if in parallel — in series the resistances add."), (2 * r, "All three resistors must be added.")]
        diagram = net3([comp("resistor", a)] * 3)
        steps = [{"question": "What is the total resistance, in Ω?", "answer": float(rt)}]
    elif kind == "parallel":
        rt = r / 3
        text = f"Three {r} Ω resistors are connected in parallel. Calculate the total resistance."
        work = [_L(rf"\frac{{1}}{{R_T}} = \frac{{3}}{{{r}}}"), _L(rf"R_T = {_ltx(rt)}\ \Omega")]
        wrong = [(3 / r, "1/R_T was not inverted."), (3 * r, "The resistors were added as if in series.")]
        diagram = net3([par(*[[comp("resistor", a)] for _ in range(3)])])
        steps = [{"question": "What is 1/R_T, in Ω⁻¹ (give it to 3 s.f.)?", "answer": _sig(3 / r)}, {"question": "What is the total resistance, in Ω?", "answer": _sig(rt)}]
    elif kind == "pair_series":
        rp = r / 2
        rt = rp + r
        text = f"Two {r} Ω resistors are connected in parallel and this combination is connected in series with a third {r} Ω resistor. Calculate the total resistance."
        work = [_L(rf"\frac{{1}}{{R_P}} = \frac{{1}}{{{r}}} + \frac{{1}}{{{r}}} \Rightarrow R_P = {_ltx(rp)}\ \Omega"), _L(rf"R_T = {_ltx(rp)} + {r} = {_ltx(rt)}\ \Omega")]
        wrong = [(r / 3, "All three were treated as parallel."), (3 * r, "All three were added as if in series."), (rp, "The series resistor was left out.")]
        diagram = net3([par([comp("resistor", a)], [comp("resistor", a)]), comp("resistor", a)])
        steps = [{"question": "What is the resistance of the parallel pair, in Ω?", "answer": _sig(rp)}, {"question": "What is the total resistance, in Ω?", "answer": _sig(rt)}]
    else:
        rs = 2 * r
        rt = rs * r / (rs + r)
        text = f"Two {r} Ω resistors are connected in series and this combination is connected in parallel with a third {r} Ω resistor. Calculate the total resistance."
        work = [_L(rf"R_S = {r} + {r} = {rs}\ \Omega"), _L(rf"\frac{{1}}{{R_T}} = \frac{{1}}{{{rs}}} + \frac{{1}}{{{r}}} \Rightarrow R_T = {_ltx(rt)}\ \Omega")]
        wrong = [(r / 3, "All three were treated as parallel."), (3 * r, "All three were added as if in series."), (r / 2 + r, "The two in series are the pair — they must be added first, then combined in parallel with the third.")]
        diagram = net3([par([comp("resistor", a), comp("resistor", a)], [comp("resistor", a)])])
        steps = [{"question": "What is the resistance of the series pair, in Ω?", "answer": float(rs)}, {"question": "What is the total resistance, in Ω?", "answer": _sig(rt)}]
    opts = [{"value": _sig(rt), "mistake": None, "working": work}] + [{"value": _sig(v), "mistake": why, "working": work} for v, why in wrong]
    qobj = _q(text, _sig(rt), "Ω", opts, "Circuit Rules", steps if len(steps) > 1 else None, level)
    return with_diagram(qobj, diagram)


# (device, number lo, hi, power each (W), supply V)
_PARALLEL_SETS = [("LED spotlights", 3, 5, 4.8, 12), ("halogen lamps", 2, 5, 20, 12), ("garden lights", 3, 5, 3.0, 12),
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
    qobj = _q(text, _sig(It), "A", opts, "Circuit Rules", scaffold, level)
    return with_diagram(qobj, loop_circuit([par(*[[comp("heater" if dev == "heaters" else "lamp")] for _ in range(n)])], supply_label=f"{V} V"))


def gen_ec_circuit_changes(level="N5"):
    kind = random.choice(["add_branch", "ldr_branch", "advantage"])
    if kind == "add_branch":
        qobj = _choice("A switch is closed that connects another resistor in parallel with the existing one. What happens to the supply current, and why?",
                       "It increases, because the total resistance of the circuit decreases.",
                       [("It increases, because the resistance goes down.", "Must make clear it is the TOTAL resistance of the circuit (course report 2023)."),
                        ("It decreases, because there is more resistance in the circuit.", "Adding a parallel branch lowers the total resistance."),
                        ("It stays the same, because the supply voltage is unchanged.", "The total resistance changes, so the current does.")], "Circuit Rules", level)
        return with_diagram(qobj, loop_circuit([par([comp("resistor")], [comp("switch", "S"), comp("resistor")])]))
    if kind == "ldr_branch":
        qobj = _choice("An LDR is in one branch of a parallel circuit and a fixed resistor is in the other. The light level falls. What happens to the current in the fixed resistor?",
                       "It stays the same, because the voltage across it is unchanged.",
                       [("It increases, because the LDR branch takes less current.", "Parallel branches each have the supply voltage; the resistor's current doesn't change (course report 2024)."),
                        ("It decreases, because the LDR's resistance increases.", "Only the LDR branch current decreases."),
                        ("It becomes zero.", "The resistor still has the supply voltage across it.")], "Circuit Rules", level)
        return with_diagram(qobj, loop_circuit([par([comp("ldr", "LDR")], [comp("resistor")])]))
    qobj = _choice("Which is an advantage of connecting spotlights in parallel rather than in series?",
                   "Each spotlight operates at the correct (supply) voltage, and if one fails the others stay on.",
                   [("They all have the same voltage.", "Must say they operate at the CORRECT voltage (course report 2025)."),
                    ("The current is the same in each spotlight.", "That is a property of series circuits."),
                    ("The total resistance is higher, so less current is drawn.", "The total resistance in parallel is lower.")], "Circuit Rules", level)
    return with_diagram(qobj, loop_circuit([par([comp("lamp")], [comp("lamp")], [comp("lamp")])]))


# ════════════════ Which branch? and resistance of a wire ════════════════
_BRANCH_SETS = [(5.0, 10, 20, 12), (6.0, 12, 24, 9.0), (10, 20, 40, 6.0), (4.0, 8.0, 16, 12), (20, 30, 60, 9.0), (15, 30, 45, 6.0)]


def gen_ec_parallel_compare(level="N5"):
    """Three resistors in parallel: which has the largest current (smallest R) or the largest voltage (all equal)."""
    rs = list(random.choice(_BRANCH_SETS))
    V = rs.pop()
    random.shuffle(rs)
    labels = [f"{r:g} Ω" for r in rs]
    small, large = min(rs), max(rs)
    diagram = loop_circuit([par(*[[comp("resistor", lab)] for lab in labels])], supply_label=f"{V:g} V")
    names = f"{labels[0]}, {labels[1]} and {labels[2]}"
    variant = random.choice(["current", "voltage", "series_voltage"])
    if variant == "series_voltage":
        text = f"Three resistors of {names} are connected in series across a {V:g} V supply. Which resistor has the largest voltage across it, and why?"
        mid = [r for r in rs if r not in (small, large)][0]
        qobj = _choice(text, f"The {large:g} Ω resistor, because the current is the same in each resistor so the largest resistance has the largest voltage.",
                       [(f"The {small:g} Ω resistor, because it has the smallest resistance.", "In series the current is the same, so V = IR gives the largest voltage across the largest resistance."),
                        ("They all have the same voltage, because the current is the same through each resistor.", "The current is the same, but V = IR, so resistors of different sizes have different voltages."),
                        (f"The {mid:g} Ω resistor, because it is in the middle of the circuit.", "Compare the resistances: with the same current, the largest R has the largest V.")],
                       "Circuit Rules", level)
        return with_diagram(qobj, loop_circuit([comp("resistor", lab) for lab in labels], supply_label=f"{V:g} V"))
    if variant == "current":
        text = (f"Three resistors of {names} are connected in three parallel branches across a {V:g} V supply. "
                "Which resistor has the largest current in it, and why?")
        mid = [r for r in rs if r not in (small, large)][0]
        qobj = _choice(text, f"The {small:g} Ω resistor, because each branch has the same voltage so the smallest resistance has the largest current.",
                       [(f"The {large:g} Ω resistor, because it has the largest resistance.", "A larger resistance means a SMALLER current for the same voltage (I = V ÷ R)."),
                        (f"The {mid:g} Ω resistor, because it is in the middle of the circuit.", "Compare the resistances: the voltage across every branch is the same, so the smallest R has the largest I."),
                        ("They all have the same current, because the voltage is the same across each branch.", "The voltage is the same, but I = V ÷ R, so branches with different resistances have different currents.")],
                       "Circuit Rules", level)
    else:
        text = (f"Three resistors of {names} are connected in three parallel branches across a {V:g} V supply. "
                "Which resistor has the largest voltage across it, and why?")
        qobj = _choice(text, f"None of them: each has {V:g} V across it, because the voltage is the same across every branch of a parallel circuit.",
                       [(f"The {large:g} Ω resistor, because it has the largest resistance.", "In parallel every branch has the full supply voltage, whatever its resistance."),
                        (f"The {small:g} Ω resistor, because it has the largest current.", "The current differs between branches but the voltage is the same across each."),
                        (f"The {V:g} V is shared out between them, so the largest resistor gets the most.", "That is the series rule. In parallel every branch has the full supply voltage.")],
                       "Circuit Rules", level)
    return with_diagram(qobj, diagram)


# (cross-sectional areas in mm², lengths in m)
_WIRE_AREAS = [0.25, 0.50, 1.0, 2.0]
_WIRE_LENGTHS = [0.5, 1.0, 2.0, 4.0]


def gen_ec_wire_compare(level="N5"):
    """Four wires of the same material: which has the greatest (or smallest) resistance."""
    while True:
        combos = random.sample([(L, A) for L in _WIRE_LENGTHS for A in _WIRE_AREAS], 4)
        ratios = [L / A for L, A in combos]
        if len(set(ratios)) == 4 and sorted(ratios)[-1] / sorted(ratios)[-2] > 1.3 and sorted(ratios)[1] / sorted(ratios)[0] > 1.3:
            break
    greatest = random.random() < 0.5
    names = "ABCD"
    lines = "\n".join(f"- Wire {n}: length {L:g} m, cross-sectional area {A:g} mm²" for n, (L, A) in zip(names, combos))
    target = max(ratios) if greatest else min(ratios)
    ti = ratios.index(target)
    word = "greatest" if greatest else "smallest"
    text = f"Four wires are made from the same material.\n\n{lines}\n\nWhich wire has the {word} resistance?"
    wrong = []
    for i, (n, (L, A)) in enumerate(zip(names, combos)):
        if i == ti:
            continue
        longest, thinnest = L == max(c[0] for c in combos), A == min(c[1] for c in combos)
        if greatest:
            why = ("Resistance depends on BOTH length and thickness: a longer wire has more resistance, a thicker wire has less."
                   if (longest or thinnest) else "A shorter or thicker wire has less resistance.")
        else:
            why = ("Resistance depends on BOTH length and thickness: a shorter wire has less resistance, a thicker wire has less."
                   if (L == min(c[0] for c in combos) or A == max(c[1] for c in combos)) else "A longer or thinner wire has more resistance.")
        wrong.append((f"Wire {n}", why))
    return _choice(text, f"Wire {names[ti]}", wrong, "Resistance of a Wire", level)


def gen_ec_wire_explain(level="N5"):
    kind = random.choice(["length", "area", "temperature", "cable", "factors"])
    if kind == "length":
        return _choice("A longer wire of the same material and thickness replaces a shorter one. What happens to the resistance?",
                       "It increases.", [("It decreases.", "Longer wire, more resistance."), ("It stays the same.", "Length is one of the factors that affects the resistance of a wire.")],
                       "Resistance of a Wire", level)
    if kind == "area":
        return _choice("A thicker wire of the same material and length replaces a thinner one. What happens to the resistance?",
                       "It decreases, because the larger cross-sectional area gives charge more room to flow.",
                       [("It increases, because there is more wire.", "A thicker wire has a SMALLER resistance."),
                        ("It stays the same, because the material is the same.", "Cross-sectional area is one of the factors that affects the resistance of a wire.")],
                       "Resistance of a Wire", level)
    if kind == "temperature":
        return _choice("The temperature of a metal wire increases. What happens to the resistance of the wire?",
                       "It increases.", [("It decreases.", "A metal wire's resistance increases as its temperature increases."), ("It stays the same.", "Temperature is one of the factors that affects the resistance of a wire.")],
                       "Resistance of a Wire", level)
    if kind == "cable":
        return _choice("The cable to an electric cooker is made from thick copper wire rather than thin copper wire. Why?",
                       "A thicker wire has a smaller resistance, so less energy is transferred as heat in the cable.",
                       [("A thicker wire has a greater resistance, so more current flows.", "A thicker wire has a SMALLER resistance."),
                        ("A thicker wire is stronger, so it does not break.", "The reason is electrical: a smaller resistance means less heating in the cable."),
                        ("A thicker wire has a smaller resistance, so the voltage is greater.", "Lower resistance means less heat in the cable; it does not increase the voltage.")],
                       "Resistance of a Wire", level)
    return _choice("Which of these are factors that affect the resistance of a metal wire?",
                   "Length, cross-sectional area and temperature.",
                   [("Length and colour.", "Colour has no effect on resistance."), ("Cross-sectional area and the voltage across it.", "Voltage is not a property of the wire."),
                    ("Temperature and current only.", "Length and cross-sectional area also affect the resistance.")],
                   "Resistance of a Wire", level)


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
    qobj = _q(text, _sig(R), "Ω", opts, "LEDs and Transistor Switches", scaffold, level)
    return with_diagram(qobj, loop_circuit([comp("led") for _ in range(n)] + [comp("resistor", "R")], supply_label=f"{vs:g} V"))


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
    i_ma = vs / (r1 + r2)
    work = [_L(rf"R_T = {r1:g} + {r2:g} = {_ltx(r1 + r2)}\ \mathrm{{k\Omega}}"), _L(r"V = IR"),
            _L(rf"{vs:g} = I \times {_ltx(r1 + r2)} \Rightarrow I = {_ltx(i_ma)}\ \mathrm{{mA}}"),
            _L(rf"V_2 = {_ltx(i_ma)} \times {r2:g} = {_ltx(v2)}\ \mathrm{{V}}"), _T(f"{_txt(v2)} V is {'at least' if on == 'ON' else 'less than'} {vsw} V, so the transistor is {on.lower()}.")]
    opts = [{"value": _sig(v2), "mistake": None, "working": work},
            {"value": _sig(r1 / (r1 + r2) * vs), "mistake": "That's the voltage across the variable resistor — the current must be used with the sensor's resistance.", "working": work},
            {"value": _sig(r2 / r1 * vs), "mistake": "The supply voltage goes with the TOTAL resistance R₁ + R₂ when finding the current.", "working": work},
            {"value": _sig(vs / (r1 + r2)), "mistake": "That is the current in mA — now use V = IR again with the sensor's resistance to find the voltage.", "working": work},
            {"value": _sig(vs * r2 / (r1 + r2) + vsw), "mistake": "The switching voltage isn't part of the calculation — it's only compared with your answer.", "working": work}]
    scaffold = [{"question": "What is the total resistance, in kΩ?", "answer": _sig(r1 + r2)},
                {"question": "What is the current in the circuit, in mA?", "answer": _sig(i_ma)},
                {"question": f"What is the voltage across the {sensor}, in V?", "answer": _sig(v2)}]
    qobj = _q(text, _sig(v2), "V", opts, "LEDs and Transistor Switches", scaffold, level)
    return with_diagram(qobj, divider("variable", f"{r1:g} kΩ", "ldr" if sensor == "LDR" else "thermistor", f"{sensor} ({r2:g} kΩ)", f"+{vs:g} V", transistor="npn" if vsw == 0.7 else "mosfet", output_kind="lamp"))


def _a(word):
    return 'An' if word[0] in 'AEIOUL' and word != 'LED' or word == 'LDR' else 'A'


def gen_ec_sensor_voltage(level="N5"):
    """LURVD / TURVD: how the voltages in a sensor potential divider change (MCQ with the circuit drawn)."""
    sensor = random.choice(["LDR", "thermistor"])
    quantity = "light level" if sensor == "LDR" else "temperature"
    up = random.choice([True, False])                      # does the physical quantity increase?
    sensor_top = random.choice([True, False])
    about_sensor = random.choice([True, False])
    r_up = not up                                          # LURVD / TURVD: quantity up -> resistance down
    sensor_v_up = r_up
    answer_up = sensor_v_up if about_sensor else not sensor_v_up
    target = f"the {sensor}" if about_sensor else "the fixed resistor"
    mn = "LURVD" if sensor == "LDR" else "TURVD"
    text = (f"{_a(sensor)} {sensor} and a fixed resistor form a potential divider across a 5.0 V supply. {"The light level on the LDR" if sensor == "LDR" else "The temperature of the thermistor"} "
            f"{'increases' if up else 'decreases'}. What happens to the voltage across {target}?")
    why = (f"{mn}: when the {quantity} {'increases' if up else 'decreases'} the resistance of the {sensor} {'decreases' if not r_up else 'increases'}, "
           f"so the voltage across the {sensor} {'decreases' if not sensor_v_up else 'increases'}"
           + ("." if about_sensor else "; the voltages add up to the supply voltage, so the voltage across the fixed resistor changes the opposite way."))
    right, wrong = ("It increases.", "It decreases.") if answer_up else ("It decreases.", "It increases.")
    qobj = _choice(text, right,
                   [(wrong, why if about_sensor else why + " You may have used the sensor's change for the other component."),
                    ("It stays the same.", "The supply voltage is shared between the two components, so each voltage changes when a resistance changes.")],
                   "LEDs and Transistor Switches", level)
    top, bottom = (("ldr" if sensor == "LDR" else "thermistor", sensor), ("resistor", "fixed resistor")) if sensor_top else \
                  (("resistor", "fixed resistor"), ("ldr" if sensor == "LDR" else "thermistor", sensor))
    return with_diagram(qobj, divider(top[0], top[1], bottom[0], bottom[1], "+5.0 V"))


def gen_ec_transistor_explain(level="N5", sensor_top=None):
    """Four-step explanation (sensor voltage -> voltage across the transistor -> transistor on -> device on), sensor at the top or bottom."""
    sensor = random.choice(["LDR", "thermistor"])
    if sensor_top is None:
        sensor_top = random.choice([True, False])
    device = random.choice(["a lamp", "a motor", "a heater"] if sensor == "thermistor" else ["a lamp", "a motor"])
    # the MOSFET is across the BOTTOM component: sensor at the bottom -> on when its resistance rises; at the top -> on when it falls
    r_up = not sensor_top
    if sensor == "LDR":
        condition, quantity, mn = ("it gets dark" if r_up else "it gets light"), "light level", "LURVD"
        q_dir = "decreases" if r_up else "increases"
    else:
        condition, quantity, mn = ("it gets cold" if r_up else "it gets warm"), "temperature", "TURVD"
        q_dir = "decreases" if r_up else "increases"
    r_word, r_opp = ("increases", "decreases") if r_up else ("decreases", "increases")
    sv_word = r_word                                       # voltage across the sensor changes the same way as its resistance
    gate_comp = "the fixed resistor" if sensor_top else f"the {sensor}"
    stem = (f"{_a(sensor)} {sensor} ({'top' if sensor_top else 'bottom'}) and a fixed resistor ({'bottom' if sensor_top else 'top'}) form a potential divider. "
            f"A MOSFET's gate is connected across {gate_comp}, and the MOSFET switches on {device}. Which explanation of how {device} switches on when {condition} is best?")
    steps = (f"The {quantity} {q_dir}, so the resistance of the {sensor} {r_word} and the voltage across the {sensor} {sv_word} ({mn}). "
             + (f"The voltage across the fixed resistor, in parallel with the MOSFET, increases. " if sensor_top else f"The {sensor} is in parallel with the MOSFET, so the voltage across the MOSFET increases. ")
             + f"At the switching voltage the MOSFET switches on, so {device} in series with it switches on.")
    wrong = [(f"The {sensor} lets less current through, so more current goes to the MOSFET and it switches on {device}.",
              "Transistor circuits must be explained in terms of resistance and VOLTAGE, not current (course reports 2024 and 2025)."),
             (f"The {quantity} {q_dir}, so the resistance of the {sensor} {r_opp} and the voltage across the {sensor} {r_opp}. "
              f"The MOSFET reaches its switching voltage and switches on {device}.",
              f"When {condition}, the resistance of the {sensor} {r_word.upper()}."),
             (f"The {quantity} {q_dir}, so the resistance of the {sensor} {r_word}. The MOSFET switches on {device}.",
              "The link through the VOLTAGES — the voltage across the sensor, then the voltage across the MOSFET reaching its switching voltage — is missing."),
             (f"The {quantity} {q_dir}, so the resistance of the {sensor} {r_word} and the voltage across the {sensor} {sv_word}. "
              + (f"The voltage across the fixed resistor also decreases. " if sensor_top else f"The voltage across the fixed resistor increases. ")
              + f"The MOSFET switches on {device}.",
              "The voltages in a potential divider change in opposite directions (they add up to the supply voltage); the MOSFET is across "
              + ("the fixed resistor, whose voltage goes the OPPOSITE way to the sensor's." if sensor_top else f"the {sensor}, so it is the {sensor}'s voltage that matters."))]
    qobj = _choice(stem, steps, wrong, "LEDs and Transistor Switches", level)
    top, bottom = (("ldr" if sensor == "LDR" else "thermistor", sensor), ("resistor", "")) if sensor_top else (("resistor", ""), ("ldr" if sensor == "LDR" else "thermistor", sensor))
    return with_diagram(qobj, divider(top[0], top[1], bottom[0], bottom[1], transistor="mosfet",
                                      output_kind="lamp" if device == "a lamp" else ("motor" if device == "a motor" else "heater"), output_label=device[2:]))


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


_PIR_SYMBOL = {"heating element": "heater", "lamp filament": "lamp"}


def _pir_circuit(el):
    return loop_circuit([comp("ammeter"), comp(_PIR_SYMBOL.get(el, "resistor"), el, voltmeter="V")])


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
        qobj = _q(text, _sig(P), "W", opts, "Power and Fuses", scaffold, level)
        return with_diagram(qobj, _pir_circuit(el))
    V = random.choice([6.0, 12.0, 24.0, 230.0])
    R = random.randint(rlo, rhi) * (20 if V == 230 else 1)
    P = V * V / R
    text = f"A {V:g} V supply is connected across a {R} Ω {el}. Calculate the power developed."
    work = [_L(r"P = \frac{V^2}{R}"), _L(rf"P = \frac{{{V:g}^2}}{{{R}}}"), _L(rf"P = {_ltx(P)}\ \mathrm{{W}}")]
    opts = [{"value": _sig(P), "mistake": None, "working": work},
            {"value": _sig(V / R), "mistake": "That's the current (V ÷ R) — the voltage must be squared for the power.", "working": work},
            {"value": _sig(V * V * R), "mistake": "P = V² ÷ R — divide by R.", "working": work}]
    qobj = _q(text, _sig(P), "W", opts, "Power and Fuses", None, level)
    return with_diagram(qobj, _pir_circuit(el))


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


def gen_ec_transistor_explain_bottom(level="N5"):
    return gen_ec_transistor_explain(level, sensor_top=False)


def gen_ec_transistor_explain_top(level="N5"):
    return gen_ec_transistor_explain(level, sensor_top=True)
