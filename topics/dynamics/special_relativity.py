import random
import math
import pathlib
from core.models.question_model import PhysicsQuestion

_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "relativity_widget.html"
).read_text(encoding="utf-8")

_TOPIC = "Our Dynamic Universe"
_QTYPE = "Special Relativity"

_NOTES = """
## Special Relativity

**Relative velocity at everyday speeds:** velocities simply add or subtract. Put every speed
in the same frame first (e.g. everything relative to the ground), then compare.

**Einstein's postulates** (apply in any inertial frame — one that is not accelerating):
1. The laws of physics are the same in all inertial frames of reference.
2. The speed of light in a vacuum is the same for all observers — it does not add to the
   speed of the source or the observer. If you give a number (3.00 × 10⁸ m/s), you must give
   the unit.

**Time dilation** (relationships sheet):
$$t' = \\frac{t}{\\sqrt{1 - \\left(\\frac{v}{c}\\right)^2}}$$

**Length contraction** (relationships sheet):
$$l' = l\\sqrt{1 - \\left(\\frac{v}{c}\\right)^2}$$

| Symbol | Quantity | Unit |
|---|---|---|
| t | Time measured in the frame where the clock (or event) is **at rest** | s |
| t′ | Time measured by an observer who sees the clock **moving** | s |
| l | Length measured in the frame where the object is **at rest** | m |
| l′ | Length measured by an observer who sees the object **moving** | m |
| v | Relative speed of the two frames | m/s |
| c | Speed of light = 3.00 × 10⁸ m/s | m/s |

> **Decide which frame the clock or object is at rest in before you substitute.** It is not
> always the spacecraft: a bridge, a tunnel, a beacon on the Moon, the atmosphere or the gap
> between two detectors is at rest on Earth, so l or t is the value measured on Earth and the
> spacecraft or particle measures l′ or t′.
>
> **Check your answer:** t′ is always longer than t; l′ is always shorter than l.
>
> **Convert prefixes** (µs, ns, km) before substituting, and give the answer in the unit asked for.

**Explanations — always name a frame of reference.** E.g. *"In the Earth observer's frame of
reference, the mean lifetime of the muons is greater"* or *"In the muons' frame of reference,
the distance to the ground is shorter."* An answer that doesn't name a frame gets no mark.
"""

_C = 3.00e8  # speed of light, m/s

_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
_UNSUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")

_SCI_HINT = " (Enter very large or small numbers in e-notation, e.g. 2.5e-8 for 2.5 × 10⁻⁸.)"


# ── formatting helpers ──────────────────────────────────────────────────────

def _sig(x, sf=3):
    return float(f"{x:.{sf}g}")


def _txt(x, sf=3):
    """Plain-text number to sf significant figures (trailing zeros kept, so
    12.0 stays 12.0), in × 10ⁿ form outside 0.01–10⁴. Never e-notation."""
    x = _sig(x, sf)
    if x == 0:
        return "0"
    if 0.01 <= abs(x) < 1e4:
        decimals = max(0, sf - 1 - math.floor(math.log10(abs(x))))
        return f"{x:.{decimals}f}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    return f"{coeff} × 10{str(int(exp)).translate(_SUP)}"


def _ltx(x, sf=3):
    t = _txt(x, sf)
    if "×" not in t:
        return t
    coeff, rest = t.split(" × 10")
    return rf"{coeff} \times 10^{{{rest.translate(_UNSUP)}}}"


def _L(s):
    return {"type": "latex", "content": s}


def _T(s):
    return {"type": "text", "content": s}


def _lor(beta):
    return math.sqrt(1 - beta ** 2)


# v/c values used in SQA papers span 0.10c–0.999c — never just 0.6c/0.8c, whose
# √(1−(v/c)²) = 0.8/0.6 pupils can pattern-match without calculating.
_BETAS = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
          0.85, 0.88, 0.90, 0.92, 0.95, 0.97, 0.98, 0.99, 0.995, 0.998, 0.999]


def _speed(lo, hi, allow_ms=True):
    """Pick a speed with lo <= v/c <= hi. Returns (beta, text, latex). About a
    third of the time (when it has a clean 3 s.f. value) the speed is given in
    m/s, as in the 2016, 2024 and 2025 papers, so pupils must form v/c."""
    beta = random.choice([b for b in _BETAS if lo <= b <= hi])
    if allow_ms and abs(beta * 300 - round(beta * 300)) < 1e-9 and random.random() < 0.35:
        return beta, f"{_txt(beta * _C)} m/s", _ltx(beta * _C)
    return beta, f"{_b(beta)}c", f"{_b(beta)}c"


def _b(beta):
    """v/c as printed: at least 2 d.p., e.g. 0.60c, 0.995c."""
    return f"{beta:.2f}" if round(beta, 2) == beta else f"{beta:g}"


def _beta_sub(beta, v_latex):
    """LaTeX for (v/c)² in a substitution line."""
    if v_latex.endswith("c"):
        return rf"\left({_b(beta)}\right)^2"
    return rf"\left(\frac{{{v_latex}}}{{3.00 \times 10^{{8}}}}\right)^2"


def _dedup(options_data, correct):
    """Drop distractors within 2% of the answer or an earlier distractor (the
    UI's answer tolerance), so a typed answer maps to one diagnosis only."""
    kept, seen = [], [float(correct)]
    for opt in options_data:
        if opt["mistake"] is None:
            continue
        v = float(opt["value"])
        if all(abs(v - s) > 0.02 * max(abs(s), 1e-30) for s in seen):
            kept.append(opt)
            seen.append(v)
    correct_opt = next((o for o in options_data if o["mistake"] is None), None)
    return [correct_opt or {"value": correct, "mistake": None, "working": []}] + kept


def _num(question, answer, options, unit, scaffold=None, level="Higher"):
    """Like make_question(), but tells the correct option apart by its
    mistake=None flag rather than make_question's round(value, 6) match —
    which treats every value below ~10⁻⁶ (particle lifetimes, pion transit
    times) as equal to the answer and silently drops all the distractors."""
    options = _dedup(options, answer)
    return PhysicsQuestion(
        question_text=question, correct_answer=float(answer), unit=unit,
        topic=_TOPIC, question_type=_QTYPE, level=level, notes=_NOTES,
        working=options[0].get("working", []),
        distractors=[{"value": float(o["value"]), "display": f"{o['value']} {unit}",
                      "mistake": o["mistake"], "working": o.get("working", [])}
                     for o in options[1:]],
        scaffold=[{"prompt": st["question"], "answer": st["answer"], "unit": st.get("unit", "")}
                  for st in (scaffold or [])],
    )


def _choice(question_text, correct, wrong, level="Higher", working_text=None):
    """wrong: list of (option text, why it's wrong)."""
    working = [_T(working_text)] if working_text else []
    distractors = [{"value": w, "mistake": why, "working": working} for w, why in wrong]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(
        question_text=question_text, correct_answer=correct, unit="",
        topic=_TOPIC, question_type=_QTYPE, level=level,
        distractors=distractors, working=working, notes=_NOTES,
        metadata={"type": "classification", "options": options},
    )


def _explain(question_text, answer_text, level="Higher"):
    return PhysicsQuestion(
        question_text=question_text, correct_answer="", unit="",
        topic=_TOPIC, question_type=_QTYPE, level=level, notes=_NOTES,
        metadata={"type": "explain", "explain_text": answer_text},
    )


def _scenario(context, parts, level="Higher"):
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic=_TOPIC, question_type=_QTYPE, level=level,
        is_scenario=True, scenario_context=context, parts=parts,
    )


def _part(question, answer, options, unit, scaffold, level):
    return _num(question, answer, options, unit, scaffold, level)


def _speed_scaffold(v_txt, beta):
    return [] if v_txt.endswith("c") else [{"question": "What is v/c?", "answer": beta}]


# ── Time dilation: t' = t / √(1 − (v/c)²) ────────────────────────────────────

# (plural name, mean lifetime in own frame (s), as printed, beta lo, beta hi)
_PARTICLES = [
    ("Muons", 2.20e-6, "2.20 µs", 0.95, 0.999),
    ("Pions", 26.0e-9, "26.0 ns", 0.85, 0.99),
    ("Kaons", 12.4e-9, "12.4 ns", 0.80, 0.98),
    ("Lambda particles", 2.63e-10, "2.63 × 10⁻¹⁰ s", 0.80, 0.97),
    ("Sigma particles", 1.48e-10, "1.48 × 10⁻¹⁰ s", 0.80, 0.97),
]

# (first mention, later mention)
_PLACES = [("Earth", "Earth"), ("a nearby planet", "the planet"), ("the Moon", "the Moon"),
           ("a space station", "the space station")]
_CRAFT = ["A spacecraft", "A probe", "A rocket", "A shuttlecraft"]


def _t_forward_work(t, beta, v_ltx, ans, note=None):
    work = [_T(note)] if note else []
    work += [
        _L(r"t' = \frac{t}{\sqrt{1 - \left(\frac{v}{c}\right)^2}}"),
        _L(rf"t' = \frac{{{_ltx(t)}}}{{\sqrt{{1 - {_beta_sub(beta, v_ltx)}}}}}"),
        _L(rf"t' = {_ltx(ans)}\ \mathrm{{s}}"),
    ]
    return work


def gen_t_prime(level="Higher"):
    """Find the dilated time t′ — a spacecraft clock, a particle lifetime, or
    a clock at rest on the Moon/station seen from a passing spacecraft."""
    kind = random.choice(["ship", "particle", "beacon"])
    prefix = None

    if kind == "ship":
        beta, v_txt, v_ltx = _speed(0.30, 0.95)
        t = _sig(random.uniform(5, 300))
        place, the_place = random.choice(_PLACES)
        question = (f"{random.choice(_CRAFT)} travels at a constant speed of {v_txt} relative to "
                    f"{place}. A clock on board measures a time interval of {_txt(t)} s. "
                    f"Calculate the time interval as measured by an observer on {the_place}.")
        note = f"The clock is at rest on board, so t = {_txt(t)} s. The observer on {the_place} sees it moving and measures t′."
        swapped = "You multiplied by √(1−(v/c)²). The on-board clock is at rest in the spacecraft, so its reading is t; the observer who sees it moving measures the longer time t′."
    elif kind == "particle":
        name, t, tau_txt, lo, hi = random.choice(_PARTICLES)
        beta, v_txt, v_ltx = _speed(lo, hi)
        question = (f"{name} have a mean lifetime of {tau_txt} in their own frame of reference. "
                    f"In an experiment they travel at {v_txt} relative to a stationary observer. "
                    f"Calculate the mean lifetime of the {name.lower()} as measured by this "
                    f"observer, in seconds." + _SCI_HINT)
        prefix = "µs" if "µs" in tau_txt else "ns" if "ns" in tau_txt else None
        note = f"The lifetime in the particles' own frame is t = {_txt(t)} s."
        swapped = "You multiplied by √(1−(v/c)²). The lifetime in the particles' own frame is t; the stationary observer sees them moving and measures the longer lifetime t′."
    else:
        beta, v_txt, v_ltx = _speed(0.30, 0.95)
        t = _sig(random.uniform(1.0, 30.0))
        where = random.choice(["on the Moon", "on a space station", "on the surface of Mars"])
        question = (f"A beacon {where} flashes once every {_txt(t)} s, as measured by an observer "
                    f"standing beside it. A spacecraft passes at a constant speed of {v_txt}. "
                    f"Calculate the time between flashes as measured by an observer on the "
                    f"spacecraft.")
        note = f"The beacon is at rest {where}, so t = {_txt(t)} s. This time it is the spacecraft observer who sees the clock moving and measures t′."
        swapped = f"You multiplied by √(1−(v/c)²). The beacon is at rest {where}, so {_txt(t)} s is the proper time t — the spacecraft observer sees it moving and measures the longer time t′."

    lor = _lor(beta)
    ans = _sig(t / lor)
    work = _t_forward_work(t, beta, v_ltx, ans, note)
    opts = [
        {"value": ans, "mistake": None, "working": work},
        {"value": _sig(t * lor), "mistake": swapped, "working": work},
        {"value": _sig(t / lor ** 2), "mistake": "Divide by √(1−(v/c)²), not by (1−(v/c)²) — don't forget the square root.", "working": work},
        {"value": _sig(t / math.sqrt(1 - beta)), "mistake": "Square v/c before subtracting it from 1: √(1 − (v/c)²), not √(1 − v/c).", "working": work},
    ]
    if prefix:
        factor = 1e6 if prefix == "µs" else 1e9
        opts.append({"value": _sig(ans * factor),
                     "mistake": f"That's the right number of {prefix}, but the question asks for seconds — 1 {prefix} = 10{'⁻⁶' if prefix == 'µs' else '⁻⁹'} s.",
                     "working": work})
    scaffold = _speed_scaffold(v_txt, beta) + [
        {"question": "What is √(1 − (v/c)²)?", "answer": _sig(lor, 4)},
        {"question": "What is the dilated time t′ (in s)?", "answer": ans},
    ]
    return _num(question, ans, opts, "s", scaffold, level)


def gen_t_proper(level="Higher"):
    """Find the proper time t from a dilated time — including the 2019 P1
    'journey time in hours' form."""
    craft = random.choice(_CRAFT)
    if random.choice([True, False]):
        beta, v_txt, v_ltx = _speed(0.30, 0.95)
        tp = _sig(random.uniform(10, 400))
        unit, u_ltx = "s", r"\ \mathrm{s}"
        question = (f"{craft} travels at a constant speed of {v_txt} relative to Earth. An "
                    f"observer on Earth measures a time interval of {_txt(tp)} s for a process "
                    f"taking place on board. Calculate the time interval for this process as "
                    f"measured by the crew.")
    else:
        beta, v_txt, v_ltx = _speed(0.20, 0.80)
        tp = _sig(random.uniform(10, 90))
        unit, u_ltx = "hours", r"\text{ hours}"
        question = (f"{craft} travels at {v_txt} relative to Earth. An observer on Earth measures "
                    f"the time taken for the spacecraft to travel between two points as "
                    f"{_txt(tp)} hours. Calculate the time taken for this journey as measured "
                    f"by the crew, in hours.")
    lor = _lor(beta)
    ans = _sig(tp * lor)
    work = [
        _T("The crew's clock is at rest in the spacecraft (and present at both events), so the crew measure t. The Earth observer measures t′."),
        _L(r"t' = \frac{t}{\sqrt{1 - \left(\frac{v}{c}\right)^2}}"),
        _L(rf"{_ltx(tp)} = \frac{{t}}{{\sqrt{{1 - {_beta_sub(beta, v_ltx)}}}}}"),
        _L(rf"t = {_ltx(ans)}{u_ltx}"),
    ]
    opts = [
        {"value": ans, "mistake": None, "working": work},
        {"value": _sig(tp / lor), "mistake": "You divided by √(1−(v/c)²), making the crew's time longer. The Earth value is already the dilated time t′ — the crew's proper time t must be shorter.", "working": work},
        {"value": _sig(tp * lor ** 2), "mistake": "Multiply by √(1−(v/c)²), not by (1−(v/c)²) — don't forget the square root.", "working": work},
        {"value": tp, "mistake": "The crew measure a different (shorter) time — apply the time dilation relationship.", "working": work},
    ]
    scaffold = _speed_scaffold(v_txt, beta) + [
        {"question": "What is √(1 − (v/c)²)?", "answer": _sig(lor, 4)},
        {"question": f"What is the proper time t measured by the crew (in {unit})?", "answer": ans},
    ]
    return _num(question, ans, opts, unit, scaffold, level)


def gen_v_from_time_dilation(level="Higher"):
    beta = random.choice([b for b in _BETAS if 0.30 <= b <= 0.99])
    lor = _lor(beta)
    if random.choice([True, False]):
        t = _sig(random.uniform(5, 200))
        tp = _sig(t / lor)
        question = (f"{random.choice(_CRAFT)} makes a journey which the crew time at {_txt(t)} s, "
                    f"while an observer on Earth times the same journey at {_txt(tp)} s. "
                    f"Calculate the speed of the spacecraft relative to Earth, in m/s." + _SCI_HINT)
    else:
        name, t, tau_txt, _, _ = random.choice(_PARTICLES)
        tp = _sig(t / lor)
        question = (f"{name} have a mean lifetime of {tau_txt} in their own frame of reference. "
                    f"An observer in a laboratory measures their mean lifetime as {_txt(tp)} s. "
                    f"Calculate the speed of the {name.lower()} relative to the laboratory, in "
                    f"m/s." + _SCI_HINT)
    ratio = t / tp
    b = math.sqrt(1 - ratio ** 2)
    v = _sig(b * _C)
    work = [
        _L(r"t' = \frac{t}{\sqrt{1 - \left(\frac{v}{c}\right)^2}}"),
        _L(rf"{_ltx(tp)} = \frac{{{_ltx(t)}}}{{\sqrt{{1 - \left(\frac{{v}}{{3.00 \times 10^{{8}}}}\right)^2}}}}"),
        _L(rf"v = {_ltx(v)}\ \mathrm{{m/s}}\quad ({_txt(b)}c)"),
    ]
    opts = [
        {"value": v, "mistake": None, "working": work},
        {"value": _sig(ratio * _C), "mistake": "t/t′ is √(1−(v/c)²), not v/c — you still need v/c = √(1 − (t/t′)²).", "working": work},
        {"value": _sig((1 - ratio ** 2) * _C), "mistake": "You forgot to take the square root when finding v/c from 1 − (t/t′)².", "working": work},
        {"value": _sig(b), "mistake": "That's v/c. The question asks for the speed in m/s — multiply by 3.00 × 10⁸ m/s.", "working": work},
    ]
    scaffold = [
        {"question": "What is t/t′ (both in the same unit)?", "answer": _sig(ratio, 4)},
        {"question": "What is v/c?", "answer": _sig(b)},
        {"question": "What is v in m/s?", "answer": v},
    ]
    return _num(question, v, opts, "m/s", scaffold, level)


# ── Length contraction: l' = l √(1 − (v/c)²) ─────────────────────────────────

# Objects at rest on Earth, measured from a moving frame (2017, 2022, 2024, 2025
# papers): (template, proper length lo, hi in m, beta lo, beta hi, "as measured …", thing)
_EARTH_OBJECTS = [
    ("The Skye Bridge has a length of {L} as measured by an observer standing on it. A "
     "spacecraft flies parallel to the bridge at a constant speed of {v} relative to Earth.",
     490, 510, 0.30, 0.95, "by an observer on the spacecraft", "the bridge"),
    ("The Tay Road Bridge has a length of {L} as measured by an observer standing on it. A "
     "spacecraft flies parallel to the bridge at a constant speed of {v} relative to Earth.",
     2240, 2260, 0.30, 0.95, "by an observer on the spacecraft", "the bridge"),
    ("A runway has a length of {L} as measured by an observer on the ground. A spacecraft "
     "flies parallel to the runway at a constant speed of {v} relative to the ground.",
     2000, 4000, 0.30, 0.95, "by the crew of the spacecraft", "the runway"),
    ("Protons travel at {v} along a straight section of beam pipe in a particle accelerator. "
     "Technicians measure the length of this section as {L}.",
     500, 3000, 0.99, 0.999, "in the frame of reference of the protons", "this section of beam pipe"),
    ("Muons travel vertically downwards at {v} relative to the Earth. An observer on Earth "
     "measures the thickness of the atmosphere through which they travel as {L}.",
     8000, 15000, 0.98, 0.999, "in the muons' frame of reference", "the atmosphere"),
    ("A beam of pions travels at {v} relative to a stationary observer, passing between two "
     "detectors which are {L} apart as measured by the stationary observer.",
     20, 60, 0.85, 0.99, "in the frame of reference of the pions", "the gap between the detectors"),
]


def _len_txt(m):
    """Length as it would be written in a question: km for ≥ 1000 m."""
    return f"{_txt(m / 1000)} km" if m >= 1000 else f"{_txt(m)} m"


def _l_forward_work(l, beta, v_ltx, ans, note=None):
    work = [_T(note)] if note else []
    work += [
        _L(r"l' = l\sqrt{1 - \left(\frac{v}{c}\right)^2}"),
        _L(rf"l' = {_ltx(l)} \times \sqrt{{1 - {_beta_sub(beta, v_ltx)}}}"),
        _L(rf"l' = {_ltx(ans)}\ \mathrm{{m}}"),
    ]
    return work


def gen_l_prime(level="Higher"):
    """Contracted length of a moving spacecraft, measured from outside it."""
    beta, v_txt, v_ltx = _speed(0.30, 0.95)
    l = _sig(random.uniform(40, 400))
    place, the_place = random.choice(_PLACES)
    question = (f"A technician on board a spacecraft measures its length as {_txt(l)} m. The "
                f"spacecraft travels at a constant speed of {v_txt} relative to {place}. "
                f"Calculate the length of the spacecraft as measured by an observer on {the_place}.")
    lor = _lor(beta)
    ans = _sig(l * lor)
    work = _l_forward_work(l, beta, v_ltx, ans,
                           "The spacecraft is at rest relative to the technician, so l is the technician's value.")
    opts = [
        {"value": ans, "mistake": None, "working": work},
        {"value": _sig(l / lor), "mistake": "Your answer is longer than the technician's length — but a moving object is measured shorter. l is the technician's value; multiply by √(1−(v/c)²).", "working": work},
        {"value": _sig(l * lor ** 2), "mistake": "Multiply by √(1−(v/c)²), not by (1−(v/c)²) — don't forget the square root.", "working": work},
        {"value": l, "mistake": "The observer sees the spacecraft moving, so measures a contracted (shorter) length.", "working": work},
    ]
    scaffold = _speed_scaffold(v_txt, beta) + [
        {"question": "What is √(1 − (v/c)²)?", "answer": _sig(lor, 4)},
        {"question": "What is the contracted length l′ (in m)?", "answer": ans},
    ]
    return _num(question, ans, opts, "m", scaffold, level)


def gen_l_prime_earth_object(level="Higher"):
    """Proper length is on Earth (bridge, runway, beam pipe, atmosphere,
    detector gap) and the moving frame measures l′. The 2022 course report
    noted many candidates substituted the wrong way round here and got an
    answer longer than the measured length."""
    template, lo, hi, blo, bhi, measured, thing = random.choice(_EARTH_OBJECTS)
    beta, v_txt, v_ltx = _speed(blo, bhi)
    l = _sig(random.uniform(lo, hi))
    lor = _lor(beta)
    ans = _sig(l * lor)
    question = (template.format(L=_len_txt(l), v=v_txt) +
                f" Calculate the length of {thing} as measured {measured}, in metres.")
    thing_cap = thing[0].upper() + thing[1:]
    note = (f"{thing_cap} is at rest on Earth, so l = {_txt(l)} m is the proper length. "
            f"The moving observer measures l′, which must be shorter.")
    work = _l_forward_work(l, beta, v_ltx, ans, note)
    opts = [
        {"value": ans, "mistake": None, "working": work},
        {"value": _sig(l / lor), "mistake": f"Your answer is longer than the Earth measurement. {thing_cap} is at rest on Earth, so the Earth value is the proper length l — the moving observer measures a shorter l′.", "working": work},
        {"value": _sig(l * lor ** 2), "mistake": "Multiply by √(1−(v/c)²), not by (1−(v/c)²) — don't forget the square root.", "working": work},
    ]
    if l >= 1000:
        opts.append({"value": _sig(ans / 1000), "mistake": "That's the answer in km — the question asks for metres.", "working": work})
    scaffold = _speed_scaffold(v_txt, beta) + [
        {"question": "What is the proper length l, in metres?", "answer": l},
        {"question": "What is √(1 − (v/c)²)?", "answer": _sig(lor, 4)},
        {"question": "What is the contracted length l′ (in m)?", "answer": ans},
    ]
    return _num(question, ans, opts, "m", scaffold, level)


def gen_l_proper(level="Higher"):
    beta, v_txt, v_ltx = _speed(0.30, 0.95)
    lp = _sig(random.uniform(30, 300))
    place, the_place = random.choice(_PLACES)
    question = (f"An observer on {place} measures the length of a passing spacecraft as "
                f"{_txt(lp)} m. The spacecraft travels at {v_txt} relative to {the_place}. "
                f"Calculate the length of the spacecraft as measured by its crew.")
    lor = _lor(beta)
    ans = _sig(lp / lor)
    work = [
        _T(f"The crew are at rest relative to the spacecraft, so they measure l. The observer on {the_place} measures the contracted length l′."),
        _L(r"l' = l\sqrt{1 - \left(\frac{v}{c}\right)^2}"),
        _L(rf"{_ltx(lp)} = l \times \sqrt{{1 - {_beta_sub(beta, v_ltx)}}}"),
        _L(rf"l = {_ltx(ans)}\ \mathrm{{m}}"),
    ]
    opts = [
        {"value": ans, "mistake": None, "working": work},
        {"value": _sig(lp * lor), "mistake": f"{_txt(lp)} m is already the contracted length l′. The crew's (proper) length must be longer — divide by √(1−(v/c)²).", "working": work},
        {"value": _sig(lp / lor ** 2), "mistake": "Divide by √(1−(v/c)²), not by (1−(v/c)²) — don't forget the square root.", "working": work},
        {"value": lp, "mistake": "The crew measure a different (longer) length — apply the length contraction relationship.", "working": work},
    ]
    scaffold = _speed_scaffold(v_txt, beta) + [
        {"question": "What is √(1 − (v/c)²)?", "answer": _sig(lor, 4)},
        {"question": "What is the proper length l (in m)?", "answer": ans},
    ]
    return _num(question, ans, opts, "m", scaffold, level)


def gen_v_from_length_contraction(level="Higher"):
    beta = random.choice([b for b in _BETAS if 0.30 <= b <= 0.99])
    l = _sig(random.uniform(50, 400))
    lp = _sig(l * _lor(beta))
    place, the_place = random.choice(_PLACES)
    question = (f"A spacecraft has a length of {_txt(l)} m as measured by its crew. An observer "
                f"on {place} measures its length as {_txt(lp)} m as it passes. Calculate the "
                f"speed of the spacecraft relative to {the_place}, in m/s." + _SCI_HINT)
    ratio = lp / l
    b = math.sqrt(1 - ratio ** 2)
    v = _sig(b * _C)
    work = [
        _L(r"l' = l\sqrt{1 - \left(\frac{v}{c}\right)^2}"),
        _L(rf"{_ltx(lp)} = {_ltx(l)} \times \sqrt{{1 - \left(\frac{{v}}{{3.00 \times 10^{{8}}}}\right)^2}}"),
        _L(rf"v = {_ltx(v)}\ \mathrm{{m/s}}\quad ({_txt(b)}c)"),
    ]
    opts = [
        {"value": v, "mistake": None, "working": work},
        {"value": _sig(ratio * _C), "mistake": "l′/l is √(1−(v/c)²), not v/c — you still need v/c = √(1 − (l′/l)²).", "working": work},
        {"value": _sig((1 - ratio ** 2) * _C), "mistake": "You forgot to take the square root when finding v/c from 1 − (l′/l)².", "working": work},
        {"value": _sig((1 - ratio) * _C), "mistake": "The relationship doesn't rearrange to 1 − l′/l — use v/c = √(1 − (l′/l)²).", "working": work},
        {"value": _sig(b), "mistake": "That's v/c. The question asks for the speed in m/s — multiply by 3.00 × 10⁸ m/s.", "working": work},
    ]
    scaffold = [
        {"question": "What is l′/l?", "answer": _sig(ratio, 4)},
        {"question": "What is v/c?", "answer": _sig(b)},
        {"question": "What is v in m/s?", "answer": v},
    ]
    return _num(question, v, opts, "m/s", scaffold, level)


# ── Multi-part muon / pion scenarios (2019 P2 Q4, 2022 P2 Q6 style) ─────────

_EXPLAIN_FRAMES = (
    "**Either:** in the **{obs} frame of reference**, the mean lifetime of the {p} is greater "
    "(time dilation), so they travel further before decaying.\n\n"
    "**Or:** in the **{p}' frame of reference**, the {d} is shorter (length contraction).\n\n"
    "*Your answer must name a frame of reference — the 2022 course report says most candidates "
    "lost this mark by not doing so.*"
)


def gen_muon_scenario(level="Higher"):
    tau = 2.20e-6
    beta = random.choice([0.98, 0.99, 0.995, 0.998])
    lor = _lor(beta)
    h = _sig(random.uniform(8, 15), 2) * 1000
    v = beta * _C
    d = _sig(v * tau)
    tp = _sig(tau / lor)
    lp = _sig(h * lor)
    context = (f"Muons are created about {_len_txt(h)} above the Earth's surface. They have a "
               f"mean lifetime of 2.20 µs in their own frame of reference and travel at "
               f"{_b(beta)}c relative to an observer on Earth.")

    w1 = [_L("d = vt"),
          _L(rf"d = ({_b(beta)} \times 3.00 \times 10^{{8}}) \times 2.20 \times 10^{{-6}}"),
          _L(rf"d = {_ltx(d)}\ \mathrm{{m}}")]
    p1 = _part(
        "Calculate the mean distance travelled by the muons using their own mean lifetime "
        "(ignoring relativity), in metres.", d,
        [{"value": d, "mistake": None, "working": w1},
         {"value": _sig(_C * tau), "mistake": f"Use the muons' speed, {_b(beta)} × 3.00 × 10⁸ m/s, not c.", "working": w1},
         {"value": _sig(v * tp), "mistake": "This part uses the muons' own lifetime (2.20 µs), not the dilated lifetime.", "working": w1},
         {"value": _sig(v * 2.20), "mistake": "Convert 2.20 µs to 2.20 × 10⁻⁶ s before substituting.", "working": w1}],
        "m", [{"question": "What is v in m/s?", "answer": _sig(v)},
              {"question": "What is d in m?", "answer": d}], level)

    w2 = _t_forward_work(tau, beta, f"{_b(beta)}c", tp)
    p2 = _part(
        "Calculate the mean lifetime of the muons as measured by the observer on Earth, in "
        "seconds." + _SCI_HINT, tp,
        [{"value": tp, "mistake": None, "working": w2},
         {"value": _sig(tau * lor), "mistake": "The Earth observer sees the muons moving, so measures the longer time t′ — divide by √(1−(v/c)²).", "working": w2},
         {"value": _sig(tp * 1e6), "mistake": "That's the answer in µs — the question asks for seconds.", "working": w2}],
        "s", [{"question": "What is √(1 − (v/c)²)?", "answer": _sig(lor, 4)},
              {"question": "What is t′ in s?", "answer": tp}], level)

    w3 = _l_forward_work(h, beta, f"{_b(beta)}c", lp,
                         f"The atmosphere is at rest on Earth, so l = {_txt(h)} m. The muons measure l′.")
    p3 = _part(
        f"Calculate the {_len_txt(h)} distance as measured in the muons' frame of reference, in "
        f"metres.", lp,
        [{"value": lp, "mistake": None, "working": w3},
         {"value": _sig(h / lor), "mistake": "Your answer is longer than the Earth value. The atmosphere is at rest on Earth, so the Earth value is l — the muons measure a shorter l′.", "working": w3},
         {"value": _sig(lp / 1000), "mistake": "That's in km — the question asks for metres.", "working": w3}],
        "m", [{"question": "What is l in m?", "answer": h},
              {"question": "What is l′ in m?", "answer": lp}], level)

    p4 = _explain(
        "Explain why a greater number of muons are detected on the Earth's surface than would "
        "be expected if relativistic effects were not taken into account. Write your answer in "
        "your jotter, then compare.",
        _EXPLAIN_FRAMES.format(obs="Earth observer's", p="muons",
                               d="distance to the Earth's surface"), level)
    return _scenario(context, [p1, p2, p3, p4], level)


def gen_pion_scenario(level="Higher"):
    beta = random.choice([0.90, 0.92, 0.95, 0.97, 0.98, 0.99])
    lor = _lor(beta)
    gap = _sig(random.uniform(20, 60))
    v = beta * _C
    t = _sig(gap / v)
    lp = _sig(gap * lor)
    context = (f"A beam of pions travels in a straight line at {_b(beta)}c relative to a stationary "
               f"observer. The beam passes between two detectors which are {_txt(gap)} m apart "
               f"as measured by the stationary observer. Pions have a mean lifetime of 26 ns in "
               f"their own frame of reference.")
    w1 = [_L("d = vt"), _L(rf"{_ltx(gap)} = ({_b(beta)} \times 3.00 \times 10^{{8}}) \times t"),
          _L(rf"t = {_ltx(t)}\ \mathrm{{s}}")]
    p1 = _part(
        "Calculate the time taken for a pion to travel between the two detectors in the frame "
        "of reference of the stationary observer, in seconds." + _SCI_HINT, t,
        [{"value": t, "mistake": None, "working": w1},
         {"value": _sig(gap / _C), "mistake": f"Use the pions' speed, {_b(beta)} × 3.00 × 10⁸ m/s, not c.", "working": w1},
         {"value": _sig(t / lor), "mistake": "No relativity is needed here — in the stationary observer's frame, the time is just distance ÷ speed.", "working": w1}],
        "s", [{"question": "What is v in m/s?", "answer": _sig(v)},
              {"question": "What is t in s?", "answer": t}], level)

    w2 = _l_forward_work(gap, beta, f"{_b(beta)}c", lp,
                         f"The detectors are at rest relative to the stationary observer, so l = {_txt(gap)} m. The pions measure l′, which must be shorter.")
    p2 = _part(
        "Calculate the distance between the two detectors in the frame of reference of the "
        "pions.", lp,
        [{"value": lp, "mistake": None, "working": w2},
         {"value": _sig(gap / lor), "mistake": f"Your answer is longer than {_txt(gap)} m — the 2022 course report flagged exactly this error. The detectors are at rest for the stationary observer, so {_txt(gap)} m is l; the pions measure a shorter l′.", "working": w2},
         {"value": _sig(gap * lor ** 2), "mistake": "Multiply by √(1−(v/c)²), not by (1−(v/c)²).", "working": w2}],
        "m", [{"question": "What is √(1 − (v/c)²)?", "answer": _sig(lor, 4)},
              {"question": "What is l′ in m?", "answer": lp}], level)

    p3 = _explain(
        "Explain why a greater number of pions reach the second detector than would be expected "
        "if relativistic effects were not taken into account. Write your answer in your jotter, "
        "then compare.",
        _EXPLAIN_FRAMES.format(obs="stationary observer's", p="pions",
                               d=f"distance between the detectors (less than {_txt(gap)} m)"), level)
    return _scenario(context, [p1, p2, p3], level)


# ── Simple (Newtonian) relative velocity ─────────────────────────────────────

# (label A, label B, location, speed lo, speed hi) — speeds tied to the objects.
_PARALLEL_CONTEXTS = [
    ("Train A", "Train B", "on parallel tracks", 15, 50),
    ("Car A", "Car B", "on a straight motorway", 15, 35),
    ("Cyclist A", "Cyclist B", "on a straight cycle path", 4, 14),
    ("Ferry A", "Ferry B", "in the Minch", 4, 10),
    ("Runner A", "Runner B", "on a straight running track", 3, 8),
]


def gen_relative_velocity_parallel(level="Higher"):
    """Speed of A relative to B: same or opposite directions (single step)."""
    label_a, label_b, location, lo, hi = random.choice(_PARALLEL_CONTEXTS)
    dp = 0 if hi > 20 else 1
    v1 = round(random.uniform(lo + 2, hi), dp)
    v2 = round(random.uniform(lo, v1 - 1), dp)
    same = random.choice([True, False])
    answer = round(v1 - v2 if same else v1 + v2, 1)
    direction = f"in the same direction as {label_a}" if same else f"in the opposite direction to {label_a}"
    question = (f"{label_a} travels at {v1:g} m/s relative to the ground. {label_b} travels at "
                f"{v2:g} m/s relative to the ground, {location}, {direction}. Determine the speed "
                f"of {label_a} relative to {label_b}.")
    work = [_T("Same direction → subtract the speeds." if same else "Opposite directions → add the speeds."),
            _L(rf"v = {v1:g} {'-' if same else '+'} {v2:g} = {answer:g}\ \mathrm{{m/s}}")]
    opts = [
        {"value": answer, "mistake": None, "working": work},
        {"value": round(v1 + v2 if same else v1 - v2, 1),
         "mistake": "They travel in the same direction, so subtract the speeds." if same else "They travel in opposite directions, so add the speeds.",
         "working": work},
        {"value": v1, "mistake": f"This ignores {label_b}'s motion — you must combine both speeds.", "working": work},
    ]
    return _num(question, answer, opts, "m/s", None, level)


# (vehicle, frame, walker, noun for the vehicle, vehicle lo, hi, walker lo, hi)
_WALK_CONTEXTS = [
    ("A CalMac ferry", "the sea", "A passenger", "ferry", 5.0, 9.0, 0.8, 1.8),
    ("A train", "the track", "A passenger", "train", 8.0, 30.0, 0.8, 1.8),
    ("A moving walkway", "the building", "A traveller", "walkway", 0.5, 1.0, 0.8, 1.6),
    ("A cruise ship", "the sea", "A crew member", "ship", 6.0, 11.0, 0.8, 2.0),
]


def gen_relative_velocity_walker(level="Higher"):
    vehicle, frame, walker, noun, vlo, vhi, wlo, whi = random.choice(_WALK_CONTEXTS)
    v = round(random.uniform(vlo, vhi), 2 if vhi < 2 else 1)
    w = round(random.uniform(wlo, whi), 1)
    forward = random.choice([True, False])
    if w >= v:
        forward = True  # walking backwards faster than a slow walkway moves reverses direction
    answer = round(v + w if forward else v - w, 2)
    way = "in the direction of travel" if forward else "against the direction of travel"
    question = (f"{vehicle} travels at {v:g} m/s relative to {frame}. {walker} walks {way} at "
                f"{w:g} m/s relative to the {noun}. Determine the speed of the "
                f"{walker.split(' ', 1)[1]} relative to {frame}.")
    work = [_L(rf"v = {v:g} {'+' if forward else '-'} {w:g} = {answer:g}\ \mathrm{{m/s}}")]
    opts = [
        {"value": answer, "mistake": None, "working": work},
        {"value": round(v - w if forward else v + w, 2),
         "mistake": "Walking in the direction of travel adds to the speed." if forward else "Walking against the direction of travel takes speed away — subtract.",
         "working": work},
        {"value": w, "mistake": f"That's the speed relative to the {noun}, not relative to {frame}.", "working": work},
    ]
    return _num(question, answer, opts, "m/s", None, level)


def gen_relative_velocity_three_body(level="Higher"):
    """Walker on one moving frame, compared with a second moving object — the
    2023 P2 Q4(b) type ('many candidates were unable to…') and 2016 walkway."""
    kind = random.choice(["trains", "walkway", "ferry"])
    if kind == "trains":
        va = round(random.uniform(2.5, 6.0), 1)
        vb = round(random.uniform(2.5, 6.0), 1)
        w = round(random.uniform(0.8, 1.8), 1)
        rear = random.choice([True, False])
        walker_ground = round(va - w if rear else va + w, 2)
        context = (f"Two trains travel side by side in the same direction along parallel tracks. "
                   f"Train A travels at {va:g} m/s and Train B at {vb:g} m/s, both relative to the "
                   f"platform. A passenger on Train A walks towards the {'rear' if rear else 'front'} "
                   f"of the train at {w:g} m/s relative to Train A. Determine the speed of the "
                   f"walking passenger relative to a passenger seated on Train B.")
        step1 = f"Walking passenger relative to platform = {va:g} {'−' if rear else '+'} {w:g} = {walker_ground:g} m/s"
        other = vb
        wrong_walk = round(va + w if rear else va - w, 2)
    elif kind == "walkway":
        vw = round(random.uniform(0.6, 1.0), 2)
        w = round(random.uniform(1.0, 1.5), 2)
        other = round(random.uniform(1.2, 2.2), 2)
        walker_ground = round(vw + w, 2)
        context = (f"A moving walkway travels at {vw:g} m/s relative to the building. A student "
                   f"walks along it, in the direction of travel, at {w:g} m/s relative to the "
                   f"walkway. A second student walks alongside the walkway at {other:g} m/s "
                   f"relative to the building, in the same direction. Determine the speed of the "
                   f"first student relative to the second student.")
        step1 = f"First student relative to building = {vw:g} + {w:g} = {walker_ground:g} m/s"
        wrong_walk = round(abs(vw - w), 2)
    else:
        vf = round(random.uniform(7.0, 10.0), 1)
        w = round(random.uniform(1.0, 2.0), 1)
        other = round(random.uniform(4.0, 9.0), 1)
        walker_ground = round(vf - w, 2)
        context = (f"A CalMac ferry sails at {vf:g} m/s relative to the sea. A passenger walks "
                   f"towards the stern (rear) at {w:g} m/s relative to the ferry. A RIB travels "
                   f"alongside, in the same direction, at {other:g} m/s relative to the sea. "
                   f"Determine the speed of the walking passenger relative to the RIB.")
        step1 = f"Passenger relative to sea = {vf:g} − {w:g} = {walker_ground:g} m/s"
        wrong_walk = round(vf + w, 2)
    answer = round(abs(walker_ground - other), 2)
    if answer < 0.1:
        return gen_relative_velocity_three_body(level)
    work = [_T("Step 1 — put the walker in the same frame as the other object:"), _T(step1),
            _T("Step 2 — both speeds are now relative to the same frame, so subtract:"),
            _L(rf"v = |{walker_ground:g} - {other:g}| = {answer:g}\ \mathrm{{m/s}}")]
    opts = [
        {"value": answer, "mistake": None, "working": work},
        {"value": round(abs(wrong_walk - other), 2), "mistake": "Check the walker's direction in step 1 — walking towards the rear subtracts from the vehicle's speed; walking forwards adds.", "working": work},
        {"value": walker_ground, "mistake": "That's the walker's speed relative to the ground — now compare it with the other object's speed.", "working": work},
        {"value": round(walker_ground + other, 2), "mistake": "Both move in the same direction, so subtract to find the relative speed.", "working": work},
    ]
    scaffold = [
        {"question": "Step 1: what is the walker's speed relative to the platform/building/sea (m/s)?", "answer": walker_ground},
        {"question": "Step 2: what is the relative speed (m/s)?", "answer": answer},
    ]
    return _num(context, answer, opts, "m/s", scaffold, level)


# ── Postulates, frames of reference and explanations ────────────────────────

def gen_inertial_frame(level="Higher"):
    part = _choice(
        "Which of the following best describes an inertial frame of reference?",
        "A frame of reference that is not accelerating — at rest or moving at constant velocity.",
        [("A frame of reference that is fixed to the surface of the Earth.",
          "Any frame moving at constant velocity (or at rest) is inertial — a spacecraft in deep space too."),
         ("A frame of reference that is accelerating uniformly.",
          "An accelerating frame is non-inertial — an inertial frame has zero acceleration."),
         ("A frame of reference in which the speed of light is not constant.",
          "The speed of light is the same in every inertial frame — that's the second postulate.")],
        level)
    return _scenario("", [part], level)


def gen_postulate_light_speed(level="Higher"):
    """Paper 2 'State the speed … Justify' (2016, 2023): 1 mark for the value
    WITH unit, 1 for the justification."""
    beta, v_txt, _ = _speed(0.30, 0.95, allow_ms=False)
    if random.choice([True, False]):
        context = (f"A spacecraft travels at a constant speed of {v_txt} relative to a stationary "
                   f"observer. The spacecraft emits a beam of light towards the observer.")
        q = "What speed does the stationary observer measure for the light? Choose the answer with the correct justification."
    else:
        context = (f"An astronaut travels directly towards a distant star at a constant speed of "
                   f"{v_txt} relative to the star.")
        q = "What speed does the astronaut measure for the light from the star? Choose the answer with the correct justification."
    correct = "3.00 × 10⁸ m/s — the speed of light is the same for all observers (in all inertial frames of reference)."
    part = _choice(q, correct, [
        (f"{_txt((1 + beta) * _C)} m/s — the speeds add, as they would for everyday objects.",
         "Speeds don't add to the speed of light — it is c for every observer (second postulate)."),
        (f"{_txt((1 - beta) * _C)} m/s — the relative speed is reduced.",
         "The measured speed of light doesn't depend on the motion of the source or observer."),
        ("3.00 × 10⁸ — the speed of light is the same for all observers.",
         "Right number and reason, but no unit. The marking instructions give 0 marks for a numerical speed without its unit."),
    ], level, working_text="Second postulate: the speed of light in a vacuum is the same for all observers, whatever the motion of the source or the observer.")
    return _scenario(context, [part], level)


def gen_light_speed_paper1(level="Higher"):
    """Paper 1 style (2017 Q6, 2019 Q9): numerical options around c."""
    beta = random.choice([0.10, 0.15, 0.20, 0.25, 0.30])
    in_ms = random.choice([True, False])
    craft_speed = f"{_txt(beta * _C, 2)} m/s" if in_ms else f"{beta:.2f}c"
    context = (f"A spacecraft is travelling at {craft_speed} relative to a star. An observer on "
               f"the spacecraft measures the speed of light emitted by the star.")
    fmt = (lambda k: f"{_txt(k * _C, 2)} m/s") if in_ms else (lambda k: f"{k:.2f}c")
    correct = fmt(1.0)
    wrong = [(fmt(1 - beta), "The observer's speed doesn't subtract from the speed of light — it is c for every observer."),
             (fmt(1 + beta), "The observer's speed doesn't add to the speed of light — it is c for every observer."),
             (fmt(math.sqrt(1 - beta ** 2)), "√(1−(v/c)²) is for time and length, not the speed of light — light is measured at c by every observer.")]
    seen, unique = {correct}, []
    for w in wrong:
        if w[0] not in seen:
            seen.add(w[0])
            unique.append(w)
    part = _choice("The measured speed of light is", correct, unique, level,
                   working_text="Second postulate: the speed of light in a vacuum is the same for all observers.")
    return _scenario(context, [part], level)


def gen_einstein_postulates(level="Higher"):
    part = _choice(
        "Which of the following correctly states Einstein's two postulates of special relativity?",
        "1) The laws of physics are the same in all inertial frames of reference. 2) The speed of "
        "light in a vacuum is the same for all observers.",
        [("1) The laws of physics are the same in all frames of reference, including accelerating "
          "ones. 2) The speed of light in a vacuum is the same for all observers.",
          "The first postulate applies to inertial (non-accelerating) frames only."),
         ("1) The laws of physics are the same in all inertial frames of reference. 2) The speed "
          "of light in a vacuum depends on the speed of the source.",
          "The speed of light does NOT depend on the motion of the source (or observer)."),
         ("1) Time and length are the same for every observer. 2) The speed of light adds to the "
          "velocity of the observer.",
          "Neither is a postulate — time and length are not absolute, and speeds do not add to c.")],
        level)
    return _scenario("", [part], level)


def gen_name_the_effect(level="Higher"):
    """2025 P2 Q4(a) — the report noted 'dilatation' was a common misspelling."""
    if random.choice([True, False]):
        q = ("A time interval measured by an observer who sees a clock moving at high speed is "
             "longer than the interval measured by an observer at rest relative to the clock. "
             "State the name of this effect.")
        correct = "Time dilation"
        wrong = [("Time dilatation", "Watch the spelling — it is dilation (the 2025 course report flagged ‘dilatation’ as a common error)."),
                 ("Length contraction", "Length contraction is about lengths, not time intervals."),
                 ("The Doppler effect", "The Doppler effect is a change in the frequency of a wave, not a time interval between events.")]
    else:
        q = ("The length of an object measured by an observer who sees it moving at high speed is "
             "shorter than the length measured by an observer at rest relative to it. State the "
             "name of this effect.")
        correct = "Length contraction"
        wrong = [("Time dilation", "Time dilation is about time intervals, not lengths."),
                 ("Length dilation", "Dilation means stretching — the moving object is measured shorter, so it is contraction."),
                 ("Redshift", "Redshift is a change in the wavelength of light, not in an object's length.")]
    return _scenario("", [_choice(q, correct, wrong, level)], level)


# (who, what they do, their claim) — all everyday speeds
_EVERYDAY = [
    ("An airline pilot", "flies long-haul routes at about 250 m/s", "their watch will run noticeably slow and must be reset regularly"),
    ("A train driver", "drives at 80 m/s over large distances", "they will need to reset their watch frequently"),
    ("A lorry driver", "drives about 100 000 km each year at 25 m/s", "their watch will be noticeably behind by the end of each year"),
    ("A CalMac captain", "sails between Uig and Tarbert several times a day at 8 m/s", "the ship's clock will fall noticeably behind the clocks on shore"),
]


def gen_everyday_speed(level="Higher"):
    """2025 P2 Q4(c): 'State whether the student is correct. Justify.'"""
    who, does, claim = random.choice(_EVERYDAY)
    context = f"{who} {does}. They claim that, because of time dilation, {claim}."
    part = _choice(
        "State whether the claim is correct, with the correct justification.",
        "Incorrect — this is not a relativistic speed (nowhere near c), so the time dilation is negligible.",
        [("Correct — any moving clock runs slow, so it will lose a noticeable amount of time.",
          "Time dilation does happen, but at this speed √(1−(v/c)²) is so close to 1 that the effect is far too small to notice."),
         ("Correct — the effect builds up over many hours of travel until it is noticeable.",
          "Even over a lifetime of travel at everyday speeds the difference is tiny — nowhere near enough to need a watch reset."),
         ("Incorrect — time dilation only affects light, not clocks.",
          "Time dilation affects all clocks and processes — but it is only significant at speeds close to c.")],
        level, working_text="Relativistic effects are only significant at speeds approaching c (roughly 0.1c or more). At everyday speeds they are negligible.")
    return _scenario(context, [part], level)


def gen_clock_statement_frame(level="Higher"):
    """2016 P2 Q4(b)(iii): the marking instructions accept correct, incorrect or
    'can't say' — but only with a frame of reference."""
    beta = random.choice([0.6, 0.8, 0.9, 0.95])
    context = (f"A spacecraft travels past Earth at {_b(beta)}c. A student states: "
               f"\"The clocks on board the spacecraft run slower.\"")
    part = _choice(
        "Which response best explains whether the student is correct?",
        "It depends on the frame of reference: in the frame of an observer on Earth the clocks "
        "run slow; in the crew's frame of reference the clocks are at rest and run normally.",
        [("Correct — the spacecraft is moving fast, so its clocks run slow.",
          "No frame of reference is named. The marking instructions require the answer to refer to (or imply) a frame — the crew see their own clocks running normally."),
         ("Correct — the crew notice their own clocks running slow.",
          "The crew are at rest relative to their clocks, so in their frame the clocks run normally."),
         ("Incorrect — clocks cannot be affected by speed.",
          "Moving clocks are measured to run slow by an observer who sees them moving (time dilation).")],
        level)
    return _scenario(context, [part], level)


def gen_rod_greater_length(level="Higher"):
    context = ("A rod is at rest on board a fast-moving spacecraft. Observer X travels alongside "
               "the rod on the spacecraft. Observer Y is stationary on Earth as the spacecraft "
               "passes.")
    part = _choice(
        "Which observer measures the greater length for the rod, and why?",
        "X — the rod is at rest in X's frame of reference, so X measures its proper length; in "
        "Y's frame the rod is moving, so its length is contracted.",
        [("Y — Y is stationary, so Y measures the true length.",
          "‘Stationary’ doesn't mean ‘proper’. The proper length is measured in the frame where the rod is at rest — the spacecraft."),
         ("Both measure the same length — the rod doesn't change.",
          "Y sees the rod moving at high speed, so Y measures a contracted length."),
         ("X — the rod is moving in X's frame of reference, so it is longer.",
          "The rod is at rest in X's frame — and moving objects are measured shorter, not longer.")],
        level)
    return _scenario(context, [part], level)


def gen_who_is_right_clocks(level="Higher"):
    context = (
        "A spacecraft travels at a constant, high speed relative to an observer on Earth. Both "
        "carry identical clocks.\n\n"
        "The astronaut says: \"My clock is running normally — it's the Earth observer's clock that "
        "is running slow.\"\n\n"
        "The Earth observer says: \"My clock is running normally — it's the astronaut's clock "
        "that is running slow.\""
    )
    part = _choice(
        "Who is correct?",
        "Both — each is at rest in their own inertial frame of reference and sees the other's "
        "clock moving, so each measures the other clock to run slow.",
        [("Only the astronaut — the spacecraft is the one that is really moving.",
          "There is no absolute motion — in the astronaut's frame, the Earth is moving past them."),
         ("Only the Earth observer — Earth is a fixed, stationary frame.",
          "Earth is not a special frame — it moves relative to the spacecraft just as much as the spacecraft moves relative to it."),
         ("Neither — both clocks must run at the same rate.",
          "Each observer genuinely measures the other's moving clock to run slow.")],
        level)
    return _scenario(context, [part], level)


def gen_who_is_right_muon(level="Higher"):
    context = (
        "A fast-moving muon is created high in the atmosphere and travels towards a detector on "
        "the ground before it decays.\n\n"
        "An observer on the ground says: \"The muon's decay clock is time dilated because it's "
        "moving so fast, so it survives long enough to reach the ground.\"\n\n"
        "An observer travelling with the muon says: \"My decay clock is running normally — it's "
        "the distance through the atmosphere that is length contracted.\""
    )
    part = _choice(
        "Who is correct?",
        "Both — time dilation (in the ground observer's frame of reference) and length "
        "contraction (in the muon's frame of reference) describe the same outcome.",
        [("Only the ground observer — length contraction isn't a real effect.",
          "Length contraction is just as real — it is the correct description in the muon's frame."),
         ("Only the muon's observer — time dilation isn't a real effect.",
          "Time dilation is the correct description in the ground frame."),
         ("Neither — the muon should decay before reaching the ground in both frames.",
          "That's the non-relativistic prediction — experimentally, more muons reach the ground than it allows.")],
        level)
    return _scenario(context, [part], level)


# ── Grouped generators, one per selectable sub-type in the app ──────────────

_VELOCITY_GENS = [gen_relative_velocity_parallel, gen_relative_velocity_walker,
                  gen_relative_velocity_three_body]
_TIME_DILATION_GENS = [gen_t_prime, gen_t_prime, gen_t_proper, gen_v_from_time_dilation,
                       gen_muon_scenario]
_LENGTH_CONTRACTION_GENS = [gen_l_prime, gen_l_prime_earth_object, gen_l_prime_earth_object,
                            gen_l_proper, gen_v_from_length_contraction, gen_pion_scenario]
_DEFINITIONS_GENS = [
    gen_inertial_frame,
    gen_postulate_light_speed,
    gen_light_speed_paper1,
    gen_einstein_postulates,
    gen_name_the_effect,
    gen_everyday_speed,
    gen_clock_statement_frame,
    gen_rod_greater_length,
    gen_who_is_right_clocks,
    gen_who_is_right_muon,
]
_ALL_GENS = _VELOCITY_GENS + _TIME_DILATION_GENS + _LENGTH_CONTRACTION_GENS + _DEFINITIONS_GENS


def _with_widget(q):
    q.metadata["widget_html"] = _WIDGET_HTML
    return q


def generate_special_relativity(level="Higher"):
    return _with_widget(random.choice(_ALL_GENS)(level=level))


def generate_relativity_velocity(level="Higher"):
    return _with_widget(random.choice(_VELOCITY_GENS)(level=level))


def generate_relativity_time_dilation(level="Higher"):
    return _with_widget(random.choice(_TIME_DILATION_GENS)(level=level))


def generate_relativity_length_contraction(level="Higher"):
    return _with_widget(random.choice(_LENGTH_CONTRACTION_GENS)(level=level))


def generate_relativity_definitions(level="Higher"):
    return _with_widget(random.choice(_DEFINITIONS_GENS)(level=level))
