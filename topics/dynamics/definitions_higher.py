from utils.definitions import make_definition_generators

# Definitions needed for Higher Our Dynamic Universe, worded as accepted in SQA
# marking instructions. Split to match the app's Part 1 / Part 2 pacing. See
# utils/definitions.py for the entry format.

# ── Part 1: motion, forces, momentum, energy ───────────────────────────────────

PART1_DEFINITIONS = {
    # Motion
    "scalar quantity": {
        "group": "Motion",
        "definition": "A quantity that has magnitude only.",
        "confusables": ["vector quantity"],
    },
    "vector quantity": {
        "group": "Motion",
        "definition": "A quantity that has both magnitude and direction.",
        "confusables": ["scalar quantity"],
    },
    "displacement": {
        "group": "Motion",
        "definition": "The distance travelled in a stated direction from the starting point.",
        "confusables": ["velocity"],
    },
    "velocity": {
        "group": "Motion",
        "definition": "The rate of change of displacement.",
        "confusables": ["acceleration", "displacement"],
    },
    "acceleration": {
        "group": "Motion",
        "definition": "The rate of change of velocity.",
        "confusables": ["velocity"],
        "traps": [("The rate of change of displacement.",
                   "That is **velocity**. Acceleration is the rate of change of velocity.")],
    },
    "component of a vector": {
        "group": "Motion",
        "definition": "The effect of a vector in a particular direction — a vector can be split "
                      "into two components at right angles to each other.",
        "confusables": ["vector quantity"],
    },

    # Forces
    "Newton's first law": {
        "group": "Forces",
        "definition": "An object will remain at rest, or continue to move at a constant "
                      "velocity, unless acted on by an unbalanced force.",
        "confusables": ["Newton's second law", "Newton's third law"],
    },
    "Newton's second law": {
        "group": "Forces",
        "definition": "The acceleration of an object is directly proportional to the unbalanced "
                      "force acting on it and inversely proportional to its mass (F = ma).",
        "confusables": ["Newton's first law", "Newton's third law"],
    },
    "Newton's third law": {
        "group": "Forces",
        "definition": "If object A exerts a force on object B, then object B exerts an equal "
                      "and opposite force on object A.",
        "confusables": ["Newton's first law", "Newton's second law"],
        "traps": [("If object A exerts a force on object B, then an equal and opposite force "
                   "acts on object A, so the forces on A cancel out.",
                   "Newton's third law pairs act on **different** objects, so they never cancel "
                   "each other out.")],
    },
    "tension": {
        "group": "Forces",
        "definition": "The pulling force exerted by a string, cable or tow bar.",
        "confusables": ["friction"],
    },
    "friction": {
        "group": "Forces",
        "definition": "A force that opposes the motion of an object.",
        "confusables": ["tension"],
    },
    "terminal velocity": {
        "group": "Forces",
        "definition": "The constant velocity reached by a falling object when the air "
                      "resistance acting on it is equal in size to its weight.",
        "confusables": ["Newton's first law"],
    },
    "apparent weight": {
        "group": "Forces",
        "definition": "The reading on a set of scales — equal to the upward (normal reaction) "
                      "force the scales exert on the object.",
        "confusables": ["tension", "Newton's third law"],
        "traps": [("The force of gravity acting on the object.",
                   "That is the object's actual weight, which doesn't change. Apparent weight "
                   "is what the **scales** read, which changes when the lift accelerates.")],
    },

    # Momentum and impulse
    "momentum": {
        "group": "Momentum and impulse",
        "definition": "The product of an object's mass and its velocity (p = mv).",
        "confusables": ["impulse", "work done"],
        "traps": [("The product of an object's mass and its speed.",
                   "Momentum is a **vector**, so it uses velocity, not speed.")],
    },
    "impulse": {
        "group": "Momentum and impulse",
        "definition": "The change in momentum of an object — equal to the average force "
                      "multiplied by the time for which it acts (Ft).",
        "confusables": ["momentum", "work done"],
        "traps": [("The average force multiplied by the distance through which it acts.",
                   "Force × distance is **work done**. Impulse is force × **time**.")],
    },
    "conservation of linear momentum": {
        "group": "Momentum and impulse",
        "definition": "In the absence of external forces, the total momentum before a collision "
                      "or explosion is equal to the total momentum after.",
        "confusables": ["conservation of energy", "elastic collision"],
    },
    "elastic collision": {
        "group": "Momentum and impulse",
        "definition": "A collision in which both momentum and kinetic energy are conserved.",
        "confusables": ["inelastic collision"],
    },
    "inelastic collision": {
        "group": "Momentum and impulse",
        "definition": "A collision in which momentum is conserved but kinetic energy is not.",
        "confusables": ["elastic collision"],
        "traps": [("A collision in which neither momentum nor kinetic energy is conserved.",
                   "Momentum is **always** conserved in a collision when no external forces "
                   "act — only kinetic energy is lost.")],
    },

    # Energy
    "work done": {
        "group": "Energy",
        "definition": "The energy transferred when a force moves an object through a distance "
                      "(Ew = Fd).",
        "confusables": ["power", "impulse"],
    },
    "power": {
        "group": "Energy",
        "definition": "The energy transferred per unit time.",
        "confusables": ["work done"],
    },
    "conservation of energy": {
        "group": "Energy",
        "definition": "Energy cannot be created or destroyed, only changed from one form to "
                      "another.",
        "confusables": ["conservation of linear momentum"],
    },
}

PART1_STATEMENTS = [
    # key, statement, correct?, explanation
    ("mom_vec", "Momentum is a vector quantity.", True,
     "p = mv and velocity is a vector, so momentum has magnitude and direction."),
    ("mom_vec", "Momentum is a scalar quantity.", False,
     "Momentum is a **vector** — it takes the direction of the velocity."),
    ("inelastic", "In an inelastic collision momentum is conserved but kinetic energy is not.",
     True, "Some kinetic energy is changed into other forms, e.g. heat and sound."),
    ("inelastic", "In an inelastic collision neither momentum nor kinetic energy is conserved.",
     False, "Momentum is **always** conserved when no external forces act."),
    ("impulse", "Impulse is equal to the change in momentum.", True,
     "Ft = mv − mu."),
    ("impulse", "For the same change in momentum, increasing the time of contact increases the "
     "average force.", False,
     "Ft = Δp — a **longer** contact time gives a **smaller** average force."),
    ("n3", "The two forces in a Newton's third law pair act on different objects.", True,
     "That is why third-law pairs never cancel each other out."),
    ("n3", "The two forces in a Newton's third law pair act on the same object and cancel out.",
     False, "Third-law pairs act on **different** objects."),
    ("lift", "When a lift accelerates upwards, the reading on scales inside it is greater than "
     "the person's weight.", True,
     "An upward unbalanced force is needed, so the scales push up with more than the weight."),
    ("lift", "When a lift moves upwards at a constant velocity, the reading on scales inside it "
     "is greater than the person's weight.", False,
     "At constant velocity the forces are **balanced**, so the scales read the weight."),
    ("graphs", "The area under a velocity–time graph gives the displacement.", True,
     "Area = velocity × time = displacement."),
    ("graphs", "The gradient of a displacement–time graph gives the acceleration.", False,
     "The gradient of a displacement–time graph gives the **velocity**."),
    ("freefall", "An object in free fall has an apparent weight of zero.", True,
     "Nothing pushes up on it — the only force acting is its weight."),
]

# ── Part 2: projectiles, gravitation, special relativity, expanding Universe ───

PART2_DEFINITIONS = {
    # Projectiles and gravitation
    "projectile": {
        "group": "Projectiles and gravitation",
        "definition": "An object that, once launched, moves under the influence of gravity only.",
        "confusables": ["gravitational field"],
    },
    "gravitational field": {
        "group": "Projectiles and gravitation",
        "definition": "A region in which a mass experiences a force.",
        "confusables": ["gravitational field strength"],
    },
    "gravitational field strength": {
        "group": "Projectiles and gravitation",
        "definition": "The gravitational force acting per unit mass.",
        "confusables": ["gravitational field", "Newton's law of universal gravitation"],
        "traps": [("The mass per unit gravitational force.",
                   "It is the other way round — g = F ÷ m (N/kg).")],
    },
    "Newton's law of universal gravitation": {
        "group": "Projectiles and gravitation",
        "definition": "Every mass attracts every other mass with a force that is directly "
                      "proportional to the product of their masses and inversely proportional "
                      "to the square of the distance between their centres.",
        "confusables": ["gravitational field strength"],
        "traps": [("Every mass attracts every other mass with a force that is directly "
                   "proportional to the product of their masses and inversely proportional "
                   "to the distance between their centres.",
                   "It is an **inverse square** law — the force depends on 1 ÷ r².")],
    },

    # Special relativity
    "frame of reference": {
        "group": "Special relativity",
        "definition": "The viewpoint, with its own coordinates and clock, from which an observer "
                      "makes measurements.",
        "confusables": ["inertial frame of reference"],
    },
    "inertial frame of reference": {
        "group": "Special relativity",
        "definition": "A frame of reference that is not accelerating — it is at rest or moving "
                      "at a constant velocity.",
        "confusables": ["frame of reference"],
    },
    "first postulate of special relativity": {
        "group": "Special relativity",
        "definition": "The laws of physics are the same for all observers in inertial frames "
                      "of reference.",
        "confusables": ["second postulate of special relativity"],
    },
    "second postulate of special relativity": {
        "group": "Special relativity",
        "definition": "The speed of light in a vacuum is the same for all observers, whatever "
                      "their motion.",
        "confusables": ["first postulate of special relativity"],
    },
    "time dilation": {
        "group": "Special relativity",
        "definition": "A clock moving relative to an observer is measured to run slower than a "
                      "clock at rest relative to that observer.",
        "confusables": ["length contraction"],
        "traps": [("A clock moving relative to an observer is measured to run faster than a "
                   "clock at rest relative to that observer.",
                   "Moving clocks run **slow** — the observer measures a longer time "
                   "(t′ > t).")],
    },
    "length contraction": {
        "group": "Special relativity",
        "definition": "An object moving relative to an observer is measured to be shorter, in "
                      "its direction of motion, than when it is at rest.",
        "confusables": ["time dilation"],
        "traps": [("An object moving relative to an observer is measured to be longer, in its "
                   "direction of motion, than when it is at rest.",
                   "Moving objects are measured to be **shorter** (l′ < l).")],
    },

    # The expanding Universe
    "Doppler effect": {
        "group": "The expanding Universe",
        "definition": "The change in the observed frequency of a wave when the source and the "
                      "observer are moving relative to each other.",
        "confusables": ["redshift"],
    },
    "redshift": {
        "group": "The expanding Universe",
        "definition": "The increase in the observed wavelength of light from a source moving "
                      "away from the observer.",
        "confusables": ["Doppler effect", "Hubble's law"],
        "traps": [("The decrease in the observed wavelength of light from a source moving "
                   "away from the observer.",
                   "A source moving away has its light stretched to **longer** wavelengths — "
                   "towards the red end of the spectrum.")],
    },
    "Hubble's law": {
        "group": "The expanding Universe",
        "definition": "The recessional velocity of a galaxy is directly proportional to its "
                      "distance from us (v = H₀d).",
        "confusables": ["redshift"],
        "traps": [("The recessional velocity of a galaxy is inversely proportional to its "
                   "distance from us.",
                   "More distant galaxies are moving away **faster** — v is directly "
                   "proportional to d.")],
    },
    "dark matter": {
        "group": "The expanding Universe",
        "definition": "Matter that does not emit light but whose gravitational effect is "
                      "detected, e.g. from the orbital speeds of stars in galaxies.",
        "confusables": ["dark energy"],
    },
    "dark energy": {
        "group": "The expanding Universe",
        "definition": "The unknown cause of the accelerating rate of expansion of the Universe.",
        "confusables": ["dark matter"],
    },
    "cosmic microwave background": {
        "group": "The expanding Universe",
        "definition": "Radiation left over from the early Universe, detected as microwaves "
                      "coming from every direction — evidence for the Big Bang.",
        "confusables": ["redshift", "dark energy"],
    },
}

PART2_STATEMENTS = [
    # key, statement, correct?, explanation
    ("proj", "The horizontal velocity of a projectile is constant (ignoring air resistance).",
     True, "No horizontal force acts, so there is no horizontal acceleration."),
    ("proj", "At the highest point of its path, the velocity of a projectile is zero.", False,
     "Only the **vertical** velocity is zero — the horizontal velocity is unchanged."),
    ("grav", "If the distance between two masses doubles, the gravitational force between them "
     "is quartered.", True, "F ∝ 1 ÷ r², so doubling r divides F by 2² = 4."),
    ("grav", "If the distance between two masses doubles, the gravitational force between them "
     "halves.", False, "It is an **inverse square** law — the force is quartered."),
    ("c", "The speed of light in a vacuum is the same for all observers.", True,
     "This is the second postulate of special relativity."),
    ("dilation", "A clock moving relative to an observer is measured to run slow.", True,
     "This is time dilation."),
    ("dilation", "Time dilation is noticeable at everyday speeds such as a car on a motorway.",
     False, "Relativistic effects are only significant at speeds close to the speed of light."),
    ("length", "An object moving relative to an observer is measured to be longer in its "
     "direction of motion.", False,
     "Length contraction — the moving object is measured to be **shorter**."),
    ("redshift", "Light from a galaxy moving away from us is redshifted.", True,
     "Its observed wavelength is longer than the wavelength emitted."),
    ("hubble", "The more distant a galaxy, the greater its recessional velocity.", True,
     "Hubble's law: v = H₀d."),
    ("dark", "Dark energy is used to explain why the expansion of the Universe is "
     "accelerating.", True, "This is what dark energy was proposed to explain."),
    ("dark", "Dark matter is used to explain why the expansion of the Universe is "
     "accelerating.", False,
     "That is **dark energy**. Dark matter explains the orbital speeds of stars in galaxies."),
    ("cmb", "The cosmic microwave background is evidence for the Big Bang.", True,
     "It is radiation left over from the hot, dense early Universe."),
]

PART1_GENERATORS = make_definition_generators(
    "Our Dynamic Universe", PART1_DEFINITIONS, PART1_STATEMENTS,
    title="Our Dynamic Universe Definitions (Part 1)")
PART2_GENERATORS = make_definition_generators(
    "Our Dynamic Universe", PART2_DEFINITIONS, PART2_STATEMENTS,
    title="Our Dynamic Universe Definitions (Part 2)")

# Crash Higher covers the whole of Our Dynamic Universe as one unit.
CRASH_GENERATORS = make_definition_generators(
    "Our Dynamic Universe", {**PART1_DEFINITIONS, **PART2_DEFINITIONS}, PART1_STATEMENTS + PART2_STATEMENTS,
    title="Our Dynamic Universe Definitions")
