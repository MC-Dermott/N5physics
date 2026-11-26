"""AH Rotational Motion and Astrophysics — exam-style multi-part scenarios in the style of SQA papers.

"Show" questions are asked as calculations of the shown value, so they can be marked.
"""
import math

from topics.exam_style.base import Exam, pick, sig, fmt, ltx
from topics.rotational_motion.angular_motion_ah import NOTES as ANG, NOTES_C
from topics.rotational_motion.astrophysics_ah import NOTES_GR, NOTES_S
from topics.rotational_motion.common_ah import (
    AU, C, G, LEVEL, LIGHT_YEAR, M_EARTH, M_SUN, R_EARTH, R_SUN, SIGMA, UNIT, uni,
)
from topics.rotational_motion.gravitation_ah import NOTES as GRAV
from topics.rotational_motion.kinematics_ah import NOTES as KIN
from topics.rotational_motion.rotational_dynamics_ah import NOTES as ROT

_KIN, _ANG, _CEN = "Kinematic Relationships", "Angular Motion", "Centripetal Force"
_ROT, _GRAV, _GR, _STAR = "Rotational Dynamics", "Gravitation", "General Relativity", "Stellar Physics"

_NOTES = {_KIN: KIN, _ANG: ANG, _CEN: NOTES_C, _ROT: ROT, _GRAV: GRAV, _GR: NOTES_GR, _STAR: NOTES_S}


def _exam():
    return Exam(UNIT, LEVEL, _NOTES)


def _test_car(level=LEVEL):
    ex = _exam()
    a, b = uni(0.10, 0.30, 2), uni(1.5, 3.5)
    t, r = uni(3.0, 6.0), uni(0.28, 0.36, 2)
    v = 3 * a * t**2 + 2 * b * t
    acc = 6 * a * t + 2 * b
    ex.on(_KIN).num(f"Calculate the velocity of the car at t = {t:g} s.", v, "m s⁻¹",
                    wrong=[((a * t**3 + b * t**2) / t, "That is the average velocity. Differentiate s.")],
                    working=[r"v = \frac{ds}{dt}", rf"v = {ltx(3*a)}t^2 + {sig(2*b):g}t = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num(f"Calculate the acceleration of the car at t = {t:g} s.", acc, "m s⁻²",
           wrong=[(v / t, "The acceleration is not constant — differentiate v.")],
           working=[r"a = \frac{dv}{dt}", rf"a = {ltx(6*a)}t + {sig(2*b):g} = {ltx(acc)}\ \mathrm{{m\,s^{{-2}}}}"])
    ex.on(_ANG).num(f"The wheels have a radius of {r:g} m and do not slip. Calculate the angular velocity of a "
                    f"wheel at t = {t:g} s.", sig(v) / r, "rad s⁻¹",
                    wrong=[(sig(v) * r, "v = rω, so ω = v/r.")],
                    working=[r"v = r\omega", rf"\omega = {ltx(sig(v)/r)}\ \mathrm{{rad\,s^{{-1}}}}"])
    ex.on(_KIN).choice("Why can s = ut + ½at² not be used to find the displacement of this car?",
                       "The acceleration is not constant.",
                       [("The car starts from rest.", "The equation works with u = 0."),
                        ("The velocity is changing.", "It works for changing velocity if a is constant."),
                        ("The car moves in a straight line.", "It applies to straight line motion.")])
    return ex.build(f"A car is tested on a straight track. Its displacement s, in metres, for the first 8 s is "
                    f"given by **s = {a:g}t³ + {b:g}t²**, where t is in seconds.")


def _cyclist_bend(level=LEVEL):
    ex = _exam()
    k, u = uni(0.10, 0.30, 2), uni(3.0, 6.0)
    t = uni(3.0, 5.0)
    v = u + k * t**2 / 2
    s = u * t + k * t**3 / 6
    R, m = uni(18.0, 35.0), pick(72, 78, 84)
    ex.on(_KIN).num(f"Calculate the velocity of the cyclist at t = {t:g} s.", v, "m s⁻¹",
                    wrong=[(v - u, "Include the constant of integration."), (u + k * t**2, "∫kt dt = ½kt².")],
                    working=[rf"v = \int {k:g}t\,dt = {ltx(k/2)}t^2 + {u:g}", rf"v = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num(f"Calculate the distance travelled in the first {t:g} s.", s, "m",
           wrong=[(u * t + 0.5 * k * t * t**2, "The acceleration changes, so integrate.")],
           working=[rf"s = \int v\,dt = {ltx(k/6)}t^3 + {u:g}t", rf"s = {ltx(s)}\ \mathrm{{m}}"])
    F = m * sig(v)**2 / R
    ex.on(_CEN).num(f"The cyclist then goes round a level bend of radius {R:g} m at a constant {fmt(v)} m s⁻¹. "
                    f"The total mass of cyclist and bicycle is {m} kg. Calculate the centripetal force required.",
                    F, "N", wrong=[(m * sig(v) / R, "v must be squared.")],
                    working=[r"F = \frac{mv^2}{r}", rf"F = {ltx(F)}\ \mathrm{{N}}"])
    ex.choice("What provides this centripetal force?", "Friction between the tyres and the road.",
              [("An outward centrifugal force.", "No outward force acts on the cyclist."),
               ("The weight of the cyclist.", "The weight is vertical; the road is level."),
               ("The driving force along the direction of motion.", "The central force is perpendicular to the motion.")])
    return ex.build(f"A cyclist passes a marker at {u:g} m s⁻¹ and accelerates along a straight road. The "
                    f"acceleration, in m s⁻², is given by **a = {k:g}t**.")


def _spin_drier(level=LEVEL):
    ex = _exam()
    rpm, t = pick(900, 1100, 1200, 1400), uni(12.0, 25.0)
    r, m = uni(0.20, 0.28, 2), uni(0.020, 0.080, 3)
    w = rpm * 2 * math.pi / 60
    ws = sig(w)
    alpha = ws / t
    theta = ws * t / 2
    F = m * r * ws**2
    ex.on(_ANG).num("Calculate the maximum angular velocity of the drum in rad s⁻¹.", w, "rad s⁻¹",
                    wrong=[(rpm / 60, "Multiply by 2π.")],
                    working=[rf"\omega = \frac{{{rpm} \times 2\pi}}{{60}} = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"])
    ex.num("Calculate the angular acceleration of the drum.", alpha, "rad s⁻²",
           working=[r"\omega = \omega_o + \alpha t", rf"\alpha = {ltx(alpha)}\ \mathrm{{rad\,s^{{-2}}}}"])
    ex.num("Determine the number of revolutions made while the drum speeds up.", theta / (2 * math.pi), "",
           wrong=[(theta, "That is in radians. Divide by 2π.")],
           working=[rf"\theta = \tfrac{{1}}{{2}}\alpha t^2 = {ltx(theta)}\ \mathrm{{rad}}",
                    rf"\frac{{\theta}}{{2\pi}} = {ltx(theta/(2*math.pi))}"],
           scaffold=[("What is the angular displacement?", theta, "rad")])
    ex.on(_CEN).num(f"At maximum speed, calculate the centripetal force on an item of mass {m:g} kg, {r:g} m from "
                    f"the axis.", F, "N", wrong=[(m * r * ws, "ω must be squared.")],
                    working=[r"F = mr\omega^2", rf"F = {ltx(F)}\ \mathrm{{N}}"])
    ex.choice("Water leaves the wet clothes through holes in the drum, but the clothes stay inside. Why?",
              "The drum exerts a central force on the clothes; at a hole no central force acts on the water, so it moves off along a tangent.",
              [("A centrifugal force throws the water radially outwards.", "No outward force acts on the water."),
               ("The water has no inertia once it leaves the clothes.", "It is its inertia that keeps it moving along the tangent."),
               ("The centripetal force pushes the water out through the holes.", "A centripetal force is towards the centre.")])
    return ex.build(f"The drum of a spin drier starts from rest and accelerates uniformly to {rpm} revolutions per "
                    f"minute in {t:g} s.")


def _roundabout(level=LEVEL):
    ex = _exam()
    M, R = pick(110, 130, 150, 180), uni(1.1, 1.6)
    F, t = pick(60, 75, 90, 110), uni(3.0, 6.0)
    tf = pick(12, 15, 18, 20)
    m = pick(28, 32, 36, 40)
    I = sig(0.5 * M * R**2)
    alpha = (F * R - tf) / I
    a_s = sig(alpha)
    w = a_s * t
    ws = sig(w)
    w2 = I * ws / (I + m * R**2)
    ex.on(_ROT).num("Calculate the moment of inertia of the roundabout (a uniform disc, I = ½mr²).", I, "kg m²",
                    wrong=[(M * R**2, "A disc has I = ½mr²."), (0.5 * M * R, "Square the radius.")],
                    working=[r"I = \tfrac{1}{2}mr^2", rf"I = {ltx(I)}\ \mathrm{{kg\,m^2}}"])
    ex.num("Calculate the angular acceleration while the force is applied.", alpha, "rad s⁻²",
           wrong=[(F * R / I, "Subtract the frictional torque.")],
           working=[r"Fr - \tau_f = I\alpha", rf"\alpha = {ltx(alpha)}\ \mathrm{{rad\,s^{{-2}}}}"],
           scaffold=[("What is the unbalanced torque?", F * R - tf, "N m")])
    ex.on(_ANG).num(f"Calculate the angular velocity after {t:g} s.", w, "rad s⁻¹",
                    working=[r"\omega = \omega_o + \alpha t", rf"\omega = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"])
    ex.on(_ROT).num(f"The pushing then stops. A child of mass {m} kg, initially at rest, steps straight on to the "
                    f"edge. Treating the child as a point mass, calculate the angular velocity immediately "
                    f"afterwards (the roundabout was turning at {fmt(w)} rad s⁻¹).", w2, "rad s⁻¹",
                    wrong=[(I * ws / (I + m), "The child's moment of inertia is mr².")],
                    working=[r"I\omega_1 = (I + mr^2)\omega_2", rf"\omega_2 = {ltx(w2)}\ \mathrm{{rad\,s^{{-1}}}}"],
                    scaffold=[("What is the moment of inertia of the child?", m * R**2, "kg m²")])
    ex.choice("The child now moves towards the centre. Ignoring friction, what happens to the angular velocity?",
              "It increases, because I decreases and angular momentum is conserved with no external torque.",
              [("It decreases, because I decreases.", "L = Iω is constant, so ω increases when I decreases."),
               ("It stays the same, because angular momentum is conserved.", "L is conserved, but I changes."),
               ("It increases, because an external torque acts.", "There is no external torque.")])
    return ex.build(f"A playground roundabout is a uniform disc of mass {M} kg and radius {R:g} m. From rest, a "
                    f"tangential force of {F} N is applied at the rim for {t:g} s. A constant frictional torque of "
                    f"{tf} N m acts.")


def _flywheel(level=LEVEL):
    ex = _exam()
    m, r = uni(0.20, 0.60, 2), uni(0.030, 0.080, 3)
    h, t = uni(0.80, 1.50, 2), uni(2.5, 5.0)
    v = 2 * h / t
    vs = sig(v)
    w = vs / r
    ws = sig(w)
    Erot = m * 9.8 * h - 0.5 * m * vs**2
    I = 2 * sig(Erot) / ws**2
    ex.on(_KIN).num("The mass accelerates uniformly from rest. Calculate its speed just before it reaches the floor.",
                    v, "m s⁻¹", wrong=[(h / t, "That is the average speed; the final speed is twice this.")],
                    working=[r"s = \tfrac{1}{2}(u + v)t", rf"v = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.on(_ANG).num("Calculate the angular velocity of the flywheel at this instant.", vs / r, "rad s⁻¹",
                    wrong=[(vs * r, "ω = v/r.")],
                    working=[r"v = r\omega", rf"\omega = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"])
    ex.on(_ROT).num("Neglecting friction, use conservation of energy to determine the moment of inertia of the flywheel.",
                    I, "kg m²",
                    wrong=[(2 * m * 9.8 * h / ws**2, "The falling mass also has kinetic energy.")],
                    working=[r"mgh = \tfrac{1}{2}mv^2 + \tfrac{1}{2}I\omega^2", rf"I = {ltx(I)}\ \mathrm{{kg\,m^2}}"],
                    scaffold=[("What is the rotational kinetic energy?", Erot, "J")])
    ex.choice("In practice there is friction at the axle. How does the true moment of inertia compare with this value?",
              "It is smaller, because some energy does work against friction, so less becomes rotational kinetic energy.",
              [("It is larger, because friction adds to the resistance to motion.", "The measured ω already includes friction."),
               ("It is the same, because I does not depend on friction.", "I does not, but the value calculated by ignoring friction does."),
               ("It is larger, because the mass takes longer to fall.", "Consider where the potential energy goes.")])
    return ex.build(f"A student measures the moment of inertia of a flywheel. A {m:g} kg mass hangs on a string "
                    f"wrapped round the axle, radius {r:g} m. Released from rest, the mass falls {h:g} m in {t:g} s.")


def _satellite(level=LEVEL):
    ex = _exam()
    h_km, m = pick(420, 560, 780, 1200, 2000), pick(450, 800, 1500, 2400)
    r = R_EARTH + h_km * 1000
    v = math.sqrt(G * M_EARTH / r)
    Tp = 2 * math.pi * r / v
    Ep = -G * M_EARTH * m / r
    ex.on(_GRAV).num("Calculate the orbital speed of the satellite.", v, "m s⁻¹",
                     wrong=[(math.sqrt(G * M_EARTH / (h_km * 1000)), "r is measured from the centre: r = R + h.")],
                     working=[r"\frac{GMm}{r^2} = \frac{mv^2}{r}", rf"v = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                     scaffold=[("What is the orbit radius?", r, "m")])
    ex.on(_ANG).num("Calculate the period of the orbit.", 2 * math.pi * r / sig(v), "s",
                    working=[r"T = \frac{2\pi r}{v}", rf"T = {ltx(Tp)}\ \mathrm{{s}}"])
    ex.on(_CEN).num("Calculate the radial acceleration of the satellite.", sig(v)**2 / r, "m s⁻²",
                    wrong=[(9.8, "g is 9.8 m s⁻² only near the Earth's surface.")],
                    working=[r"a_r = \frac{v^2}{r}", rf"a_r = {ltx(sig(v)**2/r)}\ \mathrm{{m\,s^{{-2}}}}"])
    ex.on(_GRAV).num("Calculate the gravitational potential energy of the satellite.", Ep, "J",
                     wrong=[(-Ep, "Gravitational potential energy is negative.")],
                     working=[r"E_P = -\frac{GMm}{r}", rf"E_P = {ltx(Ep)}\ \mathrm{{J}}"])
    ex.choice("What is meant by the gravitational potential at a point?",
              "The work done in moving unit mass from infinity to that point.",
              [("The work done in moving a mass from the surface to that point.", "The reference is infinity, and it is per unit mass."),
               ("The gravitational force acting on unit mass at that point.", "That is the field strength."),
               ("The potential energy of any mass at that point.", "It is per unit mass.")])
    return ex.build(f"A satellite of mass {m} kg is in a circular orbit {h_km} km above the Earth's surface.\n\n"
                    f"Mass of the Earth 6.0 × 10²⁴ kg; radius of the Earth 6.4 × 10⁶ m.")


def _moon_probe(level=LEVEL):
    ex = _exam()
    name, M, R = pick(("Ganymede", 1.48e23, 2.63e6), ("Callisto", 1.08e23, 2.41e6), ("Titan", 1.35e23, 2.57e6))
    m, k = pick(300, 550, 900), pick(3, 4, 5)
    g = G * M / R**2
    v = math.sqrt(2 * G * M / R)
    dE = G * M * m * (1 / R - 1 / (k * R))
    ex.on(_GRAV).num(f"Calculate the gravitational field strength at the surface of {name}.", g, "N kg⁻¹",
                     wrong=[(9.8, "9.8 N kg⁻¹ applies on the Earth.")],
                     working=[r"F = \frac{GMm}{r^2} \quad g = \frac{F}{m}", rf"g = {ltx(g)}\ \mathrm{{N\,kg^{{-1}}}}"])
    ex.num(f"Calculate the escape velocity from the surface of {name}.", v, "m s⁻¹",
           wrong=[(math.sqrt(G * M / R), "You lost the factor of 2.")],
           working=[r"v_{esc} = \sqrt{\frac{2GM}{r}}", rf"v_{{esc}} = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num(f"A {m} kg probe is raised from the surface to a distance of {k} radii from the centre. Calculate the "
           f"increase in its gravitational potential energy.", dE, "J",
           wrong=[(m * g * (k - 1) * R, "Ep = mgh needs g to be constant. Use Ep = −GMm/r at each point.")],
           working=[r"\Delta E_P = -\frac{GMm}{r_2} - \left(-\frac{GMm}{r_1}\right)", rf"\Delta E_P = {ltx(dE)}\ \mathrm{{J}}"])
    ex.on(_GR).choice(f"Identical clocks are on the surface of {name} and in the raised probe. Ignoring effects of "
                      f"speed, which clock runs more slowly?",
                      "The surface clock, because it is at a lower altitude, where the gravitational field is stronger.",
                      [("The probe clock, because it is higher in the field.", "Time runs more slowly lower in a field."),
                       ("Neither, because the clocks are identical.", "Gravity affects the passage of time."),
                       ("The probe clock, because it has more potential energy.", "Higher clocks run faster.")])
    return ex.build(f"A probe is sent to {name}, a moon of mass {fmt(M)} kg and radius {fmt(R)} m.")


def _black_hole(level=LEVEL):
    ex = _exam()
    n, d = pick(6.5, 9.8, 14, 21, 33), pick(2, 5, 10)
    M = n * M_SUN
    rs = 2 * G * M / C**2
    ro = pick(2.0e10, 5.0e10, 8.0e10)
    Tp = 2 * math.pi * math.sqrt(ro**3 / (G * M))
    ex.on(_GR).num("Calculate the Schwarzschild radius of the black hole.", rs, "m",
                   wrong=[(2 * G * n / C**2, "Convert solar masses to kg."), (2 * G * M / C, "c must be squared.")],
                   working=[r"r = \frac{2GM}{c^2}", rf"r = {ltx(rs)}\ \mathrm{{m}}"])
    ex.on(_GRAV).num(f"A companion star orbits the black hole in a circle of radius {fmt(ro)} m. Assuming the black "
                     f"hole is much more massive than the star, calculate the period of the orbit.", Tp, "s",
                     working=[r"\frac{GMm}{r^2} = mr\left(\frac{2\pi}{T}\right)^2", rf"T = {ltx(Tp)}\ \mathrm{{s}}"])
    L_ = pick(2.0e27, 8.0e27, 3.0e28)
    dist = d * 1000 * LIGHT_YEAR
    b = L_ / (4 * math.pi * dist**2)
    ex.on(_STAR).num(f"The companion has a luminosity of {fmt(L_)} W and is {d} 000 light-years from the Earth. "
                     f"Calculate its apparent brightness.", b, "W m⁻²",
                     wrong=[(L_ / (4 * math.pi * (d * 1000)**2), "Convert light-years to metres.")],
                     working=[r"b = \frac{L}{4\pi d^2}", rf"b = {ltx(b)}\ \mathrm{{W\,m^{{-2}}}}"],
                     scaffold=[("What is the distance in metres?", dist, "m")])
    ex.on(_GR).choice("A distant observer watches a clock falling towards the event horizon. What is observed?",
                      "The clock appears to run ever more slowly, and time appears frozen at the event horizon.",
                      [("The clock appears to run faster and faster.", "Time runs more slowly deeper in the field."),
                       ("The clock runs at its normal rate until it vanishes.", "The distant observer sees time dilation."),
                       ("The clock appears to run backwards at the event horizon.", "Time appears to stop, not reverse.")])
    return ex.build(f"A black hole of mass {n:g} solar masses is in a binary system. The mass of the Sun is "
                    f"2.0 × 10³⁰ kg.")


def _nearby_star(level=LEVEL):
    ex = _exam()
    k, Tk = uni(1.3, 2.4), pick(7200, 8100, 8700, 9600)
    r = sig(k * R_SUN)
    L_ = 4 * math.pi * r**2 * SIGMA * Tk**4
    Ls = sig(L_)
    ly = uni(8.0, 80.0)
    d = ly * LIGHT_YEAR
    b = Ls / (4 * math.pi * d**2)
    ex.on(_STAR).num("Calculate the luminosity of the star.", L_, "W",
                     wrong=[(math.pi * r**2 * SIGMA * Tk**4, "The surface area is 4πr²."),
                            (4 * math.pi * r**2 * SIGMA * Tk, "T is raised to the power 4.")],
                     working=[r"L = 4\pi r^2\sigma T^4", rf"L = {ltx(L_)}\ \mathrm{{W}}"])
    ex.num(f"The star is {ly:g} light-years from the Earth. Calculate its apparent brightness.", b, "W m⁻²",
           wrong=[(Ls / (4 * math.pi * ly**2), "Convert light-years to metres.")],
           working=[r"b = \frac{L}{4\pi d^2}", rf"b = {ltx(b)}\ \mathrm{{W\,m^{{-2}}}}"],
           scaffold=[("What is the distance in metres?", d, "m")])
    ex.choice("What assumption about the star was made in using L = 4πr²σT⁴?",
              "It behaves as a black body.",
              [("It is on the main sequence.", "The relationship does not depend on the type of star."),
               ("Its luminosity equals its apparent brightness.", "These are different quantities."),
               ("Its surface temperature is increasing.", "A single, uniform surface temperature is assumed.")])
    ex.choice("The star is on the main sequence. What process in its core releases its energy?",
              "Fusion of hydrogen to form helium.",
              [("Fission of helium to form hydrogen.", "Stars release energy by fusion."),
               ("Fusion of helium to form carbon.", "That happens after the main sequence."),
               ("Burning hydrogen in oxygen.", "This is nuclear, not chemical.")])
    ex.choice("The star is more massive than the Sun. How does its main sequence lifetime compare with the Sun's?",
              "It is shorter, because it fuses its hydrogen at a greater rate.",
              [("It is longer, because it has more fuel.", "The rate of fusion is much greater."),
               ("It is the same.", "Lifetime depends on mass."),
               ("It is longer, because it is hotter.", "A hotter core uses fuel faster.")])
    return ex.build(f"A main sequence star has a radius of {fmt(r)} m and a surface temperature of {Tk} K.")


def _red_giant(level=LEVEL):
    ex = _exam()
    Tk, k = pick(3400, 3700, 4100, 4500), pick(220, 380, 520, 900)
    L_ = sig(k * 3.83e26 * pick(1.0, 2.5, 6.0))
    pa = SIGMA * Tk**4
    r = math.sqrt(L_ / (4 * math.pi * sig(pa)))
    d_au = r / AU
    ex.on(_STAR).num("Calculate the power radiated per unit area of the star's surface.", pa, "W m⁻²",
                     wrong=[(SIGMA * Tk, "T is raised to the power 4.")],
                     working=[r"\frac{P}{A} = \sigma T^4", rf"\frac{{P}}{{A}} = {ltx(pa)}\ \mathrm{{W\,m^{{-2}}}}"])
    ex.num("Calculate the radius of the star.", r, "m",
           wrong=[(r**2, "That is r² — take the square root.")],
           working=[r"L = 4\pi r^2 \times \frac{P}{A}", rf"r = {ltx(r)}\ \mathrm{{m}}"])
    ex.num("Express this radius in astronomical units.", sig(r) / AU, "AU",
           working=[rf"\frac{{{ltx(r)}}}{{1.5 \times 10^{{11}}}} = {ltx(d_au)}\ \mathrm{{AU}}"])
    ex.choice("Where would this cool, very luminous star lie on a Hertzsprung–Russell diagram?",
              "Above and to the right of the main sequence.",
              [("Below and to the left of the main sequence.", "That is the white dwarf region."),
               ("At the top left end of the main sequence.", "That is for hot stars."),
               ("At the bottom right end of the main sequence.", "Those stars have low luminosity.")])
    ex.on(_GR).choice("A very massive star may eventually form a black hole. What is meant by its Schwarzschild radius?",
                      "The distance from the singularity to the event horizon.",
                      [("The radius of the singularity.", "It is the distance out to the event horizon."),
                       ("The radius of the star just before it collapses.", "It is a property of the black hole."),
                       ("The distance beyond which gravity is zero.", "Gravity extends beyond it.")])
    return ex.build(f"A star has a surface temperature of {Tk} K and a luminosity of {fmt(L_)} W.")


SCENARIOS = {
    "Car on a Test Track": _test_car,
    "Cyclist and Bend": _cyclist_bend,
    "Spin Drier": _spin_drier,
    "Playground Roundabout": _roundabout,
    "Flywheel Experiment": _flywheel,
    "Satellite in Orbit": _satellite,
    "Probe to a Moon": _moon_probe,
    "Black Hole Binary": _black_hole,
    "Main Sequence Star": _nearby_star,
    "Cool Luminous Star": _red_giant,
}
