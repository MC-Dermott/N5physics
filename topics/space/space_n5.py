"""N5 Space — question types from the N5phys Space Exploration and Cosmology worksheets.

Distractors are the errors named in the N5 course reports 2015–2025 and marking instructions: the
weight on Earth multiplied straight by another planet's g (mass not found first), the mass changing
on another planet, the thrust used in F = ma instead of the unbalanced force, ‘no gravity in space’,
geostationary satellites ‘not moving’, a higher orbit given a shorter period, a light-year treated as
a time, a conversion missed in light-years → metres, the age of the Universe given in millions, an
element counted as present when only some of its lines match, and non-physics space challenges.
"""
import math
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

TOPIC = "Space"
SPX = "Space Exploration"
COS = "Cosmology"
C = 3.0e8
YEAR = 365.25 * 24 * 60 * 60
LY = C * YEAR
G = {"Earth": 9.8, "Mars": 3.7, "the Moon": 1.6, "Jupiter": 23, "Venus": 8.9, "Mercury": 3.7, "Saturn": 9.0, "Neptune": 11}
_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

_NOTES = r"""
## N5 Space — exam technique

**Relationships (as on the relationships sheet):** $$W = mg \quad F = ma \quad d = vt$$

g (N/kg): Earth 9.8, Mars 3.7, Moon 1.6, Venus 8.9, Mercury 3.7, Jupiter 23, Saturn 9.0, Neptune 11.
Speed of light 3.0 × 10⁸ m/s; 1 year = 365.25 × 24 × 60 × 60 s; 1 light-year = 9.5 × 10¹⁵ m.

**Common errors (SQA course reports and marking instructions):**
- **Mass never changes** — find the mass from the Earth weight (m = W ÷ 9.8), then W = mg for the new place.
- Rockets: F in F = ma is the **unbalanced** force = thrust − weight. As fuel is used the mass falls, so the acceleration **increases**.
- Gravity acts in orbit — astronauts are in **free fall**. A satellite stays up because its **horizontal velocity** is large enough while its **weight** pulls it round.
- **Geostationary**: period 24 h, altitude 36 000 km. Higher orbit → **longer** period.
- A moon is a **natural** satellite; an exoplanet orbits a **star other than the Sun**.
- Slingshot → **increase in speed**; ion drive → small force for a **long time**; solar cells far from the Sun receive **less energy**.
- A **light-year is a distance**. Include every conversion: × 365.25 × 24 × 60 × 60.
- Universe: about **13.8 billion** years old, began with the Big Bang and is expanding.
- An element is in a star only if **all** of its lines appear in the star's spectrum.
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


# ════════════════ Space exploration ════════════════
# (object, mass range) — tied so masses suit the object
_OBJECTS = [("An astronaut", [62, 67, 72, 75, 80]), ("A robot rover", [24, 45, 180, 900]), ("A lander", [500, 750, 1200]),
            ("A space probe", [454, 720, 1100])]


def gen_sp_weight(level="N5"):
    name, ms = random.choice(_OBJECTS)
    m = random.choice(ms)
    place = random.choice([p for p in G if p != "Earth"])
    g = G[place]
    if random.random() < 0.5:
        W = m * g
        text = f"{name} has a mass of {m} kg. Calculate its weight on {place}."
        work = [_L(r"W = mg"), _L(rf"W = {m} \times {g:g} = {_ltx(W)}\ \mathrm{{N}}")]
        return _q(text, W, "N", _opts(work, W, (m * 9.8, f"Use g on {place} ({g:g} N/kg), not Earth's."), (m / g, "W = m × g.")), SPX, None, level)
    We = m * 9.8
    We_s = _sig(We, 2)
    mm = We_s / 9.8
    W = mm * g
    text = f"The weight of {name.lower()} on Earth is {_txt(We_s, 2)} N. Calculate its weight on {place}."
    work = [_L(r"W = mg"), _L(rf"m = \frac{{{_ltx(We_s, 2)}}}{{9.8}} = {_ltx(mm)}\ \mathrm{{kg}}"), _L(rf"W = {_ltx(mm)} \times {g:g} = {_ltx(W)}\ \mathrm{{N}}")]
    scaffold = [{"question": "What is the mass, in kg?", "answer": _sig(mm)}, {"question": f"What is the weight on {place}, in N?", "answer": _sig(W)}]
    return _q(text, W, "N", _opts(work, W, (We_s * g, "Find the MASS first: m = W ÷ 9.8."), (mm, "That's the mass — now W = mg."),
                                  (We_s, "Weight changes with g; mass doesn't.")), SPX, scaffold, level)


# (place, mass kg, thrust N) — thrust always exceeds weight
_LAUNCHES = [("Earth", 5.4e5, 7.6e6), ("Earth", 2.0e5, 3.4e6), ("Earth", 1000, 15000), ("Mars", 1.3e6, 1.2e7), ("the Moon", 1.5e4, 4.5e4)]


def gen_sp_rocket(level="N5"):
    place, m, F = random.choice(_LAUNCHES)
    g = G[place]
    W = m * g
    Fu = F - W
    a = Fu / m
    text = f"A rocket of mass {_txt(m)} kg on {place} produces an upward thrust of {_txt(F)} N. Calculate its acceleration at launch."
    work = [_L(rf"W = mg = {_ltx(m)} \times {g:g} = {_ltx(W)}\ \mathrm{{N}}"), _L(rf"F_{{un}} = {_ltx(F)} - {_ltx(W)} = {_ltx(Fu)}\ \mathrm{{N}}"),
            _L(r"F = ma"), _L(rf"a = \frac{{{_ltx(Fu)}}}{{{_ltx(m)}}} = {_ltx(a)}\ \mathrm{{m/s^2}}")]
    scaffold = [{"question": "What is the weight of the rocket, in N?", "answer": _sig(W)},
                {"question": "What is the unbalanced force, in N?", "answer": _sig(Fu)},
                {"question": "What is the acceleration, in m/s²?", "answer": _sig(a)}]
    wrong = [(F / m, "Use the UNBALANCED force (thrust − weight) — course reports 2022, 2025."), ((F + W) / m, "Weight acts downwards — subtract it.")]
    if place != "Earth" and F > m * 9.8:
        wrong.append(((F - m * 9.8) / m, f"Use g on {place} ({g:g} N/kg), not Earth's."))
    return _q(text, a, "m/s²", _opts(work, a, *wrong), SPX, scaffold, level)


def gen_sp_explain(level="N5"):
    kind = random.choice(["geo", "period", "orbit", "iss", "slingshot", "ion", "solar", "newton3", "fuel", "constant", "moon", "exoplanet", "asteroid", "challenge"])
    if kind == "geo":
        return _choice("Why does a geostationary TV satellite stay above the same point on Earth?", "Its period is 24 hours, the same as the Earth's rotation.",
                       [("It doesn't move.", "It orbits — its period matches the Earth's rotation (course report 2023)."),
                        ("It moves at the same speed as the Earth's surface.", "It goes much faster — but takes the same TIME (24 h)."),
                        ("There is no gravity at 36 000 km.", "Gravity keeps it in orbit.")], SPX, level)
    if kind == "period":
        return _choice("A satellite is moved to a higher orbit. What happens to its period?", "It increases.",
                       [("It decreases.", "Higher orbit → longer period."), ("It stays the same.", "Period depends on altitude."), ("It becomes 24 hours.", "Only at 36 000 km.")], SPX, level)
    if kind == "orbit":
        return _choice("How does the ISS stay in orbit?", "Its weight pulls it towards Earth, but its horizontal velocity is large enough that it keeps missing the surface.",
                       [("There is no gravity in space.", "Gravity acts — it provides the weight that curves the path."),
                        ("Its engines push it round constantly.", "No engine is needed — like a projectile."),
                        ("Its weight and the upward forces are balanced.", "The forces are NOT balanced — it is falling (course report 2022).")], SPX, level)
    if kind == "iss":
        return _choice("Why do astronauts on the ISS appear weightless?", "They and the station are in free fall around the Earth together.",
                       [("There is no gravity in space.", "Gravity acts — g is only slightly less (course report 2018)."),
                        ("The forces on them are balanced.", "Only weight acts — unbalanced (course report 2022)."),
                        ("They have no mass in space.", "Mass never changes.")], SPX, level)
    if kind == "slingshot":
        return _choice("How does passing close to a planet reduce a probe's journey time?", "The planet's gravity gives a slingshot that increases the probe's speed.",
                       [("The planet's gravity slows it down.", "The slingshot INCREASES its speed (course report 2025)."),
                        ("It refuels from the planet.", "No fuel is gained."), ("The planet shortens the distance.", "It's the speed that increases.")], SPX, level)
    if kind == "ion":
        return _choice("How can an ion drive's very small force give a large increase in speed?", "The small unbalanced force acts for a very long time.",
                       [("There is no friction in space.", "True, but doesn't answer — the force acts for a LONG time (course report 2025)."),
                        ("The spacecraft has a very small mass.", "Spacecraft are massive."), ("Ion drives produce a huge force.", "The force is small.")], SPX, level)
    if kind == "solar":
        return _choice("Why do a probe's solar cells produce less power far from the Sun?", "The cells receive less light energy from the Sun.",
                       [("Because the probe is further from the Sun.", "Must say LESS ENERGY is received (course report 2025)."),
                        ("There is no light in deep space.", "Some light still arrives."), ("The cells get too hot.", "It gets colder far from the Sun.")], SPX, level)
    if kind == "newton3":
        return _choice("A rocket's engines push exhaust gases downwards. What is the reaction to this force?", "The exhaust gases push the rocket upwards.",
                       [("The weight of the rocket.", "Newton's third law pairs act on the two different objects (course report 2024)."),
                        ("The ground pushes the gases upwards.", "The pair is rocket-on-gases / gases-on-rocket."),
                        ("Air resistance on the rocket.", "Not a reaction pair.")], SPX, level)
    if kind == "fuel":
        return _choice("A rocket's thrust stays constant as it climbs and uses fuel. What happens to its acceleration?",
                       "It increases, because its mass and weight decrease so the unbalanced force is larger for a smaller mass.",
                       [("It stays the same, because the thrust is constant.", "Must justify with the mass/weight change (course report 2024)."),
                        ("It decreases, because there is less fuel.", "Less mass → MORE acceleration."), ("It becomes zero.", "There is still an unbalanced force.")], SPX, level)
    if kind == "constant":
        return _choice("A probe far out in space switches off its engine. What happens?", "It keeps moving at a constant speed in a straight line.",
                       [("It slows down and stops.", "No friction — no unbalanced force (Newton's first law)."),
                        ("It keeps accelerating.", "No unbalanced force, so no acceleration."), ("It falls back to Earth.", "Far from Earth, no significant force.")], SPX, level)
    if kind == "moon":
        return _choice("What is a moon?", "A natural satellite of a planet.",
                       [("A satellite of a planet.", "Must be NATURAL (MI)."), ("A small rocky body orbiting the Sun.", "That's an asteroid."),
                        ("A planet without an atmosphere.", "Moons orbit planets.")], SPX, level)
    if kind == "exoplanet":
        return _choice("What is an exoplanet?", "A planet that orbits a star other than the Sun.",
                       [("A planet outside our galaxy.", "It is outside our SOLAR SYSTEM (course report 2024)."), ("A planet that no longer orbits a star.", "It orbits another star."),
                        ("A dwarf planet.", "Different term.")], SPX, level)
    if kind == "asteroid":
        return _choice("A small, rocky, irregular object orbits the Sun between Mars and Jupiter. It is", "an asteroid",
                       [("a dwarf planet", "Dwarf planets are round (course report 2023)."), ("a moon", "It orbits the Sun, not a planet."), ("an exoplanet", "It is in our solar system.")], SPX, level)
    return _choice("Which is a PHYSICS-related challenge for astronauts living on the Moon?", "Exposure to radiation.",
                   [("Lack of food.", "Not physics (course report 2024)."), ("There is no gravity on the Moon.", "g on the Moon is 1.6 N/kg."),
                    ("Floating away from the surface.", "Gravity holds them on the surface.")], SPX, level)


# ════════════════ Cosmology ════════════════
_STARS = [("Proxima Centauri", 4.2), ("Sirius", 8.6), ("Wolf 359", 7.8), ("Vega", 25), ("LHS 475 b's star", 41), ("a star in Orion", 97),
          ("Betelgeuse", 640), ("Rigel", 860)]


def gen_cs_lightyear(level="N5"):
    star, n = random.choice(_STARS)
    if random.random() < 0.6:
        d = n * LY
        text = f"{star} is {n:g} light-years from Earth. Calculate this distance in metres."
        work = [_L(r"d = vt"), _L(rf"d = 3.0\times10^8 \times {n:g} \times 365.25 \times 24 \times 60 \times 60"), _L(rf"d = {_ltx(d)}\ \mathrm{{m}}")]
        return _q(text, d, "m", _opts(work, d, (C * n * 365.25 * 24 * 60, "Include every conversion: × 60 for seconds is missing (course report 2015)."),
                                      (C * n, "Convert light-years to seconds of travel time first."), (n * YEAR, "Multiply by the speed of light.")), COS, None, level)
    d = _sig(n * LY, 2)
    text = f"{star} is {_txt(d, 2)} m from Earth. Calculate this distance in light-years."
    work = [_L(rf"1\ \text{{light-year}} = 3.0\times10^8 \times 365.25 \times 24 \times 60 \times 60 = {_ltx(LY)}\ \mathrm{{m}}"),
            _L(rf"\frac{{{_ltx(d, 2)}}}{{{_ltx(LY)}}} = {_ltx(d / LY)}\ \text{{light-years}}")]
    return _q(text, d / LY, "light-years", _opts(work, d / LY, (d / C, "That's the time in seconds — divide by the metres in one light-year."),
                                                 (d * LY, "Divide by 9.5 × 10¹⁵ m."), (d / (C * 365.25 * 24), "Include all the conversions.")), COS, None, level)


def gen_cs_light_time(level="N5"):
    what, d = random.choice([("the Sun to Mars (2.28 × 10¹¹ m)", 2.28e11), ("the Sun to Earth (1.50 × 10¹¹ m)", 1.50e11),
                             ("the Moon to Earth (3.84 × 10⁸ m)", 3.84e8), ("the Sun to Jupiter (7.78 × 10¹¹ m)", 7.78e11)])
    t = d / C
    text = f"Calculate the time taken for light to travel from {what}."
    work = [_L(r"d = vt"), _L(rf"{_ltx(d)} = 3.0\times10^8 \times t"), _L(rf"t = {_ltx(t)}\ \mathrm{{s}}")]
    return _q(text, t, "s", _opts(work, t, (d * C, "t = d ÷ v."), (d / 340, "Light travels at 3.0 × 10⁸ m/s.")), COS, None, level)


_ELEMENTS = {"hydrogen": "434, 486 and 656 nm", "helium": "447, 502, 588 and 668 nm", "calcium": "423, 527 and 616 nm", "sodium": "498, 569 and 610 nm"}


def gen_cs_explain(level="N5"):
    kind = random.choice(["ly", "age", "bigbang", "telescope", "spectrum", "lines", "same_time", "supernova", "elements"])
    if kind == "ly":
        return _choice("What is a light-year?", "The distance light travels in one year.",
                       [("The time for light to travel from the Sun to Earth.", "A light-year is a DISTANCE (2024 Paper 1)."),
                        ("The time light takes to travel one year.", "It is a distance."), ("The speed of light in one year.", "It is a distance.")], COS, level)
    if kind == "age":
        return _choice("What is the approximate age of the Universe?", "13.8 billion years",
                       [("14 million years", "Billion, not million (2016, Specimen Paper 1)."), ("4.6 billion years", "That's the age of the solar system."),
                        ("6000 years", "Far too young.")], COS, level)
    if kind == "bigbang":
        return _choice("Which describes the Big Bang theory?", "The Universe began from a very hot, dense point and has been expanding ever since.",
                       [("The Sun exploded to form the planets.", "It's about the origin of the whole Universe."),
                        ("The Universe has always existed unchanged.", "The theory says it had a beginning and is expanding."),
                        ("A star exploded as a supernova.", "That's a supernova, not the Big Bang.")], COS, level)
    if kind == "telescope":
        return _choice("What is an advantage of a space-based telescope?", "It is above the atmosphere, so the radiation is not absorbed or distorted.",
                       [("It is closer to the stars.", "On an astronomical scale it is no closer (course report 2024)."), ("It gives a clearer picture.", "Say WHY — no atmosphere (course report 2024)."),
                        ("It can see through planets.", "No.")], COS, level)
    if kind == "spectrum":
        return _choice("Which is a line spectrum?", "Separate bright lines of particular colours from a hot gas.",
                       [("All colours with no gaps, from a filament lamp.", "That's a continuous spectrum."), ("A rainbow.", "Continuous."),
                        ("Only infrared radiation.", "Spectra can be in any band.")], COS, level)
    if kind == "lines":
        return _choice("How are elements in a star identified from its spectrum?", "Each element has a unique pattern of lines; an element is present if all its lines appear in the star's spectrum.",
                       [("Each line in the star's spectrum is a different element.", "Each element produces several lines (course report 2022)."),
                        ("The brightest line shows the main element.", "Match the whole pattern."), ("By the colour of the star.", "Use the line pattern.")], COS, level)
    if kind == "same_time":
        return _choice("Radio waves and light leave a star at the same time. Which reaches Earth first?", "They arrive together — all EM waves travel at the same speed.",
                       [("The light — it has a higher frequency.", "Frequency doesn't affect speed in space."), ("The radio waves — they have a longer wavelength.", "Same speed."),
                        ("The light — radio waves are sound waves.", "Radio waves are electromagnetic.")], COS, level)
    if kind == "supernova":
        return _choice("Rigel is 860 light-years away. Why might it already have exploded without us knowing?", "Light from the explosion takes 860 years to reach Earth.",
                       [("Because it is 860 light-years away.", "Explain in terms of the TIME the light takes (MI)."),
                        ("Supernovae don't give out light.", "They give out huge amounts of radiation."), ("Telescopes can't see that far.", "We can see Rigel now.")], COS, level)
    present = random.sample(list(_ELEMENTS), 2)
    star_lines = sorted({int(x) for e in present for x in _ELEMENTS[e].replace("and", ",").replace("nm", "").split(",") if x.strip()})
    other = [e for e in _ELEMENTS if e not in present]
    right = " and ".join(sorted(present))
    wrong = [(" and ".join(sorted([present[0], other[0]])), f"Not all of {other[0]}'s lines are in the star's spectrum."),
             (" and ".join(sorted([present[1], other[1]])), f"Not all of {other[1]}'s lines are in the star's spectrum."),
             (" and ".join(sorted(other)), "Match ALL the lines of an element.")]
    lines = "; ".join(f"{e}: {w}" for e, w in _ELEMENTS.items())
    return _choice(f"A star's spectrum has lines at {', '.join(str(x) for x in star_lines)} nm. Element lines — {lines}. Which elements are present?",
                   right, wrong, COS, level)
