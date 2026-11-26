"""AH — Particles from space: charged particles in magnetic fields, cosmic rays and the solar wind."""
import math
import random

from topics.quanta_waves.common_ah import (
    E_CHARGE, M_ALPHA, M_E, M_P, L, T, calc, explain_set, fmt, ltx, pick_sig, sig, uni,
)

QT = "Particles from Space"

NOTES = r"""
## Particles from space

$$F = qvB \qquad F = \frac{mv^2}{r}$$

- **Solar wind:** charged particles (e.g. protons and electrons) in the form of **plasma** from the Sun.
- **Cosmic rays:** very high energy particles from sources such as the Sun, stars and black holes.
  They interact with the Earth's atmosphere, producing showers of secondary particles.
- Only the component of velocity **perpendicular** to the field, v sin θ, experiences a force.
- **Helical path:** the component of velocity **parallel** to the field is unaffected (constant); the
  component **perpendicular** to the field gives a central force and circular motion. Don't describe the
  components as "horizontal" and "vertical".
"""

_PARTICLES = [("proton", M_P, E_CHARGE), ("alpha particle", M_ALPHA, 2 * E_CHARGE), ("electron", M_E, E_CHARGE)]


def _setup():
    name, m, q = random.choice(_PARTICLES)
    v = sig(uni(1.0, 9.0) * (1e6 if name == "electron" else 1e5), 2)
    B = sig(uni(1.5, 9.0) * 10.0 ** random.choice([-5, -3]), 2)
    return name, m, q, v, B


def gen_circular_path(level="AH"):
    name, m, q, v, B = _setup()
    r = m * v / (q * B)
    kind = random.choice(["F", "r", "v"])
    an = "an" if name[0] in "ae" else "a"
    if kind == "F":
        return calc(QT, f"{an.title()} {name} (charge {fmt(q)} C) moves at {fmt(v, 2)} m s⁻¹ at right angles to a "
                        f"magnetic field of magnetic induction {fmt(B, 2)} T. Calculate the force on it.", q * v * B, "N",
                    [r"F = qvB", rf"F = {ltx(q*v*B)}\ \mathrm{{N}}"],
                    wrong=[(q * v / B, "F = qvB — multiply by B.")], notes=NOTES)
    if kind == "r":
        return calc(QT, f"{an.title()} {name} (mass {fmt(m, 4)} kg, charge {fmt(q)} C) moves at {fmt(v, 2)} m s⁻¹ at "
                        f"right angles to a magnetic field of {fmt(B, 2)} T. Calculate the radius of its path.", r, "m",
                    [r"qvB = \frac{mv^2}{r}", rf"r = \frac{{mv}}{{qB}} = {ltx(r)}\ \mathrm{{m}}"],
                    wrong=[(m * v**2 / (q * B), "Cancel one v: r = mv/qB."), (q * B / (m * v), "This is 1/r.")], notes=NOTES)
    rg = sig(r, 3)
    ans = q * B * rg / m
    return calc(QT, f"{an.title()} {name} (mass {fmt(m, 4)} kg, charge {fmt(q)} C) follows a circular path of radius "
                    f"{fmt(rg)} m in a magnetic field of {fmt(B, 2)} T. Calculate its speed.", ans, "m s⁻¹",
                [r"qvB = \frac{mv^2}{r}", rf"v = \frac{{qBr}}{{m}} = {ltx(ans)}\ \mathrm{{m\,s^{{-1}}}}"],
                wrong=[(q * B / (m * rg), "Rearrange: v = qBr/m.")], notes=NOTES)


def gen_helical_path(level="AH"):
    name, m, q, v, B = _setup()
    angle = random.randrange(20, 75, 5)
    perp = v * math.sin(math.radians(angle))
    par = v * math.cos(math.radians(angle))
    r = m * perp / (q * B)
    period = 2 * math.pi * m / (q * B)
    pitch = par * period
    stem = (f"{'An' if name[0] in 'ae' else 'A'} {name} (mass {fmt(m, 4)} kg, charge {fmt(q)} C) enters a uniform "
            f"magnetic field of {fmt(B, 2)} T at {fmt(v, 2)} m s⁻¹, at {angle}° to the field direction, and follows "
            f"a helical path. ")
    kind = random.choice(["r", "F", "pitch"])
    if kind == "r":
        return calc(QT, stem + "Calculate the radius of the helix.", r, "m",
                    [rf"v_\perp = {ltx(v, 2)} \sin {angle}^\circ = {ltx(perp)}\ \mathrm{{m\,s^{{-1}}}}",
                     r"qv_\perp B = \frac{mv_\perp^2}{r}", rf"r = {ltx(r)}\ \mathrm{{m}}"],
                    wrong=[(m * v / (q * B), "Use only the component perpendicular to the field, v sin θ."),
                           (m * par / (q * B), "That used the parallel component. Use v sin θ.")],
                    scaffold=[("What is the perpendicular component of velocity?", perp, "m s⁻¹"), ("What is r?", r, "m")], notes=NOTES)
    if kind == "F":
        return calc(QT, stem + "Calculate the magnetic force on the particle.", q * perp * B, "N",
                    [r"F = qvB", rf"F = q(v\sin\theta)B = {ltx(q*perp*B)}\ \mathrm{{N}}"],
                    wrong=[(q * v * B, "Use v sin θ, the component perpendicular to the field."),
                           (q * par * B, "The parallel component experiences no force.")], notes=NOTES)
    return calc(QT, stem + "Calculate the pitch of the helix (the distance travelled along the field in one revolution).",
                pitch, "m",
                [rf"v_\perp = {ltx(perp)} \qquad v_\parallel = {ltx(par)}\ \mathrm{{m\,s^{{-1}}}}",
                 rf"r = {ltx(r)}\ \mathrm{{m}} \qquad T = \frac{{2\pi r}}{{v_\perp}} = {ltx(period)}\ \mathrm{{s}}",
                 rf"d = v_\parallel T = {ltx(pitch)}\ \mathrm{{m}}"],
                wrong=[(perp * period, "Along the field, use the parallel component v cos θ."),
                       (v * period, "Only the parallel component moves the particle along the field.")],
                scaffold=[("What is the radius?", r, "m"), ("What is the time for one revolution?", period, "s"),
                          ("What is the pitch?", pitch, "m")], notes=NOTES)


_EXPLAIN = [
    ("A charged particle enters a magnetic field at 40° to the field direction. Why does it follow a helical path?",
     "The velocity component parallel to the field is unaffected; the perpendicular component gives a central force and circular motion.",
     [("The horizontal component of velocity is unaffected and the vertical component causes circular motion.",
       "'Horizontal' and 'vertical' are not accepted: say parallel and perpendicular to the field."),
      ("The magnetic force has one part along the field and one part at right angles to it.", "The magnetic force has no component along the field."),
      ("The magnetic field does work, so the particle speeds up as it circles.", "The force is perpendicular to the velocity, so no work is done.")],
     "One mark for each component."),
    ("What is the solar wind?",
     "A flow of charged particles from the Sun in the form of plasma.",
     [("A flow of high-energy photons from the Sun.", "It consists of charged particles."),
      ("Cosmic rays that come from outside the galaxy.", "The solar wind comes from the Sun."),
      ("Movement of the Earth's upper atmosphere caused by sunlight.", "It is not an atmospheric wind.")],
     "Mostly protons and electrons."),
    ("Which is a source of cosmic rays?",
     "Stars, including the Sun, and black holes.",
     [("The solar wind.", "'Solar wind' is not accepted as an origin of cosmic rays."),
      ("The Earth's magnetic field.", "The field deflects charged particles; it does not produce them."),
      ("Radio transmissions from satellites.", "Cosmic rays are high-energy particles from space.")],
     "Name the astronomical object."),
    ("What happens when a high-energy cosmic ray enters the Earth's atmosphere?",
     "It interacts with particles in the atmosphere, producing a shower of secondary particles.",
     [("It passes straight to the ground without interacting.", "Most interact high in the atmosphere."),
      ("It is reflected back into space by the ozone layer.", "It interacts with the air."),
      ("It follows a circular orbit around the Earth for ever.", "It interacts in the atmosphere.")],
     "Detectors on high mountains are nearer to the primary rays."),
    ("Why is a cosmic ray observatory often built at high altitude?",
     "It is closer to the cosmic rays, before more of their interactions with the atmosphere.",
     [("There is no magnetic field at high altitude.", "The Earth's field extends far beyond the atmosphere."),
      ("The gravitational field is zero there.", "It is only slightly weaker."),
      ("Cosmic rays are only produced in the upper atmosphere.", "They come from space.")],
     "Less atmosphere above the detector."),
    ("A charged particle in a helical path moves into a region where the magnetic induction is weaker. What happens, and why?",
     "The radius of the helix increases, because r = mv/qB with v perpendicular, m and q constant and B smaller.",
     [("The radius decreases, because the force is smaller.", "A smaller force gives a larger radius."),
      ("The particle speeds up, so the radius increases.", "A magnetic field does not change the speed."),
      ("The path becomes a straight line.", "There is still a field.")],
     "Say what stays constant and give the relationship."),
    ("A charged particle moves parallel to a uniform magnetic field. Describe its motion.",
     "It continues in a straight line at constant velocity, as there is no magnetic force on it.",
     [("It moves in a circle.", "That needs a velocity component perpendicular to the field."),
      ("It accelerates along the field.", "A magnetic field exerts no force along the field."),
      ("It moves in a helix.", "A helix needs both parallel and perpendicular components.")],
     "F = qvB sin θ type reasoning: the perpendicular component is zero."),
]
gen_particles_explain = explain_set(QT, _EXPLAIN, NOTES)
