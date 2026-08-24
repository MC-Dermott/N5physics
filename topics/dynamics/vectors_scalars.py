import random

from core.models.question_model import PhysicsQuestion
from utils.notes import NOTES

# Quantities restricted to the Dynamics topic (no quantities from other units).
SCALARS = ["distance", "speed", "mass", "energy", "kinetic energy", "potential energy", "work done"]
VECTORS = ["force", "acceleration", "velocity", "displacement", "weight"]


def _fmt_pair(a, b):
    order = [a, b]
    random.shuffle(order)
    return f"{order[0]}; {order[1]}"


def _pair_mistake(a, b, kind):
    return (f"{a.capitalize()} and {b} are both {kind}s — a correct pair needs one scalar "
            f"quantity and one vector quantity.")


# ── Pairs: pick the option with one scalar and one vector ──────────────────────

def gen_pairs(level="N5"):
    scalars = random.sample(SCALARS, 5)
    vectors = random.sample(VECTORS, 5)

    correct_pair = _fmt_pair(scalars[0], vectors[0])
    scalar_pair_1 = _fmt_pair(scalars[1], scalars[2])
    scalar_pair_2 = _fmt_pair(scalars[3], scalars[4])
    vector_pair_1 = _fmt_pair(vectors[1], vectors[2])
    vector_pair_2 = _fmt_pair(vectors[3], vectors[4])

    options = [correct_pair, scalar_pair_1, scalar_pair_2, vector_pair_1, vector_pair_2]
    random.shuffle(options)

    distractors = [
        {"value": scalar_pair_1, "mistake": _pair_mistake(scalars[1], scalars[2], "scalar"), "working": []},
        {"value": scalar_pair_2, "mistake": _pair_mistake(scalars[3], scalars[4], "scalar"), "working": []},
        {"value": vector_pair_1, "mistake": _pair_mistake(vectors[1], vectors[2], "vector"), "working": []},
        {"value": vector_pair_2, "mistake": _pair_mistake(vectors[3], vectors[4], "vector"), "working": []},
    ]

    working = [
        {"type": "text",
         "content": f"**{correct_pair}** — {scalars[0]} is a scalar (magnitude only) and "
                    f"{vectors[0]} is a vector (magnitude and direction), so this pair contains "
                    f"one of each."},
    ]

    return PhysicsQuestion(
        question_text="Which of the following contains **one scalar quantity and one vector quantity**?",
        correct_answer=correct_pair,
        unit="",
        distractors=distractors,
        working=working,
        notes=NOTES["vectors_scalars"],
        topic="Dynamics",
        question_type="Vectors and Scalars",
        level=level,
        metadata={"type": "classification", "options": options},
    )


# ── Identify: is a single quantity scalar or vector? ────────────────────────────

def gen_identify(level="N5"):
    target_type = random.choice(["scalar", "vector"])
    if target_type == "scalar":
        pool, distractor_pool, opposite = SCALARS, VECTORS, "vector"
    else:
        pool, distractor_pool, opposite = VECTORS, SCALARS, "scalar"

    correct = random.choice(pool)
    distractor_terms = random.sample(distractor_pool, 3)

    options = [correct] + distractor_terms
    random.shuffle(options)

    distractors = [
        {"value": t,
         "mistake": f"{t.capitalize()} is a {opposite} quantity, not a {target_type} — "
                    f"{'it has magnitude only' if opposite == 'scalar' else 'it has both magnitude and direction'}.",
         "working": []}
        for t in distractor_terms
    ]

    working = [
        {"type": "text",
         "content": f"**{correct.capitalize()}** is a {target_type} quantity — "
                    f"{'it has magnitude only, with no direction' if target_type == 'scalar' else 'it has both magnitude and direction'}."},
    ]

    return PhysicsQuestion(
        question_text=f"Which of the following is a **{target_type}** quantity?",
        correct_answer=correct,
        unit="",
        distractors=distractors,
        working=working,
        notes=NOTES["vectors_scalars"],
        topic="Dynamics",
        question_type="Vectors and Scalars",
        level=level,
        metadata={"type": "classification", "options": options},
    )


_ALL_GENS = [gen_identify, gen_pairs]


def generate_vectors_scalars(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
