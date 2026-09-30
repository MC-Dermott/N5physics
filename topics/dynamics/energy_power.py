"""N5 Energy — Power (P = E/t).

Basic: one-step P = E/t questions (find P, E or t) that test units — kW / MW, kJ / MJ and times in
minutes or hours must be converted — plus short multiple-choice checks on the unit of power and on
rearranging the equation.

Exam-style: multipart scenarios in the style of the Energy worksheet power section (Q42 onwards):
calculate the energy transferred first (Ep gained, Ek gained / lost, work done, or weight then Ep)
and then use it to find the power (or the time for a motor of known power).
"""
import math
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question
from utils.notes import NOTES
from topics.dynamics.energy import G, _big, _g_table, _num, _pick, round_sf

TOPIC, QTYPE = "Dynamics", "Energy"
_TIME_S = {"s": 1, "minutes": 60, "hours": 3600}
_PREFIX = {"W": 1, "kW": 1e3, "MW": 1e6, "J": 1, "kJ": 1e3, "MJ": 1e6}


def _L(s):
    return {"type": "latex", "content": s}


def _T(s):
    return {"type": "text", "content": s}


def _opt(value, mistake, working, unit):
    value = round_sf(value)
    return {"value": value, "display": f"{_big(value)} {unit}", "mistake": mistake, "working": working}


def _part(text, correct, opts, unit, notes, scaffold=None, level="N5"):
    """make_question with near-duplicate distractors dropped (some random values make two
    mistakes give the same number)."""
    kept = []
    for o in opts:
        if all(not math.isclose(o["value"], k["value"], rel_tol=0.03) for k in kept):
            kept.append(o)
    return make_question(text, correct, kept, unit, scaffold=scaffold, notes=notes,
                         topic=TOPIC, question_type=QTYPE, level=level)


def _explain(text, answer, notes, level="N5"):
    return PhysicsQuestion(question_text=text, correct_answer=0.0, unit="", topic=TOPIC,
                           question_type=QTYPE, level=level, notes=notes,
                           metadata={"type": "explain", "explain_text": answer})


def _scenario(context, parts, level="N5"):
    return PhysicsQuestion(question_text=context.split("\n\n")[0], correct_answer=0.0, unit="",
                           topic=TOPIC, question_type=QTYPE, level=level, is_scenario=True,
                           scenario_context=context, parts=parts)


def _time(lo, hi, step, unit):
    """Returns (t in s, value as given, unit as given, text)."""
    val = _pick(lo, hi, step)
    return val * _TIME_S[unit], val, unit, f"{_num(val)} {unit}"


def _t_conv(t_val, t_unit, t_s):
    """Working line converting a time to seconds (None if already in s)."""
    if t_unit == "s":
        return None
    per = _TIME_S[t_unit]
    return _L(rf"t = {_num(t_val)}\ \mathrm{{{t_unit}}} = {_num(t_val)} \times {per} = {_num(t_s)}\ \mathrm{{s}}")


def _t_scaffold(t_unit, t_s):
    return [{"question": "What is the time in seconds?", "answer": float(t_s), "unit": "s"}] if t_unit != "s" else []


def _energy_as_given(e_j):
    """An energy rounded to 3 s.f. in the unit an SQA question would quote it in.
    Returns (value, unit, value in J)."""
    unit = "MJ" if e_j >= 1e6 else "kJ" if e_j >= 1e4 else "J"
    val = round_sf(e_j / _PREFIX[unit])
    return val, unit, val * _PREFIX[unit]


# =========================================================
# Basic — P = E/t: units and rearranging
# Each context: power range in its own unit, time range in its own unit, and a sentence for
# each of the three forms ({E}, {P}, {t} are filled with values + units).
# =========================================================

_P_CTX = [
    dict(P=(2, 12, 0.5, "kW"), t=(20, 120, 5, "s"),
         fP="The motor on a crane transfers {E} of energy lifting a load for {t}. Calculate the power of the motor.",
         fE="The motor on a crane has a power of {P}. It lifts a load for {t}. Calculate the energy transferred by the motor.",
         ft="The motor on a crane has a power of {P}. Calculate the time taken for the motor to transfer {E} of energy."),
    dict(P=(300, 900, 10, "W"), t=(3, 12, 0.5, "s"),
         fP="A pupil running up a flight of stairs transfers {E} of energy in {t}. Calculate the power developed by the pupil.",
         fE="A pupil develops a power of {P} running up a flight of stairs in {t}. Calculate the energy transferred by the pupil.",
         ft="A pupil develops a power of {P} running up a flight of stairs. Calculate the time taken to transfer {E} of energy."),
    dict(P=(30, 90, 5, "kW"), t=(5, 20, 1, "s"),
         fP="A car engine transfers {E} of energy as the car accelerates for {t}. Calculate the power of the engine.",
         fE="A car engine has a power output of {P}. Calculate the energy it transfers in {t}.",
         ft="A car engine has a power output of {P}. Calculate the time taken for the engine to transfer {E} of energy."),
    dict(P=(150, 250, 10, "W"), t=(10, 45, 5, "minutes"),
         fP="The motor of an electric bike transfers {E} of energy during a journey lasting {t}. Calculate the power of the motor.",
         fE="The motor of an electric bike has a power of {P}. Calculate the energy transferred by the motor during a journey lasting {t}.",
         ft="The motor of an electric bike has a power of {P}. Calculate the time, in seconds, for the motor to transfer {E} of energy."),
    dict(P=(1.5, 3.5, 0.1, "MW"), t=(5, 30, 5, "minutes"),
         fP="A wind turbine on Lewis generates {E} of energy in {t}. Calculate the power output of the turbine.",
         fE="A wind turbine on Lewis has a power output of {P}. Calculate the energy it generates in {t}.",
         ft="A wind turbine on Lewis has a power output of {P}. Calculate the time, in seconds, taken to generate {E} of energy."),
    dict(P=(5, 15, 1, "kW"), t=(10, 40, 1, "s"),
         fP="A lift motor transfers {E} of energy raising the lift between floors in {t}. Calculate the power of the lift motor.",
         fE="A lift motor has a power of {P}. It raises the lift between floors in {t}. Calculate the energy transferred by the motor.",
         ft="A lift motor has a power of {P}. Calculate the time taken for the motor to transfer {E} of energy."),
    dict(P=(20, 60, 5, "kW"), t=(2, 8, 1, "minutes"),
         fP="The motor of a ski tow at Cairngorm transfers {E} of energy in {t}. Calculate the power of the motor.",
         fE="The motor of a ski tow at Cairngorm has a power of {P}. Calculate the energy it transfers in {t}.",
         ft="The motor of a ski tow at Cairngorm has a power of {P}. Calculate the time, in seconds, for it to transfer {E} of energy."),
    dict(P=(400, 1500, 50, "W"), t=(20, 60, 5, "s"),
         fP="A winch transfers {E} of energy pulling a boat up a slipway in {t}. Calculate the power of the winch.",
         fE="A winch with a power of {P} pulls a boat up a slipway for {t}. Calculate the energy transferred by the winch.",
         ft="A winch has a power of {P}. Calculate the time taken for it to transfer {E} of energy pulling a boat up a slipway."),
]


def _p_ctx():
    c = random.choice(_P_CTX)
    p_lo, p_hi, p_step, p_unit = c["P"]
    p_val = _pick(p_lo, p_hi, p_step)
    P = p_val * _PREFIX[p_unit]
    t_s, t_val, t_unit, t_txt = _time(*c["t"])
    return c, P, p_val, p_unit, t_s, t_val, t_unit, t_txt


def gen_power_find_p(level="N5"):
    c, P, _, _, t_s, t_val, t_unit, t_txt = _p_ctx()
    e_val, e_unit, E = _energy_as_given(P * t_s)
    correct = round_sf(E / t_s)

    working = [x for x in (_t_conv(t_val, t_unit, t_s),) if x] + (
        [_L(rf"E = {_num(e_val)}\ \mathrm{{{e_unit}}} = {_big(E)}\ \mathrm{{J}}")] if e_unit != "J" else []) + [
        _L(r"P = \frac{E}{t}"),
        _L(rf"P = \frac{{{_num(E)}}}{{{_num(t_s)}}}"),
        _L(rf"P = {_num(correct)}\ \mathrm{{W}}"),
    ]
    question = c["fP"].format(E=f"{_big(e_val)} {e_unit}", t=t_txt)
    opts = [_opt(correct, None, working, "W"),
            _opt(E * t_s, "You multiplied instead of dividing. P = E ÷ t.", working, "W"),
            _opt(t_s / E, "The fraction is upside down. P = E ÷ t.", working, "W")]
    if t_unit != "s":
        opts.append(_opt(E / t_val, f"The time must be in seconds — {t_txt} = {_num(t_s)} s.", working, "W"))
    if e_unit != "J":
        opts.append(_opt(e_val / t_s, f"The energy must be in joules — {_num(e_val)} {e_unit} = {_big(E)} J.", working, "W"))
    scaffold = _t_scaffold(t_unit, t_s) + (
        [{"question": "What is the energy in J?", "answer": E, "unit": "J"}] if e_unit != "J" else [])
    scaffold = scaffold + [{"question": "What is the power P?", "answer": correct, "unit": "W"}] if scaffold else None
    return _part(question, correct, opts, "W", NOTES["energy_power"], scaffold, level)


def gen_power_find_e(level="N5"):
    c, P, p_val, p_unit, t_s, t_val, t_unit, t_txt = _p_ctx()
    E = P * t_s
    ask_unit = "MJ" if E >= 1e7 else "kJ" if E >= 1e5 else "J"
    div = _PREFIX[ask_unit]
    correct = round_sf(E / div)

    working = [x for x in (_t_conv(t_val, t_unit, t_s),) if x] + (
        [_L(rf"P = {_num(p_val)}\ \mathrm{{{p_unit}}} = {_big(P)}\ \mathrm{{W}}")] if p_unit != "W" else []) + [
        _L(r"P = \frac{E}{t}"),
        _L(rf"{_num(P)} = \frac{{E}}{{{_num(t_s)}}}"),
        _L(rf"E = {_num(P)} \times {_num(t_s)} = {_big(E)}\ \mathrm{{J}}"),
    ]
    if div != 1:
        working.append(_L(rf"E = {_num(correct)}\ \mathrm{{{ask_unit}}}"))
    ask = f" Give your answer in {ask_unit}." if div != 1 else ""
    question = c["fE"].format(P=f"{_num(p_val)} {p_unit}", t=t_txt) + ask
    opts = [_opt(correct, None, working, ask_unit),
            _opt(P / t_s / div, "You divided instead of multiplying. E = P × t.", working, ask_unit),
            _opt(t_s / P / div, "You rearranged incorrectly. P = E ÷ t, so E = P × t.", working, ask_unit)]
    if t_unit != "s":
        opts.append(_opt(P * t_val / div, f"The time must be in seconds — {t_txt} = {_num(t_s)} s.", working, ask_unit))
    if p_unit != "W":
        opts.append(_opt(p_val * t_s / div, f"The power must be in watts — {_num(p_val)} {p_unit} = {_big(P)} W.", working, ask_unit))
    if div != 1:
        opts.append(_opt(E, f"You gave the answer in J. Divide by {int(div)} to convert to {ask_unit}.", working, ask_unit))
    scaffold = _t_scaffold(t_unit, t_s) + (
        [{"question": "What is the power in W?", "answer": P, "unit": "W"}] if p_unit != "W" else [])
    if div != 1:
        scaffold.append({"question": "What is the energy in J?", "answer": round_sf(E), "unit": "J"})
    scaffold = scaffold + [{"question": f"What is the energy in {ask_unit}?", "answer": correct, "unit": ask_unit}] if scaffold else None
    return _part(question, correct, opts, ask_unit, NOTES["energy_power"], scaffold, level)


def gen_power_find_t(level="N5"):
    c, P, p_val, p_unit, t_s, _, _, _ = _p_ctx()
    e_val, e_unit, E = _energy_as_given(P * t_s)
    correct = round_sf(E / P)

    working = ([_L(rf"P = {_num(p_val)}\ \mathrm{{{p_unit}}} = {_big(P)}\ \mathrm{{W}}")] if p_unit != "W" else []) + (
        [_L(rf"E = {_num(e_val)}\ \mathrm{{{e_unit}}} = {_big(E)}\ \mathrm{{J}}")] if e_unit != "J" else []) + [
        _L(r"P = \frac{E}{t}"),
        _L(rf"{_num(P)} = \frac{{{_num(E)}}}{{t}}"),
        _L(rf"t = \frac{{{_num(E)}}}{{{_num(P)}}}"),
        _L(rf"t = {_num(correct)}\ \mathrm{{s}}"),
    ]
    question = c["ft"].format(P=f"{_num(p_val)} {p_unit}", E=f"{_big(e_val)} {e_unit}")
    opts = [_opt(correct, None, working, "s"),
            _opt(P / E, "The fraction is upside down. t = E ÷ P.", working, "s"),
            _opt(E * P, "You multiplied instead of dividing. t = E ÷ P.", working, "s")]
    if p_unit != "W" or e_unit != "J":
        opts.append(_opt(e_val / p_val,
                         "Convert both values to base units (J and W) before dividing.", working, "s"))
        opts.append(_opt(E / p_val if p_unit != "W" else e_val / P,
                         (f"The power must be in watts — {_num(p_val)} {p_unit} = {_big(P)} W." if p_unit != "W"
                          else f"The energy must be in joules — {_num(e_val)} {e_unit} = {_big(E)} J."), working, "s"))
    scaffold = ([{"question": "What is the power in W?", "answer": P, "unit": "W"}] if p_unit != "W" else []) + (
        [{"question": "What is the energy in J?", "answer": E, "unit": "J"}] if e_unit != "J" else [])
    scaffold = scaffold + [{"question": "What is the time t?", "answer": correct, "unit": "s"}] if scaffold else None
    return _part(question, correct, opts, "s", NOTES["energy_power"], scaffold, level)


# (question, correct, [wrong options], explanation)
_UNIT_CASES = [
    ("What is the unit of power?", "watt (W)", ["joule (J)", "newton (N)", "second (s)"],
     "Power is measured in watts (W). Energy is in joules (J), force in newtons (N) and time in seconds (s)."),
    ("What does a power of 1 watt mean?", "1 joule of energy is transferred every second",
     ["1 joule of energy is transferred in total", "1 newton of force acts for 1 second",
      "1 second is taken to transfer any amount of energy"],
     "Power is the energy transferred per second: 1 W = 1 J/s."),
    ("Which of these is equal to 1 kW?", "1000 J/s", ["1000 J", "100 W", "1 000 000 W"],
     "kilo means × 1000, so 1 kW = 1000 W, and 1 W = 1 J/s, so 1 kW = 1000 J/s."),
    ("Which of these is equal to 2.5 MW?", "2 500 000 W", ["2500 W", "250 000 W", "2 500 000 000 W"],
     "mega means × 1 000 000, so 2.5 MW = 2.5 × 1 000 000 = 2 500 000 W."),
    ("A motor transfers energy E in a time t. Which equation gives the time t?", "t = E ÷ P",
     ["t = P ÷ E", "t = E × P", "t = P − E"],
     "Start from P = E ÷ t. Multiply both sides by t, then divide by P: t = E ÷ P."),
    ("Which equation gives the energy E transferred by a motor of power P in a time t?", "E = P × t",
     ["E = P ÷ t", "E = t ÷ P", "E = P + t"],
     "Start from P = E ÷ t and multiply both sides by t: E = P × t."),
    ("Before using P = E ÷ t, a time of 3 minutes must be written as", "180 s", ["3 s", "0.05 s", "300 s"],
     "Time must be in seconds: 3 minutes = 3 × 60 = 180 s."),
    ("Two motors lift identical loads through the same height. Motor A takes 10 s and motor B takes 20 s. "
     "Which statement is correct?", "Both transfer the same energy, but motor A has the greater power.",
     ["Motor A transfers more energy and has the greater power.",
      "Both transfer the same energy, but motor B has the greater power.",
      "Both motors have the same power."],
     "Both loads gain the same Ep (same m, g and h), so the same energy is transferred. "
     "Motor A transfers it in less time, so P = E ÷ t is greater for motor A."),
]


def gen_power_units(level="N5"):
    question, correct, wrong, reason = random.choice(_UNIT_CASES)
    working = [_T(reason)]
    options = [correct] + wrong
    random.shuffle(options)
    return PhysicsQuestion(question_text=question, correct_answer=correct, unit="",
                           distractors=[{"value": w, "mistake": reason, "working": working} for w in wrong],
                           working=working, notes=NOTES["energy_power"], topic=TOPIC, question_type=QTYPE,
                           level=level, metadata={"type": "classification", "options": options})


# =========================================================
# Exam-style — find the energy first, then the power
# =========================================================

_LOSS_EXPLAIN = ("Some energy is converted into heat (and sound) due to friction in the motor, gears and cables "
                 "(and air resistance). The motor must therefore transfer more energy than the Ep gained in the "
                 "same time, so its actual power is greater than calculated.")

# (sentence, mass unit, m_lo, m_hi, m_step, h_lo, h_hi, h_step, time range, what is lifted, machine)
_LIFT_CTX = [
    ("A crane lifts a steel beam of mass {m} through a height of {h}{t}.", "tonnes", 0.5, 2.0, 0.1,
     10, 40, 1, (20, 90, 5, "s"), "the steel beam", "the crane's motor"),
    ("A lift and its passengers have a total mass of {m}. The lift rises {h} between the ground floor and the top floor{t}.",
     "kg", 600, 1200, 50, 10, 30, 1, (10, 30, 1, "s"), "the lift and passengers", "the lift motor"),
    ("A chain lift pulls a roller-coaster car of mass {m} to the top of the first hill, {h} above the ground{t}.",
     "kg", 400, 900, 50, 20, 50, 1, (15, 40, 1, "s"), "the car", "the chain lift motor"),
    ("A hoist on a building site raises a load of bricks of mass {m} to a height of {h}{t}.", "kg", 100, 400, 10,
     5, 25, 1, (10, 40, 1, "s"), "the bricks", "the hoist motor"),
    ("A chairlift at Glencoe carries a skier of mass {m} up a vertical height of {h}{t}.", "kg", 55, 95, 1,
     150, 400, 10, (3, 8, 1, "minutes"), "the skier", "the chairlift motor"),
]


def _lift_values():
    sent, unit, mlo, mhi, mstep, hlo, hhi, hstep, trange, obj, machine = random.choice(_LIFT_CTX)
    m_val = _pick(mlo, mhi, mstep)
    m = m_val * (1000 if unit == "tonnes" else 1)
    h = _pick(hlo, hhi, hstep)
    ep = round_sf(m * G * h, 4)
    return sent, unit, m_val, m, h, ep, trange, obj, machine


def _ep_part(m_val, unit, m, h, ep, obj, level):
    conv = [_L(rf"m = {_num(m_val)}\ \mathrm{{tonnes}} \times 1000 = {_num(m)}\ \mathrm{{kg}}")] if unit == "tonnes" else []
    working = conv + [_L(r"E_p = mgh"),
                      _L(rf"E_p = {_num(m)} \times {G} \times {_num(h)}"),
                      _L(rf"E_p = {_big(ep, 4)}\ \mathrm{{J}}")]
    opts = [_opt(ep, None, working, "J"),
            _opt(m * h, "You forgot to multiply by g (9.8 N/kg). Ep = mgh.", working, "J"),
            _opt(m * G, "That is the weight (mg). Multiply by the height as well: Ep = mgh.", working, "J")]
    if unit == "tonnes":
        opts.append(_opt(m_val * G * h, "You did not convert tonnes into kilograms (× 1000).", working, "J"))
    scaffold = ([{"question": "What is the mass in kg?", "answer": m, "unit": "kg"}] if unit == "tonnes" else []) + [
        {"question": "What is m × g?", "answer": round_sf(m * G), "unit": "N"},
        {"question": "What is the gravitational potential energy gained?", "answer": round_sf(ep), "unit": "J"},
    ]
    return _part(f"Calculate the gravitational potential energy gained by {obj}.", round_sf(ep), opts, "J",
                 NOTES["energy_gpe"], scaffold, level)


def _power_part(text, E, e_label, t_s, t_val, t_unit, level, extra=()):
    """P = E/t where E comes from an earlier part. extra: additional (value, mistake) distractors."""
    correct = round_sf(E / t_s)
    working = [x for x in (_t_conv(t_val, t_unit, t_s),) if x] + [
        _T(f"Use the {e_label} from the previous part:"),
        _L(r"P = \frac{E}{t}"),
        _L(rf"P = \frac{{{_big(E, 4)}}}{{{_num(t_s)}}}"),
        _L(rf"P = {_num(correct)}\ \mathrm{{W}}"),
    ]
    opts = [_opt(correct, None, working, "W"),
            _opt(E * t_s, "You multiplied instead of dividing. P = E ÷ t.", working, "W"),
            _opt(t_s / E, "The fraction is upside down. P = E ÷ t.", working, "W")]
    if t_unit != "s":
        opts.append(_opt(E / t_val, f"The time must be in seconds — {_num(t_val)} {t_unit} = {_num(t_s)} s.", working, "W"))
    opts += [_opt(v, why, working, "W") for v, why in extra]
    scaffold = _t_scaffold(t_unit, t_s) + [
        {"question": f"What is the {e_label}, in J?", "answer": round_sf(E), "unit": "J"},
        {"question": "What is the power P?", "answer": correct, "unit": "W"},
    ]
    return _part(text, correct, opts, "W", NOTES["energy_power"], scaffold, level)


def gen_exam_lift_power(level="N5"):
    """Lift a load: (a) Ep gained, (b) power of the motor, (c) explain why the real power is greater."""
    sent, unit, m_val, m, h, ep, trange, obj, machine = _lift_values()
    t_s, t_val, t_unit, t_txt = _time(*trange)
    m_txt = f"{_num(m_val)} {unit}"
    context = (sent.format(m=m_txt, h=f"{_num(h)} m", t=f" in {t_txt}")
               + ("\n\n(1 tonne = 1000 kg)" if unit == "tonnes" else "") + f"\n\n{_g_table(G)}")
    part_a = _ep_part(m_val, unit, m, h, ep, obj, level)
    part_b = _power_part(f"Calculate the minimum power output of {machine}.", ep,
                         "gravitational potential energy gained", t_s, t_val, t_unit, level,
                         extra=[(m * G / t_s, "You divided the weight by the time. Use the energy (Ep) from part (a).")])
    part_c = _explain(f"The actual power of {machine} is greater than the value calculated. Explain why.",
                      _LOSS_EXPLAIN, NOTES["energy_power"], level)
    return _scenario(context, [part_a, part_b, part_c], level)


def gen_exam_lift_time(level="N5"):
    """Motor of known power: (a) Ep gained, (b) minimum time taken (t = E/P)."""
    sent, unit, m_val, m, h, ep, trange, obj, machine = _lift_values()
    t_guess = _pick(*trange[:3]) * _TIME_S[trange[3]]
    P = round_sf(ep / t_guess, 2)
    p_unit = "kW" if P >= 1e4 else "W"
    p_val = round_sf(P / _PREFIX[p_unit], 2)
    P = p_val * _PREFIX[p_unit]
    m_txt = f"{_num(m_val)} {unit}"
    context = (sent.format(m=m_txt, h=f"{_num(h)} m", t="") + f" The power output of {machine} is {_num(p_val)} {p_unit}."
               + ("\n\n(1 tonne = 1000 kg)" if unit == "tonnes" else "") + f"\n\n{_g_table(G)}")
    part_a = _ep_part(m_val, unit, m, h, ep, obj, level)

    correct = round_sf(ep / P)
    working = ([_L(rf"P = {_num(p_val)}\ \mathrm{{kW}} = {_big(P)}\ \mathrm{{W}}")] if p_unit == "kW" else []) + [
        _T("Use the gravitational potential energy from part (a):"),
        _L(r"P = \frac{E}{t}"),
        _L(rf"{_num(P)} = \frac{{{_big(ep, 4)}}}{{t}}"),
        _L(rf"t = \frac{{{_big(ep, 4)}}}{{{_num(P)}}}"),
        _L(rf"t = {_num(correct)}\ \mathrm{{s}}"),
    ]
    opts = [_opt(correct, None, working, "s"),
            _opt(P / ep, "The fraction is upside down. t = E ÷ P.", working, "s"),
            _opt(ep * P, "You multiplied instead of dividing. t = E ÷ P.", working, "s")]
    if p_unit == "kW":
        opts.append(_opt(ep / p_val, f"The power must be in watts — {_num(p_val)} kW = {_big(P)} W.", working, "s"))
    scaffold = ([{"question": "What is the power in W?", "answer": P, "unit": "W"}] if p_unit == "kW" else []) + [
        {"question": "What is the gravitational potential energy gained, in J?", "answer": round_sf(ep), "unit": "J"},
        {"question": "What is the time t?", "answer": correct, "unit": "s"},
    ]
    part_b = _part(f"Calculate the minimum time taken to raise {obj} through this height.", correct, opts, "s",
                   NOTES["energy_power"], scaffold, level)
    part_c = _explain("In practice, the time taken is longer than the value calculated. Explain why.",
                      "Some energy is converted into heat (and sound) due to friction in the motor, gears and cables. "
                      "Less of the energy supplied each second becomes Ep, so it takes longer to transfer the Ep needed.",
                      NOTES["energy_power"], level)
    return _scenario(context, [part_a, part_b, part_c], level)


# (subject, mass unit, m_lo, m_hi, m_step, v_lo, v_hi, time range, can start moving, power holder)
_ACCEL_CTX = [
    ("A car", "tonnes", 1.0, 1.8, 0.1, 12, 28, (6, 15, 1, "s"), True, "the car's engine"),
    ("A sprinter", "kg", 55, 85, 1, 8, 11, (2, 4, 0.5, "s"), False, "the sprinter"),
    ("A cyclist and bike, of total mass {m},", "kg", 70, 100, 5, 6, 12, (5, 15, 1, "s"), True, "the cyclist"),
    ("A lorry", "tonnes", 10, 20, 1, 10, 20, (20, 40, 1, "s"), True, "the lorry's engine"),
    ("A ScotRail train", "tonnes", 150, 300, 10, 20, 35, (1, 3, 0.5, "minutes"), True, "the train's engines"),
]


def _ek_working(m, v, ek):
    return [_L(r"E_k = \frac{1}{2}mv^2"),
            _L(rf"E_k = \frac{{1}}{{2}} \times {_num(m)} \times {v}^2"),
            _L(rf"E_k = {_big(ek, 4)}\ \mathrm{{J}}")]


def _ek_opts(m, m_val, unit, v, ek, working):
    opts = [_opt(ek, None, working, "J"),
            _opt(m * v ** 2, "You forgot the ½. Ek = ½mv².", working, "J"),
            _opt(0.5 * m * v, "You forgot to square the speed. Ek = ½mv².", working, "J")]
    if unit == "tonnes":
        opts.append(_opt(0.5 * m_val * v ** 2, "You did not convert tonnes into kilograms (× 1000).", working, "J"))
    return opts


def gen_exam_accelerate_power(level="N5"):
    """Vehicle speeds up: Ek (initial and) final, then the average power."""
    subj, unit, mlo, mhi, mstep, vlo, vhi, trange, can_move, holder = random.choice(_ACCEL_CTX)
    m_val = _pick(mlo, mhi, mstep)
    m = m_val * (1000 if unit == "tonnes" else 1)
    v = random.randint(vlo, vhi)
    u = random.randint(3, v // 2) if can_move and random.random() < 0.45 else 0
    t_s, t_val, t_unit, t_txt = _time(*trange)
    m_txt = f"{_num(m_val)} {unit}"
    conv = [_L(rf"m = {_num(m_val)}\ \mathrm{{tonnes}} \times 1000 = {_num(m)}\ \mathrm{{kg}}")] if unit == "tonnes" else []
    m_scaffold = [{"question": "What is the mass in kg?", "answer": m, "unit": "kg"}] if unit == "tonnes" else []

    if "{m}" in subj:
        who = subj.format(m=m_txt)
    else:
        who = f"{subj} of mass {m_txt}"
    start = f"from {u} m/s" if u else "from rest"
    context = (f"{who} accelerates {start} to {v} m/s in {t_txt}."
               + ("\n\n(1 tonne = 1000 kg)" if unit == "tonnes" else ""))

    ek_v = round_sf(0.5 * m * v ** 2, 4)
    parts = []
    if u:
        ek_u = round_sf(0.5 * m * u ** 2, 4)
        w_u = conv + _ek_working(m, u, ek_u)
        parts.append(_part(f"Calculate the kinetic energy at {u} m/s.", round_sf(ek_u),
                           _ek_opts(m, m_val, unit, u, ek_u, w_u), "J", NOTES["energy_ke"],
                           m_scaffold + [{"question": "What is the kinetic energy, Ek?", "answer": round_sf(ek_u), "unit": "J"}],
                           level))
        w_v = conv + _ek_working(m, v, ek_v)
        parts.append(_part(f"Calculate the kinetic energy at {v} m/s.", round_sf(ek_v),
                           _ek_opts(m, m_val, unit, v, ek_v, w_v), "J", NOTES["energy_ke"],
                           m_scaffold + [{"question": "What is the kinetic energy, Ek?", "answer": round_sf(ek_v), "unit": "J"}],
                           level))
        gained = ek_v - ek_u
        parts.append(_power_part(f"Calculate the average power developed by {holder} while accelerating.",
                                 gained, "kinetic energy gained (final Ek − initial Ek)", t_s, t_val, t_unit, level,
                                 extra=[(ek_v / t_s, "You used the final Ek only. The energy transferred is the Ek "
                                                     "gained: final Ek − initial Ek."),
                                        (0.5 * m * (v - u) ** 2 / t_s, "Work out each Ek separately and subtract — "
                                                                      "½m(v − u)² is not the Ek gained.")]))
    else:
        w_v = conv + _ek_working(m, v, ek_v)
        parts.append(_part("Calculate the kinetic energy gained.", round_sf(ek_v),
                           _ek_opts(m, m_val, unit, v, ek_v, w_v), "J", NOTES["energy_ke"],
                           m_scaffold + [{"question": "What is v²?", "answer": v ** 2},
                                         {"question": "What is the kinetic energy gained, Ek?", "answer": round_sf(ek_v), "unit": "J"}],
                           level))
        parts.append(_power_part(f"Calculate the average power developed by {holder}.", ek_v,
                                 "kinetic energy gained", t_s, t_val, t_unit, level,
                                 extra=[(m * v ** 2 / t_s, "Check part (a) — Ek = ½mv² (you left out the ½).")]))
    return _scenario(context, parts, level)


# (sentence, F unit, F range, d unit, d range, time range, doer)
_PULL_CTX = [
    ("A tractor pulls a trailer of hay along a croft track with a constant force of {F} for a distance of {d}{t}.",
     "N", (1000, 2500, 100), "m", (100, 400, 10), (30, 120, 5, "s"), "the tractor"),
    ("A horse pulls a cart with a force of {F} for a distance of {d}{t}.",
     "N", (500, 1000, 50), "m", (100, 500, 10), (1, 4, 0.5, "minutes"), "the horse"),
    ("A team of huskies pulls a sledge with a force of {F} for a distance of {d}{t}.",
     "N", (200, 600, 20), "m", (200, 800, 50), (1, 4, 0.5, "minutes"), "the huskies"),
    ("A tug boat pulls a tanker out of Grangemouth harbour with a force of {F} for a distance of {d}{t}.",
     "kN", (50, 150, 10), "km", (1.0, 3.0, 0.1), (5, 20, 1, "minutes"), "the tug boat's engines"),
    ("A winch pulls a boat {d} up a slipway with a force of {F}{t}.",
     "N", (200, 800, 50), "m", (5, 25, 1), (10, 60, 5, "s"), "the winch"),
]


def gen_exam_work_power(level="N5"):
    """Force over a distance: (a) work done, (b) power."""
    sent, fu, frange, du, drange, trange, doer = random.choice(_PULL_CTX)
    F_val, d_val = _pick(*frange), _pick(*drange)
    F = F_val * (1000 if fu == "kN" else 1)
    d = d_val * (1000 if du == "km" else 1)
    t_s, t_val, t_unit, t_txt = _time(*trange)
    ew = round_sf(F * d, 4)
    context = sent.format(F=f"{_num(F_val)} {fu}", d=f"{_num(d_val)} {du}", t=f" in {t_txt}")

    conv = ([_L(rf"F = {_num(F_val)}\ \mathrm{{kN}} = {_num(F)}\ \mathrm{{N}}")] if fu == "kN" else []) + (
        [_L(rf"d = {_num(d_val)}\ \mathrm{{km}} = {_num(d)}\ \mathrm{{m}}")] if du == "km" else [])
    working = conv + [_L(r"E_W = Fd"), _L(rf"E_W = {_num(F)} \times {_num(d)}"), _L(rf"E_W = {_big(ew, 4)}\ \mathrm{{J}}")]
    opts = [_opt(ew, None, working, "J"),
            _opt(F / d, "You divided instead of multiplying. Ew = F × d.", working, "J"),
            _opt(F * d / t_s, "You divided by the time — that is the power. Ew = Fd does not involve time.", working, "J")]
    if fu == "kN" or du == "km":
        opts.append(_opt(F_val * d_val, "Convert kN to N and km to m before substituting.", working, "J"))
    scaffold = ([{"question": "What is the force in N?", "answer": F, "unit": "N"}] if fu == "kN" else []) + (
        [{"question": "What is the distance in m?", "answer": d, "unit": "m"}] if du == "km" else []) + [
        {"question": "What is the work done, Ew?", "answer": round_sf(ew), "unit": "J"}]
    part_a = _part(f"Calculate the work done by {doer}.", round_sf(ew), opts, "J", NOTES["energy_work"], scaffold, level)
    part_b = _power_part(f"Calculate the power developed by {doer}.", ew, "work done", t_s, t_val, t_unit, level,
                         extra=[(F / t_s, "You divided the force by the time. Power = work done ÷ time.")])
    return _scenario(context, [part_a, part_b], level)


def gen_exam_stairs_power(level="N5"):
    """Pupil runs upstairs: (a) weight, (b) Ep gained (= weight × height), (c) power."""
    name = random.choice(["A pupil", "A firefighter", "A hillwalker", "A student"])
    m = _pick(45, 90, 1) if name != "A firefighter" else _pick(90, 120, 1)   # firefighter includes kit
    if name == "A hillwalker":
        h = _pick(150, 450, 10)
        t_s, t_val, t_unit, t_txt = _time(20, 60, 5, "minutes")
        where = f"climbs a hill, gaining {_num(h)} m in height, in {t_txt}"
    else:
        h = _pick(3.0, 12.0, 0.5)
        t_s, t_val, t_unit, t_txt = _time(3, 12, 0.5, "s")
        where = f"runs up a flight of stairs with a vertical height of {_num(h)} m in {t_txt}"
    mass = f"total mass {_num(m)} kg (including equipment)" if name == "A firefighter" else f"mass {_num(m)} kg"
    context = f"{name} of {mass} {where}.\n\n{_g_table(G)}"

    W = round_sf(m * G, 4)
    w_work = [_L(r"W = mg"), _L(rf"W = {_num(m)} \times {G}"), _L(rf"W = {_num(W, 4)}\ \mathrm{{N}}")]
    part_a = _part("Calculate the weight.", round_sf(W),
                   [_opt(W, None, w_work, "N"),
                    _opt(m / G, "You divided instead of multiplying. W = mg.", w_work, "N"),
                    _opt(m, "That is the mass in kg. Weight is a force: W = mg.", w_work, "N")],
                   "N", NOTES["energy_gpe"], None, level)

    ep = round_sf(W * h, 4)
    e_work = [_T("The energy gained is the gravitational potential energy (weight × height):"),
              _L(r"E_p = mgh"), _L(rf"E_p = {_num(m)} \times {G} \times {_num(h)}"), _L(rf"E_p = {_big(ep, 4)}\ \mathrm{{J}}")]
    part_b = _part("Calculate the gravitational potential energy gained.", round_sf(ep),
                   [_opt(ep, None, e_work, "J"),
                    _opt(m * h, "You forgot g. Ep = mgh (or weight × height).", e_work, "J"),
                    _opt(W / h, "You divided the weight by the height. Ep = weight × height.", e_work, "J")],
                   "J", NOTES["energy_gpe"],
                   [{"question": "What is the weight, from part (a)?", "answer": round_sf(W), "unit": "N"},
                    {"question": "What is the gravitational potential energy gained?", "answer": round_sf(ep), "unit": "J"}],
                   level)
    part_c = _power_part("Calculate the average power developed.", ep, "gravitational potential energy gained",
                         t_s, t_val, t_unit, level,
                         extra=[(W / t_s, "You divided the weight by the time. Use the energy (Ep) from part (b)."),
                                (m * h / t_s, "Check part (b) — Ep = mgh (you left out g).")])
    return _scenario(context, [part_a, part_b, part_c], level)


# (vehicle, m_lo, m_hi, m_step, v_lo, v_hi, d_lo, d_hi, t_lo, t_hi)
_BRAKE_CTX = [
    ("car", 900, 1800, 100, 12, 30, 20, 60, 3, 8),
    ("van", 1800, 3000, 100, 12, 25, 25, 60, 4, 9),
    ("motorbike", 200, 400, 20, 10, 25, 15, 45, 3, 7),
    ("cyclist and bike", 70, 100, 5, 5, 12, 5, 15, 2, 5),
]


def gen_exam_braking_power(level="N5"):
    """Braking to rest: (a) Ek lost, (b) average braking force, (c) average power of the brakes."""
    veh, mlo, mhi, mstep, vlo, vhi, dlo, dhi, tlo, thi = random.choice(_BRAKE_CTX)
    m, v = _pick(mlo, mhi, mstep), random.randint(vlo, vhi)
    d, t_s = random.randint(dlo, dhi), random.randint(tlo, thi)
    context = (f"A {veh} of {'total ' if veh == 'cyclist and bike' else ''}mass {_num(m)} kg is travelling at {v} m/s. "
               f"The brakes are applied and it comes to rest in a distance of {d} m, taking {t_s} s.")

    ek = round_sf(0.5 * m * v ** 2, 4)
    w_ek = _ek_working(m, v, ek)
    part_a = _part("Calculate the kinetic energy lost.", round_sf(ek), _ek_opts(m, m, "kg", v, ek, w_ek), "J",
                   NOTES["energy_ke"], None, level)

    F = round_sf(ek / d)
    w_f = [_T("All of the Ek is transferred by the work done by the brakes:"),
           _L(r"E_W = Fd"), _L(rf"{_big(ek, 4)} = F \times {d}"), _L(rf"F = {_num(F)}\ \mathrm{{N}}")]
    part_b = _part("Calculate the average braking force.", F,
                   [_opt(F, None, w_f, "N"),
                    _opt(ek * d, "You multiplied by the distance. F = Ew ÷ d.", w_f, "N"),
                    _opt(ek / t_s, "You divided by the time — that is the power. F = Ew ÷ d.", w_f, "N")],
                   "N", NOTES["energy_conservation"],
                   [{"question": "What is the work done by the brakes, in J?", "answer": round_sf(ek), "unit": "J"},
                    {"question": "What is the braking force F?", "answer": F, "unit": "N"}], level)

    part_c = _power_part("Calculate the average power of the brakes.", ek, "kinetic energy lost", t_s, t_s, "s", level,
                         extra=[(F / t_s, "You divided the braking force by the time. Power = energy ÷ time — "
                                          "use the Ek from part (a).")])
    return _scenario(context, [part_a, part_b, part_c], level)


_BASIC_GENS = [gen_power_find_p, gen_power_find_e, gen_power_find_t]
_EXAM_GENS  = [gen_exam_lift_power, gen_exam_lift_time, gen_exam_accelerate_power,
               gen_exam_work_power, gen_exam_stairs_power, gen_exam_braking_power]


def generate_power_basic(level="N5"):
    # mostly calculations; roughly one in five is a unit / rearranging check
    if random.random() < 0.2:
        return gen_power_units(level=level)
    return random.choice(_BASIC_GENS)(level=level)


def generate_power_exam(level="N5"):
    return random.choice(_EXAM_GENS)(level=level)
