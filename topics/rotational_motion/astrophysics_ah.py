"""AH — General relativity and stellar physics."""
import math
import random

from topics.rotational_motion.common_ah import (
    AU, C, G, LIGHT_YEAR, M_SUN, R_SUN, SIGMA, L, T, calc, explain_set, fmt, ltx, pick_sig, sig, uni,
)

QT_GR = "General Relativity"
QT_S = "Stellar Physics"

NOTES_GR = r"""
## General relativity

$$r_{Schwarzschild} = \frac{2GM}{c^2}$$

- Special relativity deals with **inertial** (non-accelerating) frames; general relativity with
  **non-inertial** (accelerating) frames.
- **Equivalence principle:** an observer cannot distinguish between the effects of a uniform gravitational
  field and a constant acceleration. So clocks run more slowly lower in a gravitational field.
- **Spacetime** is a unified representation of three dimensions of space and one of time. Mass curves
  spacetime and gravity arises from this curvature. Light and freely moving objects follow **geodesics**.
- **World lines** (time on the vertical axis): vertical line = stationary; straight sloping line = constant
  velocity; curve = accelerating.
- The **Schwarzschild radius** is the distance from the centre (singularity) of a black hole to its event
  horizon. The escape velocity there equals c. To a distant observer, time appears frozen at the event horizon.
"""

NOTES_S = r"""
## Stellar physics

$$b = \frac{L}{4\pi d^2} \qquad \frac{P}{A} = \sigma T^4 \qquad L = 4\pi r^2\sigma T^4$$

- 1 AU = 1.5 × 10¹¹ m. A light-year is the distance light travels in one year (9.47 × 10¹⁵ m).
- T is in **kelvin**; r is the radius of the **star**, d is the distance from the star to the observer.
- Stars form when gravity overcomes thermal pressure in an interstellar cloud. In a main sequence star,
  outward thermal pressure balances the inward gravitational force while hydrogen fuses in the core.
- **Proton–proton chain:** ¹H + ¹H → ²H + e⁺ + ν;  ²H + ¹H → ³He + γ;  ³He + ³He → ⁴He + 2 ¹H.
- **H–R diagram:** luminosity against surface temperature (temperature **decreasing** to the right).
  Main sequence runs top left to bottom right; giants and supergiants top right; white dwarfs bottom left.
- A star's mass determines its lifetime and whether it ends as a white dwarf, neutron star or black hole.
  More massive stars have shorter lives.
"""


def gen_schwarzschild(level="AH"):
    n = pick_sig(3.0, 60.0)
    M = sig(n * M_SUN, 3)
    r = 2 * G * M / C**2
    if random.random() < 0.65:
        return calc(QT_GR, f"A black hole has a mass of {fmt(n)} solar masses. Calculate its Schwarzschild radius.",
                    r, "m",
                    [rf"M = {fmt(n)} \times 2.0 \times 10^{{30}} = {ltx(M)}\ \mathrm{{kg}}",
                     r"r_{Schwarzschild} = \frac{2GM}{c^2}", rf"r = {ltx(r)}\ \mathrm{{m}}"],
                    wrong=[(2 * G * M / C, "c must be squared."), (G * M / C**2, "You lost the factor of 2."),
                           (2 * G * n / C**2, "Convert solar masses to kilograms.")],
                    scaffold=[("What is the mass in kg?", M, "kg"), ("What is the Schwarzschild radius?", r, "m")],
                    notes=NOTES_GR)
    rg = sig(r, 3)
    ans = rg * C**2 / (2 * G)
    return calc(QT_GR, f"The Schwarzschild radius of a black hole is {fmt(rg)} m. Calculate its mass.", ans, "kg",
                [r"r_{Schwarzschild} = \frac{2GM}{c^2}", rf"M = \frac{{rc^2}}{{2G}} = {ltx(ans)}\ \mathrm{{kg}}"],
                wrong=[(rg * C**2 / G, "You lost the factor of 2."), (rg * C / (2 * G), "c must be squared.")],
                notes=NOTES_GR)


_EXPLAIN_GR = [
    ("A clock is at the nose of a spacecraft and another at the tail. The spacecraft accelerates forwards in deep "
     "space. Which clock runs more slowly, and why?",
     "The tail clock: by the equivalence principle it is like being lower in a gravitational field, where time runs more slowly.",
     [("The nose clock: it reaches high speed first.", "Both always have the same speed."),
      ("Neither: there is no gravity in deep space.", "Acceleration has the same effects as a gravitational field."),
      ("The nose clock: it is lower in the equivalent gravitational field.", "The equivalent field points towards the tail, so the tail is lower.")],
     "State the equivalence principle, then apply it."),
    ("A clock on a GPS satellite is compared with one on the Earth's surface. Considering only general relativity, "
     "which statement is correct?",
     "The satellite clock runs faster, because it is higher in the Earth's gravitational field.",
     [("The satellite clock runs slower, because it is higher in the field.", "Clocks run more slowly lower in a field."),
      ("The satellite clock runs slower, only because it is moving fast.", "That is the special relativity effect."),
      ("They run at the same rate, because both are in the Earth's field.", "The field strength and potential differ.")],
     "Time runs more slowly deeper in a gravitational field."),
    ("According to general relativity, why does light bend as it passes close to a massive star?",
     "The star curves spacetime, and the light follows a geodesic through the curved spacetime.",
     [("Photons have mass, so Newton's law of gravitation pulls them.", "Photons have no mass."),
      ("The light is refracted by the star's gravitational field lines.", "This is not refraction."),
      ("The star slows the light, which changes its direction.", "The speed of light in a vacuum is constant.")],
     "Mass curves spacetime; light follows the shortest path in it."),
    ("On a spacetime diagram (time vertical, distance horizontal), which world line shows an accelerating object?",
     "A curved line.",
     [("A vertical straight line.", "That is a stationary object."),
      ("A sloping straight line.", "That is constant velocity."),
      ("A horizontal straight line.", "That would be at many places at one instant, which is impossible.")],
     "The gradient of a world line changes when the velocity changes."),
]
gen_relativity_explain = explain_set(QT_GR, _EXPLAIN_GR, NOTES_GR)


def gen_brightness(level="AH"):
    lum = pick_sig(2.0e25, 9.0e30, 3)
    ly = pick_sig(4.0, 900.0, 3)
    d = ly * LIGHT_YEAR
    b = lum / (4 * math.pi * d**2)
    kind = random.choice(["b", "L", "d"])
    if kind == "b":
        return calc(QT_S, f"A star of luminosity {fmt(lum)} W is {ly:g} light-years from the Earth. Calculate its "
                          f"apparent brightness.", b, "W m⁻²",
                    [rf"d = {ly:g} \times 3.00 \times 10^8 \times 365.25 \times 24 \times 3600 = {ltx(d)}\ \mathrm{{m}}",
                     r"b = \frac{L}{4\pi d^2}", rf"b = {ltx(b)}\ \mathrm{{W\,m^{{-2}}}}"],
                    wrong=[(lum / (4 * math.pi * ly**2), "Convert light-years to metres."),
                           (lum / (4 * math.pi * d), "d must be squared.")],
                    scaffold=[("What is d in metres?", d, "m"), ("What is b?", b, "W m⁻²")], notes=NOTES_S)
    dm, bg = sig(d, 3), sig(b, 3)
    if kind == "L":
        ans = bg * 4 * math.pi * dm**2
        return calc(QT_S, f"The apparent brightness of a star is {fmt(bg)} W m⁻². The star is {fmt(dm)} m away. "
                          f"Calculate its luminosity.", ans, "W",
                    [r"b = \frac{L}{4\pi d^2}", rf"L = 4\pi d^2 b = {ltx(ans)}\ \mathrm{{W}}"],
                    wrong=[(bg * 4 * math.pi * dm, "d must be squared.")], notes=NOTES_S)
    ans = math.sqrt(lum / (4 * math.pi * bg)) / LIGHT_YEAR
    return calc(QT_S, f"A star of luminosity {fmt(lum)} W has an apparent brightness of {fmt(bg)} W m⁻² at the Earth. "
                      f"Determine the distance to the star in light-years.", ans, "ly",
                [r"b = \frac{L}{4\pi d^2}", rf"d = {ltx(ans*LIGHT_YEAR)}\ \mathrm{{m}}",
                 rf"d = \frac{{{ltx(ans*LIGHT_YEAR)}}}{{{ltx(LIGHT_YEAR)}}} = {ltx(ans)}\ \mathrm{{ly}}"],
                wrong=[(ans * LIGHT_YEAR, "That is the distance in metres. Convert to light-years.")],
                scaffold=[("What is d in metres?", ans * LIGHT_YEAR, "m"), ("What is d in light-years?", ans, "ly")],
                notes=NOTES_S)


def gen_luminosity(level="AH"):
    k = pick_sig(0.30, 30.0)
    r = sig(k * R_SUN, 3)
    Tk = random.randrange(3200, 25000, 100)
    lum = 4 * math.pi * r**2 * SIGMA * Tk**4
    kind = random.choice(["L", "T", "r", "PA"])
    if kind == "PA":
        pa = SIGMA * Tk**4
        return calc(QT_S, f"A star has a surface temperature of {Tk} K. Treating it as a black body, calculate the "
                          f"power radiated by each square metre of its surface.", pa, "W m⁻²",
                    [r"\frac{P}{A} = \sigma T^4", rf"\frac{{P}}{{A}} = {ltx(pa)}\ \mathrm{{W\,m^{{-2}}}}"],
                    wrong=[(SIGMA * Tk, "T is raised to the power 4.")], notes=NOTES_S)
    if kind == "L":
        return calc(QT_S, f"A star has a radius of {fmt(r)} m and a surface temperature of {Tk} K. Calculate its "
                          f"luminosity.", lum, "W",
                    [r"L = 4\pi r^2\sigma T^4", rf"L = {ltx(lum)}\ \mathrm{{W}}"],
                    wrong=[(math.pi * r**2 * SIGMA * Tk**4, "The surface area of a sphere is 4πr²."),
                           (4 * math.pi * r**2 * SIGMA * Tk, "T is raised to the power 4.")], notes=NOTES_S)
    lg = sig(lum, 3)
    if kind == "T":
        ans = (lg / (4 * math.pi * r**2 * SIGMA)) ** 0.25
        return calc(QT_S, f"A star of radius {fmt(r)} m has a luminosity of {fmt(lg)} W. Calculate its surface "
                          f"temperature.", ans, "K",
                    [r"L = 4\pi r^2\sigma T^4", rf"T^4 = {ltx(ans**4)}\ \mathrm{{K^4}}", rf"T = {ltx(ans)}\ \mathrm{{K}}"],
                    wrong=[(math.sqrt(ans**4), "Take the fourth root, not the square root.")], notes=NOTES_S)
    ans = math.sqrt(lg / (4 * math.pi * SIGMA * Tk**4))
    return calc(QT_S, f"A star with surface temperature {Tk} K has a luminosity of {fmt(lg)} W. Calculate its radius.",
                ans, "m",
                [r"L = 4\pi r^2\sigma T^4", rf"r^2 = {ltx(ans**2)}\ \mathrm{{m^2}}", rf"r = {ltx(ans)}\ \mathrm{{m}}"],
                wrong=[(ans**2, "That is r² — take the square root.")], notes=NOTES_S)


_EXPLAIN_S = [
    ("What keeps a main sequence star a stable size?",
     "Outward thermal pressure from core fusion balances the inward gravitational force.",
     [("The outward gravitational force balances the inward thermal pressure.", "The directions are the wrong way round."),
      ("Nuclear fission in the core balances the star's weight.", "Stars fuse hydrogen."),
      ("The strong force between the star's layers balances gravity.", "The strong force acts only over nuclear distances.")],
     "Name both effects and their directions."),
    ("The hydrogen in the core of a star like the Sun runs low. What happens next?",
     "The core shrinks and heats, shell hydrogen fusion starts, and the surface expands and cools.",
     [("The core expands and cools, and the star becomes a white dwarf immediately.", "It becomes a giant first."),
      ("The surface shrinks and heats, moving the star up the main sequence.", "The surface expands and cools."),
      ("Fusion stops everywhere and the star becomes a neutron star.", "Shell fusion starts; the Sun is not massive enough for a neutron star.")],
     "The star moves to the giant region of the H–R diagram."),
    ("Where are white dwarf stars on a Hertzsprung–Russell diagram?",
     "Bottom left: high surface temperature and low luminosity.",
     [("Top right: low surface temperature and high luminosity.", "That is where giants and supergiants are."),
      ("Bottom right: low surface temperature and low luminosity.", "That is the cool end of the main sequence."),
      ("Top left: high surface temperature and high luminosity.", "That is the hot end of the main sequence.")],
     "Temperature decreases from left to right."),
    ("Two stars have the same surface temperature. Star X is 100 times more luminous than star Y. How do their "
     "radii compare?",
     "X's radius is 10 times Y's, because L ∝ r² when T is constant.",
     [("X's radius is 100 times Y's, because L ∝ r.", "L depends on r²."),
      ("X's radius is 10 000 times Y's.", "Take the square root of the luminosity ratio."),
      ("They are equal, because the temperatures are equal.", "Luminosity also depends on surface area.")],
     "L = 4πr²σT⁴: state what is constant, then the relationship."),
    ("Which of these correctly describes the lifetime of a massive main sequence star compared with the Sun?",
     "It is shorter, because it uses its hydrogen at a much greater rate.",
     [("It is longer, because it has more hydrogen.", "It fuses hydrogen much faster than the extra mass makes up for."),
      ("It is the same, because both fuse hydrogen.", "The rate of fusion depends on mass."),
      ("It is longer, because its stronger gravity slows fusion.", "Stronger gravity gives a hotter core and faster fusion.")],
     "Mass determines lifetime."),
    ("What is the first stage of the proton–proton chain?",
     "Two protons fuse to form deuterium, releasing a positron and a neutrino.",
     [("Two protons fuse to form helium-3, releasing a gamma ray.", "Helium-3 forms in the second stage."),
      ("Four protons fuse at once to form helium-4.", "The chain happens in stages."),
      ("Two helium-3 nuclei fuse to form helium-4 and two protons.", "That is the last stage.")],
     "¹H + ¹H → ²H + e⁺ + ν."),
]
gen_stellar_explain = explain_set(QT_S, _EXPLAIN_S, NOTES_S)
