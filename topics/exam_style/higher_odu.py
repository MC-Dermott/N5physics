"""Higher Our Dynamic Universe — exam-style multi-part questions, one generator per topic.

Recognised wrong answers follow the Higher marking instructions and course reports: sign errors in
the equations of motion (deceleration taken as positive, g not negative going up), the change in
momentum found without reversing the sign of a rebound velocity, Ek treated as conserved in an
inelastic collision, mg sin θ / mg cos θ swapped, the radius used without adding the height,
the Lorentz factor applied the wrong way round, and the redshift calculated from the emitted
wavelength instead of the change.
"""
import math
import random

from topics.dynamics.projectile_higher import generate_projectile_exam_mixed
from topics.dynamics.towing import gen_exam_style as gen_towing_exam_style
from topics.exam_style.base import Exam, T, exam_style, fmt, graph, ltx, pick, reuse, sig

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


def _ex(qtype, level, unit=UNIT1):
    return Exam(unit, qtype, level, NOTES[qtype])


# ════════════════ Equations of Motion ════════════════

def _eom_braking(level="Higher"):
    ex = _ex("Equations of Motion", level)
    u, a = pick(18, 20, 24, 25, 30), -pick(4.0, 5.0, 6.0, 7.5)
    s = -u ** 2 / (2 * a)
    ex.num("Calculate the distance the car travels while braking.", s, "m",
           wrong=[(u ** 2 / -a, "v² = u² + 2as: don't forget the 2."), (u ** 2 / (2 * a), "a is negative (deceleration), so s = −u² ÷ 2a is positive."),
                  (u / -a, "Use v² = u² + 2as.")],
           working=[r"v^2 = u^2 + 2as", rf"0 = {u}^2 + 2 \times ({a:g}) \times s", rf"s = {ltx(s)}\ \text{{m}}"])
    t = -u / a
    ex.num("Calculate the time taken for the car to stop.", t, "s",
           wrong=[(u * -a, "v = u + at → t = (v − u) ÷ a."), (2 * t, "v = u + at.")],
           working=[r"v = u + at", rf"0 = {u} + ({a:g})t", rf"t = {ltx(t)}\ \text{{s}}"])
    t1 = pick(1.0, 1.5, 2.0)
    s1 = u * t1 + 0.5 * a * t1 ** 2
    ex.num(f"Calculate the distance travelled in the first {t1:g} s of braking.", s1, "m",
           wrong=[(u * t1 - 0.5 * a * t1 ** 2, "The car is decelerating: a is NEGATIVE in s = ut + ½at²."), (u * t1, "Include the ½at² term.")],
           working=[r"s = ut + \tfrac{1}{2}at^2", rf"s = ({u} \times {t1:g}) + \tfrac{{1}}{{2}} \times ({a:g}) \times {t1:g}^2", rf"s = {ltx(s1)}\ \text{{m}}"])
    return ex.build(f"A car travelling at {u} m/s brakes with a constant deceleration of {-a:g} m/s² until it stops.")


def _eom_throw(level="Higher"):
    ex = _ex("Equations of Motion", level)
    u = pick(8.0, 9.8, 12.0, 14.7, 15.0)
    h = u ** 2 / (2 * G)
    ex.num("Calculate the maximum height reached by the ball above the point of release.", h, "m",
           wrong=[(u ** 2 / G, "v² = u² + 2as — the 2 is needed."), (u / G, "Use v² = u² + 2as with v = 0.")],
           working=[r"v^2 = u^2 + 2as", rf"0 = {u:g}^2 + 2 \times (-9.8) \times s", rf"s = {ltx(h)}\ \text{{m}}"])
    t = u / G
    ex.num("Calculate the time taken to reach the maximum height.", t, "s",
           wrong=[(u * G, "v = u + at → t = −u ÷ a."), (2 * t, "That's the time to return to the hand.")],
           working=[r"v = u + at", rf"0 = {u:g} + (-9.8)t", rf"t = {ltx(t)}\ \text{{s}}"])
    hd = pick(1.0, 1.5, 2.0)
    v = -math.sqrt(u ** 2 + 2 * G * hd)
    ex.num(f"The ball misses the catcher and lands {hd:g} m below the point of release. Calculate its velocity just before it lands "
           f"(take upwards as positive).", v, "m/s",
           wrong=[(-v, "The ball is moving DOWN — the velocity is negative."), (-math.sqrt(u ** 2 - 2 * G * hd) if u ** 2 > 2 * G * hd else -u, "s is negative (below the release point) and a is negative: 2as is positive."),
                  (-u, "It falls further than its release height, so it's faster than u.")],
           working=[r"v^2 = u^2 + 2as", rf"v^2 = {u:g}^2 + 2 \times (-9.8) \times (-{hd:g})", rf"v = -{ltx(-v)}\ \text{{m/s}}"])
    return ex.build(f"A ball is thrown vertically upwards with a speed of {u:g} m/s. Air resistance can be ignored.")


def _eom_runway(level="Higher"):
    ex = _ex("Equations of Motion", level)
    a, s = pick(2.0, 2.5, 3.0, 3.5), pick(1200, 1500, 1800, 2000)
    v = math.sqrt(2 * a * s)
    ex.num(f"The aircraft accelerates uniformly from rest at {a:g} m/s² along {s} m of runway. Calculate its speed at the end of the runway.",
           v, "m/s",
           wrong=[(2 * a * s, "Take the square root: v = √(2as)."), (math.sqrt(a * s), "v² = u² + 2as — include the 2."), (a * s, "Use v² = u² + 2as.")],
           working=[r"v^2 = u^2 + 2as", rf"v^2 = 0 + 2 \times {a:g} \times {s}", rf"v = {ltx(v)}\ \text{{m/s}}"])
    t = sig(v) / a
    ex.num("Calculate the time taken to travel along the runway.", t, "s",
           wrong=[(sig(v) * a, "t = (v − u) ÷ a."), (s / sig(v), "The speed isn't constant — use v = u + at (or s = ½(u+v)t).")],
           working=[r"v = u + at", rf"{ltx(v)} = 0 + {a:g}t", rf"t = {ltx(t)}\ \text{{s}}"])
    ex.num("Calculate the average speed of the aircraft along the runway.", sig(v) / 2, "m/s",
           wrong=[(sig(v), "That's the final speed."), (s / t / 2, "Average speed = total distance ÷ total time.")],
           working=[rf"\bar{{v}} = \frac{{s}}{{t}} = \frac{{{s}}}{{{ltx(t)}}} = {ltx(sig(v) / 2)}\ \text{{m/s}}"])
    return ex.build("An aircraft takes off from a runway.")


gen_eom_exam = exam_style(_eom_braking, _eom_throw, _eom_runway)


# ════════════════ Graphs of Motion ════════════════

def _gom_ball(level="Higher"):
    ex = _ex("Graphs of Motion", level)
    u = pick(9.8, 14.7, 19.6)
    t_top = u / G
    fig = graph([(0, u), (t_top, 0), (2 * t_top, -u)], labels=["", "P", ""])
    ex.num("Use the graph to calculate the acceleration of the ball.", -G, "m/s²",
           wrong=[(G, "The gradient is negative (the line slopes down)."), (u / (2 * t_top), "Gradient = Δv ÷ Δt over a straight section.")],
           working=[rf"a = \frac{{\Delta v}}{{\Delta t}} = \frac{{0 - {u:g}}}{{{t_top:g}}} = -9.8\ \text{{m/s}}^2"])
    h = 0.5 * u * t_top
    ex.num("Calculate the maximum height reached by the ball.", h, "m",
           wrong=[(u * t_top, "Area of a triangle = ½ × base × height."), (0, "That's the displacement at the END; the maximum height is at P.")],
           working=[rf"s = \text{{area}} = \tfrac{{1}}{{2}} \times {t_top:g} \times {u:g} = {ltx(h)}\ \text{{m}}"])
    ex.num(f"Calculate the displacement of the ball after {2 * t_top:g} s.", 0, "m",
           wrong=[(2 * h, "Area BELOW the axis is negative displacement — the two areas cancel."), (h, "Include the area below the axis (negative).")],
           working=[rf"s = (+{ltx(h)}) + (-{ltx(h)}) = 0\ \text{{m}}"])
    ex.choice("Which statement describes the acceleration–time graph for the ball's flight?",
              "A horizontal line at −9.8 m/s² for the whole flight.",
              [("A line that is zero at P, the top of the flight.", "The acceleration is −9.8 m/s² even at the top; only the VELOCITY is zero."),
               ("A horizontal line at +9.8 m/s² while rising and −9.8 m/s² while falling.", "The acceleration is always downwards."),
               ("A straight line sloping down from +9.8 to −9.8 m/s².", "That's the shape of the VELOCITY–time graph.")])
    return ex.build(f"A ball is thrown vertically upwards with a speed of {u:g} m/s and caught at the same height. The graph shows its "
                    f"velocity (upwards positive). Air resistance can be ignored.", figure=fig)


def _gom_lift(level="Higher"):
    ex = _ex("Graphs of Motion", level)
    v = pick(2.0, 2.5, 3.0, 4.0)
    t1, t2, t3 = pick(2, 2.5, 4), pick(6, 8, 10), pick(2, 4, 5)
    T1, T2, T3 = t1, t1 + t2, t1 + t2 + t3
    fig = graph([(0, 0), (T1, v), (T2, v), (T3, 0)], labels=["", "A", "B", "C"])
    ex.num("Calculate the acceleration of the lift between B and C.", -v / t3, "m/s²",
           wrong=[(v / t3, "The lift slows down — the acceleration is negative.")],
           working=[rf"a = \frac{{0 - {v:g}}}{{{t3:g}}} = {ltx(-v / t3)}\ \text{{m/s}}^2"])
    s = 0.5 * v * t1 + v * t2 + 0.5 * v * t3
    ex.num("Calculate the total distance the lift rises.", s, "m",
           wrong=[(v * T3, "The first and last sections are triangles."), (v * t2, "Include all three sections.")],
           working=[rf"s = \tfrac{{1}}{{2}}({t1:g})({v:g}) + ({t2:g})({v:g}) + \tfrac{{1}}{{2}}({t3:g})({v:g}) = {ltx(s)}\ \text{{m}}"])
    ex.choice("Which describes the acceleration–time graph for this journey?",
              f"Positive constant ({fmt(v / t1)} m/s²) from 0 to A, zero from A to B, negative constant from B to C.",
              [("Zero throughout, because the lift ends at rest.", "The lift accelerates and decelerates."),
               ("Positive throughout, because the lift moves upwards the whole time.", "The direction of motion isn't the direction of acceleration."),
               ("Increasing from 0 to A, constant from A to B, decreasing from B to C.", "That's the shape of the velocity–time graph.")])
    return ex.build("The velocity–time graph shows the motion of a lift moving upwards between two floors.", figure=fig)


gen_gom_exam = exam_style(_gom_ball, _gom_lift)


# ════════════════ Components of Vectors ════════════════

def _cov_slope(level="Higher"):
    ex = _ex("Components of Vectors", level)
    m, th = pick(2.0, 3.5, 5.0, 8.0, 12.0), pick(15, 20, 25, 30, 35)
    W_par = m * G * math.sin(math.radians(th))
    ex.num("Calculate the component of the block's weight acting down the slope.", W_par, "N",
           wrong=[(m * G * math.cos(math.radians(th)), "Down the slope is mg sin θ; mg cos θ is perpendicular to the slope."),
                  (m * math.sin(math.radians(th)), "Use the weight (mg).")],
           working=[r"W_\parallel = mg\sin\theta", rf"W_\parallel = {m:g} \times 9.8 \times \sin {th}^\circ = {ltx(W_par)}\ \text{{N}}"])
    Ff = sig(W_par * random.uniform(0.3, 0.7), 2)
    a = (sig(W_par) - Ff) / m
    ex.num(f"A constant frictional force of {Ff:g} N acts on the block. Calculate its acceleration down the slope.", a, "m/s²",
           wrong=[(sig(W_par) / m, "Subtract the friction to find the unbalanced force."), ((sig(W_par) + Ff) / m, "Friction acts UP the slope — subtract it."),
                  (G * math.sin(math.radians(th)), "Include the frictional force.")],
           working=[rf"F_{{un}} = {ltx(W_par)} - {Ff:g} = {ltx(sig(W_par) - Ff)}\ \text{{N}}", r"a = \frac{F_{un}}{m}", rf"a = {ltx(a)}\ \text{{m/s}}^2"])
    ex.choice("The angle of the slope is increased. What happens to the component of the weight down the slope?",
              "It increases, because sin θ increases as θ increases.",
              [("It decreases, because cos θ decreases.", "The component DOWN the slope is mg sin θ."),
               ("It stays the same — the weight hasn't changed.", "The weight is the same, but its component along the slope changes."),
               ("It becomes zero at 45°.", "sin θ increases all the way to 90°.")])
    return ex.build(f"A block of mass {m:g} kg slides down a slope at {th}° to the horizontal.")


def _cov_sledge(level="Higher"):
    ex = _ex("Components of Vectors", level)
    F, th = pick(40, 60, 80, 120), pick(20, 25, 30, 35, 40)
    Fh = F * math.cos(math.radians(th))
    ex.num(f"Calculate the horizontal component of the pulling force.", Fh, "N",
           wrong=[(F * math.sin(math.radians(th)), "The horizontal (adjacent) component is F cos θ."), (F, "Only the horizontal component moves the sledge forward.")],
           working=[rf"F_h = F\cos\theta = {F} \cos {th}^\circ = {ltx(Fh)}\ \text{{N}}"])
    m, Ff = pick(15, 20, 25, 30), sig(Fh * random.uniform(0.4, 0.8), 2)
    a = (sig(Fh) - Ff) / m
    ex.num(f"The sledge has a mass of {m} kg and the frictional force on it is {Ff:g} N. Calculate its acceleration.", a, "m/s²",
           wrong=[((F - Ff) / m, "Use the HORIZONTAL component of the pull."), (sig(Fh) / m, "Subtract the friction.")],
           working=[rf"F_{{un}} = {ltx(Fh)} - {Ff:g} = {ltx(sig(Fh) - Ff)}\ \text{{N}}", rf"a = \frac{{F_{{un}}}}{{m}} = {ltx(a)}\ \text{{m/s}}^2"])
    d = pick(10, 20, 25)
    W = sig(Fh) * d
    ex.num(f"Calculate the work done by the pulling force as the sledge moves {d} m horizontally.", W, "J",
           wrong=[(F * d, "Only the component in the direction of motion does work: F cos θ × d.")],
           working=[rf"E_w = F_h d = {ltx(Fh)} \times {d} = {ltx(W)}\ \text{{J}}"])
    return ex.build(f"A child pulls a sledge across flat snow with a force of {F} N, using a rope at {th}° above the horizontal.")


gen_components_exam = exam_style(_cov_slope, _cov_sledge)


# ════════════════ Momentum and Impulse ════════════════

def _mom_collision(level="Higher"):
    ex = _ex("Momentum and Impulse", level)
    m1, m2, u1 = random.choice([(1200, 800, 15), (1500, 1000, 12), (0.4, 0.6, 3.0), (2.0, 3.0, 5.0), (900, 1100, 20)])
    v = m1 * u1 / (m1 + m2)
    ex.num("The two objects stick together after the collision. Calculate their velocity immediately after.", v, "m/s",
           wrong=[(m1 * u1 / m2, "After the collision the combined mass (m₁ + m₂) moves together."), (u1 / 2, "Use conservation of momentum."),
                  (u1, "Momentum is shared with the second object, so the velocity drops.")],
           working=[r"m_1u_1 + m_2u_2 = (m_1 + m_2)v", rf"{m1:g} \times {u1:g} + 0 = ({m1:g} + {m2:g})v", rf"v = {ltx(v)}\ \text{{m/s}}"])
    Ek1 = 0.5 * m1 * u1 ** 2
    Ek2 = 0.5 * (m1 + m2) * sig(v) ** 2
    ex.num("Calculate the kinetic energy lost in the collision.", Ek1 - Ek2, "J",
           wrong=[(Ek1, "Subtract the kinetic energy after the collision."), (Ek2, "Find the DIFFERENCE before − after.")],
           working=[rf"E_{{k,before}} = \tfrac{{1}}{{2}}({m1:g})({u1:g})^2 = {ltx(Ek1)}\ \text{{J}}",
                    rf"E_{{k,after}} = \tfrac{{1}}{{2}}({m1 + m2:g})({ltx(v)})^2 = {ltx(Ek2)}\ \text{{J}}", rf"\Delta E_k = {ltx(Ek1 - Ek2)}\ \text{{J}}"],
           scaffold=[("Ek before, in J?", Ek1, "J"), ("Ek after, in J?", Ek2, "J")])
    ex.choice("Is the collision elastic or inelastic?", "Inelastic — kinetic energy is not conserved.",
              [("Elastic — momentum is conserved.", "Momentum is conserved in ALL collisions; elastic means Ek is conserved too."),
               ("Elastic — kinetic energy is conserved.", "Kinetic energy was lost."),
               ("Inelastic — momentum is not conserved.", "Momentum IS conserved; it's Ek that isn't.")])
    return ex.build(f"An object of mass {m1:g} kg moving at {u1:g} m/s collides with a stationary object of mass {m2:g} kg.")


def _mom_bat(level="Higher"):
    ex = _ex("Momentum and Impulse", level)
    m, u, v, t_ms = pick(0.057, 0.145, 0.16), pick(20, 25, 30), pick(25, 30, 35, 40), pick(1.5, 2.0, 3.0, 5.0)
    dp = m * v - m * (-u)
    ex.num(f"The ball arrives at {u} m/s and leaves in the opposite direction at {v} m/s. Calculate the size of its change in momentum.",
           dp, "kg m/s",
           wrong=[(m * (v - u), "The ball reverses direction: Δp = mv − mu with u NEGATIVE."), (m * v, "Include the initial momentum.")],
           working=[rf"\Delta p = mv - mu = {m:g} \times {v} - {m:g} \times (-{u}) = {ltx(dp)}\ \text{{kg m/s}}"])
    F = sig(dp) / (t_ms / 1000)
    ex.num(f"The bat is in contact with the ball for {t_ms:g} ms. Calculate the average force exerted on the ball.", F, "N",
           wrong=[(sig(dp) / t_ms, "Convert ms to s."), (sig(dp) * t_ms / 1000, "F = Δp ÷ t.")],
           working=[r"Ft = \Delta p", rf"F = \frac{{{ltx(dp)}}}{{{t_ms:g} \times 10^{{-3}}}} = {ltx(F)}\ \text{{N}}"])
    ex.choice("The player 'follows through' so the bat stays in contact with the ball for longer, with the same average force. What is the effect?",
              "The impulse is greater, so the ball's change in momentum is greater and it leaves faster.",
              [("The force on the ball is reduced, so it leaves slower.", "The force is the same; a longer time gives a bigger impulse."),
               ("There's no effect — the force is the same.", "Impulse = F × t, so a longer time increases it."),
               ("The ball's mass increases.", "Mass is unchanged.")])
    return ex.build(f"A ball of mass {m:g} kg is hit by a bat.")


def _mom_recoil(level="Higher"):
    ex = _ex("Momentum and Impulse", level)
    mb, vb, mc = random.choice([(0.02, 400, 4.0), (5.0, 200, 1500), (0.05, 300, 5.0), (12, 150, 2000)])
    vc = -mb * vb / mc
    ex.num(f"The projectile leaves at {vb} m/s. Calculate the recoil velocity of the gun (take the projectile's direction as positive).",
           vc, "m/s",
           wrong=[(-vc, "The gun recoils BACKWARDS — negative velocity."), (-vb / mc, "Use momentum: mass × velocity of the projectile.")],
           working=[r"0 = m_bv_b + m_gv_g", rf"0 = {mb:g} \times {vb} + {mc:g}v_g", rf"v_g = {ltx(vc)}\ \text{{m/s}}"])
    Ek = 0.5 * mb * vb ** 2 + 0.5 * mc * sig(vc) ** 2
    ex.num("Calculate the total kinetic energy produced in the firing.", Ek, "J",
           wrong=[(0.5 * mb * vb ** 2, "Include the gun's kinetic energy as well."), (0, "Momentum is zero before and after, but Ek is not.")],
           working=[rf"E_k = \tfrac{{1}}{{2}}({mb:g})({vb})^2 + \tfrac{{1}}{{2}}({mc:g})({ltx(vc)})^2 = {ltx(Ek)}\ \text{{J}}"])
    ex.choice("What is the total momentum of the gun and projectile just after firing?", "Zero",
              [("Equal to the projectile's momentum.", "The gun has an equal and opposite momentum."), ("Double the projectile's momentum.", "They're in opposite directions."),
               ("It can't be found without the force.", "Momentum is conserved: zero before, so zero after.")])
    return ex.build(f"A gun of mass {mc:g} kg, initially at rest, fires a projectile of mass {mb:g} kg.")


gen_momentum_exam = exam_style(_mom_collision, _mom_bat, _mom_recoil)


# ════════════════ Energy, Work and Power ════════════════

def _ewp_cyclist(level="Higher"):
    ex = _ex("Energy, Work and Power", level)
    m, h, v, d = pick(70, 80, 90), pick(12, 15, 20), pick(10, 12, 14), pick(150, 200, 250)
    Ep = m * G * h
    Ek = 0.5 * m * v ** 2
    ex.num("Calculate the gravitational potential energy lost by the cyclist.", Ep, "J",
           wrong=[(m * h, "Ep = mgh.")], working=[rf"E_p = mgh = {m} \times 9.8 \times {h} = {ltx(Ep)}\ \text{{J}}"])
    ex.num("Calculate the kinetic energy of the cyclist at the bottom of the hill.", Ek, "J",
           wrong=[(m * v ** 2, "Ek = ½mv².")], working=[rf"E_k = \tfrac{{1}}{{2}}mv^2 = 0.5 \times {m} \times {v}^2 = {ltx(Ek)}\ \text{{J}}"])
    F = (sig(Ep) - sig(Ek)) / d
    ex.num(f"The road down the hill is {d} m long. Calculate the average frictional force on the cyclist.", F, "N",
           wrong=[(sig(Ep) / d, "Only the energy LOST (Ep − Ek) is work done against friction."), ((sig(Ep) - sig(Ek)) / h, f"Use the distance along the road ({d} m).")],
           working=[rf"E_w = E_p - E_k = {ltx(Ep)} - {ltx(Ek)} = {ltx(sig(Ep) - sig(Ek))}\ \text{{J}}", r"E_w = Fd", rf"F = {ltx(F)}\ \text{{N}}"])
    return ex.build(f"A cyclist of total mass {m} kg freewheels from rest down a hill of vertical height {h} m, reaching {v} m/s at the bottom.")


def _ewp_crane(level="Higher"):
    ex = _ex("Energy, Work and Power", level)
    m, h, t = pick(250, 400, 500, 800), pick(12, 15, 20, 30), pick(15, 20, 25, 30)
    Ep = m * G * h
    ex.num("Calculate the gravitational potential energy gained by the load.", Ep, "J",
           wrong=[(m * h, "Ep = mgh.")], working=[rf"E_p = {m} \times 9.8 \times {h} = {ltx(Ep)}\ \text{{J}}"])
    P = sig(Ep) / t
    ex.num(f"The lift takes {t} s at a constant speed. Calculate the useful power output of the crane motor.", P, "W",
           wrong=[(sig(Ep) * t, "P = E ÷ t.")], working=[rf"P = \frac{{E}}{{t}} = \frac{{{ltx(Ep)}}}{{{t}}} = {ltx(P)}\ \text{{W}}"])
    eff = pick(40, 50, 60, 75)
    Pin = P / (eff / 100)
    ex.num(f"The motor is {eff}% efficient. Calculate its input power.", Pin, "W",
           wrong=[(P * eff / 100, "Input power is GREATER than the useful output."), (P * eff, "Efficiency = useful ÷ input × 100.")],
           working=[rf"P_{{in}} = \frac{{P_{{out}}}}{{\text{{efficiency}}}} = \frac{{{ltx(P)}}}{{{eff / 100:g}}} = {ltx(Pin)}\ \text{{W}}"])
    return ex.build(f"A crane lifts a load of mass {m} kg vertically through {h} m.")


gen_ewp_exam = exam_style(_ewp_cyclist, _ewp_crane)


# ════════════════ Effective Weight ════════════════

def _ew_lift(level="Higher"):
    ex = _ex("Effective Weight", level)
    m, a = pick(50, 60, 65, 70, 80), pick(0.5, 0.8, 1.2, 1.5, 2.0)
    ex.num(f"The lift accelerates upwards at {a:g} m/s². Calculate the reading on the scales.", m * (G + a), "N",
           wrong=[(m * (G - a), "Accelerating UP increases the reading: R = m(g + a)."), (m * G, "The lift is accelerating — R ≠ mg."), (m * a, "R − mg = ma.")],
           working=[r"R - mg = ma", rf"R = {m}(9.8 + {a:g}) = {ltx(m * (G + a))}\ \text{{N}}"])
    ex.num("The lift then moves upwards at a constant speed. Calculate the reading on the scales.", m * G, "N",
           wrong=[(m * (G + a), "At constant speed a = 0, so R = mg.")], working=[rf"R = mg = {m} \times 9.8 = {ltx(m * G)}\ \text{{N}}"])
    a2 = pick(0.6, 1.0, 1.4)
    ex.num(f"The lift slows down at {a2:g} m/s² as it approaches the top floor. Calculate the reading on the scales.", m * (G - a2), "N",
           wrong=[(m * (G + a2), "Slowing down while moving UP is a DOWNWARD acceleration: R = m(g − a).")],
           working=[r"R = m(g - a)", rf"R = {m}(9.8 - {a2:g}) = {ltx(m * (G - a2))}\ \text{{N}}"])
    ex.choice("If the lift cable broke and the lift fell freely, what would the scales read?", "Zero",
              [("mg", "In free fall both the person and scales accelerate at g, so there's no contact force."),
               ("2mg", "The reading falls, not rises."), ("Slightly less than mg", "In true free fall the reading is zero.")])
    return ex.build(f"A person of mass {m} kg stands on bathroom scales in a lift.")


def _ew_find_a(level="Higher"):
    ex = _ex("Effective Weight", level)
    m = pick(55, 60, 72, 80)
    a = pick(-1.5, -1.0, 0.8, 1.2, 1.8)
    R = sig(m * (G + a))
    ex.num(f"At one point the scales read {fmt(R)} N. Calculate the acceleration of the lift (upwards positive).", (R - m * G) / m, "m/s²",
           wrong=[(R / m, "R − mg = ma: subtract the weight first."), (-(R - m * G) / m, "Take upwards as positive: a = (R − mg) ÷ m.")],
           working=[r"R - mg = ma", rf"{fmt(R)} - {m} \times 9.8 = {m}a", rf"a = {ltx((R - m * G) / m)}\ \text{{m/s}}^2"])
    up = a > 0
    ex.choice("Which motion of the lift could give this reading?",
              "Accelerating upwards (or slowing down while moving down)." if up else "Accelerating downwards (or slowing down while moving up).",
              [("Accelerating downwards (or slowing down while moving up)." if up else "Accelerating upwards (or slowing down while moving down).",
                "The reading is " + ("greater" if up else "less") + " than mg."),
               ("Moving at constant speed.", "At constant speed the reading equals mg.")])
    return ex.build(f"A pupil of mass {m} kg stands on scales in a lift.")


gen_effective_weight_exam = exam_style(_ew_lift, _ew_find_a)


# ════════════════ Gravitation ════════════════

def _grav_satellite(level="Higher"):
    ex = _ex("Gravitation", level, UNIT2)
    m, h_km = pick(500, 750, 1200, 2500), pick(400, 600, 800, 20000)
    r = R_EARTH + h_km * 1000
    ex.num("Calculate the distance between the centre of the Earth and the satellite.", r, "m",
           wrong=[(h_km * 1000, "Add the Earth's radius: r is measured centre to centre."), (R_EARTH + h_km, "Convert km to m.")],
           working=[rf"r = 6.4 \times 10^6 + {h_km} \times 10^3 = {ltx(r)}\ \text{{m}}"])
    F = G_N * M_EARTH * m / sig(r) ** 2
    ex.num("Calculate the gravitational force between the Earth and the satellite.", F, "N",
           wrong=[(G_N * M_EARTH * m / (h_km * 1000) ** 2, "r is from the Earth's CENTRE (radius + height)."),
                  (G_N * M_EARTH * m / sig(r), "Square the distance: F = Gm₁m₂ ÷ r².")],
           working=[r"F = \frac{Gm_1m_2}{r^2}", rf"F = \frac{{6.67\times10^{{-11}} \times 6.0\times10^{{24}} \times {m}}}{{({ltx(r)})^2}}", rf"F = {ltx(F)}\ \text{{N}}"])
    ex.choice("The satellite is moved to an orbit where its distance from the Earth's centre is doubled. What happens to the gravitational force?",
              "It becomes a quarter of its original value.",
              [("It halves.", "F ∝ 1/r²: doubling r divides F by 4."), ("It stays the same.", "F depends on r."), ("It doubles.", "F decreases as r increases.")])
    return ex.build(f"A satellite of mass {m} kg orbits {h_km} km above the Earth's surface. "
                    f"(Mass of Earth = 6.0 × 10²⁴ kg; radius of Earth = 6.4 × 10⁶ m)")


def _grav_moon(level="Higher"):
    ex = _ex("Gravitation", level, UNIT2)
    m_moon, d = 7.3e22, 3.84e8
    F = G_N * M_EARTH * m_moon / d ** 2
    ex.num("Calculate the gravitational force between the Earth and the Moon.", F, "N",
           wrong=[(G_N * M_EARTH * m_moon / d, "Square the distance."), (M_EARTH * m_moon / d ** 2, "Include G.")],
           working=[rf"F = \frac{{6.67\times10^{{-11}} \times 6.0\times10^{{24}} \times 7.3\times10^{{22}}}}{{(3.84\times10^8)^2}} = {ltx(F)}\ \text{{N}}"])
    m1, m2, r = pick(60, 70, 80), pick(55, 65, 75), pick(0.5, 1.0, 2.0)
    F2 = G_N * m1 * m2 / r ** 2
    ex.num(f"Two pupils of mass {m1} kg and {m2} kg stand {r:g} m apart. Calculate the gravitational force between them.", F2, "N",
           wrong=[(G_N * m1 * m2 / r, "Square the distance."), (m1 * m2 / r ** 2, "Include G = 6.67 × 10⁻¹¹.")],
           working=[rf"F = \frac{{6.67\times10^{{-11}} \times {m1} \times {m2}}}{{{r:g}^2}} = {ltx(F2)}\ \text{{N}}"])
    ex.choice("Why don't the pupils notice the force between them?", "G is very small, so the force between everyday masses is tiny.",
              [("Gravity only acts between planets.", "Gravity acts between ALL masses."), ("The force is cancelled by air resistance.", "Air resistance isn't involved."),
               ("The pupils are too far apart for gravity to act.", "Gravity has infinite range — it's just very weak here.")])
    return ex.build("Gravitational forces act between all masses. (Mass of Earth = 6.0 × 10²⁴ kg, mass of Moon = 7.3 × 10²² kg, "
                    "Earth–Moon distance = 3.84 × 10⁸ m)")


gen_gravitation_exam = exam_style(_grav_satellite, _grav_moon)


# ════════════════ Special Relativity ════════════════

def _sr_muon(level="Higher"):
    ex = _ex("Special Relativity", level, UNIT2)
    frac = pick(0.95, 0.98, 0.99, 0.995)
    t0 = 2.2e-6
    gamma = 1 / math.sqrt(1 - frac ** 2)
    t = t0 * gamma
    ex.num("Calculate the mean lifetime of the muons as measured by an observer on Earth.", t, "s",
           wrong=[(t0 * math.sqrt(1 - frac ** 2), "Time DILATES for a moving clock: divide by √(1 − v²/c²)."),
                  (t0 / (1 - frac ** 2), "Take the square root of (1 − v²/c²).")],
           working=[r"t' = \frac{t}{\sqrt{1 - \frac{v^2}{c^2}}}", rf"t' = \frac{{2.2\times10^{{-6}}}}{{\sqrt{{1 - {frac:g}^2}}}} = {ltx(t)}\ \text{{s}}"])
    d = frac * C * sig(t)
    ex.num("Calculate the mean distance travelled by a muon in the Earth's frame of reference.", d, "m",
           wrong=[(frac * C * t0, "In the Earth frame, use the DILATED lifetime."), (C * sig(t), f"The muons travel at {frac:g}c.")],
           working=[rf"d = vt' = {frac:g} \times 3.00\times10^8 \times {ltx(t)} = {ltx(d)}\ \text{{m}}"])
    ex.choice("Why do far more muons reach the Earth's surface than expected without relativity?",
              "In the Earth's frame the muons' lifetime is dilated, so they travel further before decaying.",
              [("The muons travel faster than the speed of light.", "Nothing with mass can reach c."),
               ("The atmosphere speeds the muons up.", "It's the time dilation of their lifetime."),
               ("The muons' lifetime is shorter in the Earth's frame.", "Their lifetime is LONGER in the Earth's frame.")])
    return ex.build(f"Muons are created in the upper atmosphere and travel towards the Earth at {frac:g}c. "
                    f"In their own frame of reference they have a mean lifetime of 2.2 × 10⁻⁶ s.")


def _sr_ship(level="Higher"):
    ex = _ex("Special Relativity", level, UNIT2)
    frac, L0 = pick(0.6, 0.75, 0.8, 0.9), pick(80, 120, 150, 200)
    k = math.sqrt(1 - frac ** 2)
    L = L0 * k
    ex.num("Calculate the length of the spaceship as measured by an observer on a space station it passes.", L, "m",
           wrong=[(L0 / k, "Moving objects CONTRACT: l' = l√(1 − v²/c²)."), (L0 * (1 - frac ** 2), "Take the square root.")],
           working=[r"l' = l\sqrt{1 - \frac{v^2}{c^2}}", rf"l' = {L0}\sqrt{{1 - {frac:g}^2}} = {ltx(L)}\ \text{{m}}"])
    t_crew = pick(30, 60, 120)
    t_obs = t_crew / k
    ex.num(f"A clock on board measures {t_crew} s between two events on the ship. Calculate the time between these events measured on the space station.",
           t_obs, "s",
           wrong=[(t_crew * k, "The station observer measures a LONGER time (time dilation).")],
           working=[rf"t' = \frac{{t}}{{\sqrt{{1 - v^2/c^2}}}} = \frac{{{t_crew}}}{{{k:.3g}}} = {ltx(t_obs)}\ \text{{s}}"])
    ex.choice("The crew shine a beam of light forwards. What speed do observers on the space station measure for the light?",
              "3.00 × 10⁸ m/s — the speed of light is the same for all observers.",
              [(f"{1 + frac:g}c — the ship's speed adds to the light's.", "The speed of light is the same in all frames."),
               (f"{1 - frac:g}c — the light moves away from the ship at c.", "Every observer measures c."),
               ("It depends on the wavelength of the light.", "All light travels at c in a vacuum.")])
    return ex.build(f"A spaceship of length {L0} m (measured by its crew) travels past a space station at {frac:g}c.")


gen_relativity_exam = exam_style(_sr_muon, _sr_ship)


# ════════════════ The Expanding Universe ════════════════

def _eu_galaxy(level="Higher"):
    ex = _ex("The Expanding Universe", level, UNIT2)
    lam_r = pick(656, 486, 434)
    z = pick(0.010, 0.015, 0.020, 0.025, 0.030)
    lam_o = round(lam_r * (1 + z), 1)
    zc = (lam_o - lam_r) / lam_r
    ex.num(f"A hydrogen line of wavelength {lam_r} nm in the laboratory is observed at {lam_o:g} nm in the galaxy's spectrum. Calculate the redshift.",
           zc, "", wrong=[((lam_o - lam_r) / lam_o, "Divide by the REST (emitted) wavelength."), (lam_o / lam_r, "z = (λ_obs − λ_rest) ÷ λ_rest.")],
           working=[rf"z = \frac{{\lambda_{{obs}} - \lambda_{{rest}}}}{{\lambda_{{rest}}}} = \frac{{{lam_o:g} - {lam_r}}}{{{lam_r}}} = {ltx(zc)}"])
    v = sig(zc) * C
    ex.num("Calculate the recessional velocity of the galaxy.", v, "m/s",
           wrong=[(sig(zc) / C, "v = z × c.")], working=[rf"v = zc = {ltx(zc)} \times 3.00\times10^8 = {ltx(v)}\ \text{{m/s}}"])
    d = sig(v) / H0
    ex.num("Calculate the distance to the galaxy.", d, "m",
           wrong=[(sig(v) * H0, "d = v ÷ H₀."), (sig(v) / 1000 / H0, "Use v in m/s.")],
           working=[r"v = H_0d", rf"d = \frac{{{ltx(v)}}}{{2.3\times10^{{-18}}}} = {ltx(d)}\ \text{{m}}"])
    ex.choice("What does the redshift of distant galaxies show?", "The galaxies are moving away from us — the Universe is expanding.",
              [("The galaxies are made of red stars.", "Redshift is a shift in wavelength due to motion."),
               ("The galaxies are moving towards us.", "That would be a blueshift."),
               ("The light has slowed down on its way to Earth.", "Light travels at c; its wavelength is stretched.")])
    return ex.build("Light from a distant galaxy is analysed with a spectroscope. (H₀ = 2.3 × 10⁻¹⁸ s⁻¹)")


def _eu_siren(level="Higher"):
    ex = _ex("The Expanding Universe", level, UNIT2)
    fs, vs = pick(500, 640, 800, 960), pick(15, 20, 25, 30)
    fa = fs * 340 / (340 - vs)
    ex.num("Calculate the frequency heard by the pedestrian as the ambulance approaches.", fa, "Hz",
           wrong=[(fs * 340 / (340 + vs), "Approaching → HIGHER frequency: use v − v_s."), (fs * (340 - vs) / 340, "f_o = f_s × v ÷ (v − v_s).")],
           working=[r"f_o = f_s\left(\frac{v}{v - v_s}\right)", rf"f_o = {fs}\left(\frac{{340}}{{340 - {vs}}}\right) = {ltx(fa)}\ \text{{Hz}}"])
    fr = fs * 340 / (340 + vs)
    ex.num("Calculate the frequency heard as the ambulance moves away.", fr, "Hz",
           wrong=[(fa, "Moving away → LOWER frequency: use v + v_s.")],
           working=[rf"f_o = {fs}\left(\frac{{340}}{{340 + {vs}}}\right) = {ltx(fr)}\ \text{{Hz}}"])
    ex.choice("Explain why the frequency heard is higher as the ambulance approaches.",
              "The source moves towards the listener, so the wavefronts are squashed together: a shorter wavelength reaches the listener, giving a higher frequency.",
              [("The sound travels faster when the ambulance approaches.", "The speed of sound in air doesn't change."),
               ("The siren emits a higher frequency when moving.", "The emitted frequency is constant."),
               ("The wavelength increases as the source approaches.", "The wavelength DEcreases.")])
    return ex.build(f"An ambulance with a siren of frequency {fs} Hz travels at {vs} m/s past a pedestrian. Speed of sound = 340 m/s.")


def _eu_age(level="Higher"):
    ex = _ex("The Expanding Universe", level, UNIT2)
    t = 1 / H0
    ex.num("Using H₀ = 2.3 × 10⁻¹⁸ s⁻¹, estimate the age of the Universe in seconds.", t, "s",
           wrong=[(H0, "Age ≈ 1 ÷ H₀.")], working=[rf"t = \frac{{1}}{{H_0}} = \frac{{1}}{{2.3\times10^{{-18}}}} = {ltx(t)}\ \text{{s}}"])
    ex.num("Convert this age to years.", sig(t) / YEAR, "",
           wrong=[(sig(t) / (24 * 3600), "Divide by the number of seconds in a YEAR (365 × 24 × 3600).")],
           working=[rf"\frac{{{ltx(t)}}}{{365 \times 24 \times 3600}} = {ltx(sig(t) / YEAR)}\ \text{{years}}"])
    ex.choice("Measurements of the rotation of galaxies suggest there is more mass than can be seen. What is this called?", "Dark matter",
              [("Dark energy", "Dark energy explains the ACCELERATING expansion."), ("Black body radiation", "That's thermal emission from hot objects."),
               ("Redshift", "Redshift is evidence for expansion.")])
    return ex.build("Hubble's law can be used to estimate the age of the Universe.")


gen_expanding_universe_exam = exam_style(_eu_galaxy, _eu_siren, _eu_age)


EXAM_PART1 = {
    "Equations of Motion":    gen_eom_exam,
    "Graphs of Motion":       gen_gom_exam,
    "Towing":                 exam_style(reuse(gen_towing_exam_style, qtype="Towing")),
    "Components of Vectors":  gen_components_exam,
    "Momentum and Impulse":   gen_momentum_exam,
    "Energy, Work and Power": gen_ewp_exam,
    "Effective Weight":       gen_effective_weight_exam,
}

EXAM_PART2 = {
    "Projectile Motion":      exam_style(reuse(generate_projectile_exam_mixed, qtype="Projectile Motion")),
    "Gravitation":            gen_gravitation_exam,
    "Special Relativity":     gen_relativity_exam,
    "The Expanding Universe": gen_expanding_universe_exam,
}

EXAM = {**EXAM_PART1, **EXAM_PART2}
