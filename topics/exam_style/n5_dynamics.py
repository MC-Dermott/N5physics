"""N5 Dynamics — exam-style multi-part questions, one generator per topic.

Each scenario follows an SQA paper pattern: one context, two to four linked parts (a calculation
whose answer feeds the next, then a state/explain part asked as multiple choice). Recognised wrong
answers come from the N5 marking instructions and course reports: minutes/km/cm not converted,
the change in speed not used, the unbalanced force not found first, ½ or the square root dropped
from Ek, and a negative acceleration given for a deceleration (or vice versa).
"""
import math
import random

from topics.dynamics.energy_power import generate_power_exam
from topics.exam_style.base import Exam, T, exam_style, fmt, graph, ltx, pick, reuse, sig

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


def _ex(qtype, level):
    return Exam(UNIT, qtype, level, NOTES[qtype])


def _bearing(east, north):
    return math.degrees(math.atan2(east, north)) % 360


def _bearing_text(b):
    return f"{b:05.1f}°" if b < 100 else f"{b:.1f}°"


# ════════════════ Speed, Distance & Time ════════════════

def _sdt_train(level="N5"):
    ex = _ex("Speed, Distance & Time", level)
    d1, t1 = pick(12, 18, 24, 30, 36), pick(10, 12, 15, 20)
    d2, t2 = pick(9, 15, 21, 27), pick(8, 10, 14, 18)
    stop = pick(2, 3, 4, 5)
    v1 = d1 * 1000 / (t1 * 60)
    ex.num(f"Calculate the average speed of the train between A and B, in m/s.", v1, "m/s",
           wrong=[(d1 * 1000 / t1, "Convert the time to seconds: minutes × 60."),
                  (d1 / (t1 * 60), "Convert the distance to metres: km × 1000."),
                  (d1 / t1, "Work in metres and seconds.")],
           working=[r"\bar{v} = \frac{d}{t}", rf"\bar{{v}} = \frac{{{d1} \times 1000}}{{{t1} \times 60}}",
                    rf"\bar{{v}} = {ltx(v1)}\ \text{{m/s}}"],
           scaffold=[("Distance in metres?", d1 * 1000, "m"), ("Time in seconds?", t1 * 60, "s")])
    total_t = (t1 + stop + t2) * 60
    v = (d1 + d2) * 1000 / total_t
    ex.num("Calculate the average speed of the train for the whole journey from A to C, including the stop at B.",
           v, "m/s",
           wrong=[((d1 + d2) * 1000 / ((t1 + t2) * 60), "Average speed uses the TOTAL time — include the time stopped at B."),
                  ((v1 + d2 * 1000 / (t2 * 60)) / 2, "Don't average the two speeds — use total distance ÷ total time.")],
           working=[rf"d = ({d1} + {d2}) \times 1000 = {(d1 + d2) * 1000}\ \text{{m}}",
                    rf"t = ({t1} + {stop} + {t2}) \times 60 = {total_t}\ \text{{s}}",
                    rf"\bar{{v}} = \frac{{d}}{{t}} = \frac{{{(d1 + d2) * 1000}}}{{{total_t}}} = {ltx(v)}\ \text{{m/s}}"],
           scaffold=[("Total distance in metres?", (d1 + d2) * 1000, "m"), ("Total time in seconds, including the stop?", total_t, "s")])
    ex.choice("The train's speedometer showed a top speed between A and B that was greater than your answer to Part 1. "
              "Which statement explains this?",
              "The train's speed changes during the journey; the average speed is total distance ÷ total time, "
              "so at some instants the train is moving faster than its average speed.",
              [("The speedometer is inaccurate.", "Average and instantaneous speeds are different quantities — they needn't match."),
               ("Average speed is always the top speed divided by two.", "Average speed = total distance ÷ total time."),
               ("The train must have travelled a greater distance than measured.", "The distance is fixed — the speed varies during the journey.")])
    return ex.build(f"A train travels {d1} km from station A to station B in {t1} minutes. It stops at B for "
                    f"{stop} minutes, then travels a further {d2} km to station C in {t2} minutes.")


def _sdt_runner(level="N5"):
    ex = _ex("Speed, Distance & Time", level)
    d = pick(100, 200, 400)
    v_true = random.uniform(5.5, 8.0) if d <= 200 else random.uniform(5.0, 6.5)
    t = round(d / v_true, 1)
    v = d / t
    ex.num(f"Calculate the runner's average speed.", v, "m/s",
           wrong=[(t / d, "Speed = distance ÷ time, not time ÷ distance."), (d * t, "Divide the distance by the time.")],
           working=[r"\bar{v} = \frac{d}{t}", rf"\bar{{v}} = \frac{{{d}}}{{{t:g}}}", rf"\bar{{v}} = {ltx(v)}\ \text{{m/s}}"])
    D = pick(800, 1500, 3000)
    tD = D / sig(v)
    ex.num(f"The runner says they could keep up this average speed for a {D} m race. Calculate the time "
           f"they would take.", tD, "s",
           wrong=[(D * sig(v), "t = d ÷ v̄ — divide the distance by the speed."), (D / sig(v) / 60, "Give the time in seconds.")],
           working=[r"t = \frac{d}{\bar{v}}", rf"t = \frac{{{D}}}{{{ltx(v)}}}", rf"t = {ltx(tD)}\ \text{{s}}"])
    ex.choice("Which method should the pupils have used to measure the runner's average speed?",
              "Measure the length of the course with a measuring tape, time the run from start to finish with a "
              "stopwatch, then divide the distance by the time.",
              [("Place a single light gate at the finish line and record the time it is blocked.",
                "A light gate at one point measures an INSTANTANEOUS speed, not the average over the course."),
               ("Time the run with a stopwatch and multiply the time by the distance.", "Average speed = distance ÷ time."),
               ("Measure the runner's top speed with a speed gun.", "That is an instantaneous speed, not the average.")])
    return ex.build(f"Pupils time a runner over a {d} m course. The runner takes {t:g} s.")


def _sdt_rover(level="N5"):
    ex = _ex("Speed, Distance & Time", level)
    v_cm = pick(3.0, 4.2, 5.0, 6.5)
    hrs = pick(1.5, 2, 2.5, 3)
    d = v_cm / 100 * hrs * 3600
    ex.num(f"The rover travels at an average speed of {v_cm:g} cm/s for {hrs:g} hours. "
           f"Calculate the distance it travels, in metres.", d, "m",
           wrong=[(v_cm * hrs * 3600, "Convert cm/s to m/s first (÷ 100)."),
                  (v_cm / 100 * hrs, "Convert the time to seconds: hours × 3600."),
                  (v_cm / 100 * hrs * 60, "1 hour = 3600 s, not 60 s.")],
           working=[rf"\bar{{v}} = {v_cm:g}\ \text{{cm/s}} = {v_cm / 100:g}\ \text{{m/s}}",
                    rf"t = {hrs:g} \times 3600 = {hrs * 3600:g}\ \text{{s}}",
                    r"d = \bar{v}t", rf"d = {v_cm / 100:g} \times {hrs * 3600:g} = {ltx(d)}\ \text{{m}}"],
           scaffold=[("Speed in m/s?", v_cm / 100, "m/s"), ("Time in seconds?", hrs * 3600, "s")])
    mins = pick(4, 6, 8, 12, 15, 20)
    D = C * mins * 60
    ex.num(f"Radio signals from the rover take {mins} minutes to reach Earth. Calculate the distance between the "
           f"rover and Earth at that time.", D, "m",
           wrong=[(C * mins, "Convert the time to seconds: minutes × 60."), (C / (mins * 60), "d = v × t — multiply.")],
           working=[r"d = vt", rf"d = 3 \times 10^8 \times ({mins} \times 60)", rf"d = {ltx(D)}\ \text{{m}}"])
    ex.choice("Why can't engineers on Earth steer the rover around obstacles in real time?",
              "Radio signals take several minutes to travel between Earth and Mars, so commands would arrive too late.",
              [("Radio waves travel slower than sound in space.", "Radio waves travel at 3 × 10⁸ m/s — sound cannot travel in space at all."),
               ("Radio waves cannot travel through a vacuum.", "All electromagnetic waves travel through a vacuum."),
               ("The rover moves too fast to be controlled.", "The rover moves very slowly — the problem is the signal travel time.")])
    return ex.build("A rover explores the surface of Mars, controlled by engineers on Earth. Radio signals travel at 3.0 × 10⁸ m/s.")


gen_sdt_exam = exam_style(_sdt_train, _sdt_runner, _sdt_rover)


# ════════════════ Acceleration ════════════════

def _acc_car(level="N5"):
    ex = _ex("Acceleration", level)
    u, a, t = pick(4, 5, 8, 10), pick(1.5, 2.0, 2.5, 3.0), pick(4, 5, 6, 8)
    v = u + a * t
    ex.num("Calculate the acceleration of the car.", a, "m/s²",
           wrong=[(v / t, "Use the CHANGE in speed (v − u), not the final speed."),
                  ((u + v) / t, "a = (v − u) ÷ t — subtract the initial speed."),
                  (t / (v - u), "a = (v − u) ÷ t, not t ÷ (v − u).")],
           working=[r"a = \frac{v - u}{t}", rf"a = \frac{{{v:g} - {u}}}{{{t}}}", rf"a = {ltx(a)}\ \text{{m/s}}^2"])
    t2 = pick(3, 4, 5, 6)
    a2 = -v / t2
    ex.num(f"The driver then brakes and the car comes to rest in {t2} s. Calculate the acceleration of the car "
           f"while it is braking.", a2, "m/s²",
           wrong=[(v / t2, "The car is slowing down, so its acceleration is NEGATIVE."),
                  (-t2 / v, "a = (v − u) ÷ t.")],
           working=[r"a = \frac{v - u}{t}", rf"a = \frac{{0 - {v:g}}}{{{t2}}}", rf"a = {ltx(a2)}\ \text{{m/s}}^2"])
    V = pick(20, 24, 25, 30)
    tt = V / a
    ex.num(f"On a test track the car accelerates from rest at the same rate as in Part 1. Calculate the time it takes "
           f"to reach {V} m/s.", tt, "s",
           wrong=[(V * a, "Rearrange a = (v − u)/t for t: t = (v − u) ÷ a."), (a / V, "t = (v − u) ÷ a.")],
           working=[r"t = \frac{v - u}{a}", rf"t = \frac{{{V} - 0}}{{{ltx(a)}}}", rf"t = {ltx(tt)}\ \text{{s}}"])
    return ex.build(f"A car travelling at {u} m/s accelerates uniformly to {v:g} m/s in {t} s.")


def _acc_trolley(level="N5"):
    ex = _ex("Acceleration", level)
    L = pick(5.0, 6.0, 8.0, 10.0)
    t1 = sig(L / 100 / random.uniform(0.35, 0.6), 3)
    t2 = sig(L / 100 / random.uniform(0.9, 1.4), 3)
    dt = pick(0.6, 0.75, 0.8, 0.9, 1.2)
    v1, v2 = L / 100 / t1, L / 100 / t2
    a = (v2 - v1) / dt
    ex.num("Calculate the speed of the trolley as it passes through light gate 1.", v1, "m/s",
           wrong=[(L / t1, "Convert the card length to metres (÷ 100)."), (t1 / (L / 100), "v = d ÷ t.")],
           working=[r"v = \frac{d}{t}", rf"v = \frac{{{L / 100:g}}}{{{t1:g}}}", rf"v = {ltx(v1)}\ \text{{m/s}}"])
    ex.num("Calculate the speed of the trolley as it passes through light gate 2.", v2, "m/s",
           wrong=[(L / t2, "Convert the card length to metres (÷ 100).")],
           working=[r"v = \frac{d}{t}", rf"v = \frac{{{L / 100:g}}}{{{t2:g}}}", rf"v = {ltx(v2)}\ \text{{m/s}}"])
    ex.num("Calculate the acceleration of the trolley.", a, "m/s²",
           wrong=[(v2 / dt, "Use the CHANGE in speed between the gates (v − u)."),
                  ((v2 - v1) / (t1 + t2), f"Use the time to travel BETWEEN the gates ({dt:g} s), not the times the card blocks them."),
                  ((v2 - v1) * dt, "a = (v − u) ÷ t.")],
           working=[r"a = \frac{v - u}{t}", rf"a = \frac{{{ltx(v2)} - {ltx(v1)}}}{{{dt:g}}}", rf"a = {ltx(a)}\ \text{{m/s}}^2"],
           scaffold=[("Change in speed, in m/s?", v2 - v1, "m/s")])
    ex.choice("Why are light gates used rather than a stopwatch to time the card?",
              "The times are very short; light gates remove human reaction time, so the times are more accurate.",
              [("Light gates measure the distance as well as the time.", "The card length is measured separately with a ruler."),
               ("A stopwatch cannot measure times less than 10 s.", "The problem is reaction time, not the stopwatch's range."),
               ("Light gates make the trolley accelerate more uniformly.", "Light gates don't affect the trolley's motion.")])
    return ex.build(f"A trolley runs down a slope through two light gates. A card of length {L:g} cm on the trolley "
                    f"blocks light gate 1 for {t1:g} s and light gate 2 for {t2:g} s. The trolley takes {dt:g} s to "
                    f"travel from gate 1 to gate 2.")


def _acc_cyclist(level="N5"):
    ex = _ex("Acceleration", level)
    u, a, t = pick(2, 3, 4, 5), pick(0.4, 0.5, 0.6, 0.8, 1.2), pick(5, 6, 8, 10)
    v = u + a * t
    ex.num("Calculate the cyclist's speed at the end of this time.", v, "m/s",
           wrong=[(a * t, "Add the initial speed: v = u + at."), (u + a / t, "v = u + a × t."), (u * a * t, "v = u + at.")],
           working=[r"a = \frac{v - u}{t} \Rightarrow v = u + at", rf"v = {u} + ({a:g} \times {t})", rf"v = {ltx(v)}\ \text{{m/s}}"])
    t2 = pick(4, 5, 6, 8)
    a2 = -v / t2
    ex.num(f"The cyclist then brakes and comes to rest in {t2} s. Calculate her acceleration while braking.", a2, "m/s²",
           wrong=[(v / t2, "She is slowing down — the acceleration is NEGATIVE.")],
           working=[r"a = \frac{v - u}{t}", rf"a = \frac{{0 - {ltx(v)}}}{{{t2}}}", rf"a = {ltx(a2)}\ \text{{m/s}}^2"])
    ex.choice(f"What is meant by an acceleration of {a:g} m/s²?",
              f"The velocity increases by {a:g} m/s every second.",
              [(f"The cyclist travels {a:g} m every second.", "That describes a SPEED of " + f"{a:g} m/s."),
               (f"The velocity is {a:g} m/s.", "Acceleration is the CHANGE in velocity per second."),
               (f"The distance increases by {a:g} m every second squared.", "Acceleration is change in velocity per unit time.")])
    return ex.build(f"A cyclist travelling at {u} m/s accelerates uniformly at {a:g} m/s² for {t} s.")


gen_acceleration_exam = exam_style(_acc_car, _acc_trolley, _acc_cyclist)


# ════════════════ Forces ════════════════

def _forces_car(level="N5"):
    ex = _ex("Forces", level)
    m = pick(850, 1000, 1200, 1400, 1600)
    Fd = pick(2400, 3000, 3600, 4200, 4800)
    Ff = pick(400, 600, 800, 1000)
    Fu = Fd - Ff
    a = Fu / m
    ex.num("Calculate the unbalanced force acting on the car.", Fu, "N",
           wrong=[(Fd + Ff, "Friction acts AGAINST the driving force — subtract it.")],
           working=[rf"F_{{un}} = {Fd} - {Ff} = {Fu}\ \text{{N}}"])
    ex.num("Calculate the acceleration of the car.", a, "m/s²",
           wrong=[(Fd / m, "Use the UNBALANCED force, not the driving force."), (m / Fu, "a = F ÷ m."),
                  ((Fd + Ff) / m, "Unbalanced force = driving force − friction.")],
           working=[r"F = ma", rf"{Fu} = {m} \times a", rf"a = {ltx(a)}\ \text{{m/s}}^2"])
    ex.choice("Later, the car travels along the road at a constant speed. Which statement is correct?",
              "The driving force is equal in size to the frictional forces — the forces are balanced.",
              [("The driving force is greater than the frictional forces.", "Then there would be an unbalanced force and the car would accelerate."),
               ("There are no forces acting on the car.", "Forces still act; they are balanced (Newton's first law)."),
               ("The driving force must be zero.", "Friction still acts, so a driving force is needed to balance it.")])
    return ex.build(f"A car of mass {m} kg has a driving force of {Fd} N. The total frictional force acting on it is {Ff} N.")


def _forces_rocket(level="N5"):
    ex = _ex("Forces", level)
    m = pick(1.5e4, 2.0e4, 2.4e4, 3.2e4, 5.0e4)
    ratio = random.uniform(1.4, 2.2)
    thrust = sig(m * G * ratio, 2)
    W = m * G
    Fu = thrust - W
    a = Fu / m
    ex.num("Calculate the weight of the rocket.", W, "N",
           wrong=[(m, "Weight is a force: W = mg."), (m / G, "W = m × g.")],
           working=[r"W = mg", rf"W = {ltx(m)} \times 9.8", rf"W = {ltx(W)}\ \text{{N}}"])
    ex.num("Calculate the acceleration of the rocket as it lifts off.", a, "m/s²",
           wrong=[(thrust / m, "Find the UNBALANCED force first: thrust − weight."),
                  ((thrust + W) / m, "Weight acts DOWN, against the thrust — subtract it.")],
           working=[rf"F_{{un}} = {ltx(thrust)} - {ltx(W)} = {ltx(Fu)}\ \text{{N}}", r"F = ma",
                    rf"a = \frac{{{ltx(Fu)}}}{{{ltx(m)}}} = {ltx(a)}\ \text{{m/s}}^2"],
           scaffold=[("Unbalanced force, in N?", Fu, "N")])
    ex.choice("The thrust stays constant as the rocket rises. What happens to the acceleration of the rocket, and why?",
              "It increases — fuel is used up, so the mass (and weight) of the rocket decreases.",
              [("It stays the same — the thrust is constant.", "The mass decreases as fuel burns, so a = F/m increases."),
               ("It decreases — the rocket gets further from the ground.", "The change in g over this height is tiny; the mass loss dominates."),
               ("It decreases — air resistance disappears.", "Less air resistance would INCREASE the acceleration.")])
    return ex.build(f"A rocket of mass {fmt(m)} kg lifts off vertically. Its engines produce a thrust of {fmt(thrust)} N.")


def _forces_tugs(level="N5"):
    ex = _ex("Forces", level)
    F1, F2 = random.choice([(3000, 4000), (6000, 8000), (5000, 12000), (2400, 7000), (4500, 6000), (8000, 15000)])
    m = pick(2.0e5, 2.5e5, 4.0e5, 5.0e5)
    R = math.hypot(F1, F2)
    brg = _bearing(F1, F2)
    ex.num("Calculate the size of the resultant force on the ship.", R, "N",
           wrong=[(F1 + F2, "The forces are at right angles — use Pythagoras, not addition."), (abs(F2 - F1), "Use Pythagoras.")],
           working=[r"F^2 = F_1^2 + F_2^2", rf"F = \sqrt{{{F1}^2 + {F2}^2}}", rf"F = {ltx(R)}\ \text{{N}}"])
    ex.num("Calculate the direction of the resultant force, as a bearing (in degrees).", brg, "",
           wrong=[(90 - brg, "Bearings are measured clockwise from NORTH."), (math.degrees(math.atan2(F2, F1)), "Measure the angle from north.")],
           working=[rf"\tan\theta = \frac{{{F1}}}{{{F2}}}", rf"\theta = {brg:.1f}^\circ",
                    T(f"Bearing = {_bearing_text(brg)}")])
    a = R / m
    ex.num("Ignoring friction, calculate the initial acceleration of the ship.", a, "m/s²",
           wrong=[(F2 / m, "Use the RESULTANT force."), ((F1 + F2) / m, "The resultant of forces at right angles comes from Pythagoras.")],
           working=[r"F = ma", rf"a = \frac{{{ltx(R)}}}{{{ltx(m)}}}", rf"a = {ltx(a)}\ \text{{m/s}}^2"])
    return ex.build(f"Two tugs pull a ship of mass {fmt(m)} kg. One tug pulls due north with a force of {F2} N; "
                    f"the other pulls due east with a force of {F1} N.")


gen_forces_exam = exam_style(_forces_car, _forces_rocket, _forces_tugs)


# ════════════════ Vertical Motion ════════════════

def _vm_skydiver(level="N5"):
    ex = _ex("Vertical Motion", level)
    m = pick(60, 65, 72, 80, 85, 90)
    W = m * G
    R = sig(W * random.uniform(0.3, 0.7), 2)
    a = (W - R) / m
    ex.num("Calculate the weight of the skydiver.", W, "N",
           wrong=[(m, "Weight = mg."), (m / G, "W = m × g.")],
           working=[r"W = mg", rf"W = {m} \times 9.8 = {ltx(W)}\ \text{{N}}"])
    ex.num(f"At one point during the fall, the air resistance acting on the skydiver is {fmt(R)} N. "
           f"Calculate the acceleration of the skydiver at this point.", a, "m/s²",
           wrong=[(R / m, "Use the UNBALANCED force: weight − air resistance."), (W / m, "Air resistance reduces the unbalanced force."),
                  ((W + R) / m, "Air resistance acts UPWARDS, against the weight.")],
           working=[rf"F_{{un}} = {ltx(W)} - {ltx(R)} = {ltx(W - R)}\ \text{{N}}", r"F = ma", rf"a = {ltx(a)}\ \text{{m/s}}^2"],
           scaffold=[("Unbalanced force, in N?", W - R, "N")])
    ex.choice("Later, the skydiver falls at a constant speed. Which explanation is correct?",
              "Air resistance increases with speed until it is equal to the weight; the forces are balanced, so the speed is constant.",
              [("Gravity stops acting once the skydiver reaches a high speed.", "Weight still acts — it is balanced by air resistance."),
               ("Air resistance is now greater than the weight.", "Then the skydiver would be slowing down."),
               ("The skydiver has run out of energy to accelerate.", "It's about forces: balanced forces → constant speed.")])
    R2 = sig(W * random.uniform(1.6, 2.6), 2)
    a2 = (W - R2) / m
    ex.num(f"When the parachute opens, the air resistance increases to {fmt(R2)} N. Calculate the acceleration of the "
           f"skydiver at this instant (take downwards as positive).", a2, "m/s²",
           wrong=[(-a2, "Air resistance is greater than the weight, so the unbalanced force is UPWARDS — the acceleration is negative."),
                  (R2 / m, "Use the unbalanced force: weight − air resistance.")],
           working=[rf"F_{{un}} = {ltx(W)} - {ltx(R2)} = {ltx(W - R2)}\ \text{{N}}", r"F = ma", rf"a = {ltx(a2)}\ \text{{m/s}}^2",
                    T("Negative — the skydiver slows down.")])
    return ex.build(f"A skydiver of mass {m} kg jumps from a plane.")


def _vm_lander(level="N5"):
    ex = _ex("Vertical Motion", level)
    m = pick(400, 600, 750, 900, 1200)
    W = m * 1.6
    thrust = sig(W * random.uniform(1.3, 2.0), 2)
    a = (thrust - W) / m
    ex.num("Calculate the weight of the lander on the Moon.", W, "N",
           wrong=[(m * G, "On the Moon, g = 1.6 N/kg (data sheet)."), (m, "Weight = mg.")],
           working=[r"W = mg", rf"W = {m} \times 1.6 = {ltx(W)}\ \text{{N}}"])
    ex.num(f"Calculate the size of the lander's acceleration while its engine produces an upward thrust of {fmt(thrust)} N.",
           a, "m/s²",
           wrong=[(thrust / m, "Use the unbalanced force: thrust − weight."), ((thrust - m * G) / m, "Use the Moon's g (1.6 N/kg) for the weight.")],
           working=[rf"F_{{un}} = {ltx(thrust)} - {ltx(W)} = {ltx(thrust - W)}\ \text{{N}}", r"F = ma",
                    rf"a = \frac{{{ltx(thrust - W)}}}{{{m}}} = {ltx(a)}\ \text{{m/s}}^2"])
    ex.choice("The lander is moving downwards towards the surface while the engine fires. What happens to its speed?",
              "It decreases — the unbalanced force is upwards, opposite to the direction of motion.",
              [("It increases — it is moving downwards, the same direction as its weight.", "Thrust is greater than weight, so the unbalanced force is UPWARDS."),
               ("It stays constant — the engine balances the weight.", "Thrust is greater than the weight, so the forces are unbalanced."),
               ("The lander immediately starts moving upwards.", "An upward unbalanced force first slows the downward motion.")])
    return ex.build(f"A lunar lander of mass {m} kg descends towards the Moon's surface. (g on the Moon = 1.6 N/kg)")


def _vm_parachute(level="N5"):
    ex = _ex("Vertical Motion", level)
    m = pick(70, 75, 80, 90, 95)
    v1, v2 = pick(45, 50, 55, 60), pick(5, 6, 8)
    t = pick(2, 2.5, 3, 4)
    a = (v2 - v1) / t
    ex.num(f"When the parachute opens, the skydiver's speed falls from {v1} m/s to {v2} m/s in {t:g} s. "
           f"Calculate the acceleration of the skydiver (take downwards as positive).", a, "m/s²",
           wrong=[(-a, "The skydiver slows down — the acceleration is negative."), (v1 / t, "Use the change in speed.")],
           working=[r"a = \frac{v - u}{t}", rf"a = \frac{{{v2} - {v1}}}{{{t:g}}}", rf"a = {ltx(a)}\ \text{{m/s}}^2"])
    F = m * abs(a)
    ex.num("Calculate the size of the unbalanced force on the skydiver during this time.", F, "N",
           wrong=[(abs(a) / m, "F = m × a."), (m * G, "That's the weight, not the unbalanced force.")],
           working=[r"F = ma", rf"F = {m} \times {ltx(abs(a))}", rf"F = {ltx(F)}\ \text{{N}}"])
    W = m * G
    R = F + W
    ex.num("Calculate the air resistance acting on the skydiver during this time.", R, "N",
           wrong=[(F, "The unbalanced force = air resistance − weight, so air resistance = F + W."),
                  (abs(F - W), "Air resistance must be GREATER than the weight to slow the skydiver: add them.")],
           working=[rf"W = mg = {m} \times 9.8 = {ltx(W)}\ \text{{N}}", r"F_{un} = R - W \Rightarrow R = F_{un} + W",
                    rf"R = {ltx(F)} + {ltx(W)} = {ltx(R)}\ \text{{N}}"],
           scaffold=[("Weight of the skydiver, in N?", W, "N")])
    return ex.build(f"A skydiver of mass {m} kg (including equipment) is falling at a constant speed when she opens her parachute.")


gen_vertical_motion_exam = exam_style(_vm_skydiver, _vm_lander, _vm_parachute)


# ════════════════ Weight ════════════════

def _weight_planet(level="N5"):
    ex = _ex("Weight", level)
    m = pick(180, 240, 320, 450, 900)
    planet = pick("Venus", "Jupiter", "Saturn", "Neptune", "Moon")
    g = PLANET_G[planet]
    Wp = m * g
    ex.num("Calculate the weight of the probe on Earth.", m * G, "N",
           wrong=[(m, "Weight is a force (N): W = mg."), (m / G, "W = m × g.")],
           working=[r"W = mg", rf"W = {m} \times 9.8 = {ltx(m * G)}\ \text{{N}}"])
    ex.num(f"On a different planet or moon, the probe's weight is {fmt(Wp)} N. Calculate the gravitational field strength there.",
           g, "N/kg",
           wrong=[(m / Wp, "g = W ÷ m."), (Wp * m, "g = W ÷ m.")],
           working=[r"W = mg \Rightarrow g = \frac{W}{m}", rf"g = \frac{{{ltx(Wp)}}}{{{m}}} = {ltx(g)}\ \text{{N/kg}}"])
    others = [p for p in PLANET_G if abs(PLANET_G[p] - g) > 0.5]
    wrong = random.sample(others, 3)
    ex.choice("Use the data sheet to identify where the probe is.", planet,
              [(p, f"g on {p} is {PLANET_G[p]:g} N/kg.") for p in wrong])
    ex.choice("How does the mass of the probe there compare with its mass on Earth?",
              "It is the same — mass does not depend on gravitational field strength.",
              [("It is smaller where g is smaller.", "Weight changes with g; mass doesn't."),
               ("It is larger where g is larger.", "Mass is the amount of matter — it doesn't change."),
               ("The probe has no mass in space.", "Mass never changes; only weight depends on g.")])
    return ex.build(f"A space probe has a mass of {m} kg.")


def _weight_astronaut(level="N5"):
    ex = _ex("Weight", level)
    m = pick(95, 110, 120, 135, 150)
    WE = m * G
    ex.num(f"An astronaut in a space suit has a weight of {fmt(WE)} N on Earth. Calculate the total mass of the astronaut and suit.",
           m, "kg",
           wrong=[(WE * G, "m = W ÷ g."), (WE, "Mass is in kg: m = W ÷ g.")],
           working=[r"W = mg \Rightarrow m = \frac{W}{g}", rf"m = \frac{{{ltx(WE)}}}{{9.8}} = {ltx(m)}\ \text{{kg}}"])
    Wm = m * PLANET_G["Mars"]
    ex.num("Calculate the weight of the astronaut and suit on Mars.", Wm, "N",
           wrong=[(WE / PLANET_G["Mars"], "W = m × g with Mars's g (3.7 N/kg)."), (m, "Weight = mg.")],
           working=[rf"W = mg = {m} \times 3.7 = {ltx(Wm)}\ \text{{N}}"])
    ex.choice("The astronaut finds it easier to lift equipment on Mars than on Earth. Why?",
              "The gravitational field strength on Mars is smaller, so the weight of the equipment is smaller; its mass is unchanged.",
              [("The mass of the equipment is smaller on Mars.", "Mass is the same everywhere — weight is what changes."),
               ("There is no gravity on Mars.", "g on Mars is 3.7 N/kg."),
               ("Mars has no atmosphere, so there's no weight.", "Weight depends on g, not on the atmosphere.")])
    return ex.build("Astronauts plan a mission to Mars. (Use the data sheet values of g.)")


gen_weight_exam = exam_style(_weight_planet, _weight_astronaut)


# ════════════════ Energy ════════════════

def _energy_skate(level="N5"):
    ex = _ex("Energy", level)
    m, h = pick(45, 52, 60, 68, 75), pick(2.0, 2.5, 3.2, 4.0, 4.5)
    Ep = m * G * h
    v = math.sqrt(2 * Ep / m)
    ex.num("Calculate the gravitational potential energy lost by the skateboarder as she drops to the bottom of the ramp.",
           Ep, "J", wrong=[(m * h, "Ep = mgh — include g."), (m * G / h, "Ep = m × g × h.")],
           working=[r"E_p = mgh", rf"E_p = {m} \times 9.8 \times {h:g}", rf"E_p = {ltx(Ep)}\ \text{{J}}"])
    ex.num("Calculate her maximum possible speed at the bottom of the ramp.", v, "m/s",
           wrong=[(2 * Ep / m, "Take the SQUARE ROOT: v = √(2Ek/m)."), (math.sqrt(Ep / m), "Ek = ½mv², so v = √(2Ek ÷ m)."),
                  (Ep / m, "v = √(2Ek ÷ m).")],
           working=[r"E_k = E_p", rf"\tfrac{{1}}{{2}} \times {m} \times v^2 = {ltx(Ep)}", rf"v = {ltx(v)}\ \text{{m/s}}"])
    ex.choice("Her actual speed at the bottom is less than this. Why?",
              "Some of the energy is converted into heat (and sound) by friction and air resistance.",
              [("Energy is destroyed as she moves down the ramp.", "Energy cannot be destroyed — it is converted to other forms."),
               ("Her mass increases as she speeds up.", "Her mass doesn't change."),
               ("Gravitational potential energy can't be converted to kinetic energy.", "It can — but some is converted to heat too.")])
    return ex.build(f"A skateboarder of mass {m} kg starts from rest at the top of a ramp {h:g} m high.")


def _energy_braking(level="N5"):
    ex = _ex("Energy", level)
    m, v = pick(900, 1100, 1250, 1500), pick(12, 14, 15, 18, 20, 25)
    Ek = 0.5 * m * v ** 2
    ex.num("Calculate the kinetic energy of the car.", Ek, "J",
           wrong=[(m * v ** 2, "Ek = ½mv² — don't forget the ½."), (0.5 * m * v, "Square the speed."),
                  ((0.5 * m * v) ** 2, "Only the speed is squared.")],
           working=[r"E_k = \tfrac{1}{2}mv^2", rf"E_k = 0.5 \times {m} \times {v}^2", rf"E_k = {ltx(Ek)}\ \text{{J}}"])
    F = pick(4000, 5000, 6000, 7500, 8000)
    d = Ek / F
    ex.num(f"The brakes apply a constant force of {F} N. Calculate the minimum stopping distance of the car.", d, "m",
           wrong=[(Ek * F, "Ew = Fd, so d = Ew ÷ F."), (F / Ek, "d = Ew ÷ F.")],
           working=[r"E_w = E_k", r"E_w = Fd", rf"{ltx(Ek)} = {F} \times d", rf"d = {ltx(d)}\ \text{{m}}"])
    ex.choice("What happens to the car's kinetic energy as it stops?",
              "It is converted mainly into heat in the brakes (work is done against friction).",
              [("It is converted into gravitational potential energy.", "The car stays at the same height."),
               ("It is destroyed by the brakes.", "Energy is conserved — it is converted, not destroyed."),
               ("It is stored in the brakes as kinetic energy.", "The brakes get hot — heat energy.")])
    return ex.build(f"A car of mass {m} kg is travelling at {v} m/s when the driver brakes.")


gen_energy_exam = exam_style(_energy_skate, _energy_braking, reuse(generate_power_exam))


# ════════════════ Projectile Motion ════════════════

def _proj_cliff(level="N5"):
    ex = _ex("Projectile Motion", level)
    vh, t = pick(6, 8, 10, 12, 15), pick(1.2, 1.5, 1.8, 2.0, 2.5)
    dh = vh * t
    vv = G * t
    h = 0.5 * vv * t
    ex.num("Calculate the horizontal distance travelled by the ball.", dh, "m",
           wrong=[(vh / t, "d = v × t."), (0.5 * vh * t, "Horizontal velocity is constant — no ½.")],
           working=[r"d_h = v_h t", rf"d_h = {vh} \times {t:g} = {ltx(dh)}\ \text{{m}}"])
    ex.num("Calculate the vertical velocity of the ball just before it lands in the sea.", vv, "m/s",
           wrong=[(math.hypot(vh, vv), "The question asks for the VERTICAL velocity only."), (vh, "The vertical velocity starts at zero and increases at 9.8 m/s²."),
                  (G / t, "v = u + at = 0 + 9.8 × t.")],
           working=[r"v_v = u + at", rf"v_v = 0 + 9.8 \times {t:g} = {ltx(vv)}\ \text{{m/s}}"])
    ex.num("Calculate the height of the cliff (use the area under the vertical velocity–time graph).", h, "m",
           wrong=[(vv * t, "The vertical v–t graph is a triangle: area = ½ × base × height."), (dh, "That's the horizontal distance.")],
           working=[r"h = \text{area under } v_v\text{–}t \text{ graph} = \tfrac{1}{2} \times t \times v_v",
                    rf"h = 0.5 \times {t:g} \times {ltx(vv)} = {ltx(h)}\ \text{{m}}"])
    ex.choice("Why does the horizontal velocity of the ball stay constant (ignoring air resistance)?",
              "There is no unbalanced horizontal force acting on the ball.",
              [("Gravity acts horizontally on the ball.", "Gravity acts vertically."),
               ("The ball's weight balances its horizontal velocity.", "Forces can't balance a velocity — there's simply no horizontal force."),
               ("The ball is still being pushed by the kick.", "Once released, no horizontal force acts.")])
    return ex.build(f"A ball is kicked horizontally at {vh} m/s from the top of a cliff. It lands in the sea {t:g} s later. "
                    f"Air resistance can be ignored.")


def _proj_package(level="N5"):
    ex = _ex("Projectile Motion", level)
    vp, t = pick(40, 50, 60, 70), pick(3.0, 4.0, 5.0, 6.0)
    vv = G * t
    ex.num("Calculate the vertical velocity of the package just before it reaches the ground.", vv, "m/s",
           wrong=[(vp, "The horizontal velocity doesn't affect the vertical motion."), (G / t, "v = u + at.")],
           working=[r"v_v = u + at", rf"v_v = 0 + 9.8 \times {t:g} = {ltx(vv)}\ \text{{m/s}}"])
    dh = vp * t
    ex.num("Calculate the horizontal distance travelled by the package while it falls.", dh, "m",
           wrong=[(0.5 * vp * t, "The horizontal velocity is constant — d = vt, no ½."), (vv * t, "Use the HORIZONTAL velocity.")],
           working=[r"d_h = v_h t", rf"d_h = {vp} \times {t:g} = {ltx(dh)}\ \text{{m}}"])
    ex.choice("Where is the aircraft when the package hits the ground (ignoring air resistance)?",
              "Directly above the package — both have the same constant horizontal velocity.",
              [("Behind the package.", "The package doesn't speed up horizontally."),
               ("Directly above the point where the package was released.", "The aircraft keeps moving forward."),
               ("Far ahead of the package.", "The package keeps the aircraft's horizontal velocity.")])
    return ex.build(f"An aircraft flying horizontally at {vp} m/s releases a package. The package takes {t:g} s to reach the ground. "
                    f"Air resistance can be ignored.")


gen_projectile_exam = exam_style(_proj_cliff, _proj_package)


# ════════════════ Distance and Displacement ════════════════

def _dd_walk(level="N5"):
    ex = _ex("Distance and Displacement", level)
    n, e = random.choice([(3.0, 4.0), (6.0, 8.0), (5.0, 12.0), (2.4, 1.0), (4.5, 6.0), (9.0, 4.0), (1.2, 3.5)])
    dist = n + e
    disp = math.hypot(n, e)
    brg = _bearing(e, n)
    ex.num("Calculate the total distance walked.", dist, "km", wrong=[(disp, "That's the displacement — distance is the total path length.")],
           working=[rf"d = {n:g} + {e:g} = {ltx(dist)}\ \text{{km}}"])
    ex.num("Calculate the size of the walker's displacement.", disp, "km",
           wrong=[(dist, "Displacement is the straight line from start to finish — use Pythagoras."), (abs(e - n), "Use Pythagoras.")],
           working=[rf"s = \sqrt{{{n:g}^2 + {e:g}^2}} = {ltx(disp)}\ \text{{km}}"])
    ex.num("Calculate the direction of the displacement as a bearing (in degrees).", brg, "",
           wrong=[(90 - brg, "Bearings are measured clockwise from NORTH.")],
           working=[rf"\tan\theta = \frac{{{e:g}}}{{{n:g}}}", rf"\theta = {brg:.1f}^\circ", T(f"Bearing {_bearing_text(brg)}")])
    return ex.build(f"A walker walks {n:g} km due north, then {e:g} km due east.")


def _dd_orienteer(level="N5"):
    ex = _ex("Distance and Displacement", level)
    e1, n1 = pick(800, 900, 1200, 1500), pick(600, 900, 1000, 1600)
    w = pick(200, 300, 400, 500)
    dist = e1 + n1 + w
    east = e1 - w
    disp = math.hypot(east, n1)
    brg = _bearing(east, n1)
    ex.num("Calculate the total distance travelled by the orienteer.", dist, "m",
           wrong=[(disp, "Distance is the total length of the path."), (e1 + n1 - w, "Distance is a scalar — add all the legs.")],
           working=[rf"d = {e1} + {n1} + {w} = {dist}\ \text{{m}}"])
    ex.num("Calculate the size of the orienteer's displacement from the start.", disp, "m",
           wrong=[(math.hypot(e1, n1), f"Going west reduces the eastward displacement: {e1} − {w}."),
                  (dist, "Displacement is the straight line from start to finish.")],
           working=[rf"\text{{east}} = {e1} - {w} = {east}\ \text{{m}}", rf"s = \sqrt{{{east}^2 + {n1}^2}} = {ltx(disp)}\ \text{{m}}"],
           scaffold=[("Overall eastward distance from the start, in m?", east, "m")])
    ex.num("Calculate the direction of the displacement as a bearing (in degrees).", brg, "",
           wrong=[(90 - brg, "Measure the bearing clockwise from north.")],
           working=[rf"\tan\theta = \frac{{{east}}}{{{n1}}}", rf"\theta = {brg:.1f}^\circ", T(f"Bearing {_bearing_text(brg)}")])
    ex.choice("Why is displacement a vector quantity?", "It has both a size (magnitude) and a direction.",
              [("It is measured in metres.", "Distance is also measured in metres but is a scalar."),
               ("It is always smaller than the distance.", "That's not what makes it a vector."),
               ("It only has a size.", "That's a scalar.")])
    return ex.build(f"In an orienteering race, a competitor runs {e1} m due east, then {n1} m due north, then {w} m due west.")


gen_displacement_exam = exam_style(_dd_walk, _dd_orienteer)


# ════════════════ Vectors and Scalars ════════════════

def _vs_track(level="N5"):
    ex = _ex("Vectors and Scalars", level)
    D, t = pick(60, 80, 100, 120), pick(20, 25, 30, 40)
    dist = math.pi * D / 2
    ex.choice("Which list contains only vector quantities?", "displacement, velocity, force",
              [("distance, speed, time", "These are all scalars."), ("displacement, speed, mass", "Speed and mass are scalars."),
               ("velocity, energy, acceleration", "Energy is a scalar.")])
    ex.num("Calculate the runner's average speed.", dist / t, "m/s",
           wrong=[(D / t, "Average SPEED uses the distance along the track (half the circumference)."),
                  (math.pi * D / t, "Half a lap is half the circumference: πd ÷ 2.")],
           working=[rf"d = \tfrac{{1}}{{2}} \pi \times {D} = {ltx(dist)}\ \text{{m}}", rf"\bar{{v}} = \frac{{d}}{{t}} = {ltx(dist / t)}\ \text{{m/s}}"],
           scaffold=[("Distance run, in m?", dist, "m")])
    ex.num("Calculate the size of the runner's average velocity.", D / t, "m/s",
           wrong=[(dist / t, "Average VELOCITY uses the displacement — the straight line across the track (the diameter).")],
           working=[rf"s = {D}\ \text{{m (the diameter)}}", rf"\bar{{v}} = \frac{{s}}{{t}} = \frac{{{D}}}{{{t}}} = {ltx(D / t)}\ \text{{m/s}}"])
    return ex.build(f"A runner runs half a lap of a circular track of diameter {D} m, from one side to the point directly "
                    f"opposite, in {t} s.")


def _vs_river(level="N5"):
    ex = _ex("Vectors and Scalars", level)
    vb, vc = random.choice([(3.0, 4.0), (1.5, 2.0), (2.4, 0.7), (4.0, 3.0), (1.2, 0.5), (2.0, 1.5)])
    R = math.hypot(vb, vc)
    brg = _bearing(vc, vb)
    ex.num("Calculate the size of the resultant velocity of the boat.", R, "m/s",
           wrong=[(vb + vc, "The velocities are at right angles — use Pythagoras."), (abs(vb - vc), "Use Pythagoras.")],
           working=[rf"v = \sqrt{{{vb:g}^2 + {vc:g}^2}} = {ltx(R)}\ \text{{m/s}}"])
    ex.num("Calculate the direction of the resultant velocity as a bearing (in degrees).", brg, "",
           wrong=[(90 - brg, "Measure the bearing clockwise from north.")],
           working=[rf"\tan\theta = \frac{{{vc:g}}}{{{vb:g}}}", rf"\theta = {brg:.1f}^\circ", T(f"Bearing {_bearing_text(brg)}")])
    ex.choice("Which statement explains the difference between speed and velocity?",
              "Velocity is speed in a stated direction — velocity is a vector, speed is a scalar.",
              [("Speed is a vector, velocity is a scalar.", "The other way round."),
               ("Velocity is always larger than speed.", "Their magnitudes can be equal; the difference is direction."),
               ("They are measured in different units.", "Both are measured in m/s.")])
    return ex.build(f"A boat sets off due north across a river at {vb:g} m/s relative to the water. The river flows due east at {vc:g} m/s.")


gen_vectors_exam = exam_style(_vs_track, _vs_river)


# ════════════════ Speed and Velocity ════════════════

def _sv_cyclist(level="N5"):
    ex = _ex("Speed and Velocity", level)
    e, n = random.choice([(1200, 900), (2400, 1000), (1600, 1200), (800, 1500), (3000, 4000)])
    t1, t2 = pick(150, 200, 240, 300), pick(120, 180, 200, 250)
    t = t1 + t2
    s = math.hypot(e, n)
    brg = _bearing(e, n)
    ex.num("Calculate the cyclist's average speed for the whole journey.", (e + n) / t, "m/s",
           wrong=[(s / t, "Average SPEED uses the total distance."), ((e / t1 + n / t2) / 2, "Use total distance ÷ total time.")],
           working=[rf"\bar{{v}} = \frac{{{e} + {n}}}{{{t1} + {t2}}} = {ltx((e + n) / t)}\ \text{{m/s}}"])
    ex.num("Calculate the size of the cyclist's displacement.", s, "m",
           wrong=[(e + n, "Displacement is the straight line from start to finish — Pythagoras.")],
           working=[rf"s = \sqrt{{{e}^2 + {n}^2}} = {ltx(s)}\ \text{{m}}"])
    ex.num("Calculate the size of the cyclist's average velocity.", s / t, "m/s",
           wrong=[((e + n) / t, "Average VELOCITY = displacement ÷ time.")],
           working=[rf"\bar{{v}} = \frac{{s}}{{t}} = \frac{{{ltx(s)}}}{{{t}}} = {ltx(s / t)}\ \text{{m/s}}"])
    ex.num("Calculate the direction of the average velocity as a bearing (in degrees).", brg, "",
           wrong=[(90 - brg, "Measure the bearing clockwise from north.")],
           working=[rf"\tan\theta = \frac{{{e}}}{{{n}}}", rf"\theta = {brg:.1f}^\circ", T(f"Bearing {_bearing_text(brg)}")])
    return ex.build(f"A cyclist rides {e} m due east in {t1} s, then {n} m due north in {t2} s.")


def _sv_plane(level="N5"):
    ex = _ex("Speed and Velocity", level)
    vp, vw = random.choice([(80, 15), (120, 22), (60, 11), (150, 36), (90, 20)])
    R = math.hypot(vp, vw)
    brg = _bearing(vw, vp)
    ex.num("Calculate the size of the resultant velocity of the aircraft.", R, "m/s",
           wrong=[(vp + vw, "The velocities are at right angles — Pythagoras."), (vp - vw, "Use Pythagoras.")],
           working=[rf"v = \sqrt{{{vp}^2 + {vw}^2}} = {ltx(R)}\ \text{{m/s}}"])
    ex.num("Calculate the direction of the resultant velocity as a bearing (in degrees).", brg, "",
           wrong=[(90 - brg, "Measure the bearing clockwise from north.")],
           working=[rf"\tan\theta = \frac{{{vw}}}{{{vp}}}", rf"\theta = {brg:.1f}^\circ", T(f"Bearing {_bearing_text(brg)}")])
    mins = pick(5, 10, 15, 20)
    s = sig(R) * mins * 60
    ex.num(f"Calculate the size of the aircraft's displacement after {mins} minutes.", s, "m",
           wrong=[(sig(R) * mins, "Convert minutes to seconds."), (vp * mins * 60, "Use the RESULTANT velocity.")],
           working=[rf"s = \bar{{v}}t = {ltx(R)} \times ({mins} \times 60) = {ltx(s)}\ \text{{m}}"])
    return ex.build(f"An aircraft heads due north with a speed of {vp} m/s relative to the air. A wind blows due east at {vw} m/s.")


gen_speed_velocity_exam = exam_style(_sv_cyclist, _sv_plane)


# ════════════════ Velocity-Time Graphs ════════════════

def _vt_car(level="N5"):
    ex = _ex("Velocity-Time Graphs", level)
    v = pick(8, 10, 12, 15, 16, 20)
    t1, t2, t3 = pick(4, 5, 8), pick(6, 10, 12, 15), pick(2, 4, 5)
    T1, T2, T3 = t1, t1 + t2, t1 + t2 + t3
    a = v / t1
    dist = 0.5 * v * t1 + v * t2 + 0.5 * v * t3
    fig = graph([(0, 0), (T1, v), (T2, v), (T3, 0)], labels=["O", "A", "B", "C"])
    ex.num("Calculate the acceleration of the car between O and A.", a, "m/s²",
           wrong=[(t1 / v, "a = change in velocity ÷ time."), (v * t1, "That's (twice) the area; gradient = Δv ÷ t.")],
           working=[r"a = \frac{v - u}{t}", rf"a = \frac{{{v} - 0}}{{{t1}}} = {ltx(a)}\ \text{{m/s}}^2"])
    ex.num("Calculate the total distance travelled by the car.", dist, "m",
           wrong=[(v * T3, "The triangles have area ½ × base × height."), (v * t2, "Include the areas of all three sections."),
                  (0.5 * v * T3, "The middle section is a rectangle, not a triangle.")],
           working=[r"d = \text{area under graph}", rf"d = (\tfrac{{1}}{{2}} \times {t1} \times {v}) + ({t2} \times {v}) + (\tfrac{{1}}{{2}} \times {t3} \times {v})",
                    rf"d = {ltx(dist)}\ \text{{m}}"])
    ex.num("Calculate the average speed of the car for the whole journey.", dist / T3, "m/s",
           wrong=[(v / 2, "Average speed = total distance ÷ total time."), (v, "That's the top speed.")],
           working=[rf"\bar{{v}} = \frac{{d}}{{t}} = \frac{{{ltx(dist)}}}{{{T3}}} = {ltx(dist / T3)}\ \text{{m/s}}"])
    ex.choice("Describe the motion of the car between B and C.", "Constant (uniform) deceleration.",
              [("Constant velocity.", "The line slopes down — the velocity is decreasing."),
               ("Moving backwards.", "The velocity is still positive; it is slowing down."),
               ("Constant acceleration.", "The gradient is negative — deceleration.")])
    return ex.build("The graph shows how the velocity of a car changes during a short journey.", figure=fig)


def _vt_train(level="N5"):
    ex = _ex("Velocity-Time Graphs", level)
    u, v = pick(4, 5, 6, 8), pick(14, 16, 18, 20, 24)
    t1, t2, t3 = pick(10, 15, 20), pick(20, 30, 40), pick(8, 10, 12, 16)
    T1, T2, T3 = t1, t1 + t2, t1 + t2 + t3
    fig = graph([(0, u), (T1, v), (T2, v), (T3, 0)], labels=["P", "Q", "R", "S"])
    d1 = 0.5 * (u + v) * t1
    ex.num("Calculate the distance travelled by the train between P and Q.", d1, "m",
           wrong=[(0.5 * v * t1, "The shape is a trapezium — include the rectangle under the starting velocity."),
                  (v * t1, "Area of a trapezium = ½ × (u + v) × t.")],
           working=[r"d = \text{area} = \text{rectangle} + \text{triangle}", rf"d = ({u} \times {t1}) + (\tfrac{{1}}{{2}} \times {t1} \times {v - u})",
                    rf"d = {ltx(d1)}\ \text{{m}}"])
    a3 = -v / t3
    ex.num("Calculate the acceleration of the train between R and S.", a3, "m/s²",
           wrong=[(v / t3, "The train is slowing down — the acceleration is negative."), (-t3 / v, "a = Δv ÷ t.")],
           working=[r"a = \frac{v - u}{t}", rf"a = \frac{{0 - {v}}}{{{t3}}} = {ltx(a3)}\ \text{{m/s}}^2"])
    ex.choice("During which section is the unbalanced force on the train zero?", "Q to R",
              [("P to Q", "The train is accelerating, so there's an unbalanced force."),
               ("R to S", "The train is decelerating, so there's an unbalanced force (backwards)."),
               ("At S only", "Q→R is at constant velocity — balanced forces.")])
    return ex.build("The graph shows the velocity of a train between two stations.", figure=fig)


gen_vt_graphs_exam = exam_style(_vt_car, _vt_train)


EXAM = {
    "Speed, Distance & Time":    gen_sdt_exam,
    "Acceleration":              gen_acceleration_exam,
    "Forces":                    gen_forces_exam,
    "Vertical Motion":           gen_vertical_motion_exam,
    "Weight":                    gen_weight_exam,
    "Energy":                    gen_energy_exam,
    "Projectile Motion":         gen_projectile_exam,
    "Distance and Displacement": gen_displacement_exam,
    "Vectors and Scalars":       gen_vectors_exam,
    "Speed and Velocity":        gen_speed_velocity_exam,
    "Velocity-Time Graphs":      gen_vt_graphs_exam,
}
