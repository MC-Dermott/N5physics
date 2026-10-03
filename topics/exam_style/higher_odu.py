"""Higher Our Dynamic Universe — exam-style questions that cut across the unit's topics, like SQA paper questions.

Recognised wrong answers follow the Higher marking instructions and course reports: sign errors in
the equations of motion (deceleration taken as positive, g not negative going up), the change in
momentum found without reversing the sign of a rebound velocity, Ek treated as conserved in an
inelastic collision, mg sin θ / mg cos θ swapped, the radius used without adding the height,
the Lorentz factor applied the wrong way round, and the redshift calculated from the emitted
wavelength instead of the change.
"""
import math
import random

from topics.exam_style.base import Exam, T, fmt, graph, ltx, pick, sig
from utils.projectile_diagram import cliff_launch, platform_landing

UNIT1 = "Our Dynamic Universe (Part 1)"
UNIT2 = "Our Dynamic Universe (Part 2)"
G = 9.8
G_N = 6.67e-11
C = 3.00e8
H0 = 2.3e-18
M_EARTH, R_EARTH = 6.0e24, 6.4e6
YEAR = 365 * 24 * 3600


def _notes(title, body):
    return f"## {title} — exam technique\n\n{body}"


NOTES = {
    "Equations of Motion": _notes("Equations of motion", r"""
$v = u + at$ &nbsp; $s = ut + \frac{1}{2}at^2$ &nbsp; $v^2 = u^2 + 2as$ &nbsp; $s = \frac{1}{2}(u + v)t$

- Choose a positive direction and stick to it: a deceleration is a **negative** acceleration; going up, $a = -9.8$ m/s².
- At the maximum height, the vertical velocity is **zero**.
- List s, u, v, a, t first and pick the equation without the quantity you don't know.
"""),
    "Graphs of Motion": _notes("Graphs of motion", r"""
- v–t: gradient = acceleration, area = **displacement** (area below the axis is negative).
- a–t: area = change in velocity.
- A ball thrown up and falling freely has a **constant** acceleration of −9.8 m/s² throughout (taking up as positive) — a straight v–t line crossing the time axis at the top of its flight.
"""),
    "Towing": _notes("Towing", r"""
Whole system: $F_{driving} - F_{friction,total} = (m_1 + m_2)a$. Then isolate the trailer: $T - F_{friction,trailer} = m_{trailer}\,a$.
"""),
    "Components of Vectors": _notes("Components of vectors", r"""
Component **down a slope** = $mg\sin\theta$; component **perpendicular** to the slope = $mg\cos\theta$.

A force F at angle θ to the horizontal: horizontal component $F\cos\theta$, vertical component $F\sin\theta$.
Find the **unbalanced** force along the direction of motion, then $F = ma$.
"""),
    "Momentum and Impulse": _notes("Momentum and impulse", r"""
$p = mv$ &nbsp; Total momentum before = total momentum after (no external forces) &nbsp; $Ft = mv - mu = \Delta p$

- Momentum is a **vector**: a rebound reverses the sign of the velocity.
- **Elastic**: Ek is conserved. **Inelastic**: Ek is **not** conserved (some becomes heat/sound).
- Increasing the contact time reduces the average force for the same change in momentum.
"""),
    "Energy, Work and Power": _notes("Energy, work and power", r"""
$E_w = Fd$ &nbsp; $E_p = mgh$ &nbsp; $E_k = \frac{1}{2}mv^2$ &nbsp; $P = \frac{E}{t}$

Energy lost to friction = (Ep + Ek at start) − (Ep + Ek at end), and $E_w = F_f d$ gives the average frictional force.
"""),
    "Effective Weight": _notes("Effective weight", r"""
Scales read the **normal reaction** R. Taking up as positive: $R - mg = ma$, so $R = m(g + a)$.

- Accelerating up / decelerating while moving down → reading **greater** than mg.
- Accelerating down / decelerating while moving up → reading **less** than mg.
- Constant velocity → reading = mg. Free fall → reading = 0 (apparent weightlessness).
"""),
    "Projectile Motion": _notes("Projectile motion", r"""
Resolve the launch velocity: $u_h = u\cos\theta$, $u_v = u\sin\theta$. Horizontal: constant velocity. Vertical: $a = -9.8$ m/s².
"""),
    "Gravitation": _notes("Gravitation", r"""
$F = \frac{Gm_1m_2}{r^2}$, $G = 6.67\times10^{-11}$ N m² kg⁻² — r is the distance between the **centres** (radius + height).

- Inverse square: doubling r makes F a **quarter**.
- Earth: mass $6.0\times10^{24}$ kg, radius $6.4\times10^6$ m.
"""),
    "Special Relativity": _notes("Special relativity", r"""
$t' = \frac{t}{\sqrt{1 - \frac{v^2}{c^2}}}$ &nbsp; $l' = l\sqrt{1 - \frac{v^2}{c^2}}$

- The speed of light in a vacuum is the **same for all observers**.
- A moving clock runs slow (time dilation, t' > t); a moving object is shorter (length contraction, l' < l).
- t and l are measured in the object's own frame (its **proper** time and length).
"""),
    "The Expanding Universe": _notes("The expanding universe", r"""
$z = \frac{\lambda_{obs} - \lambda_{rest}}{\lambda_{rest}}$ &nbsp; $z = \frac{v}{c}$ &nbsp; $v = H_0d$ &nbsp; $f_o = f_s\left(\frac{v}{v \pm v_s}\right)$

- $H_0 = 2.3 \times 10^{-18}$ s⁻¹; age of the Universe ≈ $1/H_0$.
- Doppler: source approaching → observed frequency **higher** (− sign); receding → **lower** (+ sign).
- Redshift of light from distant galaxies is evidence that the Universe is **expanding**.
"""),
}


def _ex(level, unit=UNIT1):
    return Exam(unit, level, NOTES)


# ════════════════════════════ Part 1 ════════════════════════════

def car_and_trailer(level="Higher"):
    ex = _ex(level)
    m1, m2 = pick(1200, 1400, 1600), pick(400, 600, 800)
    f1, f2 = pick(300, 400, 500), pick(150, 200, 250)
    F = pick(2400, 3000, 3600)
    a = (F - f1 - f2) / (m1 + m2)
    ex.on("Towing").num(f"The car's driving force is {F} N. The frictional forces are {f1} N on the car and {f2} N on the trailer. "
        f"Calculate the acceleration of the car and trailer.", a, "m/s²",
        wrong=[(F / (m1 + m2), "Subtract BOTH frictional forces first."), ((F - f1 - f2) / m1, "Use the TOTAL mass (car + trailer)."),
               ((F - f1) / (m1 + m2), "Include the trailer's friction too.")],
        working=[r"F_{un} = F - f_{car} - f_{trailer}", rf"a = \frac{{{F} - {f1} - {f2}}}{{{m1} + {m2}}} = {ltx(a)}\ \text{{m/s}}^2"])
    Tn = m2 * sig(a) + f2
    ex.on("Towing").num("Calculate the tension in the tow bar.", Tn, "N",
        wrong=[(m2 * sig(a), "The tension must also overcome the trailer's friction: T = ma + f."), (F - f1, "Isolate the TRAILER: T − f = m_trailer × a.")],
        working=[r"T - f_{trailer} = m_{trailer}a", rf"T = {m2} \times {ltx(a)} + {f2} = {ltx(Tn)}\ \text{{N}}"])
    t = pick(5, 6, 8, 10)
    v = sig(a) * t
    ex.on("Equations of Motion").num(f"The car starts from rest. Calculate its speed after {t} s.", v, "m/s",
        wrong=[(sig(a) / t, "v = u + at."), (0.5 * sig(a) * t ** 2, "That's the displacement; v = u + at.")],
        working=[rf"v = u + at = 0 + {ltx(a)} \times {t} = {ltx(v)}\ \text{{m/s}}"])
    s = 0.5 * sig(a) * t ** 2
    ex.on("Equations of Motion").num(f"Calculate the distance travelled in these {t} s.", s, "m",
        wrong=[(sig(a) * t ** 2, "s = ut + ½at² — include the ½."), (v * t, "The car accelerates; use s = ut + ½at².")],
        working=[rf"s = ut + \tfrac{{1}}{{2}}at^2 = 0 + \tfrac{{1}}{{2}} \times {ltx(a)} \times {t}^2 = {ltx(s)}\ \text{{m}}"])
    ex.on("Energy, Work and Power").num("Calculate the work done by the driving force in this time.", F * sig(s), "J",
        wrong=[((F - f1 - f2) * sig(s), "Use the DRIVING force for the work it does."), (F / sig(s), "E_w = F × d.")],
        working=[rf"E_w = Fd = {F} \times {ltx(s)} = {ltx(F * sig(s))}\ \text{{J}}"])
    ex.on("Towing").choice("The friction on the trailer increases but the acceleration is kept the same. What happens to the tension in the tow bar?",
        "It increases — T − f = ma, so a larger friction needs a larger tension for the same acceleration.",
        [("It decreases.", "Friction opposes the tension, so more tension is needed."),
         ("It stays the same, because the acceleration is unchanged.", "Only the resultant on the trailer is unchanged."),
         ("It becomes zero.", "The trailer still needs to be pulled.")])
    return ex.build(f"A car of mass {m1} kg tows a trailer of mass {m2} kg along a level road.")


def skier(level="Higher"):
    ex = _ex(level)
    m, th = pick(55, 60, 70, 80), pick(15, 20, 25, 30)
    Wp = m * G * math.sin(math.radians(th))
    ex.on("Components of Vectors").num("Calculate the component of the skier's weight acting down the slope.", Wp, "N",
        wrong=[(m * G * math.cos(math.radians(th)), "Down the slope is mg sin θ."), (m * G, "Only the component along the slope.")],
        working=[rf"W_\parallel = mg\sin\theta = {m} \times 9.8 \times \sin {th}^\circ = {ltx(Wp)}\ \text{{N}}"])
    f = sig(Wp * random.uniform(0.25, 0.5), 2)
    a = (sig(Wp) - f) / m
    ex.on("Components of Vectors").num(f"The frictional force on the skier is {fmt(f)} N. Calculate her acceleration down the slope.", a, "m/s²",
        wrong=[(sig(Wp) / m, "Subtract the friction first."), ((sig(Wp) + f) / m, "Friction acts UP the slope.")],
        working=[rf"a = \frac{{{ltx(Wp)} - {fmt(f)}}}{{{m}}} = {ltx(a)}\ \text{{m/s}}^2"])
    s = pick(40, 50, 60, 80)
    v = math.sqrt(2 * sig(a) * s)
    ex.on("Equations of Motion").num(f"She starts from rest. Calculate her speed after sliding {s} m down the slope.", v, "m/s",
        wrong=[(2 * sig(a) * s, "Take the square root."), (math.sqrt(sig(a) * s), "v² = u² + 2as.")],
        working=[rf"v^2 = u^2 + 2as = 0 + 2 \times {ltx(a)} \times {s}", rf"v = {ltx(v)}\ \text{{m/s}}"])
    ex.on("Energy, Work and Power").num("Calculate the work done against friction over this distance.", f * s, "J",
        wrong=[(sig(Wp) * s, "Use the FRICTIONAL force."), (f / s, "E_w = F × d.")],
        working=[rf"E_w = Fd = {fmt(f)} \times {s} = {ltx(f * s)}\ \text{{J}}"])
    ex.on("Components of Vectors").choice("The slope becomes steeper. What happens to the component of her weight down the slope?",
        "It increases, because sin θ increases as θ increases.",
        [("It decreases, because cos θ decreases.", "Down the slope is mg sin θ."), ("It stays the same.", "Weight is the same, the component changes."),
         ("It decreases, because she has less contact with the snow.", "The component down the slope increases.")])
    return ex.build(f"A skier of mass {m} kg slides down a straight slope at {th}° to the horizontal.")


def lift_journey(level="Higher"):
    ex = _ex(level)
    m = pick(60, 70, 80)
    v = pick(2.0, 3.0, 4.0)
    t1, t2, t3 = pick(2, 2.5, 4), pick(6, 8, 10), pick(2, 4, 5)
    T1, T2, T3 = t1, t1 + t2, t1 + t2 + t3
    fig = graph([(0, 0), (T1, v), (T2, v), (T3, 0)], labels=["", "A", "B", "C"])
    a = v / t1
    ex.on("Graphs of Motion").num("Use the graph to calculate the acceleration of the lift in the first stage.", a, "m/s²",
        wrong=[(t1 / v, "Gradient = Δv ÷ Δt."), (v * t1, "The gradient, not the area.")],
        working=[rf"a = \frac{{{v:g} - 0}}{{{t1:g}}} = {ltx(a)}\ \text{{m/s}}^2"])
    ex.on("Effective Weight").num(f"A passenger of mass {m} kg stands on scales in the lift. Calculate the reading on the scales during the first stage.",
        m * (G + sig(a)), "N",
        wrong=[(m * (G - sig(a)), "Accelerating UP: R = m(g + a)."), (m * G, "The lift is accelerating, so R ≠ mg.")],
        working=[r"R - mg = ma", rf"R = {m}(9.8 + {ltx(a)}) = {ltx(m * (G + sig(a)))}\ \text{{N}}"])
    ex.on("Effective Weight").choice("What does the scale read between B and C?", "Less than the passenger's weight.",
        [("More than the passenger's weight.", "Slowing down while moving up is a DOWNWARD acceleration."),
         ("Exactly the passenger's weight.", "The lift is accelerating (decelerating)."), ("Zero.", "Only in free fall.")])
    h = 0.5 * v * t1 + v * t2 + 0.5 * v * t3
    ex.on("Graphs of Motion").num("Calculate the height the lift rises.", h, "m",
        wrong=[(v * T3, "The first and last sections are triangles."), (v * t2, "Include every section.")],
        working=[rf"h = \text{{area}} = \tfrac{{1}}{{2}}({t1:g})({v:g}) + ({t2:g})({v:g}) + \tfrac{{1}}{{2}}({t3:g})({v:g}) = {ltx(h)}\ \text{{m}}"])
    Ep = m * G * sig(h)
    ex.on("Energy, Work and Power").num("Calculate the gravitational potential energy gained by the passenger.", Ep, "J",
        wrong=[(m * sig(h), "Ep = mgh.")], working=[rf"E_p = mgh = {m} \times 9.8 \times {ltx(h)} = {ltx(Ep)}\ \text{{J}}"])
    return ex.build("The graph shows the velocity of a lift moving upwards between floors.", figure=fig)


def trolley_collision(level="Higher"):
    ex = _ex(level)
    m1, m2, u = random.choice([(0.8, 1.2, 0.5), (1.0, 1.5, 0.6), (0.5, 0.75, 0.8), (2.0, 1.0, 0.9)])
    v = m1 * u / (m1 + m2)
    ex.on("Momentum and Impulse").num(f"Trolley A ({m1:g} kg) moving at {u:g} m/s hits stationary trolley B ({m2:g} kg) and they stick together. "
        f"Calculate their velocity just after the collision.", v, "m/s",
        wrong=[(m1 * u / m2, "Both trolleys move together: use (m₁ + m₂)."), (u / 2, "Use conservation of momentum.")],
        working=[r"m_1u_1 = (m_1 + m_2)v", rf"{m1:g} \times {u:g} = ({m1:g} + {m2:g})v", rf"v = {ltx(v)}\ \text{{m/s}}"])
    Ek1, Ek2 = 0.5 * m1 * u ** 2, 0.5 * (m1 + m2) * sig(v) ** 2
    ex.on("Momentum and Impulse").num("Calculate the kinetic energy lost in the collision.", Ek1 - Ek2, "J",
        wrong=[(Ek1, "Subtract the Ek after."), (Ek2, "Find before − after.")],
        working=[rf"E_{{k,before}} = {ltx(Ek1)}\ \text{{J}}", rf"E_{{k,after}} = {ltx(Ek2)}\ \text{{J}}", rf"\Delta E_k = {ltx(Ek1 - Ek2)}\ \text{{J}}"])
    ex.on("Momentum and Impulse").choice("Is the collision elastic or inelastic?", "Inelastic — kinetic energy is not conserved.",
        [("Elastic — momentum is conserved.", "Momentum is conserved in all collisions."), ("Elastic — Ek is conserved.", "Ek was lost."),
         ("Inelastic — momentum is not conserved.", "Momentum IS conserved.")])
    t_ms = pick(40, 50, 80)
    F = m2 * sig(v) / (t_ms / 1000)
    ex.on("Momentum and Impulse").num(f"The collision lasts {t_ms} ms. Calculate the average force on trolley B.", F, "N",
        wrong=[(m2 * sig(v) / t_ms, "Convert ms to s."), (m1 * u / (t_ms / 1000), "Use B's change in momentum.")],
        working=[rf"F = \frac{{\Delta p}}{{t}} = \frac{{{m2:g} \times {ltx(v)}}}{{{t_ms}\times10^{{-3}}}} = {ltx(F)}\ \text{{N}}"])
    a = -pick(0.05, 0.08, 0.1)
    s = -sig(v) ** 2 / (2 * a)
    ex.on("Equations of Motion").num(f"Friction then decelerates the trolleys at {-a:g} m/s². Calculate how far they travel before stopping.", s, "m",
        wrong=[(sig(v) ** 2 / -a, "v² = u² + 2as — include the 2."), (sig(v) / -a, "Use v² = u² + 2as.")],
        working=[rf"0 = {ltx(v)}^2 + 2({a:g})s", rf"s = {ltx(s)}\ \text{{m}}"])
    return ex.build("Two trolleys collide on a level track.")


def thrown_ball(level="Higher"):
    ex = _ex(level)
    u, m = pick(9.8, 14.7, 19.6), pick(0.15, 0.2, 0.4)
    ex.on("Equations of Motion").num(f"A ball is thrown vertically upwards at {u:g} m/s. Calculate the maximum height it reaches.", u ** 2 / (2 * G), "m",
        wrong=[(u ** 2 / G, "Include the 2: v² = u² + 2as."), (u / G, "Use v² = u² + 2as with v = 0.")],
        working=[rf"0 = {u:g}^2 + 2(-9.8)s", rf"s = {ltx(u ** 2 / (2 * G))}\ \text{{m}}"])
    ex.on("Equations of Motion").num("Calculate the time for the ball to return to the thrower's hand.", 2 * u / G, "s",
        wrong=[(u / G, "That's the time to the TOP — double it."), (u * G, "Use v = u + at.")],
        working=[rf"-{u:g} = {u:g} + (-9.8)t", rf"t = {ltx(2 * u / G)}\ \text{{s}}"])
    ex.on("Graphs of Motion").choice("Which describes the velocity–time graph for the flight (upwards positive)?",
        "A straight line with a constant negative gradient, crossing the time axis at the top of the flight.",
        [("A horizontal line, because the acceleration is constant.", "That's the ACCELERATION–time graph."),
         ("A V shape touching zero at the top.", "Velocity goes negative when the ball falls."),
         ("A curve getting steeper.", "The acceleration is constant, so the graph is straight.")])
    t_ms = pick(50, 80, 100)
    F = m * u / (t_ms / 1000)
    ex.on("Momentum and Impulse").num(f"The {m:g} kg ball is caught at {u:g} m/s and stopped in {t_ms} ms. Calculate the average force on the hand.", F, "N",
        wrong=[(m * u / t_ms, "Convert ms to s."), (m * u * t_ms / 1000, "F = Δp ÷ t.")],
        working=[rf"F = \frac{{mv - mu}}{{t}} = \frac{{{m:g} \times {u:g}}}{{{t_ms}\times10^{{-3}}}} = {ltx(F)}\ \text{{N}}"])
    ex.on("Momentum and Impulse").choice("Why does moving the hand back while catching reduce the force?",
        "It increases the time to stop the ball; the change in momentum is the same, so the average force is smaller.",
        [("It reduces the ball's change in momentum.", "Δp is the same — it's the time that changes."),
         ("It reduces the ball's mass.", "Mass is unchanged."), ("It increases the impulse.", "The impulse (Δp) is the same.")])
    return ex.build("A ball is thrown vertically upwards and caught at the same height. Air resistance can be ignored.")


# ════════════════════════════ Part 2 ════════════════════════════

def moon_golf(level="Higher"):
    ex = _ex(level, UNIT2)
    M, R, m = 7.3e22, 1.74e6, 0.046
    F = G_N * M * m / R ** 2
    ex.on("Gravitation").num(f"Calculate the gravitational force on a {m:g} kg golf ball on the Moon's surface.", F, "N",
        wrong=[(G_N * M * m / R, "Square the radius."), (m * G, "Use F = GMm/r² for the Moon, not g on Earth.")],
        working=[rf"F = \frac{{GMm}}{{r^2}} = \frac{{6.67\times10^{{-11}} \times 7.3\times10^{{22}} \times {m:g}}}{{(1.74\times10^6)^2}} = {ltx(F)}\ \text{{N}}"])
    g = sig(F) / m
    ex.on("Gravitation").num("Calculate the gravitational field strength on the Moon's surface.", g, "N/kg",
        wrong=[(sig(F) * m, "g = F ÷ m.")], working=[rf"g = \frac{{F}}{{m}} = {ltx(g)}\ \text{{N/kg}}"])
    u, th = pick(15, 20, 25), pick(30, 40, 45, 50)
    uh, uv = u * math.cos(math.radians(th)), u * math.sin(math.radians(th))
    ex.on("Projectile Motion").num(f"The ball is hit at {u} m/s at {th}° to the horizontal. Calculate the vertical component of its initial velocity.", uv, "m/s",
        wrong=[(uh, "Vertical component = u sin θ."), (u, "Resolve the velocity.")],
        working=[rf"u_v = u\sin\theta = {u} \sin {th}^\circ = {ltx(uv)}\ \text{{m/s}}"])
    tf = 2 * sig(uv) / g
    ex.on("Projectile Motion").num("Using your value of g for the Moon, calculate the time of flight (it lands at the same level).", tf, "s",
        wrong=[(sig(uv) / g, "That's the time to the top — double it."), (2 * sig(uv) / G, "Use the Moon's g, not 9.8.")],
        working=[rf"t = \frac{{2u_v}}{{g}} = \frac{{2 \times {ltx(uv)}}}{{{ltx(g)}}} = {ltx(tf)}\ \text{{s}}"])
    rng = sig(uh) * sig(tf)
    ex.on("Projectile Motion").num("Calculate the horizontal distance travelled by the ball.", rng, "m",
        wrong=[(u * sig(tf), "Use the HORIZONTAL component, u cos θ."), (sig(uv) * sig(tf), "Horizontal: u cos θ.")],
        working=[rf"d = u_h t = ({u}\cos {th}^\circ) \times {ltx(tf)} = {ltx(rng)}\ \text{{m}}"])
    return ex.build("An astronaut hits a golf ball on the Moon. (Mass of Moon = 7.3 × 10²² kg, radius = 1.74 × 10⁶ m, "
                    "G = 6.67 × 10⁻¹¹ N m² kg⁻²; ignore the curvature of the Moon)", )


def mars_drop(level="Higher"):
    ex = _ex(level, UNIT2)
    M, R = 6.4e23, 3.4e6
    m = pick(150, 250, 400)
    F = G_N * M * m / R ** 2
    ex.on("Gravitation").num(f"Calculate the gravitational force on a {m} kg lander at the surface of Mars.", F, "N",
        wrong=[(G_N * M * m / R, "Square the radius."), (m * G, "Use F = GMm/r² for Mars.")],
        working=[rf"F = \frac{{6.67\times10^{{-11}} \times 6.4\times10^{{23}} \times {m}}}{{(3.4\times10^6)^2}} = {ltx(F)}\ \text{{N}}"])
    g = sig(F) / m
    ex.on("Gravitation").num("Calculate the gravitational field strength at the surface of Mars.", g, "N/kg",
        wrong=[(sig(F) * m, "g = F ÷ m.")], working=[rf"g = \frac{{F}}{{m}} = {ltx(g)}\ \text{{N/kg}}"])
    h, vh = pick(20, 30, 45), pick(5, 8, 10)
    t = math.sqrt(2 * h / sig(g))
    ex.on("Projectile Motion").num(f"Flying horizontally at {vh} m/s, {h} m above the ground, the lander drops a probe. Calculate the time the probe takes to fall.",
        t, "s",
        wrong=[(math.sqrt(2 * h / G), "Use g on Mars."), (2 * h / sig(g), "Take the square root: s = ½gt²."), (math.sqrt(h / sig(g)), "s = ½gt² → t = √(2s/g).")],
        working=[r"s = ut + \tfrac{1}{2}at^2", rf"{h} = 0 + \tfrac{{1}}{{2}} \times {ltx(g)} \times t^2", rf"t = {ltx(t)}\ \text{{s}}"])
    ex.on("Projectile Motion").num("Calculate the horizontal distance the probe travels while falling.", vh * sig(t), "m",
        wrong=[(0.5 * vh * sig(t), "Horizontal velocity is constant — no ½.")],
        working=[rf"d = v_h t = {vh} \times {ltx(t)} = {ltx(vh * sig(t))}\ \text{{m}}"])
    ex.on("Gravitation").choice("How would the fall time compare if the probe were dropped from the same height on Earth?",
        "Shorter — g is larger on Earth.", [("Longer — g is larger on Earth.", "Larger g → faster fall → shorter time."),
                                           ("The same — fall time depends only on height.", "It depends on g too."),
                                           ("Longer — Earth has an atmosphere.", "Ignoring air resistance, larger g gives a shorter time.")])
    return ex.build("A lander explores Mars. (Mass of Mars = 6.4 × 10²³ kg, radius = 3.4 × 10⁶ m, G = 6.67 × 10⁻¹¹ N m² kg⁻²)")


def star_journey(level="Higher"):
    ex = _ex(level, UNIT2)
    frac, d_ly = pick(0.6, 0.8, 0.9), pick(4.2, 6.0, 8.6, 12.0)
    k = math.sqrt(1 - frac ** 2)
    t_e = d_ly / frac
    ex.on("Special Relativity").num(f"The ship travels at {frac:g}c to a star {d_ly:g} light-years away (measured from Earth). "
        f"Calculate the journey time measured on Earth, in years.", t_e, "",
        wrong=[(d_ly * frac, "t = d ÷ v."), (d_ly, f"The ship travels at {frac:g}c, not c.")],
        working=[rf"t = \frac{{d}}{{v}} = \frac{{{d_ly:g}\ \text{{ly}}}}{{{frac:g}c}} = {ltx(t_e)}\ \text{{years}}"])
    ex.on("Special Relativity").num("Calculate the journey time measured by the crew, in years.", sig(t_e) * k, "",
        wrong=[(sig(t_e) / k, "The crew's clock is the moving clock — it records the SHORTER (proper) time.")],
        working=[r"t' = \frac{t}{\sqrt{1 - v^2/c^2}} \Rightarrow t_{crew} = t_{Earth}\sqrt{1 - v^2/c^2}",
                 rf"t_{{crew}} = {ltx(t_e)} \times \sqrt{{1 - {frac:g}^2}} = {ltx(sig(t_e) * k)}\ \text{{years}}"])
    ex.on("Special Relativity").num("Calculate the distance to the star as measured by the crew, in light-years.", d_ly * k, "",
        wrong=[(d_ly / k, "Lengths CONTRACT for the moving observer: l' = l√(1 − v²/c²).")],
        working=[rf"l' = {d_ly:g}\sqrt{{1 - {frac:g}^2}} = {ltx(d_ly * k)}\ \text{{ly}}"])
    ex.on("The Expanding Universe").choice("The ship sends a radio signal back to Earth while moving away. How does the received frequency compare with the transmitted frequency?",
        "It is lower — the source is moving away (Doppler effect).",
        [("It is higher — the source is moving away.", "Moving away → longer wavelength → lower frequency."),
         ("It is the same — radio waves travel at c.", "The speed is c, but the frequency is Doppler-shifted."),
         ("It is zero — signals can't catch up.", "Signals travel at c, faster than the ship.")])
    ex.on("Special Relativity").choice("What speed would observers on Earth measure for that radio signal?", "3.00 × 10⁸ m/s",
        [(f"{1 - frac:g}c", "The speed of light is the same for all observers."), (f"{1 + frac:g}c", "Speeds don't add for light."),
         ("It depends on the ship's speed.", "c is the same in every frame.")])
    return ex.build(f"A spaceship travels from Earth to a distant star at a constant speed of {frac:g}c.")


def space_telescope(level="Higher"):
    ex = _ex(level, UNIT2)
    m, h_km = pick(11000, 6500, 2400), pick(540, 600, 700)
    r = R_EARTH + h_km * 1000
    F = G_N * M_EARTH * m / sig(r) ** 2
    ex.on("Gravitation").num(f"The telescope ({m} kg) orbits {h_km} km above the Earth's surface. Calculate the gravitational force on it.", F, "N",
        wrong=[(G_N * M_EARTH * m / (h_km * 1000) ** 2, "r is from Earth's CENTRE: add the radius."), (G_N * M_EARTH * m / sig(r), "Square r.")],
        working=[rf"r = 6.4\times10^6 + {h_km}\times10^3 = {ltx(r)}\ \text{{m}}",
                 rf"F = \frac{{6.67\times10^{{-11}} \times 6.0\times10^{{24}} \times {m}}}{{({ltx(r)})^2}} = {ltx(F)}\ \text{{N}}"])
    lam_r = pick(656, 486)
    z = pick(0.010, 0.015, 0.020, 0.025)
    lam_o = round(lam_r * (1 + z), 1)
    zc = (lam_o - lam_r) / lam_r
    ex.on("The Expanding Universe").num(f"A hydrogen line of rest wavelength {lam_r} nm is observed at {lam_o:g} nm in a galaxy's spectrum. Calculate the redshift.",
        zc, "", wrong=[((lam_o - lam_r) / lam_o, "Divide by the REST wavelength."), (lam_o / lam_r, "z = Δλ ÷ λ_rest.")],
        working=[rf"z = \frac{{{lam_o:g} - {lam_r}}}{{{lam_r}}} = {ltx(zc)}"])
    v = sig(zc) * C
    ex.on("The Expanding Universe").num("Calculate the recessional velocity of the galaxy.", v, "m/s",
        wrong=[(sig(zc) / C, "v = zc.")], working=[rf"v = zc = {ltx(zc)} \times 3.00\times10^8 = {ltx(v)}\ \text{{m/s}}"])
    ex.on("The Expanding Universe").num("Calculate the distance to the galaxy.", sig(v) / H0, "m",
        wrong=[(sig(v) * H0, "d = v ÷ H₀.")], working=[rf"d = \frac{{v}}{{H_0}} = \frac{{{ltx(v)}}}{{2.3\times10^{{-18}}}} = {ltx(sig(v) / H0)}\ \text{{m}}"])
    ex.on("The Expanding Universe").choice("Observations show the expansion of the Universe is accelerating. What is this attributed to?", "Dark energy",
        [("Dark matter", "Dark matter explains galaxy rotation speeds."), ("Gravity", "Gravity would slow the expansion."),
         ("Redshift", "Redshift is the evidence, not the cause.")])
    return ex.build("A space telescope in orbit around the Earth observes distant galaxies. (Mass of Earth = 6.0 × 10²⁴ kg, radius = 6.4 × 10⁶ m, "
                    "H₀ = 2.3 × 10⁻¹⁸ s⁻¹)")


def off_a_cliff(level="Higher"):
    ex = _ex(level, UNIT2).on("Projectile Motion")
    what, below = random.choice([("ball", "sea"), ("stone", "beach"), ("ball", "ground")])
    u, th, h = pick(12, 15, 18, 20), pick(30, 35, 40, 45), pick(15, 20, 25, 30, 40)
    uh, uv = u * math.cos(math.radians(th)), u * math.sin(math.radians(th))
    ex.num("Calculate the vertical component of the initial velocity.", uv, "m/s",
           wrong=[(uh, "Vertical component = u sin θ."), (u, "Resolve the velocity into components.")],
           working=[rf"u_v = u\sin\theta = {u} \sin {th}^\circ = {ltx(uv)}\ \text{{m/s}}"])
    t1 = uv / G
    rise = uv ** 2 / (2 * G)
    Hmax = h + rise
    ex.num(f"Calculate the maximum height of the {what} above the {below}.", Hmax, "m",
           wrong=[(rise, f"That's the height above the LAUNCH point — add the {h} m cliff."), (h + uv ** 2 / G, "v² = u² + 2as: include the 2.")],
           working=[r"v^2 = u^2 + 2as", rf"0 = {ltx(uv)}^2 + 2(-9.8)s \Rightarrow s = {ltx(rise)}\ \text{{m}}",
                    rf"H = {h} + {ltx(rise)} = {ltx(Hmax)}\ \text{{m}}"],
           scaffold=[("Height gained above the launch point, in m?", rise, "m")])
    t2 = math.sqrt(2 * Hmax / G)
    ex.num(f"Calculate the total time the {what} is in the air.", t1 + t2, "s",
           wrong=[(2 * t1, f"That's the time to return to the LAUNCH height — the {what} keeps falling to the {below}."),
                  (t2, "Add the time taken to rise to the highest point."),
                  (t1 + math.sqrt(2 * h / G), f"From the highest point it falls the FULL height H = {fmt(Hmax)} m, not just the cliff height.")],
           working=[T("Time to the highest point:"), rf"0 = {ltx(uv)} + (-9.8)t_1 \Rightarrow t_1 = {ltx(t1)}\ \text{{s}}",
                    T(f"From the highest point (u = 0) it falls {fmt(Hmax)} m:"),
                    rf"{ltx(Hmax)} = \tfrac{{1}}{{2}} \times 9.8 \times t_2^2 \Rightarrow t_2 = {ltx(t2)}\ \text{{s}}",
                    rf"t = t_1 + t_2 = {ltx(t1 + t2)}\ \text{{s}}"],
           scaffold=[("Time to the highest point, in s?", t1, "s"), ("Time to fall from the highest point, in s?", t2, "s")])
    d = uh * (t1 + t2)
    ex.num(f"Calculate the horizontal distance from the foot of the cliff to where the {what} lands.", d, "m",
           wrong=[(u * (t1 + t2), "Use the HORIZONTAL component, u cos θ."), (uh * 2 * t1, "Use the total time of flight, including the fall below the cliff top.")],
           working=[rf"u_h = {u}\cos {th}^\circ = {ltx(uh)}\ \text{{m/s}}", rf"d = u_h t = {ltx(uh)} \times {ltx(t1 + t2)} = {ltx(d)}\ \text{{m}}"])
    vv = -G * t2
    ex.num(f"Calculate the vertical velocity of the {what} just before it lands (take upwards as positive).", vv, "m/s",
           wrong=[(-vv, "It is moving DOWN, so the vertical velocity is negative."), (-uv, f"It lands {h} m below its launch point, so it is moving faster than it was launched.")],
           working=[rf"v = u + at = 0 + (-9.8) \times {ltx(t2)} = {ltx(vv)}\ \text{{m/s}}"])
    ex.choice(f"In practice, air resistance acts on the {what}. How does this affect where it lands?",
              "It lands closer to the cliff, because air resistance reduces its horizontal velocity.",
              [("It lands further away, because air resistance slows its fall.", "Air resistance also reduces the horizontal velocity, so the range is shorter."),
               ("It lands in the same place — air resistance only acts vertically.", "Air resistance opposes the motion in every direction, including horizontally."),
               ("It lands in the same place — the horizontal velocity is always constant.", "That's only true when air resistance is ignored.")])
    return ex.build(f"A {what} is launched at {u} m/s at {th}° above the horizontal from the top of a cliff {h} m above the {below}. "
                    f"Ignore air resistance unless told otherwise.",
                    diagram=cliff_launch(f"u = {u} m/s", f"{th}°", f"{h} m", what))


def onto_a_platform(level="Higher"):
    ex = _ex(level, UNIT2).on("Projectile Motion")
    what = pick("ball", "beanbag")
    u, th = pick(14, 16, 18, 20), pick(50, 55, 60)
    uh, uv = u * math.cos(math.radians(th)), u * math.sin(math.radians(th))
    Hmax = uv ** 2 / (2 * G)
    h = round(Hmax * random.uniform(0.3, 0.65), 1)
    ex.num("Calculate the horizontal component of the initial velocity.", uh, "m/s",
           wrong=[(uv, "Horizontal component = u cos θ."), (u, "Resolve the velocity into components.")],
           working=[rf"u_h = u\cos\theta = {u} \cos {th}^\circ = {ltx(uh)}\ \text{{m/s}}"])
    ex.num(f"Calculate the maximum height reached by the {what}.", Hmax, "m",
           wrong=[(uv ** 2 / G, "v² = u² + 2as: include the 2."), (u ** 2 / (2 * G), "Use the VERTICAL component, u sin θ.")],
           working=[rf"u_v = {u}\sin {th}^\circ = {ltx(uv)}\ \text{{m/s}}", rf"0 = {ltx(uv)}^2 + 2(-9.8)s \Rightarrow s = {ltx(Hmax)}\ \text{{m}}"],
           scaffold=[("Vertical component of the initial velocity, in m/s?", uv, "m/s")])
    t1 = uv / G
    drop = Hmax - h
    t2 = math.sqrt(2 * drop / G)
    ex.num(f"The {what} lands on the platform while it is falling. Calculate the time from launch until it lands.", t1 + t2, "s",
           wrong=[(2 * t1, "That's the time to return to GROUND level — the platform is higher, so it lands sooner."),
                  (t1 - t2, "That's when it passes the platform's height on the way UP; it lands on the way down."),
                  (t1 + math.sqrt(2 * h / G), f"From the highest point it only falls H − h = {fmt(drop)} m to the platform.")],
           working=[rf"t_1 = \frac{{u_v}}{{g}} = \frac{{{ltx(uv)}}}{{9.8}} = {ltx(t1)}\ \text{{s}}",
                    T(f"From the highest point (u = 0) it falls {fmt(Hmax)} − {h:g} = {fmt(drop)} m:"),
                    rf"{ltx(drop)} = \tfrac{{1}}{{2}} \times 9.8 \times t_2^2 \Rightarrow t_2 = {ltx(t2)}\ \text{{s}}",
                    rf"t = t_1 + t_2 = {ltx(t1 + t2)}\ \text{{s}}"],
           scaffold=[("Time to the highest point, in s?", t1, "s"), ("Height fallen from the highest point to the platform, in m?", drop, "m")])
    d = uh * (t1 + t2)
    ex.num(f"Calculate the horizontal distance the {what} travels before landing.", d, "m",
           wrong=[(u * (t1 + t2), "Use the horizontal component, u cos θ."), (uh * 2 * t1, "Use the time until it lands on the platform.")],
           working=[rf"d = u_h t = {ltx(uh)} \times {ltx(t1 + t2)} = {ltx(d)}\ \text{{m}}"])
    vv = -G * t2
    ex.num(f"Calculate the vertical velocity of the {what} as it lands (take upwards as positive).", vv, "m/s",
           wrong=[(-vv, "It is falling, so the vertical velocity is negative."), (-uv, "It lands higher than it started, so it is moving more slowly than at launch.")],
           working=[rf"v = u + at = 0 + (-9.8) \times {ltx(t2)} = {ltx(vv)}\ \text{{m/s}}"])
    ex.choice(f"How does the {what}'s speed as it lands compare with its launch speed, and why?",
              "It is smaller — the platform is higher than the launch point, so some kinetic energy has become gravitational potential energy.",
              [("It is the same — the horizontal velocity is constant.", "The VERTICAL velocity is smaller on landing, so the speed is smaller."),
               ("It is larger — it has been accelerating downwards.", "It hasn't fallen back to its launch height."),
               ("It is smaller because of air resistance.", "Air resistance is ignored here; it's because the platform is higher.")])
    return ex.build(f"A {what} is thrown from ground level at {u} m/s at {th}° above the horizontal. It lands on a flat platform "
                    f"{h:g} m above the ground. Ignore air resistance.",
                    diagram=platform_landing(f"u = {u} m/s", f"{th}°", f"{h:g} m", what))


SCENARIOS_PART1 = {
    "Car and Trailer":    car_and_trailer,
    "Skier":              skier,
    "Lift Journey":       lift_journey,
    "Trolley Collision":  trolley_collision,
    "Thrown Ball":        thrown_ball,
}

SCENARIOS_PART2 = {
    "Off a Cliff":        off_a_cliff,
    "Onto a Platform":    onto_a_platform,
    "Golf on the Moon":   moon_golf,
    "Lander on Mars":     mars_drop,
    "Journey to a Star":  star_journey,
    "Space Telescope":    space_telescope,
}
