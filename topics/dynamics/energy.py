import math
import random
from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question
from utils.notes import NOTES


def round_sf(value, sf=3):
    return float(f"{value:.{sf}g}")


def fmt_J(j):
    j = float(j)
    if abs(j) >= 1_000_000:
        return f"{j / 1_000_000:g} MJ"
    if abs(j) >= 1000:
        return f"{j / 1000:g} kJ"
    return f"{j:g} J"


def _g_table(g):
    return f"| Constant | Value |\n|---|---|\n| g | {g} N/kg |"


def _distinct_options(gen):
    """Re-roll a generator until its distractors are all different from each
    other and from the correct answer (some random values make them coincide)."""
    def wrapped(level="N5"):
        for _ in range(20):
            q = gen(level=level)
            vals = [round(float(d["value"]), 6) for d in q.distractors]
            ca = float(q.correct_answer) if not isinstance(q.correct_answer, str) else None
            near = ca is not None and any(abs(v - ca) <= 0.02 * abs(ca) for v in vals)
            if len(vals) == 3 and len(set(vals)) == 3 and not near:
                break
        return q
    wrapped.__name__ = gen.__name__
    return wrapped


G = 9.8   # N/kg — N5 data sheet value for Earth


def _num(x, sf=3):
    """Pupil-facing number: rounded to sf, never in scientific notation."""
    x = float(f"{x:.{sf}g}")
    return f"{int(x)}" if x == int(x) else f"{x:f}".rstrip("0").rstrip(".")


def _big(x, sf=3):
    """_num for question text, with SQA-style space grouping (4 500 000)."""
    t = _num(x, sf)
    whole, _, frac = t.partition(".")
    if len(whole) > 4:
        whole = f"{int(whole):,}".replace(",", " ")
    return whole + ("." + frac if frac else "")


def _mass(ctx):
    """ctx = (name, unit, lo, hi, step) with unit "g", "kg" or "tonnes".
    Returns (mass_kg, mass_text, unit_as_given, value_as_given)."""
    name, unit, lo, hi, step = ctx[:5]
    val = round(random.choice([lo + i * step for i in range(int(round((hi - lo) / step)) + 1)]), 3)
    kg = {"g": val / 1000, "kg": val, "tonnes": val * 1000}[unit]
    return round(kg, 6), f"{_big(val)} {unit}", unit, val


def _to_kg_step(unit, val, kg):
    """Working/scaffold line converting a given mass to kg (None if already kg)."""
    if unit == "g":
        return f"m = {_num(val)}\\ \\mathrm{{g}} \\div 1000 = {_num(kg)}\\ \\mathrm{{kg}}"
    if unit == "tonnes":
        return f"m = {_num(val)}\\ \\mathrm{{tonnes}} \\times 1000 = {_num(kg)}\\ \\mathrm{{kg}}"
    return None


def _unit_mistake(unit):
    return {"g": "You did not convert grams into kilograms (÷ 1000).",
            "tonnes": "You did not convert tonnes into kilograms (× 1000)."}.get(unit)


# =========================================================
# GPE — Ep = mgh
# Context tuples tie each object to a sensible mass (kg) and height (m) range.
# =========================================================

_GPE_CTX = [
    # (object, unit, m_lo, m_hi, m_step, h_lo, h_hi, h_step, sentence)
    ("box of books",       "kg", 2, 8, 0.5, 1.0, 2.0, 0.1, "is lifted onto a shelf {h} m high"),
    ("bag of seed potatoes", "kg", 10, 25, 5, 0.8, 1.5, 0.1, "is lifted onto a trailer {h} m high"),
    ("hillwalker",         "kg", 50, 90, 1, 200, 800, 10, "climbs a hill, gaining {h} m in height"),
    ("pupil",              "kg", 40, 70, 1, 3.0, 12.0, 0.5, "climbs a flight of stairs {h} m high"),
    ("shipping container", "kg", 1000, 3000, 100, 5, 20, 1, "is lifted {h} m by a harbour crane"),
    ("drone",              "kg", 0.8, 3.0, 0.1, 20, 120, 5, "rises vertically through {h} m"),
    ("football",           "kg", 0.40, 0.45, 0.05, 3.0, 8.0, 0.5, "lands on a roof {h} m above the ground"),
]


def _gpe_ctx():
    c = random.choice(_GPE_CTX)
    obj, _, mlo, mhi, mstep, hlo, hhi, hstep, sentence = c
    m, m_txt, _, _ = _mass((obj, "kg", mlo, mhi, mstep))
    n_h = int(round((hhi - hlo) / hstep))
    h = round(hlo + random.randint(0, n_h) * hstep, 2)
    return obj, m, m_txt, h, sentence.format(h=_num(h))


def gen_gpe(level="N5"):
    obj, m, m_txt, h, action = _gpe_ctx()
    correct = round_sf(m * G * h)
    working = [
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"E_p = {_num(m)} \times {G} \times {_num(h)}"},
        {"type": "latex", "content": rf"E_p = {_num(correct)}\ \mathrm{{J}}"},
    ]
    question = (f"A {obj} of mass {m_txt} {action}. Calculate the gravitational potential energy gained."
                f"\n\n{_g_table(G)}")
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(m / (G * h)), "mistake": "You rearranged the equation incorrectly. Ep = mgh.", "working": working},
        {"value": round_sf(m * h), "mistake": "You forgot to multiply by g (9.8 N/kg).", "working": working},
        {"value": round_sf(m * G + h), "mistake": "You used the equation incorrectly. Ep = m × g × h.", "working": working},
    ]
    scaffold = [
        {"question": "What is m × g?", "answer": round_sf(m * G)},
        {"question": "What is the gravitational potential energy Ep?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "J", notes=NOTES["energy_gpe"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


def gen_gpe_mass(level="N5"):
    obj, m, _, h, action = _gpe_ctx()
    energy = round_sf(m * G * h, 4)
    correct = round_sf(energy / (G * h))
    working = [
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"{_num(energy, 4)} = m \times {G} \times {_num(h)}"},
        {"type": "latex", "content": rf"m = \frac{{{_num(energy, 4)}}}{{{G} \times {_num(h)}}}"},
        {"type": "latex", "content": rf"m = {_num(correct)}\ \mathrm{{kg}}"},
    ]
    question = (f"A {obj} {action} and gains {_big(energy, 4)} J of gravitational potential energy. "
                f"Calculate the mass of the {obj}.\n\n{_g_table(G)}")
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(energy * G * h), "mistake": "You rearranged the equation incorrectly. m = Ep ÷ (g × h).", "working": working},
        {"value": round_sf(correct * 1000), "mistake": "You gave the answer in grams, not kilograms.", "working": working},
        {"value": round_sf(energy / G), "mistake": "You forgot to divide by h as well as g.", "working": working},
    ]
    scaffold = [
        {"question": "What is g × h?", "answer": round_sf(G * h)},
        {"question": "What is the mass m?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "kg", notes=NOTES["energy_gpe"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


def gen_gpe_height(level="N5"):
    obj, m, m_txt, h, action = _gpe_ctx()
    energy = round_sf(m * G * h, 4)
    correct = round_sf(energy / (m * G))
    working = [
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"{_num(energy, 4)} = {_num(m)} \times {G} \times h"},
        {"type": "latex", "content": rf"h = \frac{{{_num(energy, 4)}}}{{{_num(m)} \times {G}}}"},
        {"type": "latex", "content": rf"h = {_num(correct)}\ \mathrm{{m}}"},
    ]
    question = (f"A {obj} of mass {m_txt} gains {_big(energy, 4)} J of gravitational potential energy "
                f"as it is raised. Calculate the height it is raised.\n\n{_g_table(G)}")
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(energy * m * G), "mistake": "You rearranged the equation incorrectly. h = Ep ÷ (m × g).", "working": working},
        {"value": round_sf(energy / m), "mistake": "You forgot to divide by g as well.", "working": working},
        {"value": round_sf(energy / G), "mistake": "You forgot to divide by m as well.", "working": working},
    ]
    scaffold = [
        {"question": "What is m × g?", "answer": round_sf(m * G)},
        {"question": "What is the height h?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "m", notes=NOTES["energy_gpe"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


# =========================================================
# KE — Ek = ½mv²  (tests units: g → kg, tonnes → kg, kJ / MJ)
# Context tuples: (object, mass unit, lo, hi, step, v_lo, v_hi)
# =========================================================

_KE_CTX = [
    ("golf ball",          "g",      44, 46, 1,     40, 70),
    ("tennis ball",        "g",      56, 58, 1,     20, 50),
    ("cricket ball",       "g",      155, 165, 5,   20, 35),
    ("football",           "g",      400, 450, 10,  10, 25),
    ("hockey ball",        "g",      150, 165, 5,   10, 30),
    ("cyclist and bike",   "kg",     70, 100, 5,    5, 12),
    ("runner",             "kg",     50, 80, 1,     4, 9),
    ("car",                "tonnes", 1.0, 1.8, 0.1, 10, 30),
    ("van",                "tonnes", 2.0, 3.5, 0.1, 10, 25),
    ("lorry",              "tonnes", 10, 20, 1,     10, 25),
    ("CalMac ferry",       "tonnes", 3000, 5000, 100, 6, 9),
]


def _ke_ctx():
    c = random.choice(_KE_CTX)
    m, m_txt, unit, val = _mass(c)
    v = random.randint(c[5], c[6])
    return c[0], m, m_txt, unit, val, v


def _energy_unit_for(ek):
    """Pick the unit a 'give your answer in …' question asks for."""
    if ek >= 1e6:
        return "MJ", 1e6
    if ek >= 1e4:
        return "kJ", 1e3
    return "J", 1


def gen_ke(level="N5"):
    obj, m, m_txt, unit, val, v = _ke_ctx()
    ek = 0.5 * m * v ** 2
    e_unit, e_div = _energy_unit_for(ek)
    correct = round_sf(ek / e_div)
    conv = _to_kg_step(unit, val, m)

    working = ([{"type": "latex", "content": conv}] if conv else []) + [
        {"type": "latex", "content": r"E_k = \frac{1}{2}mv^2"},
        {"type": "latex", "content": rf"E_k = \frac{{1}}{{2}} \times {_num(m)} \times {v}^2"},
        {"type": "latex", "content": rf"E_k = {_num(ek, 4)}\ \mathrm{{J}}"},
    ]
    if e_div != 1:
        working.append({"type": "latex", "content": rf"E_k = {_num(correct)}\ \mathrm{{{e_unit}}}"})
    ask = f" Give your answer in {e_unit}." if e_div != 1 else ""
    question = (f"A {obj} of mass {m_txt} is moving at {v} m/s. Calculate its kinetic energy.{ask}"
                + ("\n\n(1 tonne = 1000 kg)" if unit == "tonnes" else ""))

    unit_err = round_sf(0.5 * val * v ** 2 / e_div) if unit != "kg" else round_sf(ek)  # ek (J) when asked kJ/MJ
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(m * v ** 2 / e_div), "mistake": "You forgot the ½ in the equation. Ek = ½mv².", "working": working},
        {"value": round_sf(0.5 * m * v / e_div), "mistake": "You forgot to square the speed. Ek = ½mv².", "working": working},
        {"value": unit_err,
         "mistake": _unit_mistake(unit) or f"You gave the answer in J. Divide by {int(e_div)} to convert to {e_unit}.",
         "working": working},
    ]
    scaffold = ([{"question": "What is the mass in kg?", "answer": m, "unit": "kg"}] if conv else []) + [
        {"question": "What is v²?", "answer": v ** 2},
        {"question": "What is the kinetic energy in J?", "answer": round_sf(ek), "unit": "J"},
    ]
    if e_div != 1:
        scaffold.append({"question": f"What is the kinetic energy in {e_unit}?", "answer": correct, "unit": e_unit})
    return make_question(question, correct, options_data, e_unit, notes=NOTES["energy_ke"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


def gen_ke_mass(level="N5"):
    obj, m, _, _, _, v = _ke_ctx()
    ek = 0.5 * m * v ** 2
    e_unit, e_div = _energy_unit_for(ek)
    e_given = round_sf(ek / e_div, 3)
    ek_j = e_given * e_div
    correct = round_sf(2 * ek_j / v ** 2)

    conv = [{"type": "latex", "content": rf"E_k = {_num(e_given)}\ \mathrm{{{e_unit}}} = {_num(ek_j)}\ \mathrm{{J}}"}] if e_div != 1 else []
    working = conv + [
        {"type": "latex", "content": r"E_k = \frac{1}{2}mv^2"},
        {"type": "latex", "content": rf"{_num(ek_j)} = \frac{{1}}{{2}} \times m \times {v}^2"},
        {"type": "latex", "content": rf"m = \frac{{{_num(ek_j)}}}{{\frac{{1}}{{2}} \times {v}^2}}"},
        {"type": "latex", "content": rf"m = {_num(correct)}\ \mathrm{{kg}}"},
    ]
    question = f"A {obj} moving at {v} m/s has {_num(e_given)} {e_unit} of kinetic energy. Calculate the mass of the {obj} in kg."
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(ek_j * v ** 2 / 2), "mistake": "You rearranged the equation incorrectly. m = 2Ek ÷ v².", "working": working},
        {"value": round_sf(ek_j / v ** 2), "mistake": "You forgot to multiply by 2. m = 2Ek ÷ v².", "working": working},
        {"value": round_sf(2 * e_given / v ** 2) if e_div != 1 else round_sf(2 * ek_j / v),
         "mistake": (f"You did not convert {e_unit} into J before substituting." if e_div != 1
                     else "You forgot to square the speed. m = 2Ek ÷ v²."), "working": working},
    ]
    scaffold = ([{"question": "What is the kinetic energy in J?", "answer": ek_j, "unit": "J"}] if e_div != 1 else []) + [
        {"question": "What is v²?", "answer": v ** 2},
        {"question": "What is the mass m?", "answer": correct, "unit": "kg"},
    ]
    return make_question(question, correct, options_data, "kg", notes=NOTES["energy_ke"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


def gen_ke_velocity(level="N5"):
    obj, m, m_txt, unit, val, v = _ke_ctx()
    ek = 0.5 * m * v ** 2
    e_unit, e_div = _energy_unit_for(ek)
    e_given = round_sf(ek / e_div, 3)
    ek_j = e_given * e_div
    v2 = 2 * ek_j / m
    correct = round_sf(math.sqrt(v2))

    conv = _to_kg_step(unit, val, m)
    working = ([{"type": "latex", "content": conv}] if conv else []) + (
        [{"type": "latex", "content": rf"E_k = {_num(e_given)}\ \mathrm{{{e_unit}}} = {_num(ek_j)}\ \mathrm{{J}}"}]
        if e_div != 1 else []) + [
        {"type": "latex", "content": r"E_k = \frac{1}{2}mv^2"},
        {"type": "latex", "content": rf"{_num(ek_j)} = \frac{{1}}{{2}} \times {_num(m)} \times v^2"},
        {"type": "latex", "content": rf"v^2 = {_num(v2, 4)}"},
        {"type": "latex", "content": rf"v = {_num(correct)}\ \mathrm{{m/s}}"},
    ]
    question = (f"A {obj} of mass {m_txt} has {_num(e_given)} {e_unit} of kinetic energy. Calculate its speed."
                + ("\n\n(1 tonne = 1000 kg)" if unit == "tonnes" else ""))
    if unit != "kg":
        unit_err = round_sf(math.sqrt(2 * ek_j / val))
        unit_msg = _unit_mistake(unit)
    elif e_div != 1:
        unit_err = round_sf(math.sqrt(2 * e_given / m))
        unit_msg = f"You did not convert {e_unit} into J before substituting."
    else:
        unit_err = round_sf(2 * ek_j / m)
        unit_msg = "You found v² — remember to take the square root."
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(math.sqrt(ek_j / m)), "mistake": "You forgot the ½ — multiply Ek by 2 before dividing by m.", "working": working},
        {"value": round_sf(ek_j / (0.5 * m)) if unit_err != round_sf(2 * ek_j / m) else round_sf(math.sqrt(2 * ek_j)),
         "mistake": ("You found v² — remember to take the square root." if unit_err != round_sf(2 * ek_j / m)
                     else "You forgot to divide by the mass."), "working": working},
        {"value": unit_err, "mistake": unit_msg, "working": working},
    ]
    scaffold = ([{"question": "What is the mass in kg?", "answer": m, "unit": "kg"}] if conv else []) + (
        [{"question": "What is the kinetic energy in J?", "answer": ek_j, "unit": "J"}] if e_div != 1 else []) + [
        {"question": "What is v²?", "answer": round_sf(v2)},
        {"question": "What is the speed v?", "answer": correct, "unit": "m/s"},
    ]
    return make_question(question, correct, options_data, "m/s", notes=NOTES["energy_ke"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


# =========================================================
# Work Done — Ew = Fd   (a time is usually given as a distractor)
# Each context ties the object to sensible force/distance/time ranges and has
# its own wording for each of the three question forms.
# =========================================================

_WORK_CTX = [
    dict(F=(20, 60, 5), d=(10, 40, 1), t=(10, 40), fu="N", du="m",
         fwd="A pupil pushes a trolley with a force of {F} for {d}{t}. Calculate the work done by the pupil.",
         find_F="A pupil does {E} of work pushing a trolley {d}{t}. Calculate the force the pupil exerts on the trolley.",
         find_d="A pupil pushes a trolley with a force of {F}, doing {E} of work{t}. Calculate the distance the trolley moves."),
    dict(F=(500, 1000, 50), d=(100, 500, 10), t=(120, 420), fu="N", du="m",
         fwd="A horse pulls a cart with a force of {F} for {d}{t}. Calculate the work done by the horse.",
         find_F="A horse does {E} of work pulling a cart {d}{t}. Calculate the force the horse exerts.",
         find_d="A horse pulls a cart with a force of {F}, doing {E} of work{t}. Calculate the distance the cart is pulled."),
    dict(F=(1000, 2500, 100), d=(100, 400, 10), t=(30, 120), fu="N", du="m",
         fwd="A tractor pulls a trailer of hay along a croft track with a force of {F} for {d}{t}. Calculate the work done by the tractor.",
         find_F="A tractor does {E} of work pulling a trailer of hay {d} along a croft track{t}. Calculate the force exerted by the tractor.",
         find_d="A tractor pulls a trailer of hay with a force of {F}, doing {E} of work{t}. Calculate the distance travelled."),
    dict(F=(200, 800, 50), d=(5, 25, 1), t=(10, 60), fu="N", du="m",
         fwd="A winch pulls a boat {d} up a slipway with a force of {F}{t}. Calculate the work done by the winch.",
         find_F="A winch does {E} of work pulling a boat {d} up a slipway{t}. Calculate the force exerted by the winch.",
         find_d="A winch pulls a boat up a slipway with a force of {F}, doing {E} of work{t}. Calculate the distance the boat is pulled."),
    dict(F=(30, 80, 5), d=(20, 100, 5), t=(30, 150), fu="N", du="m",
         fwd="A child pulls a sledge with a force of {F} for {d}{t}. Calculate the work done by the child.",
         find_F="A child does {E} of work pulling a sledge {d}{t}. Calculate the force the child exerts.",
         find_d="A child pulls a sledge with a force of {F}, doing {E} of work{t}. Calculate the distance the sledge is pulled."),
    dict(F=(100, 200, 10), d=(1.0, 3.0, 0.1), t=(120, 480), fu="kN", du="km",
         fwd="The engines of a CalMac ferry provide a forward force of {F}. The ferry travels {d}{t}. Calculate the work done by the engines.",
         find_F="The engines of a CalMac ferry do {E} of work as the ferry travels {d}{t}. Calculate the forward force provided by the engines in N.",
         find_d="The engines of a CalMac ferry provide a forward force of {F} and do {E} of work{t}. Calculate the distance the ferry travels in m."),
    dict(F=(3, 8, 0.5), d=(0.5, 2.0, 0.1), t=(30, 120), fu="kN", du="km",
         fwd="A lorry's engine provides a driving force of {F} over a distance of {d}{t}. Calculate the work done by the engine.",
         find_F="A lorry's engine does {E} of work driving the lorry {d}{t}. Calculate the driving force in N.",
         find_d="A lorry's engine provides a driving force of {F} and does {E} of work{t}. Calculate the distance travelled in m."),
]


def _pick(lo, hi, step):
    return round(lo + random.randint(0, int(round((hi - lo) / step))) * step, 3)


def _work_ctx():
    c = random.choice(_WORK_CTX)
    F_val, d_val = _pick(*c["F"]), _pick(*c["d"])
    F = F_val * (1000 if c["fu"] == "kN" else 1)
    d = d_val * (1000 if c["du"] == "km" else 1)
    t_s = random.choice([x for x in range(c["t"][0], c["t"][1] + 1) if x % 5 == 0])
    if t_s >= 120 and t_s % 60 == 0:
        t_txt = f"{t_s // 60} minutes"
    else:
        t_txt = f"{t_s} s"
    if random.random() >= 0.8:          # most, but not all, questions include a time distractor
        t_s, t_txt = None, None
    return dict(c=c, F=F, d=d, F_val=F_val, d_val=d_val,
                F_txt=f"{_num(F_val)} {c['fu']}", d_txt=f"{_num(d_val)} {c['du']}",
                t_s=t_s, t_txt=t_txt, t_clause=f" in {t_txt}" if t_txt else "")


def _work_notes(w, need_F=True, need_d=True):
    lines = []
    if w["t_txt"]:
        lines.append({"type": "text", "content": f"The time ({w['t_txt']}) is not needed — $E_W = Fd$ does not involve time."})
    if need_F and w["c"]["fu"] == "kN":
        lines.append({"type": "latex", "content": rf"F = {_num(w['F_val'])}\ \mathrm{{kN}} = {_num(w['F'])}\ \mathrm{{N}}"})
    if need_d and w["c"]["du"] == "km":
        lines.append({"type": "latex", "content": rf"d = {_num(w['d_val'])}\ \mathrm{{km}} = {_num(w['d'])}\ \mathrm{{m}}"})
    return lines


def _work_scaffold(w, final_q, final_ans, final_unit, need_F=True, need_d=True):
    """Unit-conversion checkpoints only. A plain single-step Ew = Fd with nothing
    to convert gets no scaffold."""
    steps = []
    if need_F and w["c"]["fu"] == "kN":
        steps.append({"question": "What is the force in N?", "answer": w["F"], "unit": "N"})
    if need_d and w["c"]["du"] == "km":
        steps.append({"question": "What is the distance in m?", "answer": w["d"], "unit": "m"})
    return steps + [{"question": final_q, "answer": final_ans, "unit": final_unit}] if steps else None


def _converted(w, need_F=True, need_d=True):
    return (need_F and w["c"]["fu"] == "kN") or (need_d and w["c"]["du"] == "km")


def gen_workdone(level="N5"):
    w = _work_ctx()
    correct = round_sf(w["F"] * w["d"])
    working = _work_notes(w) + [
        {"type": "latex", "content": r"E_W = Fd"},
        {"type": "latex", "content": rf"E_W = {_num(w['F'])} \times {_num(w['d'])}"},
        {"type": "latex", "content": rf"E_W = {_num(correct)}\ \mathrm{{J}}"},
    ]
    question = w["c"]["fwd"].format(F=w["F_txt"], d=w["d_txt"], t=w["t_clause"])
    t_s = w["t_s"]
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(w["F"] / w["d"]), "mistake": "You divided instead of multiplying. Ew = F × d.", "working": working},
        {"value": round_sf(w["F_val"] * w["d_val"]) if _converted(w) else round_sf(w["F"] + w["d"]),
         "mistake": ("You did not convert kN to N and/or km to m before substituting." if _converted(w)
                     else "You added instead of multiplying. Ew = F × d."), "working": working},
        {"value": round_sf(w["F"] * w["d"] / t_s) if t_s else round_sf(w["d"] / w["F"]),
         "mistake": ("You divided by the time. Ew = Fd — time is not needed (that would be power)." if t_s
                     else "You divided the wrong way around."), "working": working},
    ]
    return make_question(question, correct, options_data, "J", notes=NOTES["energy_work"],
                         topic="Dynamics", question_type="Energy", level=level,
                         scaffold=_work_scaffold(w, "What is the work done Ew?", correct, "J"))


def gen_work_force(level="N5"):
    w = _work_ctx()
    ew = round_sf(w["F"] * w["d"], 4)
    correct = round_sf(ew / w["d"])
    working = _work_notes(w, need_F=False) + [
        {"type": "latex", "content": r"E_W = Fd"},
        {"type": "latex", "content": rf"{_num(ew, 4)} = F \times {_num(w['d'])}"},
        {"type": "latex", "content": rf"F = \frac{{{_num(ew, 4)}}}{{{_num(w['d'])}}}"},
        {"type": "latex", "content": rf"F = {_num(correct)}\ \mathrm{{N}}"},
    ]
    question = w["c"]["find_F"].format(E=f"{_big(ew, 4)} J", d=w["d_txt"], t=w["t_clause"])
    t_s = w["t_s"]
    km = w["c"]["du"] == "km"
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(ew * w["d"]), "mistake": "You multiplied instead of dividing. F = Ew ÷ d.", "working": working},
        {"value": round_sf(ew / w["d_val"]) if km else round_sf(w["d"] / ew),
         "mistake": ("You did not convert km to m before substituting." if km
                     else "You divided the wrong way around. F = Ew ÷ d."), "working": working},
        {"value": round_sf(ew / t_s) if t_s else round_sf(ew - w["d"]),
         "mistake": ("You divided by the time. Ew = Fd — time is not needed." if t_s
                     else "You subtracted instead of dividing. F = Ew ÷ d."), "working": working},
    ]
    return make_question(question, correct, options_data, "N", notes=NOTES["energy_work"],
                         topic="Dynamics", question_type="Energy", level=level,
                         scaffold=_work_scaffold(w, "What is the force F?", correct, "N", need_F=False))


def gen_work_distance(level="N5"):
    w = _work_ctx()
    ew = round_sf(w["F"] * w["d"], 4)
    correct = round_sf(ew / w["F"])
    working = _work_notes(w, need_d=False) + [
        {"type": "latex", "content": r"E_W = Fd"},
        {"type": "latex", "content": rf"{_num(ew, 4)} = {_num(w['F'])} \times d"},
        {"type": "latex", "content": rf"d = \frac{{{_num(ew, 4)}}}{{{_num(w['F'])}}}"},
        {"type": "latex", "content": rf"d = {_num(correct)}\ \mathrm{{m}}"},
    ]
    question = w["c"]["find_d"].format(E=f"{_big(ew, 4)} J", F=w["F_txt"], t=w["t_clause"])
    t_s = w["t_s"]
    kn = w["c"]["fu"] == "kN"
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(ew * w["F"]), "mistake": "You multiplied instead of dividing. d = Ew ÷ F.", "working": working},
        {"value": round_sf(ew / w["F_val"]) if kn else round_sf(w["F"] / ew),
         "mistake": ("You did not convert kN to N before substituting." if kn
                     else "You divided the wrong way around. d = Ew ÷ F."), "working": working},
        {"value": round_sf(ew / t_s) if t_s else round_sf(ew - w["F"]),
         "mistake": ("You divided by the time. Ew = Fd — time is not needed." if t_s
                     else "You subtracted instead of dividing. d = Ew ÷ F."), "working": working},
    ]
    return make_question(question, correct, options_data, "m", notes=NOTES["energy_work"],
                         topic="Dynamics", question_type="Energy", level=level,
                         scaffold=_work_scaffold(w, "What is the distance d?", correct, "m", need_d=False))


# =========================================================
# Conservation of Energy — Ep ⇄ Ek, energy lost to friction
# =========================================================

_SLIDE_OBJECTS = ["sledge", "skateboarder", "go-kart", "toboggan", "trolley"]
_BRAKE_OBJECTS = ["car", "van", "cyclist", "motorbike"]

# Ep → Ek. (sentence, mass unit, m_lo, m_hi, m_step, h_lo, h_hi, h_step, ending)
# The mass is always given — solutions calculate the initial Ep first and then
# use that value as Ek, rather than cancelling m algebraically.
_FALL_CTX = [
    ("A ball of mass {m} is dropped from a height of {h}.", "kg", 0.2, 0.6, 0.05, 2, 12, 0.5,
     "Calculate the speed of the ball just before it hits the ground."),
    ("A rock of mass {m} breaks off a sea cliff at Mangersta and falls {h} into the sea.", "kg", 1.0, 5.0, 0.5, 10, 40, 1,
     "Calculate the speed of the rock just before it hits the water."),
    ("A gannet of mass {m} folds its wings and dives from rest, {h} above the sea off St Kilda.", "kg", 2.5, 3.5, 0.1, 15, 40, 1,
     "Calculate the speed of the gannet as it enters the water."),
    ("A child on a swing has a total mass of {m}. The swing is released from rest {h} above its lowest point.",
     "kg", 20, 45, 1, 0.3, 1.2, 0.05, "Calculate the speed of the swing at its lowest point."),
    ("A sledge and rider of total mass {m} start from rest at the top of a snowy slope with a vertical height of {h}.",
     "kg", 30, 90, 5, 3, 15, 0.5, "Calculate the speed of the sledge at the bottom of the slope."),
    ("A roller-coaster car of mass {m} is released from rest at the top of a drop with a vertical height of {h}.",
     "kg", 300, 800, 50, 10, 40, 1, "Calculate the speed of the car at the bottom of the drop."),
    ("An apple of mass {m} falls from a branch {h} above the ground.", "g", 100, 300, 10, 1.5, 6, 0.5,
     "Calculate the speed of the apple just before it hits the ground."),
]

# Ek → Ep. (object, mass unit, m_lo, m_hi, m_step, v_lo, v_hi, launch phrase, height phrase)
_UP_CTX = [
    ("ball", "kg", 0.15, 0.6, 0.05, 5, 16, "is thrown vertically upwards at {v}", "maximum height reached by the ball"),
    ("tennis ball", "g", 56, 58, 1, 10, 25, "is hit vertically upwards at {v}", "maximum height reached by the tennis ball"),
    ("cricket ball", "g", 155, 165, 5, 6, 15, "is thrown vertically upwards at {v}", "maximum height reached by the cricket ball"),
    ("skateboarder", "kg", 40, 75, 1, 3, 8, "rolls towards a ramp at {v} and rolls up it until they stop",
     "maximum vertical height the skateboarder reaches"),
    ("cyclist and bike", "kg", 70, 100, 5, 4, 10, "freewheel at {v} towards the bottom of a hill and coast up it until they stop",
     "maximum vertical height the cyclist reaches"),
]


def _cons_mass(unit, lo, hi, step):
    m_val = _pick(lo, hi, step)
    m = m_val / 1000 if unit == "g" else m_val
    return m, m_val, f"{_num(m_val)} {unit}"


def gen_cons_falling_speed(level="N5"):
    sent, unit, mlo, mhi, mstep, hlo, hhi, hstep, ending = random.choice(_FALL_CTX)
    m, m_val, m_txt = _cons_mass(unit, mlo, mhi, mstep)
    h = _pick(hlo, hhi, hstep)
    ep = round_sf(m * G * h, 4)
    v2 = 2 * ep / m
    correct = round_sf(math.sqrt(v2))

    conv = [{"type": "latex", "content": _to_kg_step("g", m_val, m)}] if unit == "g" else []
    working = conv + [
        {"type": "text",  "content": "Step 1 — calculate the initial energy (all Ep at the top):"},
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"E_p = {_num(m)} \times {G} \times {_num(h)}"},
        {"type": "latex", "content": rf"E_p = {_num(ep, 4)}\ \mathrm{{J}}"},
        {"type": "text",  "content": "Step 2 — no energy is lost, so all the Ep lost becomes Ek:"},
        {"type": "latex", "content": rf"E_k = {_num(ep, 4)}\ \mathrm{{J}}"},
        {"type": "latex", "content": r"E_k = \frac{1}{2}mv^2"},
        {"type": "latex", "content": rf"{_num(ep, 4)} = \frac{{1}}{{2}} \times {_num(m)} \times v^2"},
        {"type": "latex", "content": rf"v^2 = {_num(v2, 4)}"},
        {"type": "latex", "content": rf"v = {_num(correct)}\ \mathrm{{m/s}}"},
    ]
    question = (sent.format(m=m_txt, h=f"{_num(h)} m") + " Friction and air resistance can be ignored. "
                + ending + f"\n\n{_g_table(G)}")
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(math.sqrt(ep / m)), "mistake": "You forgot the ½ in Ek = ½mv². v² = Ek ÷ (½ × m).", "working": working},
        {"value": round_sf(v2), "mistake": "You found v² — remember to take the square root.", "working": working},
        {"value": round_sf(math.sqrt(2 * ep)), "mistake": "You forgot to divide by the mass. v² = Ek ÷ (½ × m).", "working": working},
    ]
    scaffold = ([{"question": "What is the mass in kg?", "answer": m, "unit": "kg"}] if unit == "g" else []) + [
        {"question": "What is the initial gravitational potential energy, Ep?", "answer": ep, "unit": "J"},
        {"question": "What is the kinetic energy at the bottom, Ek?", "answer": ep, "unit": "J"},
        {"question": "What is v²?", "answer": round_sf(v2)},
        {"question": "What is the speed v?", "answer": correct, "unit": "m/s"},
    ]
    return make_question(question, correct, options_data, "m/s", notes=NOTES["energy_conservation"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


def gen_cons_max_height(level="N5"):
    obj, unit, mlo, mhi, mstep, vlo, vhi, launch, target = random.choice(_UP_CTX)
    m, m_val, m_txt = _cons_mass(unit, mlo, mhi, mstep)
    v = random.randint(vlo, vhi)
    ek = round_sf(0.5 * m * v ** 2, 4)
    correct = round_sf(ek / (m * G))

    conv = [{"type": "latex", "content": _to_kg_step("g", m_val, m)}] if unit == "g" else []
    working = conv + [
        {"type": "text",  "content": "Step 1 — calculate the initial energy (all Ek at the start):"},
        {"type": "latex", "content": r"E_k = \frac{1}{2}mv^2"},
        {"type": "latex", "content": rf"E_k = \frac{{1}}{{2}} \times {_num(m)} \times {v}^2"},
        {"type": "latex", "content": rf"E_k = {_num(ek, 4)}\ \mathrm{{J}}"},
        {"type": "text",  "content": "Step 2 — at the maximum height all the Ek has become Ep:"},
        {"type": "latex", "content": rf"E_p = {_num(ek, 4)}\ \mathrm{{J}}"},
        {"type": "latex", "content": r"E_p = mgh"},
        {"type": "latex", "content": rf"{_num(ek, 4)} = {_num(m)} \times {G} \times h"},
        {"type": "latex", "content": rf"h = {_num(correct)}\ \mathrm{{m}}"},
    ]
    subject = f"A {obj}" if obj != "cyclist and bike" else "A cyclist and bike"
    question = (f"{subject} of {'total ' if obj == 'cyclist and bike' else ''}mass {m_txt} "
                f"{launch.format(v=f'{v} m/s')}. Friction and air resistance can be ignored. "
                f"Calculate the {target}.\n\n{_g_table(G)}")
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round_sf(m * v ** 2 / (m * G)), "mistake": "You forgot the ½ in Ek = ½mv².", "working": working},
        {"value": round_sf(0.5 * m * v / (m * G)), "mistake": "You forgot to square the speed in Ek = ½mv².", "working": working},
        {"value": round_sf(ek / G), "mistake": "You forgot to divide by the mass. h = Ep ÷ (m × g).", "working": working},
    ]
    scaffold = ([{"question": "What is the mass in kg?", "answer": m, "unit": "kg"}] if unit == "g" else []) + [
        {"question": "What is the initial kinetic energy, Ek?", "answer": ek, "unit": "J"},
        {"question": "What is the gravitational potential energy at maximum height, Ep?", "answer": ek, "unit": "J"},
        {"question": "What is the maximum height h?", "answer": correct, "unit": "m"},
    ]
    return make_question(question, correct, options_data, "m", notes=NOTES["energy_conservation"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


def gen_cons_energy_lost(level="N5"):
    obj     = random.choice(_SLIDE_OBJECTS)
    mass_kg = random.choice(range(20, 85, 5))
    gravity = G
    height  = random.randint(3, 20)
    v_ideal = math.sqrt(2 * gravity * height)
    v       = round(random.uniform(0.5, 0.85) * v_ideal, 1)
    ep      = round_sf(mass_kg * gravity * height)
    ek      = round_sf(0.5 * mass_kg * v ** 2)
    lost    = round_sf(ep - ek)
    find_force = random.choice([True, False])
    distance   = round(height * random.uniform(2, 5))

    working = [
        {"type": "text",  "content": "Gravitational potential energy lost:"},
        {"type": "latex", "content": rf"E_p = mgh = {mass_kg} \times {gravity} \times {height} = {fmt_J(ep)}"},
        {"type": "text",  "content": "Kinetic energy at the bottom:"},
        {"type": "latex", "content": rf"E_k = \frac{{1}}{{2}}mv^2 = \frac{{1}}{{2}} \times {mass_kg} \times {v}^2 = {fmt_J(ek)}"},
        {"type": "text",  "content": "The difference is the energy lost (as heat) due to friction:"},
        {"type": "latex", "content": rf"E_{{lost}} = {ep:g} - {ek:g} = {fmt_J(lost)}"},
    ]
    question = (f"A {obj} of total mass {mass_kg} kg starts from rest at the top of a slope {height} m high. "
                f"The {obj} travels {distance} m down the slope and reaches a speed of {v} m/s at the bottom.\n\n")

    if find_force:
        correct = round_sf(lost / distance)
        working += [
            {"type": "text",  "content": "This energy equals the work done against friction:"},
            {"type": "latex", "content": r"E_W = Fd"},
            {"type": "latex", "content": rf"{lost:g} = F \times {distance}"},
            {"type": "latex", "content": rf"F = {correct}\ \mathrm{{N}}"},
        ]
        question += f"Calculate the average frictional force acting on the {obj}.\n\n{_g_table(gravity)}"
        options_data = [
            {"value": correct,                    "mistake": None, "working": working},
            {"value": round_sf(ep / distance),    "mistake": "You used all of the Ep. Only the energy lost (Ep − Ek) is work done against friction.", "working": working},
            {"value": round_sf(ek / distance),    "mistake": "You used the Ek at the bottom. The work done against friction is the energy lost (Ep − Ek).", "working": working},
            {"value": round_sf((ep + ek) / distance), "mistake": "You added Ep and Ek. The energy lost is Ep − Ek.", "working": working},
        ]
        scaffold = [
            {"question": "What is the gravitational potential energy lost, Ep?", "answer": ep},
            {"question": "What is the kinetic energy at the bottom, Ek?", "answer": ek},
            {"question": "How much energy is lost due to friction?", "answer": lost},
            {"question": "What is the average frictional force F?", "answer": correct},
        ]
        return make_question(question, correct, options_data, "N", notes=NOTES["energy_conservation"],
                             topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)

    correct = lost
    question += f"Calculate the energy lost due to friction.\n\n{_g_table(gravity)}"
    options_data = [
        {"value": correct,          "display": fmt_J(correct),        "mistake": None, "working": working},
        {"value": round_sf(ep + ek),"display": fmt_J(round_sf(ep + ek)), "mistake": "You added Ep and Ek. The energy lost is Ep − Ek.", "working": working},
        {"value": ek,               "display": fmt_J(ek),             "mistake": "That is the kinetic energy at the bottom. The energy lost is Ep − Ek.", "working": working},
        {"value": round_sf(ep - mass_kg * v ** 2), "display": fmt_J(round_sf(ep - mass_kg * v ** 2)),
         "mistake": "You forgot the ½ in Ek = ½mv².", "working": working},
    ]
    scaffold = [
        {"question": "What is the gravitational potential energy lost, Ep?", "answer": ep},
        {"question": "What is the kinetic energy at the bottom, Ek?", "answer": ek},
        {"question": "How much energy is lost due to friction?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "J", notes=NOTES["energy_conservation"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


def gen_cons_braking(level="N5"):
    obj = random.choice(_BRAKE_OBJECTS)
    if obj == "cyclist":
        mass_kg, v = random.choice(range(60, 105, 5)), random.randint(4, 12)
    elif obj == "motorbike":
        mass_kg, v = random.choice(range(200, 401, 20)), random.randint(10, 25)
    else:
        mass_kg, v = random.choice(range(800, 2001, 100)), random.randint(10, 30)
    distance = random.randint(10, 60) if obj != "cyclist" else random.randint(4, 15)
    ek       = round_sf(0.5 * mass_kg * v ** 2)
    correct  = round_sf(ek / distance)

    working = [
        {"type": "text",  "content": "Kinetic energy before braking:"},
        {"type": "latex", "content": r"E_k = \frac{1}{2}mv^2"},
        {"type": "latex", "content": rf"E_k = \frac{{1}}{{2}} \times {mass_kg} \times {v}^2 = {fmt_J(ek)}"},
        {"type": "text",  "content": "All of this Ek is transferred by the work done by the brakes (as heat):"},
        {"type": "latex", "content": r"E_W = Fd"},
        {"type": "latex", "content": rf"{ek:g} = F \times {distance}"},
        {"type": "latex", "content": rf"F = {correct}\ \mathrm{{N}}"},
    ]
    question = (f"A {obj} of mass {mass_kg} kg is travelling at {v} m/s. The brakes are applied and "
                f"it comes to rest in a distance of {distance} m.\n\n"
                f"Calculate the average braking force.")
    options_data = [
        {"value": correct,                                "mistake": None, "working": working},
        {"value": round_sf(mass_kg * v ** 2 / distance),  "mistake": "You forgot the ½ in Ek = ½mv².", "working": working},
        {"value": round_sf(0.5 * mass_kg * v / distance), "mistake": "You forgot to square the speed in Ek = ½mv².", "working": working},
        {"value": round_sf(ek * distance),                "mistake": "You multiplied by the distance. F = E_W ÷ d.", "working": working},
    ]
    scaffold = [
        {"question": "What is the kinetic energy before braking, Ek?", "answer": ek},
        {"question": "What is the work done by the brakes?", "answer": ek},
        {"question": "What is the average braking force F?", "answer": correct},
    ]
    return make_question(question, correct, options_data, "N", notes=NOTES["energy_conservation"],
                         topic="Dynamics", question_type="Energy", level=level, scaffold=scaffold)


# =========================================================
# Explain — effect of friction, mass, speed, height
# =========================================================

_HEAT_LOST = ("Some energy is converted into heat (and sound) due to friction / air resistance, "
              "so not all of the energy is transferred as calculated.")

# (question, correct, distractors, explanation)
_EXPLAIN_CASES = [
    (
        "A {slider} slides down a slope. The speed at the bottom is calculated assuming all the "
        "gravitational potential energy becomes kinetic energy. The actual speed measured is less "
        "than the calculated value. Why?",
        "Some energy is converted into heat due to friction.",
        ["The mass of the {slider} decreases as it moves.",
         "Gravitational field strength decreases as the {slider} moves down the slope.",
         "Kinetic energy is converted into gravitational potential energy on the way down."],
        _HEAT_LOST,
    ),
    (
        "A ball is thrown vertically upwards. The maximum height is calculated assuming all the "
        "kinetic energy becomes gravitational potential energy. The actual height reached is less "
        "than calculated. Why?",
        "Some energy is converted into heat due to air resistance.",
        ["The ball gains mass as it rises.",
         "The ball's kinetic energy is zero when it is thrown.",
         "Gravitational potential energy is converted into kinetic energy as the ball rises."],
        _HEAT_LOST,
    ),
    (
        "A {slider} slides down a slope from rest. If the slope were made rougher, so that the "
        "force of friction increased, what would happen to the speed of the {slider} at the bottom?",
        "Decrease",
        ["Increase", "Stay the same"],
        "More work is done against friction, so more energy is converted into heat. Less of the "
        "gravitational potential energy becomes kinetic energy, so the speed at the bottom is lower.",
    ),
    (
        "A {slider} slides down a slope from rest. How does the gravitational potential energy lost "
        "compare with the kinetic energy gained, when friction acts?",
        "The Ep lost is greater than the Ek gained.",
        ["The Ep lost is equal to the Ek gained.", "The Ep lost is less than the Ek gained."],
        "Some of the Ep lost is converted into heat by friction, so only part of it becomes Ek. "
        "The Ep lost is therefore greater than the Ek gained.",
    ),
    (
        "Two objects are dropped from the same height. One has twice the mass of the other. "
        "Ignoring air resistance, how does the speed of the heavier object just before it hits the "
        "ground compare with the lighter one?",
        "It is the same",
        ["It is double", "It is half"],
        "mgh = ½mv², so the mass cancels: v = √(2gh). The speed only depends on the height fallen "
        "(and g), not on the mass.",
    ),
    (
        "The speed of a {mover} is doubled. What happens to its kinetic energy?",
        "It is four times bigger",
        ["It doubles", "It stays the same", "It halves"],
        "Ek = ½mv². The speed is squared, so doubling v multiplies Ek by 2² = 4.",
    ),
    (
        "An object is lifted to twice the height. What happens to its gain in gravitational "
        "potential energy?",
        "It doubles",
        ["It is four times bigger", "It stays the same", "It halves"],
        "Ep = mgh. Ep is directly proportional to h, so doubling the height doubles Ep.",
    ),
    (
        "A {mover} brakes and comes to a stop. What happens to its kinetic energy?",
        "It is converted into heat in the brakes by friction.",
        ["It is converted into gravitational potential energy.",
         "It is destroyed.",
         "It is converted into chemical energy in the fuel."],
        "The braking force does work against the motion. Energy cannot be destroyed — the kinetic "
        "energy is converted into heat (and sound) by friction in the brakes.",
    ),
    (
        "A roller coaster car is released from rest at the top of the first hill. Why must the "
        "second hill be lower than the first?",
        "Some energy is converted into heat by friction, so the car cannot regain its original height.",
        ["The car gains mass as it travels.",
         "The car has more kinetic energy at the top of the second hill.",
         "Gravitational field strength is weaker at the second hill."],
        "Friction and air resistance convert some energy into heat. The car has less total energy "
        "at the second hill, so it cannot reach the same height (the Ep available is less).",
    ),
    (
        "A ball is dropped onto the ground and bounces. Why does it not bounce back up to the height it "
        "was dropped from?",
        "Some energy is converted into heat and sound when it hits the ground, so there is less energy to become Ep.",
        ["The ball's mass decreases when it bounces.",
         "Gravitational field strength is stronger on the way up.",
         "All of the kinetic energy is converted back into Ep, but gravity pulls it down early."],
        "Energy is converted into heat and sound in the collision with the ground (and by air resistance). "
        "The ball has less energy after the bounce, so less can be converted back into Ep — it cannot "
        "reach its original height.",
    ),
    (
        "A {mover} doubles its speed. The same braking force is used to stop it. What happens to the "
        "braking distance?",
        "It is four times longer",
        ["It doubles", "It stays the same", "It halves"],
        "Ek = ½mv², so doubling v makes Ek four times bigger. The brakes must do four times as much work "
        "(Ew = Fd). F is the same, so d must be four times bigger.",
    ),
    (
        "A cyclist freewheels down a hill. Which change would reduce the energy lost on the way down?",
        "Crouching into a streamlined position to reduce air resistance.",
        ["Sitting upright to catch more air.",
         "Letting some air out of the tyres.",
         "Carrying a heavier rucksack."],
        "Less air resistance (streamlining) and less friction (oiled chain, pumped-up tyres) mean less energy "
        "is converted into heat, so more of the Ep becomes Ek.",
    ),
    (
        "A ball is thrown vertically upwards. What is its kinetic energy at the maximum height?",
        "Zero",
        ["At its greatest value", "Equal to its kinetic energy at launch"],
        "At the maximum height the ball is momentarily stationary (v = 0), so Ek = ½mv² = 0. "
        "All of its kinetic energy has become gravitational potential energy.",
    ),
]


def gen_energy_explain(level="N5"):
    question_text, correct, distractor_texts, reason = random.choice(_EXPLAIN_CASES)
    fill = {"slider": random.choice(_SLIDE_OBJECTS), "mover": random.choice(_BRAKE_OBJECTS)}
    question_text = question_text.format(**fill)
    correct = correct.format(**fill)
    distractor_texts = [d.format(**fill) for d in distractor_texts]

    working = [{"type": "text", "content": reason}]
    distractors = [{"value": d, "mistake": reason, "working": working} for d in distractor_texts]
    options = [correct] + distractor_texts
    random.shuffle(options)

    return PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        distractors=distractors,
        working=working,
        notes=NOTES["energy_conservation"],
        topic="Dynamics",
        question_type="Energy",
        level=level,
        metadata={"type": "classification", "options": options},
    )


_GPE_GENS    = [_distinct_options(g) for g in (gen_gpe, gen_gpe_mass, gen_gpe_height)]
_KE_GENS     = [_distinct_options(g) for g in (gen_ke, gen_ke_mass, gen_ke_velocity)]
_WORK_GENS   = [_distinct_options(g) for g in (gen_workdone, gen_work_force, gen_work_distance)]
_CONS_GENS   = [_distinct_options(g) for g in (gen_cons_falling_speed, gen_cons_max_height,
                                               gen_cons_energy_lost, gen_cons_braking)]
_ALL_GENS    = _GPE_GENS + _KE_GENS + _WORK_GENS + _CONS_GENS


def generate_energy_gpe(level="N5"):
    return random.choice(_GPE_GENS)(level=level)


def generate_energy_ke(level="N5"):
    return random.choice(_KE_GENS)(level=level)


def generate_energy_work(level="N5"):
    return random.choice(_WORK_GENS)(level=level)


def generate_energy_conservation(level="N5"):
    return random.choice(_CONS_GENS)(level=level)


def generate_energy(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
