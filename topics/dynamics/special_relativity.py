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

**Worked Example:** A spacecraft moves at $v = 0.6c$. An observer on board measures a proper time of 10 s between two events. Calculate the dilated time measured by a stationary observer.
$$t' = \\frac{t}{\\sqrt{1 - \\frac{v^2}{c^2}}} = \\frac{10}{\\sqrt{1 - 0.6^2}} = \\frac{10}{0.8} = 12.5\\ \\mathrm{s}$$

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

# (v/c fraction, display string, √(1−v²/c²))
_VELOCITIES = [
    (0.6, "0.6c", 0.8),
    (0.8, "0.8c", 0.6),
]

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
    return make_question(question, t_prime, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level)


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
    return make_question(question, t, options_data, "s",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level)


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
    return make_question(question, l_prime, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level)


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
    return make_question(question, l, options_data, "m",
                         notes=_NOTES, topic="Our Dynamic Universe",
                         question_type="Special Relativity", level=level)


# ── Simple (Newtonian) relative velocity ─────────────────────────────────────

def gen_relative_velocity(level="Higher"):
    v1 = random.randint(20, 50)
    v2 = random.randint(5, v1 - 3)
    same_direction = random.choice([True, False])

    if same_direction:
        answer = v1 - v2
        question = (
            f"Train A travels at {v1} m/s relative to the ground. Train B travels at {v2} m/s "
            f"relative to the ground, in the same direction. Calculate the speed of Train A "
            f"relative to a passenger on Train B."
        )
        working = [
            {"type": "text",  "content": "Both trains move the same way, so subtract the speeds:"},
            {"type": "latex", "content": rf"v = {v1} - {v2} = {answer}\ \mathrm{{m/s}}"},
        ]
        wrong_op = v1 + v2
        wrong_mistake = "Since both trains travel in the same direction, subtract the speeds, don't add them."
    else:
        answer = v1 + v2
        question = (
            f"Train A travels at {v1} m/s relative to the ground. Train B travels at {v2} m/s "
            f"relative to the ground, in the opposite direction. Calculate the speed of Train A "
            f"relative to a passenger on Train B."
        )
        working = [
            {"type": "text",  "content": "The trains move towards each other, so add the speeds:"},
            {"type": "latex", "content": rf"v = {v1} + {v2} = {answer}\ \mathrm{{m/s}}"},
        ]
        wrong_op = v1 - v2
        wrong_mistake = "Since the trains travel in opposite directions, add the speeds, don't subtract them."

    options_data = [
        {"value": float(answer), "mistake": None, "working": working},
        {"value": float(wrong_op), "mistake": wrong_mistake, "working": working},
        {"value": float(v1), "mistake": "This ignores Train B's motion entirely — you must combine both speeds.", "working": working},
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
    gen_relative_velocity,
    gen_inertial_frame,
    gen_postulate_light_speed,
    gen_t_prime,
    gen_t_proper,
    gen_l_prime,
    gen_l_proper,
]


def generate_special_relativity(level="Higher"):
    q = random.choice(_ALL_GENS)(level=level)
    q.metadata["widget_html"] = _WIDGET_HTML
    return q
