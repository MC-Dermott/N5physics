"""AH — Rotational dynamics: moment of inertia, torque, angular momentum and rotational Ek."""
import math
import random

from topics.rotational_motion.common_ah import L, T, calc, explain_set, ltx, pick_sig, sig, uni

QT = "Rotational Dynamics"

NOTES = r"""
## Rotational dynamics

$$I = \sum mr^2 \qquad \tau = Fr \qquad \tau = I\alpha \qquad L = mvr = mr^2\omega \qquad L = I\omega$$

$$E_{k(rotational)} = \tfrac{1}{2}I\omega^2 \qquad E_P = E_{k(translational)} + E_{k(rotational)}$$

| Shape | Moment of inertia (on the relationships sheet) |
|---|---|
| Rod about its centre | $I = \frac{1}{12}ml^2$ |
| Rod about its end | $I = \frac{1}{3}ml^2$ |
| Disc about its centre | $I = \frac{1}{2}mr^2$ |
| Sphere about its centre | $I = \frac{2}{5}mr^2$ |

- **Moment of inertia** is a measure of an object's resistance to angular acceleration about a given axis.
  It depends on the mass **and** how the mass is distributed about the axis.
- F in τ = Fr is the force **perpendicular** to the radius. With friction, the **unbalanced** torque is
  applied torque − frictional torque.
- **Conservation of angular momentum:** the total angular momentum before an interaction is equal to the
  total angular momentum after it, **in the absence of net external torques**.
"""

_SHAPES = [
    ("a solid disc of mass {m:g} kg and radius {x:g} m about an axis through its centre", "radius", 1 / 2,
     r"I = \tfrac{1}{2}mr^2"),
    ("a solid sphere of mass {m:g} kg and radius {x:g} m about an axis through its centre", "radius", 2 / 5,
     r"I = \tfrac{2}{5}mr^2"),
    ("a uniform rod of mass {m:g} kg and length {x:g} m about an axis through its centre", "length", 1 / 12,
     r"I = \tfrac{1}{12}ml^2"),
    ("a uniform rod of mass {m:g} kg and length {x:g} m about an axis through one end", "length", 1 / 3,
     r"I = \tfrac{1}{3}ml^2"),
]


def gen_moment_of_inertia(level="AH"):
    m, x = uni(0.50, 8.0), uni(0.12, 0.90, 2)
    if random.random() < 0.65:
        desc, what, k, rel = random.choice(_SHAPES)
        I = k * m * x**2
        wrong = [(k * m * x, f"The {what} must be squared."),
                 (m * x**2, "That treats the whole mass as being at one distance. Use the relationship for this shape.")]
        if what == "radius":
            wrong.append((k * m * (x / 2)**2, "Don't halve the radius — it is already a radius."))
        return calc(QT, f"Calculate the moment of inertia of {desc.format(m=m, x=x)}.", I, "kg m²",
                    [rel, rf"I = {ltx(k)} \times {m:g} \times {x:g}^2 = {ltx(I)}\ \mathrm{{kg\,m^2}}"],
                    wrong=wrong, notes=NOTES)
    mr, R = uni(0.40, 2.0), uni(0.20, 0.60, 2)
    n, mp, rp = random.randint(2, 4), uni(0.05, 0.40, 2), uni(0.10, 0.19, 2)
    I_disc = 0.5 * mr * R**2
    I_pts = n * mp * rp**2
    I = I_disc + I_pts
    return calc(QT, f"A turntable is a uniform disc of mass {mr:g} kg and radius {R:g} m. {n} small objects, "
                    f"each of mass {mp:g} kg, are fixed to it {rp:g} m from the central axis. Calculate the total "
                    f"moment of inertia about this axis.", I, "kg m²",
                [rf"I_{{disc}} = \tfrac{{1}}{{2}}mr^2 = {ltx(I_disc)}\ \mathrm{{kg\,m^2}}",
                 rf"I_{{objects}} = \sum mr^2 = {n} \times {mp:g} \times {rp:g}^2 = {ltx(I_pts)}\ \mathrm{{kg\,m^2}}",
                 rf"I = {ltx(I)}\ \mathrm{{kg\,m^2}}"],
                wrong=[(I_disc + mp * rp**2, f"There are {n} objects — add I for each one."),
                       (I_disc, "Include the moment of inertia of the added objects.")],
                scaffold=[("What is I for the disc?", I_disc, "kg m²"), ("What is I for all the objects?", I_pts, "kg m²"),
                          ("What is the total I?", I, "kg m²")], notes=NOTES)


def gen_torque(level="AH"):
    M, r = uni(2.0, 12.0), uni(0.15, 0.50, 2)
    I = sig(0.5 * M * r**2, 3)
    F = pick_sig(5.0, 40.0)
    tau = F * r
    kind = random.choice(["alpha", "friction", "frictional_torque", "time"])
    base = f"A force of {F:g} N is applied tangentially to the rim of a wheel of radius {r:g} m and moment of inertia {I:g} kg m². "
    if kind == "alpha":
        a = tau / I
        return calc(QT, base + "Friction is negligible. Calculate the angular acceleration of the wheel.", a, "rad s⁻²",
                    [r"\tau = Fr", rf"\tau = {F:g} \times {r:g} = {ltx(tau)}\ \mathrm{{N\,m}}",
                     r"\tau = I\alpha", rf"\alpha = {ltx(a)}\ \mathrm{{rad\,s^{{-2}}}}"],
                    wrong=[(F / I, "F is a force, not a torque. Find τ = Fr first."), (F / M, "Use τ = Iα, not F = ma.")],
                    scaffold=[("What is the torque?", tau, "N m"), ("What is α?", a, "rad s⁻²")], notes=NOTES)
    tf = sig(tau * uni(0.10, 0.45, 2), 2)
    a = (tau - tf) / I
    if kind == "friction":
        return calc(QT, base + f"A frictional torque of {tf:g} N m acts. Calculate the angular acceleration.", a, "rad s⁻²",
                    [rf"\tau_{{un}} = Fr - \tau_f = {ltx(tau)} - {tf:g} = {ltx(tau - tf)}\ \mathrm{{N\,m}}",
                     r"\tau = I\alpha", rf"\alpha = {ltx(a)}\ \mathrm{{rad\,s^{{-2}}}}"],
                    wrong=[(tau / I, "Subtract the frictional torque to get the unbalanced torque."),
                           ((tau + tf) / I, "Friction opposes the motion — subtract it.")],
                    scaffold=[("What is the applied torque?", tau, "N m"), ("What is the unbalanced torque?", tau - tf, "N m"),
                              ("What is α?", a, "rad s⁻²")], notes=NOTES)
    if kind == "frictional_torque":
        a_m = sig(a, 2)
        tf_ans = tau - I * a_m
        return calc(QT, base + f"The measured angular acceleration is {a_m:g} rad s⁻². Calculate the frictional torque.",
                    tf_ans, "N m",
                    [rf"\tau_{{un}} = I\alpha = {I:g} \times {a_m:g} = {ltx(I*a_m)}\ \mathrm{{N\,m}}",
                     rf"\tau_f = Fr - \tau_{{un}} = {ltx(tf_ans)}\ \mathrm{{N\,m}}"],
                    wrong=[(I * a_m, "That is the unbalanced torque. Subtract it from the applied torque Fr."),
                           (tau, "That is the applied torque.")],
                    scaffold=[("What is the applied torque?", tau, "N m"), ("What is the unbalanced torque?", I * a_m, "N m"),
                              ("What is the frictional torque?", tf_ans, "N m")], notes=NOTES)
    w1 = pick_sig(10.0, 50.0)
    t = w1 / a
    return calc(QT, base + f"A frictional torque of {tf:g} N m acts. The wheel starts from rest. Calculate the time "
                           f"taken to reach {w1:g} rad s⁻¹.", t, "s",
                [rf"Fr - \tau_f = I\alpha \qquad \alpha = {ltx(a)}\ \mathrm{{rad\,s^{{-2}}}}",
                 r"\omega = \omega_o + \alpha t", rf"t = {ltx(t)}\ \mathrm{{s}}"],
                wrong=[(w1 * I / tau, "Friction was left out of the unbalanced torque.")],
                scaffold=[("What is α?", a, "rad s⁻²"), ("What is the time?", t, "s")], notes=NOTES)


def gen_angular_momentum(level="AH"):
    I1 = uni(0.040, 0.250, 3)
    w1 = pick_sig(4.0, 15.0)
    kind = random.choice(["clay", "disc", "skater", "point"])
    if kind == "point":
        m, v, r = uni(0.020, 0.200, 3), pick_sig(2.0, 12.0), uni(0.20, 0.90, 2)
        Lm = m * v * r
        return calc(QT, f"A {m:g} kg ball moves at {v:g} m s⁻¹ along a line which passes {r:g} m from a pivot. "
                        f"Calculate the angular momentum of the ball about the pivot.", Lm, "kg m² s⁻¹",
                    [r"L = mvr", rf"L = {m:g} \times {v:g} \times {r:g} = {ltx(Lm)}\ \mathrm{{kg\,m^2\,s^{{-1}}}}"],
                    wrong=[(m * v, "That is the linear momentum."), (m * v * r**2, "L = mvr — r is not squared here.")],
                    notes=NOTES)
    if kind == "clay":
        m, r = uni(0.050, 0.300, 3), uni(0.15, 0.40, 2)
        I2 = I1 + m * r**2
        w2 = I1 * w1 / I2
        return calc(QT, f"A turntable of moment of inertia {I1:g} kg m² rotates freely at {w1:g} rad s⁻¹. A "
                        f"{m:g} kg piece of clay is dropped vertically and sticks {r:g} m from the axis. Calculate "
                        f"the angular velocity immediately afterwards.", w2, "rad s⁻¹",
                    [rf"I_{{clay}} = mr^2 = {ltx(m*r**2)}\ \mathrm{{kg\,m^2}}", r"I_1\omega_1 = (I_1 + mr^2)\omega_2",
                     rf"{I1:g} \times {w1:g} = {ltx(I2)} \times \omega_2",
                     rf"\omega_2 = {ltx(w2)}\ \mathrm{{rad\,s^{{-1}}}}"],
                    wrong=[(I1 * w1 / (I1 + m), "The clay's moment of inertia is mr², not m."),
                           (I1 * w1 / (m * r**2), "The turntable is still rotating — add both moments of inertia."),
                           (w1 * math.sqrt(I1 / I2), "Angular momentum is conserved, not rotational kinetic energy: the collision is inelastic.")],
                    scaffold=[("What is the total angular momentum before?", I1 * w1, "kg m² s⁻¹"),
                              ("What is the total moment of inertia after?", I2, "kg m²"),
                              ("What is the final angular velocity?", w2, "rad s⁻¹")], notes=NOTES)
    if kind == "disc":
        I2 = uni(0.020, 0.150, 3)
        w2 = I1 * w1 / (I1 + I2)
        return calc(QT, f"A disc of moment of inertia {I1:g} kg m² rotates at {w1:g} rad s⁻¹. A second, stationary "
                        f"disc of moment of inertia {I2:g} kg m² is lowered onto it on the same axis and they rotate "
                        f"together. No external torque acts. Calculate the final angular velocity.", w2, "rad s⁻¹",
                    [r"I_1\omega_1 = (I_1 + I_2)\omega_2", rf"\omega_2 = {ltx(w2)}\ \mathrm{{rad\,s^{{-1}}}}"],
                    wrong=[(I1 * w1 / I2, "Both discs rotate afterwards."), (w1 / 2, "Only true if the moments of inertia are equal.")],
                    notes=NOTES)
    I_in, I_out = uni(0.8, 1.6), uni(2.2, 4.5)
    w2 = I_out * w1 / I_in
    return calc(QT, f"A skater spins at {w1:g} rad s⁻¹ with arms outstretched, moment of inertia {I_out:g} kg m². "
                    f"The skater pulls in their arms and the moment of inertia becomes {I_in:g} kg m². Calculate "
                    f"the new angular velocity.", w2, "rad s⁻¹",
                [r"I_1\omega_1 = I_2\omega_2", rf"{I_out:g} \times {w1:g} = {I_in:g} \times \omega_2",
                 rf"\omega_2 = {ltx(w2)}\ \mathrm{{rad\,s^{{-1}}}}"],
                wrong=[(I_in * w1 / I_out, "A smaller moment of inertia gives a larger angular velocity.")], notes=NOTES)


def gen_rotational_energy(level="AH"):
    kind = random.choice(["ek", "rolling", "falling"])
    if kind == "ek":
        I, w = uni(0.050, 0.600, 3), pick_sig(8.0, 60.0)
        E = 0.5 * I * w**2
        return calc(QT, f"A flywheel of moment of inertia {I:g} kg m² rotates at {w:g} rad s⁻¹. Calculate its "
                        f"rotational kinetic energy.", E, "J",
                    [r"E_k = \tfrac{1}{2}I\omega^2", rf"E_k = 0.5 \times {I:g} \times {w:g}^2 = {ltx(E)}\ \mathrm{{J}}"],
                    wrong=[(0.5 * I * w, "ω must be squared."), (I * w**2, "Don't forget the ½.")], notes=NOTES)
    if kind == "rolling":
        name, k, frac = random.choice([("solid sphere", 2 / 5, r"\tfrac{2}{5}"), ("solid cylinder", 1 / 2, r"\tfrac{1}{2}"),
                                       ("thin hoop", 1.0, "1")])
        m, h, r = uni(0.20, 2.0, 2), uni(0.20, 1.20, 2), uni(0.030, 0.120, 3)
        I = k * m * r**2
        v = math.sqrt(2 * 9.8 * h / (1 + k))
        return calc(QT, f"A {name} of mass {m:g} kg, radius {r:g} m and moment of inertia {sig(I):g} kg m² starts "
                        f"from rest and rolls without slipping down a slope through a vertical height of {h:g} m. "
                        f"Calculate its speed at the bottom.", v, "m s⁻¹",
                    [r"mgh = \tfrac{1}{2}mv^2 + \tfrac{1}{2}I\omega^2 \qquad \omega = \frac{v}{r}",
                     rf"{ltx(m*9.8*h)} = {ltx(0.5*m*(1+k))}\,v^2", rf"v = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(math.sqrt(2 * 9.8 * h), "Some of the potential energy becomes rotational kinetic energy."),
                           (math.sqrt(2 * 9.8 * h / k), "Include the translational kinetic energy too.")],
                    scaffold=[("What is the potential energy lost?", m * 9.8 * h, "J"),
                              ("What is the speed at the bottom?", v, "m s⁻¹")], notes=NOTES)
    m, r = uni(0.10, 0.80, 2), uni(0.050, 0.200, 3)
    I = sig(uni(0.5, 3.0) * m * r**2, 2)
    h = uni(0.40, 1.60, 2)
    v = math.sqrt(2 * m * 9.8 * h / (m + I / r**2))
    w = v / r
    return calc(QT, f"A {m:g} kg mass hangs from a light string wrapped round a pulley of radius {r:g} m and moment "
                    f"of inertia {I:g} kg m². The mass is released from rest and falls {h:g} m. Friction is "
                    f"negligible. Calculate the angular velocity of the pulley at this instant.", w, "rad s⁻¹",
                [r"mgh = \tfrac{1}{2}mv^2 + \tfrac{1}{2}I\omega^2 \qquad v = r\omega",
                 rf"{ltx(m*9.8*h)} = {ltx(0.5*(m*r**2 + I))}\,\omega^2", rf"\omega = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"],
                wrong=[(math.sqrt(2 * m * 9.8 * h / I), "The falling mass also has kinetic energy."),
                       (v, "That is the speed of the mass. ω = v/r.")],
                scaffold=[("What is the potential energy lost?", m * 9.8 * h, "J"),
                          ("What is the angular velocity?", w, "rad s⁻¹")], notes=NOTES)


_EXPLAIN = [
    ("A solid disc and a thin hoop of the same mass and radius are released together at the top of a slope and "
     "roll without slipping. Which reaches the bottom first, and why?",
     "The disc: it has the smaller moment of inertia, so less of the energy becomes rotational and its speed is greater.",
     [("The hoop: it has the larger moment of inertia, so it gains more speed.", "A larger I takes a larger share of the energy as rotation."),
      ("They arrive together, because they have the same mass and lose the same potential energy.",
       "The same energy is shared differently between translation and rotation."),
      ("The hoop: its mass is further from the axis, so the torque on it is greater.", "The torque is not what is larger — I is.")],
     "Same Ep lost. The hoop's mass is all at radius r, so its I is larger and its translational Ek is smaller."),
    ("A skater spinning on ice pulls in their arms and spins faster. Which explains this?",
     "No external torque acts, so L = Iω is constant; I decreases, so ω increases.",
     [("Rotational kinetic energy is conserved; I decreases, so ω increases.", "The skater does work pulling in their arms, so Ek increases."),
      ("Pulling in the arms applies an external torque which increases ω.", "The force is internal to the skater."),
      ("The skater's mass decreases, so ω increases.", "The mass is unchanged; its distribution changes.")],
     "State what is conserved, the condition, and the relationship."),
    ("A small block is dropped vertically on to a freely rotating turntable and sticks to it. A second trial uses "
     "an identical block placed further from the axis. How does the final angular velocity compare with the first trial?",
     "It is less, because the moment of inertia of the system is greater and angular momentum is conserved.",
     [("It is less, because the mass of the system is greater.",
       "The mass is the same in both trials. The justification must be in terms of moment of inertia."),
      ("It is greater, because the block has a larger tangential speed.",
       "The block arrives with no angular momentum about the axis."),
      ("It is the same, because the same block is used.", "I = mr² depends on the distance from the axis.")],
     "Same L before. A larger r gives a larger I, so ω is smaller."),
    ("A force is applied tangentially to a flywheel. The same force is then applied at a greater distance from "
     "the axis of rotation. Why is the angular acceleration greater?",
     "The torque is greater (τ = Fr) and the moment of inertia is unchanged, so α = τ/I is greater.",
     [("The moment of inertia is smaller further from the axis.", "Moving the force does not change the mass distribution."),
      ("The force is greater further from the axis.", "The force is the same; the torque changes."),
      ("The tangential speed is greater further from the axis.", "That does not explain the change in angular acceleration.")],
     "Give the distance from the axis of rotation, τ = Fr, then τ = Iα."),
    ("The same unbalanced torque is applied to two wheels of equal mass. Wheel X has its mass concentrated at the "
     "rim; wheel Y has its mass near the axle. How do their angular accelerations compare?",
     "Y's is greater: its mass is closer to the axis, so I is smaller and α = τ/I is larger.",
     [("X's is greater: its mass is further out, so I is smaller.", "Mass further from the axis gives a larger I."),
      ("They are equal, because the masses and torques are equal.", "I depends on how the mass is distributed."),
      ("X's is greater: the rim has a larger tangential speed.", "Tangential speed does not set α.")],
     "τ = Iα with τ constant."),
    ("A tangential force accelerates a wheel against a constant frictional torque. The applied force is then removed. "
     "Which describes the motion?",
     "The frictional torque is now the unbalanced torque, so the wheel has a constant angular deceleration until it stops.",
     [("The wheel stops immediately.", "It has angular momentum, which takes time to be removed."),
      ("The wheel continues at constant angular velocity.", "A frictional torque still acts."),
      ("The angular deceleration increases as the wheel slows.", "The frictional torque is constant, so α is constant.")],
     "An unbalanced torque changes the angular motion: α = τ/I."),
]
gen_rotation_explain = explain_set(QT, _EXPLAIN, NOTES)
