import random
from utils.make_question import make_question
from core.models.question_model import PhysicsQuestion

_NOTES = """
## Efficiency

$$\\text{Efficiency} = \\frac{\\text{Useful Energy}}{\\text{Input Energy}} \\times 100\\%$$

- **Input energy** = total electrical energy supplied
- **Useful energy** = energy transferred to the desired output (e.g. heat, light, sound)
- **Wasted energy** = input energy − useful energy (usually lost as unwanted heat)
- Efficiency is always between 0% and 100%

**Example:** If a kettle is supplied with 400 000 J and heats the water with 160 000 J,
$$\\text{Efficiency} = \\frac{160\\,000}{400\\,000} \\times 100\\% = 40\\%$$
"""

_NOTES_COMBINED = """
## Electrical Power and Efficiency

**Power:**
$$E = P \\times t$$

**Efficiency:**
$$\\text{Efficiency} = \\frac{\\text{Useful Energy}}{\\text{Input Energy}} \\times 100\\%$$

| Symbol | Quantity | Unit |
|---|---|---|
| P | Power | W |
| E | Energy | J |
| t | Time | s |
"""

# E_total values are multiples of 100 000 to guarantee clean E_useful integers.
_E_TOTALS = [100_000, 200_000, 300_000, 400_000, 500_000, 600_000, 800_000, 1_000_000]
_EFFICIENCIES = [20, 25, 30, 40, 50, 60, 70, 75, 80]

_APPLIANCES = [
    ("electric kettle",   1600),
    ("electric kettle",   2000),
    ("hair dryer",        1200),
    ("hair dryer",        2400),
    ("iron",              1000),
    ("iron",              2000),
    ("toaster",            800),
    ("toaster",           1200),
    ("microwave oven",     800),
    ("microwave oven",    1000),
    ("electric fire",     2000),
    ("electric fire",     3000),
    ("fan heater",        1500),
    ("fan heater",        2000),
]

_TIMES = [60, 90, 120, 150, 180, 240, 300, 360, 450, 600]


def _dedup(options_data, correct):
    correct_r = round(float(correct), 4)
    seen = {correct_r}
    cleaned = []
    for opt in options_data:
        key = round(float(opt["value"]), 4)
        if key not in seen:
            seen.add(key)
            cleaned.append(opt)
        elif opt["mistake"] is None:
            cleaned.insert(0, opt)
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


def _efficiency_working(E_useful, E_total, eff):
    return [
        {"type": "text",  "content": "Use the efficiency formula:"},
        {"type": "latex", "content": r"\text{Efficiency} = \frac{\text{Useful Energy}}{\text{Input Energy}} \times 100\%"},
        {"type": "latex", "content": rf"\text{{Efficiency}} = \frac{{{E_useful}}}{{{E_total}}} \times 100\%"},
        {"type": "latex", "content": rf"\text{{Efficiency}} = {eff}\%"},
    ]


def gen_find_efficiency(level="N4"):
    E_total = random.choice(_E_TOTALS)
    eff = random.choice(_EFFICIENCIES)
    E_useful = E_total * eff // 100
    working = _efficiency_working(E_useful, E_total, eff)

    # Avoid 100-eff equalling eff when eff=50
    waste_eff = 100 - eff
    options_data = [
        {"value": eff,                                    "mistake": None,                                                                "working": working},
        {"value": round(E_total / E_useful * 100, 1),     "mistake": "Divide useful energy by input energy — not the other way round.",   "working": working},
        {"value": round(E_useful / E_total, 4),           "mistake": "Multiply by 100% — efficiency is a percentage, not a decimal.",     "working": working},
        {"value": waste_eff if waste_eff != eff else eff + 5, "mistake": "This is the percentage of energy wasted, not the efficiency.",  "working": working},
    ]
    appliances = ["electric kettle", "iron", "hair dryer", "fan heater", "electric shower", "microwave oven"]
    appliance = random.choice(appliances)
    return make_question(
        f"An {appliance} is supplied with {E_total} J of electrical energy. "
        f"The useful energy output is {E_useful} J. "
        f"Calculate the percentage efficiency of the {appliance}.",
        eff, _dedup(options_data, eff), "%",
        notes=_NOTES, topic="Electricity and Energy",
        question_type="Efficiency", level=level,
    )


def gen_find_useful_energy(level="N4"):
    E_total = random.choice(_E_TOTALS)
    eff = random.choice(_EFFICIENCIES)
    E_useful = E_total * eff // 100
    working = [
        {"type": "text",  "content": "Rearrange the efficiency formula for useful energy:"},
        {"type": "latex", "content": r"\text{Useful Energy} = \frac{\text{Efficiency}}{100} \times \text{Input Energy}"},
        {"type": "latex", "content": rf"\text{{Useful Energy}} = \frac{{{eff}}}{{100}} \times {E_total}"},
        {"type": "latex", "content": rf"\text{{Useful Energy}} = {E_useful}\ \mathrm{{J}}"},
    ]
    E_inverted = round(E_total * 100 / eff)
    E_waste = E_total - E_useful
    options_data = [
        {"value": E_useful,    "mistake": None,                                                                                   "working": working},
        {"value": E_inverted,  "mistake": "Multiply input energy by (efficiency ÷ 100) — do not divide by efficiency.",           "working": working},
        {"value": E_waste,     "mistake": "This is the wasted energy. The useful energy = (efficiency ÷ 100) × input energy.",    "working": working},
        {"value": E_total * eff, "mistake": "Divide by 100 — efficiency is a percentage, so use efficiency ÷ 100.",              "working": working},
    ]
    appliances = ["electric kettle", "iron", "hair dryer", "fan heater", "electric shower", "microwave oven"]
    appliance = random.choice(appliances)
    return make_question(
        f"An {appliance} has an efficiency of {eff}%. "
        f"It is supplied with {E_total} J of electrical energy. "
        f"Calculate the useful energy output.",
        E_useful, _dedup(options_data, E_useful), "J",
        notes=_NOTES, topic="Electricity and Energy",
        question_type="Efficiency", level=level,
    )


def generate_efficiency(level="N4"):
    return random.choice([gen_find_efficiency, gen_find_useful_energy])(level=level)


# ── Combined scenario (exam-style Q2) ─────────────────────────────────────────

def generate_power_efficiency_scenario(level="N4"):
    appliance, P = random.choice(_APPLIANCES)
    t = random.choice(_TIMES)
    E_total = P * t
    eff = random.choice(_EFFICIENCIES)
    E_useful = E_total * eff // 100

    context = (
        f"An {appliance} has a power rating of **{P} W**. "
        f"It is switched on for **{t} seconds**."
    )

    # Part 1 — calculate E from P × t
    part1_working = [
        {"type": "text",  "content": "Rearrange P = E/t for E:"},
        {"type": "latex", "content": r"E = P \times t"},
        {"type": "latex", "content": rf"E = {P} \times {t}"},
        {"type": "latex", "content": rf"E = {E_total}\ \mathrm{{J}}"},
    ]
    part1 = PhysicsQuestion(
        question_text="Calculate how much electrical energy is supplied to the appliance in this time.",
        correct_answer=E_total,
        unit="J",
        topic="Electricity and Energy",
        question_type="Power and Efficiency",
        level=level,
        distractors=[
            {"value": round(P / t, 4), "mistake": "Use E = P × t — do not divide P by t.",      "working": part1_working},
            {"value": P + t,           "mistake": "Multiply P and t — do not add them.",          "working": part1_working},
            {"value": E_total // 2,    "mistake": "Check your calculation — E = P × t.",          "working": part1_working},
        ],
        working=part1_working,
        notes=_NOTES_COMBINED,
    )

    # Part 2 — calculate efficiency using E_total from Part 1
    part2_working = _efficiency_working(E_useful, E_total, eff)
    waste_eff = 100 - eff
    part2 = PhysicsQuestion(
        question_text=(
            f"The useful energy output of the appliance is {E_useful} J. "
            f"Calculate the percentage efficiency."
        ),
        correct_answer=eff,
        unit="%",
        topic="Electricity and Energy",
        question_type="Power and Efficiency",
        level=level,
        distractors=[
            {"value": round(E_total / E_useful * 100, 1),
             "mistake": "Divide useful energy by input energy — not the other way round.", "working": part2_working},
            {"value": round(E_useful / E_total, 4),
             "mistake": "Multiply by 100% — efficiency is a percentage, not a decimal.",  "working": part2_working},
            {"value": waste_eff if waste_eff != eff else eff + 5,
             "mistake": "This is the percentage of energy wasted, not the efficiency.",   "working": part2_working},
        ],
        working=part2_working,
        notes=_NOTES_COMBINED,
    )

    return PhysicsQuestion(
        question_text="",
        correct_answer=0,
        unit="",
        topic="Electricity and Energy",
        question_type="Power and Efficiency",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part1, part2],
    )
