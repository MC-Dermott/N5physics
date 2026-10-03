"""N5 Radiation — exam-style question types from the past-paper/course-report worksheets.

Mirrors the two N5phys Radiation worksheets (Nuclear Radiation and Dosimetry; Half-Life, Fission
and Fusion). The older generators (dose, half_life, activity) drill one-step calculations; these add
the question styles SQA sets, with distractors that are the errors named in the N5 course reports
2015–2025 and marking instructions: µ/m prefixes not converted, each absorbed dose not weighted
separately, the equivalent dose used as the absorbed dose, time converted to seconds when the dose
rate is per hour, minutes or hours left in A = N/t, dividing by the number of half-lives instead of
halving, ionisation and fission described with ‘atoms’, penetration explained without the context's
materials, and chain reactions described as one nucleus splitting repeatedly.
"""
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

TOPIC = "Radiation"
DOS = "Nuclear Radiation and Dosimetry"
HLF = "Half-Life, Fission and Fusion"
WR = {"alpha particles": 20, "beta particles": 1, "gamma rays": 1, "X-rays": 1, "fast neutrons": 10, "slow neutrons": 3}
_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

_NOTES = r"""
## N5 Radiation — exam technique

**Relationships (as on the relationships sheet):**
$$A = \frac{N}{t} \quad D = \frac{E}{m} \quad H = Dw_R \quad \dot{H} = \frac{H}{t} \quad P = \frac{E}{t}$$

Weighting factors: alpha 20, beta 1, gamma 1, X-rays 1, fast neutrons 10, slow neutrons 3.
Annual: UK background 2.2 mSv; limit for the public 1 mSv; for a radiation worker 20 mSv.

**Common errors (SQA course reports and marking instructions):**
- **Ionisation**: an atom gains or loses an **electron**. A **beta** particle is a fast electron **from the nucleus**; **gamma** is high-frequency EM radiation.
- Explain absorption **in the context** (paper? soil? the detector's air?) — not just "alpha is stopped by paper".
- Convert **µ, m, k** prefixes. Weight **each** absorbed dose separately before adding.
- To find D from H, divide by $w_R$ first. Keep the time in **hours** if the rate is per hour.
- Activity is decays per **second**. Count half-lives by **halving** repeatedly — show the halving.
- Half-life: the time for the **activity** to halve (not "the radiation"). Subtract the **background count rate**.
- Fission: a large **nucleus** splits; the **neutrons** released split further nuclei (chain reaction). Fusion: two small nuclei join — needs very high temperatures; plasma held by magnetic fields.
- Uses of nuclear **radiation**: tracers, sterilising, smoke detectors, thickness gauges, treating cancer — generating electricity is a use of nuclear **reactions**.
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


def _q(text, answer, unit, options, qtype, scaffold=None, level="N5"):
    kept = []
    for o in options:
        o["value"] = _sig(o["value"])
        o.setdefault("display", f"{_txt(o['value'])} {unit}".strip())
        if all(abs(o["value"] - k["value"]) > 0.02 * max(abs(o["value"]), abs(k["value"])) for k in kept):
            kept.append(o)
    return make_question(text, _sig(answer), kept, unit, scaffold=scaffold, notes=_NOTES,
                         topic=TOPIC, question_type=qtype, level=level)


def _choice(text, correct, wrong, qtype, level="N5"):
    distractors = [{"value": w, "mistake": why, "working": []} for w, why in wrong]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(question_text=text, correct_answer=correct, unit="", distractors=distractors,
                           working=[], notes=_NOTES, topic=TOPIC, question_type=qtype, level=level,
                           metadata={"type": "classification", "options": options})


def _opts(work, right, *wrong):
    return [{"value": right, "mistake": None, "working": work}] + [{"value": v, "mistake": m, "working": work} for v, m in wrong]


# ════════════════ Dosimetry ════════════════
# (who, mass range kg, energy choices with prefix) — tied so doses are realistic
_ABSORBERS = [("A radiographer", (60, 70, 80), [(7.2, "mJ", 1e-3), (3.6, "mJ", 1e-3)]),
              ("A technician", (64, 75, 80), [(1.2, "µJ", 1e-6), (4.5, "µJ", 1e-6)]),
              ("A patient's liver", (1.5, 2.0), [(90, "µJ", 1e-6), (45, "µJ", 1e-6)]),
              ("A tissue sample", (0.10, 0.25, 0.50), [(9.6, "µJ", 1e-6), (2.5, "µJ", 1e-6)])]


def gen_rd_dose(level="N5"):
    kind = random.choice(["D", "H_total", "D_from_H", "rate"])
    if kind == "D":
        who, ms, es = random.choice(_ABSORBERS)
        m = random.choice(ms)
        val, pre, mult = random.choice(es)
        D = val * mult / m
        text = f"{who} of mass {m:g} kg absorbs {val:g} {pre} of energy from radiation. Calculate the absorbed dose."
        work = [_L(r"D = \frac{E}{m}"), _L(rf"D = \frac{{{val:g}\times10^{{{-3 if mult == 1e-3 else -6}}}}}{{{m:g}}} = {_ltx(D)}\ \mathrm{{Gy}}")]
        return _q(text, D, "Gy", _opts(work, D, (val / m, f"Convert {pre} to J (course report 2023: the micro prefix)."), (val * mult * m, "D = E ÷ m.")), DOS, None, level)
    if kind == "H_total":
        (r1, w1), (r2, w2) = random.sample([(r, w) for r, w in WR.items() if r != "X-rays"], 2)
        d1, d2 = random.choice([0.20, 2.2, 3.0, 5.0, 15]), random.choice([0.50, 3.4, 6.0, 20])
        H = d1 * w1 + d2 * w2
        text = f"A tissue sample receives an absorbed dose of {d1:g} µGy from {r1} and {d2:g} µGy from {r2}. Calculate the total equivalent dose, in µSv."
        work = [_L(r"H = Dw_R"), _L(rf"H = {d1:g}\times{w1} + {d2:g}\times{w2} = {_ltx(H)}\ \mu\mathrm{{Sv}}")]
        scaffold = [{"question": f"What is the equivalent dose from the {r1}, in µSv?", "answer": _sig(d1 * w1)},
                    {"question": f"What is the equivalent dose from the {r2}, in µSv?", "answer": _sig(d2 * w2)},
                    {"question": "What is the total equivalent dose, in µSv?", "answer": _sig(H)}]
        return _q(text, H, "µSv", _opts(work, H, (d1 + d2, "Multiply each absorbed dose by its weighting factor."),
                                        ((d1 + d2) * max(w1, w2), "Weight EACH dose separately, then add (2017, 2024 Paper 1)."),
                                        (d1 / w1 + d2 / w2, "H = D × w_R — multiply, don't divide.")), DOS, scaffold, level)
    if kind == "D_from_H":
        r = random.choice(["alpha particles", "fast neutrons", "slow neutrons"])
        w = WR[r]
        H_us = random.choice([4.0, 12, 30, 60])
        m = random.choice([50, 64, 70])
        D = H_us * 1e-6 / w
        E = D * m
        text = f"A {m} kg patient receives an equivalent dose of {H_us:g} µSv from {r}. Calculate the energy absorbed."
        work = [_L(r"H = Dw_R"), _L(rf"D = \frac{{{H_us:g}\times10^{{-6}}}}{{{w}}} = {_ltx(D)}\ \mathrm{{Gy}}"), _L(r"D = \frac{E}{m}"),
                _L(rf"E = {_ltx(D)} \times {m} = {_ltx(E)}\ \mathrm{{J}}")]
        scaffold = [{"question": "What is the absorbed dose, in Gy?", "answer": _sig(D)}, {"question": "What is the energy absorbed, in J?", "answer": _sig(E)}]
        return _q(text, E, "J", _opts(work, E, (H_us * 1e-6 * m, "The equivalent dose is not the absorbed dose — divide by w_R first (course report 2025)."),
                                      (H_us * m, "Convert µSv (× 10⁻⁶)."), (D / m, "E = D × m.")), DOS, scaffold, level)
    rate, unit, t, tunit, conv = random.choice([(6.0, "µSv/h", 3.5, "hours", 1), (0.40, "mSv/h", 30, "minutes", 1 / 60),
                                                (5.0, "µSv/h", 8, "hours", 1), (2.5, "µSv/h", 45, "minutes", 1 / 60)])
    th = t * conv
    H = rate * th
    hu = unit.split("/")[0]
    text = f"A worker is exposed to an equivalent dose rate of {rate:g} {unit} for {t:g} {tunit}. Calculate the equivalent dose received, in {hu}."
    work = [_L(r"\dot{H} = \frac{H}{t}"), _L(rf"t = {_ltx(th)}\ \mathrm{{h}}"), _L(rf"H = {rate:g} \times {_ltx(th)} = {_ltx(H)}\ \text{{{hu}}}")]
    wrong = [(rate * t * 3600 * conv, "The rate is per HOUR — keep the time in hours (course report 2023).")]
    if conv != 1:
        wrong.append((rate * t, "Convert minutes to hours (course report 2018)."))
    return _q(text, H, hu, _opts(work, H, *wrong, (rate / th, "H = Ḣ × t.")), DOS, None, level)


def gen_rd_nature(level="N5"):
    kind = random.choice(["ionisation", "beta", "gamma", "penetration", "smoke", "pipe", "absorbers", "use", "limits"])
    if kind == "ionisation":
        return _choice("What is meant by ionisation?", "An atom gaining or losing an electron.",
                       [("A nucleus splitting into two.", "That's fission."), ("An atom losing a proton.", "It is ELECTRONS that are gained or lost."),
                        ("A nucleus emitting a gamma ray.", "That's gamma emission.")], DOS, level)
    if kind == "beta":
        return _choice("What is a beta particle?", "A fast-moving electron emitted from the nucleus.",
                       [("An electron.", "Must say it comes from the NUCLEUS (course report 2018)."), ("A helium nucleus.", "That's an alpha particle."),
                        ("High-frequency electromagnetic radiation.", "That's gamma.")], DOS, level)
    if kind == "gamma":
        return _choice("What is a gamma ray?", "High-frequency electromagnetic radiation emitted from a nucleus.",
                       [("A fast electron from the nucleus.", "That's beta."), ("A helium nucleus.", "That's alpha."),
                        ("A neutron.", "Gamma is electromagnetic radiation (course report 2015).")], DOS, level)
    if kind == "penetration":
        return _choice("Which radiation is the most ionising and the least penetrating?", "alpha",
                       [("gamma", "Gamma is the least ionising and most penetrating."), ("beta", "Beta is in between."), ("X-rays", "Not nuclear radiation; weakly ionising.")], DOS, level)
    if kind == "smoke":
        return _choice("Why does a smoke detector use an alpha source?", "Alpha is highly ionising and has a short range in air, so it does not escape the detector.",
                       [("Alpha is stopped by a sheet of paper.", "There's no paper in a smoke detector — give a reason that fits the context (course report 2022)."),
                        ("Alpha is the most penetrating.", "Alpha is the LEAST penetrating."), ("Alpha has the shortest half-life.", "Americium-241 has a long half-life.")], DOS, level)
    if kind == "pipe":
        return _choice("A tracer is used to find a leak in a pipe buried under tarmac and rock. Why must it emit gamma radiation?",
                       "Alpha and beta would be absorbed by the tarmac and rock and not reach the detector.",
                       [("Gamma is the most ionising.", "Gamma is the LEAST ionising."), ("Gamma is the most penetrating.", "Refer to the materials above the pipe (course report 2025)."),
                        ("Gamma has the longest half-life.", "Half-life depends on the source, not the radiation type.")], DOS, level)
    if kind == "absorbers":
        return _choice("Paper reduces the count rate from a source; adding 3 mm of aluminium makes no further difference; 8 mm of lead reduces it further. What does the source emit?",
                       "alpha and gamma", [("alpha and beta", "Aluminium would have reduced the count if beta were present."),
                                           ("beta and gamma", "Paper reduced the count, so alpha is present."), ("gamma only", "Paper reduced the count, so alpha is present.")], DOS, level)
    if kind == "use":
        return _choice("Which is a use of nuclear RADIATION?", "Sterilising medical equipment",
                       [("Generating electricity in a power station", "That's a use of nuclear REACTIONS (course report 2023)."),
                        ("Nuclear weapons", "A use of nuclear reactions, not radiation."), ("Heating homes", "Not a use of radiation.")], DOS, level)
    return _choice("What is the annual effective dose limit for a member of the public?", "1 mSv",
                   [("2.2 mSv", "That's the average UK background dose."), ("20 mSv", "That's the limit for a radiation worker."), ("0 mSv", "Background radiation can't be avoided.")], DOS, level)


# ════════════════ Half-life, fission and fusion ════════════════

def gen_hl_activity(level="N5"):
    kind = random.choice(["A", "N", "after", "halflife", "fraction"])
    if kind == "A":
        N, t, tunit, conv = random.choice([(1800, 3, "minutes", 60), (3000, 2, "minutes", 60), (240, 1, "minute", 60),
                                           (1.8e6, 10, "hours", 3600), (1.44e8, 2, "hours", 3600)])
        A = N / (t * conv)
        text = f"{_txt(N)} nuclei in a source decay in {t} {tunit}. Calculate the activity."
        work = [_L(r"A = \frac{N}{t}"), _L(rf"A = \frac{{{_ltx(N)}}}{{{t} \times {conv}}} = {_ltx(A)}\ \mathrm{{Bq}}")]
        return _q(text, A, "Bq", _opts(work, A, (N / t, f"Convert {tunit} to seconds."), (N * t * conv, "A = N ÷ t.")), HLF, None, level)
    if kind == "N":
        A, pre, mult, t, tunit, conv = random.choice([(5.2, "MBq", 1e6, 1.2, "hours", 3600), (2.4e4, "Bq", 1, 15, "minutes", 60),
                                                      (5.5, "Bq", 1, 1, "minute", 60), (80, "kBq", 1e3, 2, "minutes", 60)])
        N = A * mult * t * conv
        text = f"A source has an average activity of {_txt(A)} {pre}. Calculate the number of nuclei that decay in {t:g} {tunit}."
        work = [_L(r"A = \frac{N}{t}"), _L(rf"N = {_ltx(A * mult)} \times {_ltx(t * conv)} = {_ltx(N)}")]
        return _q(text, N, "", _opts(work, N, (A * mult * t, f"Convert {tunit} to seconds (course report 2025)."), (A * t * conv, f"Convert {pre} to Bq.")), HLF, None, level)
    A0 = random.choice([800, 1600, 3200, 6400, 12000, 848000])
    th = random.choice([2, 5.3, 8, 15, 30, 36])
    n = random.choice([2, 3, 4])
    A = A0 / 2 ** n
    if kind == "after":
        text = f"A source has an activity of {A0:g} Bq and a half-life of {th:g} hours. Determine its activity {n * th:g} hours later."
        work = [_L(rf"\text{{number of half-lives}} = \frac{{{n * th:g}}}{{{th:g}}} = {n}"), _L(rf"{A0:g} \to " + r" \to ".join(f"{A0 / 2 ** k:g}" for k in range(1, n + 1)))]
        scaffold = [{"question": "How many half-lives is this?", "answer": n}, {"question": "What is the activity, in Bq?", "answer": _sig(A)}]
        return _q(text, A, "Bq", _opts(work, A, (A0 / n, "Halve n times — don't divide by the number of half-lives."), (A0 / 2, "That's after ONE half-life.")), HLF, scaffold, level)
    if kind == "halflife":
        text = f"The activity of a source falls from {A0:g} Bq to {A:g} Bq in {n * th:g} days. Determine its half-life."
        work = [_L(rf"{A0:g} \to " + r" \to ".join(f"{A0 / 2 ** k:g}" for k in range(1, n + 1)) + rf"\ ({n}\ \text{{half-lives}})"),
                _L(rf"\text{{half-life}} = \frac{{{n * th:g}}}{{{n}}} = {th:g}\ \text{{days}}")]
        return _q(text, th, "days", _opts(work, th, (n * th / 2, "Count how many times it halves."), (n * th, "That's the total time, not the half-life.")), HLF, None, level)
    frac = {2: "one-quarter", 3: "one-eighth", 4: "one-sixteenth"}[n]
    text = f"Nuclear waste has a half-life of {th:g} years. Determine the time for its activity to fall to {frac} of its original value."
    work = [_L(rf"1 \to " + r" \to ".join(f"1/{2 ** k}" for k in range(1, n + 1)) + rf"\ ({n}\ \text{{half-lives}})"), _L(rf"t = {n} \times {th:g} = {n * th:g}\ \text{{years}}")]
    return _q(text, n * th, "years", _opts(work, n * th, (2 ** n * th, f"{frac} is {n} half-lives, not {2 ** n}."), (th / n, "Multiply the half-life by the number of half-lives.")), HLF, None, level)


def gen_hl_fission_power(level="N5"):
    e_each = random.choice([2.9e-11, 3.2e-11, 3.5e-11])
    kind = random.choice(["power", "number"])
    if kind == "power":
        n = random.choice([1.5e21, 3.0e21, 6.0e21])
        E = n * e_each
        P = E / 60
        text = f"Each fission in a reactor releases {_txt(e_each)} J. {_txt(n)} fissions occur each minute. Calculate the power output."
        work = [_L(rf"E = {_ltx(n)} \times {_ltx(e_each)} = {_ltx(E)}\ \mathrm{{J}}"), _L(r"P = \frac{E}{t}"), _L(rf"P = \frac{{{_ltx(E)}}}{{60}} = {_ltx(P)}\ \mathrm{{W}}")]
        scaffold = [{"question": "What is the energy released per minute, in J?", "answer": _sig(E)}, {"question": "What is the power, in W?", "answer": _sig(P)}]
        return _q(text, P, "W", _opts(work, P, (E, "That's the energy per MINUTE — divide by 60 s for the power."), (e_each / 60, "Multiply by the number of fissions.")), HLF, scaffold, level)
    P_mw = random.choice([150, 200, 500])
    E = P_mw * 1e6 * 3600
    N = E / e_each
    text = f"A reactor has a power output of {P_mw} MW. Each fission releases {_txt(e_each)} J. Determine the minimum number of fissions each hour."
    work = [_L(r"P = \frac{E}{t}"), _L(rf"E = {P_mw}\times10^6 \times 3600 = {_ltx(E)}\ \mathrm{{J}}"), _L(rf"N = \frac{{{_ltx(E)}}}{{{_ltx(e_each)}}} = {_ltx(N)}")]
    scaffold = [{"question": "What is the energy produced in one hour, in J?", "answer": _sig(E)}, {"question": "How many fissions is that?", "answer": _sig(N)}]
    return _q(text, N, "", _opts(work, N, (P_mw * 1e6 / e_each, "That's per SECOND — the question asks per hour (course report 2022)."),
                                 (P_mw * 3600 / e_each, "Convert MW to W.")), HLF, scaffold, level)


def gen_hl_explain(level="N5"):
    kind = random.choice(["halflife", "chain", "fission", "fusion", "plasma", "experiment", "background", "tracer", "longer"])
    if kind == "halflife":
        return _choice("What is meant by half-life?", "The time for the activity of a source to fall to half its original value.",
                       [("The time for the radiation to halve.", "Must refer to ACTIVITY — ‘radiation/radioactivity’ not accepted (MI)."),
                        ("Half the time a source stays radioactive.", "Not a definition."), ("The time for the mass of a source to halve.", "It is the activity that halves.")], HLF, level)
    if kind == "chain":
        return _choice("How does one fission lead to a chain reaction?", "Neutrons released by the fission go on to split further nuclei, which release more neutrons.",
                       [("The same nucleus keeps splitting again and again.", "Different nuclei are split by the released neutrons (course reports 2017, 2024)."),
                        ("The neutrons themselves split.", "Neutrons are released, not split."),
                        ("Electrons released split more nuclei.", "It is NEUTRONS.")], HLF, level)
    if kind == "fission":
        return _choice("What is nuclear fission?", "A large nucleus splits into smaller nuclei, releasing energy and neutrons.",
                       [("A large atom splits into smaller atoms.", "Use ‘nucleus’, not ‘atom’ (course report 2022)."),
                        ("Two small nuclei join together.", "That's fusion."), ("An atom loses an electron.", "That's ionisation.")], HLF, level)
    if kind == "fusion":
        return _choice("Energy is released when two small nuclei combine to form a larger nucleus. This is", "nuclear fusion",
                       [("nuclear fission", "Fission SPLITS a large nucleus."), ("alpha decay", "Alpha decay emits a helium nucleus."), ("ionisation", "That's electrons gained or lost.")], HLF, level)
    if kind == "plasma":
        return _choice("What is a difficulty in SUSTAINING fusion in a reactor?", "Keeping the plasma at a very high temperature and contained by magnetic fields.",
                       [("It costs a lot of money.", "Not physics (course report 2022)."), ("Fusion only happens at low temperatures.", "Fusion needs very HIGH temperatures."),
                        ("Starting the reaction needs a neutron.", "That's fission; the question is about sustaining fusion.")], HLF, level)
    if kind == "experiment":
        return _choice("A half-life experiment's readings fall only slightly over 20 minutes. How could the half-life be found more easily?",
                       "Take readings over a longer time.", [("Move the source closer to the Geiger-Müller tube.", "That doesn't change how quickly the activity halves (course report 2024)."),
                                                             ("Take readings every 30 s instead of 60 s.", "More points over the same short time won't show a halving."),
                                                             ("Use a ratemeter instead of a counter.", "The problem is the time span.")], HLF, level)
    if kind == "background":
        return _choice("What extra measurement is needed to find the corrected count rate?", "The background count rate",
                       [("The background radiation", "Must be ‘background count (rate)’ (course report 2023)."), ("The half-life", "Not needed for the correction."),
                        ("The mass of the source", "Not needed.")], HLF, level)
    if kind == "tracer":
        return _choice("Which is the most suitable tracer to monitor blood flow with a detector outside the body?", "gamma emitter, half-life 2 days",
                       [("beta emitter, half-life 2 days", "Beta is absorbed by the body."), ("gamma emitter, half-life 2 seconds", "Decays before the test is done."),
                        ("gamma emitter, half-life 2 years", "Stays active in the patient far too long.")], HLF, level)
    return _choice("A tritium torch (half-life 12.3 years) gets dimmer over 15 years. Why?", "The activity decreases, so fewer beta particles are emitted per second and less light is produced.",
                   [("The radioactivity runs out.", "Use ‘activity’ — the number of decays per second (course report 2018)."),
                    ("The beta particles get weaker.", "Each particle is the same; there are fewer per second."),
                    ("The half-life gets shorter.", "The half-life is constant.")], HLF, level)
