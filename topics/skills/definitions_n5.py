from utils.definitions import make_definition_generators

# Definitions for N5 practical and analysis skills (assignment and experimental-method questions),
# worded as in the SQA marking instructions and assignment guidance. See utils/definitions.py.


def _d(group, definition, confusables=(), traps=()):
    return {"group": group, "definition": definition, "confusables": list(confusables), "traps": list(traps)}


DEFINITIONS = {
    "independent variable": _d("Variables", "The variable that is deliberately changed in an experiment.", ["dependent variable", "controlled variable"]),
    "dependent variable": _d("Variables", "The variable that is measured in an experiment.", ["independent variable"]),
    "controlled variable": _d("Variables", "A variable that is kept the same to make the experiment a fair test.", ["independent variable"]),
    "reading uncertainty": _d("Uncertainty", "The uncertainty in a single reading: ± half the smallest division on an analogue scale, or ± 1 in the last digit on a digital display.",
                              ["random uncertainty"]),
    "random uncertainty": _d("Uncertainty", "Uncertainty caused by unpredictable variations between repeated readings, estimated as (maximum − minimum) ÷ number of values.",
                             ["systematic uncertainty", "reading uncertainty"]),
    "systematic uncertainty": _d("Uncertainty", "An uncertainty that shifts every reading by the same amount in the same direction, e.g. a meter that doesn't read zero.",
                                 ["random uncertainty"],
                                 [("An uncertainty that is reduced by repeating readings.", "Repeating readings reduces **random** uncertainty, not systematic.")]),
    "mean": _d("Processing data", "The sum of the repeated values divided by the number of values.", ["random uncertainty"]),
    "accuracy": _d("Quality of results", "How close a measured value is to the true (accepted) value.", ["precision", "reliability"],
                   [("How close repeated readings are to each other.", "That is **precision** (or reliability).")]),
    "precision": _d("Quality of results", "How close repeated measurements are to each other (a small spread).", ["accuracy"]),
    "reliability": _d("Quality of results", "How consistently the same result is obtained when the experiment is repeated.", ["accuracy"]),
}
OVERLAPS = [{"precision", "reliability"}]
STATEMENTS = [
    ("repeat", "Repeating measurements and finding the mean improves the reliability of the results.", True, "It reduces the effect of random uncertainty."),
    ("repeat", "Repeating measurements removes a systematic uncertainty.", False, "A systematic error affects every repeat the same way."),
    ("random", "Random uncertainty = (maximum value − minimum value) ÷ number of values.", True, "As on the relationships sheet."),
    ("reading", "The reading uncertainty of a digital meter is ± 1 in the last digit.", True, "For an analogue scale it is ± half a division."),
    ("reading", "The reading uncertainty of an analogue scale is ± 1 division.", False, "It is ± **half** the smallest division."),
    ("line", "A line of best fit that does not pass through the origin can show a systematic uncertainty.", True, "Every point is shifted by the same amount."),
    ("line", "A line of best fit should always be forced through the origin.", False, "Draw the best fit to the points; don't force it (course reports 2024–2025)."),
    ("var", "The independent variable is plotted on the x-axis.", True, "The dependent variable goes on the y-axis."),
    ("aim", "‘To find out if voltage affects current’ is a good aim for an N5 assignment.", False,
     "A yes/no aim is not acceptable — the aim must be to find the relationship (course reports 2024–2025)."),
    ("aim", "‘To investigate the relationship between the current and the voltage across a resistor’ is an acceptable aim.", True,
     "It names both variables and asks for a relationship."),
]
GENERATORS = make_definition_generators("Skills", DEFINITIONS, STATEMENTS, OVERLAPS, title="N5 Skills Definitions")
