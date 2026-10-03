"""N5 Space — exam-style questions that cut across space exploration and cosmology, like SQA paper questions.

Recognised wrong answers follow the N5 marking instructions and course reports: the weight on Earth
multiplied straight by another planet's g, the thrust used as the unbalanced force, the echo/signal
distance not converted from km, ‘no gravity in space’, geostationary satellites ‘not moving’, a
conversion missed in light-years → metres, ‘closer to the stars’ as a telescope advantage, and an
element counted as present when only some of its lines match.
"""
from topics.exam_style.base import Exam, fmt, ltx, pick, sig

UNIT = "Space"
C = 3.0e8
YEAR = 365.25 * 24 * 60 * 60

NOTES = {
    "Space Exploration": r"""## Space exploration — exam technique

$W = mg$ &nbsp; $F = ma$ &nbsp; $d = vt$ — g: Earth 9.8, Mars 3.7, Moon 1.6 N/kg.

- Mass never changes: find m from the Earth weight first.
- Unbalanced force at launch = thrust − weight. As fuel is used, the acceleration **increases**.
- Geostationary: 24 h, 36 000 km. Higher orbit → longer period. Astronauts in orbit are in **free fall**.
- Slingshot → increase in speed. Ion drive → small force for a long time.
""",
    "Cosmology": r"""## Cosmology — exam technique

$d = vt$ with t = (light-years) × 365.25 × 24 × 60 × 60 s.

- A light-year is a **distance**. The Universe is about **13.8 billion** years old (Big Bang).
- Space telescopes: no atmospheric absorption/distortion — not "closer".
- An element is present only if **all** its lines appear in the star's spectrum.
""",
}


def _ex(level):
    return Exam(UNIT, level, NOTES)


# ════════════════ Mars mission: weight → launch acceleration → slingshot → signal time ════════════════

def mars_mission(level="N5"):
    ex = _ex(level)
    We = pick(686, 735, 784)
    m = We / 9.8
    ex.on("Space Exploration").num(f"An astronaut weighs {We} N on Earth. Calculate her weight on Mars.", m * 3.7, "N",
        wrong=[(We * 3.7, "Find the mass first: m = W ÷ 9.8."), (m, "That's her mass — now W = mg."), (We, "Weight depends on g.")],
        working=[rf"m = \frac{{{We}}}{{9.8}} = {fmt(m)}\ \text{{kg}}", rf"W = mg = {fmt(m)} \times 3.7 = {fmt(m * 3.7)}\ \text{{N}}"],
        scaffold=[("Mass of the astronaut (kg)", m, "kg")])
    M, F = pick((1.3e6, 1.2e7), (1.0e6, 9.0e6), (8.0e5, 7.0e6))
    W = M * 3.7
    a = (F - W) / M
    ex.on("Space Exploration").num(f"For the return journey, the spaceship (mass {fmt(M)} kg) produces an upward thrust of {fmt(F)} N on Mars. Calculate its acceleration at launch.",
        a, "m/s²", wrong=[(F / M, "Use the UNBALANCED force: thrust − weight (course report 2022)."), ((F - M * 9.8) / M, "Use g on Mars (3.7 N/kg).")],
        working=[rf"W = mg = {ltx(M)} \times 3.7 = {ltx(W)}\ \text{{N}}", rf"F = {ltx(F)} - {ltx(W)} = {ltx(F - W)}\ \text{{N}}", rf"a = \frac{{F}}{{m}} = {fmt(a)}\ \text{{m/s}}^2"],
        scaffold=[("Weight on Mars (N)", W, "N"), ("Unbalanced force (N)", F - W, "N")])
    ex.on("Space Exploration").choice("As the spaceship climbs and burns fuel, the thrust stays constant. What happens to its acceleration?",
        "It increases — its mass decreases, so its weight falls and the unbalanced force acts on a smaller mass.",
        [("It stays the same because the thrust is constant.", "Must justify with the decreasing mass (course report 2024)."),
         ("It decreases because there is less fuel.", "Less mass → greater acceleration."), ("It becomes zero once it leaves the surface.", "There is still an unbalanced force.")])
    d = pick(5.5e10, 7.8e10, 2.25e11)
    ex.on("Cosmology").num(f"Mars is {fmt(d)} m from Earth. Calculate the time for a radio message to reach Mission Control.", d / C, "s",
        wrong=[(d / 340, "Radio waves travel at the speed of light."), (d * C, "t = d ÷ v.")],
        working=[r"d = vt", rf"t = \frac{{{ltx(d)}}}{{3.0\times10^8}} = {fmt(d / C)}\ \text{{s}}"])
    ex.on("Space Exploration").choice("On the way, the spacecraft passed close to the Moon. How did this shorten the journey?",
        "The Moon's gravity gave it a slingshot, increasing its speed.",
        [("The Moon's gravity slowed it down.", "The slingshot increases speed (course report 2025)."), ("It refuelled at the Moon.", "No."),
         ("The Moon blocked radiation.", "Not related to journey time.")])
    return ex.build("A crewed spaceship travels to Mars and back. g on Earth = 9.8 N/kg; g on Mars = 3.7 N/kg.")


# ════════════════ Satellites: geostationary → period → weight in orbit → free fall ════════════════

def satellites(level="N5"):
    ex = _ex(level)
    ex.on("Space Exploration").choice("UKube-1 (825 km, 101 min), Kosmos (19 100 km, 676 min) and Astra (36 000 km, 24 h). Which transmits TV to a fixed dish, and why?",
        "Astra — it is geostationary (period 24 hours, altitude 36 000 km).",
        [("Astra — it doesn't move.", "It orbits; its period matches Earth's rotation (course report 2023)."),
         ("UKube-1 — it is closest to Earth.", "A low orbit passes overhead quickly."), ("Kosmos — it is in the middle.", "Only a 24-hour period keeps it over one point.")])
    ex.on("Space Exploration").choice("A new satellite will orbit at 1200 km. Predict its period.", "about 110 minutes",
        [("about 90 minutes", "Higher than 825 km → longer than 101 min."), ("about 700 minutes", "That would need a much higher orbit."),
         ("24 hours", "Only at 36 000 km.")])
    m, g = pick(3.5, 4.0, 12), pick(7.7, 7.5)
    ex.on("Space Exploration").num(f"At 825 km, g = {g:g} N/kg. UKube-1 has a mass of {m:g} kg. Calculate its weight in orbit.", m * g, "N",
        wrong=[(m * 9.8, "Use g at the orbit, as given."), (m / g, "W = m × g.")], working=[rf"W = mg = {m:g} \times {g:g} = {fmt(m * g)}\ \text{{N}}"])
    ex.on("Space Exploration").choice("An astronaut on the ISS floats. Why?", "She and the ISS are in free fall together around the Earth.",
        [("There is no gravity in space.", "g is about 8.7 N/kg there (course report 2018)."), ("The forces on her are balanced.", "Only weight acts (course report 2022)."),
         ("Her mass is zero in orbit.", "Mass never changes.")])
    d = 20200e3
    ex.on("Space Exploration").num("A GPS satellite is 20 200 km directly overhead. Calculate the time for its signal to reach a receiver.", d / C, "s",
        wrong=[(20200 / C, "Convert km to m (course report 2025)."), (d / 340, "Use the speed of light.")],
        working=[r"d = vt", rf"t = \frac{{20\,200\times10^3}}{{3.0\times10^8}} = {fmt(d / C)}\ \text{{s}}"])
    return ex.build("Satellites orbit the Earth at different altitudes for communications, navigation and science.")


# ════════════════ Space telescope: light-years → advantage → spectra → age ════════════════

def space_telescope(level="N5"):
    ex = _ex(level)
    n = pick(41, 97, 343, 860)
    d = n * C * YEAR
    ex.on("Cosmology").num(f"The James Webb Space Telescope observes a star {n} light-years away. Calculate this distance in metres.", d, "m",
        wrong=[(n * C * 365.25 * 24 * 60, "Include every conversion (× 60 × 60) — course report 2015."), (n * C, "Convert light-years to seconds of travel.")],
        working=[r"d = vt", rf"d = 3.0\times10^8 \times {n} \times 365.25 \times 24 \times 60 \times 60 = {ltx(d)}\ \text{{m}}"])
    ex.on("Cosmology").choice("State an advantage of a space-based telescope.", "It is above the atmosphere, so radiation is not absorbed or distorted.",
        [("It is closer to the stars.", "On astronomical scales it is no closer (course report 2024)."), ("It gives a clearer picture.", "Say why (course report 2024)."),
         ("It works only at night.", "It can be used at any time.")])
    ex.on("Cosmology").choice("The star's spectrum contains all of hydrogen's lines and two of helium's four lines. Which element(s) are definitely present?",
        "hydrogen only", [("hydrogen and helium", "ALL of helium's lines must appear."), ("helium only", "Hydrogen's lines are all there."),
                          ("neither", "All of hydrogen's lines match.")])
    ex.on("Cosmology").choice("The light we receive left the star long ago. What is a light-year?", "The distance light travels in one year.",
        [("The time light takes to reach Earth from the Sun.", "A light-year is a distance (2024 Paper 1)."), ("The age of a star.", "It is a distance."),
         ("The speed of light in a year.", "It is a distance.")])
    ex.on("Space Exploration").choice("Space telescopes are satellites. Which is another benefit of satellites?", "Weather forecasting and GPS navigation.",
        [("Reducing the Earth's gravity.", "Satellites don't affect g."), ("Producing electricity for homes.", "Not a satellite benefit in the course."),
         ("Making the Moon brighter.", "No.")])
    ex.on("Cosmology").choice("Telescopes help to study the origin of the Universe. Approximately how old is the Universe?", "13.8 billion years",
        [("14 million years", "Billion, not million."), ("4.6 billion years", "That's the solar system."), ("13.8 thousand years", "Far too young.")])
    return ex.build("Space-based telescopes such as the James Webb Space Telescope observe distant stars and galaxies. Speed of light = 3.0 × 10⁸ m/s.")


SCENARIOS = {
    "Mars Mission":     mars_mission,
    "Satellites":       satellites,
    "Space Telescope":  space_telescope,
}
