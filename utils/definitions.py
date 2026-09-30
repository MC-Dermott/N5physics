import random

from core.models.question_model import PhysicsQuestion

# Shared engine for the "Definitions" multiple-choice question type. Each unit
# supplies its own bank of definitions (and past-paper style statements) and
# gets back the three question styles:
#
#   Term → Definition               pick the correct definition of a given term
#   Definition → Term               name the term that a definition describes
#   Which Statements Are Correct?   past-paper style I / II / III statements
#
# Definitions bank — {term: entry}, each entry:
#   group        — heading the term is listed under in the notes
#   definition   — the wording to learn (as accepted in the marking instructions)
#   confusables  — terms whose definitions make the most convincing distractors
#   traps        — (wrong definition, why it's wrong) pairs taken from exam misconceptions
#
# Overlaps — sets of terms where one definition also fits another, so they must
# never appear as options in the same question.
#
# Statements — (key, statement, correct?, explanation). Two statements with the
# same key are about the same idea and never appear together.

_NUMERALS = ["I", "II", "III"]
# The answer combinations in the order SQA lists them.
_COMBINATIONS = [
    (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2),
]


def _display(term):
    """Capitalise the first letter without lower-casing the rest (Newton, Universe)."""
    return term[0].upper() + term[1:]


def _combo_label(combo):
    names = [_NUMERALS[i] for i in combo]
    if len(names) == 1:
        return f"{names[0]} only"
    if len(names) == 2:
        return f"{names[0]} and {names[1]} only"
    return "I, II and III"


def definitions_notes(title, definitions):
    """Notes listing every definition in the bank, one table per group."""
    groups = {}
    for term, entry in definitions.items():
        groups.setdefault(entry["group"], []).append((term, entry["definition"]))

    blocks = [f"## {title}"]
    for group, rows in groups.items():
        table = "\n".join(f"| {_display(term)} | {definition} |" for term, definition in rows)
        blocks.append(f"**{group}**\n\n| Term | Definition |\n|---|---|\n{table}")
    return "\n\n".join(blocks) + "\n"


def make_definition_generators(topic, definitions, statements, overlaps=(), notes=None,
                               title=None):
    """Returns {question style: generator} for one unit's Definitions question type.
    Notes default to a table of the whole bank, headed `title`."""
    terms = list(definitions)
    if notes is None:
        notes = definitions_notes(title or f"{topic} Definitions", definitions)

    def overlapping(a, b):
        return any(a in group and b in group for group in overlaps)

    def pick_distractor_terms(term, n):
        """Confusable terms first, then others from the same group, then anything."""
        entry = definitions[term]
        chosen = [t for t in entry.get("confusables", [])
                  if t in definitions and not overlapping(term, t)]
        random.shuffle(chosen)
        chosen = chosen[:n]

        usable = [t for t in terms if t != term and t not in chosen and not overlapping(term, t)]
        same_group = [t for t in usable if definitions[t]["group"] == entry["group"]]
        random.shuffle(same_group)
        chosen += same_group[:n - len(chosen)]

        others = [t for t in usable if t not in chosen]
        random.shuffle(others)
        chosen += others[:n - len(chosen)]
        return chosen

    def make_question(question_text, correct, distractors, options, working, level):
        return PhysicsQuestion(
            question_text=question_text,
            correct_answer=correct,
            unit="",
            distractors=distractors,
            working=working,
            notes=notes,
            topic=topic,
            question_type="Definitions",
            level=level,
            metadata={"type": "classification", "options": options},
        )

    def gen_term_to_definition(level="N5"):
        term = random.choice(terms)
        entry = definitions[term]
        correct = entry["definition"]

        distractors = []
        # At most one exam-style trap, so the rest come from genuine definitions.
        traps = entry.get("traps", [])
        for wrong, why in random.sample(traps, min(1, len(traps))):
            distractors.append({"value": wrong, "mistake": why, "working": []})

        # Skip a term whose definition is the trap's wording, so no option appears twice.
        others = [t for t in pick_distractor_terms(term, len(terms))
                  if definitions[t]["definition"] not in {d["value"] for d in distractors}]
        for other in others[:4 - len(distractors)]:
            distractors.append({
                "value": definitions[other]["definition"],
                "mistake": f"That is the definition of **{other}**, not {term}.",
                "working": [],
            })

        options = [correct] + [d["value"] for d in distractors]
        random.shuffle(options)

        working = [{"type": "text", "content": f"**{_display(term)}:** {correct}"}]

        return make_question(
            f"Which of the following is the definition of **{term}**?",
            correct, distractors, options, working, level,
        )

    def gen_definition_to_term(level="N5"):
        term = random.choice(terms)
        entry = definitions[term]
        others = pick_distractor_terms(term, 4)

        correct = _display(term)
        distractors = [
            {"value": _display(other),
             "mistake": f"{_display(other)} is defined as: *{definitions[other]['definition']}*",
             "working": []}
            for other in others
        ]

        options = [correct] + [d["value"] for d in distractors]
        random.shuffle(options)

        working = [{"type": "text", "content": f"**{correct}:** {entry['definition']}"}]

        return make_question(
            f"Which term is described by the following definition?\n\n> {entry['definition']}",
            correct, distractors, options, working, level,
        )

    def gen_statements(level="N5"):
        keys = list({s[0] for s in statements})
        while True:
            chosen_keys = random.sample(keys, 3)
            chosen = [random.choice([s for s in statements if s[0] == k]) for k in chosen_keys]
            # At least one statement must be correct so the answer is one of the combinations.
            if any(s[2] for s in chosen):
                break

        correct_combo = tuple(i for i, s in enumerate(chosen) if s[2])
        correct = _combo_label(correct_combo)

        wrong_combos = random.sample([c for c in _COMBINATIONS if c != correct_combo], 4)
        distractors = []
        for combo in wrong_combos:
            reasons = []
            for i, (_, text, is_true, why) in enumerate(chosen):
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
            f"**{_NUMERALS[i]}** &nbsp; {text}" for i, (_, text, _, _) in enumerate(chosen))
        question_text = ("A student makes the following statements:\n\n"
                         f"{statement_lines}\n\n"
                         "Which of these statements is/are correct?")

        working = [
            {"type": "text",
             "content": f"**{_NUMERALS[i]}** {'✓ Correct' if is_true else '✗ Not correct'} — {why}"}
            for i, (_, _, is_true, why) in enumerate(chosen)
        ]
        working.append({"type": "text", "content": f"So the answer is **{correct}**."})

        return make_question(question_text, correct, distractors, options, working, level)

    return {
        "Term → Definition":             gen_term_to_definition,
        "Definition → Term":             gen_definition_to_term,
        "Which Statements Are Correct?": gen_statements,
    }
