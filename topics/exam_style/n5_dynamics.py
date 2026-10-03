"""N5 Dynamics — exam-style questions that cut across the unit's topics, like SQA paper questions.

Each scenario follows one context (a car journey, a skydiver, a rocket…) through linked parts, each
tagged with the topic it tests. Recognised wrong answers come from the N5 marking instructions and
course reports: minutes/km/cm not converted, the change in speed not used, the unbalanced force not
found first, ½ or the square root dropped from Ek, and the sign of a deceleration.
"""
import math
import random

from topics.exam_style.base import Exam, T, fmt, graph, ltx, pick, sig

UNIT = "Dynamics"
G = 9.8
C = 3e8
# N5 data sheet gravitational field strengths (N/kg)
PLANET_G = {"Mercury": 3.7, "Venus": 8.9, "Mars": 3.7, "Jupiter": 23, "Saturn": 9.0,
            "Uranus": 8.7, "Neptune": 11, "Moon": 1.6}


def _notes(title, body):
    return f"## {title} — exam technique\n\n{body}"


NOTES = {
    "Speed, Distance & Time": _notes("Speed, distance and time", r"""
$d = \bar{v}t$ — always work in **metres** and **seconds**: km × 1000, minutes × 60, hours × 3600.

- **Average** speed = total distance ÷ total time — include any time spent stopped.
- **Instantaneous** speed is the speed at one moment (light gate: length of card ÷ time to pass through).
- To measure an average speed: measure the distance (metre stick / trundle wheel), time it (stopwatch), use $\bar{v} = d/t$.
"""),
    "Acceleration": _notes("Acceleration", r"""
$a = \frac{v - u}{t}$ — acceleration is the **change in velocity per unit time** (m/s²).

- Use the **change** in speed, $v - u$, not the final speed on its own.
- Slowing down gives a **negative** acceleration.
- Light gates: speed = length of card ÷ time to pass through the gate. A light gate removes human reaction time.
"""),
    "Forces": _notes("Forces", r"""
$F = ma$ — $F$ is the **unbalanced (resultant) force**: find it first.

- Driving force − friction = unbalanced force. Thrust − weight = unbalanced force (vertical).
- Balanced forces → constant speed (or at rest) — Newton's first law.
- Forces at right angles: magnitude by Pythagoras, direction by $\tan\theta = \frac{\text{opp}}{\text{adj}}$, given as a bearing (from north, clockwise).
"""),
    "Vertical Motion": _notes("Vertical motion", r"""
$W = mg$ and $F = ma$ with **unbalanced force = weight − air resistance** (falling) or **thrust − weight** (rising).

- As a skydiver speeds up, air resistance increases until it equals the weight → balanced forces → **terminal velocity**.
- Parachute opens → air resistance greater than weight → unbalanced force **upwards** → the skydiver **slows down** (negative acceleration while moving down).
"""),
    "Weight": _notes("Weight", r"""
$W = mg$ — weight (N) is a force; mass (kg) is the amount of matter and **does not change** from planet to planet.

Data sheet $g$ (N/kg): Earth 9.8, Moon 1.6, Mercury 3.7, Venus 8.9, Mars 3.7, Jupiter 23, Saturn 9.0, Uranus 8.7, Neptune 11.
"""),
    "Energy": _notes("Energy", r"""
$E_p = mgh$ &nbsp; $E_k = \frac{1}{2}mv^2$ &nbsp; $E_w = Fd$ &nbsp; $P = \frac{E}{t}$

- Conservation: Ep lost = Ek gained (if no energy is lost). Then $v = \sqrt{\frac{2E_k}{m}}$ — don't forget the **square root** and the **½**.
- Real speeds are smaller because energy is converted to **heat (and sound)** by friction / air resistance.
- Braking: work done by the brakes = kinetic energy lost, so $d = E_k / F$.
"""),
    "Projectile Motion": _notes("Projectile motion", r"""
**Horizontal:** constant velocity — $d_h = v_h t$. **Vertical:** constant acceleration of 9.8 m/s² from rest — $v_v = at$.

- Height fallen = area under the vertical v–t graph = $\frac{1}{2} v_v t$.
- Horizontal velocity is constant because (ignoring air resistance) there is **no horizontal unbalanced force**.
- The time of flight depends only on the vertical motion.
"""),
    "Distance and Displacement": _notes("Distance and displacement", r"""
**Distance** (scalar) = total length of the path. **Displacement** (vector) = straight line from start to finish, **with a direction**.

- At right angles: magnitude by Pythagoras, direction by $\tan\theta$.
- Give the direction as a **bearing**: measured clockwise from north, as three figures (e.g. 037°).
"""),
    "Vectors and Scalars": _notes("Vectors and scalars", r"""
**Scalar:** magnitude only (distance, speed, mass, time, energy). **Vector:** magnitude **and direction** (displacement, velocity, acceleration, force, weight).

- Average speed = distance ÷ time; average velocity = displacement ÷ time.
- Vectors at right angles combine by Pythagoras; give the direction too.
"""),
    "Speed and Velocity": _notes("Speed and velocity", r"""
Average speed = $\frac{\text{total distance}}{\text{total time}}$ (scalar); average velocity = $\frac{\text{displacement}}{\text{total time}}$ (vector — give a direction).

- Resultant velocity: add velocities at right angles with Pythagoras; direction with $\tan\theta$ as a bearing.
"""),
    "Velocity-Time Graphs": _notes("Velocity–time graphs", r"""
- **Gradient** = acceleration: $a = \frac{v - u}{t}$ for one straight section.
- **Area under** the graph = distance travelled (split into rectangles and triangles).
- Horizontal line = constant velocity = **balanced forces** (zero unbalanced force).
- Average speed for the journey = total area ÷ total time.
"""),
}


NOTES["Definitions"] = ""


def _ex(level):
    return Exam(UNIT, level, NOTES)


def _bearing(east, north):
    return math.degrees(math.atan2(east, north)) % 360


def _bearing_text(b):
    return f"{b:05.1f}°" if b < 100 else f"{b:.1f}°"


# ════════════════ Car journey: v–t graph → acceleration → F = ma → Ek → braking distance ════════════════

def car_journey(level="N5"):
    ex = _ex(level)
    m = pick(900, 1000, 1200, 1400)
    v, t1, t2, t3 = pick(12, 15, 16, 20), pick(4, 5, 8), pick(10, 12, 15), pick(3, 4, 5)
    T1, T2, T3 = t1, t1 + t2, t1 + t2 + t3
    fig = graph([(0, 0), (T1, v), (T2, v), (T3, 0)], labels=["O", "A", "B", "C"])
    a = v / t1
    ex.on("Velocity-Time Graphs").num("Use the graph to calculate the acceleration of the car between O and A.", a, "m/s²",
        wrong=[(t1 / v, "a = change in velocity ÷ time."), (v * t1, "Acceleration is the GRADIENT, not the area.")],
        working=[r"a = \frac{v - u}{t}", rf"a = \frac{{{v} - 0}}{{{t1}}} = {ltx(a)}\ \text{{m/s}}^2"])
    F = m * sig(a)
    ex.on("Forces").num(f"The mass of the car is {m} kg. Calculate the unbalanced force on the car between O and A.", F, "N",
        wrong=[(m / sig(a), "F = m × a."), (m * G, "That's the weight, not the unbalanced force.")],
        working=[r"F = ma", rf"F = {m} \times {ltx(a)} = {ltx(F)}\ \text{{N}}"])
    ex.on("Forces").choice("Between A and B the car travels at a constant velocity. Which statement is correct?",
        "The driving force is equal to the frictional forces — the forces are balanced.",
        [("The driving force is greater than the frictional forces.", "That would make the car accelerate."),
         ("There are no forces acting on the car.", "Forces act, but they are balanced (Newton's first law)."),
         ("The driving force is zero.", "A driving force is still needed to balance friction.")])
    dist = 0.5 * v * t1 + v * t2 + 0.5 * v * t3
    ex.on("Velocity-Time Graphs").num("Calculate the total distance travelled by the car.", dist, "m",
        wrong=[(v * T3, "The first and last sections are triangles: ½ × base × height."), (v * t2, "Include all three sections.")],
        working=[r"d = \text{area under graph}",
                 rf"d = (\tfrac{{1}}{{2}} \times {t1} \times {v}) + ({t2} \times {v}) + (\tfrac{{1}}{{2}} \times {t3} \times {v}) = {ltx(dist)}\ \text{{m}}"])
    Ek = 0.5 * m * v ** 2
    ex.on("Energy").num("Calculate the kinetic energy of the car between A and B.", Ek, "J",
        wrong=[(m * v ** 2, "Ek = ½mv² — don't forget the ½."), (0.5 * m * v, "Square the speed.")],
        working=[r"E_k = \tfrac{1}{2}mv^2", rf"E_k = 0.5 \times {m} \times {v}^2 = {ltx(Ek)}\ \text{{J}}"])
    d3 = 0.5 * v * t3
    Fb = sig(Ek) / d3
    ex.on("Energy").num(f"The car stops between B and C, travelling {fmt(d3)} m. Calculate the average braking force.", Fb, "N",
        wrong=[(sig(Ek) * d3, "Ew = Fd, so F = Ew ÷ d."), (m * v / t3 * 2, "Use the work done: all the Ek is transferred by the brakes.")],
        working=[r"E_w = E_k = Fd", rf"F = \frac{{{ltx(Ek)}}}{{{fmt(d3)}}} = {ltx(Fb)}\ \text{{N}}"])
    return ex.build("The graph shows how the velocity of a car changes during a short journey.", figure=fig)


# ════════════════ Skydiver: weight → acceleration → terminal velocity → parachute ════════════════

def skydiver(level="N5"):
    ex = _ex(level)
    m = pick(65, 72, 80, 85, 90)
    W = m * G
    ex.on("Weight").num("Calculate the weight of the skydiver.", W, "N",
        wrong=[(m, "Weight = mg (a force, in N)."), (m / G, "W = m × g.")],
        working=[r"W = mg", rf"W = {m} \times 9.8 = {ltx(W)}\ \text{{N}}"])
    R = sig(W * random.uniform(0.3, 0.7), 2)
    a = (sig(W) - R) / m
    ex.on("Vertical Motion").num(f"At one point the air resistance on the skydiver is {fmt(R)} N. Calculate her acceleration at this point.",
        a, "m/s²",
        wrong=[(R / m, "Use the UNBALANCED force: weight − air resistance."), (G, "Air resistance reduces the acceleration."),
               ((sig(W) + R) / m, "Air resistance acts UPWARDS — subtract it.")],
        working=[rf"F_{{un}} = {ltx(W)} - {fmt(R)} = {ltx(sig(W) - R)}\ \text{{N}}", r"a = \frac{F}{m}", rf"a = {ltx(a)}\ \text{{m/s}}^2"])
    ex.on("Vertical Motion").choice("Later, she falls at a constant speed. Explain why.",
        "Air resistance increases with speed until it equals her weight; the forces are balanced, so the speed is constant.",
        [("Gravity stops acting at high speed.", "Her weight still acts — it is balanced by air resistance."),
         ("Air resistance is greater than her weight.", "Then she would slow down."),
         ("She has run out of energy to accelerate.", "Balanced forces → constant speed.")])
    v1, v2, t = pick(50, 55, 60), pick(5, 6, 8), pick(2.0, 2.5, 3.0, 4.0)
    a2 = (v2 - v1) / t
    ex.on("Acceleration").num(f"When her parachute opens, her speed falls from {v1} m/s to {v2} m/s in {t:g} s. "
        f"Calculate her acceleration (take downwards as positive).", a2, "m/s²",
        wrong=[(-a2, "She slows down — the acceleration is NEGATIVE."), (v2 / t, "Use the change in speed (v − u).")],
        working=[r"a = \frac{v - u}{t}", rf"a = \frac{{{v2} - {v1}}}{{{t:g}}} = {ltx(a2)}\ \text{{m/s}}^2"])
    Fun = m * abs(sig(a2))
    Rp = Fun + sig(W)
    ex.on("Vertical Motion").num("Calculate the air resistance acting on her while she slows down.", Rp, "N",
        wrong=[(Fun, "That's the unbalanced force. Air resistance = unbalanced force + weight."),
               (abs(Fun - sig(W)), "Air resistance must be GREATER than the weight to slow her: add them.")],
        working=[rf"F_{{un}} = ma = {m} \times {ltx(abs(a2))} = {ltx(Fun)}\ \text{{N}}", r"F_{un} = R - W \Rightarrow R = F_{un} + W",
                 rf"R = {ltx(Fun)} + {ltx(W)} = {ltx(Rp)}\ \text{{N}}"],
        scaffold=[("Size of the unbalanced force, in N?", Fun, "N")])
    return ex.build(f"A skydiver of mass {m} kg (including equipment) jumps from an aircraft.")


# ════════════════ Mission to another planet: weight → lift-off → g → signals ════════════════

def space_mission(level="N5"):
    ex = _ex(level)
    m = pick(2.0e4, 2.4e4, 3.2e4, 5.0e4)
    W = m * G
    thrust = sig(W * random.uniform(1.4, 2.0), 2)
    ex.on("Weight").num("Calculate the weight of the rocket on Earth.", W, "N",
        wrong=[(m, "W = mg."), (m / G, "W = m × g.")],
        working=[rf"W = mg = {fmt(m)} \times 9.8 = {ltx(W)}\ \text{{N}}"])
    a = (thrust - sig(W)) / m
    ex.on("Forces").num(f"The engines produce a thrust of {fmt(thrust)} N. Calculate the initial acceleration of the rocket.", a, "m/s²",
        wrong=[(thrust / m, "Find the unbalanced force first: thrust − weight."), ((thrust + sig(W)) / m, "Weight acts against the thrust.")],
        working=[rf"F_{{un}} = {ltx(thrust)} - {ltx(W)} = {ltx(thrust - sig(W))}\ \text{{N}}", rf"a = \frac{{F}}{{m}} = {ltx(a)}\ \text{{m/s}}^2"],
        scaffold=[("Unbalanced force, in N?", thrust - sig(W), "N")])
    ex.on("Forces").choice("The thrust stays constant as the rocket climbs. What happens to its acceleration?",
        "It increases, because fuel is burned so the mass of the rocket decreases.",
        [("It stays constant, because the thrust is constant.", "a = F/m and the mass is decreasing."),
         ("It decreases, because air resistance disappears.", "Less air resistance would increase a."),
         ("It decreases, because the rocket gets heavier.", "The rocket loses mass as fuel burns.")])
    mp = pick(240, 450, 600, 900)
    planet = pick("Venus", "Jupiter", "Saturn", "Neptune", "Moon")
    g = PLANET_G[planet]
    Wp = mp * g
    ex.on("Weight").num(f"A probe of mass {mp} kg lands on a planet where its weight is {fmt(Wp)} N. Calculate the gravitational field strength there.",
        g, "N/kg", wrong=[(mp / Wp, "g = W ÷ m."), (Wp * mp, "g = W ÷ m.")],
        working=[rf"g = \frac{{W}}{{m}} = \frac{{{fmt(Wp)}}}{{{mp}}} = {ltx(g)}\ \text{{N/kg}}"])
    wrong = random.sample([p for p in PLANET_G if abs(PLANET_G[p] - g) > 0.5], 3)
    ex.on("Weight").choice("Use the data sheet to identify where the probe has landed.", planet,
        [(p, f"g on {p} is {PLANET_G[p]:g} N/kg.") for p in wrong])
    mins = pick(4, 8, 12, 20, 35)
    D = C * mins * 60
    ex.on("Speed, Distance & Time").num(f"Radio signals from the probe take {mins} minutes to reach Earth. Calculate the distance from the probe to Earth.",
        D, "m", wrong=[(C * mins, "Convert minutes to seconds."), (C / (mins * 60), "d = v × t.")],
        working=[rf"d = vt = 3 \times 10^8 \times ({mins} \times 60) = {ltx(D)}\ \text{{m}}"])
    return ex.build(f"A rocket of mass {fmt(m)} kg launches a space probe. Radio signals travel at 3.0 × 10⁸ m/s.")


# ════════════════ Ski jump: Ep → speed → projectile ════════════════

def ski_jump(level="N5"):
    ex = _ex(level)
    m, h = pick(55, 60, 70, 75), pick(5.0, 7.2, 8.0, 11.25)
    Ep = m * G * h
    ex.on("Energy").num("Calculate the gravitational potential energy lost by the skier on the ramp.", Ep, "J",
        wrong=[(m * h, "Ep = mgh."), (m * G / h, "Ep = m × g × h.")],
        working=[rf"E_p = mgh = {m} \times 9.8 \times {h:g} = {ltx(Ep)}\ \text{{J}}"])
    v = math.sqrt(2 * sig(Ep) / m)
    ex.on("Energy").num("Assuming no energy is lost, calculate the skier's speed at the end of the ramp.", v, "m/s",
        wrong=[(2 * sig(Ep) / m, "Take the square root: v = √(2Ek/m)."), (math.sqrt(sig(Ep) / m), "Ek = ½mv², so v = √(2Ek ÷ m).")],
        working=[r"E_k = E_p = \tfrac{1}{2}mv^2", rf"v = \sqrt{{\frac{{2 \times {ltx(Ep)}}}{{{m}}}}} = {ltx(v)}\ \text{{m/s}}"])
    ex.on("Energy").choice("Her actual speed is less than this. Why?",
        "Some energy is converted to heat (and sound) by friction and air resistance.",
        [("Energy is destroyed on the ramp.", "Energy is converted, never destroyed."),
         ("Her mass increases as she speeds up.", "Her mass doesn't change."),
         ("Ep can't be converted into Ek.", "It can — but some becomes heat too.")])
    vh, t = pick(8, 10, 12), pick(1.2, 1.5, 2.0)
    ex.on("Projectile Motion").num(f"She leaves the horizontal end of the ramp at {vh} m/s and is in the air for {t:g} s. "
        f"Calculate the horizontal distance she travels in the air.", vh * t, "m",
        wrong=[(0.5 * vh * t, "Horizontal velocity is constant — no ½."), (vh / t, "d = v × t.")],
        working=[rf"d_h = v_h t = {vh} \times {t:g} = {ltx(vh * t)}\ \text{{m}}"])
    vv = G * t
    ex.on("Projectile Motion").num("Calculate her vertical velocity just before she lands.", vv, "m/s",
        wrong=[(vh, "Vertical velocity starts at zero and increases at 9.8 m/s²."), (G / t, "v = u + at.")],
        working=[rf"v_v = u + at = 0 + 9.8 \times {t:g} = {ltx(vv)}\ \text{{m/s}}"])
    ex.on("Projectile Motion").choice("Why does her horizontal velocity stay constant while she is in the air (ignoring air resistance)?",
        "There is no unbalanced horizontal force acting on her.",
        [("Gravity acts horizontally.", "Gravity acts vertically."), ("The ramp keeps pushing her.", "Once airborne there's no horizontal force."),
         ("Her weight balances her velocity.", "Forces can't balance a velocity.")])
    return ex.build(f"A ski jumper of mass {m} kg starts from rest at the top of a ramp {h:g} m high.")


# ════════════════ Orienteering: distance, displacement, speed, velocity ════════════════

def orienteering(level="N5"):
    ex = _ex(level)
    e, n = random.choice([(1200, 900), (2400, 1000), (1600, 1200), (800, 1500), (3000, 4000), (1500, 2000)])
    t1, t2 = pick(300, 400, 480, 600), pick(240, 300, 360, 450)
    t = t1 + t2
    s = math.hypot(e, n)
    brg = _bearing(e, n)
    ex.on("Distance and Displacement").num("Calculate the total distance travelled.", e + n, "m",
        wrong=[(s, "That's the displacement. Distance is the total path length.")],
        working=[rf"d = {e} + {n} = {e + n}\ \text{{m}}"])
    ex.on("Distance and Displacement").num("Calculate the size of the runner's displacement.", s, "m",
        wrong=[(e + n, "Displacement is the straight line from start to finish — use Pythagoras."), (abs(e - n), "Use Pythagoras.")],
        working=[rf"s = \sqrt{{{e}^2 + {n}^2}} = {ltx(s)}\ \text{{m}}"])
    ex.on("Distance and Displacement").num("Calculate the direction of the displacement as a bearing (in degrees).", brg, "",
        wrong=[(90 - brg, "Bearings are measured clockwise from NORTH.")],
        working=[rf"\tan\theta = \frac{{{e}}}{{{n}}}", rf"\theta = {brg:.1f}^\circ", T(f"Bearing {_bearing_text(brg)}")])
    ex.on("Speed and Velocity").num("Calculate the runner's average speed.", (e + n) / t, "m/s",
        wrong=[(s / t, "Average SPEED uses the total distance."), ((e / t1 + n / t2) / 2, "Use total distance ÷ total time.")],
        working=[rf"\bar{{v}} = \frac{{{e + n}}}{{{t}}} = {ltx((e + n) / t)}\ \text{{m/s}}"])
    ex.on("Speed and Velocity").num("Calculate the size of the runner's average velocity.", sig(s) / t, "m/s",
        wrong=[((e + n) / t, "Average VELOCITY uses the displacement.")],
        working=[rf"\bar{{v}} = \frac{{s}}{{t}} = \frac{{{ltx(s)}}}{{{t}}} = {ltx(sig(s) / t)}\ \text{{m/s}}"])
    ex.on("Vectors and Scalars").choice("Which pair shows a scalar quantity followed by its vector equivalent?",
        "speed, velocity",
        [("velocity, speed", "Speed is the scalar; velocity is the vector."), ("displacement, distance", "Distance is the scalar."),
         ("force, mass", "Mass is a scalar and force is a vector — but they aren't equivalents.")])
    return ex.build(f"In an orienteering event, a runner runs {e} m due east in {t1} s, then {n} m due north in {t2} s.")


# ════════════════ Supply drop: resultant velocity → projectile ════════════════

def supply_drop(level="N5"):
    ex = _ex(level)
    vp, vw = random.choice([(80, 15), (60, 11), (90, 20), (120, 22)])
    R = math.hypot(vp, vw)
    brg = _bearing(vw, vp)
    ex.on("Speed and Velocity").num("Calculate the size of the aircraft's resultant velocity.", R, "m/s",
        wrong=[(vp + vw, "The velocities are at right angles — use Pythagoras."), (vp - vw, "Use Pythagoras.")],
        working=[rf"v = \sqrt{{{vp}^2 + {vw}^2}} = {ltx(R)}\ \text{{m/s}}"])
    ex.on("Vectors and Scalars").num("Calculate the direction of the resultant velocity as a bearing (in degrees).", brg, "",
        wrong=[(90 - brg, "Measure the bearing clockwise from north.")],
        working=[rf"\tan\theta = \frac{{{vw}}}{{{vp}}}", rf"\theta = {brg:.1f}^\circ", T(f"Bearing {_bearing_text(brg)}")])
    t = pick(3.0, 4.0, 5.0, 6.0)
    vv = G * t
    ex.on("Projectile Motion").num(f"A package is dropped and takes {t:g} s to reach the ground. Calculate its vertical velocity just "
        f"before it lands (ignore air resistance).", vv, "m/s",
        wrong=[(G / t, "v = u + at."), (R, "The vertical velocity starts at zero.")],
        working=[rf"v_v = 0 + 9.8 \times {t:g} = {ltx(vv)}\ \text{{m/s}}"])
    h = 0.5 * vv * t
    ex.on("Projectile Motion").num("Calculate the height from which the package was dropped.", h, "m",
        wrong=[(vv * t, "The vertical v–t graph is a triangle: area = ½ × t × v.")],
        working=[rf"h = \tfrac{{1}}{{2}} \times {t:g} \times {ltx(vv)} = {ltx(h)}\ \text{{m}}"])
    ex.on("Projectile Motion").choice("Ignoring air resistance, where is the aircraft when the package lands?",
        "Directly above the package — they have the same horizontal velocity.",
        [("Behind the package.", "The package doesn't speed up horizontally."),
         ("Above the point where the package was released.", "The aircraft has moved on."),
         ("Far ahead of the package.", "The package keeps the aircraft's horizontal velocity.")])
    return ex.build(f"An aircraft heads due north at {vp} m/s relative to the air. A wind blows due east at {vw} m/s.")


# ════════════════ Trolley on a slope: light gates → acceleration → force → energy ════════════════

def trolley(level="N5"):
    ex = _ex(level)
    L = pick(5.0, 8.0, 10.0)
    t1 = sig(L / 100 / random.uniform(0.35, 0.6), 3)
    t2 = sig(L / 100 / random.uniform(0.9, 1.4), 3)
    dt = pick(0.6, 0.75, 0.8, 1.2)
    m = pick(0.5, 0.75, 0.8, 1.2)
    v1, v2 = L / 100 / t1, L / 100 / t2
    ex.on("Speed, Distance & Time").num("Calculate the instantaneous speed of the trolley at light gate 1.", v1, "m/s",
        wrong=[(L / t1, "Convert the card length to metres."), (t1 / (L / 100), "v = d ÷ t.")],
        working=[rf"v = \frac{{d}}{{t}} = \frac{{{L / 100:g}}}{{{t1:g}}} = {ltx(v1)}\ \text{{m/s}}"])
    ex.on("Speed, Distance & Time").num("Calculate the instantaneous speed of the trolley at light gate 2.", v2, "m/s",
        wrong=[(L / t2, "Convert the card length to metres.")],
        working=[rf"v = \frac{{{L / 100:g}}}{{{t2:g}}} = {ltx(v2)}\ \text{{m/s}}"])
    a = (sig(v2) - sig(v1)) / dt
    ex.on("Acceleration").num("Calculate the acceleration of the trolley.", a, "m/s²",
        wrong=[(sig(v2) / dt, "Use the CHANGE in speed."), ((sig(v2) - sig(v1)) / (t1 + t2), f"Use the time BETWEEN the gates ({dt:g} s).")],
        working=[r"a = \frac{v - u}{t}", rf"a = \frac{{{ltx(v2)} - {ltx(v1)}}}{{{dt:g}}} = {ltx(a)}\ \text{{m/s}}^2"])
    F = m * sig(a)
    ex.on("Forces").num(f"The trolley has a mass of {m:g} kg. Calculate the unbalanced force on it.", F, "N",
        wrong=[(m * G, "That's the weight."), (m / sig(a), "F = m × a.")],
        working=[rf"F = ma = {m:g} \times {ltx(a)} = {ltx(F)}\ \text{{N}}"])
    dEk = 0.5 * m * (sig(v2) ** 2 - sig(v1) ** 2)
    ex.on("Energy").num("Calculate the kinetic energy gained by the trolley between the gates.", dEk, "J",
        wrong=[(0.5 * m * (sig(v2) - sig(v1)) ** 2, "Find each Ek, then subtract — don't square the change in speed."),
               (0.5 * m * sig(v2) ** 2, "Subtract the Ek at gate 1.")],
        working=[rf"E_{{k1}} = \tfrac{{1}}{{2}} \times {m:g} \times {ltx(v1)}^2", rf"E_{{k2}} = \tfrac{{1}}{{2}} \times {m:g} \times {ltx(v2)}^2",
                 rf"\Delta E_k = {ltx(dEk)}\ \text{{J}}"])
    ex.on("Acceleration").choice("Why are light gates used rather than a stopwatch?",
        "The times are very short; light gates remove human reaction time, so they are more accurate.",
        [("Light gates measure the distance too.", "The card length is measured with a ruler."),
         ("A stopwatch can't measure times under 10 s.", "The issue is reaction time."),
         ("Light gates make the acceleration more uniform.", "They don't affect the motion.")])
    return ex.build(f"A trolley runs down a slope through two light gates. A {L:g} cm card on the trolley blocks gate 1 for {t1:g} s "
                    f"and gate 2 for {t2:g} s. It takes {dt:g} s to travel between the gates.")


# ════════════════ Crane: weight → Ep → power → lifting force ════════════════

def crane(level="N5"):
    ex = _ex(level)
    m, h, t = pick(250, 400, 500, 800), pick(12, 15, 20, 30), pick(20, 25, 30, 40)
    W = m * G
    ex.on("Weight").num("Calculate the weight of the load.", W, "N", wrong=[(m, "W = mg.")],
        working=[rf"W = mg = {m} \times 9.8 = {ltx(W)}\ \text{{N}}"])
    Ep = sig(W) * h
    ex.on("Energy").num(f"The load is lifted {h} m. Calculate the gravitational potential energy it gains.", Ep, "J",
        wrong=[(m * h, "Ep = mgh."), (sig(W) / h, "Ep = mgh.")],
        working=[rf"E_p = mgh = {m} \times 9.8 \times {h} = {ltx(Ep)}\ \text{{J}}"])
    P = sig(Ep) / t
    ex.on("Energy").num(f"The lift takes {t} s. Calculate the minimum power output of the crane's motor.", P, "W",
        wrong=[(sig(Ep) * t, "P = E ÷ t.")], working=[rf"P = \frac{{E}}{{t}} = \frac{{{ltx(Ep)}}}{{{t}}} = {ltx(P)}\ \text{{W}}"])
    a = pick(0.2, 0.4, 0.5)
    T_ = m * (G + a)
    ex.on("Vertical Motion").num(f"At the start of the lift the load accelerates upwards at {a:g} m/s². Calculate the tension in the cable.",
        T_, "N",
        wrong=[(m * a, "Tension − weight = ma, so tension = ma + weight."), (sig(W), "The load accelerates, so the tension is more than the weight."),
               (m * (G - a), "Accelerating UPWARDS needs tension GREATER than the weight.")],
        working=[r"T - W = ma", rf"T = {m} \times {a:g} + {ltx(W)} = {ltx(T_)}\ \text{{N}}"])
    return ex.build(f"A crane lifts a load of mass {m} kg vertically.")


SCENARIOS = {
    "Car Journey":     car_journey,
    "Skydiver":        skydiver,
    "Space Mission":   space_mission,
    "Ski Jump":        ski_jump,
    "Orienteering":    orienteering,
    "Supply Drop":     supply_drop,
    "Trolley on a Slope": trolley,
    "Crane":           crane,
}
