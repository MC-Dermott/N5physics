import random
import pathlib
from utils.make_question import make_question
from utils.notes import NOTES
from topics.dynamics.forces import generate_forces

_FBD_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "free_body_diagram_widget.html"
).read_text(encoding="utf-8")


def _with_fbd_widget(question):
    question.metadata["widget_html"] = _FBD_WIDGET_HTML
    return question

G = 9.8


def gen_horizontal_unbalanced_force(level="S3"):
    """Reuses forces.py's driving-vs-friction generators (same F_unbalanced = F_driving -
    F_friction / F = ma family the worksheet's Q1/Q4 test), just relabelled so the
    recorded question_type matches this S3 topic instead of forces.py's own "Forces"."""
    q = generate_forces(level=level)
    q.question_type = "Unbalanced Forces"
    return q

# (label, mass_lo, mass_hi, applied_lo, applied_hi) — applied force is checked
# against weight below to guarantee a positive (upward) unbalanced force.
_SCENARIOS = [
    ("rocket", "the rocket's engines produce a thrust of", 500, 3000, 8000, 40000),
    ("hot air balloon", "its burner produces a lift force of", 200, 800, 3000, 10000),
    ("crane-lifted mass", "the crane's cable pulls upward with a force of", 5, 50, 100, 700),
    ("drone", "its rotors produce an upward force of", 1, 5, 20, 80),
]


def _draw_scenario():
    label, phrase, m_lo, m_hi, f_lo, f_hi = random.choice(_SCENARIOS)
    for _ in range(20):
        mass = random.randint(m_lo, m_hi)
        applied = random.randint(f_lo, f_hi)
        weight = round(mass * G, 2)
        if applied > weight * 1.15:  # comfortably positive unbalanced force
            break
    return label, phrase, mass, applied, weight


def _round3(x):
    return float(f"{x:.3g}")


def _dedup(options_data, correct):
    seen = {round(float(correct), 4)}
    cleaned = []
    for opt in options_data:
        key = round(float(opt["value"]), 4)
        if key not in seen:
            seen.add(key)
            cleaned.append(opt)
        elif opt["mistake"] is None:
            cleaned.insert(0, opt)
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


def gen_vertical_unbalanced_force(level="S3"):
    label, phrase, mass, applied, weight = _draw_scenario()
    unbalanced = _round3(applied - weight)
    accel = _round3(unbalanced / mass)

    working = [
        {"type": "text",  "content": "First find the weight, then subtract it from the applied force:"},
        {"type": "latex", "content": r"W = mg"},
        {"type": "latex", "content": rf"W = {mass} \times {G} = {weight}\ \mathrm{{N}}"},
        {"type": "latex", "content": r"F_{\text{unbalanced}} = F_{\text{applied}} - W"},
        {"type": "latex", "content": rf"F_{{unbalanced}} = {applied} - {weight}"},
        {"type": "latex", "content": rf"F_{{unbalanced}} = {unbalanced}\ \mathrm{{N}}"},
    ]
    question = (
        f"A {label} of mass {mass} kg is launching vertically — {phrase} {applied} N.\n\n"
        f"Calculate the unbalanced force acting on the {label}."
    )
    forgot_weight = float(applied)
    swapped = _round3(weight - applied)
    options_data = [
        {"value": unbalanced, "mistake": None, "working": working},
        {"value": forgot_weight,
         "mistake": "That's just the applied force — you need to subtract the weight to find the "
                    "unbalanced force.",
         "working": working},
        {"value": swapped,
         "mistake": "You calculated weight − applied force instead of applied force − weight.",
         "working": working},
    ]
    options_data = _dedup(options_data, unbalanced)
    scaffold = [
        {"question": "What is the weight of the object?", "answer": weight},
        {"question": "What is the unbalanced force?", "answer": unbalanced},
    ]
    scaffold.insert(1, _fbd_step_vertical(applied, weight, label))
    return _with_fbd_widget(make_question(question, unbalanced, options_data, "N", scaffold=scaffold,
                         notes=NOTES["unbalanced_forces_s3"], topic="Dynamics",
                         question_type="Unbalanced Forces", level=level))


def gen_vertical_acceleration(level="S3"):
    label, phrase, mass, applied, weight = _draw_scenario()
    unbalanced = round(applied - weight, 2)
    accel = _round3(unbalanced / mass)

    working = [
        {"type": "text",  "content": "Find the weight, then the unbalanced force, then the acceleration:"},
        {"type": "latex", "content": rf"W = mg = {mass} \times {G} = {weight}\ \mathrm{{N}}"},
        {"type": "latex", "content": rf"F_{{unbalanced}} = {applied} - {weight} = {unbalanced}\ \mathrm{{N}}"},
        {"type": "latex", "content": r"a = \frac{F_{\text{unbalanced}}}{m}"},
        {"type": "latex", "content": rf"a = \frac{{{unbalanced}}}{{{mass}}}"},
        {"type": "latex", "content": rf"a = {accel}\ \mathrm{{m/s^2}}"},
    ]
    question = (
        f"A {label} of mass {mass} kg is launching vertically — {phrase} {applied} N.\n\n"
        f"Calculate the {label}'s acceleration."
    )
    forgot_weight_accel = _round3(applied / mass)
    options_data = [
        {"value": accel, "mistake": None, "working": working},
        {"value": forgot_weight_accel,
         "mistake": "You divided the applied force straight by mass — first subtract the weight to "
                    "get the unbalanced force, then divide that by mass.",
         "working": working},
    ]
    options_data = _dedup(options_data, accel)
    scaffold = [
        {"question": "What is the weight of the object?", "answer": weight},
        {"question": "What is the unbalanced force?", "answer": unbalanced},
        {"question": "What is the acceleration?", "answer": accel},
    ]
    scaffold.insert(1, _fbd_step_vertical(applied, weight, label))
    return _with_fbd_widget(make_question(question, accel, options_data, "m/s²", scaffold=scaffold,
                         notes=NOTES["unbalanced_forces_s3"], topic="Dynamics",
                         question_type="Unbalanced Forces", level=level))


def generate_unbalanced_forces_s3(level="S3"):
    return random.choice([gen_vertical_unbalanced_force, gen_vertical_acceleration])(level=level)


# ───────────── Added Nov 2026 to match the rebuilt Unbalanced Forces worksheet ─────────────
from core.models.question_model import PhysicsQuestion


def _n(x):
    """Pupil-facing number: no e-notation, spaces in thousands, trailing zeros trimmed."""
    x = float(x)
    if abs(x - round(x)) < 1e-9:
        v = int(round(x))
        return f"{v:,}".replace(",", " ") if abs(v) >= 10000 else str(v)
    return f"{x:.2f}".rstrip("0").rstrip(".")


def fbd_svg(forces, obj=""):
    """Example free body diagram as an SVG string. forces: [(direction, label, relative_length 0-1), ...] with
    direction one of up / down / left / right. Arrows start on the box and are drawn to a sensible scale."""
    W, H, cx, cy, half = 300, 300, 150, 150, 28
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<rect x="{cx-half}" y="{cy-half}" width="{2*half}" height="{2*half}" fill="#dde6f3" stroke="#1f3b66" stroke-width="2"/>']
    if obj:
        parts.append(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#1f3b66">{obj}</text>')
    for d, label, rel in forces:
        ln = 28 + 55 * rel
        vx, vy = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}[d]
        x0, y0 = cx + vx * half, cy + vy * half
        x1, y1 = x0 + vx * ln, y0 + vy * ln
        parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#c0392b" stroke-width="3"/>')
        px, py = -vy, vx
        parts.append(f'<polygon points="{x1},{y1} {x1-vx*10+px*6},{y1-vy*10+py*6} {x1-vx*10-px*6},{y1-vy*10-py*6}" fill="#c0392b"/>')
        tx, ty = x1 + vx * 8 + (0 if vx else 0), y1 + vy * 8
        anchor = "middle" if vx == 0 else ("start" if vx > 0 else "end")
        ty = ty + (4 if vy == 0 else (10 if vy > 0 else -4))
        parts.append(f'<text x="{tx}" y="{ty}" text-anchor="{anchor}" font-family="sans-serif" font-size="13" fill="#333">{label}</text>')
    parts.append('</svg>')
    return "".join(parts)


def _fbd_step(forces, obj=""):
    return {"question": "Draw a free body diagram. Show every force as an arrow that starts on the object, labelled with its "
                        "size, with longer arrows for bigger forces. Check yours against this example:",
            "instruction": True, "svg": fbd_svg(forces, obj)}


def _fbd_step_vertical(applied, weight, label=""):
    big = max(applied, weight)
    return _fbd_step([("up", f"{_n(applied)} N", _rel(applied, big)), ("down", f"{_n(weight)} N", _rel(weight, big))])


def _rel(a, b):
    """Relative arrow length of a (0-1) compared with the bigger force b."""
    return 1.0 if a >= b else max(0.25, a / b)


def _numeric(question, correct, wrong, unit, working, scaffold=None, level="S3"):
    """wrong: list of (value, mistake). Single correct option plus distractors, dedup'd."""
    options = [{"value": correct, "mistake": None, "working": working}]
    options += [{"value": v, "mistake": m, "working": working} for v, m in wrong]
    options = _dedup(options, correct)
    for v, why in ((correct * 2, "Check your arithmetic — this is double the correct value."),
                   (round(correct / 2, 3), "Check your arithmetic — this is half the correct value.")):
        if len(options) < 3 and all(abs(float(o["value"]) - v) > 1e-6 for o in options) and v > 0:
            options.append({"value": v, "mistake": why, "working": working})
    return make_question(question, correct, options, unit, scaffold=scaffold,
                         notes=NOTES["unbalanced_forces_s3"], topic="Dynamics",
                         question_type="Unbalanced Forces", level=level)


def _mc(text, correct, wrong, level="S3"):
    """Multiple-choice (word answers): wrong = [(option, why it's wrong), ...]."""
    distractors = [{"value": w, "mistake": why, "working": []} for w, why in wrong]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(question_text=text, correct_answer=correct, unit="", distractors=distractors,
                           working=[], notes=NOTES["unbalanced_forces_s3"], topic="Dynamics",
                           question_type="Unbalanced Forces", level=level,
                           metadata={"type": "classification", "options": options})


# (object, masses, friction forces) — masses and forces tied to the object so they are always sensible
_HORIZ = [
    ("van", [1200, 1500, 1800, 2000], [400, 600, 800, 1000]),
    ("cyclist and bike", [80, 90, 100, 110], [40, 60, 80, 100]),
    ("quad bike", [220, 250, 280], [100, 150, 200]),
    ("team of huskies pulling a sledge", [150, 180, 200], [60, 80, 100]),
]


def gen_unknown_force(level="S3"):
    """Find friction (given driving force + unbalanced force) or the driving force (given mass, acceleration, friction)."""
    obj, masses, fricts = random.choice(_HORIZ)
    if random.random() < 0.5:
        m, f = random.choice(masses), random.choice(fricts)
        a = random.choice([0.5, 1.0, 1.5, 2.0])
        unb = m * a
        drive = unb + f
        working = [{"type": "text", "content": "Find the unbalanced force, then the driving force:"},
                   {"type": "latex", "content": rf"F = ma = {_n(m)} \times {_n(a)} = {_n(unb)}\ \mathrm{{N}}"},
                   {"type": "latex", "content": r"F_{\text{unbalanced}} = F_{\text{driving}} - F_{\text{friction}}"},
                   {"type": "latex", "content": rf"{_n(unb)} = F_{{driving}} - {_n(f)}"},
                   {"type": "latex", "content": rf"F_{{driving}} = {_n(unb)} + {_n(f)} = {_n(drive)}\ \mathrm{{N}}"}]
        q = (f"A {obj} of mass {_n(m)} kg is accelerating at {_n(a)} m/s². The friction force on it is {_n(f)} N.\n\n"
             f"Calculate the driving force.")
        wrong = [(unb, "That is the unbalanced force. The driving force is bigger — it has to beat the friction too."),
                 (m * a - f, "You subtracted the friction. Driving force = unbalanced force + friction."),
                 (drive + f, "You added the friction twice.")]
        sc = [{"question": "What is the unbalanced force?", "answer": unb},
              _fbd_step([("right", f"{_n(drive)} N", 1.0), ("left", f"{_n(f)} N", _rel(f, drive))]),
              {"question": "What is the driving force?", "answer": drive}]
        return _with_fbd_widget(_numeric(q, drive, [w for w in wrong if w[0] > 0], "N", working, sc, level))
    f = random.choice(fricts)
    unb = random.choice([u for u in (100, 200, 250, 300, 400, 500) if u < 2 * f + 300])
    drive = f + unb
    working = [{"type": "latex", "content": r"F_{\text{unbalanced}} = F_{\text{driving}} - F_{\text{friction}}"},
               {"type": "latex", "content": rf"{_n(unb)} = {_n(drive)} - F_{{friction}}"},
               {"type": "latex", "content": rf"F_{{friction}} = {_n(drive)} - {_n(unb)} = {_n(f)}\ \mathrm{{N}}"}]
    q = (f"A {obj} is driven forwards with a force of {_n(drive)} N. The unbalanced force on it is {_n(unb)} N forwards.\n\n"
         f"Calculate the size of the friction force.")
    wrong = [(drive + unb, "You added the unbalanced force. Friction = driving force − unbalanced force."),
             (unb, "That is the unbalanced force given in the question."),
             (drive, "That is the driving force given in the question.")]
    sc = [_fbd_step([("right", f"{_n(drive)} N", 1.0), ("left", "friction = ?", _rel(f, drive))]),
          {"question": "What is the friction force?", "answer": f, "unit": "N"}]
    return _with_fbd_widget(_numeric(q, f, wrong, "N", working, sc, level))


_FMA_OBJECTS = [
    ("crate", [20, 40, 50, 60]), ("trolley", [2, 4, 5]), ("quad bike", [200, 250, 400]),
    ("motorbike", [200, 250, 400]), ("shopping trolley", [10, 20, 25]), ("small boat", [100, 200, 500]),
]


def gen_fma(level="S3"):
    """F = ma in all three arrangements, with clean numbers (m × a is always a tidy force)."""
    obj, masses = random.choice(_FMA_OBJECTS)
    m = random.choice(masses)
    a = random.choice([0.5, 1.0, 1.5, 2.0, 2.5, 4.0])
    F = m * a
    kind = random.choice(["a", "F", "m"])
    if kind == "a":
        q = f"A {obj} of mass {_n(m)} kg has an unbalanced force of {_n(F)} N acting on it.\n\nCalculate its acceleration."
        ans, unit = a, "m/s²"
        working = [{"type": "latex", "content": r"F = ma"}, {"type": "latex", "content": rf"{_n(F)} = {_n(m)} \times a"},
                   {"type": "latex", "content": rf"a = \frac{{{_n(F)}}}{{{_n(m)}}} = {_n(a)}\ \mathrm{{m/s^2}}"}]
        wrong = [(F * m, "You multiplied force by mass. Rearrange F = ma to a = F ÷ m."),
                 (m / F, "You divided mass by force — the wrong way up."),
                 (F - m, "You subtracted. Use a = F ÷ m.")]
    elif kind == "F":
        q = f"A {obj} of mass {_n(m)} kg accelerates at {_n(a)} m/s².\n\nCalculate the unbalanced force on it."
        ans, unit = F, "N"
        working = [{"type": "latex", "content": r"F = ma"}, {"type": "latex", "content": rf"F = {_n(m)} \times {_n(a)} = {_n(F)}\ \mathrm{{N}}"}]
        wrong = [(m / a, "You divided mass by acceleration. F = m × a."),
                 (m + a, "You added. F = m × a."),
                 (a / m, "You divided acceleration by mass. F = m × a.")]
    else:
        q = f"An unbalanced force of {_n(F)} N gives a {obj} an acceleration of {_n(a)} m/s².\n\nCalculate the mass of the {obj}."
        ans, unit = m, "kg"
        working = [{"type": "latex", "content": r"F = ma"}, {"type": "latex", "content": rf"{_n(F)} = m \times {_n(a)}"},
                   {"type": "latex", "content": rf"m = \frac{{{_n(F)}}}{{{_n(a)}}} = {_n(m)}\ \mathrm{{kg}}"}]
        wrong = [(F * a, "You multiplied. Rearrange F = ma to m = F ÷ a."),
                 (a / F, "You divided acceleration by force — the wrong way up."),
                 (F - a, "You subtracted. m = F ÷ a.")]
    wrong = [w for w in wrong if w[0] > 0]
    return _numeric(q, ans, wrong, unit, working, None, level)


def gen_skydiver_calculation(level="S3"):
    """Falling skydiver: weight, then unbalanced force (weight − air resistance), then acceleration."""
    m = random.choice([60, 70, 80, 90])
    W = round(m * G, 1)
    R = random.choice([100, 120, 150, 200, 250])
    unb = round(W - R, 1)
    a = round(unb / m, 2)
    working = [{"type": "latex", "content": rf"W = mg = {m} \times {G} = {_n(W)}\ \mathrm{{N}}"},
               {"type": "latex", "content": rf"F_{{unbalanced}} = W - F_{{air}} = {_n(W)} - {_n(R)} = {_n(unb)}\ \mathrm{{N}}"},
               {"type": "latex", "content": r"F = ma"},
               {"type": "latex", "content": rf"a = \frac{{{_n(unb)}}}{{{m}}} = {_n(a)}\ \mathrm{{m/s^2}}"}]
    q = (f"A skydiver of mass {m} kg jumps from a plane. Just after leaving the plane the air resistance on the skydiver is {_n(R)} N.\n\n"
         f"Calculate the acceleration of the skydiver.")
    wrong = [(round(R / m, 2), "You divided the air resistance by the mass. Use the unbalanced force (weight − air resistance)."),
             (round(W / m, 2), "You forgot the air resistance — that's just g. Subtract it from the weight first."),
             (round((W + R) / m, 2), "You added the air resistance. It acts upwards, against the weight, so subtract it.")]
    sc = [{"question": "What is the weight of the skydiver?", "answer": W, "unit": "N"},
          _fbd_step([("up", f"{_n(R)} N", _rel(R, W)), ("down", f"{_n(W)} N", 1.0)]),
          {"question": "What is the unbalanced force?", "answer": unb, "unit": "N"},
          {"question": "What is the acceleration?", "answer": a, "unit": "m/s²"}]
    return _with_fbd_widget(_numeric(q, a, wrong, "m/s²", working, sc, level))


def gen_explain_motion(level="S3"):
    """Explain questions: skydivers (terminal speed, parachute), balanced forces, rockets in space."""
    kind = random.choice(["terminal", "chute", "newspeed", "car_const", "car_accel", "space", "diver_balanced"])
    if kind == "terminal":
        return _mc("A skydiver stops speeding up a few seconds after leaving the plane. Which explanation is correct?",
                   "The air resistance has increased until it equals the weight, so the forces are balanced",
                   [("The air resistance has increased until it is bigger than the weight", "Then the skydiver would slow down. At terminal speed they are EQUAL."),
                    ("The weight of the skydiver has decreased", "Weight stays the same (W = mg)."),
                    ("Gravity stops acting on the skydiver", "Gravity still acts — the air resistance has just grown to match it.")], level)
    if kind == "chute":
        return _mc("A skydiver falling at a steady speed opens the parachute. Why does the skydiver slow down?",
                   "The air resistance becomes bigger than the weight, so there is an unbalanced force upwards",
                   [("The weight becomes smaller than before", "The weight doesn't change when a parachute opens."),
                    ("The air resistance becomes equal to the weight", "Equal forces would mean a steady speed — not slowing down."),
                    ("The parachute stops gravity", "Gravity still acts; the air resistance is just bigger.")], level)
    if kind == "newspeed":
        return _mc("After the parachute opens the skydiver slows down and then falls at a new, lower, steady speed. Why?",
                   "As the skydiver slows the air resistance decreases until it equals the weight again",
                   [("As the skydiver slows the air resistance increases until it equals the weight", "Slower speed means LESS air resistance."),
                    ("The weight decreases until it equals the air resistance", "The weight stays the same."),
                    ("The parachute folds up", "The parachute stays open; the air resistance falls as the speed falls.")], level)
    if kind == "car_const":
        return _mc("A car's engine force is 2000 N and the resistive forces total 2000 N. Describe the car's motion.",
                   "It moves at a constant speed in a straight line, because the forces are balanced",
                   [("It accelerates, because the engine is on", "Equal forces are balanced — no acceleration."),
                    ("It slows down, because of the resistive forces", "The engine force cancels them exactly."),
                    ("It is stationary", "Balanced forces mean constant velocity OR at rest — it is already moving.")], level)
    if kind == "car_accel":
        return _mc("A car's engine force is 2000 N and the resistive forces total 700 N. Describe the car's motion.",
                   "It accelerates forwards, because the forces are unbalanced",
                   [("It moves at a constant speed, because the engine is on", "The forces are not equal, so they are unbalanced."),
                    ("It slows down, because the resistive forces are acting", "The engine force is bigger, so the car speeds up."),
                    ("It accelerates backwards", "The unbalanced force acts in the direction of the bigger force — forwards.")], level)
    if kind == "space":
        return _mc("A rocket is travelling at 2000 m/s far from any planet. Its engines are switched off. Describe its motion.",
                   "It continues at 2000 m/s in a straight line, because there is no unbalanced force",
                   [("It slows down and stops, because the engines are off", "With no friction or air resistance there is nothing to slow it down."),
                    ("It speeds up, because there is nothing in the way", "No force means no acceleration."),
                    ("It drops back towards the Earth", "It is far from any planet, so no force acts on it.")], level)
    return _mc("A skydiver falls at a steady speed with the parachute closed. What is the size of the air resistance?",
               "It is equal to the skydiver's weight, because the forces are balanced",
               [("It is zero", "There is air resistance — it equals the weight."),
                ("It is bigger than the weight", "Then the skydiver would be slowing down."),
                ("It is smaller than the weight", "Then the skydiver would still be speeding up.")], level)


# (object, masses, engine/driving force options, label for the resistive force) — tied so numbers suit the object
_SLOW = [
    ("lorry", [6000, 8000, 10000], [0, 1000, 2000], "resistive forces"),
    ("car", [800, 900, 1000, 1200], [0, 200, 400], "resistive forces"),
    ("cyclist and bike", [80, 90, 100], [0, 20, 40], "resistive forces"),
    ("skier gliding on flat snow", [60, 70, 80], [0], "friction"),
]


def gen_slowing_down(level="S3"):
    """Horizontal, slowing down: resistive forces bigger than the driving force. Find the deceleration."""
    obj, masses, drives, rname = random.choice(_SLOW)
    m = random.choice(masses)
    a = random.choice([0.5, 1.0, 1.5, 2.0])
    drive = random.choice(drives)
    unb = m * a
    res = unb + drive
    forces = [("left", f"{_n(res)} N", 1.0)] + ([("right", f"{_n(drive)} N", _rel(drive, res))] if drive else [])
    if drive:
        q = (f"A {obj} of mass {_n(m)} kg is slowing down. The driving force on it is {_n(drive)} N and the {rname} total {_n(res)} N.\n\n"
             f"Calculate the size of its deceleration (acceleration backwards).")
        working = [{"type": "latex", "content": rf"F_{{unbalanced}} = {_n(res)} - {_n(drive)} = {_n(unb)}\ \mathrm{{N\ backwards}}"}]
    else:
        q = (f"A {obj} of mass {_n(m)} kg is slowing down. There is no driving force and the {rname} total {_n(res)} N.\n\n"
             f"Calculate the size of its deceleration (acceleration backwards).")
        working = [{"type": "latex", "content": rf"F_{{unbalanced}} = {_n(res)}\ \mathrm{{N\ backwards}}"}]
    working += [{"type": "latex", "content": r"F = ma"}, {"type": "latex", "content": rf"{_n(unb)} = {_n(m)} \times a"},
                {"type": "latex", "content": rf"a = \frac{{{_n(unb)}}}{{{_n(m)}}} = {_n(a)}\ \mathrm{{m/s^2\ backwards}}"}]
    wrong = [(round(res / m, 3), "You used the resistive force on its own. Use the unbalanced force (resistive − driving)."),
             (round((res + drive) / m, 3), "You added the driving force. It acts against the resistive forces, so subtract it."),
             (round(drive / m, 3), "You used the driving force. The unbalanced force is the DIFFERENCE between the two forces.")]
    sc = [{"question": "What is the size of the unbalanced force?", "answer": unb, "unit": "N"},
          _fbd_step(forces),
          {"question": "What is the deceleration?", "answer": a, "unit": "m/s²"}]
    return _with_fbd_widget(_numeric(q, a, [w for w in wrong if w[0] > 0], "m/s²", working, sc, level))


def gen_unknown_vertical_force(level="S3"):
    """Vertical, starting from the acceleration: unbalanced force = ma, then the unknown upward force."""
    if random.random() < 0.5:
        m = random.choice([500, 1000, 1500, 2000])
        a = random.choice([0.5, 1.0, 1.5, 2.0])
        W = round(m * G, 1)
        L = W + m * a
        q = (f"A helicopter of mass {_n(m)} kg accelerates upwards at {_n(a)} m/s².\n\nCalculate the upward (lift) force on the helicopter.")
        working = [{"type": "latex", "content": rf"W = mg = {_n(m)} \times {G} = {_n(W)}\ \mathrm{{N}}"},
                   {"type": "latex", "content": rf"F = ma = {_n(m)} \times {_n(a)} = {_n(m * a)}\ \mathrm{{N}}"},
                   {"type": "latex", "content": rf"F_{{unbalanced}} = L - W: {_n(m * a)} = L - {_n(W)}"},
                   {"type": "latex", "content": rf"L = {_n(m * a)} + {_n(W)} = {_n(L)}\ \mathrm{{N}}"}]
        wrong = [(round(W - m * a, 1), "You subtracted. The lift must be BIGGER than the weight for an upward acceleration."),
                 (round(m * a, 1), "That is just the unbalanced force. Add the weight to get the lift force."),
                 (W, "That is only the weight — the helicopter is accelerating, so the lift is bigger.")]
        sc = [{"question": "What is the weight?", "answer": W, "unit": "N"},
              {"question": "What is the unbalanced force (ma)?", "answer": m * a, "unit": "N"},
              _fbd_step([("up", "L", 1.0), ("down", f"{_n(W)} N", 0.85)]),
              {"question": "What is the lift force?", "answer": L, "unit": "N"}]
        return _with_fbd_widget(_numeric(q, L, wrong, "N", working, sc, level))
    m = random.choice([10, 20, 40, 50])
    a = random.choice([0.5, 1.0, 2.0])
    W = round(m * G, 1)
    T = W - m * a
    q = (f"A {_n(m)} kg mass is lowered on a rope. It accelerates downwards at {_n(a)} m/s².\n\nCalculate the force the rope pulls upwards with.")
    working = [{"type": "latex", "content": rf"W = mg = {_n(m)} \times {G} = {_n(W)}\ \mathrm{{N}}"},
               {"type": "latex", "content": rf"F = ma = {_n(m)} \times {_n(a)} = {_n(m * a)}\ \mathrm{{N}}"},
               {"type": "latex", "content": rf"F_{{unbalanced}} = W - T: {_n(m * a)} = {_n(W)} - T"},
               {"type": "latex", "content": rf"T = {_n(W)} - {_n(m * a)} = {_n(T)}\ \mathrm{{N}}"}]
    wrong = [(round(W + m * a, 1), "You added. The rope force must be SMALLER than the weight for a downward acceleration."),
             (round(m * a, 1), "That is just the unbalanced force. Subtract it from the weight."),
             (W, "That is only the weight — the mass is accelerating downwards, so the rope force is smaller.")]
    sc = [{"question": "What is the weight?", "answer": W, "unit": "N"},
          {"question": "What is the unbalanced force (ma)?", "answer": m * a, "unit": "N"},
          _fbd_step([("down", f"{_n(W)} N", 1.0), ("up", "T", 0.8)]),
          {"question": "What is the rope force?", "answer": T, "unit": "N"}]
    return _with_fbd_widget(_numeric(q, T, wrong, "N", working, sc, level))
