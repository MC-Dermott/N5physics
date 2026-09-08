# Worked examples shown to students before they practise each question type.
#
# Key:   (topic, question_type)                — applies to every sub-type/level
#        (topic, question_type, sub_type)       — applies to one specific sub-type/level
# Value: markdown string (rendered with st.markdown, supports $...$ / $$...$$ LaTeX)
#
# A (topic, question_type, sub_type) key takes priority over the plain
# (topic, question_type) key when both exist.
#
# Question types with no hand-authored entry here fall back to derive_example()
# below, which generates one automatically from the generator itself.

import random

EXAMPLES = {
    ("Our Dynamic Universe", "Towing", "Level 1 — One Trailer, No Friction"): r"""
**Example:** A 1000 kg car tows a single 250 kg trailer with a driving force of 2500 N and no friction.

*(a) Calculate the acceleration.*
$$a = \frac{F}{m_c + m_t} = \frac{2500}{1000 + 250} = 2\ \mathrm{m/s^2}$$

*(b) Calculate the tension in the tow bar.*

Considering the trailer alone (the only force on it is the tension):
$$T = m_t \times a = 250 \times 2 = 500\ \mathrm{N}$$
""",

    ("Our Dynamic Universe", "Towing", "Level 2 — One Trailer, With Friction"): r"""
**Example:** A 1000 kg car tows a 250 kg trailer with a driving force of 3000 N. Friction acts
on the car with 200 N and on the trailer with 100 N.

*(a) Calculate the acceleration.*
$$a = \frac{F - f_c - f_t}{m_c + m_t} = \frac{3000 - 200 - 100}{1250} = 2.16\ \mathrm{m/s^2}$$

*(b) Calculate the tension in the tow bar.*

Considering the trailer alone (tension forward, friction backward):
$$T = (m_t \times a) + f_t = (250 \times 2.16) + 100 = 640\ \mathrm{N}$$
""",

    ("Our Dynamic Universe", "Towing", "Level 3 — Multiple Trailers, No Friction"): r"""
**Example:** A 1000 kg car tows trailer 1 (300 kg) and trailer 2 (200 kg) with a driving force
of 3000 N and no friction.

*(a) Calculate the acceleration of the whole collection (car + both trailers).*
$$a = \frac{F}{m_c + m_{t1} + m_{t2}} = \frac{3000}{1500} = 2\ \mathrm{m/s^2}$$

*(b) Calculate the tension in the tow bar connecting the car to the trailers.*

Treat the towed vehicles (trailer 1 + trailer 2) as a single group — the tow bar must pull
**both** of them:
$$T = (m_{t1} + m_{t2}) \times a = (300 + 200) \times 2 = 1000\ \mathrm{N}$$
""",

    ("Our Dynamic Universe", "Towing", "Level 4 — Multiple Trailers, With Friction"): r"""
**Example:** A 1000 kg car tows trailer 1 (300 kg) and trailer 2 (200 kg) with a driving force
of 4000 N. Friction: 200 N on the car, 100 N on trailer 1, 50 N on trailer 2.

*(a) Calculate the acceleration of the whole collection (car + both trailers).*
$$a = \frac{F - f_c - f_{t1} - f_{t2}}{m_c + m_{t1} + m_{t2}} = \frac{4000 - 200 - 100 - 50}{1500} = 2.43\ \mathrm{m/s^2}$$

*(b) Calculate the tension in the tow bar connecting the car to the trailers.*

Treat the towed vehicles (trailer 1 + trailer 2) as a single group, opposed by both their
friction forces:
$$T = ((m_{t1} + m_{t2}) \times a) + f_{t1} + f_{t2} = (500 \times 2.43) + 100 + 50 = 1365\ \mathrm{N}$$
""",

    ("Our Dynamic Universe", "Towing", "Level 5 — Exam Style"): r"""
**Example:** A bike tows a trailer. Parts (a) and (b) ask you to calculate the acceleration and
the tension in the tow bar, exactly as in the earlier levels.

**Part (c):** As the speed of the bike and trailer increases, the friction forces on both the
bike and the trailer increase. The acceleration remains 0.58 m/s². Which statement correctly
describes what happens to the tension in the tow bar, and why?

- Decreases — the extra friction on the trailer means less tension is needed to keep it moving.
- Stays the same — since the acceleration doesn't change, none of the individual forces need to change either.
- Increases — because the driving force from the bike's engine must increase to maintain the same acceleration.
- **Increases — considering the trailer alone, T − F_friction = m × a. Since the acceleration stays constant, the extra friction must be balanced by extra tension.** ✓

The correct option is the last one: friction opposes the tension, so for the equation
$T - F_{\text{friction}} = m \times a$ to keep balancing with a fixed right-hand side, T must
rise to match the extra friction. (The third option is a common trap — it's true of the
*driving force*, but the question asks specifically about the *tow bar tension*.)
""",

    ("Dynamics", "Acceleration", "Change in Speed"): r"""
**Example:** A car has an acceleration of −4 m/s² for 6 s.

*Calculate the change in speed.*

Rearrange $a = \dfrac{v - u}{t}$ for the change in speed, $v - u$:
$$v - u = at$$
$$v - u = (-4) \times 6 = -24\ \mathrm{m/s}$$

The change in speed is **−24 m/s** — the negative sign shows the acceleration is a
deceleration, so the car's speed decreases by 24 m/s.
""",

    ("Dynamics", "Acceleration", "Initial & Final Speed"): r"""
**Example:** A cyclist starts with a speed of 3 m/s and has an acceleration of 2 m/s² for 5 s.

*Calculate the final speed.*

$$v = u + at$$
$$v = 3 + (2 \times 5) = 13\ \mathrm{m/s}$$

**Example (finding the initial speed):** A runner has an acceleration of −1 m/s² for 4 s and
reaches a final speed of 4 m/s.

*Calculate the initial speed.*

Rearrange $v = u + at$ for $u$:
$$u = v - at$$
$$u = 4 - (-1 \times 4) = 8\ \mathrm{m/s}$$
""",

    ("Dynamics", "Distance and Displacement", "Level 1 — 1D"): r"""
**Example:** A cyclist travels 15 m east, then 22 m west, then 8 m east.

*(a) Calculate the total distance travelled.*

Distance adds up the magnitude of every leg, regardless of direction:
$$d = 15 + 22 + 8 = 45\ \mathrm{m}$$

*(b) Taking east as positive, calculate the resultant displacement.*

Displacement adds the **signed** values, so legs in opposite directions partly cancel:
$$s = (+15) + (-22) + (+8) = +1\ \mathrm{m}$$

The resultant displacement is **1 m east**.
""",

    ("Dynamics", "Distance and Displacement", "Level 2 — Two Displacements (2D)"): r"""
**Example:** A boat travels 8 km north and 6 km east.

*Calculate the magnitude and bearing of the resultant displacement.*

**Magnitude** — combine the two perpendicular legs with Pythagoras:
$$R = \sqrt{8^2 + 6^2} = \sqrt{100} = 10\ \mathrm{km}$$

**Bearing** — find the angle east of north, then apply the quadrant rule:
$$\theta = \tan^{-1}\left(\frac{6}{8}\right) = 36.9°$$

Both legs are positive (north and east), so the resultant lies in the NE quadrant, where bearing $= \theta$:
$$\text{Bearing} = 037°$$
""",

    ("Dynamics", "Vectors and Scalars", "Identify Scalar or Vector"): r"""
**Example:** Which of the following is a vector quantity — mass, energy, or acceleration?

A scalar quantity has magnitude only. A vector quantity has magnitude **and** direction.

- Mass has a size (e.g. 5 kg) but no direction → **scalar**
- Energy has a size (e.g. 200 J) but no direction → **scalar**
- Acceleration has a size (e.g. 3 m/s²) **and** a direction (e.g. downwards) → **vector**

The answer is **acceleration**.
""",

    ("Dynamics", "Vectors and Scalars", "Scalar & Vector Pairs"): r"""
**Example:** Which of the following contains one scalar quantity and one vector quantity?

| Option | Pair | Both same type? |
|---|---|---|
| A | acceleration; displacement | Both vectors ✗ |
| B | kinetic energy; speed | Both scalars ✗ |
| C | velocity; weight | Both vectors ✗ |
| D | potential energy; work done | Both scalars ✗ |
| E | distance; force | Distance is a scalar, force is a vector ✓ |

The answer is **E — distance; force**, since it is the only option with one of each type.
""",

    ("Dynamics", "Distance and Displacement", "Level 3 — Multiple Displacements (2D)"): r"""
**Example:** A hiker walks 12 km north, then 9 km east, then 4 km south.

*Calculate the magnitude and bearing of the resultant displacement from the start.*

**Step 1 — resolve onto the N/E axes and sum each axis separately:**
$$\Sigma N = 12 - 4 = 8\ \mathrm{km} \qquad \Sigma E = 9\ \mathrm{km}$$

**Step 2 — magnitude** (Pythagoras):
$$R = \sqrt{(\Sigma N)^2 + (\Sigma E)^2} = \sqrt{8^2 + 9^2} = \sqrt{145} = 12.04\ \mathrm{km}$$

**Step 3 — bearing:**
$$\theta = \tan^{-1}\left(\frac{9}{8}\right) = 48.4°$$

$\Sigma N$ and $\Sigma E$ are both positive, so the resultant lies in the NE quadrant, where bearing $= \theta$:
$$\text{Bearing} = 048°$$
""",

    ("Dynamics", "Speed and Velocity", "From a Compound Displacement"): r"""
**Example:** A hiker walks 400 m north, then 300 m east, taking 50 s.

*Calculate the hiker's average speed and average velocity.*

$$\text{speed} = \frac{\text{distance}}{\text{time}} \qquad \text{velocity} = \frac{\text{displacement}}{\text{time}}$$

Total distance = 400 + 300 = 700 m, so speed = 700 ÷ 50 = **14 m/s**

Resultant displacement (Pythagoras) = $\sqrt{400^2 + 300^2}$ = 500 m, so velocity = 500 ÷ 50 = **10 m/s**

**Common exam trap:** speed is always greater than (or equal to) the magnitude of velocity for
the same journey, since the straight-line displacement can never be longer than the path
actually walked.
""",

    ("Dynamics", "Speed and Velocity", "Resultant Velocity"): r"""
**Example (same line):** A train travels at 25 m/s. A passenger walks towards the front of the
train at 1.5 m/s.

Both velocities act along the same line, so add them:
$$\text{resultant velocity} = 25 + 1.5 = 26.5\ \mathrm{m/s}$$

**Example (at an angle):** A boat's engine gives it 3.0 m/s directly across a river. The current
flows at 4.0 m/s along the river.

The two velocities are perpendicular, so combine with Pythagoras and trigonometry:
$$v = \sqrt{3.0^2 + 4.0^2} = 5.0\ \mathrm{m/s}, \quad \theta = \tan^{-1}\left(\frac{4.0}{3.0}\right) = 53.1°\ \text{from straight across}$$

**Common exam trap:** if the two velocities act in *opposite* directions along the same line,
subtract them rather than adding.
""",

    ("Dynamics", "Velocity-Time Graphs"): r"""
**Example (distance & displacement):** A car accelerates from rest to 8 m/s over 4 s, then
brakes and reverses, reaching −4 m/s after a further 4 s.

- Stage 1 (triangle) = ½ × 4 × 8 = 16 m
- Stage 2 crosses zero at t = 6.67 s: forward part ≈ ½ × 2.67 × 8 = 10.7 m; reverse part ≈
  ½ × 1.33 × 4 = 2.7 m
- Distance ≈ 16 + 10.7 + 2.7 = **29.3 m**          Displacement ≈ 16 + 10.7 − 2.7 = **24.0 m**

**Example (acceleration over an interval):** A graph shows a vehicle's velocity rising steadily
from 0 to 20 m/s over the first 10 s. Between t = 2 s and t = 8 s: at t = 2 s, v = 4 m/s; at
t = 8 s, v = 16 m/s.

The gradient of a v-t graph gives the acceleration, using any two points on the same
straight-line section:
$$a = \frac{16 - 4}{8 - 2} = 2\ \mathrm{m/s^2}$$

**Common exam trap:** distance is the *area*, not a single velocity value read off the graph —
always check whether the shape under the line is a rectangle, triangle, or trapezium, and
whether any part of it lies below the time axis.
""",

    ("Our Dynamic Universe", "Equations of Motion", "Horizontal Motion"): r"""
**Example:** A car travelling at 10 m/s accelerates uniformly at 2 m/s² for 5 s.

*Calculate its final velocity.*
$$v = u + at = 10 + (2 \times 5) = 20\ \mathrm{m/s}$$
""",

    ("Our Dynamic Universe", "Equations of Motion", "Vertical Motion"): r"""
**Example:** A stone is dropped from rest from a bridge and takes 3.0 s to reach the water.

*Calculate the height of the bridge above the water.*

An object dropped from rest has u = 0 and accelerates at g = 9.8 m/s²:
$$s = ut + \frac{1}{2}at^2 = 0 + \frac{1}{2}\times 9.8\times 3.0^2 = 44.1\ \mathrm{m}$$
""",

    ("Our Dynamic Universe", "Graphs of Motion"): r"""
**Example:** A v–t graph rises in a straight line from 0 to 8 m/s over the first 4 s, then stays
constant at 8 m/s for the next 3 s.

- Acceleration in the first 4 s = gradient = $\frac{8 - 0}{4} = 2\ \mathrm{m/s^2}$
- Displacement in the first 4 s = area under the graph (triangle) = $\frac{1}{2} \times 4 \times 8 = 16\ \mathrm{m}$
- Acceleration during the constant-speed phase = **0 m/s²** (horizontal line)

**Common exam trap:** don't assume the s–t and a–t graphs look like copies of the v–t graph.
Only the *gradient* (→ a–t) and *area* (→ s–t) relationships matter — always check whether the
shape should be straight or curved, and check the sign.
""",

    ("Our Dynamic Universe", "Special Relativity"): r"""
**Example:** A spacecraft moves at $v = 0.6c$. An observer on board measures a proper time of
10 s between two events.

*Calculate the dilated time measured by a stationary observer.*
$$t' = \frac{t}{\sqrt{1 - \frac{v^2}{c^2}}} = \frac{10}{\sqrt{1 - 0.6^2}} = \frac{10}{0.8} = 12.5\ \mathrm{s}$$

**Important:** t' > t (stationary observer measures a longer time), and l' < l (stationary
observer measures a shorter length) — both formulae use the same factor √(1 − v²/c²).
""",

    ("Our Dynamic Universe", "Gravitation"): r"""
**Example:** Calculate the gravitational field strength at the surface of a planet with mass
$M = 5.97 \times 10^{24}$ kg and radius $R = 6.37 \times 10^{6}$ m.
$$g = \frac{GM}{r^2} = \frac{6.674 \times 10^{-11} \times 5.97 \times 10^{24}}{(6.37 \times 10^{6})^2} = 9.8\ \mathrm{N/kg}$$

**Important:** r is measured from the **centre of the planet** ($r = R + h$), not the orbital
height — always convert distances to metres before substituting.
""",

    ("Our Dynamic Universe", "Momentum and Impulse"): r"""
**Example (collision, objects separate):** A trolley of mass 0.50 kg moving at 1.5 m/s (right,
positive) collides with a trolley of mass 0.30 kg moving at 1.0 m/s to the left. After the
collision the first trolley rebounds at 0.30 m/s to the left.

*Calculate the velocity of the second trolley.*
$$m_1u_1 + m_2u_2 = m_1v_1 + m_2v_2$$
$$(0.50 \times 1.5) + (0.30 \times -1.0) = (0.50 \times -0.30) + (0.30 \times v_2)$$
$$0.75 - 0.30 = -0.15 + 0.30v_2 \implies v_2 = 2.0\ \mathrm{m/s}$$

**Important:** total momentum before a collision or explosion always equals total momentum
after, provided no external forces act. Always state which direction is positive before
substituting — a velocity in the opposite direction must be entered as negative.
""",

    ("Our Dynamic Universe", "Energy, Work and Power"): r"""
**Example (conservation of energy):** A skateboarder of mass 55 kg starts from rest at the top
of a ramp of height 2.0 m. She reaches 5.5 m/s at the bottom, having travelled 8.0 m along the
ramp.

*Calculate the average frictional force acting on her.*
$$E_p = mgh = 55 \times 9.8 \times 2.0 = 1078\ \mathrm{J} \qquad E_k = \tfrac{1}{2}mv^2 = \tfrac{1}{2} \times 55 \times 5.5^2 = 832\ \mathrm{J}$$
$$\text{energy lost} = 1078 - 832 = 246\ \mathrm{J} \qquad E_W = Fd \implies 246 = F \times 8.0 \implies F = 31\ \mathrm{N}$$

**Important:** any energy that "goes missing" between two points has been lost, usually to
friction, and that lost energy equals the work done against the resistive force.
""",

    ("Our Dynamic Universe", "Effective Weight"): r"""
**Example:** A person of mass 70 kg stands on bathroom scales inside a lift. The lift is moving
upwards but slowing down at a rate of 1.5 m/s².

*Calculate the reading R on the scales.*

The lift moves upwards but is slowing down, so its acceleration acts downwards — the reading R
is less than the weight W:
$$mg - R = ma$$
$$(70 \times 9.8) - R = 70 \times 1.5$$
$$R = 686 - 105 = 581\ \mathrm{N}$$

**Important:** the same physics applies beyond lifts — a crane cable's tension, a rocket's
thrust, or the force a drone's platform exerts on a parcel all follow the same F = ma / W = mg
reasoning. In true free fall, the only force acting is gravity, so a supporting force reads 0 N.
""",

    ("Our Dynamic Universe", "Components of Vectors"): r"""
**Example:** A force of 50 N acts at 40° above the horizontal.

*Resolve it into horizontal and vertical components.*
$$F_x = 50\cos40° = 38.3\ \mathrm{N} \qquad F_y = 50\sin40° = 32.1\ \mathrm{N}$$

**Important:** always check which angle is given — the angle to the horizontal, or the angle to
the slope/vertical — since this decides whether a component uses sin or cos.
""",

    ("Our Dynamic Universe", "Projectile Motion", "Level 1 — Same Height"): r"""
**Example:** An object is launched at 20 m/s at 30° above the horizontal on flat ground.

*Calculate the range.*
$$v_H = 20\cos30° = 17.3\ \mathrm{m/s} \qquad v_V = 20\sin30° = 10\ \mathrm{m/s}$$
$$t_{\text{up}} = \frac{v_V}{g} = \frac{10}{9.8} = 1.02\ \mathrm{s} \quad\Rightarrow\quad t_{\text{total}} = 2.04\ \mathrm{s}$$
$$R = v_H \times t_{\text{total}} = 17.3 \times 2.04 = 35.3\ \mathrm{m}$$

**Most common mistake:** using $t_{\text{up}}$ (time to reach the top) instead of
$t_{\text{total}} = 2t_{\text{up}}$ when calculating the range.
""",

    ("Our Dynamic Universe", "Projectile Motion", "Level 3 — Exam Style"): r"""
**Example:** An object is launched at 20 m/s at 30° above the horizontal on flat ground.

*Calculate the range.*
$$v_H = 20\cos30° = 17.3\ \mathrm{m/s} \qquad v_V = 20\sin30° = 10\ \mathrm{m/s}$$
$$t_{\text{up}} = \frac{v_V}{g} = \frac{10}{9.8} = 1.02\ \mathrm{s} \quad\Rightarrow\quad t_{\text{total}} = 2.04\ \mathrm{s}$$
$$R = v_H \times t_{\text{total}} = 17.3 \times 2.04 = 35.3\ \mathrm{m}$$

**Most common mistake:** using $t_{\text{up}}$ (time to reach the top) instead of
$t_{\text{total}} = 2t_{\text{up}}$ when calculating the range.
""",

    ("Our Dynamic Universe", "Projectile Motion", "Level 2 — Different Height"): r"""
**Example:** An object is launched horizontally at 15 m/s from a height of 20 m.

*Calculate the resultant speed at impact.*
$$t = \sqrt{\frac{2h}{g}} = \sqrt{\frac{2 \times 20}{9.8}} = 2.02\ \mathrm{s}$$
$$v_y = gt = 9.8 \times 2.02 = 19.8\ \mathrm{m/s}$$
$$v = \sqrt{v_H^2 + v_y^2} = \sqrt{15^2 + 19.8^2} = 24.8\ \mathrm{m/s}$$

**Common mistake:** using $h = gt^2$ (forgetting the $\frac{1}{2}$) gives a time too small by a
factor of $\sqrt{2}$.
""",

    ("Our Dynamic Universe", "Projectile Motion", "Time to Maximum Height"): r"""
**Example:** An object is launched at 20 m/s at 30° above the horizontal.

*Calculate the time and height at which it reaches its maximum height.*
$$v_V = 20\sin30° = 10\ \mathrm{m/s}$$
$$t_{\text{up}} = \frac{v_V}{g} = \frac{10}{9.8} = 1.02\ \mathrm{s}$$
$$h_{\text{max}} = \frac{v_V^2}{2g} = \frac{10^2}{19.6} = 5.1\ \mathrm{m}$$

**Most common mistake:** using the full initial speed v instead of its vertical component
$v_V$, or forgetting the factor of 2 in the denominator of $h_{\text{max}} = v_V^2 \div 2g$.
""",

    ("Particles and Waves", "Standard Model", "Particle Classification"): r"""
**Example:** Classify the electron.

It has half-integer spin, so it is a **fermion**. It does not feel the strong force and is not
made of quarks, so it is a **lepton** (not a hadron).

The electron is a **fermion and lepton**.
""",

    ("Particles and Waves", "Standard Model", "Order of Magnitude"): r"""
**Example:** The muon has a mass of $1.88 \times 10^{-28}$ kg (order of magnitude −28) and the
neutron has a mass of $1.67 \times 10^{-27}$ kg (order of magnitude −27).

*Find the difference in order of magnitude.*
$$|-27 - (-28)| = 1$$
""",

    ("Electricity and Energy", "Electrical Power"): r"""
**Example:** A 500 W appliance runs for 120 s.

*Calculate the energy transferred.*
$$E = P \times t = 500 \times 120 = 60\,000\ \mathrm{J}$$
""",

    ("Electricity and Energy", "Efficiency"): r"""
**Example:** A kettle is supplied with 400 000 J and heats the water with 160 000 J.

*Calculate the efficiency.*
$$\text{Efficiency} = \frac{160\,000}{400\,000} \times 100\% = 40\%$$
""",

    ("Electricity and Energy", "Power and Efficiency"): r"""
**Example:** A 2000 W heater runs for 300 s, supplying 480 000 J of useful heat.

*Calculate the input energy and the efficiency.*
$$E = P \times t = 2000 \times 300 = 600\,000\ \mathrm{J}$$
$$\text{Efficiency} = \frac{480\,000}{600\,000} \times 100\% = 80\%$$
""",

    ("Electricity and Energy", "Renewable Energy"): r"""
**Example:** Is coal renewable or non-renewable?

Coal is burned as a fuel and cannot be replaced once used up, so **coal is non-renewable**.
""",

    ("Electricity and Energy", "Input/Output Devices"): r"""
**Example:** Is an LDR (light dependent resistor) a digital or analogue input device?

An LDR's resistance changes smoothly over a continuous range of light levels, so **an LDR is
an analogue input device**.
""",

    ("Electricity and Energy", "Electromagnets"): r"""
**Example:** Why is an electromagnet used in a scrapyard crane rather than a permanent magnet?

Because an electromagnet **can be switched off** to release the lifted scrap metal — a
permanent magnet cannot be turned off.
""",
}


def get_examples(topic, question_type, sub_type=None):
    if sub_type is not None:
        example = EXAMPLES.get((topic, question_type, sub_type))
        if example is not None:
            return example
    return EXAMPLES.get((topic, question_type))


def _format_working(working):
    lines = []
    for step in working:
        if step.get("type") == "latex":
            lines.append(f"$${step['content']}$$")
        else:
            lines.append(step["content"])
    return "\n\n".join(lines)


def _format_example_question(q, heading):
    if q.metadata.get("type") == "explain":
        body = q.metadata.get("explain_text", "")
    else:
        body = _format_working(q.working)
        answer = f"{q.correct_answer} {q.unit}".strip()
        if body:
            body += f"\n\n**Answer:** {answer}"
        else:
            body = f"**Answer:** {answer}"
    parts = [f"**{heading}:** {q.question_text}"]
    if body:
        parts.append(body)
    return "\n\n".join(parts)


def derive_example(generate_fn, seed=42):
    """
    Fallback for question types with no hand-authored EXAMPLES entry: runs
    generate_fn with a fixed seed so the same canonical instance is produced
    every time, then formats its own question text + working (equation ->
    substitution -> answer) as a worked example — the same steps normally
    shown in the "Worked Solution" expander after answering.
    """
    state = random.getstate()
    try:
        random.seed(seed)
        q = generate_fn()
    finally:
        random.setstate(state)

    if not q.is_scenario:
        return _format_example_question(q, "Example")

    blocks = [q.scenario_context] if q.scenario_context else []
    blocks += [
        _format_example_question(part, f"Part {i + 1}")
        for i, part in enumerate(q.parts)
    ]
    return "\n\n---\n\n".join(blocks)
