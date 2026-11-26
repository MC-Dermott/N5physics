"""The shape of one explain question, shared by the explain question banks."""


def _q(source, context, question, points, avoid=None, gate=False):
    """points: one string per mark. gate: SQA's "look for this statement first" rule — if the first point
    is missing or wrong, no marks are given. avoid: wording the marking instructions reject."""
    return {"source": source, "context": context, "question": question, "points": points,
            "avoid": avoid, "gate": gate}
