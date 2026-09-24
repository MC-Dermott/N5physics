import random
import pathlib
from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question
from utils.notes import NOTES

_ACCELERATION_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "acceleration_widget.html"
).read_text(encoding="utf-8")


def _with_acceleration_widget(question):
    question.metadata["widget_html"] = _ACCELERATION_WIDGET_HTML
    return question


_LIGHT_GATE_NOTES = r"""
## Measuring acceleration with light gates — $a = \frac{v - u}{t}$

A card of known length is fixed to the trolley. As the card passes through a light gate,
the timer records how long the beam is blocked.

**Instantaneous speed at a light gate:**
$$v = \frac{\text{length of card}}{\text{time for card to pass through the gate}}$$

**Two light gates (X then Y):**
- Initial speed $u$ = speed at the first gate
- Final speed $v$ = speed at the second gate
- $t$ = time for the trolley to travel **between** the gates (not the time at a gate)

**One light gate, trolley released from rest:**
- $u = 0$
- $v$ = speed at the light gate
- $t$ = time from release until the card reaches the light gate (measured with a stop-clock)

**Measurements needed (two gates):** length of the card, time for the card to pass through
each light gate, and the time taken to travel between the light gates.

> **Important:** Convert the card length to metres before calculating a speed. Releasing the
> trolley from a different point on the **same** slope does **not** change its acceleration —
> only the speeds at the gates change.
"""

_CONTEXTS = ["car", "cyclist", "runner", "train", "bus", "motorbike", "sprinter", "lorry"]


def _fmt(x):
    return f"{x:g}"


def _dedup(options_data, correct):
    """Remove distractor entries whose value equals the correct answer or another distractor."""
    seen = {round(float(correct), 4)}
    cleaned = []
    for opt in options_data:
        key = round(float(opt["value"]), 4)
        if key not in seen:
            seen.add(key)
            cleaned.append(opt)
        elif opt["mistake"] is None:
            cleaned.insert(0, opt)  # always keep correct
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


def _question(question, correct, options_data, unit, notes, scaffold=None, level="N5"):
    options_data = _dedup(options_data, correct)
    return make_question(question, correct, options_data, unit, scaffold=scaffold,
                         notes=notes, topic="Dynamics", question_type="Acceleration", level=level)


def _choice_question(question_text, correct, distractors, working, level):
    """Text-choice (classification) question: correct is a string, distractors are
    (option_text, mistake) pairs."""
    distractor_data = [{"value": text, "mistake": mistake, "working": working}
                       for text, mistake in distractors]
    options = [correct] + [text for text, _ in distractors]
    random.shuffle(options)
    return PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        distractors=distractor_data,
        working=working,
        notes=_LIGHT_GATE_NOTES,
        topic="Dynamics",
        question_type="Acceleration",
        level=level,
        metadata={"type": "classification", "options": options},
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sub-type 1 — Using a = (v − u) / t
# ═══════════════════════════════════════════════════════════════════════════

_N5_ACCELS = [0.4, 0.5, 0.8, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0]


def gen_find_acceleration(level="N5"):
    obj = random.choice(_CONTEXTS)
    a = random.choice(_N5_ACCELS)
    t = random.choice([2.0, 2.5, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0])
    case = random.choice(["speeds up", "from rest", "slows down"])

    if case == "from rest":
        u = 0.0
        v = round(a * t, 1)
        question = (f"A {obj} starts from rest and reaches a speed of {_fmt(v)} m/s in {_fmt(t)} s.\n\n"
                    f"Calculate the acceleration of the {obj}.")
    elif case == "speeds up":
        u = float(random.randint(2, 15))
        v = round(u + a * t, 1)
        question = (f"A {obj} speeds up from {_fmt(u)} m/s to {_fmt(v)} m/s in {_fmt(t)} s.\n\n"
                    f"Calculate the acceleration of the {obj}.")
    else:
        v = float(random.randint(0, 8))
        u = round(v + a * t, 1)
        question = (f"A {obj} slows down from {_fmt(u)} m/s to {_fmt(v)} m/s in {_fmt(t)} s.\n\n"
                    f"Calculate the acceleration of the {obj}.")

    correct = round((v - u) / t, 2)
    working = [
        {"type": "latex", "content": r"a = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"a = \frac{{{_fmt(v)} - {_fmt(u)}}}{{{_fmt(t)}}}"},
        {"type": "latex", "content": rf"a = {_fmt(correct)}\ \mathrm{{m/s^2}}"},
    ]
    if correct < 0:
        working.append({"type": "text", "content": "The negative sign shows the object is decelerating "
                                                   "(slowing down)."})
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": -correct,
         "mistake": "You calculated (u − v) ÷ t. It is final speed minus initial speed: a = (v − u) ÷ t. "
                    "An object that is slowing down has a negative acceleration.",
         "working": working},
        {"value": round(v - u, 2),
         "mistake": "That's the change in speed — you still need to divide by the time.",
         "working": working},
        {"value": round(v / t, 2),
         "mistake": "You divided the final speed by the time — subtract the initial speed first.",
         "working": working},
        {"value": round((v + u) / t, 2),
         "mistake": "You added the speeds. Acceleration uses the change in speed, v − u.",
         "working": working},
    ]
    return _with_acceleration_widget(_question(question, correct, options_data, "m/s²",
                                               NOTES["acceleration_s3"], level=level))


def gen_find_final_speed(level="N5"):
    obj = random.choice(_CONTEXTS)
    a = random.choice(_N5_ACCELS)
    t = random.choice([2.0, 3.0, 4.0, 5.0, 6.0, 8.0])
    u = float(random.randint(0, 20))
    correct = round(u + a * t, 2)

    start = "starts from rest and" if u == 0 else f"is travelling at {_fmt(u)} m/s. It then"
    question = (f"A {obj} {start} accelerates uniformly at {_fmt(a)} m/s² for {_fmt(t)} s.\n\n"
                f"Calculate the final speed of the {obj}.")
    working = [
        {"type": "latex", "content": r"a = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"{_fmt(a)} = \frac{{v - {_fmt(u)}}}{{{_fmt(t)}}}"},
        {"type": "latex", "content": rf"v = {_fmt(u)} + ({_fmt(a)} \times {_fmt(t)})"},
        {"type": "latex", "content": rf"v = {_fmt(correct)}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round(a * t, 2),
         "mistake": "That's only the change in speed (at) — add it to the initial speed: v = u + at.",
         "working": working},
        {"value": round(u - a * t, 2),
         "mistake": "The object is speeding up, so add at to u: v = u + at.",
         "working": working},
        {"value": round((u + a) * t, 2),
         "mistake": "Only the acceleration is multiplied by the time: v = u + (a × t).",
         "working": working},
        {"value": round(u + a / t, 2),
         "mistake": "You divided a by t — the change in speed is a × t.",
         "working": working},
        {"value": round(u + a + t, 2),
         "mistake": "You added a and t — the change in speed is a × t.",
         "working": working},
    ]
    return _with_acceleration_widget(_question(question, correct, options_data, "m/s",
                                               NOTES["acceleration_s3"], level=level))


def gen_find_initial_speed(level="N5"):
    obj = random.choice(_CONTEXTS)
    a = random.choice(_N5_ACCELS)
    t = random.choice([2.0, 3.0, 4.0, 5.0, 6.0, 8.0])
    v = float(random.randint(0, 12))
    correct = round(v + a * t, 2)   # slowing down: u = v − (−a)t

    question = (f"A {obj} slows down at a constant rate of {_fmt(a)} m/s² for {_fmt(t)} s.\n\n"
                f"Its final speed is {_fmt(v)} m/s.\n\n"
                f"Calculate the initial speed of the {obj}.")
    working = [
        {"type": "text",  "content": "The object is slowing down, so its acceleration is negative:"},
        {"type": "latex", "content": rf"a = -{_fmt(a)}\ \mathrm{{m/s^2}}"},
        {"type": "latex", "content": r"a = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"-{_fmt(a)} = \frac{{{_fmt(v)} - u}}{{{_fmt(t)}}}"},
        {"type": "latex", "content": rf"u = {_fmt(v)} + ({_fmt(a)} \times {_fmt(t)})"},
        {"type": "latex", "content": rf"u = {_fmt(correct)}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round(v - a * t, 2),
         "mistake": "The object is slowing down, so it must have started faster than it finished. "
                    "The acceleration is negative, which gives u = v + (a × t) here.",
         "working": working},
        {"value": round(a * t, 2),
         "mistake": "That's only the change in speed — add it to the final speed.",
         "working": working},
        {"value": round(a * t - v, 2),
         "mistake": "Check the rearrangement: the initial speed is the final speed plus the speed lost.",
         "working": working},
        {"value": round(v + a / t, 2),
         "mistake": "You divided a by t — the speed lost is a × t.",
         "working": working},
        {"value": round(v + a + t, 2),
         "mistake": "You added a and t — the speed lost is a × t.",
         "working": working},
    ]
    return _with_acceleration_widget(_question(question, correct, options_data, "m/s",
                                               NOTES["acceleration_s3"], level=level))


def gen_find_time(level="N5"):
    obj = random.choice(_CONTEXTS)
    a = random.choice(_N5_ACCELS)
    t_true = random.choice([2.0, 2.5, 4.0, 5.0, 6.0, 8.0, 10.0])
    u = float(random.randint(0, 10))
    v = round(u + a * t_true, 1)
    correct = round((v - u) / a, 2)

    start = "from rest" if u == 0 else f"from {_fmt(u)} m/s"
    question = (f"A {obj} accelerates uniformly at {_fmt(a)} m/s² {start} to {_fmt(v)} m/s.\n\n"
                f"Calculate the time taken.")
    working = [
        {"type": "latex", "content": r"a = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"{_fmt(a)} = \frac{{{_fmt(v)} - {_fmt(u)}}}{{t}}"},
        {"type": "latex", "content": rf"t = \frac{{{_fmt(v)} - {_fmt(u)}}}{{{_fmt(a)}}}"},
        {"type": "latex", "content": rf"t = {_fmt(correct)}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round(v / a, 2),
         "mistake": "You divided the final speed by a — use the change in speed, v − u.",
         "working": working},
        {"value": round((v - u) * a, 2),
         "mistake": "You multiplied by the acceleration — rearrange to t = (v − u) ÷ a.",
         "working": working},
        {"value": round(a / (v - u), 3),
         "mistake": "You divided the wrong way round — t = (v − u) ÷ a.",
         "working": working},
        {"value": round(v - u, 2),
         "mistake": "That's the change in speed — divide it by the acceleration to find the time.",
         "working": working},
    ]
    return _with_acceleration_widget(_question(question, correct, options_data, "s",
                                               NOTES["acceleration_s3"], level=level))


def generate_acceleration_equation(level="N5"):
    return random.choice([gen_find_acceleration, gen_find_final_speed,
                          gen_find_initial_speed, gen_find_time])(level=level)


# ═══════════════════════════════════════════════════════════════════════════
# Sub-type 2 — Trolley on a slope: light-gate calculations
# (SQA 2015 P2 Q8, 2018 P2 Q2, 2020 P2 Q2)
# ═══════════════════════════════════════════════════════════════════════════

def _card_length():
    """Returns (length_m, display_str, raw_cm_or_None)."""
    cm = random.choice([2.5, 3.0, 4.0, 4.5, 5.0, 6.0])
    if random.random() < 0.5:
        return cm / 100, f"{_fmt(cm)} cm", cm
    return cm / 100, f"{_fmt(round(cm / 100, 3))} m", None


def gen_speed_at_light_gate(level="N5"):
    length_m, length_str, raw_cm = _card_length()
    v_target = random.choice([0.25, 0.3, 0.4, 0.45, 0.5, 0.6, 0.75, 0.8])
    t_gate = round(length_m / v_target, 3)
    correct = round(length_m / t_gate, 2)

    question = (f"A trolley rolls down a slope. A card of length {length_str} is fixed to the trolley.\n\n"
                f"The card takes {_fmt(t_gate)} s to pass through a light gate.\n\n"
                f"Calculate the instantaneous speed of the trolley at the light gate.")
    working = []
    if raw_cm is not None:
        working.append({"type": "text", "content": f"Convert the card length to metres: "
                                                   f"{length_str} = {_fmt(length_m)} m"})
    working += [
        {"type": "latex", "content": r"v = \frac{d}{t}"},
        {"type": "latex", "content": rf"v = \frac{{{_fmt(length_m)}}}{{{_fmt(t_gate)}}}"},
        {"type": "latex", "content": rf"v = {_fmt(correct)}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round(t_gate / length_m, 2),
         "mistake": "You divided time by distance — speed = card length ÷ time.",
         "working": working},
        {"value": round(length_m * t_gate, 5),
         "mistake": "You multiplied — speed = card length ÷ time.",
         "working": working},
    ]
    scaffold = None
    if raw_cm is not None:
        options_data.append({
            "value": round(raw_cm / t_gate, 1),
            "mistake": "You used the card length in cm — convert it to metres first.",
            "working": working,
        })
        scaffold = [
            {"question": "What is the length of the card in metres?", "answer": length_m, "unit": "m"},
            {"question": "What is the instantaneous speed at the light gate?", "answer": correct, "unit": "m/s"},
        ]
    return _question(question, correct, options_data, "m/s", _LIGHT_GATE_NOTES,
                     scaffold=scaffold, level=level)


def gen_two_gate_acceleration(level="N5"):
    length_m, length_str, raw_cm = _card_length()
    u_target = random.choice([0.2, 0.25, 0.3, 0.35, 0.4, 0.5])
    a_target = random.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8])
    t_between = random.choice([0.4, 0.5, 0.56, 0.6, 0.75, 0.8, 1.0])
    v_target = u_target + a_target * t_between

    t_x = round(length_m / u_target, 3)
    t_y = round(length_m / v_target, 3)
    v_x = round(length_m / t_x, 2)
    v_y = round(length_m / t_y, 2)
    correct = round((v_y - v_x) / t_between, 2)

    question = (
        "A student uses two light gates, X and Y, to measure the acceleration of a trolley "
        "rolling down a slope. A card is fixed to the trolley.\n\n"
        f"- Length of card: {length_str}\n"
        f"- Time for card to pass through light gate X: {_fmt(t_x)} s\n"
        f"- Time for card to pass through light gate Y: {_fmt(t_y)} s\n"
        f"- Time for trolley to travel from light gate X to light gate Y: {_fmt(t_between)} s\n\n"
        "Determine the acceleration of the trolley."
    )
    working = []
    if raw_cm is not None:
        working.append({"type": "text", "content": f"Card length = {length_str} = {_fmt(length_m)} m"})
    working += [
        {"type": "text",  "content": "Speed at light gate X (initial speed):"},
        {"type": "latex", "content": rf"u = \frac{{{_fmt(length_m)}}}{{{_fmt(t_x)}}} = {_fmt(v_x)}\ \mathrm{{m/s}}"},
        {"type": "text",  "content": "Speed at light gate Y (final speed):"},
        {"type": "latex", "content": rf"v = \frac{{{_fmt(length_m)}}}{{{_fmt(t_y)}}} = {_fmt(v_y)}\ \mathrm{{m/s}}"},
        {"type": "text",  "content": "Use the time taken to travel between the gates:"},
        {"type": "latex", "content": r"a = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"a = \frac{{{_fmt(v_y)} - {_fmt(v_x)}}}{{{_fmt(t_between)}}}"},
        {"type": "latex", "content": rf"a = {_fmt(correct)}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round(v_y - v_x, 2),
         "mistake": "That's the change in speed — divide it by the time taken to travel between the gates.",
         "working": working},
        {"value": round(v_y / t_between, 2),
         "mistake": "The trolley was already moving at gate X, so u isn't zero — use a = (v − u) ÷ t.",
         "working": working},
        {"value": round((v_y - v_x) / t_y, 2),
         "mistake": "t is the time to travel between the gates, not the time for the card to pass through a gate.",
         "working": working},
        {"value": round((v_y - v_x) / (t_y - t_x), 2),
         "mistake": "The gate times are for the card passing through each gate — t is the time taken "
                    "to travel between the gates.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the speed of the trolley at light gate X?", "answer": v_x, "unit": "m/s"},
        {"question": "What is the speed of the trolley at light gate Y?", "answer": v_y, "unit": "m/s"},
        {"question": "What is the acceleration of the trolley?", "answer": correct, "unit": "m/s²"},
    ]
    return _question(question, correct, options_data, "m/s²", _LIGHT_GATE_NOTES,
                     scaffold=scaffold, level=level)


def gen_one_gate_from_rest(level="N5"):
    length_m, length_str, raw_cm = _card_length()
    a_target = random.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.6])
    t_release = random.choice([1.2, 1.5, 1.6, 2.0, 2.4, 2.5])
    v_target = a_target * t_release

    t_gate = round(length_m / v_target, 3)
    v = round(length_m / t_gate, 2)
    correct = round(v / t_release, 2)

    question = (
        "A trolley is released from rest at the top of a slope. A card is fixed to the trolley "
        "and a light gate is placed further down the slope.\n\n"
        f"- Length of card: {length_str}\n"
        f"- Time for card to pass through the light gate: {_fmt(t_gate)} s\n"
        f"- Time from release until the card reaches the light gate (stop-clock): {_fmt(t_release)} s\n\n"
        "Determine the acceleration of the trolley."
    )
    working = []
    if raw_cm is not None:
        working.append({"type": "text", "content": f"Card length = {length_str} = {_fmt(length_m)} m"})
    working += [
        {"type": "text",  "content": "Speed at the light gate (final speed):"},
        {"type": "latex", "content": rf"v = \frac{{{_fmt(length_m)}}}{{{_fmt(t_gate)}}} = {_fmt(v)}\ \mathrm{{m/s}}"},
        {"type": "text",  "content": "Released from rest, so u = 0:"},
        {"type": "latex", "content": r"a = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"a = \frac{{{_fmt(v)} - 0}}{{{_fmt(t_release)}}}"},
        {"type": "latex", "content": rf"a = {_fmt(correct)}\ \mathrm{{m/s^2}}"},
    ]
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round(v / t_gate, 2),
         "mistake": "t is the time from release to the light gate, not the time for the card to pass through the gate.",
         "working": working},
        {"value": v,
         "mistake": "That's the speed at the light gate — divide it by the time taken to reach the gate.",
         "working": working},
        {"value": round(v * t_release, 2),
         "mistake": "You multiplied by the time — a = (v − u) ÷ t.",
         "working": working},
    ]
    scaffold = [
        {"question": "What is the speed of the trolley at the light gate?", "answer": v, "unit": "m/s"},
        {"question": "What is the acceleration of the trolley?", "answer": correct, "unit": "m/s²"},
    ]
    return _question(question, correct, options_data, "m/s²", _LIGHT_GATE_NOTES,
                     scaffold=scaffold, level=level)


def gen_time_between_gates(level="N5"):
    u = random.choice([0.2, 0.25, 0.3, 0.4, 0.5])
    a = random.choice([0.2, 0.25, 0.4, 0.5, 0.8])
    t_true = random.choice([0.4, 0.5, 0.6, 0.8, 1.0, 1.2])
    v = round(u + a * t_true, 2)
    correct = round((v - u) / a, 2)

    question = (
        f"A trolley accelerates down a slope at {_fmt(a)} m/s². Light gates measure its speed as "
        f"{_fmt(u)} m/s at light gate X and {_fmt(v)} m/s at light gate Y.\n\n"
        "Calculate the time taken for the trolley to travel from light gate X to light gate Y."
    )
    working = [
        {"type": "latex", "content": r"a = \frac{v - u}{t}"},
        {"type": "latex", "content": rf"{_fmt(a)} = \frac{{{_fmt(v)} - {_fmt(u)}}}{{t}}"},
        {"type": "latex", "content": rf"t = {_fmt(correct)}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": correct, "mistake": None, "working": working},
        {"value": round(v / a, 2),
         "mistake": "The trolley is already moving at gate X — use the change in speed, v − u.",
         "working": working},
        {"value": round((v - u) * a, 3),
         "mistake": "You multiplied by the acceleration — rearrange to t = (v − u) ÷ a.",
         "working": working},
        {"value": round((v + u) / a, 2),
         "mistake": "You added the speeds — acceleration uses the change in speed, v − u.",
         "working": working},
    ]
    return _question(question, correct, options_data, "s", _LIGHT_GATE_NOTES, level=level)


def generate_trolley_light_gates(level="N5"):
    return random.choice([gen_speed_at_light_gate, gen_two_gate_acceleration,
                          gen_two_gate_acceleration, gen_one_gate_from_rest,
                          gen_time_between_gates])(level=level)


# ═══════════════════════════════════════════════════════════════════════════
# Sub-type 3 — Trolley on a slope: method and explanation
# (SQA 2015 P2 Q8a, 2017 P1 Q16, 2020 P2 Q2a, 2022 P1 Q2)
# ═══════════════════════════════════════════════════════════════════════════

def gen_measurements_two_gates(level="N5"):
    question = (
        "A student uses a trolley with a card attached, two light gates and electronic timers to "
        "determine the acceleration of the trolley as it rolls down a slope.\n\n"
        "Which measurements must the student make?"
    )
    correct = ("Length of the card, time for the card to pass through each light gate, "
               "and time for the trolley to travel between the light gates")
    working = [
        {"type": "text", "content": "Speed at each gate = length of card ÷ time for the card to pass "
                                    "through that gate. This gives u (first gate) and v (second gate)."},
        {"type": "text", "content": "t in a = (v − u) ÷ t is the time to travel between the gates."},
    ]
    distractors = [
        ("Length of the card, time for the card to pass through each light gate, "
         "and the distance between the light gates",
         "The distance between the gates isn't used in a = (v − u) ÷ t — you need the time "
         "taken to travel between the gates."),
        ("Mass of the trolley, length of the card, and time for the card to pass through each light gate",
         "Mass isn't needed to find acceleration from speeds — and without the time between "
         "the gates you can't use a = (v − u) ÷ t."),
        ("Distance between the light gates and time for the trolley to travel between them",
         "That only gives the average speed between the gates. You need the speed at each "
         "gate, which requires the card length and the time at each gate."),
    ]
    return _choice_question(question, correct, distractors, working, level)


def gen_measurements_one_gate(level="N5"):
    question = (
        "A trolley is released from rest at the top of a ramp. A card is fixed to the trolley and "
        "there is a single light gate further down the ramp. The student also has a stop-clock.\n\n"
        "Which measurements must the student make to determine the acceleration of the trolley?"
    )
    correct = ("Length of the card, time for the card to pass through the light gate, "
               "and time from release until the trolley reaches the light gate")
    working = [
        {"type": "text", "content": "Final speed v = length of card ÷ time for card to pass through the gate."},
        {"type": "text", "content": "Initial speed u = 0 because the trolley is released from rest."},
        {"type": "text", "content": "t = time from release until the trolley reaches the gate (stop-clock)."},
    ]
    distractors = [
        ("Length of the card and time for the card to pass through the light gate only",
         "This gives the speed at the gate, but you also need the time taken to reach that "
         "speed — the time from release to the gate."),
        ("Length of the ramp and time from release until the trolley reaches the light gate",
         "That gives an average speed, not the speed at the gate. You need the card length "
         "and the time for the card to pass through the gate."),
        ("Mass of the trolley, length of the card, and time for the card to pass through the light gate",
         "Mass isn't needed — and you still need the time taken to reach the gate."),
    ]
    return _choice_question(question, correct, distractors, working, level)


def gen_release_point(level="N5"):
    closer = random.choice([True, False])
    where = ("closer to the light gates (further down the slope)" if closer
             else "further up the slope, further from the light gates")
    speed_word = "less" if closer else "greater"
    question = (
        "A trolley is released from rest and rolls down a slope with constant acceleration. A computer "
        "connected to two light gates displays the acceleration and the average speed of the trolley "
        "between the gates.\n\n"
        f"The trolley is now released from rest at a point {where}. The slope is unchanged.\n\n"
        "How do the new results compare with the first results?"
    )
    correct = f"Acceleration: the same. Average speed between the gates: {speed_word}."
    working = [
        {"type": "text", "content": "The slope is unchanged, so the unbalanced force on the trolley and "
                                    "its acceleration are the same."},
        {"type": "text", "content": "Released closer to the gates, the trolley has less time to speed up "
                                    "before reaching them, so it is moving more slowly between them."
                                    if closer else
                                    "Released further from the gates, the trolley has more time to speed up "
                                    "before reaching them, so it is moving faster between them."},
    ]
    other = "greater" if closer else "less"
    distractors = [
        (f"Acceleration: {speed_word}. Average speed between the gates: {speed_word}.",
         "The acceleration depends on the slope, not on where the trolley is released. "
         "The slope hasn't changed."),
        ("Acceleration: the same. Average speed between the gates: the same.",
         f"The trolley reaches the gates {'sooner' if closer else 'later'}, having had "
         f"{'less' if closer else 'more'} time to speed up — so its speed there is different."),
        (f"Acceleration: the same. Average speed between the gates: {other}.",
         "Think about how long the trolley has been speeding up before it reaches the gates."),
    ]
    return _choice_question(question, correct, distractors, working, level)


def gen_steeper_slope(level="N5"):
    steeper = random.choice([True, False])
    change = "made steeper" if steeper else "made less steep"
    question = (
        "A student measures the acceleration of a trolley as it rolls down a slope using light gates.\n\n"
        f"The slope is now {change}. The trolley is released from the same point on the slope.\n\n"
        "What happens to the acceleration of the trolley?"
    )
    correct = "The acceleration increases." if steeper else "The acceleration decreases."
    working = [
        {"type": "text", "content": f"A {'steeper' if steeper else 'less steep'} slope gives a "
                                    f"{'larger' if steeper else 'smaller'} unbalanced force down the slope, "
                                    f"so the acceleration {'increases' if steeper else 'decreases'}."},
    ]
    wrong = "The acceleration decreases." if steeper else "The acceleration increases."
    distractors = [
        (wrong, f"A {'steeper' if steeper else 'less steep'} slope makes the unbalanced force down the "
                f"slope {'bigger' if steeper else 'smaller'}."),
        ("The acceleration stays the same.",
         "Changing the angle of the slope changes the unbalanced force on the trolley, so the "
         "acceleration changes."),
    ]
    return _choice_question(question, correct, distractors, working, level)


def gen_constant_acceleration_speeds(level="N5"):
    u = random.choice([0.0, 0.0, 1.0, 2.0])
    dv = random.choice([2.0, 3.0, 4.0])
    v = u + dv
    avg = (u + v) / 2
    start = "is released from rest at P" if u == 0 else "passes P"
    question = (
        f"A toy car {start} and travels down a slope with a constant acceleration to Q.\n\n"
        "Which set of values could be the speed at P, the speed at Q, and the average speed "
        "between P and Q?"
    )

    def row(p, q, a):
        return f"Speed at P: {_fmt(p)} m/s, speed at Q: {_fmt(q)} m/s, average speed: {_fmt(a)} m/s"

    correct = row(u, v, avg)
    working = [
        {"type": "text", "content": "With constant acceleration the speed increases steadily, so the average "
                                    "speed is halfway between the speed at P and the speed at Q."},
        {"type": "latex", "content": rf"\text{{average speed}} = \frac{{{_fmt(u)} + {_fmt(v)}}}{{2}} = {_fmt(avg)}\ \mathrm{{m/s}}"},
    ]
    distractors = [
        (row(u, v, v),
         "The car is speeding up, so its average speed must be less than its speed at Q."),
        (row(v, v, v),
         "With constant acceleration, the speed at Q must be greater than the speed at P."),
        (row(v, u, avg),
         "The car is accelerating down the slope, so it must be faster at Q than at P."),
    ]
    if u > 0:
        distractors.append((row(u, v, u + v),
                            "The average speed is halfway between the two speeds — not their sum."))
    return _choice_question(question, correct, distractors, working, level)


def generate_trolley_explain(level="N5"):
    return random.choice([gen_measurements_two_gates, gen_measurements_one_gate,
                          gen_release_point, gen_steeper_slope,
                          gen_constant_acceleration_speeds])(level=level)
