import random
from utils.make_question import make_question
from utils.notes import NOTES

SUPPLY_V = 5.0


def _gen_r_kohm():
    return random.randint(1, 10) * 0.5


def _gen_r_ohm():
    return random.randint(5, 50) * 10


def _gen_v():
    return round(random.randint(1, 17) * 0.5, 1)


# ── Transistor-style potential divider (fixed 5 V supply) ───────────────────

def gen_transistor_supply_given(level="N5"):
    while True:
        r_fixed = _gen_r_kohm()
        r_var   = _gen_r_kohm()
        r_total = r_fixed + r_var
        current = round(SUPPLY_V / r_total, 3)   # mA (V ÷ kΩ)
        target  = random.choice(["fixed", "variable"])
        r_used  = r_fixed if target == "fixed" else r_var
        r_other = r_var   if target == "fixed" else r_fixed
        name    = "fixed resistor" if target == "fixed" else "variable resistor"
        correct = round(current * r_used, 2)      # mA × kΩ = V
        v_other = round(current * r_other, 2)
        if correct > 0 and v_other > 0:
            break

    working = [
        {"type": "text",  "content": "Step 1: find the current using Ohm's Law."},
        {"type": "latex", "content": r"I = \frac{V}{R}"},
        {"type": "latex", "content": rf"I = \frac{{{SUPPLY_V}}}{{{r_total}}}\ \mathrm{{kΩ}} = {current}\ \mathrm{{mA}}"},
        {"type": "text",  "content": f"Step 2: find the voltage across the {name}."},
        {"type": "latex", "content": r"V = IR"},
        {"type": "latex", "content": rf"V = {current}\ \mathrm{{mA}} \times {r_used}\ \mathrm{{kΩ}} = {correct}\ \mathrm{{V}}"},
    ]
    scaffold = [
        {"question": "Calculate the current in the circuit.", "answer": float(current), "unit": "mA"},
        {"question": f"Calculate the voltage across the {name}.", "answer": float(correct), "unit": "V"},
    ]
    question = (
        f"A transistor switching circuit has two resistors in series connected to a {SUPPLY_V} V supply:\n\n"
        f"- Fixed resistor = {r_fixed} kΩ\n"
        f"- Variable resistor = {r_var} kΩ\n\n"
        f"Calculate the voltage across the {name}."
    )
    options_data = [
        {"value": float(correct),  "display": f"{correct} V",  "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(v_other),  "display": f"{v_other} V",  "summary": "Incorrect.", "mistake": f"You found the voltage across the other resistor. The {name} has resistance {r_used} kΩ.", "working": working},
        {"value": SUPPLY_V,        "display": f"{SUPPLY_V} V", "summary": "Incorrect.", "mistake": "This is the supply voltage. The voltage is shared across the resistors in proportion to their resistance.", "working": working},
        {"value": float(current),  "display": f"{current} mA", "summary": "Incorrect.", "mistake": "You gave the current in the circuit, not the voltage. Use V = IR to find the voltage.", "working": working},
    ]
    return make_question(question, float(correct), options_data, "V", scaffold=scaffold,
                         notes=NOTES["electricity_current"], topic="Electricity", question_type="Circuits", level=level)


def gen_transistor_partial_voltage(level="N5"):
    while True:
        r_fixed = _gen_r_kohm()
        r_var   = _gen_r_kohm()
        r_total = r_fixed + r_var
        current = round(SUPPLY_V / r_total, 3)
        v_fixed = round(current * r_fixed, 2)
        v_var   = round(current * r_var, 2)
        given   = random.choice(["fixed", "variable"])
        if given == "fixed":
            given_v, given_name = v_fixed, "fixed resistor"
            correct, target_name = v_var, "variable resistor"
            r_target = r_var
        else:
            given_v, given_name = v_var, "variable resistor"
            correct, target_name = v_fixed, "fixed resistor"
            r_target = r_fixed
        if correct > 0 and given_v > 0:
            break

    working = [
        {"type": "text",  "content": "The current is the same through both series resistors."},
        {"type": "latex", "content": rf"I = \frac{{V_{{\mathrm{{given}}}}}}{{R_{{\mathrm{{given}}}}}} = \frac{{{given_v}}}{{{r_fixed if given == 'fixed' else r_var}}} = {current}\ \mathrm{{mA}}"},
        {"type": "latex", "content": r"V = IR"},
        {"type": "latex", "content": rf"V = {current} \times {r_target} = {correct}\ \mathrm{{V}}"},
    ]
    scaffold = [
        {"question": "Calculate the current using the given voltage and resistor.", "answer": float(current), "unit": "mA"},
        {"question": f"Calculate the voltage across the {target_name}.", "answer": float(correct), "unit": "V"},
    ]
    question = (
        f"A transistor circuit has two resistors in series:\n\n"
        f"- Fixed resistor = {r_fixed} kΩ\n"
        f"- Variable resistor = {r_var} kΩ\n\n"
        f"The voltage across the {given_name} is {given_v} V.\n\n"
        f"Calculate the voltage across the {target_name}."
    )
    v_sum = round(given_v + correct, 2)
    options_data = [
        {"value": float(correct),  "display": f"{correct} V",    "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(given_v),  "display": f"{given_v} V",    "summary": "Incorrect.", "mistake": f"You gave the voltage across the {given_name}. Find the current first, then use V = IR for the {target_name}.", "working": working},
        {"value": float(v_sum),    "display": f"{v_sum} V",      "summary": "Incorrect.", "mistake": "You added the two voltages. The voltages share the supply — they don't add beyond it.", "working": working},
        {"value": SUPPLY_V,        "display": f"{SUPPLY_V} V",   "summary": "Incorrect.", "mistake": "This is the supply voltage. Find the current using V=IR, then use it to find the voltage across the target resistor.", "working": working},
    ]
    return make_question(question, float(correct), options_data, "V", scaffold=scaffold,
                         notes=NOTES["electricity_current"], topic="Electricity", question_type="Circuits", level=level)


# ── Complex circuit (R2 ∥ R3 in series with R1) ─────────────────────────────

def _parallel_eq(r2, r3):
    return (r2 * r3) / (r2 + r3)


def gen_complex_supply_given(level="N5"):
    for _ in range(200):
        r1 = _gen_r_ohm()
        r2 = _gen_r_ohm()
        r3 = _gen_r_ohm()
        vp = _gen_v()
        req = _parallel_eq(r2, r3)
        i_total = vp / req
        v1 = round(i_total * r1, 2)
        v_total = round(vp + v1, 2)
        if 0 < v_total <= 9 and v1 > 0 and round(v1, 0) != round(vp, 0):
            i_total = round(i_total, 3)
            target = random.choice(["R1", "parallel"])
            correct = v1 if target == "R1" else vp
            break
    else:
        r1, r2, r3 = 200, 300, 300
        vp, v1 = 3.0, 2.0
        v_total = 5.0
        i_total = 0.02
        target, correct = "R1", v1

    working = [
        {"type": "text",  "content": "The parallel combination (R2 ∥ R3) has voltage V_P across it."},
        {"type": "latex", "content": rf"I = \frac{{V_P}}{{R_{{eq}}}} = \frac{{{vp}}}{{{round(_parallel_eq(r2,r3),1)}}} = {i_total}\ \mathrm{{A}}"},
        {"type": "latex", "content": r"V_{R1} = IR_1"},
        {"type": "latex", "content": rf"V_{{R1}} = {i_total} \times {r1} = {v1}\ \mathrm{{V}}"},
        {"type": "text",  "content": "In a series circuit: V_supply = V_R1 + V_parallel"},
        {"type": "latex", "content": rf"V_{{supply}} = {v1} + {vp} = {v_total}\ \mathrm{{V}}"},
    ]
    scaffold = [
        {"question": "Calculate the total current in the circuit.", "answer": float(i_total), "unit": "A"},
        {"question": f"Calculate the voltage across {'R1' if target == 'R1' else 'the parallel combination'}.", "answer": float(correct), "unit": "V"},
    ]
    question = (
        f"A circuit has R2 and R3 in parallel, connected in series with R1:\n\n"
        f"- R1 = {r1} Ω\n"
        f"- R2 = {r2} Ω\n"
        f"- R3 = {r3} Ω\n"
        f"- Supply voltage = {v_total} V\n\n"
        f"Calculate the voltage across {'R1' if target == 'R1' else 'the parallel combination (R2 and R3)'}."
    )
    wrong = vp if target == "R1" else v1
    options_data = [
        {"value": float(correct),  "display": f"{correct} V",   "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(wrong),    "display": f"{wrong} V",     "summary": "Incorrect.", "mistake": "You found the voltage across the other part of the circuit. Remember V_supply = V_R1 + V_parallel.", "working": working},
        {"value": float(v_total),  "display": f"{v_total} V",   "summary": "Incorrect.", "mistake": "This is the full supply voltage. Find the total current first, then use V = IR for the component.", "working": working},
        {"value": float(i_total),  "display": f"{i_total} A",   "summary": "Incorrect.", "mistake": "You gave the current, not the voltage. Use V = IR to find the voltage across the resistor.", "working": working},
    ]
    return make_question(question, float(correct), options_data, "V", scaffold=scaffold,
                         notes=NOTES["electricity_current"], topic="Electricity", question_type="Circuits", level=level)


def gen_complex_partial_voltage(level="N5"):
    for _ in range(200):
        r1 = _gen_r_ohm()
        r2 = _gen_r_ohm()
        r3 = _gen_r_ohm()
        vp = _gen_v()
        req = _parallel_eq(r2, r3)
        i_total = vp / req
        v1 = round(i_total * r1, 2)
        if 0 < v1 <= 9 and round(v1, 1) != round(vp, 1):
            i_total = round(i_total, 3)
            break
    else:
        r1, r2, r3 = 200, 300, 300
        vp, v1, i_total = 3.0, 2.0, 0.02

    working = [
        {"type": "text",  "content": "Find the total current using the voltage across the parallel combination."},
        {"type": "latex", "content": r"I = \frac{V_P}{R_{eq}}"},
        {"type": "latex", "content": rf"I = \frac{{{vp}}}{{{round(_parallel_eq(r2,r3),1)}}} = {i_total}\ \mathrm{{A}}"},
        {"type": "text",  "content": "Apply Ohm's Law to R1:"},
        {"type": "latex", "content": r"V_{R1} = IR_1"},
        {"type": "latex", "content": rf"V_{{R1}} = {i_total} \times {r1} = {v1}\ \mathrm{{V}}"},
    ]
    scaffold = [
        {"question": "Calculate the total current in the circuit.", "answer": float(i_total), "unit": "A"},
        {"question": "Calculate the voltage across R1.", "answer": float(v1), "unit": "V"},
    ]
    question = (
        f"A circuit has R2 and R3 in parallel, connected in series with R1:\n\n"
        f"- R1 = {r1} Ω\n"
        f"- R2 = {r2} Ω\n"
        f"- R3 = {r3} Ω\n\n"
        f"The voltage across the parallel combination (R2 and R3) is {vp} V.\n\n"
        f"Calculate the voltage across R1."
    )
    v_total = round(vp + v1, 2)
    options_data = [
        {"value": float(v1),      "display": f"{v1} V",      "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(vp),      "display": f"{vp} V",      "summary": "Incorrect.", "mistake": "This is the voltage across the parallel combination, not R1. Find the current first using I = V_P ÷ R_eq, then V_R1 = I × R1.", "working": working},
        {"value": float(v_total), "display": f"{v_total} V", "summary": "Incorrect.", "mistake": "You added the voltages together. This would be the supply voltage, not the voltage across R1.", "working": working},
        {"value": float(i_total), "display": f"{i_total} A", "summary": "Incorrect.", "mistake": "You gave the current value, not the voltage. Use V = IR to find the voltage across R1.", "working": working},
    ]
    return make_question(question, float(v1), options_data, "V", scaffold=scaffold,
                         notes=NOTES["electricity_current"], topic="Electricity", question_type="Circuits", level=level)


_ALL_GENS = [gen_transistor_supply_given, gen_transistor_partial_voltage,
             gen_complex_supply_given, gen_complex_partial_voltage]


def generate_circuits(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
