import random

from core.models.question_model import PhysicsQuestion
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

_TERMS = list(DEFINITIONS)

# Terms where one definition also fits the other, so they must never appear as
# options in the same question.
_OVERLAPS = [
    {"speed", "average speed", "instantaneous speed"},
    {"unbalanced (resultant) force", "the newton"},
]


def _overlaps(a, b):
    return any(a in group and b in group for group in _OVERLAPS)


def _display(term):
    """Capitalise the first letter without lower-casing the rest (Newton, Universe)."""
    return term[0].upper() + term[1:]


def _pick_distractor_terms(term, n):
    """Confusable terms first, then others from the same group, then anything."""
    entry = DEFINITIONS[term]
    chosen = [t for t in entry.get("confusables", [])
              if t in DEFINITIONS and not _overlaps(term, t)]
    random.shuffle(chosen)
    chosen = chosen[:n]

    usable = [t for t in _TERMS if t != term and t not in chosen and not _overlaps(term, t)]
    same_group = [t for t in usable if DEFINITIONS[t]["group"] == entry["group"]]
    random.shuffle(same_group)
    chosen += same_group[:n - len(chosen)]

    others = [t for t in usable if t not in chosen]
    random.shuffle(others)
    chosen += others[:n - len(chosen)]
    return chosen


def _make_question(question_text, correct, distractors, options, working, level):
    return PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        distractors=distractors,
        working=working,
        notes=NOTES["dynamics_definitions"],
        topic="Dynamics",
        question_type="Definitions",
        level=level,
        metadata={"type": "classification", "options": options},
    )


# ── Term → definition: pick the correct definition of a given term ─────────────

def gen_term_to_definition(level="N5"):
    term = random.choice(_TERMS)
    entry = DEFINITIONS[term]
    correct = entry["definition"]

    distractors = []
    # At most one exam-style trap, so the rest come from genuine definitions.
    for wrong, why in random.sample(entry.get("traps", []), min(1, len(entry.get("traps", [])))):
        distractors.append({"value": wrong, "mistake": why, "working": []})

    for other in _pick_distractor_terms(term, 4 - len(distractors)):
        distractors.append({
            "value": DEFINITIONS[other]["definition"],
            "mistake": f"That is the definition of **{other}**, not {term}.",
            "working": [],
        })

    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)

    working = [{"type": "text", "content": f"**{_display(term)}:** {correct}"}]

    return _make_question(
        f"Which of the following is the definition of **{term}**?",
        correct, distractors, options, working, level,
    )


# ── Definition → term: name the term that a definition describes ───────────────

def gen_definition_to_term(level="N5"):
    term = random.choice(_TERMS)
    entry = DEFINITIONS[term]
    others = _pick_distractor_terms(term, 4)

    correct = _display(term)
    distractors = [
        {"value": _display(other),
         "mistake": f"{_display(other)} is defined as: *{DEFINITIONS[other]['definition']}*",
         "working": []}
        for other in others
    ]

    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)

    working = [{"type": "text", "content": f"**{correct}:** {entry['definition']}"}]

    return _make_question(
        f"Which term is described by the following definition?\n\n> {entry['definition']}",
        correct, distractors, options, working, level,
    )


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

_NUMERALS = ["I", "II", "III"]
# The answer combinations in the order SQA lists them.
_COMBINATIONS = [
    (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2),
]


def _combo_label(combo):
    names = [_NUMERALS[i] for i in combo]
    if len(names) == 1:
        return f"{names[0]} only"
    if len(names) == 2:
        return f"{names[0]} and {names[1]} only"
    return "I, II and III"


def gen_statements(level="N5"):
    keys = list({s[0] for s in STATEMENTS})
    chosen_keys = random.sample(keys, 3)
    statements = [random.choice([s for s in STATEMENTS if s[0] == k]) for k in chosen_keys]

    # At least one statement must be correct so the answer is one of the combinations.
    if not any(s[2] for s in statements):
        return gen_statements(level)

    correct_combo = tuple(i for i, s in enumerate(statements) if s[2])
    correct = _combo_label(correct_combo)

    wrong_combos = random.sample([c for c in _COMBINATIONS if c != correct_combo], 4)
    distractors = []
    for combo in wrong_combos:
        reasons = []
        for i, (_, text, is_true, why) in enumerate(statements):
            picked = i in combo
            if picked and not is_true:
                reasons.append(f"Statement {_NUMERALS[i]} is **not** correct — {why}")
            elif not picked and is_true:
                reasons.append(f"Statement {_NUMERALS[i]} **is** correct — {why}")
        distractors.append({"value": _combo_label(combo), "mistake": " ".join(reasons),
                            "working": []})

    options = [_combo_label(c) for c in _COMBINATIONS
               if c == correct_combo or c in wrong_combos]

    statement_lines = "\n\n".join(
        f"**{_NUMERALS[i]}** &nbsp; {text}" for i, (_, text, _, _) in enumerate(statements))
    question_text = ("A student makes the following statements:\n\n"
                     f"{statement_lines}\n\n"
                     "Which of these statements is/are correct?")

    working = [
        {"type": "text",
         "content": f"**{_NUMERALS[i]}** {'✓ Correct' if is_true else '✗ Not correct'} — {why}"}
        for i, (_, _, is_true, why) in enumerate(statements)
    ]
    working.append({"type": "text", "content": f"So the answer is **{correct}**."})

    return _make_question(question_text, correct, distractors, options, working, level)


_ALL_GENS = [gen_term_to_definition, gen_definition_to_term, gen_statements]


def generate_dynamics_definitions(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
