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
        f"A boat travels {abs(north)} km {_n_dir(north)} and {abs(east)} km {_e_dir(east)}.\n\n"
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
        f"A boat travels {abs(north)} km {_n_dir(north)} and {abs(east)} km {_e_dir(east)}.\n\n"
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
    return random.choice(_ALL_GENS)(level=level)
