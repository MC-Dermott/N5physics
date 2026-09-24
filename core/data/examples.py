# Worked examples shown to students before they practise each question type.
#
# Key:   (topic, question_type)                — applies to every sub-type/level
#        (topic, question_type, sub_type)       — applies to one specific sub-type/level
# Value: markdown string (rendered with st.markdown, supports $...$ / $$...$$ LaTeX)
#
# A (topic, question_type, sub_type) key takes priority over the plain
# (topic, question_type) key when both exist.
#
# Calculation-based examples follow the house style: state the equation, then
# substitute the known numbers into it, then (rearranging first if the target
# isn't already the subject) give the answer. Purely conceptual/classification
# examples (no equation to substitute into) are just explained in prose.
#
# Topics are keyed by the real SQA unit name (e.g. "Our Dynamic Universe"),
# not the app's pacing split ("Our Dynamic Universe (Part 1)"/"(Part 2)") —
# get_examples() strips that suffix via canonical_unit() before looking up.
#
# Question types with no hand-authored entry here fall back to a worked example
# generated from the generator itself — once a question has been generated, one
# of the same variant (see matching_example()), so the example always shows the
# same kind of question the student is answering.
#
# Only add a hand-authored entry when its generator always asks the same thing
# (the same unknown, the same parts) and the example shows exactly that — for a
# generator that randomises between variants (find a / find t / find Δv…), a
# single fixed example can't match every question, so leave it to the fallback.

import random
import re

from core.data.past_papers import canonical_unit

EXAMPLES = {
    ("Our Dynamic Universe", "Towing", "Level 1 — One Trailer, No Friction"): r"""
**Example:** A 1000 kg car tows a single 250 kg trailer with a driving force of 2500 N and no friction.

**(a) Calculate the acceleration.**

Apply Newton's second law to the whole system (car + trailer):

*Equation:*
$$F = ma$$

*Substitute:*
$$2500 = (1000 + 250) \times a$$

*Rearrange and solve:*
$$a = \frac{2500}{1250} = 2.0\ \mathrm{m/s^2}$$

**(b) Calculate the tension in the tow bar.**

Consider the trailer alone — the only horizontal force on it is the tension T:

*Equation:*
$$F = ma$$

*Substitute:*
$$T = 250 \times 2.0$$

*Answer:*
$$T = 500\ \mathrm{N}$$
""",

    ("Our Dynamic Universe", "Towing", "Level 2 — One Trailer, With Friction"): r"""
**Example:** A 1000 kg car tows a 250 kg trailer with a driving force of 3000 N. Friction acts
on the car with 200 N and on the trailer with 100 N.

**(a) Calculate the acceleration.**

For the whole system, the unbalanced force is the driving force minus the total friction:

$$F_{\text{unbalanced}} = 3000 - 200 - 100 = 2700\ \mathrm{N}$$

*Equation:*
$$F = ma$$

*Substitute:*
$$2700 = (1000 + 250) \times a$$

*Rearrange and solve:*
$$a = \frac{2700}{1250} = 2.16\ \mathrm{m/s^2}$$

**(b) Calculate the tension in the tow bar.**

Consider the trailer alone — tension T forward, friction backward, so the unbalanced force on it
is $T - 100$:

*Equation:*
$$F = ma$$

*Substitute:*
$$T - 100 = 250 \times 2.16$$

*Rearrange and solve:*
$$T = 540 + 100 = 640\ \mathrm{N}$$
""",

    ("Our Dynamic Universe", "Towing", "Level 3 — Multiple Trailers, No Friction"): r"""
**Example:** A 1000 kg car tows trailer 1 (300 kg) and trailer 2 (200 kg) with a driving force
of 3000 N and no friction.

**(a) Calculate the acceleration of the whole collection (car + both trailers).**

*Equation:*
$$F = ma$$

*Substitute:*
$$3000 = (1000 + 300 + 200) \times a$$

*Rearrange and solve:*
$$a = \frac{3000}{1500} = 2.0\ \mathrm{m/s^2}$$

**(b) Calculate the tension in the tow bar connecting the car to the trailers.**

Treat the towed vehicles (trailer 1 + trailer 2) as a single group — the tow bar must pull
**both** of them:

*Equation:*
$$F = ma$$

*Substitute:*
$$T = (300 + 200) \times 2.0$$

*Answer:*
$$T = 1000\ \mathrm{N}$$
""",

    ("Our Dynamic Universe", "Towing", "Level 4 — Multiple Trailers, With Friction"): r"""
**Example:** A 1000 kg car tows trailer 1 (300 kg) and trailer 2 (200 kg) with a driving force
of 4000 N. Friction: 200 N on the car, 100 N on trailer 1, 50 N on trailer 2.

**(a) Calculate the acceleration of the whole collection (car + both trailers).**

The unbalanced force is the driving force minus the total friction:

$$F_{\text{unbalanced}} = 4000 - 200 - 100 - 50 = 3650\ \mathrm{N}$$

*Equation:*
$$F = ma$$

*Substitute:*
$$3650 = (1000 + 300 + 200) \times a$$

*Rearrange and solve:*
$$a = \frac{3650}{1500} = 2.43\ \mathrm{m/s^2}$$

**(b) Calculate the tension in the tow bar connecting the car to the trailers.**

Treat the towed vehicles (trailer 1 + trailer 2) as a single group, opposed by both their
friction forces, so the unbalanced force on the group is $T - 100 - 50$:

*Equation:*
$$F = ma$$

*Substitute:*
$$T - 100 - 50 = (300 + 200) \times 2.43$$

*Rearrange and solve:*
$$T = 1215 + 150 = 1365\ \mathrm{N}$$
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

    ("Dynamics", "Velocity-Time Graphs", "Which Graph Matches?"): r"""
**Example:** A ball is dropped from rest and caught at the ground.

Four velocity-time graphs (A–D) are shown. Which one matches this description?

A ball moving freely under gravity changes direction *smoothly*, passing gradually through
v = 0. A ball that **bounces** changes direction *instantly* — the graph jumps straight from
a negative velocity to a smaller positive one, without passing through zero.

Since the ball here is simply dropped and caught (no bounce, no throw upward), its velocity
starts at 0 and increases in one direction only — the correct graph is a single straight ramp
starting from the origin, with no direction change at all.

**Common exam trap:** don't confuse this with a ball *thrown upward and caught* (a smooth,
symmetric crossing through zero) or a ball that *bounces* (a graph with a sudden jump). Match
the shape of the graph to what physically happens at each stage of the motion.
""",

    ("Our Dynamic Universe", "Graphs of Motion", "Graph Matching"): r"""
**Example:** A car accelerates uniformly from rest, reaching 15 m/s after 5 s. Its
velocity–time graph (a straight line from the origin) is shown.

Which combination of graphs (A–E) correctly shows the displacement–time and
acceleration–time graphs for this motion?

- **Acceleration–time graph:** since the v–t graph is a straight line, the acceleration is
  constant — the a–t graph must be a single **horizontal line** at
  $a = \frac{15}{5} = 3\ \mathrm{m/s^2}$, not sloped and not changing level.
- **Displacement–time graph:** since the acceleration is constant and non-zero, displacement
  builds up according to $s = ut + \tfrac{1}{2}at^2$ — the s–t graph must be a **curve** (part
  of a parabola), not a straight line copying the shape of the v–t graph.

The correct option is the one pairing a horizontal a–t line with a correctly curved s–t graph,
both with the correct sign.

**Common exam trap:** a straight-line v–t graph does *not* mean the s–t graph is also straight
— only a *constant* velocity (horizontal v–t line) gives a straight s–t graph.
""",

    ("Our Dynamic Universe", "Gravitation", "3 — g at a Height"): r"""
**Example:** A satellite of mass 1200 kg orbits the Earth at a height of 400 km above the
surface. The Earth has mass $5.97 \times 10^{24}$ kg and radius $6.37 \times 10^{6}$ m.

**(a) Calculate the gravitational force between the satellite and the Earth.**

r is measured from the **centre** of the Earth, so add the height (in metres) to the radius:

$$r = 6.37 \times 10^{6} + 4.00 \times 10^{5} = 6.77 \times 10^{6}\ \mathrm{m}$$

*Equation:*
$$F = G\frac{m_1 m_2}{r^2}$$

*Substitute:*
$$F = 6.67 \times 10^{-11} \times \frac{5.97 \times 10^{24} \times 1200}{(6.77 \times 10^{6})^2}$$

*Answer:*
$$F = 1.04 \times 10^{4}\ \mathrm{N}$$

**(b) Calculate the gravitational field strength at this height.**

The gravitational force is the satellite's weight at this height:

*Equation:*
$$W = mg$$

*Substitute:*
$$1.04 \times 10^{4} = 1200 \times g$$

*Rearrange and solve:*
$$g = 8.7\ \mathrm{N/kg}$$

**Important:** always convert the height to metres and add the planet's radius before
substituting — using the height alone for r is the most common mistake.
""",

    ("Our Dynamic Universe", "Momentum and Impulse", "Collisions — Stick Together"): r"""
**Example:** Trolley A (mass 0.50 kg), moving at 2.0 m/s, collides with trolley B (mass
0.30 kg), which is stationary. The two trolleys stick together after the collision.

*Calculate their common velocity.*

Total momentum before = total momentum after:

*Equation:*
$$m_1u_1 + m_2u_2 = (m_1 + m_2)v$$

*Substitute:*
$$(0.50 \times 2.0) + (0.30 \times 0) = (0.50 + 0.30)v$$

*Rearrange and solve:*
$$1.0 = 0.80v \implies v = 1.25\ \mathrm{m/s}$$

**Important:** after sticking together, both objects move at the *same* final velocity — use
the combined mass on the right-hand side, not the two masses separately.
""",

    ("Our Dynamic Universe", "Momentum and Impulse", "Collisions — Separate"): r"""
**Example:** A trolley of mass 0.50 kg moving at 1.5 m/s (right, positive) collides with a
trolley of mass 0.30 kg moving at 1.0 m/s to the left. After the collision the first trolley
rebounds at 0.30 m/s to the left.

*Calculate the velocity of the second trolley.*

*Equation:*
$$m_1u_1 + m_2u_2 = m_1v_1 + m_2v_2$$

*Substitute:*
$$(0.50 \times 1.5) + (0.30 \times -1.0) = (0.50 \times -0.30) + (0.30 \times v_2)$$

*Rearrange and solve:*
$$0.75 - 0.30 = -0.15 + 0.30v_2 \implies v_2 = 2.0\ \mathrm{m/s}$$

**Important:** total momentum before a collision or explosion always equals total momentum
after, provided no external forces act. Always state which direction is positive before
substituting — a velocity in the opposite direction must be entered as negative.
""",

    ("Our Dynamic Universe", "Momentum and Impulse", "Explosions and Recoil"): r"""
**Example:** A stationary firework shell of total mass 2.0 kg explodes into two fragments:
fragment A (mass 0.8 kg) and fragment B (mass 1.2 kg). Fragment A moves off at 15 m/s.

*Calculate the velocity of fragment B immediately after the explosion.*

Total momentum before the explosion is zero:

*Equation:*
$$0 = m_1v_1 + m_2v_2$$

*Substitute:*
$$0 = (0.8 \times 15) + 1.2v_2$$

*Rearrange and solve:*
$$0 = 12 + 1.2v_2 \implies v_2 = -10\ \mathrm{m/s}$$

**Important:** since total momentum starts at zero, the two fragments must always move off in
**opposite** directions with equal and opposite momenta — a negative answer here just means
fragment B moves the opposite way to fragment A.
""",

    ("Our Dynamic Universe", "Momentum and Impulse", "Elastic and Inelastic Collisions"): r"""
**Example:** Trolley A of mass 0.50 kg moving at 4.0 m/s collides with a stationary trolley B
of mass 0.50 kg. After the collision the two move off together at 2.0 m/s.

*Determine, by calculation, whether the collision is elastic or inelastic.*

Whether a collision is elastic or inelastic is decided by comparing the **total kinetic
energy** before and after (momentum is always conserved in a collision, so it cannot be used
to decide this):

$$E_k(\text{before}) = \tfrac{1}{2} \times 0.50 \times 4.0^2 = 4.0\ \mathrm{J}$$
$$E_k(\text{after}) = \left(\tfrac{1}{2} \times 0.50 \times 2.0^2\right) + \left(\tfrac{1}{2} \times 0.50 \times 2.0^2\right) = 2.0\ \mathrm{J}$$

Since $E_k(\text{before}) > E_k(\text{after})$, kinetic energy has been lost, so the collision
is **inelastic**.

**Common exam trap:** an *elastic* collision needs $E_k(\text{before}) = E_k(\text{after})$
exactly — if the two totals differ at all, the collision is inelastic, even if momentum still
balances perfectly on both sides.
""",

    ("Our Dynamic Universe", "Momentum and Impulse", "Explain — Reducing Injury"): r"""
**Example:** During a crash, an airbag inflates, then slowly deflates as the passenger's head
presses into it.

*Explain, in terms of impulse, why this reduces the risk of injury to the passenger.*

The change in momentum (mv − mu) needed to bring the passenger's head to rest is fixed by the
crash — the airbag can't change *that*. What it changes is the **time** over which it happens:

$$Ft = mv - mu$$

Since the right-hand side is fixed, increasing $t$ (the airbag lets the head decelerate over a
longer time than hitting the dashboard directly) must decrease $F$ — and it is the force that
causes injury, not the change in momentum itself.

**Common exam trap:** these questions are often answered with "it reduces the impulse" or "it
reduces the force" without saying *why* — full marks need the chain of reasoning: the change in
momentum is fixed → the device increases the time → so the force must decrease. Also watch the
direction of the time/force relationship — a *longer* time gives a *smaller* force, not a larger
one.
""",

    ("Our Dynamic Universe", "Energy, Work and Power", "Conservation — Frictional Force"): r"""
**Example:** A skateboarder of mass 55 kg starts from rest at the top of a ramp of height
2.0 m. She reaches 5.5 m/s at the bottom, having travelled 8.0 m along the ramp.

*Calculate the average frictional force acting on her.*

**Step 1 — GPE lost:**

*Equation:*
$$E_p = mgh$$

*Substitute:*
$$E_p = 55 \times 9.8 \times 2.0$$

*Answer:*
$$E_p = 1078\ \mathrm{J}$$

**Step 2 — KE gained:**

*Equation:*
$$E_k = \tfrac{1}{2}mv^2$$

*Substitute:*
$$E_k = \tfrac{1}{2} \times 55 \times 5.5^2$$

*Answer:*
$$E_k = 832\ \mathrm{J}$$

**Step 3 — energy lost to friction, then the frictional force:**

*Equation:*
$$\text{energy lost} = E_p - E_k \qquad E_W = Fd$$

*Substitute:*
$$\text{energy lost} = 1078 - 832 = 246\ \mathrm{J} \qquad 246 = F \times 8.0$$

*Rearrange and solve:*
$$F = \frac{246}{8.0} = 31\ \mathrm{N}$$

**Important:** any energy that "goes missing" between two points has been lost, usually to
friction, and that lost energy equals the work done against the resistive force.
""",

    ("Our Dynamic Universe", "Effective Weight", "Beyond Lifts — Explain Free Fall"): r"""
**Example:** A skydiver of mass 75 kg is falling and speeding up at a rate of 9.8 m/s² (free
fall) before their parachute opens. A harness sensor recording the force exerted on the
skydiver by their equipment reads 0 N. Explain why this reading is 0 N.

In free fall, gravity (weight) is the **only** force acting on the skydiver — the equipment
exerts no additional supporting force. Since the resultant force is just the weight, the
acceleration equals g, and the harness sensor, which measures any *extra* supporting force,
reads 0 N.

**Common exam trap:** this doesn't mean gravity has "switched off" — it's still acting exactly
as normal. It's the *absence of any other force* that makes the sensor read zero, not the
absence of weight.
""",

    ("Our Dynamic Universe", "Components of Vectors", "Level 1 — Finding Components"): r"""
**Example:** A force of 50 N acts at 40° above the horizontal.

*Resolve it into horizontal and vertical components.*

*Equation:*
$$F_x = F\cos\theta \qquad F_y = F\sin\theta$$

*Substitute:*
$$F_x = 50\cos40° \qquad F_y = 50\sin40°$$

*Answer:*
$$F_x = 38.3\ \mathrm{N} \qquad F_y = 32.1\ \mathrm{N}$$

**Important:** always check which angle is given — the angle to the horizontal, or the angle to
the slope/vertical — since this decides whether a component uses sin or cos.
""",

    ("Our Dynamic Universe", "Components of Vectors", "Level 3 — Weight on a Slope"): r"""
**Example:** A crate of mass 20 kg rests on a ramp inclined at 25° to the horizontal.

**(a) Calculate the weight of the object.**

*Equation:*
$$W = mg$$

*Substitute:*
$$W = 20 \times 9.8$$

*Answer:*
$$W = 196\ \mathrm{N}$$

**(b) Calculate the component of the weight acting parallel to (down) the slope.**

*Equation:*
$$W_{\parallel} = W\sin\theta$$

*Substitute:*
$$W_{\parallel} = 196 \times \sin25°$$

*Answer:*
$$W_{\parallel} = 82.8\ \mathrm{N}$$

**Common exam trap:** the component *parallel* to the slope uses **sin** θ, and the component
*perpendicular* to the slope (into the surface) uses **cos** θ — mixing these up is the most
common mistake.
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

*Equation:*
$$\Delta = |\text{OoM}_1 - \text{OoM}_2|$$

*Substitute:*
$$\Delta = |-27 - (-28)|$$

*Answer:*
$$\Delta = 1$$
""",

    ("Electricity and Energy", "Power and Efficiency"): r"""
**Example:** A 2000 W heater runs for 300 s, supplying 480 000 J of useful heat.

*Calculate the input energy and the efficiency.*

**(a) Input energy:**

*Equation:*
$$E = P \times t$$

*Substitute:*
$$E = 2000 \times 300$$

*Answer:*
$$E = 600\,000\ \mathrm{J}$$

**(b) Efficiency:**

*Equation:*
$$\text{Efficiency} = \frac{\text{Useful Energy}}{\text{Input Energy}} \times 100\%$$

*Substitute:*
$$\text{Efficiency} = \frac{480\,000}{600\,000} \times 100\%$$

*Answer:*
$$\text{Efficiency} = 80\%$$
""",

}


def get_examples(topic, question_type, sub_type=None):
    topic = canonical_unit(topic)
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


def get_canonical_question(generate_fn, seed=42):
    """
    Runs generate_fn with a fixed seed so the same canonical instance is
    produced every time — used to preview a question type's notes/example
    before the student has generated a real (randomised) question.
    """
    state = random.getstate()
    try:
        random.seed(seed)
        q = generate_fn()
    finally:
        random.setstate(state)
    return q


def notes_for(q):
    """A question's own notes, or — for a scenario — the notes shared by
    (most of) its parts, shown once rather than repeated per part."""
    if not q.is_scenario:
        return q.notes or ""
    notes_list = [p.notes for p in q.parts if p.notes]
    if not notes_list:
        return ""
    return max(set(notes_list), key=notes_list.count)


def format_example(q):
    """Formats an already-generated question's own question text + working
    (equation -> substitution -> answer, the same convention used throughout
    this file) as a worked example — the same steps normally shown in the
    "Worked Solution" expander after answering."""
    if not q.is_scenario:
        return _format_example_question(q, "Example")

    blocks = [q.scenario_context] if q.scenario_context else []
    blocks += [
        _format_example_question(part, f"Part {i + 1}")
        for i, part in enumerate(q.parts)
    ]
    return "\n\n---\n\n".join(blocks)


def derive_example(generate_fn, seed=42):
    """Fallback for question types with no hand-authored EXAMPLES entry —
    see format_example()."""
    return format_example(get_canonical_question(generate_fn, seed=seed))


# ── Matching an example to a generated question ──────────────────────────────
#
# Most generators pick between several variants at random (which quantity is
# unknown, which units, series vs parallel…), so the example for a generated
# question is taken from another run of the same generator that produced the
# same variant — identified by the answer's unit and the shape of the first
# equation in the working, with the numbers stripped out.

_CHOICE_TYPES = ("classification", "graph_mcq", "explain")


def _equation_shape(latex):
    shape = re.sub(r"\d+(?:\.\d+)?", "#", latex)
    shape = re.sub(r"[\s()\-−]", "", shape)
    return re.sub(r"#(?:\+#)+", "#+#", shape)


def _part_signature(q):
    """(kind, unit, first-equation shape, number of working steps) — the step
    count separates e.g. a plain d = vt from one needing an hours → s conversion."""
    if q.metadata.get("type") in _CHOICE_TYPES or q.metadata.get("options"):
        return ("choice", q.metadata.get("type"), "", 0)
    first_equation = next(
        (step["content"] for step in q.working if step.get("type") == "latex"), "")
    return ("calc", q.unit, _equation_shape(first_equation), len(q.working))


def _signature(q, fields):
    parts = q.parts if q.is_scenario else [q]
    return tuple(_part_signature(p)[:fields] for p in parts)


# Strictest first: same working structure → same first equation → same unit(s).
_MATCH_LEVELS = (4, 3, 2)


def _full_text(q):
    if q.is_scenario:
        return q.scenario_context + "".join(p.question_text for p in q.parts)
    return q.question_text


def matching_example(generate_fn, q, attempts=150):
    """A different question from generate_fn of the same variant as q — the
    closest match found in `attempts` runs (see _MATCH_LEVELS), else any other
    instance. Seeds are fixed so the example for a given question is stable
    across reruns."""
    targets = [_signature(q, n) for n in _MATCH_LEVELS]
    target_text = _full_text(q)
    best, best_rank = None, len(_MATCH_LEVELS)
    state = random.getstate()
    try:
        for seed in range(attempts):
            random.seed(1000 + seed)
            candidate = generate_fn()
            if _full_text(candidate) == target_text:
                continue
            rank = next((i for i, n in enumerate(_MATCH_LEVELS)
                         if _signature(candidate, n) == targets[i]), len(_MATCH_LEVELS))
            if rank == 0:
                return candidate
            if best is None or rank < best_rank:
                best, best_rank = candidate, rank
    finally:
        random.setstate(state)
    return best or q


def example_for_question(generate_fn, q):
    """Worked-example markdown of the same variant as the generated question q."""
    return format_example(matching_example(generate_fn, q))
