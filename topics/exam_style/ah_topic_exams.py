"""Advanced Higher — single-topic exam-style questions, each modelled on an SQA AH question (named above
each one), with new numbers each time. They give every topic its own "Exam style" set and also join the
unit's exam-style pool.
"""
import math

from topics.exam_style.base import fmt, ltx, pick, sig
from topics.exam_style import ah_quanta_waves as qw, ah_rotational_astro as ra
from topics.rotational_motion.common_ah import AU, C, G, LEVEL, LIGHT_YEAR, M_EARTH, M_SUN, R_SUN, SIGMA, uni
from topics.quanta_waves.common_ah import H, E_CHARGE, M_P


def _wm(v):
    return {"type": "text", "content": v}


# ════ Kinematic relationships (2016 Q1) ════
def athlete(level=LEVEL):
    ex = ra._exam().on("Kinematic Relationships")
    a, b, t = uni(0.10, 0.40, 2), uni(1.2, 2.6), uni(2.5, 4.0)
    v, s, acc = a * t**2 + b * t, a * t**3 / 3 + b * t**2 / 2, 2 * a * t + b
    ex.num(f"Determine the speed of the athlete at t = {t:g} s.", v, "m s⁻¹",
           working=[rf"v = {a:g}({t:g})^2 + {b:g}({t:g}) = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num(f"Determine, using calculus methods, the distance travelled in this time.", s, "m",
           wrong=[(v * t / 2, "The acceleration is not constant — integrate."), (v * t, "Integrate v with respect to t.")],
           working=[rf"s = \int_0^{{{t:g}}} v\,dt = \left[{ltx(a/3)}t^3 + {ltx(b/2)}t^2\right] = {ltx(s)}\ \mathrm{{m}}"])
    ex.num(f"Determine the acceleration at t = {t:g} s.", acc, "m s⁻²",
           wrong=[(v / t, "Differentiate v.")], working=[rf"a = \frac{{dv}}{{dt}} = {ltx(acc)}\ \mathrm{{m\,s^{{-2}}}}"])
    return ex.build(f"For the first part of a race, an athlete's speed in m s⁻¹ is modelled by **v = {a:g}t² + {b:g}t**.")


# ════ Kinematic relationships (2022 Q1) ════
def car_gradient(level=LEVEL):
    ex = ra._exam().on("Kinematic Relationships")
    a, b, t = uni(0.080, 0.200, 3), uni(0.9, 2.0, 2), uni(8.0, 16.0)
    v = a * t**2 + b * t
    acc = 2 * a * t + b
    s = a * t**3 / 3 + b * t**2 / 2
    ex.num(f"Using calculus methods, determine the acceleration of the car at t = {t:g} s.", acc, "m s⁻²",
           wrong=[(v / t, "That is the average acceleration.")],
           working=[rf"a = \frac{{dv}}{{dt}} = 2({a:g})t + {b:g} = {ltx(acc)}\ \mathrm{{m\,s^{{-2}}}}"])
    ex.num("Using calculus methods, determine the displacement of the car at this time.", s, "m",
           wrong=[(v * t / 2, "This assumes constant acceleration.")],
           working=[rf"s = \int v\,dt = {ltx(a/3)}t^3 + {ltx(b/2)}t^2 = {ltx(s)}\ \mathrm{{m}}"])
    ex.choice("What does the gradient of the car's velocity–time graph represent?", "The instantaneous acceleration.",
              [("The displacement.", "That is the area under the graph."),
               ("The average velocity.", "A gradient is a rate of change."),
               ("The change in velocity.", "That is the area under an acceleration–time graph.")])
    return ex.build(f"A car accelerates from rest along a straight track. Its velocity in m s⁻¹ is **v = {a:g}t² + {b:g}t**.")


# ════ Angular motion (2020 Q2) ════
def flywheel_stop(level=LEVEL):
    ex = ra._exam().on("Angular Motion")
    r, v, t = uni(0.25, 0.45, 2), uni(5.0, 9.0), uni(4.0, 7.0)
    w = v / r
    ws = sig(w)
    alpha = -pick(0.3, 0.4, 0.5) * ws / t
    als = sig(alpha, 2)
    th = ws * t + 0.5 * als * t**2
    ex.num(f"A point on the rim has a tangential speed of {v:g} m s⁻¹. Calculate the angular velocity of the wheel.", w, "rad s⁻¹",
           wrong=[(v * r, "v = rω.")], working=[rf"\omega = \frac{{v}}{{r}} = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"])
    ex.num(f"The wheel then slows with angular acceleration {als:g} rad s⁻² for {t:g} s. Determine the number of revolutions it makes in this time.",
           th / (2 * math.pi), "", wrong=[(th, "Divide the angle by 2π.")],
           working=[rf"\theta = \omega_o t + \tfrac12\alpha t^2 = {ltx(th)}\ \mathrm{{rad}}", rf"\frac{{\theta}}{{2\pi}} = {ltx(th/(2*math.pi))}"],
           scaffold=[("What is the angular displacement?", th, "rad")])
    ex.choice("With a smaller angular deceleration over the same time, how would the number of revolutions compare, and why?",
              "Greater, because the smaller angular acceleration means a greater angular displacement in this time.",
              [("Smaller, because the wheel slows less.", "It stays fast for longer."),
               ("The same, because the time is the same.", "The angular displacement depends on α."),
               ("Greater, because there is less friction, with no need to mention α.", "The angular acceleration must be specified.")])
    return ex.build(f"A flywheel of radius {r:g} m is rotating.")


# ════ Angular motion (2025 Q2, 2024 Q3) ════
def drum_spin_up(level=LEVEL):
    ex = ra._exam().on("Angular Motion")
    al, t, r = uni(0.080, 0.200, 3), pick(24, 28, 34, 40), uni(2.5, 4.5)
    w = al * t
    th = 0.5 * al * t**2
    ex.num(f"Calculate the angular velocity of the drum after {t} s.", w, "rad s⁻¹",
           working=[rf"\omega = \omega_o + \alpha t = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"])
    ex.num("Calculate the angle turned through in this time.", th, "rad",
           wrong=[(w * t, "The drum starts from rest.")], working=[rf"\theta = \tfrac12\alpha t^2 = {ltx(th)}\ \mathrm{{rad}}"])
    ex.num(f"Calculate the tangential speed of a point on the wall, {r:g} m from the axis, at this time.", r * sig(w), "m s⁻¹",
           working=[rf"v = r\omega = {ltx(r*sig(w))}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num("Calculate the tangential acceleration of this point.", r * al, "m s⁻²",
           wrong=[(r * w**2, "That is the radial acceleration.")], working=[rf"a_t = r\alpha = {ltx(r*al)}\ \mathrm{{m\,s^{{-2}}}}"])
    return ex.build(f"The drum of a fairground ride starts from rest with a uniform angular acceleration of {al:g} rad s⁻².")


# ════ Centripetal force (2018 Q2) ════
def toy_car_track(level=LEVEL):
    ex = ra._exam().on("Centripetal Force")
    r, v, m = uni(1.4, 2.4), uni(2.8, 4.2), uni(0.30, 0.55, 2)
    ar = v**2 / r
    F = m * ar
    Fmax = sig(F * pick(0.8, 0.9), 2)
    R = uni(0.50, 0.90, 2)
    ex.choice("Why is the car accelerating although its speed is constant?", "Its direction, and so its velocity, is changing.",
              [("There is an unbalanced force outwards.", "No outward force acts."),
               ("The engine force is greater than friction.", "The speed is constant."),
               ("It is not accelerating.", "Velocity is a vector.")])
    ex.num("Calculate the radial acceleration of the car.", ar, "m s⁻²", wrong=[(v / r, "aᵣ = v²/r.")],
           working=[rf"a_r = \frac{{v^2}}{{r}} = {ltx(ar)}\ \mathrm{{m\,s^{{-2}}}}"])
    ex.num("Calculate the centripetal force required.", F, "N", working=[rf"F = ma_r = {ltx(F)}\ \mathrm{{N}}"])
    ex.choice(f"The maximum friction between the tyres and the track is {Fmax:g} N. What happens?",
              "The car leaves the circular path, because friction is insufficient to provide the central force needed.",
              [("The car stays on the track, because friction is less than the force needed.", "It needs at least the required force."),
               ("The car moves outwards because the centripetal force overcomes friction.", "Friction provides the central force."),
               ("The car moves towards the centre.", "There is too little force towards the centre.")])
    ex.num(f"The car then crosses a raised section of track that is part of a vertical circle of radius {R:g} m. "
           f"Calculate the greatest speed at which it stays in contact at the top.", math.sqrt(9.8 * R), "m s⁻¹",
           wrong=[(9.8 * R, "Take the square root.")],
           working=[r"mg = \frac{mv^2}{r}", rf"v = {ltx(math.sqrt(9.8*R))}\ \mathrm{{m\,s^{{-1}}}}"])
    return ex.build(f"A radio-controlled car of mass {m:g} kg travels at a constant {v:g} m s⁻¹ round a level circular track of radius {r:g} m.")


# ════ Centripetal force (2024 Q2, 2016 Q2: conical pendulum) ════
def conical_pendulum(level=LEVEL):
    ex = ra._exam().on("Centripetal Force")
    m, r, ang = uni(0.12, 0.40, 2), uni(0.30, 0.70, 2), pick(25, 30, 35, 40)
    W = m * 9.8
    F = W * math.tan(math.radians(ang))
    w = math.sqrt(F / (m * r))
    ten = W / math.cos(math.radians(ang))
    ex.choice("Which forces act on the object?", "Its weight and the tension in the string.",
              [("Its weight, the tension and a centripetal force.", "The central force is the horizontal component of tension, not an extra force."),
               ("Its weight, the tension and a centrifugal force.", "There is no centrifugal force."),
               ("Only the centripetal force.", "Weight and tension act.")])
    ex.num("Calculate the central force on the object.", F, "N", wrong=[(W / math.tan(math.radians(ang)), "Horizontal ÷ vertical = tan θ.")],
           working=[r"T\cos\theta = mg \qquad T\sin\theta = F", rf"F = mg\tan\theta = {ltx(F)}\ \mathrm{{N}}"])
    ex.num("Calculate the angular velocity of the object.", math.sqrt(sig(F) / (m * r)), "rad s⁻¹",
           wrong=[(F / (m * r), "That is ω².")], working=[r"F = mr\omega^2", rf"\omega = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"])
    ex.num("Calculate the tension in the string.", ten, "N", wrong=[(W * math.cos(math.radians(ang)), "T = mg ÷ cos θ.")],
           working=[rf"T = \frac{{mg}}{{\cos\theta}} = {ltx(ten)}\ \mathrm{{N}}"])
    return ex.build(f"An object of mass {m:g} kg on a string moves in a horizontal circle of radius {r:g} m, with the string at {ang}° to the vertical.")


# ════ Rotational dynamics (2023 Q3) ════
def ring_on_table(level=LEVEL):
    ex = ra._exam().on("Rotational Dynamics")
    F, al = pick(6.3e-3, 8.4e-3, 9.6e-3), uni(0.50, 0.90, 3)
    I = F / al
    w1, w2 = uni(6.5, 9.0, 2), uni(4.5, 6.0, 2)
    Is = sig(I)
    Ir = Is * (w1 - w2) / w2
    dE = 0.5 * Is * w1**2 - 0.5 * (Is + sig(Ir)) * w2**2
    ex.num(f"An unbalanced torque of {fmt(F)} N m gives the turntable an angular acceleration of {al:g} rad s⁻². Calculate its moment of inertia.",
           I, "kg m²", wrong=[(F * al, "I = τ ÷ α.")], working=[rf"\tau = I\alpha \qquad I = {ltx(I)}\ \mathrm{{kg\,m^2}}"])
    ex.num(f"Rotating freely at {w1:g} rad s⁻¹, it has a stationary ring dropped on to it. They rotate together at {w2:g} rad s⁻¹. Calculate the moment of inertia of the ring.",
           Ir, "kg m²", wrong=[(Is * w1 / w2, "That is the total; subtract the turntable's.")],
           working=[r"I_1\omega_1 = (I_1 + I_{ring})\omega_2", rf"I_{{ring}} = {ltx(Ir)}\ \mathrm{{kg\,m^2}}"])
    ex.num("Calculate the loss of rotational kinetic energy.", dE, "J",
           wrong=[(0.5 * Is * (w1 - w2)**2, "Subtract the energies, not the angular velocities.")],
           working=[rf"\Delta E_k = \tfrac12 I_1\omega_1^2 - \tfrac12(I_1+I_{{ring}})\omega_2^2 = {ltx(dE)}\ \mathrm{{J}}"])
    ex.choice("State the principle of conservation of angular momentum.",
              "Total angular momentum before equals total angular momentum after, in the absence of external torques.",
              [("Angular momentum is conserved.", "This scores nothing on its own."),
               ("Total angular momentum before equals total angular momentum after.", "The condition about external torques is missing."),
               ("Total rotational kinetic energy before equals that after, with no external torques.", "Kinetic energy is lost here.")])
    return ex.build("A student investigates the rotation of a turntable.")


# ════ Rotational dynamics (2019 Q3 rod; 2025 Q9 torque) ════
def gymnast(level=LEVEL):
    ex = ra._exam().on("Rotational Dynamics")
    m, l = pick(52, 58, 63, 70), uni(1.8, 2.3)
    I = m * l**2 / 3
    w = uni(1.5, 3.0)
    I2 = sig(I * pick(0.35, 0.45, 0.55), 2)
    w2 = sig(I) * w / I2
    ex.num("Show that the gymnast can be modelled as a rod rotating about one end: calculate the moment of inertia.", I, "kg m²",
           wrong=[(m * l**2 / 12, "The bar is at one end of the 'rod'.")], working=[rf"I = \tfrac13 ml^2 = {ltx(I)}\ \mathrm{{kg\,m^2}}"])
    ex.num(f"The straight gymnast rotates at {w:g} rad s⁻¹. Calculate the angular momentum.", sig(I) * w, "kg m² s⁻¹",
           working=[rf"L = I\omega = {ltx(sig(I)*w)}\ \mathrm{{kg\,m^2\,s^{{-1}}}}"])
    ex.num(f"The gymnast moves into a pike position with moment of inertia {I2:g} kg m². Ignoring external torques, calculate the new angular velocity.",
           w2, "rad s⁻¹", wrong=[(w * I2 / sig(I), "A smaller I gives a larger ω.")],
           working=[r"I_1\omega_1 = I_2\omega_2", rf"\omega_2 = {ltx(w2)}\ \mathrm{{rad\,s^{{-1}}}}"])
    ex.choice("Why does the pike position decrease the moment of inertia?", "The mass is distributed closer to the axis of rotation.",
              [("The gymnast's mass decreases.", "The mass is unchanged."),
               ("The gymnast's angular velocity increases.", "That is a result, not the cause."),
               ("The mass is lower down.", "It is the distance from the axis that matters.")])
    return ex.build(f"A gymnast of mass {m} kg and length (hands to feet) {l:g} m rotates in a straight position around a high bar.")


# ════ Gravitation (2017 Q4) ════
def asteroid_probe(level=LEVEL):
    ex = ra._exam().on("Gravitation")
    M, rad = uni(1.5, 3.5, 2) * 1e20, pick(2.1e5, 2.6e5, 3.1e5)
    h1, h2 = pick(3.8e5, 6.8e5), pick(1.5e6, 2.4e6)
    r1, r2, m = rad + h1, rad + h2, pick(750, 1240, 1600)
    T1 = 2 * math.pi * math.sqrt(r1**3 / (G * M))
    V1, V2 = -G * M / r1, -G * M / r2
    ex.num("Calculate the period of the probe in the lower orbit.", T1, "s",
           wrong=[(2 * math.pi * math.sqrt(h1**3 / (G * M)), "r is measured from the centre.")],
           working=[r"\frac{GMm}{r^2} = mr\left(\frac{2\pi}{T}\right)^2", rf"T = {ltx(T1)}\ \mathrm{{s}}"])
    ex.choice("What is meant by the gravitational potential of a point in space?", "The work done in moving unit mass from infinity to that point.",
              [("The work done in moving a mass from infinity to that point.", "It must be unit mass."),
               ("The work done in moving unit mass from that point to infinity.", "The direction is from infinity."),
               ("The force on unit mass at that point.", "That is field strength.")])
    ex.num("Calculate the gravitational potential at the radius of the lower orbit.", V1, "J kg⁻¹",
           wrong=[(-V1, "Potential is negative.")], working=[rf"V = -\frac{{GM}}{{r}} = {ltx(V1)}\ \mathrm{{J\,kg^{{-1}}}}"])
    ex.num(f"The probe, of mass {m} kg, moves to the higher orbit, of radius {fmt(r2)} m. Determine the change in its gravitational potential energy.",
           (V2 - V1) * m, "J", wrong=[((V1 - V2) * m, "Final minus initial.")],
           working=[rf"\Delta E_P = (V_2 - V_1)m = {ltx((V2-V1)*m)}\ \mathrm{{J}}"],
           scaffold=[("What is the potential at the higher orbit?", V2, "J kg⁻¹")])
    return ex.build(f"A space probe orbits an asteroid of mass {fmt(M)} kg in a circular orbit of radius {fmt(r1)} m.")


# ════ Gravitation (2023 Q4 escape velocity; 2025 Q4) ════
def mars_launch(level=LEVEL):
    ex = ra._exam().on("Gravitation")
    M, R = 6.42e23, 3.39e6
    h = pick(250, 400, 500, 800) * 1000
    r = R + h
    v = math.sqrt(2 * G * M / R)
    ex.num("Calculate the escape velocity from the surface of Mars.", v, "m s⁻¹", wrong=[(math.sqrt(G * M / R), "Include the factor of 2.")],
           working=[rf"v_{{esc}} = \sqrt{{\frac{{2GM}}{{r}}}} = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.choice(f"A vehicle is to reach an orbit {h//1000} km above the surface. Why does it not need to reach this escape velocity?",
              "The orbit is not at infinity: the vehicle is still in the gravitational field of Mars.",
              [("Mars has no atmosphere.", "This is not about the atmosphere."),
               ("Its mass is small, so its escape velocity is smaller.", "Escape velocity is independent of its mass."),
               ("The gravitational field is zero in orbit.", "The field provides the central force.")])
    ex.num("Calculate the orbital speed needed at this altitude.", math.sqrt(G * M / r), "m s⁻¹",
           wrong=[(math.sqrt(G * M / h), "r = R + h.")],
           working=[r"\frac{GMm}{r^2} = \frac{mv^2}{r}", rf"v = {ltx(math.sqrt(G*M/r))}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num("Calculate the gravitational field strength at this altitude.", G * M / r**2, "N kg⁻¹",
           wrong=[(G * M / R**2, "That is the value at the surface.")],
           working=[rf"g = \frac{{GM}}{{r^2}} = {ltx(G*M/r**2)}\ \mathrm{{N\,kg^{{-1}}}}"])
    return ex.build("Mars has a mass of 6.42 × 10²³ kg and a radius of 3.39 × 10⁶ m.")


# ════ General relativity (2016 Q5, 2026 Q5) ════
def accelerating_ship(level=LEVEL):
    ex = ra._exam().on("General Relativity")
    n = pick(18, 26, 33, 41)
    rs = 2 * G * n * M_SUN / C**2
    ex.choice("What is meant by the equivalence principle?",
              "It is not possible to distinguish between the effects on an observer of constant acceleration and a uniform gravitational field.",
              [("It is not possible to distinguish between constant velocity and a uniform gravitational field.", "It is acceleration."),
               ("Gravity and acceleration have the same units.", "It is about their effects on an observer."),
               ("Mass and energy are equivalent.", "That is a different idea.")])
    ex.choice("In a spacecraft accelerating in deep space, a ball is thrown across the cabin. What path does an astronaut see?",
              "A curve towards the rear of the spacecraft, as it would fall in a gravitational field.",
              [("A straight line.", "Only at constant velocity."), ("A curve towards the front.", "The floor accelerates towards the ball."),
               ("A circle.", "The acceleration is in one direction.")])
    ex.choice("A clock is at the front and an identical clock at the rear of the accelerating spacecraft. Which runs slower, and why?",
              "The rear clock: it experiences the same effect as being in a stronger gravitational field.",
              [("The rear clock: it has a greater acceleration.", "Different accelerations is wrong physics."),
               ("The front clock: it is higher in the equivalent field.", "Higher in the field means faster."),
               ("Neither: there is no gravity.", "Acceleration has equivalent effects.")])
    ex.num(f"The spacecraft later observes a black hole of {n} solar masses. Calculate its Schwarzschild radius.", rs, "m",
           wrong=[(2 * G * n / C**2, "Convert to kilograms.")],
           working=[rf"r = \frac{{2GM}}{{c^2}} = {ltx(rs)}\ \mathrm{{m}}"])
    ex.choice("A star is observed orbiting the black hole. What does this show about the radius of its orbit?",
              "It is greater than the Schwarzschild radius, since nothing from within the event horizon can be observed.",
              [("It is less than the Schwarzschild radius.", "It could not then be seen."),
               ("It equals the Schwarzschild radius.", "Light could not escape to us from within the horizon."),
               ("Nothing, because black holes cannot be studied.", "Its visibility is the evidence.")])
    return ex.build("General relativity describes the effects of accelerating frames of reference and gravitational fields.")


# ════ General relativity (2019 Q6, 2018 Q5) ════
def event_horizon(level=LEVEL):
    ex = ra._exam().on("General Relativity")
    M = uni(2.0, 9.0) * 1e36
    rs = 2 * G * M / C**2
    ex.num("Calculate the Schwarzschild radius of the black hole.", rs, "m", wrong=[(G * M / C**2, "Include the 2.")],
           working=[rf"r = \frac{{2GM}}{{c^2}} = {ltx(rs)}\ \mathrm{{m}}"])
    ex.choice("What is the escape velocity at its event horizon?", "The speed of light, 3.00 × 10⁸ m s⁻¹.",
              [("Zero.", "It is the speed of light."), ("Greater than the speed of light everywhere outside it.", "Outside, it is less than c."),
               ("The speed of sound.", "It is c.")])
    ex.choice("How does general relativity explain the orbit of a star around the black hole?",
              "Mass curves spacetime, and the star follows a geodesic in the curved spacetime.",
              [("A force acts through flat spacetime.", "In GR gravity arises from curvature."),
               ("The star follows a world line that is always straight.", "Spacetime is curved."),
               ("Spacetime curves the mass of the star.", "Mass curves spacetime.")])
    ex.choice("On a spacetime diagram with time on the vertical axis, which world line shows an object moving at constant velocity?",
              "A sloping straight line.", [("A vertical line.", "That is stationary."), ("A curve.", "That is accelerating."),
                                          ("A horizontal line.", "That is impossible.")])
    return ex.build(f"A black hole at the centre of a galaxy has a mass of {fmt(M)} kg.")


# ════ Stellar physics (2023 Q6, SPQ Q4) ════
def supergiant(level=LEVEL):
    ex = ra._exam().on("Stellar Physics")
    r, T_ = uni(3.0, 9.0) * 1e10, pick(9800, 11000, 12000, 21000)
    L_ = 4 * math.pi * r**2 * SIGMA * T_**4
    ly = pick(430, 640, 773, 860)
    b = sig(L_) / (4 * math.pi * (ly * LIGHT_YEAR)**2)
    ex.num("Calculate the luminosity of the star.", L_, "W", wrong=[(4 * math.pi * r**2 * SIGMA * T_, "T is to the power 4.")],
           working=[rf"L = 4\pi r^2\sigma T^4 = {ltx(L_)}\ \mathrm{{W}}"])
    ex.choice("What assumption is made in this calculation?", "The star behaves as a black body.",
              [("The star is on the main sequence.", "Not needed."), ("The star is a point source of heat only.", "Its radius is used."),
               ("The apparent brightness equals the luminosity.", "They are different.")])
    ex.num(f"The star is {ly} light-years from the Earth. Calculate its apparent brightness.", b, "W m⁻²",
           wrong=[(sig(L_) / (4 * math.pi * ly**2), "Convert light-years to metres.")],
           working=[rf"b = \frac{{L}}{{4\pi d^2}} = {ltx(b)}\ \mathrm{{W\,m^{{-2}}}}"],
           scaffold=[("What is the distance in metres?", ly * LIGHT_YEAR, "m")])
    ex.choice("Explain the change in radius after such a star leaves the main sequence.",
              "It increases while thermal pressure exceeds the gravitational force, and stops when the two balance.",
              [("It increases because gravity disappears.", "Gravity still acts."),
               ("It increases because the star gains mass.", "Compare pressure and gravity."),
               ("It decreases while thermal pressure exceeds gravity.", "That would make it expand.")])
    return ex.build(f"A very luminous star has a radius of {fmt(r)} m and a surface temperature of {T_} K.")


# ════ Waves (2017 Q9) ════
def vibrating_string(level=LEVEL):
    ex = qw._exam().on("Waves")
    f, lam = pick(110, 147, 196, 220), uni(1.1, 1.9, 2)
    A = pick(7.5e-4, 9.5e-4, 1.2e-3)
    w, k = sig(2 * math.pi * f), sig(2 * math.pi / lam)
    ff, lv = w / (2 * math.pi), 2 * math.pi / k
    frac = pick(0.12, 0.25, 0.40)
    ex.num("Determine the frequency of the wave.", ff, "Hz", wrong=[(w, "That is 2πf.")],
           working=[rf"2\pi f = {w:g} \qquad f = {ltx(ff)}\ \mathrm{{Hz}}"])
    ex.num("Determine the speed of the wave.", ff * lv, "m s⁻¹", wrong=[(ff * k, "The coefficient of x is 2π/λ.")],
           working=[rf"\lambda = \frac{{2\pi}}{{{k:g}}} = {ltx(lv)}\ \mathrm{{m}}", rf"v = f\lambda = {ltx(ff*lv)}\ \mathrm{{m\,s^{{-1}}}}"],
           scaffold=[("What is the wavelength?", lv, "m")])
    ex.num(f"Further along the string the wave has only {frac:g} of its original energy. Calculate its amplitude there.",
           A * math.sqrt(frac), "m", wrong=[(A * frac, "E ∝ A².")],
           working=[r"\frac{E_1}{A_1^2} = \frac{E_2}{A_2^2}", rf"A_2 = {ltx(A*math.sqrt(frac))}\ \mathrm{{m}}"])
    ex.choice("A stationary wave is set up on the string. In terms of superposition, how is it produced?",
              "Waves reflected from each end interfere, producing maxima and minima.",
              [("The wave stops moving when it reaches the end.", "It is reflected."),
               ("Two waves of different frequencies add together.", "The reflected wave has the same frequency."),
               ("The string absorbs the wave at regular points.", "Nodes come from destructive interference.")])
    return ex.build(f"A wave on a stretched string is described by **y = {fmt(A, 2)} sin({w:g}t − {k:g}x)**, in SI units.")


# ════ Waves (SPQ Q8: microwave oven) ════
def microwave_oven(level=LEVEL):
    ex = qw._exam().on("Waves")
    f, d = 2.45e9, uni(0.058, 0.064, 3)
    v = f * 2 * d
    x = sig(2 * d * pick(0.15, 0.30, 0.70), 2)
    ex.choice("How is a stationary wave formed in the oven?", "The reflected wave interferes with the transmitted wave.",
              [("Two waves of different frequencies travel together.", "One frequency, opposite directions."),
               ("The microwaves slow to a stop.", "The wave is a superposition."),
               ("The food absorbs the whole wave.", "Reflection and interference are needed.")])
    ex.choice("Why does the butter melt only in certain spots?",
              "At antinodes the energy is high so it melts; at nodes there is little energy so it does not.",
              [("At nodes the energy is high, so it melts.", "Nodes are points of destructive interference."),
               ("The microwaves only travel through some parts of the butter.", "Think of nodes and antinodes."),
               ("The butter is thinner in those places.", "The pattern comes from the stationary wave.")])
    ex.num(f"The distance between the centres of neighbouring melted spots is {d:g} m. The frequency is 2.45 × 10⁹ Hz. "
           f"Determine the speed of the microwaves.", v, "m s⁻¹", wrong=[(f * d, "Antinodes are half a wavelength apart.")],
           working=[rf"\lambda = 2 \times {d:g}", rf"v = f\lambda = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
           scaffold=[("What is the wavelength?", 2 * d, "m")])
    ex.num(f"Using this wavelength, calculate the phase difference between two points {x:g} m apart on one travelling wave.",
           math.pi * x / d, "rad", working=[rf"\phi = \frac{{2\pi x}}{{\lambda}} = {ltx(math.pi*x/d)}\ \mathrm{{rad}}"])
    return ex.build("The turntable is removed from a microwave oven and a plate of butter is heated inside.")


# ════ Interference (2018 Q11, SPQ Q9: wedge) ════
def hair_wedge(level=LEVEL):
    ex = qw._exam().on("Interference")
    nm, l = pick(589, 633), pick(0.075, 0.090, 0.110)
    d = sig(uni(6.0, 9.5) * 1e-5, 2)
    N = pick(19, 20)
    dx = nm * 1e-9 * l / (2 * d)
    total = sig(N * dx)
    ans = nm * 1e-9 * l / (2 * total / N)
    ex.choice("Is the pattern produced by division of amplitude or of wavefront?", "Division of amplitude.",
              [("Division of wavefront.", "The light is partly reflected at two surfaces."), ("Neither; it is refraction.", "It is interference."),
               ("Division of frequency.", "No such method.")])
    ex.num("Determine the diameter of the hair.", ans, "m", wrong=[(nm * 1e-9 * l / (2 * total), f"Divide by {N} first."), (2 * ans, "Δx = λl/2d.")],
           working=[rf"\Delta x = {ltx(total/N)}\ \mathrm{{m}}", rf"d = \frac{{\lambda l}}{{2\Delta x}} = {ltx(ans)}\ \mathrm{{m}}"],
           scaffold=[("What is the fringe separation?", total / N, "m")])
    ex.choice(f"Why measure across {N} fringe separations rather than one?", "To reduce the percentage uncertainty in the fringe separation.",
              [("To reduce the scale reading uncertainty of the microscope.", "That is unchanged."), ("To make the fringes sharper.", "It does not."),
               ("To reduce the absolute uncertainty of the instrument.", "That is unchanged.")])
    ex.choice("The hair is replaced by a thicker wire. How does the fringe separation change, and why?",
              "It is less, because d increases while λ and l are constant (Δx = λl/2d).",
              [("It is greater, because the wedge angle is larger.", "Δx ∝ 1/d."), ("It is unchanged.", "d has changed."),
               ("It is less, because the wavelength is smaller.", "λ is unchanged.")])
    return ex.build(f"A hair separates two glass slides, in contact at one end, forming an air wedge {l:g} m long. In light of "
                    f"wavelength {nm} nm, {N} fringe separations measure {fmt(total)} m.")


# ════ Interference (2020 Q10, 2023 Q11: coatings) ════
def lens_coating(level=LEVEL):
    ex = qw._exam().on("Interference")
    n, nm = pick((1.38, "magnesium fluoride"), (1.30, "a polymer"), (1.34, "a coating")), pick(480, 530, 560, 600)
    n, name = n
    d = nm * 1e-9 / (4 * n)
    ex.choice("Why is a coating of a particular thickness non-reflecting for one wavelength?",
              "It gives destructive interference of the reflected rays for that wavelength.",
              [("It absorbs that wavelength.", "It is interference."), ("It refracts that wavelength away from the lens.", "It is interference."),
               ("It gives constructive interference of the reflected rays.", "That would increase reflection.")])
    ex.num("Calculate the minimum thickness of the coating.", d, "m", wrong=[(nm * 1e-9 / (2 * n), "d = λ/4n.")],
           working=[rf"d = \frac{{\lambda}}{{4n}} = {ltx(d)}\ \mathrm{{m}}"])
    ex.num(f"Calculate the optical path through the coating once, for this thickness.", n * sig(d), "m",
           wrong=[(sig(d) / n, "opd = n × gpd.")], working=[rf"opd = n \times gpd = {ltx(n*sig(d))}\ \mathrm{{m}}"])
    ex.choice("Why may the lens look coloured in reflected white light?",
              "Only some wavelengths are cancelled; the other reflected colours combine to give a tint.",
              [("The coating is a dye.", "It is transparent."), ("All wavelengths are cancelled equally.", "Only one is fully cancelled."),
               ("White light is polarised by the coating.", "The effect is interference.")])
    return ex.build(f"A glass lens (refractive index 1.51) has a thin coating of {name} (refractive index {n:g}) to make it "
                    f"non-reflecting at {nm} nm.")


# ════ Particles from space (2018 Q8, 2025 Q7) ════
def cosmic_proton(level=LEVEL):
    ex = qw._exam().on("Particles from Space")
    v, B = sig(uni(1.0, 4.0) * 1e6, 2), sig(uni(2.0, 6.0) * 1e-5, 2)
    r = M_P * v / (E_CHARGE * B)
    ex.choice("State an origin of cosmic rays.", "The Sun, other stars or black holes.",
              [("The solar wind.", "'Solar wind' is not accepted."), ("The Earth's magnetic field.", "It deflects particles."),
               ("The ozone layer.", "They come from space.")])
    ex.num("Calculate the force on the proton.", E_CHARGE * v * B, "N", working=[rf"F = qvB = {ltx(E_CHARGE*v*B)}\ \mathrm{{N}}"])
    ex.num("Calculate the radius of its path.", r, "m", wrong=[(M_P * v**2 / (E_CHARGE * B), "r = mv/qB.")],
           working=[rf"r = \frac{{mv}}{{qB}} = {ltx(r)}\ \mathrm{{m}}"])
    ex.choice("It moves into a region of weaker magnetic induction. What happens to the radius, and why?",
              "It increases, because the magnetic induction is smaller while m, v and q are constant.",
              [("It decreases, because the force is smaller.", "A smaller force gives a larger radius."),
               ("It is unchanged.", "r depends on B."), ("It increases, because the proton speeds up.", "The speed is unchanged.")])
    return ex.build(f"A cosmic ray proton travels at {fmt(v, 2)} m s⁻¹ at right angles to a region of the Earth's magnetic "
                    f"field of magnetic induction {fmt(B, 2)} T.")


# ════ Simple harmonic motion (2022 Q10, 2025 Q9) ════
def seesaw(level=LEVEL):
    ex = qw._exam().on("Simple Harmonic Motion")
    m, A, T_ = pick(18, 24, 28, 32), uni(0.20, 0.40, 2), uni(2.2, 3.4)
    w = 2 * math.pi / T_
    ws = sig(w)
    ex.choice("What is meant by simple harmonic motion?",
              "Motion in which the unbalanced force is proportional to, and in the opposite direction to, the displacement from the rest position.",
              [("Motion in which the force is proportional to the displacement.", "The direction is missing."),
               ("Any motion that repeats.", "Not all periodic motion is SHM."), ("Motion at constant speed back and forth.", "The speed varies.")])
    ex.num("Calculate the angular frequency of the motion.", w, "rad s⁻¹", wrong=[(1 / T_, "ω = 2π/T.")],
           working=[rf"\omega = \frac{{2\pi}}{{T}} = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"])
    ex.num("Calculate the maximum speed of the child.", ws * A, "m s⁻¹", working=[rf"v_{{max}} = \omega A = {ltx(ws*A)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num("Calculate the maximum potential energy associated with the motion.", 0.5 * m * ws**2 * A**2, "J",
           working=[rf"E_P = \tfrac12 m\omega^2 y^2 = {ltx(0.5*m*ws**2*A**2)}\ \mathrm{{J}}"])
    ex.choice("The child then bounces off the seat each cycle. Why is the motion no longer approximately SHM?",
              "The force is no longer directly proportional to the displacement from equilibrium.",
              [("The period is too long.", "Consider force and displacement."), ("The child's mass changes.", "It does not."),
               ("Energy is lost to sound.", "That is damping, not the definition.")])
    return ex.build(f"A child of mass {m} kg on a seesaw moves vertically with approximately simple harmonic motion of "
                    f"amplitude {A:g} m and period {T_:g} s.")


# ════ Polarisation (2024 Q12, 2023 Q12) ════
def screen_polarisation(level=LEVEL):
    ex = qw._exam().on("Polarisation")
    ip = pick(52.4, 53.1, 56.1, 56.5)
    n = math.tan(math.radians(ip))
    ex.choice("How could a student determine whether the light from a laptop screen is plane-polarised?",
              "Rotate one polaroid analyser in front of the screen and observe whether the intensity changes.",
              [("Rotate an analyser placed after a polariser in front of the screen.", "Two polaroids scores nothing."),
               ("Hold a polaroid still in front of the screen.", "It must be rotated."),
               ("Pass the light through a diffraction grating.", "That tests wavelength.")])
    ex.choice("The light is polarised. What is seen as the analyser is rotated through 180° from maximum brightness?",
              "The brightness falls gradually to a minimum and then rises to a maximum again.",
              [("It stays constant.", "That would be unpolarised."), ("It switches off suddenly at 90°.", "The change is gradual."),
               ("It falls steadily for the whole 180°.", "It recovers after 90°.")])
    ex.num(f"Light reflected from a glass table is completely polarised at an angle of incidence of {ip:g}°. Calculate the "
           f"refractive index of the glass.", n, "", wrong=[(1 / math.sin(math.radians(ip)), "n = tan iP.")],
           working=[rf"n = \tan i_P = {ltx(n)}"])
    ex.num("Determine the angle between the incident ray and the reflected ray at this angle.", 2 * ip, "°",
           wrong=[(ip, "Both rays are at iP to the normal.")], working=[rf"2 \times {ip:g} = {2*ip:g}^\circ"])
    return ex.build("A student investigates polarised light.")


ROTATIONAL = {
    "Athlete's Race": athlete, "Test Car": car_gradient,
    "Slowing Flywheel": flywheel_stop, "Fairground Drum": drum_spin_up,
    "Car on a Circular Track": toy_car_track, "Conical Pendulum": conical_pendulum,
    "Turntable and Ring": ring_on_table, "Gymnast on a Bar": gymnast,
    "Probe at an Asteroid": asteroid_probe, "Launch from Mars": mars_launch,
    "Accelerating Spacecraft": accelerating_ship, "Galactic Black Hole": event_horizon,
    "Very Luminous Star": supergiant,
}

QUANTA = {
    "Cosmic Ray Proton": cosmic_proton,
    "Child on a Seesaw": seesaw,
    "Vibrating String": vibrating_string, "Microwave Oven": microwave_oven,
    "Hair Wedge": hair_wedge, "Lens Coating": lens_coating,
    "Laptop Screen": screen_polarisation,
}
