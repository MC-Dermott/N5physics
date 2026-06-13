import random
from utils.make_question import make_question
from utils.notes import NOTES


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def _gen_r():
    return random.randint(1, 10) * 0.5  # 0.5 to 5.0 kΩ


def _gen_v():
    return random.randint(1, 17) * 0.5  # 0.5 to 8.5 V


def _current_working(v, r_total):
    return [
        {"type": "text",  "content": "First calculate the total current using Ohm's Law:"},
        {"type": "latex", "content": r"I = \frac{V}{R}"},
        {"type": "latex", "content": rf"I = \frac{{{v}}}{{{r_total}\ \mathrm{{k\Omega}}}}"},
    ]


def _voltage_working(i, r, result):
    return [
        {"type": "text",  "content": "Now calculate the voltage across the resistor:"},
        {"type": "latex", "content": r"V = IR"},
        {"type": "latex", "content": rf"V = {round_sf(i)} \times {r}"},
        {"type": "latex", "content": rf"V = {result}\ \mathrm{{V}}"},
    ]


def gen_type1(level="N5"):
    while True:
        r1 = _gen_r()
        r2 = _gen_r()
        v_supply = _gen_v()
        r_total = r1 + r2
        current = round(v_supply / r_total, 3)  # mA (since R in kΩ)
        target = random.choice(["R1", "R2"])
        r_used = r1 if target == "R1" else r2
        correct = round(current * r_used, 2)
        other = round(current * (r_total - r_used), 2)
        if correct <= 0:
            continue

        full_working = _current_working(v_supply, r_total) + _voltage_working(current, r_used, correct)

        question = (
            f"A potential divider circuit contains two resistors in series:\n\n"
            f"- R1 = {r1} kΩ\n"
            f"- R2 = {r2} kΩ\n"
            f"- Supply voltage = {v_supply} V\n\n"
            f"Calculate the voltage across {target}."
        )
        scaffold = [
            {"question": "Calculate the current in the circuit (in mA).", "answer": current, "unit": "mA"},
            {"question": f"Calculate the voltage across {target}.", "answer": correct, "unit": "V"},
        ]
        options_data = [
            {"value": correct,     "summary": "Correct!",   "mistake": None,
             "working": full_working},
            {"value": v_supply - correct, "summary": "Incorrect.",
             "mistake": "You subtracted the supply voltage from the correct answer — use Ohm's Law to find the voltage across each resistor separately.",
             "working": full_working},
            {"value": other,       "summary": "Incorrect.",
             "mistake": f"You calculated the voltage across the other resistor. Use V = I × {target[1]}, not the other one.",
             "working": full_working},
            {"value": round(v_supply * r_used / r_total, 2), "summary": "Incorrect.",
             "mistake": "Check your current calculation: I = V_supply ÷ R_total, then V = I × R_target.",
             "working": full_working},
        ]
        return make_question(question, correct, options_data, "V", scaffold=scaffold,
                             notes=NOTES.get("potential_divider", NOTES["ohms_law"]),
                             topic="Electricity", question_type="Potential Divider", level=level)


def gen_type2(level="N5"):
    while True:
        r1 = _gen_r()
        r2 = _gen_r()
        v_supply = _gen_v()
        r_total = r1 + r2
        current = round(v_supply / r_total, 3)
        v_r1 = round(current * r1, 2)
        v_r2 = round(current * r2, 2)
        given = random.choice(["R1", "R2"])
        if given == "R1":
            given_voltage, correct, r_used = v_r1, v_r2, r2
        else:
            given_voltage, correct, r_used = v_r2, v_r1, r1
        if correct <= 0 or given_voltage <= 0:
            continue

        full_working = _current_working(v_supply, r_total) + _voltage_working(current, r_used, correct)

        question = (
            f"A potential divider circuit contains two resistors in series:\n\n"
            f"- R1 = {r1} kΩ\n"
            f"- R2 = {r2} kΩ\n\n"
            f"The voltage across {given} is {given_voltage} V.\n\n"
            f"Calculate the voltage across the other resistor."
        )
        scaffold = [
            {"question": "Calculate the total supply voltage.", "answer": v_supply, "unit": "V"},
            {"question": "Calculate the voltage across the other resistor.", "answer": correct, "unit": "V"},
        ]
        options_data = [
            {"value": correct,           "summary": "Correct!",   "mistake": None,
             "working": full_working},
            {"value": given_voltage,     "summary": "Incorrect.",
             "mistake": "The voltage across each resistor is proportional to its resistance — they aren't necessarily equal.",
             "working": full_working},
            {"value": v_supply,          "summary": "Incorrect.",
             "mistake": "This is the total supply voltage, not the voltage across the other resistor. The voltages across each resistor must add up to the supply voltage.",
             "working": full_working},
            {"value": round(v_supply - given_voltage, 2), "summary": "Incorrect.",
             "mistake": "Check your working — the voltages across the two resistors must add up to the supply voltage.",
             "working": full_working},
        ]
        # The last two are the same (v_supply - given_voltage IS correct in type2 if approached right)
        # Actually v_supply - given_voltage = correct IS correct here. Let me reconsider.
        # v_r1 + v_r2 = v_supply, so correct = v_supply - given_voltage. But my options_data[3] shows this as "Incorrect." That's wrong.
        # I need to pick a different distractor.
        # Let me fix: use wrong R in the calculation
        wrong_r_result = round(current * (r_total - r_used), 2)  # same as correct if symmetric
        # Actually, use v_supply + given_voltage as a distractor
        sum_err = round(v_supply + given_voltage, 2)
        options_data[3] = {
            "value": sum_err,
            "summary": "Incorrect.",
            "mistake": "The voltages across the two resistors add up to the supply voltage, not beyond it.",
            "working": full_working,
        }
        return make_question(question, correct, options_data, "V", scaffold=scaffold,
                             notes=NOTES.get("potential_divider", NOTES["ohms_law"]),
                             topic="Electricity", question_type="Potential Divider", level=level)


_ALL_GENS = [gen_type1, gen_type2]


def generate_potential_divider(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
