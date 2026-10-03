"""N5 Radiation — exam-style questions that cut across the unit's topics, like SQA paper questions: dose, half-life and activity.

Recognised wrong answers follow the N5 marking instructions and course reports: the radiation
weighting factor left out or divided by, minutes not converted for activity, the number of
half-lives miscounted (e.g. halving the time instead of the activity), and the background count
rate not subtracted.
"""
import math
import random

from topics.exam_style.base import Exam, T, fmt, graph, ltx, pick, sig

UNIT = "Radiation"
W_R = {"alpha particles": 20, "fast neutrons": 10, "slow neutrons": 3, "beta particles": 1, "gamma rays": 1}

NOTES = {
    "Dose": r"""## Dose — exam technique

$D = \frac{E}{m}$ (Gy) &nbsp; $H = Dw_R$ (Sv) &nbsp; $\dot{H} = \frac{H}{t}$

- Radiation weighting factors: alpha 20, fast neutrons 10, slow neutrons 3, beta 1, gamma 1.
- Equivalent dose $H$ takes account of the **type** of radiation (and so the biological effect).
- Annual effective dose limits: 1 mSv for a member of the public; 20 mSv for a radiation worker. Average UK background ≈ 2.2 mSv per year.
""",
    "Half-Life": r"""## Half-life — exam technique

**Half-life** is the time taken for the **activity** (or the number of unstable nuclei) to fall to **half** its original value.

- Halve the activity repeatedly: count the number of halvings, then × half-life.
- Subtract the **background** count rate before finding a half-life from measurements.
- A medical tracer: gamma (penetrates the body to reach the detector) with a **short** half-life (low dose to the patient).
""",
    "Activity": r"""## Activity — exam technique

$A = \frac{N}{t}$ — activity in becquerels (Bq): **1 Bq = 1 decay per second**. Time in **seconds**.

- kBq = × 10³, MBq = × 10⁶.
- Alpha: most ionising, stopped by paper. Beta: stopped by a few mm of aluminium. Gamma: reduced by thick lead / concrete.
""",
}

NOTES["Nuclear Radiation and Dosimetry"] = r"""## Radiation and dose — exam technique

$D = \frac{E}{m}$ &nbsp; $H = Dw_R$ &nbsp; $\dot{H} = \frac{H}{t}$ — weight **each** absorbed dose separately; keep the time in hours for a rate per hour.

- Ionisation: an atom gains or loses an **electron**. Beta: a fast electron **from the nucleus**.
- Explain absorption using the materials **in the question** (soil, packaging, air in a detector).
- Uses of nuclear **radiation**: tracers, sterilising, smoke detectors, gauges, treating cancer.
"""
NOTES["Half-Life, Fission and Fusion"] = r"""## Half-life, fission and fusion — exam technique

$A = \frac{N}{t}$ (t in s) &nbsp; $P = \frac{E}{t}$

- Half-life: time for the **activity** to halve — show the halving.
- Fission: a large **nucleus** splits; **neutrons** released split further nuclei (chain reaction).
- Fusion: two small nuclei join; needs very high temperatures; plasma contained by magnetic fields.
"""


def _ex(level):
    return Exam(UNIT, level, NOTES)


# ════════════════ Medical tracer: activity → half-life → dose ════════════════

def medical_tracer(level="N5"):
    ex = _ex(level)
    A_M, th = pick(80, 120, 160, 400), pick(6, 8, 13)
    ex.on("Activity").num(f"The tracer has an activity of {A_M} MBq. Calculate the number of nuclei that decay in 1 minute.",
        A_M * 1e6 * 60, "",
        wrong=[(A_M * 60, "Convert MBq to Bq (× 10⁶)."), (A_M * 1e6, "Multiply by the time in seconds (60 s).")],
        working=[rf"N = At = {A_M} \times 10^6 \times 60 = {ltx(A_M * 1e6 * 60)}"])
    n = pick(3, 4)
    ex.on("Half-Life").num(f"The tracer has a half-life of {th} hours. Calculate its activity {n * th} hours after it is prepared.",
        A_M * 0.5 ** n, "MBq",
        wrong=[(A_M / n, "Halve once for EACH half-life."), (A_M * 0.5 ** (n - 1), f"{n * th} hours is {n} half-lives.")],
        working=[rf"\frac{{{n * th}}}{{{th}}} = {n}\ \text{{half-lives}}",
                 rf"{A_M} \to " + r" \to ".join(f"{A_M * 0.5 ** k:g}" for k in range(1, n + 1)) + r"\ \text{MBq}"],
        scaffold=[("Number of half-lives?", n, "")])
    E_mJ, m = pick(0.6, 1.2, 1.8, 2.4), pick(60, 70, 80)
    D = E_mJ / 1000 / m
    ex.on("Dose").num(f"The patient, of mass {m} kg, absorbs {E_mJ:g} mJ of energy from the tracer. Calculate the absorbed dose.", D, "Gy",
        wrong=[(E_mJ / m, "Convert mJ to J."), (E_mJ / 1000 * m, "D = E ÷ m.")],
        working=[rf"D = \frac{{E}}{{m}} = \frac{{{E_mJ / 1000:g}}}{{{m}}} = {ltx(D)}\ \text{{Gy}}"])
    ex.on("Dose").num("The tracer emits gamma rays (weighting factor 1). Calculate the equivalent dose.", D, "Sv",
        wrong=[(D * 20, "Gamma has a weighting factor of 1 — 20 is for alpha.")],
        working=[rf"H = Dw_R = {ltx(D)} \times 1 = {ltx(D)}\ \text{{Sv}}"])
    ex.on("Half-Life").choice("Why is a gamma source with a short half-life chosen as a tracer?",
        "Gamma passes out of the body to the detector, and a short half-life means the patient's dose is low.",
        [("Alpha would be better because it is detected more easily.", "Alpha can't leave the body and is highly ionising."),
         ("A long half-life keeps the tracer working for years.", "That would give the patient a large dose."),
         ("Gamma is the most ionising radiation.", "Gamma is the LEAST ionising.")])
    return ex.build(f"A hospital uses a radioactive tracer to image a patient's organ.")


# ════════════════ Nuclear worker: dose rate → annual dose → source decay ════════════════

def nuclear_worker(level="N5"):
    ex = _ex(level)
    rate, hrs, weeks = pick(2.0, 3.0, 4.0, 5.0, 8.0), pick(20, 25, 30, 35), pick(44, 46, 48)
    Hw = rate * hrs / 1000
    ex.on("Dose").num(f"The equivalent dose rate at her workstation is {rate:g} μSv/h. She works there {hrs} hours a week. "
        f"Calculate her equivalent dose each week, in mSv.", Hw, "mSv",
        wrong=[(rate * hrs, "Convert μSv to mSv (÷ 1000)."), (rate / hrs / 1000, "H = Ḣ × t.")],
        working=[rf"H = \dot{{H}}t = {rate:g} \times {hrs} = {rate * hrs:g}\ \mu\text{{Sv}} = {ltx(Hw)}\ \text{{mSv}}"])
    Hy = sig(Hw) * weeks
    ex.on("Dose").num(f"She works {weeks} weeks a year. Calculate her annual equivalent dose from work, in mSv.", Hy, "mSv",
        wrong=[(sig(Hw) * 52, f"She works {weeks} weeks, not 52.")], working=[rf"H = {ltx(Hw)} \times {weeks} = {ltx(Hy)}\ \text{{mSv}}"])
    ok = Hy < 20
    ex.on("Dose").choice("The annual limit for a radiation worker is 20 mSv. Is she within it?",
        f"{'Yes' if ok else 'No'} — {fmt(Hy)} mSv is {'less' if ok else 'more'} than 20 mSv.",
        [(f"{'No' if ok else 'Yes'} — {fmt(Hy)} mSv is {'more' if ok else 'less'} than 20 mSv.", "Compare the annual dose with 20 mSv.")])
    A0, th = pick(800, 960, 1600), pick(5, 6, 8)
    n = pick(2, 3, 4)
    ex.on("Half-Life").num(f"The source she works with had an activity of {A0} kBq. Its half-life is {th} years. Calculate its activity after {n * th} years.",
        A0 * 0.5 ** n, "kBq",
        wrong=[(A0 / n, "Halve once for each half-life."), (A0 * 0.5 ** (n + 1), f"{n * th} years is {n} half-lives.")],
        working=[rf"{n}\ \text{{half-lives}}: {A0} \to " + r" \to ".join(f"{A0 * 0.5 ** k:g}" for k in range(1, n + 1))])
    A = A0 * 0.5 ** n * 1000
    ex.on("Activity").num("Calculate the number of decays in one minute at this activity.", A * 60, "",
        wrong=[(A0 * 0.5 ** n * 60, "Convert kBq to Bq."), (A, "Multiply by the time (60 s).")],
        working=[rf"N = At = {fmt(A)} \times 60 = {ltx(A * 60)}"])
    ex.on("Dose").choice("Which is a sensible way for her to reduce her dose?",
        "Spend less time near the source, keep further away from it, and use shielding.",
        [("Stand closer for a shorter time.", "Closer increases the dose rate."), ("Wear sunglasses.", "These don't stop ionising radiation."),
         ("Work longer hours less often.", "Total time is what matters.")])
    return ex.build("A technician works with radioactive sources at a power station.")


# ════════════════ School experiment: half-life graph → background → activity ════════════════

def school_experiment(level="N5"):
    ex = _ex(level)
    C0, th = pick(640, 800, 960, 1280), pick(2, 3, 4, 5)
    pts = [(t / 10, C0 * 0.5 ** (t / 10 / th)) for t in range(0, th * 10 * 4 + 1)]
    fig = graph(pts, xlabel="Time (minutes)", ylabel="Corrected count rate (counts per minute)", smooth=True)
    ex.on("Half-Life").num("Use the graph to find the half-life of the source, in minutes.", th, "",
        wrong=[(2 * th, "Read the time for ONE halving."), (th / 2, f"Read when the count rate is {C0 // 2} counts per minute.")],
        working=[T(f"Count rate falls from {C0} to {C0 // 2} counts per minute in {th} minutes.")])
    bg = pick(20, 24, 30)
    ex.on("Half-Life").num(f"The background count rate is {bg} counts per minute. What count rate did the counter actually record at t = 0?",
        C0 + bg, "", wrong=[(C0 - bg, "The counter records the background too — ADD it."), (C0, "Add the background.")],
        working=[rf"{C0} + {bg} = {C0 + bg}"])
    ex.on("Activity").num(f"The counter records {C0} counts in one minute (after correction). Calculate the corrected count rate in counts per second.",
        C0 / 60, "", wrong=[(C0 * 60, "Divide by 60 s."), (C0, "Convert to per second.")],
        working=[rf"\frac{{{C0}}}{{60}} = {ltx(C0 / 60)}\ \text{{counts per second}}"])
    ex.on("Definitions").choice("A sheet of paper between the source and the counter makes no difference, but 3 mm of aluminium reduces the count rate to background. "
        "Which radiation is emitted?", "Beta",
        [("Alpha", "Alpha would be stopped by the paper."), ("Gamma", "Gamma passes through 3 mm of aluminium."),
         ("Alpha and gamma", "Paper made no difference, so no alpha; aluminium stopped it all, so no gamma.")])
    return ex.build("Pupils measure the count rate from a radioactive source over time. The graph shows the corrected count rate.", figure=fig)


# ════════════════ Mask steriliser: gamma source → half-life → dose → energy ════════════════

def steriliser(level="N5"):
    ex = _ex(level)
    A0, th, n = pick(848000, 640000, 960000), pick(5.3, 5.2), pick(2, 3, 4)
    A = A0 / 2 ** n
    ex.on("Half-Life, Fission and Fusion").num(f"The cobalt-60 source has an activity of {A0} GBq. Its half-life is {th:g} years. Determine its activity {fmt(n * th)} years later, in GBq.",
        A, "GBq", wrong=[(A0 / n, "Halve repeatedly — don't divide by the number of half-lives."), (A0 / 2, "That is after one half-life.")],
        working=[rf"\text{{half-lives}} = \frac{{{fmt(n * th)}}}{{{th:g}}} = {n}", rf"{A0} \to " + r" \to ".join(f"{A0 / 2 ** k:g}" for k in range(1, n + 1))])
    Dtot, rate = pick(25000, 30000), pick(0.50, 0.25)
    ex.on("Nuclear Radiation and Dosimetry").num(f"Each mask must receive an absorbed dose of {Dtot // 1000} kGy. The steriliser gives {rate:g} Gy each second. Determine the time needed.",
        Dtot / rate, "s", wrong=[(Dtot / 1000 / rate, "Convert kGy to Gy."), (Dtot * rate, "time = dose ÷ dose per second.")],
        working=[rf"t = \frac{{{Dtot}}}{{{rate:g}}} = {fmt(Dtot / rate)}\ \text{{s}}"])
    m = pick(2.2e-3, 3.0e-3, 4.0e-3)
    E = Dtot * m
    ex.on("Nuclear Radiation and Dosimetry").num(f"Each mask has a mass of {fmt(m)} kg. Calculate the energy absorbed by each mask.", E, "J",
        wrong=[(Dtot / 1000 * m, "Convert kGy to Gy."), (Dtot / m, "E = D × m.")],
        working=[r"D = \frac{E}{m}", rf"E = {Dtot} \times {ltx(m)} = {fmt(E)}\ \text{{J}}"])
    ex.on("Nuclear Radiation and Dosimetry").choice("Why is gamma radiation used to sterilise masks sealed in plastic packages?",
        "Gamma passes through the plastic packaging and kills the bacteria inside.",
        [("Gamma is the most ionising radiation.", "Gamma is the LEAST ionising — it's chosen because it penetrates the packaging."),
         ("Gamma makes the masks radioactive.", "Irradiation does not make them radioactive."), ("Alpha would pass through the packaging too.", "Alpha is stopped by the plastic.")])
    return ex.build("Medical face masks are sterilised by gamma radiation from a cobalt-60 source in a shielded steriliser.")


# ════════════════ Icebreaker reactor: fission → number of fissions → chain reaction → fusion ════════════════

def icebreaker(level="N5"):
    ex = _ex(level)
    ex.on("Half-Life, Fission and Fusion").choice("The ship's reactor uses nuclear fission. What is nuclear fission?",
        "A large nucleus splits into smaller nuclei, releasing energy and neutrons.",
        [("A large atom splits into smaller atoms.", "Use ‘nucleus’ not ‘atom’ (course report 2022)."), ("Two small nuclei join together.", "That's fusion."),
         ("An atom loses electrons.", "That's ionisation.")])
    P, e = pick(150, 100, 200), pick(2.9e-11, 3.2e-11)
    E = P * 1e6 * 3600
    ex.on("Half-Life, Fission and Fusion").num(f"The reactor's power output is {P} MW. Calculate the energy produced in one hour.", E, "J",
        wrong=[(P * 3600, "Convert MW to W."), (P * 1e6 * 60, "One hour = 3600 s.")], working=[r"P = \frac{E}{t}", rf"E = {P}\times10^6 \times 3600 = {ltx(E)}\ \text{{J}}"])
    ex.on("Half-Life, Fission and Fusion").num(f"Each fission releases {fmt(e)} J. Determine the minimum number of fissions each hour.", sig(E) / e, "",
        wrong=[(P * 1e6 / e, "That's per second — the question asks per hour (course report 2022)."), (e * sig(E), "Divide the energy by the energy per fission.")],
        working=[rf"N = \frac{{{ltx(E)}}}{{{ltx(e)}}} = {ltx(sig(E) / e)}"])
    ex.on("Half-Life, Fission and Fusion").choice("How does one fission keep the reactor running?", "Neutrons released go on to split further nuclei — a chain reaction.",
        [("The same nucleus keeps splitting.", "Different nuclei (course report 2024)."), ("Electrons released split more nuclei.", "Neutrons."),
         ("The neutrons split into smaller neutrons.", "Neutrons are released, not split.")])
    ex.on("Nuclear Radiation and Dosimetry").num("A crew member receives 2.2 µGy from slow neutrons and 3.4 µGy from gamma rays in a shift. Calculate the total equivalent dose, in µSv.",
        2.2 * 3 + 3.4, "µSv", wrong=[(5.6, "Weight each absorbed dose (slow neutrons × 3)."), (5.6 * 3, "Weight EACH dose separately.")],
        working=[r"H = Dw_R", r"H = 2.2 \times 3 + 3.4 \times 1 = 10\ \mu\text{Sv}"])
    return ex.build("A nuclear-powered icebreaker ship uses electricity generated from nuclear fission to drive its engines.")


# ════════════════ Pipe leak: tracer choice → half-life → activity → dose rate ════════════════

def pipe_leak(level="N5"):
    ex = _ex(level)
    ex.on("Nuclear Radiation and Dosimetry").choice("A tracer is added to water in a pipe buried under tarmac, crushed rock and earth. Why must it emit gamma radiation?",
        "Alpha and beta would be absorbed by the tarmac, rock and earth, so would not reach the detector.",
        [("Gamma is the most penetrating radiation.", "Refer to the materials in this situation (course report 2025)."),
         ("Gamma is the most ionising.", "Gamma is the least ionising."), ("Gamma has the shortest half-life.", "Half-life depends on the source.")])
    ex.on("Half-Life, Fission and Fusion").choice("Which source is most suitable? Sodium-24 (15 h, beta and gamma); bismuth-204 (11 h, beta only); barium-133 (10 years, gamma); barium-137m (2.6 min, gamma)",
        "sodium-24", [("bismuth-204", "Beta only — absorbed by the ground."), ("barium-133", "Half-life far too long — stays active in the water."),
                      ("barium-137m", "Half-life too short — decays before the test is complete.")])
    A0, n = pick(12800, 6400, 3200), pick(2, 3)
    ex.on("Half-Life, Fission and Fusion").num(f"The tracer has an initial activity of {A0} Bq. Determine its activity {15 * n} hours later.", A0 / 2 ** n, "Bq",
        wrong=[(A0 / n, "Halve repeatedly."), (A0 / 2 ** (n + 1), "Count the half-lives: 15 h each.")],
        working=[rf"\text{{half-lives}} = {15 * n} \div 15 = {n}", rf"{A0} \to " + r" \to ".join(f"{A0 / 2 ** k:g}" for k in range(1, n + 1))])
    rate, mins = pick(2.0, 3.0, 4.5), pick(30, 45, 90)
    H = rate * mins / 60
    ex.on("Nuclear Radiation and Dosimetry").num(f"An engineer works near the pipe for {mins} minutes where the equivalent dose rate is {rate:g} µSv/h. Calculate the equivalent dose received, in µSv.",
        H, "µSv", wrong=[(rate * mins, "The rate is per HOUR — convert the time to hours."), (rate * mins * 60, "Keep the time in hours (course report 2023).")],
        working=[r"\dot{H} = \frac{H}{t}", rf"H = {rate:g} \times \frac{{{mins}}}{{60}} = {fmt(H)}\ \mu\text{{Sv}}"])
    return ex.build("Engineers use a radioactive tracer to find a leak in an underground wastewater pipe.")


SCENARIOS = {
    "Medical Tracer":    medical_tracer,
    "Nuclear Worker":    nuclear_worker,
    "School Experiment": school_experiment,
    "Mask Steriliser":   steriliser,
    "Icebreaker Reactor": icebreaker,
    "Pipe Leak":         pipe_leak,
}
