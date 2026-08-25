# Worked examples shown to students before they practise each question type.
#
# Key:   (topic, question_type)                — applies to every sub-type/level
#        (topic, question_type, sub_type)       — applies to one specific sub-type/level
# Value: markdown string (rendered with st.markdown, supports $...$ / $$...$$ LaTeX)
#
# A (topic, question_type, sub_type) key takes priority over the plain
# (topic, question_type) key when both exist.

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
}


def get_examples(topic, question_type, sub_type=None):
    if sub_type is not None:
        example = EXAMPLES.get((topic, question_type, sub_type))
        if example is not None:
            return example
    return EXAMPLES.get((topic, question_type))
