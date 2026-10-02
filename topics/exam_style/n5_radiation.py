"""N5 Radiation — exam-style multi-part questions: dose, half-life and activity.

Recognised wrong answers follow the N5 marking instructions and course reports: the radiation
weighting factor left out or divided by, minutes not converted for activity, the number of
half-lives miscounted (e.g. halving the time instead of the activity), and the background count
rate not subtracted.
"""
import math
import random

from topics.exam_style.base import Exam, T, exam_style, fmt, graph, ltx, pick, sig

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


def _ex(qtype, level):
    return Exam(UNIT, qtype, level, NOTES[qtype])


# ════════════════ Dose ════════════════

def _dose_tissue(level="N5"):
    ex = _ex("Dose", level)
    rad = pick("alpha particles", "fast neutrons", "slow neutrons", "gamma rays")
    w = W_R[rad]
    m = pick(0.05, 0.2, 0.5, 2.0, 5.0)
    E_mJ = pick(0.012, 0.025, 0.04, 0.06, 0.15)
    E = E_mJ / 1000
    D = E / m
    ex.num(f"The tissue absorbs {E_mJ:g} mJ of energy. Calculate the absorbed dose.", D, "Gy",
           wrong=[(E_mJ / m, "Convert mJ to J (÷ 1000)."), (E * m, "D = E ÷ m."), (m / E, "D = E ÷ m.")],
           working=[r"D = \frac{E}{m}", rf"D = \frac{{{ltx(E)}}}{{{m:g}}} = {ltx(D)}\ \text{{Gy}}"])
    H = D * w
    ex.num(f"Calculate the equivalent dose received by the tissue.", H, "Sv",
           wrong=[(D, f"Multiply by the radiation weighting factor for {rad} ({w})."), (D / w, "H = D × w_R."),
                  (D * 20 if w != 20 else D * 10, f"Use the weighting factor for {rad} ({w}).")] if w != 1 else
                 [(D * 20, "Gamma rays have a weighting factor of 1."), (D / 2, "H = D × w_R.")],
           working=[r"H = Dw_R", rf"H = {ltx(D)} \times {w} = {ltx(H)}\ \text{{Sv}}"])
    mins = pick(10, 20, 30, 40)
    Hdot = H / (mins / 60)
    ex.num(f"This dose was received in {mins} minutes. Calculate the equivalent dose rate in Sv per hour.", Hdot, "Sv/h",
           wrong=[(H / mins, "The rate is per HOUR: convert the time to hours."), (H * mins / 60, "Ḣ = H ÷ t.")],
           working=[r"\dot{H} = \frac{H}{t}", rf"\dot{{H}} = \frac{{{ltx(H)}}}{{{mins}/60}} = {ltx(Hdot)}\ \text{{Sv/h}}"])
    ex.choice("Why is the equivalent dose used rather than the absorbed dose to measure the risk of biological harm?",
              "It takes into account the type of radiation, since different radiations cause different amounts of harm for the same energy absorbed.",
              [("It is always larger than the absorbed dose.", "For beta and gamma they're equal — the point is the type of radiation."),
               ("It takes into account the mass of the tissue.", "The absorbed dose already does that."),
               ("It is measured over a longer time.", "Time is used in the dose RATE, not in H.")])
    return ex.build(f"In an experiment, a {m:g} kg sample of tissue is exposed to {rad} (radiation weighting factor = {w}).")


def _dose_worker(level="N5"):
    ex = _ex("Dose", level)
    rate_uSv = pick(2.0, 2.5, 3.0, 4.0, 5.0, 8.0)
    hrs = pick(20, 25, 30, 35)
    weeks = pick(40, 45, 46, 48)
    H_week = rate_uSv * hrs / 1000
    ex.num(f"The equivalent dose rate where she works is {rate_uSv:g} μSv per hour, and she works there for {hrs} hours each week. "
           f"Calculate her equivalent dose each week, in mSv.", H_week, "mSv",
           wrong=[(rate_uSv * hrs, "Convert μSv to mSv (÷ 1000)."), (rate_uSv / hrs / 1000, "H = Ḣ × t.")],
           working=[r"H = \dot{H}t", rf"H = {rate_uSv:g} \times {hrs} = {rate_uSv * hrs:g}\ \mu\text{{Sv}} = {ltx(H_week)}\ \text{{mSv}}"])
    H_year = H_week * weeks
    ex.num(f"She works {weeks} weeks each year. Calculate her annual equivalent dose from her work, in mSv.", H_year, "mSv",
           wrong=[(H_week * 52, f"She works {weeks} weeks, not 52."), (H_week, "Multiply by the number of weeks.")],
           working=[rf"H = {ltx(H_week)} \times {weeks} = {ltx(H_year)}\ \text{{mSv}}"])
    ok = H_year < 20
    ex.choice("The annual effective dose limit for a radiation worker is 20 mSv. Is she within the limit?",
              f"{'Yes' if ok else 'No'} — {fmt(H_year)} mSv is {'less' if ok else 'more'} than 20 mSv.",
              [(f"{'No' if ok else 'Yes'} — {fmt(H_year)} mSv is {'more' if ok else 'less'} than 20 mSv.", "Compare the annual dose with 20 mSv."),
               ("It can't be decided without the absorbed dose.", "The limit is given as an effective (equivalent) dose — compare directly.")])
    ex.choice("Which is a sensible way for her to reduce her equivalent dose?",
              "Spend less time near the source, increase her distance from it, and use shielding.",
              [("Wear sunglasses.", "Sunglasses don't shield ionising radiation."), ("Work faster for longer hours.", "More time means more dose."),
               ("Stand closer to the source for less time.", "Closer increases the dose rate.")])
    return ex.build("A radiographer works in a hospital department that uses radioactive sources.")


gen_dose_exam = exam_style(_dose_tissue, _dose_worker)


# ════════════════ Half-Life ════════════════

def _hl_graph(level="N5"):
    ex = _ex("Half-Life", level)
    A0 = pick(400, 640, 800, 1200, 1600)
    th = pick(2, 4, 5, 6, 8)
    tunit = pick("hours", "days", "minutes")
    pts = [(t / 10, A0 * 0.5 ** (t / 10 / th)) for t in range(0, th * 10 * 4 + 1)]
    fig = graph(pts, xlabel=f"Time ({tunit})", ylabel="Activity (kBq)", smooth=True)
    ex.num(f"Use the graph to find the half-life of the source, in {tunit}.", th, "",
           wrong=[(2 * th, f"Half-life is the time for the activity to fall from {A0} to {A0 // 2} kBq — just ONE halving."),
                  (th / 2, "Read the time when the activity is half its starting value.")],
           working=[T(f"Activity falls from {A0} kBq to {A0 / 2:g} kBq in {th} {tunit}."), T(f"Half-life = {th} {tunit}")])
    n = pick(5, 6)
    t_total = n * th
    A = A0 * 0.5 ** n
    ex.num(f"Calculate the activity of the source after {t_total} {tunit}.", A, "kBq",
           wrong=[(A0 / n, "Halve the activity once for EACH half-life."), (A0 * 0.5 ** (n - 1), f"{t_total} {tunit} is {n} half-lives."),
                  (A0 / (2 * n), "Halve repeatedly: ÷ 2 for each half-life.")],
           working=[rf"\text{{number of half-lives}} = \frac{{{t_total}}}{{{th}}} = {n}",
                    rf"{A0} \to " + r" \to ".join(f"{A0 * 0.5 ** k:g}" for k in range(1, n + 1)) + r"\ \text{kBq}"],
           scaffold=[("How many half-lives is this?", n, "")])
    ex.choice("A source used as a medical tracer inside the body should have which properties?",
              "It should emit gamma rays and have a short half-life.",
              [("It should emit alpha particles and have a long half-life.", "Alpha can't get out of the body and is very ionising; a long half-life gives a large dose."),
               ("It should emit gamma rays and have a long half-life.", "A long half-life keeps irradiating the patient."),
               ("It should emit beta particles and have a half-life of many years.", "Beta is absorbed in the body; and the half-life should be short.")])
    return ex.build("The graph shows how the activity of a radioactive source changes with time.", figure=fig)


def _hl_measured(level="N5"):
    ex = _ex("Half-Life", level)
    bg = pick(20, 24, 30, 36)
    C0 = pick(800, 960, 1280, 1600)
    n = pick(3, 4)
    th = pick(15, 20, 30, 45)
    t = n * th
    Cn = C0 * 0.5 ** n
    ex.num(f"The count rate from the source (after subtracting background) falls from {C0} counts per minute to {Cn:g} counts per minute in "
           f"{t} minutes. Calculate the half-life, in minutes.", th, "",
           wrong=[(t / 2, "Count the halvings: " + f"{C0} → … → {Cn:g} is {n} half-lives."), (t / (C0 / Cn), "Divide the time by the NUMBER of halvings, not the ratio."),
                  (t, "That's the total time for several half-lives.")],
           working=[rf"{C0} \to " + r" \to ".join(f"{C0 * 0.5 ** k:g}" for k in range(1, n + 1)), rf"{n}\ \text{{half-lives}} = {t}\ \text{{min}}",
                    rf"t_{{1/2}} = \frac{{{t}}}{{{n}}} = {th}\ \text{{min}}"],
           scaffold=[("How many half-lives?", n, "")])
    total = Cn + bg
    ex.num(f"The background count rate is {bg} counts per minute. What count rate did the detector actually record at {t} minutes?",
           total, "",
           wrong=[(Cn, "The detector also records the background — add it."), (Cn - bg, "ADD the background to the source's count rate.")],
           working=[rf"\text{{recorded}} = {Cn:g} + {bg} = {total:g}"])
    ex.choice("What is meant by the half-life of a radioactive source?",
              "The time taken for the activity to fall to half its original value.",
              [("Half the time it takes for the source to stop being radioactive.", "Activity never quite reaches zero."),
               ("The time taken for the mass of the source to halve.", "It's the activity (number of unstable nuclei) that halves."),
               ("The time for half the radiation to be absorbed.", "It's about the source's activity.")])
    return ex.build("Pupils measure how the count rate from a radioactive source changes over time.")


gen_half_life_exam = exam_style(_hl_graph, _hl_measured)


# ════════════════ Activity ════════════════

def _act_counts(level="N5"):
    ex = _ex("Activity", level)
    mins = pick(2, 5, 10)
    A = pick(150, 240, 400, 600, 1200)
    N = A * mins * 60
    ex.num(f"The source has {fmt(N)} decays in {mins} minutes. Calculate its activity.", A, "Bq",
           wrong=[(N / mins, "Convert minutes to seconds — activity is decays per SECOND."), (N * mins * 60, "A = N ÷ t.")],
           working=[r"A = \frac{N}{t}", rf"A = \frac{{{ltx(N)}}}{{{mins} \times 60}} = {ltx(A)}\ \text{{Bq}}"])
    hrs = pick(1, 2, 3)
    N2 = A * hrs * 3600
    ex.num(f"Assuming the activity stays constant, calculate the number of decays in {hrs} hour{'s' if hrs > 1 else ''}.", N2, "",
           wrong=[(A * hrs * 60, "1 hour = 3600 s."), (A * hrs, "Convert the time to seconds.")],
           working=[rf"N = At = {A} \times ({hrs} \times 3600) = {ltx(N2)}"])
    ex.choice("What is meant by an activity of 1 becquerel?", "One nucleus decays each second.",
              [("One nucleus decays each minute.", "Becquerel is per SECOND."), ("One joule of energy is absorbed per kilogram.", "That's a gray."),
               ("The source emits one gamma ray each hour.", "1 Bq = 1 decay per second.")])
    return ex.build("A pupil uses a Geiger-Müller tube and counter to investigate a radioactive source.")


def _act_alarm(level="N5"):
    ex = _ex("Activity", level)
    A_k = pick(30, 33, 37, 40)
    A = A_k * 1000
    ex.num(f"Calculate the number of nuclei that decay in the source in one day.", A * 86400, "",
           wrong=[(A_k * 86400, "Convert kBq to Bq (× 1000)."), (A * 24, "One day = 24 × 3600 s.")],
           working=[r"N = At", rf"N = {A_k} \times 10^3 \times (24 \times 3600) = {ltx(A * 86400)}"])
    t = pick(5, 10, 20)
    ex.num(f"Calculate the time, in seconds, for {fmt(A * t)} nuclei to decay.", t, "s",
           wrong=[(A * t / A_k, "Convert kBq to Bq."), (A / (A * t), "t = N ÷ A.")],
           working=[rf"t = \frac{{N}}{{A}} = \frac{{{ltx(A * t)}}}{{{ltx(A)}}} = {t}\ \text{{s}}"])
    ex.choice("Smoke alarms use an alpha source. Why is alpha radiation used?",
              "Alpha particles are strongly ionising and are absorbed by smoke particles, so smoke changes the current in the detector.",
              [("Alpha particles can pass through the walls of the house.", "Alpha is stopped by a sheet of paper."),
               ("Alpha particles are not ionising.", "Alpha is the MOST ionising."),
               ("Alpha particles have a long range in air.", "Alpha only travels a few cm in air.")])
    return ex.build(f"A smoke alarm contains a radioactive source with an activity of {A_k} kBq.")


gen_activity_exam = exam_style(_act_counts, _act_alarm)


EXAM = {
    "Dose":      gen_dose_exam,
    "Half-Life": gen_half_life_exam,
    "Activity":  gen_activity_exam,
}
