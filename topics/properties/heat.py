import random
from utils.make_question import make_question
from utils.notes import NOTES
from core.models.question_model import PhysicsQuestion

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


_SHC_GENS    = [gen_shc_find_q, gen_shc_find_m, gen_shc_find_dt]
_LATENT_GENS = [gen_latent_find_q, gen_latent_find_m]
_ALL_GENS    = _SHC_GENS + _LATENT_GENS


def generate_heat_shc(level="N5"):
    return random.choice(_SHC_GENS)(level=level)


def generate_heat_latent(level="N5"):
    return random.choice(_LATENT_GENS)(level=level)


def generate_heat(level="N5"):
    return random.choice(_ALL_GENS)(level=level)


def generate_heat_exam_icemachine(level="N5"):
    display_val, unit_str, mass_kg, is_grams, mass_g = _pick_mass()
    mass_text = f"{display_val} {unit_str}"
    T1 = random.choice(range(10, 61, 5))
    P  = random.choice([60, 80, 100, 120, 150, 200])

    max_ice_g  = min(mass_g, 500)
    ice_mass_g = random.choice(range(50, max_ice_g + 50, 50))
    ice_mass_kg = ice_mass_g / 1000

    Q_shc      = _shc_q(mass_g, T1)
    t_correct  = round_sf(Q_shc / P)
    Q_latent_b = _latent_q(ice_mass_g, L_FUSION)

    context = (
        f"An ice-making machine is filled with {mass_text} of water at {T1} °C. "
        f"The machine first cools the water to 0 °C, then freezes it to form ice cubes.\n\n"
        f"{GIVEN_DATA}"
    )

    # ── Part (i): SHC — find energy ──────────────────────────────────────────
    shc_working = [
        {"type": "text",  "content": "Find the temperature change:"},
        {"type": "latex", "content": rf"\Delta T = {T1} - 0 = {T1}\ \mathrm{{°C}}"},
        {"type": "text",  "content": "Use the equation:"},
        {"type": "latex", "content": r"E_H = mc\Delta T"},
        {"type": "latex", "content": rf"E_H = {mass_kg} \times {C_WATER} \times {T1}"},
        {"type": "latex", "content": rf"E_H = {Q_shc:,}\ \mathrm{{J}}"},
    ]
    opts_i = [
        {"value": float(Q_shc),
         "display": fmt_J(Q_shc), "summary": "Correct!", "mistake": None, "working": shc_working},
        {"value": round_sf(Q_shc / 1000),
         "display": fmt_J(round_sf(Q_shc / 1000)), "summary": "Incorrect.",
         "mistake": "Use c = 4200 J/kg °C, not 4·2 kJ/kg °C. Keep all values in base SI units.", "working": shc_working},
        {"value": float(Q_latent_b),
         "display": fmt_J(Q_latent_b), "summary": "Incorrect.",
         "mistake": "The water is changing temperature, not state. Use E_H = mcΔT, not E_H = mL.", "working": shc_working},
    ]
    if is_grams:
        v_g = _shc_q(mass_g * 1000, T1)
        opts_i.append({"value": float(v_g), "display": fmt_J(v_g), "summary": "Incorrect.",
                       "mistake": f"You substituted {display_val} without converting to kg. {display_val} g = {mass_kg} kg.",
                       "working": shc_working})
    else:
        opts_i.append({"value": float(_shc_q(mass_g, T1 + 5)),
                       "display": fmt_J(_shc_q(mass_g, T1 + 5)), "summary": "Incorrect.",
                       "mistake": f"ΔT = {T1} − 0 = {T1} °C (the water cools to 0 °C, not below).", "working": shc_working})

    part_i = make_question(
        "Calculate the energy removed from the water to reduce its temperature to 0 °C.",
        float(Q_shc), opts_i, "J",
        notes=NOTES["heat_shc"], topic="Properties", question_type="Heat", level=level,
    )

    # ── Part (ii): P = E/t — find time ───────────────────────────────────────
    t_kj_err  = round_sf((Q_shc / 1000) / P)
    t_inv     = round_sf(P / Q_shc)
    t_product = round_sf(P * Q_shc)

    power_working = [
        {"type": "text",  "content": "Use the power equation:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
        {"type": "text",  "content": "Rearrange for time:"},
        {"type": "latex", "content": r"t = \frac{E}{P}"},
        {"type": "latex", "content": rf"t = \frac{{{Q_shc:,}}}{{{P}}}"},
        {"type": "latex", "content": rf"t = {t_correct}\ \mathrm{{s}}"},
    ]
    opts_ii = [
        {"value": float(t_correct), "display": f"{t_correct} s", "summary": "Correct!", "mistake": None, "working": power_working},
        {"value": float(t_kj_err),  "display": f"{t_kj_err} s",  "summary": "Incorrect.",
         "mistake": f"Use energy in joules ({Q_shc:,} J), not kilojoules. t = E ÷ P.", "working": power_working},
        {"value": float(t_inv),     "display": f"{t_inv} s",     "summary": "Incorrect.",
         "mistake": "You divided P by E instead of E by P. Rearranging P = E/t gives t = E ÷ P.", "working": power_working},
        {"value": float(t_product), "display": f"{t_product} s", "summary": "Incorrect.",
         "mistake": "You multiplied E × P instead of dividing. t = E ÷ P.", "working": power_working},
    ]

    part_ii = make_question(
        f"The cooling system has a power of {P} W. "
        f"Calculate the minimum time taken to reduce the temperature of the water to 0 °C.",
        float(t_correct), opts_ii, "s",
        notes=NOTES["electricity_power_energy"], topic="Properties", question_type="Heat", level=level,
    )

    # ── Part (iii): Explain ───────────────────────────────────────────────────
    part_iii = PhysicsQuestion(
        question_text=(
            "In practice, the time taken to reduce the temperature of the water to 0 °C "
            "is much greater than the minimum time calculated above. "
            "Explain why."
        ),
        correct_answer=0.0,
        unit="",
        topic="Properties",
        question_type="Heat",
        level=level,
        metadata={
            "type": "explain",
            "explain_text": (
                "Heat energy is transferred from the warmer surroundings **into** the water. "
                "The cooling system must remove this additional heat energy as well as the "
                "heat from the water itself, so the total energy to be removed is greater "
                "than calculated. This means more time is needed."
            ),
        },
    )

    # ── Part (iv): Latent heat — find mass ───────────────────────────────────
    wrong_L_m    = round_sf(Q_latent_b / L_VAPORISATION)
    wrong_E_m    = round_sf(Q_shc / L_FUSION)
    grams_answer = float(ice_mass_g)

    latent_working = [
        {"type": "text",  "content": "Rearrange E_H = mL for mass:"},
        {"type": "latex", "content": r"m = \frac{E_H}{L}"},
        {"type": "latex", "content": rf"m = \frac{{{Q_latent_b:,}}}{{{L_FUSION:,}}}"},
        {"type": "latex", "content": rf"m = {ice_mass_kg}\ \mathrm{{kg}}"},
    ]
    opts_iv = [
        {"value": float(ice_mass_kg), "display": f"{ice_mass_kg} kg", "summary": "Correct!", "mistake": None, "working": latent_working},
        {"value": float(wrong_L_m),   "display": f"{wrong_L_m} kg",   "summary": "Incorrect.",
         "mistake": "You used the specific latent heat of vaporisation. The water is freezing, so use L_fusion = 334 000 J/kg.", "working": latent_working},
        {"value": float(wrong_E_m),   "display": f"{wrong_E_m} kg",   "summary": "Incorrect.",
         "mistake": "You used the energy from part (i) instead of the energy given in this part.", "working": latent_working},
        {"value": grams_answer,       "display": f"{ice_mass_g} kg",  "summary": "Incorrect.",
         "mistake": "Your answer is in grams, not kilograms. m = E_H ÷ L gives mass in kg.", "working": latent_working},
    ]

    part_iv = make_question(
        f"Once the water is at 0 °C, a further {fmt_J(Q_latent_b)} of energy is removed. "
        f"Calculate the maximum mass of ice produced.",
        float(ice_mass_kg), opts_iv, "kg",
        notes=NOTES["heat_shc"], topic="Properties", question_type="Heat", level=level,
    )

    return PhysicsQuestion(
        question_text=f"An ice-making machine is filled with {mass_text} of water at {T1} °C.",
        correct_answer=0.0,
        unit="",
        topic="Properties",
        question_type="Heat",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part_i, part_ii, part_iii, part_iv],
    )


def generate_heat_exam(level="N5"):
    display_val, unit_str, mass_kg, is_grams, mass_g = _pick_mass()
    mass_text = f"{display_val} {unit_str}"

    scenario_type = random.choice(["vaporise", "freeze"])

    if scenario_type == "vaporise":
        T1 = random.choice(range(10, 91, 10))
        T2 = 100
        dt = T2 - T1
        L = L_VAPORISATION
        L_name = "specific latent heat of vaporisation"
        L_alt = L_FUSION
        L_alt_name = "specific latent heat of fusion"
        direction = "heated"
        direction_verb = "heat"
        phase_verb = "completely vaporised"
    else:
        T1 = random.choice(range(10, 91, 10))
        T2 = 0
        dt = T1
        L = L_FUSION
        L_name = "specific latent heat of fusion"
        L_alt = L_VAPORISATION
        L_alt_name = "specific latent heat of vaporisation"
        direction = "cooled"
        direction_verb = "cool"
        phase_verb = "completely frozen"

    Q_shc    = _shc_q(mass_g, dt)
    Q_latent = _latent_q(mass_g, L)

    context = (
        f"A mass of {mass_text} of water is {direction} from {T1} °C to {T2} °C, "
        f"then {phase_verb}.\n\n"
        f"{GIVEN_DATA}"
    )

    # --- Part (a): SHC ---
    shc_working = [
        {"type": "text",  "content": "Find the temperature change:"},
        {"type": "latex", "content": rf"\Delta T = |{T2} - {T1}| = {dt}\ \mathrm{{°C}}"},
        {"type": "text",  "content": "Then use:"},
        {"type": "latex", "content": r"E_H = mc\Delta T"},
        {"type": "latex", "content": rf"E_H = {mass_kg} \times {C_WATER} \times {dt}"},
        {"type": "latex", "content": rf"E_H = {Q_shc:,}\ \mathrm{{J}}"},
    ]
    wrong_T = _shc_q(mass_g, T2) if T2 != 0 else _shc_q(mass_g, T1)
    opts_a = [
        {"value": float(Q_shc),            "display": fmt_J(Q_shc),            "summary": "Correct!",    "mistake": None, "working": shc_working},
        {"value": float(wrong_T),           "display": fmt_J(wrong_T),           "summary": "Incorrect.", "mistake": f"You used a temperature directly instead of the change. ΔT = |{T2} − {T1}| = {dt} °C.", "working": shc_working},
        {"value": round_sf(Q_shc / 1000),  "display": fmt_J(round_sf(Q_shc / 1000)),  "summary": "Incorrect.", "mistake": "You divided c by 1000 before substituting. Use c = 4200 J/kg °C directly.", "working": shc_working},
    ]
    if is_grams:
        v_g = _shc_q(mass_g * 1000, dt)
        opts_a.append({"value": float(v_g), "display": fmt_J(v_g), "summary": "Incorrect.", "mistake": f"You substituted {display_val} without converting to kg. {display_val} g = {mass_kg} kg.", "working": shc_working})
    else:
        opts_a.append({"value": float(Q_shc + Q_latent), "display": fmt_J(Q_shc + Q_latent), "summary": "Incorrect.", "mistake": "This is the total energy. Part (a) asks only for the heating stage.", "working": shc_working})

    part_a = make_question(
        f"Calculate the energy transferred to {direction_verb} the water from {T1} °C to {T2} °C.",
        float(Q_shc), opts_a, "J",
        notes=NOTES["heat_shc"], topic="Properties", question_type="Heat", level=level,
    )

    # --- Part (b): Latent heat ---
    latent_working = [
        {"type": "text",  "content": "Use the latent heat equation:"},
        {"type": "latex", "content": r"E_H = mL"},
        {"type": "latex", "content": rf"E_H = {mass_kg} \times {L:,}\ \mathrm{{J/kg}}"},
        {"type": "latex", "content": rf"E_H = {Q_latent:,}\ \mathrm{{J}}"},
    ]
    opts_b = [
        {"value": float(Q_latent),                    "display": fmt_J(Q_latent),                    "summary": "Correct!",    "mistake": None, "working": latent_working},
        {"value": float(_latent_q(mass_g, L_alt)),    "display": fmt_J(_latent_q(mass_g, L_alt)),    "summary": "Incorrect.", "mistake": f"You used the {L_alt_name} instead of the {L_name}. Check which change of state is happening.", "working": latent_working},
        {"value": round_sf(Q_latent / 1000),          "display": fmt_J(round_sf(Q_latent / 1000)),   "summary": "Incorrect.", "mistake": "You divided L by 1000 before substituting. Use the value directly.", "working": latent_working},
        {"value": float(Q_shc + Q_latent),            "display": fmt_J(Q_shc + Q_latent),            "summary": "Incorrect.", "mistake": "This is the total energy. Part (b) asks only for the phase change.", "working": latent_working},
    ]

    part_b = make_question(
        f"Calculate the energy transferred when the water is {phase_verb}.",
        float(Q_latent), opts_b, "J",
        notes=NOTES["heat_shc"], topic="Properties", question_type="Heat", level=level,
    )

    return PhysicsQuestion(
        question_text=(
            f"A mass of {mass_text} of water is {direction} from {T1} °C to {T2} °C, "
            f"then {phase_verb}."
        ),
        correct_answer=0.0,
        unit="",
        topic="Properties",
        question_type="Heat",
        level=level,
        is_scenario=True,
        scenario_context=context,
        parts=[part_a, part_b],
    )
