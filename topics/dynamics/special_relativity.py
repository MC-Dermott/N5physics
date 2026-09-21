import random
import math
import pathlib
from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

_WIDGET_HTML = (
    pathlib.Path(__file__).parent.parent.parent / "core" / "data" / "relativity_widget.html"
).read_text(encoding="utf-8")

_NOTES = """
## Special Relativity

**Definitions:**
- Time dilation is the stretching of the time interval between two events as measured by an
  observer who sees the clock moving, compared with an observer moving with the clock.
- Length contraction is the shortening of an object's measured length, along its direction of
  travel, as observed by someone it is moving relative to.

**Time dilation** — a moving clock runs slow:
$$t' = \\frac{t}{\\sqrt{1 - \\frac{v^2}{c^2}}}$$

**Length contraction** — a moving object appears shorter:
$$l' = l\\sqrt{1 - \\frac{v^2}{c^2}}$$

| Symbol | Quantity | Unit |
|---|---|---|
| t | Proper time (measured in moving frame) | s |
| t' | Dilated time (measured by stationary observer) | s |
| l | Proper length (measured in rest frame of object) | m |
| l' | Contracted length (measured by stationary observer) | m |
| v | Speed of the moving object | m/s |
| c | Speed of light = 3 × 10⁸ m/s | m/s |

> **Important:** t' > t (stationary observer measures a longer time).
> l' < l (stationary observer measures a shorter length).
> Both formulae use the same factor √(1 − v²/c²).

**Before relativity — simple (Newtonian) relative velocity:** at everyday speeds,
velocities in different frames simply add or subtract.

**Einstein's postulates:**
1. The laws of physics are the same in all inertial frames of reference (a frame that is
   not accelerating).
2. The speed of light in a vacuum is the same for all observers, regardless of the motion
   of the source or the observer — unlike everyday velocities, speeds do not add to it.
"""

_C = 3.00e8  # speed of light, m/s

# (v/c fraction, display string, √(1−v²/c²))
_VELOCITIES = [
    (0.6, "0.6c", 0.8),
    (0.8, "0.8c", 0.6),
]


def _v_sci(v):
    """Format a speed near the order of c as 'm.mm × 10^8' LaTeX."""
    exp = 8
    mantissa = v / 10 ** exp
    return rf"{mantissa:.2f} \times 10^{{{exp}}}"

_SHIP_CONTEXTS = [
    "A spacecraft",
    "A rocket",
    "A probe",
    "A space shuttle",
]


def _ship():
    return random.choice(_SHIP_CONTEXTS)


# ── Time dilation: t' = t / √(1 − v²/c²) ────────────────────────────────────

def gen_t_prime(level="Higher"):
    v_frac, v_str, lor = random.choice(_VELOCITIES)
    # pick t so t' = t/lor is a clean integer
    # lor = 0.8 → t multiples of 4 give clean t'; lor = 0.6 → multiples of 3
    base = 4 if lor == 0.8 else 3
    t = base * random.randint(1, 5)
    t_prime = round(t / lor, 4)
    ship = _ship()
    question = (
        f"{ship} travels at {v_str} relative to an observer on Earth. "
        f"An astronaut on board measures the journey time to be {t} s. "
        f"What journey time does the Earth observer measure?"
    )
    working = [
        {"type": "text",  "content": "Use the time dilation formula:"},
        {"type": "latex", "content": r"t' = \frac{t}{\sqrt{1 - \frac{v^2}{c^2}}}"},
        {"type": "latex", "content": rf"t' = \frac{{{t}}}{{\sqrt{{1 - {v_frac}^2}}}}"},
        {"type": "latex", "content": rf"t' = \frac{{{t}}}{{\sqrt{{1 - {round(v_frac**2,2)}}}}}"},
        {"type": "latex", "content": rf"t' = \frac{{{t}}}{{{lor}}}"},
        {"type": "latex", "content": rf"t' = {t_prime}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t_prime,              "mistake": None, "working": working},
        {"value": round(t * lor, 4),    "mistake": "You multiplied by √(1−v²/c²) instead of dividing — that is the length contraction formula, not time dilation.", "working": working},
        {"value": round(t / lor**2, 4), "mistake": "Divide by √(1−v²/c²), not by (1−v²/c²) — don't forget the square root.", "working": working},
        {"value": t,                    "mistake": "You must apply the time dilation formula — the Earth observer measures a longer time than the astronaut.", "working": working},
    ]
    options_data = _dedup(options_data, t_prime)
    scaffold = [
        {"question": "What is √(1 − v²/c²)?", "answer": lor},
        {"question": "What is the dilated time t′ measured by the Earth observer?", "answer": t_prime},
    ]
    return make_question(question, t_prime, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level, scaffold=scaffold)


def gen_t_proper(level="Higher"):
    v_frac, v_str, lor = random.choice(_VELOCITIES)
    base = 4 if lor == 0.8 else 3
    t = base * random.randint(1, 5)
    t_prime = round(t / lor, 4)
    ship = _ship()
    question = (
        f"{ship} travels at {v_str} relative to an observer on Earth. "
        f"The Earth observer measures the journey time to be {t_prime} s. "
        f"What time does the astronaut's clock show for the journey?"
    )
    working = [
        {"type": "text",  "content": "Rearrange t' = t / √(1 − v²/c²) for t:"},
        {"type": "latex", "content": r"t = t'\sqrt{1 - \frac{v^2}{c^2}}"},
        {"type": "latex", "content": rf"t = {t_prime} \times \sqrt{{1 - {v_frac}^2}}"},
        {"type": "latex", "content": rf"t = {t_prime} \times {lor}"},
        {"type": "latex", "content": rf"t = {t}\ \mathrm{{s}}"},
    ]
    options_data = [
        {"value": t,                        "mistake": None, "working": working},
        {"value": round(t_prime / lor, 4),  "mistake": "Divide by √(1−v²/c²) only when going from proper time to dilated time — here you need to multiply.", "working": working},
        {"value": round(t_prime * lor**2, 4),"mistake": "Multiply by √(1−v²/c²), not by (1−v²/c²) — don't forget the square root.", "working": working},
        {"value": t_prime,                  "mistake": "The astronaut's clock runs slow — their time is shorter than the Earth observer's time.", "working": working},
    ]
    options_data = _dedup(options_data, t)
    scaffold = [
        {"question": "What is √(1 − v²/c²)?", "answer": lor},
        {"question": "What is the proper time t shown on the astronaut's clock?", "answer": t},
    ]
    return make_question(question, t, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level, scaffold=scaffold)


def gen_v_from_time_dilation(level="Higher"):
    v_frac, v_str, lor = random.choice(_VELOCITIES)
    base = 4 if lor == 0.8 else 3
    t = base * random.randint(1, 5)
    t_prime = round(t / lor, 4)
    v = round(v_frac * _C, 4)
    ship = _ship()
    question = (
        f"{ship} makes a journey which an astronaut on board times at {t} s, while an observer "
        f"on Earth times the same journey at {t_prime} s. Calculate the speed of the spacecraft "
        f"relative to the Earth observer."
    )
    working = [
        {"type": "text",  "content": "Rearrange t' = t / √(1 − v²/c²) for v:"},
        {"type": "latex", "content": r"\sqrt{1 - \frac{v^2}{c^2}} = \frac{t}{t'}"},
        {"type": "latex", "content": rf"\sqrt{{1 - \frac{{v^2}}{{c^2}}}} = \frac{{{t}}}{{{t_prime}}} = {lor}"},
        {"type": "latex", "content": r"v = c\sqrt{1 - \left(\frac{t}{t'}\right)^2}"},
        {"type": "latex", "content": rf"v = (3.00\times10^8) \times \sqrt{{1 - {lor}^2}}"},
        {"type": "latex", "content": rf"v = (3.00\times10^8) \times {v_frac}"},
        {"type": "latex", "content": rf"v = {_v_sci(v)}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v,                          "mistake": None, "working": working},
        {"value": round(lor * _C, 4),         "mistake": "You found √(1−v²/c²) = t/t′ but then treated that value as v/c itself — you need v = c√(1−(t/t′)²).", "working": working},
        {"value": round((1 - lor ** 2) * _C, 4), "mistake": "You forgot to take the square root when finding v from 1 − (t/t′)².", "working": working},
        {"value": round((t_prime / t - 1) * _C, 4), "mistake": "That isn't how the time dilation formula rearranges for v — use v = c√(1−(t/t′)²).", "working": working},
    ]
    options_data = _dedup(options_data, v)
    scaffold = [
        {"question": "What is t/t′?", "answer": lor},
        {"question": "What is the speed v of the spacecraft, in m/s?", "answer": v},
    ]
    return make_question(question, v, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level, scaffold=scaffold)


# ── Length contraction: l' = l × √(1 − v²/c²) ────────────────────────────────

def gen_l_prime(level="Higher"):
    v_frac, v_str, lor = random.choice(_VELOCITIES)
    # pick l so l' = l*lor is a clean integer
    # lor = 0.8 → multiples of 5; lor = 0.6 → multiples of 5
    l = 5 * random.randint(1, 6)
    l_prime = round(l * lor, 4)
    ship = _ship()
    question = (
        f"{ship} is {l} m long when measured at rest. "
        f"It then travels at {v_str} relative to an observer on Earth. "
        f"What length does the Earth observer measure for the spacecraft?"
    )
    working = [
        {"type": "text",  "content": "Use the length contraction formula:"},
        {"type": "latex", "content": r"l' = l\sqrt{1 - \frac{v^2}{c^2}}"},
        {"type": "latex", "content": rf"l' = {l} \times \sqrt{{1 - {v_frac}^2}}"},
        {"type": "latex", "content": rf"l' = {l} \times {lor}"},
        {"type": "latex", "content": rf"l' = {l_prime}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": l_prime,              "mistake": None, "working": working},
        {"value": round(l / lor, 4),    "mistake": "You divided by √(1−v²/c²) instead of multiplying — that is the time dilation rearrangement, not length contraction.", "working": working},
        {"value": round(l * lor**2, 4), "mistake": "Multiply by √(1−v²/c²), not by (1−v²/c²) — don't forget the square root.", "working": working},
        {"value": l,                    "mistake": "You must apply the length contraction formula — the Earth observer measures a shorter length.", "working": working},
    ]
    options_data = _dedup(options_data, l_prime)
    scaffold = [
        {"question": "What is √(1 − v²/c²)?", "answer": lor},
        {"question": "What is the contracted length l′ measured by the Earth observer?", "answer": l_prime},
    ]
    return make_question(question, l_prime, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level, scaffold=scaffold)


def gen_l_proper(level="Higher"):
    v_frac, v_str, lor = random.choice(_VELOCITIES)
    l = 5 * random.randint(1, 6)
    l_prime = round(l * lor, 4)
    ship = _ship()
    question = (
        f"{ship} travels at {v_str} relative to an observer on Earth. "
        f"The Earth observer measures the spacecraft to be {l_prime} m long. "
        f"What is the proper length of the spacecraft?"
    )
    working = [
        {"type": "text",  "content": "Rearrange l' = l√(1 − v²/c²) for l:"},
        {"type": "latex", "content": r"l = \frac{l'}{\sqrt{1 - \frac{v^2}{c^2}}}"},
        {"type": "latex", "content": rf"l = \frac{{{l_prime}}}{{\sqrt{{1 - {v_frac}^2}}}}"},
        {"type": "latex", "content": rf"l = \frac{{{l_prime}}}{{{lor}}}"},
        {"type": "latex", "content": rf"l = {l}\ \mathrm{{m}}"},
    ]
    options_data = [
        {"value": l,                        "mistake": None, "working": working},
        {"value": round(l_prime * lor, 4),  "mistake": "Multiply by √(1−v²/c²) only when going from proper length to contracted length — here you need to divide.", "working": working},
        {"value": round(l_prime / lor**2, 4),"mistake": "Divide by √(1−v²/c²), not by (1−v²/c²) — don't forget the square root.", "working": working},
        {"value": l_prime,                  "mistake": "The proper length is always longer than the contracted length — divide l' by √(1−v²/c²).", "working": working},
    ]
    options_data = _dedup(options_data, l)
    scaffold = [
        {"question": "What is √(1 − v²/c²)?", "answer": lor},
        {"question": "What is the proper length l of the spacecraft?", "answer": l},
    ]
    return make_question(question, l, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level, scaffold=scaffold)


def gen_v_from_length_contraction(level="Higher"):
    v_frac, v_str, lor = random.choice(_VELOCITIES)
    l = 5 * random.randint(1, 6)
    l_prime = round(l * lor, 4)
    v = round(v_frac * _C, 4)
    ship = _ship()
    question = (
        f"{ship} is {l} m long when measured at rest. An observer on Earth measures its length "
        f"as {l_prime} m while it is in flight. Calculate the speed of the spacecraft relative "
        f"to the Earth observer."
    )
    working = [
        {"type": "text",  "content": "Rearrange l' = l√(1 − v²/c²) for v:"},
        {"type": "latex", "content": r"\sqrt{1 - \frac{v^2}{c^2}} = \frac{l'}{l}"},
        {"type": "latex", "content": rf"\sqrt{{1 - \frac{{v^2}}{{c^2}}}} = \frac{{{l_prime}}}{{{l}}} = {lor}"},
        {"type": "latex", "content": r"v = c\sqrt{1 - \left(\frac{l'}{l}\right)^2}"},
        {"type": "latex", "content": rf"v = (3.00\times10^8) \times \sqrt{{1 - {lor}^2}}"},
        {"type": "latex", "content": rf"v = (3.00\times10^8) \times {v_frac}"},
        {"type": "latex", "content": rf"v = {_v_sci(v)}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": v,                             "mistake": None, "working": working},
        {"value": round(lor * _C, 4),            "mistake": "You found √(1−v²/c²) = l′/l but then treated that value as v/c itself — you need v = c√(1−(l′/l)²).", "working": working},
        {"value": round((1 - lor ** 2) * _C, 4), "mistake": "You forgot to take the square root when finding v from 1 − (l′/l)².", "working": working},
        {"value": round((1 - l_prime / l) * _C, 4), "mistake": "That isn't how the length contraction formula rearranges for v — use v = c√(1−(l′/l)²).", "working": working},
    ]
    options_data = _dedup(options_data, v)
    scaffold = [
        {"question": "What is l′/l?", "answer": lor},
        {"question": "What is the speed v of the spacecraft, in m/s?", "answer": v},
    ]
    return make_question(question, v, options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level, scaffold=scaffold)


# ── Simple (Newtonian) relative velocity ─────────────────────────────────────

# (label A, label B, location phrase)
_PARALLEL_CONTEXTS = [
    ("Train A", "Train B", "on the same straight railway line"),
    ("Car A", "Car B", "on a straight motorway"),
    ("Cyclist A", "Cyclist B", "on a straight cycle path"),
    ("Speedboat A", "Speedboat B", "on a straight canal"),
    ("Runner A", "Runner B", "on a straight running track"),
]


def gen_relative_velocity_parallel(level="Higher"):
    """Velocity of A relative to B: same direction or opposite directions."""
    label_a, label_b, location = random.choice(_PARALLEL_CONTEXTS)
    v1 = random.randint(20, 50)
    v2 = random.randint(5, v1 - 3)
    same_direction = random.choice([True, False])

    if same_direction:
        answer = v1 - v2
        question = (
            f"{label_a} travels at {v1} m/s relative to the ground. {label_b} travels at {v2} m/s "
            f"relative to the ground, {location}, in the same direction as {label_a}. "
            f"Calculate the velocity of {label_a} relative to {label_b}."
        )
        working = [
            {"type": "text",  "content": f"{label_a} and {label_b} move the same way, so subtract the speeds:"},
            {"type": "latex", "content": rf"v = {v1} - {v2} = {answer}\ \mathrm{{m/s}}"},
        ]
        wrong_op = v1 + v2
        wrong_mistake = f"Since {label_a} and {label_b} travel in the same direction, subtract the speeds, don't add them."
    else:
        answer = v1 + v2
        question = (
            f"{label_a} travels at {v1} m/s relative to the ground. {label_b} travels at {v2} m/s "
            f"relative to the ground, {location}, in the opposite direction to {label_a}. "
            f"Calculate the velocity of {label_a} relative to {label_b}."
        )
        working = [
            {"type": "text",  "content": f"{label_a} and {label_b} move towards each other, so add the speeds:"},
            {"type": "latex", "content": rf"v = {v1} + {v2} = {answer}\ \mathrm{{m/s}}"},
        ]
        wrong_op = v1 - v2
        wrong_mistake = f"Since {label_a} and {label_b} travel in opposite directions, add the speeds, don't subtract them."

    options_data = [
        {"value": float(answer), "mistake": None, "working": working},
        {"value": float(wrong_op), "mistake": wrong_mistake, "working": working},
        {"value": float(v1), "mistake": f"This ignores {label_b}'s motion entirely — you must combine both speeds.", "working": working},
    ]
    options_data = _dedup(options_data, answer)
    return make_question(question, float(answer), options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level)


# (vehicle label, medium label, flow label, ground-frame label)
_PERP_CONTEXTS = [
    ("boat", "the water", "river current", "the riverbank",
     "A boat's engine gives it a velocity of {v1} m/s relative to {medium}, directed straight "
     "across a river. The {flow} flows at {v2} m/s relative to {ground}, at right angles to the "
     "boat's heading. Calculate the velocity of the boat relative to {ground}."),
    ("aircraft", "the air", "crosswind", "the ground",
     "An aircraft flies at {v1} m/s relative to {medium}, heading due north. A {flow} blows at "
     "{v2} m/s relative to {ground}, from due west — at right angles to the aircraft's heading. "
     "Calculate the velocity of the aircraft relative to {ground}."),
    ("swimmer", "the water", "current", "the riverbank",
     "A swimmer swims at {v1} m/s relative to {medium}, aiming straight across a river. The "
     "{flow} flows at {v2} m/s relative to {ground}, at right angles to the swimmer's heading. "
     "Calculate the velocity of the swimmer relative to {ground}."),
]

# Pythagorean triples (leg_a, leg_b, hypotenuse) for clean right-angle answers
_PERP_TRIPLES = [(3, 4, 5), (6, 8, 10), (9, 12, 15), (5, 12, 13), (8, 15, 17)]


def gen_relative_velocity_perpendicular(level="Higher"):
    """Velocity of A relative to B: A and B's velocities are at right angles."""
    vehicle, medium, flow, ground, template = random.choice(_PERP_CONTEXTS)
    a, b, hyp = random.choice(_PERP_TRIPLES)
    v1, v2 = a, b
    answer = hyp

    question = template.format(v1=v1, v2=v2, medium=medium, flow=flow, ground=ground)
    working = [
        {"type": "text",  "content": "The two velocities are at right angles, so combine them with Pythagoras:"},
        {"type": "latex", "content": r"v = \sqrt{v_1^2 + v_2^2}"},
        {"type": "latex", "content": rf"v = \sqrt{{{v1}^2 + {v2}^2}}"},
        {"type": "latex", "content": rf"v = {answer}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": float(answer), "mistake": None, "working": working},
        {"value": float(v1 + v2), "mistake": "The two velocities are at right angles, not parallel — you can't just add them, use Pythagoras instead.", "working": working},
        {"value": float(abs(v1 - v2)), "mistake": "The two velocities are at right angles, not opposite — you can't just subtract them, use Pythagoras instead.", "working": working},
        {"value": float(v1 ** 2 + v2 ** 2), "mistake": "You found v² but forgot to take the square root at the end.", "working": working},
    ]
    options_data = _dedup(options_data, answer)
    return make_question(question, float(answer), options_data, "m/s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level)


# ── Einstein's postulates and inertial frames of reference ──────────────────

def gen_inertial_frame(level="Higher"):
    question_text = "Which of the following best describes an inertial frame of reference?"
    correct = "A frame of reference that is not accelerating — it is either at rest or moving at a constant velocity."
    working = [
        {"type": "text", "content": "An inertial frame is one in which Newton's first law holds: it is at rest or moving with constant velocity, i.e. it is not accelerating."},
    ]
    distractors = [
        {"value": "A frame of reference that is fixed to the surface of the Earth.",
         "mistake": "An inertial frame doesn't have to be on Earth — any frame moving at constant velocity (or at rest) counts, including a spacecraft in deep space.",
         "working": working},
        {"value": "A frame of reference that is accelerating uniformly.",
         "mistake": "An accelerating frame is a non-inertial frame — an inertial frame must have zero acceleration.",
         "working": working},
        {"value": "A frame of reference in which the speed of light is not constant.",
         "mistake": "The speed of light is constant in every inertial frame, not just some of them — that's Einstein's second postulate.",
         "working": working},
    ]
    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)
    part = PhysicsQuestion(
        question_text=question_text, correct_answer=correct, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        distractors=distractors, working=working,
        metadata={"type": "classification", "options": options}, notes=_NOTES,
    )
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        is_scenario=True, scenario_context="", parts=[part],
    )


def gen_postulate_light_speed(level="Higher"):
    v_frac, v_str, _ = random.choice(_VELOCITIES)
    ship = _ship()
    context = (
        f"{ship} travels at a constant speed of {v_str} relative to a stationary observer on "
        f"Earth. The spacecraft emits a beam of light in its direction of travel."
    )
    question_text = "What speed does the stationary observer on Earth measure for the emitted light beam?"
    correct = "3.00 × 10⁸ m/s (c) — the same as it would be from a stationary source."
    working = [
        {"type": "text", "content": (
            "Einstein's second postulate states that the speed of light in a vacuum is the "
            "same for all observers in all inertial frames of reference, regardless of the "
            "motion of the source. The spacecraft's speed does not add to the speed of the "
            "light it emits."
        )},
    ]
    distractors = [
        {"value": f"3.00 × 10⁸ m/s + {v_str.replace('c','')} × (3.00 × 10⁸ m/s), added like an everyday velocity.",
         "mistake": "Velocities don't add classically at relativistic speeds — the speed of light is invariant for every observer (Einstein's second postulate).",
         "working": working},
        {"value": "Less than 3.00 × 10⁸ m/s, since the source is moving towards the observer.",
         "mistake": "The measured speed of light doesn't depend on the motion of the source — it is always c for every inertial observer.",
         "working": working},
        {"value": "It cannot be determined without knowing the observer's own speed.",
         "mistake": "The observer here is stationary, and even for a moving observer, the speed of light measured is still always c.",
         "working": working},
    ]
    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)
    part = PhysicsQuestion(
        question_text=question_text, correct_answer=correct, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        distractors=distractors, working=working,
        metadata={"type": "classification", "options": options}, notes=_NOTES,
    )
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        is_scenario=True, scenario_context=context, parts=[part],
    )


def gen_light_speed_moving_observer(level="Higher"):
    v_frac, v_str, _ = random.choice(_VELOCITIES)
    context = (
        f"A source of light is stationary on Earth. An observer travels towards the source at "
        f"a constant speed of {v_str}."
    )
    question_text = "What speed does the moving observer measure for the light from the source?"
    correct = "3.00 × 10⁸ m/s (c) — the same as a stationary observer would measure."
    working = [
        {"type": "text", "content": (
            "Einstein's second postulate states that the speed of light in a vacuum is measured "
            "as c by every observer in every inertial frame, regardless of the motion of the "
            "observer or the source. The observer's own speed does not add to or subtract from "
            "the measured speed of light."
        )},
    ]
    distractors = [
        {"value": f"3.00 × 10⁸ m/s + {v_str.replace('c','')} × (3.00 × 10⁸ m/s), since the observer moves towards the light.",
         "mistake": "Speeds don't add classically here — the speed of light is invariant, no matter how the observer is moving (Einstein's second postulate).",
         "working": working},
        {"value": f"3.00 × 10⁸ m/s − {v_str.replace('c','')} × (3.00 × 10⁸ m/s), since the observer moves towards the light.",
         "mistake": "Speeds don't subtract classically here either — every inertial observer measures the same speed of light, c.",
         "working": working},
        {"value": "It depends on how fast the observer is travelling.",
         "mistake": "The measured speed of light is always c, for any inertial observer at any speed less than c — that's what makes it invariant.",
         "working": working},
    ]
    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)
    part = PhysicsQuestion(
        question_text=question_text, correct_answer=correct, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        distractors=distractors, working=working,
        metadata={"type": "classification", "options": options}, notes=_NOTES,
    )
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        is_scenario=True, scenario_context=context, parts=[part],
    )


def gen_einstein_postulates(level="Higher"):
    question_text = "Which of the following correctly states Einstein's two postulates of special relativity?"
    correct = (
        "1) The laws of physics are the same in all inertial frames of reference. "
        "2) The speed of light in a vacuum is the same for all observers, regardless of the "
        "motion of the source or the observer."
    )
    working = [
        {"type": "text", "content": (
            "Einstein's first postulate says physics works the same way in every inertial frame — "
            "no experiment can tell you whether you're 'really' moving or at rest. His second "
            "postulate says the speed of light in a vacuum, c, is measured as the same value by "
            "every observer, however they or the source are moving."
        )},
    ]
    distractors = [
        {"value": (
            "1) The laws of physics are the same in all frames of reference, including "
            "accelerating ones. 2) The speed of light in a vacuum is the same for all observers."
         ),
         "mistake": "The first postulate applies to inertial (non-accelerating) frames only — accelerating frames are not covered by special relativity.",
         "working": working},
        {"value": (
            "1) The laws of physics are the same in all inertial frames of reference. "
            "2) The speed of light in a vacuum depends on the speed of the source."
         ),
         "mistake": "The second postulate is the opposite of this — the speed of light does NOT depend on the motion of the source (or observer).",
         "working": working},
        {"value": (
            "1) Time and length are absolute and the same for every observer. "
            "2) The speed of light adds to the velocity of the observer."
         ),
         "mistake": "Neither part of this is one of Einstein's postulates — time and length are not absolute in special relativity, and speeds do not add to c.",
         "working": working},
    ]
    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)
    part = PhysicsQuestion(
        question_text=question_text, correct_answer=correct, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        distractors=distractors, working=working,
        metadata={"type": "classification", "options": options}, notes=_NOTES,
    )
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        is_scenario=True, scenario_context="", parts=[part],
    )


# ── "Who is right?" conceptual reasoning ─────────────────────────────────────

def gen_who_is_right_clocks(level="Higher"):
    ship = _ship()
    context = (
        f"{ship} travels at a constant, high speed relative to an observer on Earth. Both the "
        f"astronaut on board and the observer on Earth carry identical clocks.\n\n"
        f"The astronaut says: \"My clock is running normally — it's the Earth observer's clock "
        f"that is running slow.\"\n\n"
        f"The Earth observer says: \"My clock is running normally — it's the astronaut's clock "
        f"that is running slow.\""
    )
    question_text = "Who is correct?"
    correct = (
        "Both are correct — each observer sees their own clock running normally and measures "
        "the other observer's moving clock to be running slow. There is no absolute frame that "
        "decides whose clock is 'really' slow."
    )
    working = [
        {"type": "text", "content": (
            "Time dilation is symmetric between two inertial observers moving relative to each "
            "other. Each regards themselves as at rest and the other as moving, so each measures "
            "the other's clock to run slow relative to their own. Since neither frame is "
            "preferred (Einstein's first postulate), both viewpoints are equally valid."
        )},
    ]
    distractors = [
        {"value": "Only the astronaut is correct, because the spacecraft is the one that is actually moving.",
         "mistake": "There is no absolute motion in special relativity — you could equally say the astronaut is at rest and the Earth is moving past them. Velocity is always relative.",
         "working": working},
        {"value": "Only the Earth observer is correct, because Earth is a fixed, stationary frame.",
         "mistake": "Earth is not a special 'stationary' frame — it is simply another inertial frame, moving relative to the spacecraft just as much as the spacecraft moves relative to it.",
         "working": working},
        {"value": "Neither is correct — both clocks must actually be running at the same rate.",
         "mistake": "Time dilation is a real, measurable effect for a moving clock, not just an appearance — each observer genuinely measures the other's clock to run slow.",
         "working": working},
    ]
    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)
    part = PhysicsQuestion(
        question_text=question_text, correct_answer=correct, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        distractors=distractors, working=working,
        metadata={"type": "classification", "options": options}, notes=_NOTES,
    )
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        is_scenario=True, scenario_context=context, parts=[part],
    )


def gen_who_is_right_muon(level="Higher"):
    context = (
        "A fast-moving muon is created high in the atmosphere and travels down towards a "
        "detector on the ground before it decays.\n\n"
        "An observer on the ground says: \"The muon's internal 'decay clock' is time dilated "
        "because it's moving so fast, so it survives long enough to reach the ground.\"\n\n"
        "An observer travelling with the muon says: \"My decay clock is running normally — it's "
        "the distance through the atmosphere that is length contracted, so I don't have as far "
        "to travel before I decay.\""
    )
    question_text = "Who is correct?"
    correct = (
        "Both are correct — time dilation (in the ground observer's frame) and length "
        "contraction (in the muon's frame) are two different, equally valid explanations for "
        "the same result: more muons reach the ground than non-relativistic physics predicts."
    )
    working = [
        {"type": "text", "content": (
            "Time dilation and length contraction are two sides of the same relativistic effect, "
            "seen from different inertial frames. In the ground frame, the muon's clock runs slow, "
            "so it lives long enough to complete the journey. In the muon's own frame, its "
            "lifetime is normal, but the distance to the ground is contracted, so less distance "
            "needs to be covered. Both frames agree on the observable outcome — the muon reaches "
            "the ground."
        )},
    ]
    distractors = [
        {"value": "Only the ground observer is correct — length contraction isn't a real effect, only time dilation is.",
         "mistake": "Length contraction is just as real as time dilation — they are two consequences of the same Lorentz transformation, and both frames give a self-consistent explanation.",
         "working": working},
        {"value": "Only the muon's observer is correct — time dilation isn't a real effect, only length contraction is.",
         "mistake": "Time dilation is just as real as length contraction — in the ground frame it is the correct explanation for why the muon survives the journey.",
         "working": working},
        {"value": "Neither is correct — the muon should decay before reaching the ground in both frames.",
         "mistake": "This is exactly the (wrong) non-relativistic prediction. Experimentally, more muons reach the ground than that prediction allows, which relativity explains via time dilation or length contraction depending on your frame.",
         "working": working},
    ]
    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)
    part = PhysicsQuestion(
        question_text=question_text, correct_answer=correct, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        distractors=distractors, working=working,
        metadata={"type": "classification", "options": options}, notes=_NOTES,
    )
    return PhysicsQuestion(
        question_text="", correct_answer=0, unit="",
        topic="Our Dynamic Universe", question_type="Special Relativity", level=level,
        is_scenario=True, scenario_context=context, parts=[part],
    )


# ── helpers ───────────────────────────────────────────────────────────────────

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


_ALL_GENS = [
    gen_relative_velocity_parallel,
    gen_relative_velocity_perpendicular,
    gen_inertial_frame,
    gen_postulate_light_speed,
    gen_light_speed_moving_observer,
    gen_einstein_postulates,
    gen_who_is_right_clocks,
    gen_who_is_right_muon,
    gen_t_prime,
    gen_t_proper,
    gen_v_from_time_dilation,
    gen_l_prime,
    gen_l_proper,
    gen_v_from_length_contraction,
]


def generate_special_relativity(level="Higher"):
    q = random.choice(_ALL_GENS)(level=level)
    q.metadata["widget_html"] = _WIDGET_HTML
    return q
