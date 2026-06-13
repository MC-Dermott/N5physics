import random
from utils.make_question import make_question
from utils.notes import NOTES

G = 9.8
G_TABLE = "| Constant | Value |\n|---|---|\n| g | 9.8 N/kg |"

CONTEXTS = {
    "bike":  {"label": "bicycle and rider", "num_wheels": 2, "mass_options": list(range(70, 141, 10)),  "area_options": [0.001, 0.002, 0.003]},
    "car":   {"label": "car",               "num_wheels": 4, "mass_options": list(range(1000, 2001, 100)), "area_options": [0.020, 0.025, 0.030, 0.040]},
    "truck": {"label": "truck",             "num_wheels": 6, "mass_options": list(range(5000, 15001, 1000)), "area_options": [0.050, 0.060, 0.070, 0.080]},
}


def fmt_N(val):
    val = float(val)
    if abs(val) >= 1000:
        return f"{val / 1000:g} kN"
    return f"{val:g} N"


def fmt_Pa(val):
    val = float(val)
    if abs(val) >= 1000:
        return f"{val / 1000:g} kPa"
    return f"{val:g} Pa"


def _pick():
    key = random.choice(list(CONTEXTS.keys()))
    ctx = CONTEXTS[key]
    mass = random.choice(ctx["mass_options"])
    area_per = random.choice(ctx["area_options"])
    n = ctx["num_wheels"]
    weight = int(round(mass * G))
    total_area = round(n * area_per, 4)
    pressure = round(weight / total_area)
    return ctx["label"], n, mass, weight, area_per, total_area, pressure


def gen_find_weight(level="N5"):
    label, n, mass, weight, area_per, total_area, pressure = _pick()
    w_div  = round(mass / G, 1)
    w_ten  = float(mass * 10)

    working = [
        {"type": "latex", "content": r"W = mg"},
        {"type": "latex", "content": rf"W = {mass} \times 9.8"},
        {"type": "latex", "content": rf"W = {fmt_N(weight)}"},
    ]
    question = f"A {label} has a total mass of {mass} kg.\n\n{G_TABLE}\n\nCalculate the weight of the {label}."
    options_data = [
        {"value": float(weight), "display": fmt_N(weight), "summary": "Correct!",   "mistake": None, "working": working},
        {"value": w_div,         "display": fmt_N(w_div),  "summary": "Incorrect.", "mistake": "You divided by g instead of multiplying. W = m × g.", "working": working},
        {"value": w_ten,         "display": fmt_N(w_ten),  "summary": "Incorrect.", "mistake": "You used g = 10 N/kg. The correct value is g = 9.8 N/kg.", "working": working},
        {"value": float(mass),   "display": fmt_N(mass),   "summary": "Incorrect.", "mistake": "You gave the mass in kg, not the weight in N. Weight = mass × g.", "working": working},
    ]
    return make_question(question, float(weight), options_data, "N", notes=NOTES["pressure"],
                         topic="Properties", question_type="Pressure", level=level)


def gen_find_pressure(level="N5"):
    label, n, mass, weight, area_per, total_area, pressure = _pick()
    p_one   = round(weight / area_per)
    p_div_n = round(pressure / n)
    p_wrong = round(weight / (total_area + area_per))

    working = [
        {"type": "text",  "content": f"Find the total contact area across all {n} tyres:"},
        {"type": "latex", "content": rf"A_{{total}} = {n} \times {area_per} = {total_area}\ \mathrm{{m^2}}"},
        {"type": "text",  "content": "Apply the pressure equation:"},
        {"type": "latex", "content": r"P = \frac{F}{A}"},
        {"type": "latex", "content": rf"P = \frac{{{fmt_N(weight)}}}{{{total_area}}}"},
        {"type": "latex", "content": rf"P = {fmt_Pa(pressure)}"},
    ]
    scaffold = [
        {"question": f"Calculate the total contact area of the {n} tyres.", "answer": total_area, "unit": "m²"},
        {"question": "Calculate the pressure.", "answer": float(pressure), "unit": "Pa"},
    ]
    question = (
        f"A {label} has a weight of {fmt_N(weight)} and {n} tyres, "
        f"each with a contact area of {area_per} m².\n\n"
        f"Calculate the pressure exerted on the ground."
    )
    options_data = [
        {"value": float(pressure), "display": fmt_Pa(pressure), "summary": "Correct!",   "mistake": None, "working": working},
        {"value": float(p_one),    "display": fmt_Pa(p_one),    "summary": "Incorrect.", "mistake": f"You used the area of one tyre. Total contact area = {n} × {area_per} = {total_area} m².", "working": working},
        {"value": float(p_div_n),  "display": fmt_Pa(p_div_n),  "summary": "Incorrect.", "mistake": f"You also divided by the number of wheels. P = F ÷ A_total, not F ÷ (A_total × n).", "working": working},
        {"value": float(p_wrong),  "display": fmt_Pa(p_wrong),  "summary": "Incorrect.", "mistake": f"Check the total contact area: {n} tyres × {area_per} m² = {total_area} m².", "working": working},
    ]
    return make_question(question, float(pressure), options_data, "Pa", scaffold=scaffold,
                         notes=NOTES["pressure"], topic="Properties", question_type="Pressure", level=level)


def gen_find_area(level="N5"):
    label, n, mass, weight, area_per, total_area, pressure = _pick()
    w_mul  = round(total_area * n, 4)
    w_add  = round(total_area + area_per, 4)

    working = [
        {"type": "latex", "content": r"A = \frac{F}{P}"},
        {"type": "latex", "content": rf"A = \frac{{{fmt_N(weight)}}}{{{fmt_Pa(pressure)}}}"},
        {"type": "latex", "content": rf"A = {total_area}\ \mathrm{{m^2}}"},
    ]
    question = (
        f"A {label} has a weight of {fmt_N(weight)} and exerts a pressure of {fmt_Pa(pressure)} on the ground.\n\n"
        f"Calculate the total contact area of the tyres on the ground."
    )
    options_data = [
        {"value": total_area, "summary": "Correct!",   "mistake": None, "working": working},
        {"value": area_per,   "summary": "Incorrect.", "mistake": f"This is the area of one tyre. Multiply by {n} to get the total: {total_area} m².", "working": working},
        {"value": w_mul,      "summary": "Incorrect.", "mistake": f"You multiplied the total area by {n} again. A = F ÷ P gives the total directly.", "working": working},
        {"value": w_add,      "summary": "Incorrect.", "mistake": f"Check the total area. A = F ÷ P = {fmt_N(weight)} ÷ {fmt_Pa(pressure)} = {total_area} m².", "working": working},
    ]
    return make_question(question, total_area, options_data, "m²", notes=NOTES["pressure"],
                         topic="Properties", question_type="Pressure", level=level)


def gen_find_force(level="N5"):
    label, n, mass, weight, area_per, total_area, pressure = _pick()
    f_one  = round(pressure * area_per, 1)
    f_x_n  = round(weight * n, 1)
    f_mass = round(weight / G)

    working = [
        {"type": "latex", "content": r"F = PA"},
        {"type": "latex", "content": rf"F = {fmt_Pa(pressure)} \times {total_area}"},
        {"type": "latex", "content": rf"F = {fmt_N(weight)}"},
    ]
    question = (
        f"A {label} exerts a pressure of {fmt_Pa(pressure)} on the ground. "
        f"The total contact area of its {n} tyres is {total_area} m².\n\n"
        f"Calculate the weight of the {label}."
    )
    options_data = [
        {"value": float(weight), "display": fmt_N(weight), "summary": "Correct!",   "mistake": None, "working": working},
        {"value": float(f_one),  "display": fmt_N(f_one),  "summary": "Incorrect.", "mistake": f"You used the area of one tyre ({area_per} m²). Use the total contact area = {total_area} m².", "working": working},
        {"value": float(f_x_n),  "display": fmt_N(f_x_n),  "summary": "Incorrect.", "mistake": f"You multiplied by {n} (the number of wheels). F = P × A_total — the total area already covers all tyres.", "working": working},
        {"value": float(f_mass), "display": f"{f_mass} kg", "summary": "Incorrect.", "mistake": "This is the mass in kg, not the weight in N. F = P × A gives the weight force.", "working": working},
    ]
    return make_question(question, float(weight), options_data, "N", notes=NOTES["pressure"],
                         topic="Properties", question_type="Pressure", level=level)


_N4_GENS  = [gen_find_weight, gen_find_pressure]
_ALL_GENS = [gen_find_weight, gen_find_pressure, gen_find_area, gen_find_force]


def generate_pressure(level="N5"):
    gens = _N4_GENS if level == "N4" else _ALL_GENS
    return random.choice(gens)(level=level)
