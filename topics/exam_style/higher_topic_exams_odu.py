"""Higher Our Dynamic Universe — exam-style questions that each stay within one topic, modelled on SQA
paper questions with changing numbers.

Recognised wrong answers follow the Higher marking instructions: signs not applied in the equations of
motion and in momentum, the wrong mass used for a coupling, sin and cos swapped, a single cable taken to
hold all the weight, only one object's kinetic energy compared, the radius not added to the altitude, and
the Lorentz factor applied the wrong way round.
"""
import math
import random

from topics.exam_style.base import Exam, fmt, graph, ltx, pick, sig
from topics.exam_style.higher_odu import C, G, G_N, H0, NOTES, UNIT1, UNIT2


def _ex(level, topic, unit=UNIT1):
    return Exam(unit, level, NOTES).on(topic)


# ════════════════════════════ Equations of motion ════════════════════════════

def rising_balloon(level="Higher"):
    ex = _ex(level, "Equations of Motion")
    u, h = pick(3.0, 4.0, 5.0, 6.0), pick(35, 45, 60, 80)
    rise = u ** 2 / (2 * G)
    ex.num("Calculate the maximum height of the sandbag above the ground.", h + rise, "m",
           wrong=[(rise, f"That's the height gained after release — add the {h} m."), (h - rise, "The bag first moves UP after release."),
                  (h, "The bag is moving upwards when released, so it rises further.")],
           working=[r"v^2 = u^2 + 2as", rf"0 = {u:g}^2 + 2(-9.8)s \Rightarrow s = {ltx(rise)}\ \text{{m}}", rf"H = {h} + {ltx(rise)} = {ltx(h + rise)}\ \text{{m}}"],
           scaffold=[("Height gained after release, in m?", rise, "m")])
    v = -math.sqrt(u ** 2 + 2 * G * h)
    ex.num("Calculate the velocity of the sandbag just before it hits the ground (take upwards as positive).", v, "m/s",
           wrong=[(-v, "The bag is moving DOWN, so its velocity is negative."), (-math.sqrt(2 * G * h), "Include the initial velocity (or fall from the maximum height)."),
                  (u - 2 * G * h, "Use v² = u² + 2as and take the square root.")],
           working=[rf"v^2 = {u:g}^2 + 2(-9.8)(-{h})", rf"v = {ltx(v)}\ \text{{m/s}}"])
    t = (u - sig(v)) / G
    ex.num("Calculate the time from release until the sandbag hits the ground.", t, "s",
           wrong=[((-sig(v) - u) / G, "u and v have opposite signs."), (math.sqrt(2 * h / G), "The bag is not released from rest."),
                  (u / G, "That's only the time to reach the highest point.")],
           working=[r"v = u + at", rf"{ltx(v)} = {u:g} + (-9.8)t", rf"t = {ltx(t)}\ \text{{s}}"])
    ex.choice("What is the velocity of the sandbag at the instant it is released?", f"{u:g} m/s upwards.",
              [("Zero.", "It was moving with the balloon, so it keeps that velocity."), ("9.8 m/s downwards.", "9.8 m/s² is the acceleration."),
               (f"{u:g} m/s downwards.", "It has the same velocity as the balloon — upwards.")])
    ex.choice("What is the acceleration of the sandbag at its highest point?", "9.8 m/s² downwards.",
              [("Zero, because it has momentarily stopped.", "Velocity is zero, but gravity still acts."),
               ("9.8 m/s² upwards.", "Gravity acts downwards."), ("It is changing from upwards to downwards.", "The acceleration is constant throughout.")])
    return ex.build(f"A hot air balloon is rising vertically at a constant {u:g} m/s. When it is {h} m above the ground a sandbag is released from it. "
                    "Air resistance can be ignored.")


def emergency_stop(level="Higher"):
    ex = _ex(level, "Equations of Motion")
    u, tr, dec = pick(18, 22, 26, 31), pick(0.60, 0.70, 0.80), pick(5.5, 6.5, 7.5)
    think = u * tr
    ex.num(f"The driver takes {tr:g} s to react before braking. Calculate the distance travelled in this time.", think, "m",
           wrong=[(u / tr, "d = vt."), (0.5 * u * tr, "The speed is constant while the driver reacts.")],
           working=[rf"d = vt = {u} \times {tr:g} = {ltx(think)}\ \text{{m}}"])
    brake = u ** 2 / (2 * dec)
    ex.num(f"The brakes then give a constant acceleration of −{dec:g} m/s². Calculate the braking distance.", brake, "m",
           wrong=[(u ** 2 / dec, "v² = u² + 2as: include the 2."), (u / dec, "That's the braking time.")],
           working=[rf"0 = {u}^2 + 2(-{dec:g})s", rf"s = {ltx(brake)}\ \text{{m}}"])
    total = tr + u / dec
    ex.num("Calculate the total time from the driver seeing the hazard until the car stops.", total, "s",
           wrong=[(u / dec, "Add the reaction time."), ((sig(think) + sig(brake)) / u, "The car slows down while braking, so d ÷ u is too short.")],
           working=[rf"0 = {u} + (-{dec:g})t \Rightarrow t = {ltx(u / dec)}\ \text{{s}}", rf"t_{{total}} = {tr:g} + {ltx(u / dec)} = {ltx(total)}\ \text{{s}}"],
           scaffold=[("Braking time, in s?", u / dec, "s")])
    ex.choice("Which describes the velocity–time graph from when the driver sees the hazard?",
              "A horizontal line during the reaction time, then a straight line falling to zero.",
              [("A straight line falling to zero from the start.", "The speed is constant while the driver reacts."),
               ("A horizontal line, then a horizontal line at zero.", "Braking takes time: the velocity decreases steadily."),
               ("A curve rising from zero.", "The car is slowing down.")])
    ex.choice("On a wet road the braking acceleration has a smaller magnitude. What effect does this have on the braking distance from the same speed?",
              "It is greater, because the car takes longer to stop and travels further.",
              [("It is smaller, because the acceleration is smaller.", "s = u² ÷ 2a: a smaller a gives a larger s."),
               ("It is the same, because the initial speed is the same.", "The distance also depends on the acceleration."),
               ("It is the same, because the reaction time is unchanged.", "The question is about the BRAKING distance.")])
    return ex.build(f"A car is travelling at {u} m/s along a straight, level road when the driver sees a hazard.")


# ════════════════════════════ Graphs of motion ════════════════════════════

def bouncing_ball_graph(level="Higher"):
    ex = _ex(level, "Graphs of Motion")
    t1, v1, v2, t2 = pick((0.40, 3.9, 2.9, 0.30), (0.50, 4.9, 3.9, 0.40), (0.60, 5.9, 4.9, 0.50))
    contact = pick(0.10, 0.15)
    t_up, t_top = round(t1 + contact, 2), round(t1 + contact + t2, 2)
    fig = graph([(0, 0), (t1, -v1), (t_up, v2), (t_top, 0)], labels=["O", "P", "Q", "R"])
    h1 = 0.5 * t1 * v1
    ex.num("Use the graph to determine the height from which the ball is dropped.", h1, "m",
           wrong=[(t1 * v1, "The area under this section is a triangle: ½ × base × height."), (v1 / t1, "That's the gradient (acceleration).")],
           working=[rf"s = \text{{area}} = \tfrac{{1}}{{2}} \times {t1:g} \times {v1:g} = {ltx(h1)}\ \text{{m}}"])
    a = (v2 + v1) / contact
    ex.num("Use the graph to calculate the magnitude of the average acceleration of the ball while it is in contact with the ground.", a, "m/s²",
           wrong=[((v1 - v2) / contact, "The velocity changes direction: v − u = v₂ − (−v₁)."), (v2 / contact, "Use the whole change in velocity.")],
           working=[rf"a = \frac{{v - u}}{{t}} = \frac{{{v2:g} - (-{v1:g})}}{{{contact:g}}} = {ltx(a)}\ \text{{m/s}}^2"])
    h2 = 0.5 * t2 * v2
    ex.num("Determine the maximum height reached after the first bounce.", h2, "m",
           wrong=[(t2 * v2, "The area is a triangle."), (0.5 * t_top * v2, "Use only the time from leaving the ground to the top.")],
           working=[rf"s = \tfrac{{1}}{{2}} \times ({t_top:g} - {t_up:g}) \times {v2:g} = {ltx(h2)}\ \text{{m}}"])
    ex.choice("Why do sections OP and QR of the graph have the same gradient?", "The ball has the same acceleration (due to gravity) whenever it is in the air.",
              [("The ball has the same speed in both sections.", "The speeds differ; the gradient is acceleration."),
               ("The ball travels the same distance in both sections.", "Distance is the area, and the areas differ."),
               ("The force from the ground is the same in both sections.", "The ball is not touching the ground then.")])
    ex.choice("What does the graph show about the collision with the ground?", "It is inelastic: the ball leaves more slowly than it arrived, so kinetic energy is lost.",
              [("It is elastic: the ball bounces back.", "Bouncing does not mean elastic; compare the kinetic energies."),
               ("It is inelastic because the velocity changes sign.", "The change of sign shows a change of direction."),
               ("It is elastic because the acceleration in the air is unchanged.", "That says nothing about energy lost in the bounce.")])
    return ex.build("A ball is dropped from rest and bounces once. The graph shows its velocity (upwards positive) from release until it reaches "
                    "the top of its first bounce.", figure=fig)


# ════════════════════════════ Towing ════════════════════════════

def train_carriages(level="Higher"):
    ex = _ex(level, "Towing")
    me, ma, mb = pick(80000, 90000, 100000), pick(35000, 40000), pick(20000, 25000, 30000)
    fe, fa, fb = pick(6000, 8000), pick(3000, 4000), pick(1500, 2000)
    drive = pick(90000, 110000, 130000)
    a = (drive - fe - fa - fb) / (me + ma + mb)
    ex.num("Calculate the acceleration of the train.", a, "m/s²",
           wrong=[(drive / (me + ma + mb), "Subtract all the frictional forces."), ((drive - fe - fa - fb) / me, "Use the total mass of the train."),
                  ((drive - fe) / (me + ma + mb), "Include the friction on both carriages.")],
           working=[rf"F_{{un}} = {drive} - {fe} - {fa} - {fb} = {drive - fe - fa - fb}\ \text{{N}}", rf"a = \frac{{F_{{un}}}}{{m_{{total}}}} = {ltx(a)}\ \text{{m/s}}^2"])
    t1 = (ma + mb) * sig(a) + fa + fb
    ex.num("Calculate the tension in the coupling between the engine and carriage A.", t1, "N",
           wrong=[((ma + mb) * sig(a), "The tension must also overcome the friction on both carriages."), (ma * sig(a) + fa, "This coupling pulls BOTH carriages."),
                  (drive - fe, "The engine accelerates too: apply F = ma to the carriages.")],
           working=[r"T_1 - f_A - f_B = (m_A + m_B)a", rf"T_1 = ({ma} + {mb}) \times {ltx(a)} + {fa} + {fb} = {ltx(t1)}\ \text{{N}}"])
    t2 = mb * sig(a) + fb
    ex.num("Calculate the tension in the coupling between carriage A and carriage B.", t2, "N",
           wrong=[(mb * sig(a), "Include the friction on carriage B."), ((ma + mb) * sig(a) + fa + fb, "This coupling pulls only carriage B.")],
           working=[r"T_2 - f_B = m_B a", rf"T_2 = {mb} \times {ltx(a)} + {fb} = {ltx(t2)}\ \text{{N}}"])
    ex.choice("The frictional forces increase as the speed increases. What must happen to the driving force to keep the acceleration the same?",
              "It must increase, so that the unbalanced force stays the same.",
              [("It can stay the same, because the mass is unchanged.", "The unbalanced force would then decrease."),
               ("It must decrease, because the train is moving faster.", "More friction needs more driving force."),
               ("It must equal the total friction.", "Then the forces are balanced and the acceleration is zero.")])
    ex.choice("The engine then travels at a constant speed. What is the tension in the coupling between carriage A and carriage B?",
              "Equal to the frictional force on carriage B.",
              [("Zero, because there is no acceleration.", "B's friction must still be balanced."),
               ("Equal to the weight of carriage B.", "Weight acts vertically."),
               ("Equal to the driving force.", "The driving force balances the friction on the whole train.")])
    return ex.build(f"An engine of mass {me} kg pulls carriage A ({ma} kg), which pulls carriage B ({mb} kg), along a straight, level track. "
                    f"The driving force is {drive} N. The frictional forces are {fe} N on the engine, {fa} N on A and {fb} N on B.")


# ════════════════════════════ Components of vectors ════════════════════════════

def crate_on_ramp(level="Higher"):
    ex = _ex(level, "Components of Vectors")
    m, th = pick(25, 40, 55, 70), pick(15, 18, 22, 28)
    along = m * G * math.sin(math.radians(th))
    perp = m * G * math.cos(math.radians(th))
    ex.num("Calculate the component of the crate's weight acting down the ramp.", along, "N",
           wrong=[(perp, "Down the slope is mg sin θ."), (m * G, "Only the component along the ramp."), (m * math.sin(math.radians(th)), "Use the weight mg.")],
           working=[rf"W_\parallel = mg\sin\theta = {m} \times 9.8 \times \sin {th}^\circ = {ltx(along)}\ \text{{N}}"])
    f = sig(along * random.uniform(0.3, 0.6), 2)
    T = sig(along) + f
    ex.num(f"The crate is pulled up the ramp at a constant speed. The frictional force is {fmt(f)} N. Calculate the tension in the rope.", T, "N",
           wrong=[(sig(along) - f, "Moving UP, friction acts DOWN the ramp, so it adds."), (sig(along), "The rope must also overcome friction."),
                  (m * G + f, "Use the component of weight along the ramp.")],
           working=[r"T = W_\parallel + F_f", rf"T = {ltx(along)} + {fmt(f)} = {ltx(T)}\ \text{{N}}"])
    ex.num("Calculate the component of the crate's weight acting at right angles to the ramp.", perp, "N",
           wrong=[(along, "At right angles to the slope is mg cos θ."), (m * G, "Resolve the weight.")],
           working=[rf"W_\perp = mg\cos\theta = {m} \times 9.8 \times \cos {th}^\circ = {ltx(perp)}\ \text{{N}}"])
    a = (sig(along) - f) / m
    ex.num("The rope is released and the crate, momentarily at rest, slides back down. The frictional force has the same size. Calculate its acceleration.",
           a, "m/s²",
           wrong=[((sig(along) + f) / m, "Sliding DOWN, friction acts UP the ramp."), (sig(along) / m, "Subtract the friction."), (G, "It is on a slope, not in free fall.")],
           working=[rf"a = \frac{{{ltx(along)} - {fmt(f)}}}{{{m}}} = {ltx(a)}\ \text{{m/s}}^2"])
    ex.choice("The ramp is made steeper. What happens to the tension needed to pull the crate at constant speed, if friction is unchanged?",
              "It increases, because the component of weight down the ramp increases.",
              [("It decreases, because cos θ decreases.", "Down the ramp is mg sin θ."),
               ("It stays the same, because the weight is unchanged.", "The component along the ramp changes."),
               ("It stays the same, because the speed is constant.", "Constant speed means balanced forces, but a bigger force must be balanced.")])
    return ex.build(f"A crate of mass {m} kg is on a ramp at {th}° to the horizontal. A rope parallel to the ramp is attached to it.")


def hanging_sign(level="Higher"):
    ex = _ex(level, "Components of Vectors")
    m, th = pick(6.0, 8.0, 12.0, 15.0), pick(25, 30, 35, 40, 50)
    W = m * G
    ex.num("Calculate the weight of the sign.", W, "N", wrong=[(m, "W = mg."), (m / G, "W = mg.")],
           working=[rf"W = mg = {m:g} \times 9.8 = {ltx(W)}\ \text{{N}}"])
    vert = sig(W) / 2
    ex.num("Determine the vertical component of the tension in one cable.", vert, "N",
           wrong=[(W, "TWO cables share the weight."), (vert * math.sin(math.radians(th)), "The vertical components simply add to equal the weight.")],
           working=[rf"2T_v = W \Rightarrow T_v = {ltx(vert)}\ \text{{N}}"])
    T = sig(vert) / math.sin(math.radians(th))
    ex.num("Calculate the tension in each cable.", T, "N",
           wrong=[(sig(vert) / math.cos(math.radians(th)), "The angle is to the HORIZONTAL, so T_v = T sin θ."),
                  (sig(vert) * math.sin(math.radians(th)), "T_v = T sin θ, so T = T_v ÷ sin θ."), (sig(W) / math.sin(math.radians(th)), "Share the weight between two cables.")],
           working=[r"T_v = T\sin\theta", rf"{ltx(vert)} = T \sin {th}^\circ \Rightarrow T = {ltx(T)}\ \text{{N}}"],
           scaffold=[("Vertical component of one tension, in N?", vert, "N")])
    horiz = sig(T) * math.cos(math.radians(th))
    ex.num("Calculate the horizontal component of the tension in one cable.", horiz, "N",
           wrong=[(sig(T) * math.sin(math.radians(th)), "Horizontal = T cos θ for an angle to the horizontal.")],
           working=[rf"T_h = T\cos\theta = {ltx(T)} \times \cos {th}^\circ = {ltx(horiz)}\ \text{{N}}"])
    ex.choice("Longer cables are fitted so that each is closer to the horizontal — a smaller angle. What happens to the tension in each cable?",
              "It increases: the vertical component must stay the same, and sin θ is smaller.",
              [("It increases because the vertical component of tension increases.", "The vertical components must still just equal the weight."),
               ("It decreases because longer cables carry less force.", "The tension depends on the angle."),
               ("It stays the same because the weight is unchanged.", "A different angle needs a different tension to give the same vertical component.")])
    return ex.build(f"A shop sign of mass {m:g} kg hangs at rest from two cables, each at {th}° to the horizontal, arranged symmetrically.")


# ════════════════════════════ Momentum and impulse ════════════════════════════

def air_track_collision(level="Higher"):
    ex = _ex(level, "Momentum and Impulse")
    mp, mq, up, uq = pick((0.18, 0.24, 1.20, 0.64), (0.20, 0.30, 0.90, 0.60), (0.15, 0.25, 1.10, 0.50))
    e = random.uniform(0.65, 0.85)
    vp = round((mp * up - mq * uq - mq * e * (up + uq)) / (mp + mq), 2)
    vq = (mp * up - mq * uq - mp * vp) / mq
    ex.num(f"After the collision P moves to the LEFT at {-vp:g} m/s. Calculate the speed of Q after the collision.", vq, "m/s",
           wrong=[((mp * up + mq * uq - mp * vp) / mq, "Momentum is a vector: Q's initial velocity is negative."),
                  ((mp * up - mq * uq + mp * vp) / mq, "P rebounds, so its final velocity is negative.")],
           working=[r"m_Pu_P + m_Qu_Q = m_Pv_P + m_Qv_Q",
                    rf"({mp:g} \times {up:g}) + ({mq:g} \times -{uq:g}) = ({mp:g} \times {vp:g}) + {mq:g}v_Q", rf"v_Q = {ltx(vq)}\ \text{{m/s}}"])
    imp = mq * (sig(vq) + uq)
    ex.num("Calculate the magnitude of the impulse on Q.", imp, "N s",
           wrong=[(abs(mq * (sig(vq) - uq)), "Q changes direction, so the velocities have opposite signs."), (mq * sig(vq), "Impulse = mv − mu.")],
           working=[rf"\text{{Impulse}} = mv - mu = {mq:g} \times ({ltx(vq)} - (-{uq:g})) = {ltx(imp)}\ \text{{N s}}"])
    ms = pick(20, 25, 40)
    F = sig(imp) / (ms / 1000)
    ex.num(f"The vehicles are in contact for {ms} ms. Calculate the average force on Q.", F, "N",
           wrong=[(sig(imp) / ms, "Convert ms to s."), (sig(imp) * ms / 1000, "F = impulse ÷ t.")],
           working=[rf"Ft = mv - mu \Rightarrow F = \frac{{{ltx(imp)}}}{{{ms}\times10^{{-3}}}} = {ltx(F)}\ \text{{N}}"])
    before = 0.5 * mp * up ** 2 + 0.5 * mq * uq ** 2
    after = 0.5 * mp * vp ** 2 + 0.5 * mq * sig(vq) ** 2
    ex.num("Calculate the total kinetic energy before the collision.", before, "J",
           wrong=[(abs(0.5 * mp * up ** 2 - 0.5 * mq * uq ** 2), "Kinetic energy is a scalar: add them."), (0.5 * mp * up ** 2, "Include BOTH vehicles.")],
           working=[rf"E_k = \tfrac12({mp:g})({up:g})^2 + \tfrac12({mq:g})({uq:g})^2 = {ltx(before)}\ \text{{J}}"])
    ex.choice(f"The total kinetic energy after the collision is {fmt(after)} J. What type of collision is this?",
              "Inelastic, because the total kinetic energy before is greater than the total kinetic energy after.",
              [("Elastic, because momentum is conserved.", "Momentum is conserved in elastic and inelastic collisions."),
               ("Elastic, because the vehicles bounce apart.", "Compare the total kinetic energies."),
               ("Inelastic, because momentum is lost.", "Momentum is conserved; kinetic energy is not.")])
    ex.choice("How does the force Q exerts on P compare with the force P exerts on Q during the collision?",
              "Equal in size and opposite in direction.",
              [("Larger, because Q has more mass.", "Newton's third law: the forces are equal in size."),
               ("Smaller, because P was moving faster.", "Newton's third law applies whatever the speeds."),
               ("Equal in size and in the same direction.", "The forces act in opposite directions.")])
    return ex.build(f"On a linear air track, vehicle P (mass {mp:g} kg) moving right at {up:g} m/s collides head-on with vehicle Q (mass {mq:g} kg) "
                    f"moving left at {uq:g} m/s. After the collision Q moves to the right. Take right as positive.")


def impact_force_graph(level="Higher"):
    ex = _ex(level, "Momentum and Impulse")
    m, u = pick(0.057, 0.16, 0.43), pick(8.0, 10.0, 12.0)
    ms = pick(6.0, 8.0, 10.0)
    v = u * random.uniform(0.6, 0.85)
    peak = float(f"{2 * m * (u + v) / (ms / 1000):.2g}")
    fig = graph([(0, 0), (ms / 2, peak), (ms, 0)], xlabel="Time (ms)", ylabel="Force (N)")
    imp = 0.5 * peak * ms / 1000
    ex.num("Use the graph to determine the magnitude of the impulse on the ball.", imp, "N s",
           wrong=[(0.5 * peak * ms, "The time is in ms."), (peak * ms / 1000, "The area is a triangle: include the ½.")],
           working=[rf"\text{{Impulse}} = \text{{area}} = \tfrac12 \times {ms:g}\times10^{{-3}} \times {peak:g} = {ltx(imp)}\ \text{{N s}}"])
    reb = sig(imp) / m - u
    ex.num(f"The ball hits the wall at {u:g} m/s. Calculate the speed at which it rebounds.", reb, "m/s",
           wrong=[(sig(imp) / m, "That's the change in velocity; the ball also had to be stopped first."), (sig(imp) / m + u, "The initial velocity has the opposite sign to the force.")],
           working=[r"Ft = mv - mu", rf"{ltx(imp)} = {m:g}v - ({m:g} \times -{u:g})", rf"v = {ltx(reb)}\ \text{{m/s}}"],
           scaffold=[("Change in velocity of the ball, in m/s?", sig(imp) / m, "m/s")])
    ex.num("Determine the average force on the ball during the contact.", peak / 2, "N",
           wrong=[(peak, "That's the MAXIMUM force."), (sig(imp) / ms, "Convert ms to s.")],
           working=[rf"F_{{avg}} = \frac{{\text{{impulse}}}}{{t}} = {ltx(peak / 2)}\ \text{{N}}"])
    ex.choice("A softer ball of the same mass hits the wall at the same speed and rebounds at the same speed. How does its force–time graph compare?",
              "A lower peak force and a longer contact time, with the same area.",
              [("A lower peak force with the same contact time.", "The impulse is unchanged, so a lower force needs a longer time."),
               ("A higher peak force and a longer contact time.", "That would give a larger impulse."),
               ("A lower peak force and a smaller area.", "The change in momentum, and so the area, is unchanged.")])
    return ex.build(f"A ball of mass {m:g} kg hits a wall at right angles and rebounds. The graph shows the force the wall exerts on it.", figure=fig)


# ════════════════════════════ Energy, work and power ════════════════════════════

def roller_coaster(level="Higher"):
    ex = _ex(level, "Energy, Work and Power")
    m, h, d = pick(450, 600, 750), pick(18, 22, 28, 35), pick(60, 75, 90)
    secs = pick(25, 30, 40)
    Ep = m * G * h
    ex.num("Calculate the gravitational potential energy gained by the car as it is raised to the top.", Ep, "J",
           wrong=[(m * h, "Ep = mgh."), (0.5 * Ep, "No ½ in Ep = mgh.")],
           working=[rf"E_p = mgh = {m} \times 9.8 \times {h} = {ltx(Ep)}\ \text{{J}}"])
    ex.num(f"The car is raised in {secs} s. Calculate the minimum power output of the motor.", sig(Ep) / secs, "W",
           wrong=[(sig(Ep) * secs, "P = E ÷ t."), (m * G / secs, "Include the height: P = mgh ÷ t.")],
           working=[rf"P = \frac Et = \frac{{{ltx(Ep)}}}{{{secs}}} = {ltx(sig(Ep) / secs)}\ \text{{W}}"])
    ideal = math.sqrt(2 * G * h)
    ex.num("The car starts from rest at the top. Calculate its speed at the bottom if there were no friction.", ideal, "m/s",
           wrong=[(2 * G * h, "Take the square root."), (math.sqrt(G * h), "mgh = ½mv², so v² = 2gh.")],
           working=[r"mgh = \tfrac12mv^2", rf"v = \sqrt{{2 \times 9.8 \times {h}}} = {ltx(ideal)}\ \text{{m/s}}"])
    v = round(ideal * random.uniform(0.75, 0.9), 1)
    lost = sig(Ep) - 0.5 * m * v ** 2
    ex.num(f"The actual speed at the bottom is {v:g} m/s. The track from top to bottom is {d} m long. Calculate the average frictional force on the car.",
           lost / d, "N",
           wrong=[(lost / h, f"Friction acts along the whole {d} m of track, not through the {h} m height."), (0.5 * m * v ** 2 / d, "Use the energy LOST: Ep − Ek."),
                  (lost, "That's the work done against friction; divide by the distance.")],
           working=[rf"E_k = \tfrac12 \times {m} \times {v:g}^2 = {ltx(0.5 * m * v ** 2)}\ \text{{J}}", rf"E_w = E_p - E_k = {ltx(lost)}\ \text{{J}}",
                    rf"F = \frac{{E_w}}{{d}} = \frac{{{ltx(lost)}}}{{{d}}} = {ltx(lost / d)}\ \text{{N}}"],
           scaffold=[("Work done against friction, in J?", lost, "J")])
    ex.choice("With passengers the car has a greater mass. Ignoring friction, how does its speed at the bottom compare?",
              "It is the same, because the mass cancels in mgh = ½mv².",
              [("It is greater, because there is more potential energy.", "There is also more mass to speed up."),
               ("It is smaller, because the car is heavier.", "Mass cancels."),
               ("It is greater, because gravity acts more strongly on it.", "The acceleration is the same.")])
    return ex.build(f"A roller coaster car of mass {m} kg is raised by a motor to the top of a slope, {h} m above the bottom, and is then released.")


# ════════════════════════════ Effective weight ════════════════════════════

def lift_and_cable(level="Higher"):
    ex = _ex(level, "Effective Weight")
    M, m = pick(600, 750, 900), pick(55, 65, 75)
    a1, a2 = pick(1.2, 1.5, 1.8), pick(0.80, 1.0, 1.4)
    T = (M + m) * (G + a1)
    ex.num(f"The lift accelerates upwards at {a1:g} m/s². Calculate the tension in the cable.", T, "N",
           wrong=[((M + m) * (G - a1), "Accelerating UP: T − W = ma, so T = m(g + a)."), ((M + m) * a1, "That's the unbalanced force; add the weight."),
                  (M * (G + a1), "Include the passenger's mass.")],
           working=[r"T - mg = ma", rf"T = ({M} + {m})(9.8 + {a1:g}) = {ltx(T)}\ \text{{N}}"])
    R = m * (G - a2)
    ex.num(f"Later the lift accelerates downwards at {a2:g} m/s². Calculate the reading on the scales, in newtons.", R, "N",
           wrong=[(m * (G + a2), "Accelerating DOWN: R = m(g − a)."), (m * G, "The lift is accelerating, so R is not equal to the weight."), (m * a2, "That's only the unbalanced force.")],
           working=[r"mg - R = ma", rf"R = {m}(9.8 - {a2:g}) = {ltx(R)}\ \text{{N}}"])
    a3 = pick(0.60, 0.90, 1.1, 1.3)
    reading = float(f"{m * (G + a3):.3g}")
    acc = (reading - m * G) / m
    ex.num(f"At another time the scales read {reading:g} N. Calculate the magnitude of the lift's acceleration.", acc, "m/s²",
           wrong=[(reading / m, "Subtract the weight first: the unbalanced force is R − mg."), ((reading - m * G) / (M + m), "Use the passenger's mass: it is their forces we are using.")],
           working=[rf"F_{{un}} = R - mg = {reading:g} - {m} \times 9.8 = {ltx(reading - m * G)}\ \text{{N}}", rf"a = \frac{{F_{{un}}}}{{m}} = {ltx(acc)}\ \text{{m/s}}^2"],
           scaffold=[("Unbalanced force on the passenger, in N?", reading - m * G, "N")])
    ex.choice("While this reading is shown, which motion is possible?", "Moving downwards and slowing down.",
              [("Moving upwards and slowing down.", "That is a downward acceleration, so the reading would be less than the weight."),
               ("Moving upwards at a constant speed.", "At constant speed the reading equals the weight."),
               ("Moving downwards and speeding up.", "That is a downward acceleration.")])
    ex.choice("If the cable snapped and there was no friction, what would the scales read, and why?",
              "Zero, because the passenger and scales both accelerate downwards at 9.8 m/s², so the scales exert no force on the passenger.",
              [("Zero, because the passenger no longer has any weight.", "The weight mg still acts; it is apparent weightlessness."),
               ("The passenger's weight, because mass is unchanged.", "Scales read the reaction force, which is zero in free fall."),
               ("More than the weight, because of the high speed.", "The reading depends on acceleration, not speed.")])
    return ex.build(f"A lift of mass {M} kg is supported by a single cable. A passenger of mass {m} kg stands on scales inside it.")


# ════════════════════════════ Gravitation ════════════════════════════

def weather_satellite(level="Higher"):
    ex = _ex(level, "Gravitation", UNIT2)
    ms, alt_km = pick(850, 1200, 2100), pick(780, 850, 2000, 20200)
    ME, RE = 6.0e24, 6.4e6
    r = RE + alt_km * 1000
    F = G_N * ME * ms / r ** 2
    ex.num("Calculate the gravitational force between the Earth and the satellite.", F, "N",
           wrong=[(G_N * ME * ms / (alt_km * 1000) ** 2, "r is measured from the CENTRE of the Earth: add the radius."), (G_N * ME * ms / r, "Square r."),
                  (ms * G, "g is smaller than 9.8 N/kg at this height.")],
           working=[rf"r = 6.4\times10^6 + {alt_km}\times10^3 = {ltx(r)}\ \text{{m}}", rf"F = G\frac{{m_1m_2}}{{r^2}} = {ltx(F)}\ \text{{N}}"],
           scaffold=[("Distance from the centre of the Earth, in m?", r, "m")])
    g = sig(F) / ms
    ex.num("Determine the gravitational field strength at the height of the satellite.", g, "N/kg",
           wrong=[(sig(F) * ms, "g = F ÷ m."), (G, "9.8 N/kg is the value at the surface.")],
           working=[rf"g = \frac Wm = \frac{{{ltx(F)}}}{{{ms}}} = {ltx(g)}\ \text{{N/kg}}"])
    surf = G_N * ME * ms / RE ** 2
    ex.num("Calculate the gravitational force on the satellite when it was at the Earth's surface, using the same relationship.", surf, "N",
           wrong=[(G_N * ME * ms / RE, "Square the radius."), (F, "At the surface r is the radius of the Earth.")],
           working=[rf"F = \frac{{6.67\times10^{{-11}} \times 6.0\times10^{{24}} \times {ms}}}{{(6.4\times10^6)^2}} = {ltx(surf)}\ \text{{N}}"])
    ex.choice("A second satellite has twice the mass and is twice as far from the centre of the Earth. How does the force on it compare with the force on the first?",
              "It is half as large.",
              [("It is the same.", "Doubling m doubles F, but doubling r quarters it."), ("It is a quarter as large.", "Include the effect of doubling the mass."),
               ("It is twice as large.", "The distance has changed too: F is proportional to 1/r².")])
    ex.choice("How does the force the satellite exerts on the Earth compare with the force the Earth exerts on the satellite?",
              "It is equal in size and opposite in direction.",
              [("It is much smaller, because the satellite has little mass.", "The two forces are always equal in size."),
               ("It is zero.", "Gravitational attraction is mutual."), ("It is equal in size and in the same direction.", "Each force pulls towards the other object.")])
    return ex.build(f"A satellite of mass {ms} kg orbits at a height of {alt_km} km above the Earth's surface. "
                    "(Mass of Earth = 6.0 × 10²⁴ kg, radius of Earth = 6.4 × 10⁶ m, G = 6.67 × 10⁻¹¹ m³ kg⁻¹ s⁻²)")


# ════════════════════════════ Special relativity ════════════════════════════

def muon_shower(level="Higher"):
    ex = _ex(level, "Special Relativity", UNIT2)
    frac, h_km = pick((0.995, 10), (0.990, 8.0), (0.980, 6.0), (0.998, 15))
    v, t0 = frac * C, 2.2e-6
    k = math.sqrt(1 - frac ** 2)
    ex.num("Calculate the distance a muon would travel in one mean lifetime if there were no relativistic effects.", v * t0, "m",
           wrong=[(C * t0, f"The muon travels at {frac:g}c."), (v / t0, "d = vt.")],
           working=[rf"d = vt = {frac:g} \times 3.00\times10^8 \times 2.2\times10^{{-6}} = {ltx(v * t0)}\ \text{{m}}"])
    t = t0 / k
    ex.num("Calculate the mean lifetime of the muons as measured by an observer on Earth.", t, "s",
           wrong=[(t0 * k, "The moving clock runs slow: the Earth observer measures a LONGER time."), (t0 / (1 - frac ** 2), "Take the square root."),
                  (t0 / math.sqrt(1 - frac), "Square v/c.")],
           working=[r"t' = \frac{t}{\sqrt{1 - v^2/c^2}}", rf"t' = \frac{{2.2\times10^{{-6}}}}{{\sqrt{{1 - {frac:g}^2}}}} = {ltx(t)}\ \text{{s}}"])
    ex.num("Calculate the mean distance a muon travels in the Earth's frame of reference.", v * sig(t), "m",
           wrong=[(v * t0, "In the Earth's frame use the dilated lifetime.")],
           working=[rf"d = vt' = {ltx(v)} \times {ltx(t)} = {ltx(v * sig(t))}\ \text{{m}}"])
    ex.num(f"The muons are created {h_km:g} km above the ground, measured from Earth. Calculate this distance in the muons' frame of reference, in km.",
           h_km * k, "km",
           wrong=[(h_km / k, "The moving observer measures a SHORTER (contracted) distance."), (h_km * (1 - frac ** 2), "Take the square root.")],
           working=[r"l' = l\sqrt{1 - v^2/c^2}", rf"l' = {h_km:g} \times \sqrt{{1 - {frac:g}^2}} = {ltx(h_km * k)}\ \text{{km}}"])
    ex.choice("Why are more muons detected at ground level than expected without relativity?",
              "In the Earth's frame of reference the muons' mean lifetime is longer, so more of them reach the ground.",
              [("The muons' lifetime is longer.", "You must say in which frame of reference."),
               ("In the muons' frame of reference their lifetime is longer.", "In their own frame the lifetime is unchanged; the distance is shorter."),
               ("In the Earth's frame of reference the distance to the ground is shorter.", "It is in the MUONS' frame that the distance is shorter.")])
    ex.choice("Light from a lamp on the ground shines towards an approaching muon. What speed of light would an observer travelling with the muon measure?",
              "3.00 × 10⁸ m/s",
              [(f"{1 + frac:g}c", "Speeds do not add for light."), (f"{1 - frac:g}c", "The speed of light is the same for all observers."),
               ("It depends on the speed of the muon.", "c is the same in every inertial frame.")])
    return ex.build(f"Muons created high in the atmosphere travel straight down at {frac:g}c. In their own frame of reference their mean lifetime is 2.2 µs.")


# ════════════════════════════ The expanding Universe ════════════════════════════

def passing_siren(level="Higher"):
    ex = _ex(level, "The Expanding Universe", UNIT2)
    fs, vs = pick(520, 640, 750, 900), pick(18, 22, 27, 31)
    vair = 340
    app = fs * vair / (vair - vs)
    ex.num("Calculate the frequency heard by the observer as the vehicle approaches.", app, "Hz",
           wrong=[(fs * vair / (vair + vs), "Approaching: use v − v_s, giving a higher frequency."), (fs * (vair - vs) / vair, "f_o = f_s × v ÷ (v − v_s).")],
           working=[r"f_o = f_s\left(\frac{v}{v - v_s}\right)", rf"f_o = {fs} \times \frac{{340}}{{340 - {vs}}} = {ltx(app)}\ \text{{Hz}}"])
    rec = fs * vair / (vair + vs)
    ex.num("Calculate the frequency heard after the vehicle has passed and is moving away.", rec, "Hz",
           wrong=[(app, "Moving away: use v + v_s."), (fs * (vair + vs) / vair, "f_o = f_s × v ÷ (v + v_s).")],
           working=[rf"f_o = {fs} \times \frac{{340}}{{340 + {vs}}} = {ltx(rec)}\ \text{{Hz}}"])
    v2 = pick(12, 15, 24, 29)
    heard = round(fs * vair / (vair - v2))
    spd = vair * (1 - fs / heard)
    ex.num(f"On another journey the observer hears {heard} Hz as the vehicle approaches. Calculate the vehicle's speed.", spd, "m/s",
           wrong=[(vair * (heard / fs - 1), "Approaching: f_o = f_s v ÷ (v − v_s); rearrange for v_s."), (heard - fs, "Use the Doppler relationship.")],
           working=[rf"{heard} = {fs} \times \frac{{340}}{{340 - v_s}}", rf"v_s = {ltx(spd)}\ \text{{m/s}}"])
    ex.choice("Explain, in terms of wavefronts, why the frequency heard is higher as the vehicle approaches.",
              "The wavefronts ahead of the vehicle are closer together, so more reach the observer each second.",
              [("The siren emits more wavefronts each second.", "The siren's own frequency does not change."),
               ("The sound travels faster towards the observer.", "The speed of sound in air is unchanged."),
               ("The sound gets louder as the vehicle gets closer.", "Loudness is not frequency.")])
    ex.choice("A passenger inside the vehicle listens to the siren. What frequency does the passenger hear?", f"{fs} Hz",
              [(f"More than {fs} Hz", "The passenger is not moving relative to the siren."), (f"Less than {fs} Hz", "There is no relative motion."),
               ("It changes as the vehicle passes the observer.", "That happens for the observer, not the passenger.")])
    return ex.build(f"An emergency vehicle sounding a {fs} Hz siren drives at {vs} m/s along a straight road, past an observer standing at the roadside. "
                    "(Speed of sound in air = 340 m/s)")


def galaxy_redshift(level="Higher"):
    ex = _ex(level, "The Expanding Universe", UNIT2)
    rest = pick(410, 434, 486, 656)
    z_true = pick(0.020, 0.035, 0.050, 0.075, 0.12)
    obs = round(rest * (1 + z_true))
    z = (obs - rest) / rest
    ex.num("Calculate the redshift of the light from the galaxy.", z, "",
           wrong=[((obs - rest) / obs, "Divide by the REST wavelength."), (obs / rest, "z = (λ_obs − λ_rest) ÷ λ_rest.")],
           working=[rf"z = \frac{{\lambda_{{obs}} - \lambda_{{rest}}}}{{\lambda_{{rest}}}} = \frac{{{obs} - {rest}}}{{{rest}}} = {ltx(z)}"])
    v = sig(z) * C
    ex.num("Calculate the recessional velocity of the galaxy.", v, "m/s",
           wrong=[(C / sig(z), "v = zc."), ((obs / rest) * C, "Use z, not λ_obs ÷ λ_rest.")],
           working=[rf"z = \frac vc \Rightarrow v = {ltx(z)} \times 3.00\times10^8 = {ltx(v)}\ \text{{m/s}}"])
    d = sig(v) / H0
    ex.num("Calculate the approximate distance to the galaxy.", d, "m",
           wrong=[(sig(v) * H0, "v = H₀d, so d = v ÷ H₀."), (H0 / sig(v), "d = v ÷ H₀.")],
           working=[rf"v = H_0d \Rightarrow d = \frac{{{ltx(v)}}}{{2.3\times10^{{-18}}}} = {ltx(d)}\ \text{{m}}"])
    ly = sig(d) / (C * 365.25 * 24 * 3600)
    ex.num("Express this distance in light-years.", ly, "ly",
           wrong=[(sig(d) / C, "That gives a time in seconds; divide by the number of metres in a light-year."), (sig(d) * C * 365.25 * 24 * 3600, "Divide by the size of a light-year.")],
           working=[r"1\ \text{ly} = 3.00\times10^8 \times 365.25 \times 24 \times 3600 = 9.47\times10^{15}\ \text{m}", rf"d = {ltx(ly)}\ \text{{ly}}"])
    ex.choice("Light from most galaxies is redshifted, and more distant galaxies have greater recessional velocities. What is this evidence for?",
              "The Universe is expanding, which supports the Big Bang theory.",
              [("The Universe is contracting.", "Contraction would give blueshifts."),
               ("Galaxies are cooling as they get older.", "Redshift here is due to recession."),
               ("The Earth is at the centre of the Universe.", "Every observer would see galaxies moving away.")])
    ex.choice("Measurements of the speed of stars around galaxies show there is more mass than can be seen. What is this unseen mass called?", "Dark matter",
              [("Dark energy", "Dark energy is linked to the accelerating expansion."), ("A black body", "A black body is a model of an emitter."),
               ("Antimatter", "The evidence is for mass that emits no detectable radiation.")])
    return ex.build(f"A spectral line that has a wavelength of {rest} nm from a source on Earth is observed at {obs} nm in the light from a distant galaxy. "
                    "(H₀ = 2.3 × 10⁻¹⁸ s⁻¹)")


TOPIC_SCENARIOS_ODU1 = {
    "Balloon and Sandbag":  rising_balloon,
    "Emergency Stop":       emergency_stop,
    "Bouncing Ball Graph":  bouncing_ball_graph,
    "Engine and Carriages": train_carriages,
    "Crate on a Ramp":      crate_on_ramp,
    "Hanging Sign":         hanging_sign,
    "Air Track Collision":  air_track_collision,
    "Ball Hitting a Wall":  impact_force_graph,
    "Roller Coaster":       roller_coaster,
    "Lift and Cable":       lift_and_cable,
}

TOPIC_SCENARIOS_ODU2 = {
    "Weather Satellite":    weather_satellite,
    "Muons":                muon_shower,
    "Passing Siren":        passing_siren,
    "Redshifted Galaxy":    galaxy_redshift,
}
