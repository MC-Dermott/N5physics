from utils.definitions import make_definition_generators
from utils.notes import NOTES

# Definitions needed for the N5 Dynamics unit, taken from what SQA past papers
# (2022–2026) and marking instructions ask for.
#
# Each entry:
#   definition   — the wording to learn (as accepted in the marking instructions)
#   confusables  — terms whose definitions make the most convincing distractors
#   traps        — (wrong definition, why it's wrong) pairs taken from exam misconceptions
DEFINITIONS = {
    # ── Motion ─────────────────────────────────────────────────────────────────
    "scalar quantity": {
        "group": "motion",
        "definition": "A quantity that has magnitude (size) only.",
        "confusables": ["vector quantity"],
    },
    "vector quantity": {
        "group": "motion",
        "definition": "A quantity that has both magnitude (size) and direction.",
        "confusables": ["scalar quantity"],
    },
    "distance": {
        "group": "motion",
        "definition": "The total length of the path travelled.",
        "confusables": ["displacement", "speed"],
    },
    "displacement": {
        "group": "motion",
        "definition": "The straight-line length from the start point to the finish point, "
                      "in a stated direction.",
        "confusables": ["distance", "velocity"],
    },
    "speed": {
        "group": "motion",
        "definition": "The distance travelled per unit time.",
        "confusables": ["velocity", "acceleration"],
    },
    "velocity": {
        "group": "motion",
        "definition": "The displacement per unit time.",
        "confusables": ["speed", "acceleration"],
    },
    "acceleration": {
        "group": "motion",
        "definition": "The change in velocity per unit time.",
        "confusables": ["velocity", "speed"],
        "traps": [("The change in speed per unit distance.",
                   "Acceleration is a change in velocity per unit **time**, not per unit distance.")],
    },
    "average speed": {
        "group": "motion",
        "definition": "The total distance travelled divided by the total time taken.",
        "confusables": ["instantaneous speed"],
    },
    "instantaneous speed": {
        "group": "motion",
        "definition": "The speed at a particular moment, measured over a very short time.",
        "confusables": ["average speed"],
    },

    # ── Forces ─────────────────────────────────────────────────────────────────
    "mass": {
        "group": "forces",
        "definition": "The amount of matter in an object.",
        "confusables": ["weight", "gravitational field strength"],
    },
    "weight": {
        "group": "forces",
        "definition": "The force of gravity acting on an object.",
        "confusables": ["mass", "gravitational field strength"],
    },
    "gravitational field strength": {
        "group": "forces",
        "definition": "The weight per unit mass.",
        "confusables": ["weight", "mass"],
        "traps": [("The mass per unit weight.",
                   "It is the other way round — gravitational field strength is weight ÷ mass "
                   "(N/kg).")],
    },
    "the newton": {
        "group": "forces",
        "definition": "The force that gives a mass of 1 kg an acceleration of 1 m/s².",
        "confusables": ["weight", "Newton's second law"],
    },
    "unbalanced (resultant) force": {
        "group": "forces",
        "definition": "The single force that has the same effect as all the forces acting on "
                      "an object combined.",
        "confusables": ["balanced forces"],
    },
    "balanced forces": {
        "group": "forces",
        "definition": "Forces that are equal in size and opposite in direction, so the "
                      "resultant force is zero.",
        "confusables": ["unbalanced (resultant) force", "friction"],
    },
    "friction": {
        "group": "forces",
        "definition": "A force that opposes the motion of an object.",
        "confusables": ["weight"],
    },
    "Newton's first law": {
        "group": "forces",
        "definition": "An object will remain at rest, or continue to move at a constant "
                      "velocity, unless acted on by an unbalanced force.",
        "confusables": ["Newton's second law", "balanced forces"],
        "traps": [("An object will only keep moving if an unbalanced force acts on it.",
                   "An object moving at constant velocity needs **no** unbalanced force — the "
                   "forces on it are balanced.")],
    },
    "Newton's second law": {
        "group": "forces",
        "definition": "The acceleration of an object is directly proportional to the "
                      "unbalanced force acting on it and inversely proportional to its mass "
                      "(F = ma).",
        "confusables": ["Newton's first law", "the newton"],
    },
    "terminal velocity": {
        "group": "forces",
        "definition": "The constant velocity reached by a falling object when the air "
                      "resistance acting on it is equal in size to its weight.",
        "confusables": ["Newton's first law"],
        "traps": [("The velocity reached by a falling object when the air resistance is "
                   "greater than its weight.",
                   "At terminal velocity the forces are **balanced** — air resistance is equal "
                   "to the weight, so the object no longer accelerates.")],
    },

    # ── Energy ─────────────────────────────────────────────────────────────────
    "work done": {
        "group": "energy",
        "definition": "The energy transferred when a force moves an object through a distance.",
        "confusables": ["kinetic energy", "gravitational potential energy"],
    },
    "kinetic energy": {
        "group": "energy",
        "definition": "The energy an object has because it is moving.",
        "confusables": ["gravitational potential energy", "work done"],
    },
    "gravitational potential energy": {
        "group": "energy",
        "definition": "The energy an object has because of its height above a surface.",
        "confusables": ["kinetic energy", "work done"],
    },
    "conservation of energy": {
        "group": "energy",
        "definition": "Energy cannot be created or destroyed, only changed from one form to "
                      "another.",
        "confusables": ["work done"],
    },

    # ── Projectiles ────────────────────────────────────────────────────────────
    "projectile": {
        "group": "forces",
        "definition": "An object that is given a horizontal velocity and then moves under "
                      "the influence of gravity only.",
        "confusables": ["terminal velocity"],
        "traps": [("An object whose horizontal velocity increases as it falls.",
                   "A projectile's horizontal velocity stays **constant** (ignoring air "
                   "resistance) — only the vertical velocity increases.")],
    },
}

# Terms where one definition also fits the other, so they must never appear as
# options in the same question.
_OVERLAPS = [
    {"speed", "average speed", "instantaneous speed"},
    {"unbalanced (resultant) force", "the newton"},
]


# ── Statements: past-paper style "Which of these statements is/are correct?" ───
#
# Each statement has a `key` so that two statements about the same idea never
# appear together.

STATEMENTS = [
    # key, statement, correct?, explanation
    ("vector", "A vector quantity has both magnitude and direction.", True,
     "A vector has magnitude **and** direction; a scalar has magnitude only."),
    ("vector", "Speed is a vector quantity.", False,
     "Speed is a **scalar** — it has magnitude only. Velocity is the vector."),
    ("displacement", "Displacement is the total length of the path travelled.", False,
     "That is **distance**. Displacement is the straight-line length from start to finish, "
     "in a stated direction."),
    ("acceleration", "Acceleration is the change in velocity per unit time.", True,
     "This is the definition of acceleration."),
    ("mass", "The mass of an object is the same on the Earth as on the Moon.", True,
     "Mass is the amount of matter in an object, so it doesn't depend on where the object is. "
     "Its **weight** changes."),
    ("mass", "Weight is the amount of matter in an object.", False,
     "That is **mass**. Weight is the force of gravity acting on an object."),
    ("gfs", "Gravitational field strength is the weight per unit mass.", True,
     "g = W ÷ m, measured in N/kg."),
    ("newton1", "An object moving at a constant velocity has balanced forces acting on it.", True,
     "Newton's first law — with no unbalanced force, an object stays at rest or moves at "
     "constant velocity."),
    ("newton1", "An object moving at a constant velocity must have an unbalanced force acting "
     "on it.", False,
     "Newton's first law — an object moving at constant velocity has **balanced** forces "
     "acting on it."),
    ("terminal", "A falling object reaches terminal velocity when the air resistance acting on "
     "it is equal in size to its weight.", True,
     "At terminal velocity the forces are balanced, so the object moves at constant velocity."),
    ("projectile", "The horizontal velocity of a projectile stays constant (ignoring air "
     "resistance).", True,
     "No horizontal force acts, so horizontal velocity is constant; only vertical velocity "
     "changes."),
    ("projectile", "The horizontal velocity of a projectile increases as it falls.", False,
     "Gravity acts vertically only — the horizontal velocity stays **constant**."),
]


_GENERATORS = make_definition_generators(
    "Dynamics", DEFINITIONS, STATEMENTS, _OVERLAPS, notes=NOTES["dynamics_definitions"])

gen_term_to_definition = _GENERATORS["Term → Definition"]
gen_definition_to_term = _GENERATORS["Definition → Term"]
gen_statements = _GENERATORS["Which Statements Are Correct?"]
