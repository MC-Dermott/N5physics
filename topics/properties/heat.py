import random
from utils.make_question import make_question
from utils.notes import NOTES

L_VAPORISATION = 2_260_000
L_FUSION       = 334_000
C_WATER        = 4200

GIVEN_DATA = (
    "| Property | Value |\n"
    "|---|---|\n"
    "| Specific latent heat of fusion of water | 334 000 J/kg |\n"
    "| Specific latent heat of vaporisation of water | 2 260 000 J/kg |\n"
    "| Specific heat capacity of water | 4200 J/kg °C |"
)

LATENT_SITUATIONS = {
    "water_to_steam": {
        "template": "A mass of {mass} of water is completely vaporised at 100 °C.",
        "desc":     "Water is completely vaporised at 100 °C.",
        "L": L_VAPORISATION, "L_alt": L_FUSION,
        "L_name": "specific latent heat of vaporisation",
        "L_alt_name": "specific latent heat of fusion",
    },
    "steam_to_water": {
        "template": "A mass of {mass} of steam is completely condensed to water at 100 °C.",
        "desc":     "Steam is completely condensed to water at 100 °C.",
        "L": L_VAPORISATION, "L_alt": L_FUSION,
        "L_name": "specific latent heat of vaporisation",
        "L_alt_name": "specific latent heat of fusion",
    },
    "ice_to_water": {
        "template": "A mass of {mass} of ice is completely melted at 0 °C.",
        "desc":     "Ice is completely melted at 0 °C.",
        "L": L_FUSION, "L_alt": L_VAPORISATION,
        "L_name": "specific latent heat of fusion",
        "L_alt_name": "specific latent heat of vaporisation",
    },
    "water_to_ice": {
        "template": "A mass of {mass} of water is completely frozen at 0 °C.",
        "desc":     "Water is completely frozen at 0 °C.",
        "L": L_FUSION, "L_alt": L_VAPORISATION,
        "L_name": "specific latent heat of fusion",
        "L_alt_name": "specific latent heat of vaporisation",
    },
}

_SITUATION_KEYS = list(LATENT_SITUATIONS.keys())


def fmt_J(j):
    j = float(j)
    if abs(j) >= 1_000_000:
        return f"{j / 1_000_000:g} MJ"
    if abs(j) >= 1000:
        return f"{j / 1000:g} kJ"
    return f"{j:g} J"


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def _pick_mass():
    mass_g = random.choice(range(100, 3100, 100))
    mass_kg = mass_g / 1000
    if mass_g < 1000:
        return mass_g, "g", mass_kg, True, mass_g
    return mass_kg, "kg", mass_kg, False, mass_g


def _latent_q(mass_g, L):
    return mass_g * L // 1000


def _shc_q(mass_g, dt):
    return mass_g * C_WATER * dt // 1000


def gen_latent_find_q(level="N5"):
    cfg = LATENT_SITUATIONS[random.choice(_SITUATION_KEYS)]
    L, L_alt = cfg["L"], cfg["L_alt"]

    display_val, unit, mass_kg, is_grams, mass_g = _pick_mass()
    mass_text = f"{display_val} {unit}"

    correct_Q = _latent_q(mass_g, L)
    wrong_L_Q = _latent_q(mass_g, L_alt)
    kj_err_Q  = round_sf(correct_Q / 1000)
    both_L_Q  = _latent_q(mass_g, L + L_alt)

    working = [
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"E_H = mL"},
        {"type": "latex", "content": rf"E_H = {mass_kg} \times {L:,}\ \mathrm{{J/kg}}"},
        {"type": "latex", "content": rf"E_H = {correct_Q:,}\ \mathrm{{J}}"},
    ]
    question = (
        f"{cfg['template'].format(mass=mass_text)}\n\n"
        f"{GIVEN_DATA}\n\n"
        f"Calculate the energy transferred."
    )

    if is_grams:
        grams_Q = _latent_q(mass_g * 1000, L)
        options_data = [
            {"value": float(correct_Q), "display": fmt_J(correct_Q), "summary": "Correct!", "mistake": None, "working": working},
            {"value": float(wrong_L_Q), "display": fmt_J(wrong_L_Q), "summary": "Incorrect.", "mistake": f"You used the {cfg['L_alt_name']} ({L_alt:,} J/kg) instead of the {cfg['L_name']} ({L:,} J/kg). Check which change of state is happening.", "working": working},
            {"value": float(grams_Q),   "display": fmt_J(grams_Q),   "summary": "Incorrect.", "mistake": f"You substituted {display_val} without converting to kg. {display_val} g = {mass_kg} kg.", "working": working},
            {"value": float(kj_err_Q),  "display": fmt_J(kj_err_Q),  "summary": "Incorrect.", "mistake": f"You divided the latent heat by 1000 before substituting. Use the value directly: L = {L:,} J/kg.", "working": working},
        ]
    else:
        options_data = [
            {"value": float(correct_Q), "display": fmt_J(correct_Q), "summary": "Correct!", "mistake": None, "working": working},
            {"value": float(wrong_L_Q), "display": fmt_J(wrong_L_Q), "summary": "Incorrect.", "mistake": f"You used the {cfg['L_alt_name']} ({L_alt:,} J/kg) instead of the {cfg['L_name']} ({L:,} J/kg). Check which change of state is happening.", "working": working},
            {"value": float(kj_err_Q),  "display": fmt_J(kj_err_Q),  "summary": "Incorrect.", "mistake": f"You divided the latent heat by 1000 before substituting. Use the value directly: L = {L:,} J/kg.", "working": working},
            {"value": float(both_L_Q),  "display": fmt_J(both_L_Q),  "summary": "Incorrect.", "mistake": f"You added both latent heat values together. Only the {cfg['L_name']} applies to this change of state.", "working": working},
        ]
    return make_question(question, float(correct_Q), options_data, "J",
                         notes=NOTES["heat_shc"], topic="Properties", question_type="Heat", level=level)


def gen_latent_find_m(level="N5"):
    cfg = LATENT_SITUATIONS[random.choice(_SITUATION_KEYS)]
    L, L_alt = cfg["L"], cfg["L_alt"]

    _, _, seed_mass, _, seed_mass_g = _pick_mass()
    Q = _latent_q(seed_mass_g, L)
    correct_m = seed_mass

    wrong_L_m   = round_sf(Q / L_alt)
    grams_answer = round_sf(correct_m * 1000)
    both_L_m    = round_sf(Q / (L + L_alt))

    working = [
        {"type": "text",  "content": "Rearrange E_H = mL to find m:"},
        {"type": "latex", "content": r"m = \frac{E_H}{L}"},
        {"type": "latex", "content": rf"m = \frac{{{Q:,}}}{{{L:,}}}"},
        {"type": "latex", "content": rf"m = {correct_m}\ \mathrm{{kg}}"},
    ]
    question = (
        f"{cfg['desc']}\n\n"
        f"Energy transferred = {fmt_J(Q)}\n\n"
        f"{GIVEN_DATA}\n\n"
        f"Calculate the mass."
    )
    options_data = [
        {"value": float(correct_m), "display": f"{correct_m} kg",     "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(wrong_L_m), "display": f"{wrong_L_m} kg",     "summary": "Incorrect.", "mistake": f"You used the {cfg['L_alt_name']} ({L_alt:,} J/kg) instead of the {cfg['L_name']} ({L:,} J/kg).", "working": working},
        {"value": float(grams_answer), "display": f"{grams_answer} kg", "summary": "Incorrect.", "mistake": "Your answer is in grams, not kilograms. The equation E_H = mL gives mass in kg.", "working": working},
        {"value": float(both_L_m), "display": f"{both_L_m} kg",      "summary": "Incorrect.", "mistake": f"You divided E_H by the sum of both latent heat values. Only the {cfg['L_name']} applies here.", "working": working},
    ]
    return make_question(question, float(correct_m), options_data, "kg",
                         notes=NOTES["heat_shc"], topic="Properties", question_type="Heat", level=level)


def gen_shc_find_q(level="N5"):
    display_val, unit, mass_kg, is_grams, mass_g = _pick_mass()
    mass_text = f"{display_val} {unit}"

    t_values = list(range(5, 101, 5))
    T1 = random.choice(t_values[:-2])
    T2 = random.choice([t for t in t_values if t > T1])
    dt = T2 - T1
    correct_Q = _shc_q(mass_g, dt)

    working = [
        {"type": "text",  "content": "First find the temperature change:"},
        {"type": "latex", "content": rf"\Delta T = {T2} - {T1} = {dt}\ \mathrm{{°C}}"},
        {"type": "text",  "content": "Then use the equation:"},
        {"type": "latex", "content": r"E_H = mc\Delta T"},
        {"type": "latex", "content": rf"E_H = {mass_kg} \times {C_WATER}\ \mathrm{{J/kg\ °C}} \times {dt}"},
        {"type": "latex", "content": rf"E_H = {correct_Q:,}\ \mathrm{{J}}"},
    ]
    scaffold = [
        {"question": f"Calculate the temperature change ΔT.", "answer": float(dt), "unit": "°C"},
        {"question": "Calculate the energy transferred.", "answer": float(correct_Q), "unit": "J"},
    ]
    question = (
        f"Water of mass {mass_text} is heated from {T1} °C to {T2} °C.\n\n"
        f"{GIVEN_DATA}\n\n"
        f"Calculate the energy transferred."
    )

    v_T2 = _shc_q(mass_g, T2)
    v_T1 = _shc_q(mass_g, T1)

    options_data = [
        {"value": float(correct_Q), "display": fmt_J(correct_Q), "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(v_T2), "display": fmt_J(v_T2), "summary": "Incorrect.", "mistake": f"You used T₂ = {T2} °C directly instead of the temperature change. ΔT = {T2} − {T1} = {dt} °C.", "working": working},
        {"value": float(v_T1), "display": fmt_J(v_T1), "summary": "Incorrect.", "mistake": f"You used T₁ = {T1} °C directly instead of the temperature change. ΔT = {T2} − {T1} = {dt} °C.", "working": working},
    ]
    if is_grams:
        v_g = _shc_q(mass_g * 1000, dt)
        options_data.append({"value": float(v_g), "display": fmt_J(v_g), "summary": "Incorrect.", "mistake": f"You substituted {display_val} without converting to kg. {display_val} g = {mass_kg} kg.", "working": working})
    else:
        v_sum = _shc_q(mass_g, T1 + T2)
        options_data.append({"value": float(v_sum), "display": fmt_J(v_sum), "summary": "Incorrect.", "mistake": f"You added T₁ and T₂ instead of subtracting. ΔT = {T2} − {T1} = {dt} °C, not {T1} + {T2} = {T1 + T2} °C.", "working": working})

    return make_question(question, float(correct_Q), options_data, "J", scaffold=scaffold,
                         notes=NOTES["heat_shc"], topic="Properties", question_type="Heat", level=level)


def gen_shc_find_m(level="N5"):
    display_val, unit, mass_kg, is_grams, mass_g = _pick_mass()
    dt = random.choice(range(5, 81, 5))
    Q = _shc_q(mass_g, dt)
    correct_m = mass_kg

    grams_answer  = round_sf(mass_kg * 1000)
    forgot_dt     = round_sf(Q / C_WATER)
    swap_dt_error = round_sf(Q * dt / C_WATER)

    working = [
        {"type": "text",  "content": "Rearrange E_H = mcΔT to find m:"},
        {"type": "latex", "content": r"m = \frac{E_H}{c\Delta T}"},
        {"type": "latex", "content": rf"m = \frac{{{Q:,}}}{{{C_WATER} \times {dt}}}"},
        {"type": "latex", "content": rf"m = {correct_m}\ \mathrm{{kg}}"},
    ]
    question = (
        f"Water is heated through a temperature change of {dt} °C.\n\n"
        f"Energy transferred = {fmt_J(Q)}\n\n"
        f"{GIVEN_DATA}\n\n"
        f"Calculate the mass of water."
    )
    options_data = [
        {"value": float(correct_m),   "display": f"{correct_m} kg",    "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(grams_answer), "display": f"{grams_answer} kg", "summary": "Incorrect.", "mistake": "Your answer is in grams, not kilograms. The equation E_H = mcΔT uses mass in kg.", "working": working},
        {"value": float(forgot_dt),    "display": f"{forgot_dt} kg",    "summary": "Incorrect.", "mistake": f"You divided E_H by c only, forgetting to divide by ΔT = {dt} °C. m = E_H ÷ (c × ΔT).", "working": working},
        {"value": float(swap_dt_error), "display": f"{swap_dt_error} kg", "summary": "Incorrect.", "mistake": "You multiplied by ΔT instead of dividing by it. m = E_H ÷ (c × ΔT).", "working": working},
    ]
    return make_question(question, float(correct_m), options_data, "kg",
                         notes=NOTES["heat_shc"], topic="Properties", question_type="Heat", level=level)


def gen_shc_find_dt(level="N5"):
    display_val, unit, mass_kg, is_grams, mass_g = _pick_mass()
    mass_text = f"{display_val} {unit}"
    dt = random.choice(range(5, 81, 5))
    Q = _shc_q(mass_g, dt)
    correct_dt = dt

    forgot_mass   = round_sf(Q / C_WATER)
    swap_m_error  = round_sf(Q * mass_kg / C_WATER)

    working = [
        {"type": "text",  "content": "Rearrange E_H = mcΔT to find ΔT:"},
        {"type": "latex", "content": r"\Delta T = \frac{E_H}{mc}"},
        {"type": "latex", "content": rf"\Delta T = \frac{{{Q:,}}}{{{mass_kg} \times {C_WATER}}}"},
        {"type": "latex", "content": rf"\Delta T = {correct_dt}\ \mathrm{{°C}}"},
    ]
    question = (
        f"Water of mass {mass_text} is heated.\n\n"
        f"Energy transferred = {fmt_J(Q)}\n\n"
        f"{GIVEN_DATA}\n\n"
        f"Calculate the temperature change."
    )
    options_data = [
        {"value": float(correct_dt),  "display": f"{correct_dt} °C",   "summary": "Correct!", "mistake": None, "working": working},
        {"value": float(forgot_mass),  "display": f"{forgot_mass} °C",  "summary": "Incorrect.", "mistake": "You divided E_H by c only, forgetting to divide by the mass. ΔT = E_H ÷ (m × c).", "working": working},
        {"value": float(swap_m_error), "display": f"{swap_m_error} °C", "summary": "Incorrect.", "mistake": "You multiplied by m instead of dividing. ΔT = E_H ÷ (m × c).", "working": working},
    ]
    if is_grams:
        options_data.append({
            "value": round_sf(Q / (display_val * C_WATER)),
            "display": f"{round_sf(Q / (display_val * C_WATER))} °C",
            "summary": "Incorrect.",
            "mistake": f"You substituted {display_val} without converting to kg. {display_val} g = {mass_kg} kg.",
            "working": working,
        })
    else:
        options_data.append({
            "value": round_sf(Q / (mass_kg * 1000 * C_WATER)),
            "display": f"{round_sf(Q / (mass_kg * 1000 * C_WATER))} °C",
            "summary": "Incorrect.",
            "mistake": f"You multiplied the mass by 1000 before substituting. The mass is already in kg: {mass_kg} kg.",
            "working": working,
        })
    return make_question(question, float(correct_dt), options_data, "°C",
                         notes=NOTES["heat_shc"], topic="Properties", question_type="Heat", level=level)


_ALL_GENS = [gen_latent_find_q, gen_latent_find_m, gen_shc_find_q, gen_shc_find_m, gen_shc_find_dt]


def generate_heat(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
