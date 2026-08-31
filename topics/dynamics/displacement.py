import random
import math
from utils.make_question import make_question
from utils.notes import NOTES


def _pick():
    north_mag = random.randint(3, 20)
    east_mag  = random.randint(3, 20)
    north = north_mag if random.choice([True, False]) else -north_mag
    east  = east_mag  if random.choice([True, False]) else -east_mag
    return east, north


def _n_dir(north):
    return "north" if north > 0 else "south"


def _e_dir(east):
    return "east" if east > 0 else "west"


def _two_leg_phrase(east, north):
    legs = [f"{abs(north)} km {_n_dir(north)}", f"{abs(east)} km {_e_dir(east)}"]
    random.shuffle(legs)
    return f"{legs[0]} and {legs[1]}"


def gen_find_magnitude(level="N5"):
    east, north = _pick()
    correct = round(math.sqrt(east ** 2 + north ** 2), 2)

    working = [
        {"type": "text",  "content": "Use Pythagoras' theorem to find the resultant:"},
        {"type": "latex", "content": r"R = \sqrt{x^2 + y^2}"},
        {"type": "latex", "content": rf"R = \sqrt{{{abs(east)}^2 + {abs(north)}^2}}"},
        {"type": "latex", "content": rf"R = {correct}\ \mathrm{{km}}"},
    ]
    question = (
        f"A boat travels {_two_leg_phrase(east, north)}.\n\n"
        f"Calculate the magnitude of the resultant displacement."
    )
    options_data = [
        {"value": float(correct),                "display": f"{correct} km",             "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(abs(east + north)),       "display": f"{abs(east + north)} km",   "summary": "Incorrect.", "mistake": "You added the two distances directly. Use Pythagoras' theorem: R = √(x² + y²).", "working": working},
        {"value": float(abs(east - north)),       "display": f"{abs(east - north)} km",   "summary": "Incorrect.", "mistake": "You subtracted the components. Use Pythagoras' theorem: R = √(x² + y²).", "working": working},
        {"value": round(east ** 2 + north ** 2, 2), "display": f"{round(east**2 + north**2, 2)} km", "summary": "Incorrect.", "mistake": "You forgot to square root the result. R = √(x² + y²), not x² + y².", "working": working},
    ]
    return make_question(question, float(correct), options_data, "km",
                         notes=NOTES["vectors"], topic="Dynamics", question_type="Vectors", level=level)


def gen_find_bearing(level="N5"):
    east, north = _pick()
    angle = round(math.degrees(math.atan(abs(east) / abs(north))), 1)

    if north > 0 and east > 0:
        bearing = angle
    elif north > 0 and east < 0:
        bearing = 360 - angle
    elif north < 0 and east < 0:
        bearing = 180 + angle
    else:
        bearing = 180 - angle

    bearing = round(bearing, 0)
    bearing_display = f"{int(bearing):03d}"

    all_bearings = [angle, round(180 - angle, 0), round(180 + angle, 0), round(360 - angle, 0)]
    distractors = [d for d in all_bearings if d != bearing][:3]

    working = [
        {"type": "latex", "content": rf"\theta = \tan^{{-1}}\!\left(\frac{{{abs(east)}}}{{{abs(north)}}}\right) = {angle}°"},
        {"type": "text",  "content": "Apply the quadrant rule (bearing measured clockwise from North):"},
        {"type": "text",  "content": "NE quadrant: bearing = θ | NW: 360 − θ | SE: 180 − θ | SW: 180 + θ"},
        {"type": "latex", "content": rf"\text{{Bearing}} = {bearing_display}°"},
    ]
    question = (
        f"A boat travels {_two_leg_phrase(east, north)}.\n\n"
        f"Calculate the bearing of the resultant displacement."
    )

    quadrant_mistakes = {
        angle:              "θ is only the angle east of north. Apply the quadrant rule to get the full bearing.",
        round(180 - angle, 0): "Check the quadrant rule: SE quadrant uses 180 − θ, NW uses 360 − θ.",
        round(180 + angle, 0): "Check the quadrant rule: SW quadrant uses 180 + θ.",
        round(360 - angle, 0): "Check the quadrant rule: NW quadrant uses 360 − θ, SE uses 180 − θ.",
    }

    options_data = [
        {"value": float(bearing), "display": f"{bearing_display}°", "summary": "Correct!", "mistake": None, "working": working},
    ]
    for d in distractors:
        options_data.append({
            "value": float(d),
            "display": f"{int(d):03d}°",
            "summary": "Incorrect.",
            "mistake": quadrant_mistakes.get(d, "Check which quadrant the resultant points into and apply the correct rule."),
            "working": working,
        })

    return make_question(question, float(bearing), options_data, "°",
                         notes=NOTES["vectors"], topic="Dynamics", question_type="Vectors", level=level)


_ALL_GENS = [gen_find_magnitude, gen_find_bearing]


def generate_vectors(level="N5"):
    """Kept for Crash Higher, which still uses the plain (non-levelled) Vectors entry."""
    return random.choice(_ALL_GENS)(level=level)


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


def _signed_expr(values):
    s = str(values[0])
    for v in values[1:]:
        s += f" + ({v})" if v < 0 else f" + {v}"
    return s


_CONTEXTS_1D = ["A cyclist", "A hiker", "A jogger", "A delivery drone", "A train"]
_BEARING_CHOICES = [b for b in range(10, 360, 10) if b % 90 != 0]


def _l1_directions(bearing_chance=0.2):
    """Usually a cardinal N/S or E/W pair; occasionally a random bearing and its reverse."""
    if random.random() < bearing_chance:
        theta = random.choice(_BEARING_CHOICES)
        pos = f"on a bearing of {theta:03d}°"
        neg = f"on a bearing of {(theta + 180) % 360:03d}°"
        return pos, neg, True
    pos, neg = random.choice([("east", "west"), ("north", "south")])
    return pos, neg, False


def _random_1d_legs(n):
    """n signed leg magnitudes along a single line, with at least one reversal."""
    while True:
        mags = [random.randint(3, 40) for _ in range(n)]
        signs = [random.choice([1, -1]) for _ in range(n)]
        if len(set(signs)) == 2:
            return mags, signs


# ── Level 1 — 1D displacement ───────────────────────────────────────────────

def gen_l1_distance(level="N5"):
    pos, neg, _ = _l1_directions()
    n = random.choice([2, 3])
    mags, signs = _random_1d_legs(n)
    signed = [s * m for s, m in zip(signs, mags)]
    distance = sum(mags)
    displacement = sum(signed)

    journey = ", then ".join(f"{m} m {pos if s > 0 else neg}" for m, s in zip(mags, signs))
    obj = random.choice(_CONTEXTS_1D)
    question = f"{obj} travels {journey}.\n\nCalculate the total distance travelled."

    working = [
        {"type": "text", "content": "Distance is the total length of the path travelled — direction doesn't "
                                     "matter, so add up the magnitudes of every leg."},
        {"type": "latex", "content": rf"d = {' + '.join(str(m) for m in mags)} = {distance}\ \mathrm{{m}}"},
    ]

    options_data = [
        {"value": float(distance), "mistake": None, "working": working},
        {"value": float(abs(displacement)),
         "mistake": "That's the magnitude of the resultant displacement, not the distance. Distance adds "
                    "every leg regardless of direction.",
         "working": working},
        {"value": float(mags[0]),
         "mistake": "You only counted one leg of the journey — add the distance travelled on every leg.",
         "working": working},
        {"value": float(distance + mags[-1]),
         "mistake": "Check your addition — it looks like one leg has been counted twice.",
         "working": working},
    ]
    options_data = _dedup(options_data, distance)
    return make_question(question, float(distance), options_data, "m",
                         notes=NOTES["vectors"], topic="Dynamics", question_type="Distance and Displacement", level=level)


def gen_l1_displacement(level="N5"):
    pos, neg, is_bearing = _l1_directions()
    n = random.choice([2, 3])
    mags, signs = _random_1d_legs(n)
    signed = [s * m for s, m in zip(signs, mags)]
    displacement = sum(signed)
    if displacement == 0:
        mags[0] += 1
        signed = [s * m for s, m in zip(signs, mags)]
        displacement = sum(signed)
    distance = sum(mags)

    journey = ", then ".join(f"{m} m {pos if s > 0 else neg}" for m, s in zip(mags, signs))
    obj = random.choice(_CONTEXTS_1D)

    if is_bearing:
        correct = abs(displacement)
        question = f"{obj} travels {journey}.\n\nCalculate the magnitude of the resultant displacement."
        working = [
            {"type": "text", "content": f"Take {pos} as positive and {neg} as negative, then add the signed "
                                         f"displacements."},
            {"type": "latex", "content": rf"s = {_signed_expr(signed)} = {displacement}\ \mathrm{{m}}"},
            {"type": "text", "content": f"Magnitude = {correct} m."},
        ]
        options_data = [
            {"value": float(correct), "mistake": None, "working": working},
            {"value": float(distance),
             "mistake": "That's the total distance travelled, not the displacement. Opposite legs partly "
                        "cancel when finding displacement.",
             "working": working},
            {"value": float(mags[0]),
             "mistake": "You only used one leg of the journey — combine all of the signed displacements.",
             "working": working},
        ]
    else:
        correct = displacement
        question = (
            f"{obj} travels {journey}. Taking {pos} as positive, calculate the resultant displacement."
        )
        working = [
            {"type": "text", "content": f"Take {pos} as positive and {neg} as negative, then add the signed "
                                         f"displacements."},
            {"type": "latex", "content": rf"s = {_signed_expr(signed)} = {displacement}\ \mathrm{{m}}"},
        ]
        options_data = [
            {"value": float(correct), "mistake": None, "working": working},
            {"value": float(-correct),
             "mistake": f"The sign is the wrong way round — {pos} was taken as positive.",
             "working": working},
            {"value": float(distance),
             "mistake": "That's the total distance travelled, not the displacement. Opposite legs partly "
                        "cancel when finding displacement.",
             "working": working},
        ]
    options_data = _dedup(options_data, correct)
    return make_question(question, float(correct), options_data, "m",
                         notes=NOTES["vectors"], topic="Dynamics", question_type="Distance and Displacement", level=level)


def generate_displacement_l1(level="N5"):
    return random.choice([gen_l1_distance, gen_l1_displacement])(level=level)


# ── Level 2 — 2D, exactly two displacements (always cardinal) ──────────────

generate_displacement_l2 = generate_vectors


# ── Level 3 — 2D, more than two displacements (always cardinal) ────────────

def _pick_multi(n_segments):
    """n_segments signed legs each along N/S or E/W, guaranteeing a genuinely 2D resultant."""
    while True:
        segs = [
            (random.choice(["N", "E"]), random.choice([1, -1]) * random.randint(3, 20))
            for _ in range(n_segments)
        ]
        north = sum(m for a, m in segs if a == "N")
        east = sum(m for a, m in segs if a == "E")
        if north != 0 and east != 0:
            return segs, east, north


def _seg_phrase_km(axis, signed_mag):
    mag = abs(signed_mag)
    if axis == "N":
        word = "north" if signed_mag > 0 else "south"
    else:
        word = "east" if signed_mag > 0 else "west"
    return f"{mag} km {word}"


def _describe_multi(segs):
    phrases = [_seg_phrase_km(a, m) for a, m in segs]
    return ", then ".join(phrases[:-1]) + f", and finally {phrases[-1]}"


_CONTEXTS_MULTI = ["plane", "hiker", "delivery drone", "ship", "cyclist"]


def gen_l3_magnitude(level="N5"):
    n = random.choice([3, 4])
    segs, east, north = _pick_multi(n)
    correct = round(math.sqrt(east ** 2 + north ** 2), 2)
    journey = _describe_multi(segs)
    obj = random.choice(_CONTEXTS_MULTI)

    north_vals = [m for a, m in segs if a == "N"]
    east_vals = [m for a, m in segs if a == "E"]

    working = [
        {"type": "text", "content": "Resolve every leg onto the North/East axes (opposite directions are "
                                     "negative), then sum each axis separately."},
        {"type": "latex", "content": rf"\Sigma N = {_signed_expr(north_vals)} = {north}\ \mathrm{{km}}"},
        {"type": "latex", "content": rf"\Sigma E = {_signed_expr(east_vals)} = {east}\ \mathrm{{km}}"},
        {"type": "text", "content": "Use Pythagoras' theorem to combine the two perpendicular components:"},
        {"type": "latex", "content": r"R = \sqrt{(\Sigma N)^2 + (\Sigma E)^2}"},
        {"type": "latex", "content": rf"R = \sqrt{{{abs(north)}^2 + {abs(east)}^2}} = {correct}\ \mathrm{{km}}"},
    ]
    question = (
        f"A {obj} travels {journey}.\n\n"
        f"Calculate the magnitude of the resultant displacement from the starting point."
    )
    options_data = [
        {"value": float(correct), "mistake": None, "working": working},
        {"value": float(abs(east) + abs(north)),
         "mistake": "You added the North and East totals directly. Combine perpendicular components with "
                    "Pythagoras: R = √(ΣN² + ΣE²).",
         "working": working},
        {"value": round(north ** 2 + east ** 2, 2),
         "mistake": "You forgot to take the square root. R = √(ΣN² + ΣE²), not "
                    "ΣN² + ΣE².",
         "working": working},
        {"value": float(sum(abs(m) for _, m in segs)),
         "mistake": "That's the total distance travelled along the path, not the straight-line resultant "
                    "displacement.",
         "working": working},
    ]
    options_data = _dedup(options_data, correct)
    return make_question(question, float(correct), options_data, "km",
                         notes=NOTES["vectors"], topic="Dynamics", question_type="Distance and Displacement", level=level)


def gen_l3_bearing(level="N5"):
    n = random.choice([3, 4])
    segs, east, north = _pick_multi(n)
    angle = round(math.degrees(math.atan(abs(east) / abs(north))), 1)

    if north > 0 and east > 0:
        bearing = angle
    elif north > 0 and east < 0:
        bearing = 360 - angle
    elif north < 0 and east < 0:
        bearing = 180 + angle
    else:
        bearing = 180 - angle

    bearing = round(bearing, 0)
    bearing_display = f"{int(bearing):03d}"

    all_bearings = [angle, round(180 - angle, 0), round(180 + angle, 0), round(360 - angle, 0)]
    distractor_bearings = [d for d in all_bearings if d != bearing][:3]

    journey = _describe_multi(segs)
    obj = random.choice(_CONTEXTS_MULTI)

    north_vals = [m for a, m in segs if a == "N"]
    east_vals = [m for a, m in segs if a == "E"]

    working = [
        {"type": "text", "content": "Resolve every leg onto the North/East axes (opposite directions are "
                                     "negative), then sum each axis separately."},
        {"type": "latex", "content": rf"\Sigma N = {_signed_expr(north_vals)} = {north}\ \mathrm{{km}}"},
        {"type": "latex", "content": rf"\Sigma E = {_signed_expr(east_vals)} = {east}\ \mathrm{{km}}"},
        {"type": "latex", "content": rf"\theta = \tan^{{-1}}\!\left(\frac{{{abs(east)}}}{{{abs(north)}}}\right) = {angle}°"},
        {"type": "text",  "content": "Apply the quadrant rule (bearing measured clockwise from North):"},
        {"type": "text",  "content": "NE quadrant: bearing = θ | NW: 360 − θ | SE: 180 − θ | SW: 180 + θ"},
        {"type": "latex", "content": rf"\text{{Bearing}} = {bearing_display}°"},
    ]
    question = (
        f"A {obj} travels {journey}.\n\n"
        f"Calculate the bearing of the resultant displacement from the starting point."
    )

    quadrant_mistakes = {
        angle:                 "θ is only the angle east/west of north. Apply the quadrant rule to get the full bearing.",
        round(180 - angle, 0): "Check the quadrant rule: SE quadrant uses 180 − θ, NW uses 360 − θ.",
        round(180 + angle, 0): "Check the quadrant rule: SW quadrant uses 180 + θ.",
        round(360 - angle, 0): "Check the quadrant rule: NW quadrant uses 360 − θ, SE uses 180 − θ.",
    }

    options_data = [{"value": float(bearing), "mistake": None, "working": working}]
    for d in distractor_bearings:
        options_data.append({
            "value": float(d),
            "mistake": quadrant_mistakes.get(d, "Check which quadrant the resultant points into and apply "
                                                 "the correct rule."),
            "working": working,
        })
    options_data = _dedup(options_data, bearing)
    return make_question(question, float(bearing), options_data, "°",
                         notes=NOTES["vectors"], topic="Dynamics", question_type="Distance and Displacement", level=level)


def generate_displacement_l3(level="N5"):
    return random.choice([gen_l3_magnitude, gen_l3_bearing])(level=level)


# ── Speed and velocity from a compound (two-leg) displacement ───────────────

_NOTES_VELOCITY = """
## Speed and Velocity

**Definitions:**
- Speed is a scalar: total distance travelled ÷ time taken. Direction doesn't matter.
- Velocity is a vector: the resultant displacement ÷ time taken. It has both a size
  and a direction.

$$\\text{speed} = \\frac{\\text{distance}}{\\text{time}} \\qquad \\text{velocity} = \\frac{\\text{displacement}}{\\text{time}}$$

For a journey made of more than one leg, the *distance* is the total length of the
path travelled (simple addition), but the *displacement* is the straight-line
distance from start to finish (found with Pythagoras' theorem for two
perpendicular legs).

**Worked Example:** A hiker walks 400 m north, then 300 m east, taking 50 s.
- Total distance = 400 + 300 = 700 m, so speed = 700 ÷ 50 = 14 m/s
- Resultant displacement = √(400² + 300²) = 500 m, so velocity = 500 ÷ 50 = 10 m/s

> **Common exam trap:** speed is always greater than (or equal to) the magnitude of
> velocity for the same journey, since the straight-line displacement can never be
> longer than the path actually walked.
"""

_SV_CONTEXTS = [
    ("cyclist", "rides"), ("hiker", "walks"), ("delivery drone", "flies"),
    ("tractor", "drives"), ("runner", "runs"), ("ferry", "sails"),
]


def gen_speed_velocity_from_displacement(level="N5"):
    ns_mag = random.choice(range(200, 1300, 100))
    ew_mag = random.choice(range(200, 1300, 100))
    north = ns_mag if random.choice([True, False]) else -ns_mag
    east = ew_mag if random.choice([True, False]) else -ew_mag
    t = random.choice([40, 50, 60, 70, 80, 90, 100, 110, 120])

    total_distance = ns_mag + ew_mag
    resultant = round(math.sqrt(ns_mag ** 2 + ew_mag ** 2), 1)
    speed = round(total_distance / t, 2)
    velocity = round(resultant / t, 2)

    ctx, verb = random.choice(_SV_CONTEXTS)
    phrase = _two_leg_phrase(east, north).replace(" km ", " m ")
    ask_speed = random.choice([True, False])

    question = (
        f"A {ctx} {verb} {phrase}. The journey takes {t} s.\n\n"
        f"Calculate the {'average speed' if ask_speed else 'magnitude of the average velocity'} "
        f"of the {ctx}."
    )

    working_common = [
        {"type": "text", "content": f"Total distance travelled = {ns_mag} + {ew_mag} = {total_distance} m"},
        {"type": "latex", "content": rf"\text{{Resultant displacement}} = \sqrt{{{ns_mag}^2 + {ew_mag}^2}} = {resultant}\ \mathrm{{m}}"},
    ]

    if ask_speed:
        working = working_common + [
            {"type": "latex", "content": r"\text{speed} = \frac{\text{distance}}{\text{time}}"},
            {"type": "latex", "content": rf"\text{{speed}} = \frac{{{total_distance}}}{{{t}}} = {speed}\ \mathrm{{m/s}}"},
        ]
        correct = speed
        options_data = [
            {"value": correct, "mistake": None, "working": working},
            {"value": velocity,
             "mistake": "That's the average velocity (using the resultant displacement). Speed uses the "
                        "total distance travelled along the path, not the straight-line displacement.",
             "working": working},
            {"value": round(max(ns_mag, ew_mag) / t, 2),
             "mistake": "You only used one leg of the journey. Speed uses the *total* distance travelled — "
                        "add both legs together first.",
             "working": working},
        ]
    else:
        working = working_common + [
            {"type": "latex", "content": r"\text{velocity} = \frac{\text{displacement}}{\text{time}}"},
            {"type": "latex", "content": rf"\text{{velocity}} = \frac{{{resultant}}}{{{t}}} = {velocity}\ \mathrm{{m/s}}"},
        ]
        correct = velocity
        options_data = [
            {"value": correct, "mistake": None, "working": working},
            {"value": speed,
             "mistake": "That's the average speed (using the total distance travelled). Velocity uses the "
                        "resultant displacement — combine the two legs with Pythagoras' theorem first.",
             "working": working},
            {"value": round(max(ns_mag, ew_mag) / t, 2),
             "mistake": "You only used one leg of the journey. Velocity uses the resultant displacement of "
                        "*both* legs — combine them with Pythagoras' theorem first.",
             "working": working},
        ]

    options_data = _dedup(options_data, correct)
    return make_question(question, float(correct), options_data, "m/s",
                         notes=_NOTES_VELOCITY, topic="Dynamics", question_type="Speed and Velocity", level=level)


# ── Relative velocity ─────────────────────────────────────────────────────────

_NOTES_RELVEL = """
## Relative Velocity

**Definition:** the velocity of one object relative to another is the velocity it appears
to have when observed from that other object.

- For objects moving **along the same line**, simply add or subtract the velocities,
  taking direction into account (velocities in opposite directions are opposite signs).
- For objects moving **at an angle to each other**, combine the two velocities using
  Pythagoras' theorem (and trigonometry for the direction), just as with any two
  perpendicular vectors.

**Worked Example (same line):** Train A travels at 25 m/s. Train B travels at 18 m/s in
the same direction. Velocity of A relative to B = 25 − 18 = 7 m/s (in the direction of travel).

**Worked Example (at an angle):** A ship travels at 12 m/s due east. A current flows at
5 m/s due north. Velocity relative to the seabed = √(12² + 5²) = 13 m/s, at
tan⁻¹(5 ÷ 12) = 22.6° north of east.

> **Common exam trap:** if the two objects move in *opposite* directions along the same
> line, their relative velocity is found by *adding* the speeds, not subtracting them.
"""

_RELVEL_1D_SAME = [
    ("lorry", "car", "overtaking"), ("cyclist", "runner", "overtaking"),
    ("tractor", "van", "overtaking"), ("ferry", "speedboat", "overtaking"),
]
_RELVEL_1D_OPPOSITE = [
    ("cyclist", "jogger"), ("rowing boat", "swimmer"), ("train", "cyclist on a path alongside the track"),
]
_RELVEL_2D = [
    ("ship", "current", "east", "north", "flows"),
    ("aircraft", "crosswind", "north", "east", "blows"),
    ("motorboat", "tidal current", "west", "south", "flows"),
]


def gen_relvel_1d(level="N5"):
    same_direction = random.choice([True, False])
    if same_direction:
        obj1, obj2, verb = random.choice(_RELVEL_1D_SAME)
        v1 = random.randint(18, 30)
        v2 = random.randint(v1 + 4, v1 + 14)
        answer = v2 - v1
        question = (
            f"A {obj1} travels at {v1} m/s. A {obj2} travels at {v2} m/s in the same "
            f"direction, {verb} the {obj1}. Calculate the velocity of the {obj2} relative "
            f"to a passenger on the {obj1}."
        )
        working = [
            {"type": "text", "content": "Both travel the same way, so subtract the speeds:"},
            {"type": "latex", "content": rf"v = {v2} - {v1} = {answer}\ \mathrm{{m/s}}"},
        ]
        wrong_op = v1 + v2
        wrong_mistake = f"Since both the {obj1} and {obj2} travel in the same direction, subtract the speeds, don't add them."
    else:
        obj1, obj2 = random.choice(_RELVEL_1D_OPPOSITE)
        v1 = random.randint(4, 10)
        v2 = random.randint(1, 6)
        answer = v1 + v2
        question = (
            f"A {obj1} travels at {v1} m/s. A {obj2} travels towards the {obj1} at {v2} m/s. "
            f"Calculate the velocity of the {obj1} relative to the {obj2}."
        )
        working = [
            {"type": "text", "content": f"Taking the {obj1}'s direction as positive, the {obj2}'s velocity is −{v2} m/s:"},
            {"type": "latex", "content": rf"v = {v1} - (-{v2}) = {v1} + {v2} = {answer}\ \mathrm{{m/s}}"},
        ]
        wrong_op = v1 - v2
        wrong_mistake = f"Since the {obj1} and {obj2} move towards each other (opposite directions), add the speeds, don't subtract them."

    options_data = [
        {"value": float(answer), "mistake": None, "working": working},
        {"value": float(wrong_op), "mistake": wrong_mistake, "working": working},
    ]
    options_data = _dedup(options_data, answer)
    return make_question(question, float(answer), options_data, "m/s",
                         notes=_NOTES_RELVEL, topic="Dynamics", question_type="Speed and Velocity", level=level)


def gen_relvel_2d(level="N5"):
    obj1, obj2, dir1, dir2, verb = random.choice(_RELVEL_2D)
    v1 = random.choice([8, 10, 12, 15, 20, 25])
    v2 = random.choice([3, 4, 5, 6, 8])
    resultant = round(math.sqrt(v1 ** 2 + v2 ** 2), 1)
    a1 = "An" if obj1[0] in "aeiou" else "A"
    a2 = "A" if obj2[0] not in "aeiou" else "An"

    question = (
        f"{a1} {obj1} travels at {v1} m/s due {dir1}. {a2} {obj2} {verb} at {v2} m/s due {dir2}. "
        f"Calculate the magnitude of the {obj1}'s resultant velocity relative to the ground."
    )
    working = [
        {"type": "text", "content": "The two velocities are perpendicular, so combine with Pythagoras' theorem:"},
        {"type": "latex", "content": rf"v = \sqrt{{{v1}^2 + {v2}^2}} = {resultant}\ \mathrm{{m/s}}"},
    ]
    options_data = [
        {"value": resultant, "mistake": None, "working": working},
        {"value": float(v1 + v2),
         "mistake": "You added the two velocities directly. Since they're perpendicular, combine them with "
                    "Pythagoras' theorem instead: v = √(v₁² + v₂²).",
         "working": working},
        {"value": float(v1),
         "mistake": f"That's just the {obj1}'s own velocity — you need to combine it with the {obj2}'s velocity too.",
         "working": working},
    ]
    options_data = _dedup(options_data, resultant)
    return make_question(question, resultant, options_data, "m/s",
                         notes=_NOTES_RELVEL, topic="Dynamics", question_type="Speed and Velocity", level=level)


def generate_relative_velocity(level="N5"):
    return random.choice([gen_relvel_1d, gen_relvel_2d])(level=level)
