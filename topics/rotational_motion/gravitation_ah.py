"""AH — Gravitation: force, satellites, gravitational potential and escape velocity."""
import math
import random

from topics.rotational_motion.common_ah import (
    G, M_EARTH, M_SUN, R_EARTH, L, T, calc, explain_set, fmt, ltx, pick_sig, sig, uni,
)

QT = "Gravitation"

NOTES = r"""
## Gravitation

$$F = \frac{GMm}{r^2} \qquad \frac{GMm}{r^2} = \frac{mv^2}{r} = mr\omega^2 = mr\left(\frac{2\pi}{T}\right)^2$$

$$V = -\frac{GM}{r} \qquad E_P = Vm = -\frac{GMm}{r} \qquad v_{esc} = \sqrt{\frac{2GM}{r}}$$

- **Gravitational field strength** is the gravitational force acting on a unit mass.
- **Gravitational potential** at a point is the work done in moving unit mass from infinity to that point.
- **Escape velocity** is the minimum velocity that allows a mass to escape a gravitational field to infinity.
- V and Ep are **negative** (zero at infinity). Keep the minus sign.
- r is measured from the **centre** of the body: r = R + h.
- Energy needed to move between two points = change in Ep, whatever path is taken.
"""

_BODIES = [("the Earth", M_EARTH, R_EARTH), ("Mars", 6.42e23, 3.39e6), ("the Moon", 7.35e22, 1.74e6),
           ("Jupiter", 1.90e27, 7.15e7)]


def gen_satellites(level="AH"):
    name, M, R = random.choice(_BODIES)
    r = sig(R * uni(1.2, 6.0), 3)
    T_ = 2 * math.pi * math.sqrt(r**3 / (G * M))
    v = math.sqrt(G * M / r)
    kind = random.choice(["period", "speed", "radius", "mass"])
    if kind == "period":
        return calc(QT, f"A satellite moves in a circular orbit of radius {fmt(r)} m around {name} "
                        f"(mass {fmt(M)} kg). Calculate the period of the orbit.", T_, "s",
                    [r"\frac{GMm}{r^2} = mr\left(\frac{2\pi}{T}\right)^2",
                     rf"T = 2\pi\sqrt{{\frac{{r^3}}{{GM}}}} = {ltx(T_)}\ \mathrm{{s}}"],
                    wrong=[(2 * math.pi * math.sqrt(r**2 / (G * M)), "r must be cubed."),
                           (r**3 / (G * M), "Take the square root and multiply by 2π.")], notes=NOTES)
    if kind == "speed":
        return calc(QT, f"A satellite moves in a circular orbit of radius {fmt(r)} m around {name} "
                        f"(mass {fmt(M)} kg). Calculate its orbital speed.", v, "m s⁻¹",
                    [r"\frac{GMm}{r^2} = \frac{mv^2}{r}", rf"v = \sqrt{{\frac{{GM}}{{r}}}} = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(math.sqrt(2 * G * M / r), "That is the escape velocity from this radius."),
                           (G * M / r, "That is v² — take the square root.")], notes=NOTES)
    if kind == "radius":
        hours = pick_sig(2.0, 30.0)
        Ts = hours * 3600
        rr = (G * M * Ts**2 / (4 * math.pi**2)) ** (1 / 3)
        return calc(QT, f"A satellite orbits {name} (mass {fmt(M)} kg) in a circular orbit with a period of "
                        f"{hours:g} hours. Calculate the radius of the orbit.", rr, "m",
                    [rf"T = {hours:g} \times 3600 = {ltx(Ts)}\ \mathrm{{s}}",
                     r"\frac{GMm}{r^2} = mr\left(\frac{2\pi}{T}\right)^2",
                     rf"r^3 = \frac{{GMT^2}}{{4\pi^2}} \qquad r = {ltx(rr)}\ \mathrm{{m}}"],
                    wrong=[((G * M * hours**2 / (4 * math.pi**2)) ** (1 / 3), "Convert the period to seconds."),
                           (math.sqrt(G * M * Ts**2 / (4 * math.pi**2)), "Take the cube root, not the square root.")],
                    scaffold=[("What is the period in seconds?", Ts, "s"), ("What is r³?", rr**3, "m³"),
                              ("What is r?", rr, "m")], notes=NOTES)
    rm = pick_sig(2.0e8, 2.0e9, 3)
    Ms = pick_sig(5e24, 2e27, 3)
    days = sig(2 * math.pi * math.sqrt(rm**3 / (G * Ms)) / 86400, 3)
    ans = 4 * math.pi**2 * rm**3 / (G * (days * 86400)**2)
    return calc(QT, f"A moon orbits a planet in a circle of radius {fmt(rm)} m with a period of {days:g} days. "
                    f"Determine the mass of the planet.", ans, "kg",
                [rf"T = {days:g} \times 86400 = {ltx(days*86400)}\ \mathrm{{s}}",
                 r"\frac{GMm}{r^2} = mr\left(\frac{2\pi}{T}\right)^2",
                 rf"M = \frac{{4\pi^2 r^3}}{{GT^2}} = {ltx(ans)}\ \mathrm{{kg}}"],
                wrong=[(4 * math.pi**2 * rm**3 / (G * days**2), "Convert the period from days to seconds.")], notes=NOTES)


def gen_potential_energy(level="AH"):
    name, M, R = random.choice(_BODIES)
    m = pick_sig(200, 6000)
    r1 = sig(R * uni(1.1, 2.0), 3)
    r2 = sig(r1 * uni(1.5, 4.0), 3)
    kind = random.choice(["V", "Ep", "change"])
    if kind == "V":
        V = -G * M / r1
        return calc(QT, f"Calculate the gravitational potential at a point {fmt(r1)} m from the centre of {name} "
                        f"(mass {fmt(M)} kg).", V, "J kg⁻¹",
                    [r"V = -\frac{GM}{r}", rf"V = {ltx(V)}\ \mathrm{{J\,kg^{{-1}}}}"],
                    wrong=[(-V, "Gravitational potential is negative."), (-G * M / r1**2, "r is not squared in V = −GM/r.")],
                    notes=NOTES)
    if kind == "Ep":
        E = -G * M * m / r1
        return calc(QT, f"A {fmt(m)} kg spacecraft is {fmt(r1)} m from the centre of {name} (mass {fmt(M)} kg). "
                        f"Calculate its gravitational potential energy.", E, "J",
                    [r"E_P = -\frac{GMm}{r}", rf"E_P = {ltx(E)}\ \mathrm{{J}}"],
                    wrong=[(-E, "Gravitational potential energy is negative."),
                           (-G * M * m / r1**2, "That is minus the force. r is not squared for Ep.")], notes=NOTES)
    dE = G * M * m * (1 / r1 - 1 / r2)
    return calc(QT, f"A {fmt(m)} kg satellite is moved from {fmt(r1)} m to {fmt(r2)} m from the centre of {name} "
                    f"(mass {fmt(M)} kg). Calculate the change in its gravitational potential energy.", dE, "J",
                [r"E_P = -\frac{GMm}{r}",
                 rf"E_{{P1}} = {ltx(-G*M*m/r1)}\ \mathrm{{J}} \qquad E_{{P2}} = {ltx(-G*M*m/r2)}\ \mathrm{{J}}",
                 rf"\Delta E_P = E_{{P2}} - E_{{P1}} = {ltx(dE)}\ \mathrm{{J}}"],
                wrong=[(-dE, "Final minus initial: moving further away increases Ep (it becomes less negative)."),
                       (G * M * m / (r2 - r1), "Find Ep at each radius, then subtract. You can't use the difference in r.")],
                scaffold=[("What is the initial Ep?", -G * M * m / r1, "J"), ("What is the final Ep?", -G * M * m / r2, "J"),
                          ("What is the change in Ep?", dE, "J")], sf=3, notes=NOTES)


def gen_escape_velocity(level="AH"):
    M = pick_sig(1e21, 9e25, 3)
    R = pick_sig(5e5, 9e6, 3)
    v = math.sqrt(2 * G * M / R)
    if random.random() < 0.65:
        return calc(QT, f"A planet has a mass of {fmt(M)} kg and a radius of {fmt(R)} m. Calculate the escape "
                        f"velocity from its surface.", v, "m s⁻¹",
                    [r"v_{esc} = \sqrt{\frac{2GM}{r}}", rf"v_{{esc}} = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(math.sqrt(G * M / R), "That is the orbital speed — escape velocity has a factor of 2."),
                           (2 * G * M / R, "Take the square root.")], notes=NOTES)
    vg = sig(v, 3)
    Mans = vg**2 * R / (2 * G)
    return calc(QT, f"The escape velocity from the surface of a planet of radius {fmt(R)} m is {fmt(vg)} m s⁻¹. "
                    f"Calculate the mass of the planet.", Mans, "kg",
                [r"v_{esc} = \sqrt{\frac{2GM}{r}}", rf"M = \frac{{v^2 r}}{{2G}} = {ltx(Mans)}\ \mathrm{{kg}}"],
                wrong=[(vg**2 * R / G, "You lost the factor of 2."), (vg * R / (2 * G), "v must be squared.")], notes=NOTES)


_EXPLAIN = [
    ("Why is the gravitational potential at a point near a planet negative?",
     "Potential is zero at infinity, and work is done by the field as unit mass moves from infinity to the point.",
     [("The gravitational force acts in the negative direction.", "Potential is a scalar."),
      ("Mass is being lost as it approaches the planet.", "No mass is lost."),
      ("Potential is defined as zero at the planet's surface.", "The zero is at infinity.")],
     "Use the definition: work done in moving unit mass from infinity to the point."),
    ("A spacecraft can travel from point P to point Q in a gravitational field by a short route or a long one. "
     "How does the change in its gravitational potential energy compare?",
     "It is the same for both routes, because the change in potential energy does not depend on the path.",
     [("It is greater for the longer route.", "Only the start and end points matter."),
      ("It is greater for the shorter route.", "Only the start and end points matter."),
      ("It depends on the speed of the spacecraft.", "Ep depends only on position.")],
     "The gravitational field is conservative."),
    ("Spacecraft X has twice the mass of spacecraft Y. How do their escape velocities from the same point compare?",
     "They are the same: the spacecraft's mass cancels, so v depends only on M and r.",
     [("X's is twice Y's.", "Both the Ek needed and the Ep depend on m, so it cancels."),
      ("X's is √2 times Y's.", "The spacecraft's mass does not appear in √(2GM/r)."),
      ("X's is half of Y's.", "The mass cancels.")],
     "½mv² = GMm/r, so m cancels."),
    ("A satellite is moved to a circular orbit of larger radius. What happens to its orbital speed and gravitational "
     "potential energy?",
     "Its speed decreases and its potential energy increases (becomes less negative).",
     [("Its speed increases and its potential energy increases.", "v = √(GM/r) decreases as r increases."),
      ("Its speed decreases and its potential energy decreases.", "−GMm/r rises towards zero."),
      ("Both stay the same, because no work is done in orbit.", "Work is needed to change the orbit.")],
     ["v = √(GM/r) with GM constant, so v decreases.", "Ep = −GMm/r becomes less negative."]),
]
gen_gravitation_explain = explain_set(QT, _EXPLAIN, NOTES)
