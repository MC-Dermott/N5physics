"""AH — Angular motion and centripetal force."""
import math
import random

from topics.rotational_motion.common_ah import L, T, calc, explain_set, fmt, ltx, pick_sig, sig, uni

QT = "Angular Motion"
QT_C = "Centripetal Force"

NOTES = r"""
## Angular motion

$$\omega = \frac{d\theta}{dt} \qquad \alpha = \frac{d\omega}{dt} = \frac{d^2\theta}{dt^2} \qquad
\omega = \frac{2\pi}{T} \qquad \omega = 2\pi f$$

$$\omega = \omega_o + \alpha t \qquad \omega^2 = \omega_o^2 + 2\alpha\theta \qquad
\theta = \omega_o t + \tfrac{1}{2}\alpha t^2$$

$$s = r\theta \qquad v = r\omega \qquad a_t = r\alpha$$

- Angles are in **radians**: 1 revolution = 2π rad = 360°.
- Revolutions per minute → rad s⁻¹: multiply by 2π, then divide by 60.
- The angular equations of motion apply only when **α is constant**.
"""

NOTES_C = r"""
## Centripetal force

$$a_r = \frac{v^2}{r} = r\omega^2 \qquad F = \frac{mv^2}{r} = mr\omega^2$$

- A **central (centripetal) force**, directed towards the centre, is needed to keep an object in
  circular motion. It causes the centripetal (radial) acceleration.
- It is not an extra force: it is provided by tension, friction, gravity, a reaction force or
  a component of these.
- Vertical circle: at the **top**, weight + tension (or reaction) = mv²/r. At the **bottom**,
  tension − weight = mv²/r. At the minimum speed at the top, the tension is zero.
- If the central force is removed, the object moves off **along the tangent**.
"""


def gen_radians_speed(level="AH"):
    rpm = random.randrange(120, 1500, 15)
    w = rpm * 2 * math.pi / 60
    kind = random.choice(["omega", "period", "theta"])
    if kind == "omega":
        return calc(QT, f"A drum rotates at {rpm} revolutions per minute. Calculate its angular velocity.",
                    w, "rad s⁻¹",
                    [r"\omega = 2\pi f", rf"\omega = 2\pi \times \frac{{{rpm}}}{{60}} = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"],
                    wrong=[(rpm / 60, "That is the frequency in revolutions per second. Multiply by 2π."),
                           (rpm * 2 * math.pi, "Divide by 60 — the rate is per minute."),
                           (rpm * 6, "That is in degrees per second. Angular velocity is in rad s⁻¹.")],
                    scaffold=[("What is the number of revolutions per second?", rpm / 60, "Hz"),
                              ("What is ω?", w, "rad s⁻¹")], notes=NOTES)
    if kind == "period":
        T_ = pick_sig(0.30, 9.0)
        w = 2 * math.pi / T_
        return calc(QT, f"A turntable takes {T_:g} s to make one complete rotation. Calculate its angular velocity.",
                    w, "rad s⁻¹",
                    [r"\omega = \frac{2\pi}{T}", rf"\omega = \frac{{2\pi}}{{{T_:g}}} = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"],
                    wrong=[(1 / T_, "That is the frequency. ω = 2π/T."),
                           (360 / T_, "That is in degrees per second, not radians per second.")], notes=NOTES)
    r, deg = uni(0.20, 1.50, 2), random.randrange(40, 320, 5)
    s = r * math.radians(deg)
    return calc(QT, f"A point on a wheel of radius {r:g} m turns through an angle of {deg}°. "
                    f"Calculate the distance the point travels along its circular path.", s, "m",
                [rf"\theta = {deg} \times \frac{{2\pi}}{{360}} = {ltx(math.radians(deg))}\ \mathrm{{rad}}",
                 r"s = r\theta", rf"s = {r:g} \times {ltx(math.radians(deg))} = {ltx(s)}\ \mathrm{{m}}"],
                wrong=[(r * deg, "θ must be in radians in s = rθ.")],
                scaffold=[("What is the angle in radians?", math.radians(deg), "rad"),
                          ("What is the distance?", s, "m")], notes=NOTES)


def gen_angular_equations(level="AH"):
    w0 = pick_sig(2.0, 12.0)
    alpha = pick_sig(1.0, 6.0)
    t = pick_sig(2.0, 9.0)
    w = w0 + alpha * t
    theta = w0 * t + 0.5 * alpha * t**2
    kind = random.choice(["alpha", "theta", "omega", "revs"])
    if kind == "alpha":
        w1 = sig(w, 3)
        a = (w1 - w0) / t
        return calc(QT, f"A flywheel speeds up uniformly from {w0:g} rad s⁻¹ to {w1:g} rad s⁻¹ in {t:g} s. "
                        f"Calculate its angular acceleration.", a, "rad s⁻²",
                    [r"\omega = \omega_o + \alpha t", rf"{w1:g} = {w0:g} + \alpha \times {t:g}",
                     rf"\alpha = {ltx(a)}\ \mathrm{{rad\,s^{{-2}}}}"],
                    wrong=[(w1 / t, "Use the change in angular velocity, ω − ω₀.")], notes=NOTES)
    if kind == "theta":
        return calc(QT, f"A wheel rotating at {w0:g} rad s⁻¹ accelerates uniformly at {alpha:g} rad s⁻² "
                        f"for {t:g} s. Calculate the angular displacement in this time.", theta, "rad",
                    [r"\theta = \omega_o t + \tfrac{1}{2}\alpha t^2",
                     rf"\theta = {w0:g} \times {t:g} + 0.5 \times {alpha:g} \times {t:g}^2",
                     rf"\theta = {ltx(theta)}\ \mathrm{{rad}}"],
                    wrong=[(w * t, "That uses the final angular velocity for the whole time."),
                           (0.5 * alpha * t**2, "You left out ω₀t — the wheel was already rotating.")], notes=NOTES)
    if kind == "omega":
        th = pick_sig(10, 90)
        w_f = math.sqrt(w0**2 + 2 * alpha * th)
        return calc(QT, f"A rotor turning at {w0:g} rad s⁻¹ accelerates uniformly at {alpha:g} rad s⁻² "
                        f"while it turns through {th:g} rad. Calculate its final angular velocity.", w_f, "rad s⁻¹",
                    [r"\omega^2 = \omega_o^2 + 2\alpha\theta",
                     rf"\omega^2 = {w0:g}^2 + 2 \times {alpha:g} \times {th:g}",
                     rf"\omega = {ltx(w_f)}\ \mathrm{{rad\,s^{{-1}}}}"],
                    wrong=[(w0**2 + 2 * alpha * th, "That is ω² — take the square root.")], notes=NOTES)
    w_i = pick_sig(20, 90)
    time = pick_sig(5.0, 30.0)
    revs = w_i * time / 2 / (2 * math.pi)
    return calc(QT, f"A fan rotating at {w_i:g} rad s⁻¹ slows uniformly to rest in {time:g} s. "
                    f"Determine the number of revolutions it makes while stopping.", revs, "",
                [rf"\alpha = \frac{{0 - {w_i:g}}}{{{time:g}}} = {ltx(-w_i/time)}\ \mathrm{{rad\,s^{{-2}}}}",
                 r"\theta = \omega_o t + \tfrac{1}{2}\alpha t^2",
                 rf"\theta = {ltx(w_i*time/2)}\ \mathrm{{rad}}",
                 rf"\text{{revolutions}} = \frac{{\theta}}{{2\pi}} = {ltx(revs)}"],
                wrong=[(w_i * time / 2, "That is the angle in radians. Divide by 2π for revolutions."),
                       (w_i * time / (2 * math.pi), "The fan is slowing down, so it does not stay at its initial rate.")],
                scaffold=[("What is the angular displacement?", w_i * time / 2, "rad"),
                          ("How many revolutions is this?", revs)], notes=NOTES)


def gen_tangential(level="AH"):
    r = uni(0.15, 1.20, 2)
    kind = random.choice(["v", "at", "omega"])
    if kind == "v":
        T_ = pick_sig(0.40, 5.0)
        v = r * 2 * math.pi / T_
        return calc(QT, f"A point is {r:g} m from the axis of a disc that rotates once every {T_:g} s. "
                        f"Calculate the tangential speed of the point.", v, "m s⁻¹",
                    [rf"\omega = \frac{{2\pi}}{{T}} = {ltx(2*math.pi/T_)}\ \mathrm{{rad\,s^{{-1}}}}",
                     r"v = r\omega", rf"v = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(r / T_, "The point travels a circumference, 2πr, each period.")],
                    scaffold=[("What is ω?", 2 * math.pi / T_, "rad s⁻¹"), ("What is v?", v, "m s⁻¹")], notes=NOTES)
    if kind == "at":
        w1, t = pick_sig(8.0, 40.0), pick_sig(2.0, 9.0)
        at = r * w1 / t
        return calc(QT, f"A wheel of radius {r:g} m starts from rest and reaches {w1:g} rad s⁻¹ in {t:g} s "
                        f"with uniform angular acceleration. Calculate the tangential acceleration of a point "
                        f"on the rim.", at, "m s⁻²",
                    [rf"\alpha = \frac{{\omega - \omega_o}}{{t}} = {ltx(w1/t)}\ \mathrm{{rad\,s^{{-2}}}}",
                     r"a_t = r\alpha", rf"a_t = {ltx(at)}\ \mathrm{{m\,s^{{-2}}}}"],
                    wrong=[(w1 / t, "That is the angular acceleration. aₜ = rα."),
                           (r * w1**2, "That is the radial acceleration at the final speed, not the tangential one.")],
                    scaffold=[("What is α?", w1 / t, "rad s⁻²"), ("What is aₜ?", at, "m s⁻²")], notes=NOTES)
    v = pick_sig(2.0, 25.0)
    return calc(QT, f"A point on the rim of a wheel of radius {r:g} m moves at {v:g} m s⁻¹. "
                    f"Calculate the angular velocity of the wheel.", v / r, "rad s⁻¹",
                [r"v = r\omega", rf"{v:g} = {r:g} \times \omega",
                 rf"\omega = {ltx(v/r)}\ \mathrm{{rad\,s^{{-1}}}}"],
                wrong=[(v * r, "Divide v by r."), (v / (2 * r), "Use the radius, not the diameter.")], notes=NOTES)


def gen_centripetal_calc(level="AH"):
    m, r = uni(0.20, 2.50, 2), uni(0.30, 1.80, 2)
    v = pick_sig(2.0, 12.0)
    kind = random.choice(["force", "force_omega", "speed", "accel"])
    if kind == "force":
        F = m * v**2 / r
        return calc(QT_C, f"A {m:g} kg mass moves at a constant {v:g} m s⁻¹ in a horizontal circle of radius "
                          f"{r:g} m. Calculate the centripetal force on it.", F, "N",
                    [r"F = \frac{mv^2}{r}", rf"F = \frac{{{m:g} \times {v:g}^2}}{{{r:g}}} = {ltx(F)}\ \mathrm{{N}}"],
                    wrong=[(m * v / r, "v must be squared."), (m * v**2 * r, "Divide by r.")], notes=NOTES_C)
    if kind == "force_omega":
        w = pick_sig(3.0, 20.0)
        F = m * r * w**2
        return calc(QT_C, f"A {m:g} kg mass rotates at {w:g} rad s⁻¹ in a circle of radius {r:g} m. "
                          f"Calculate the centripetal force on it.", F, "N",
                    [r"F = mr\omega^2", rf"F = {m:g} \times {r:g} \times {w:g}^2 = {ltx(F)}\ \mathrm{{N}}"],
                    wrong=[(m * r * w, "ω must be squared.")], notes=NOTES_C)
    if kind == "speed":
        F = sig(m * v**2 / r, 2)
        ans = math.sqrt(F * r / m)
        return calc(QT_C, f"The centripetal force on a {m:g} kg mass moving in a circle of radius {r:g} m "
                          f"is {fmt(F, 2)} N. Calculate the speed of the mass.", ans, "m s⁻¹",
                    [r"F = \frac{mv^2}{r}", rf"{ltx(F, 2)} = \frac{{{m:g} \times v^2}}{{{r:g}}}",
                     rf"v = {ltx(ans)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(F * r / m, "That is v² — take the square root.")], notes=NOTES_C)
    w = pick_sig(3.0, 20.0)
    a = r * w**2
    return calc(QT_C, f"A point moves in a circle of radius {r:g} m with angular velocity {w:g} rad s⁻¹. "
                      f"Calculate its radial acceleration.", a, "m s⁻²",
                [r"a_r = r\omega^2", rf"a_r = {r:g} \times {w:g}^2 = {ltx(a)}\ \mathrm{{m\,s^{{-2}}}}"],
                wrong=[(r * w, "That is the tangential speed. aᵣ = rω².")], notes=NOTES_C)


def gen_vertical_circle(level="AH"):
    m, r = uni(0.20, 1.50, 2), uni(0.40, 1.50, 2)
    kind = random.choice(["min_speed", "top", "bottom", "min_omega"])
    if kind == "min_speed":
        v = math.sqrt(9.8 * r)
        return calc(QT_C, f"A ball on a light string is swung in a vertical circle of radius {r:g} m. "
                          f"Calculate the minimum speed at the top of the circle for the string to stay taut.",
                    v, "m s⁻¹",
                    [T("At the minimum speed the tension is zero, so the weight provides the centripetal force."),
                     r"mg = \frac{mv^2}{r}", rf"v = \sqrt{{gr}} = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(9.8 * r, "That is v² — take the square root."), (0.0, "At zero speed the string would go slack.")],
                    notes=NOTES_C)
    if kind == "min_omega":
        w = math.sqrt(9.8 / r)
        return calc(QT_C, f"A bucket of water is swung in a vertical circle of radius {r:g} m. Calculate the "
                          f"minimum angular velocity at which the water stays in the bucket at the top.", w, "rad s⁻¹",
                    [r"mg = mr\omega^2", rf"\omega = \sqrt{{\frac{{9.8}}{{{r:g}}}}} = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"],
                    wrong=[(9.8 / r, "That is ω² — take the square root."),
                           (math.sqrt(9.8 * r), "That is the minimum speed v. The question asks for ω.")], notes=NOTES_C)
    v = pick_sig(math.sqrt(9.8 * r) * 1.3, math.sqrt(9.8 * r) * 2.5, 2)
    Fc, W = m * v**2 / r, m * 9.8
    where = "top" if kind == "top" else "bottom"
    ten = Fc - W if kind == "top" else Fc + W
    rel = r"T + mg = \frac{mv^2}{r}" if kind == "top" else r"T - mg = \frac{mv^2}{r}"
    return calc(QT_C, f"A {m:g} kg mass on a string moves in a vertical circle of radius {r:g} m. Its speed at "
                      f"the {where} of the circle is {v:g} m s⁻¹. Calculate the tension in the string there.",
                ten, "N",
                [rel, rf"\frac{{mv^2}}{{r}} = {ltx(Fc)}\ \mathrm{{N}} \qquad mg = {ltx(W)}\ \mathrm{{N}}",
                 rf"T = {ltx(ten)}\ \mathrm{{N}}"],
                wrong=[(Fc, "That is the total central force. The weight also acts."),
                       (Fc + W if kind == "top" else Fc - W,
                        "Check the direction of the weight compared with the centre of the circle.")],
                scaffold=[("What central force is needed?", Fc, "N"), ("What is the weight?", W, "N"),
                          ("What is the tension?", ten, "N")], notes=NOTES_C)


_EXPLAIN_C = [
    ("A mass on a string moves in a horizontal circle. The string suddenly breaks. Which describes the "
     "initial motion of the mass, seen from above?",
     "It moves in a straight line along the tangent to the circle.",
     [("It moves radially outwards, away from the centre.", "There is no outward force on the mass."),
      ("It carries on in a circle for a short time.", "Circular motion needs a central force."),
      ("It moves towards the centre of the circle.", "The only force towards the centre has gone.")],
     "With no central force there is no horizontal unbalanced force, so it keeps its velocity, which is tangential."),
    ("A car travels round a level bend at constant speed. Why is the car accelerating?",
     "Its direction, and so its velocity, is changing; there is an unbalanced force towards the centre.",
     [("It is not accelerating, because its speed is constant.", "Velocity is a vector — direction matters."),
      ("An unbalanced force acts outwards, away from the centre.", "The unbalanced force is towards the centre."),
      ("The engine force is greater than friction, so the speed increases.", "The speed is constant.")],
     "Acceleration is the rate of change of velocity. Friction provides the central force."),
    ("A car goes round a level bend. The road becomes icy. Why may the car now fail to follow the bend at "
     "the same speed?",
     "The maximum friction is less than the central force needed (mv²/r).",
     [("The centrifugal force on the car increases on ice.", "No outward force acts on the car."),
      ("The centripetal force overcomes the friction.",
       "This is a common wrong statement. The centripetal force is not a separate force: friction provides it."),
      ("The car's weight decreases, so it needs more friction.", "The weight does not change.")],
     "Friction provides the central force; if it cannot supply mv²/r the car moves in a path of larger radius."),
    ("Riders stand against the inside wall of a spinning drum with no floor, held up by friction. As the drum "
     "slows down they start to slide down the wall. Why?",
     "The friction from the wall no longer balances the rider's weight.",
     [("The centripetal force no longer balances the weight.",
       "The central force is horizontal, so it cannot balance the weight."),
      ("The centrifugal force pushing them into the wall disappears.", "No outward force acts on the riders."),
      ("Their weight increases as the drum slows.", "Weight does not change.")],
     "As ω falls, the central force from the wall (mrω²) falls, so the maximum friction falls below the weight. "
     "The answer must compare the vertical forces: friction and weight."),
    ("Two peas rest on a rotating plate, one further from the centre than the other. As the plate speeds up, "
     "why does the outer pea slide first?",
     "At the same ω the outer pea needs a greater central force (mrω²), and friction cannot provide it.",
     [("The centripetal force overcomes the friction on the outer pea.",
       "Friction provides the central force; it is insufficient for the force required."),
      ("The outer pea has a greater angular velocity.", "Both have the same angular velocity."),
      ("There is a greater outward force on the outer pea.", "No outward force acts on the peas.")],
     "The radius is greater, so the required central force is greater."),
    ("A fairground rider is at the bottom of a vertical loop. How does the reaction force from the seat "
     "compare with the rider's weight?",
     "It is greater than the weight, because the resultant force must point upwards, to the centre.",
     [("It equals the weight, because the rider is moving horizontally.", "The rider is accelerating upwards."),
      ("It is less than the weight, because the rider feels lighter.", "At the bottom the rider feels heavier."),
      ("It is zero, because the weight provides the central force.", "The weight acts away from the centre here.")],
     "R − mg = mv²/r, so R = mg + mv²/r."),
]
gen_centripetal_explain = explain_set(QT_C, _EXPLAIN_C, NOTES_C)
