"""Two-step wave questions combining v = fλ and T = 1/f."""
import random
import math
from utils.make_question import make_question
from utils.notes import NOTES

V_SOUND = 340


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sci_latex(val):
    exp = int(math.floor(math.log10(abs(val))))
    m = round(val / 10 ** exp, 2)
    m = int(m) if m == int(m) else m
    return rf"{m} \times 10^{{{exp}}}"


def sci_plain(val):
    exp = int(math.floor(math.log10(abs(val))))
    m = round(val / 10 ** exp, 2)
    m = int(m) if m == int(m) else m
    return f"{m} × 10{str(exp).translate(_SUP)}"


def fmt_val(val):
    if val == 0:
        return "0"
    if 0.001 <= abs(val) < 1e6:
        return str(round_sf(val))
    return sci_plain(val)


PREFIX_POWER = {"ms": r"10^{-3}", "μs": r"10^{-6}", "ns": r"10^{-9}", "cm": r"10^{-2}", "mm": r"10^{-3}"}
PREFIX_FACTOR = {"ms": 1e-3, "μs": 1e-6, "ns": 1e-9, "s": 1, "cm": 1e-2, "mm": 1e-3, "m": 1}


def best_period(T_s):
    if T_s >= 1:
        return round_sf(T_s), "s"
    elif T_s >= 1e-3:
        return round_sf(T_s * 1e3), "ms"
    elif T_s >= 1e-6:
        return round_sf(T_s * 1e6), "μs"
    else:
        return round_sf(T_s * 1e9), "ns"


SCENARIOS = [
    {"f_Hz": 100,  "lam_m": 3.4,  "lam_disp": 3.4,  "lam_unit": "m"},
    {"f_Hz": 200,  "lam_m": 1.7,  "lam_disp": 1.7,  "lam_unit": "m"},
    {"f_Hz": 680,  "lam_m": 0.5,  "lam_disp": 0.5,  "lam_unit": "m"},
    {"f_Hz": 1000, "lam_m": 0.34, "lam_disp": 34,   "lam_unit": "cm"},
    {"f_Hz": 1700, "lam_m": 0.20, "lam_disp": 20,   "lam_unit": "cm"},
    {"f_Hz": 3400, "lam_m": 0.10, "lam_disp": 10,   "lam_unit": "cm"},
]


def make_find_v(level="N5"):
    sc = random.choice(SCENARIOS)
    f_Hz, lam_m = sc["f_Hz"], sc["lam_m"]
    lam_disp, lam_unit = sc["lam_disp"], sc["lam_unit"]
    T_s = 1 / f_Hz
    T_disp, T_unit = best_period(T_s)
    correct_v = V_SOUND

    d1 = round_sf(T_s * lam_m)
    d2 = round_sf(f_Hz * lam_disp) if lam_unit != "m" else round_sf(lam_m * V_SOUND)
    d2_mistake = (f"You did not convert λ to metres before step 2. {lam_disp} {lam_unit} = {lam_m} m." if lam_unit != "m"
                  else "Check your substitution in v = fλ.")
    d3 = round_sf(f_Hz)

    lam_m_str = str(round_sf(lam_m))
    T_s_str = sci_latex(T_s) if T_s < 1e-3 else str(round_sf(T_s))
    T_power = PREFIX_POWER.get(T_unit, "")

    steps = [{"type": "text", "content": "Step 1: find frequency from the period."},
             {"type": "latex", "content": r"f = \frac{1}{T}"}]
    if T_unit != "s":
        steps.append({"type": "latex", "content": rf"T = {T_disp} \times {T_power} = {T_s_str}\ \mathrm{{s}}"})
    steps.append({"type": "latex", "content": rf"f = \frac{{1}}{{{T_s_str}}} = {f_Hz}\ \mathrm{{Hz}}"})
    if lam_unit != "m":
        steps.append({"type": "latex", "content": rf"\lambda = {lam_disp} \times {PREFIX_POWER.get(lam_unit, '')} = {lam_m_str}\ \mathrm{{m}}"})
    steps += [
        {"type": "text",  "content": "Step 2: find wave speed."},
        {"type": "latex", "content": r"v = f\lambda"},
        {"type": "latex", "content": rf"v = {f_Hz} \times {lam_m_str}"},
        {"type": "latex", "content": rf"v = {correct_v}\ \mathrm{{m/s}}"},
    ]
    scaffold = [
        {"question": "Calculate the frequency from the period.", "answer": float(f_Hz), "unit": "Hz"},
        {"question": "Calculate the wave speed.", "answer": float(correct_v), "unit": "m/s"},
    ]

    question = f"A sound wave has a period of {T_disp} {T_unit} and a wavelength of {lam_disp} {lam_unit}.\n\nCalculate the wave speed."
    options_data = [
        {"value": correct_v, "display": f"{correct_v} m/s", "summary": "Correct!", "mistake": None, "working": steps},
        {"value": d1, "display": f"{fmt_val(d1)} m/s", "summary": "Incorrect.", "mistake": "You used T directly as f in step 2. Find f = 1/T first, then v = f × λ.", "working": steps},
        {"value": d2, "display": f"{fmt_val(d2)} m/s", "summary": "Incorrect.", "mistake": d2_mistake, "working": steps},
        {"value": d3, "display": f"{fmt_val(d3)} m/s", "summary": "Incorrect.", "mistake": "You only completed step 1 and reported f as v. You still need v = f × λ.", "working": steps},
    ]
    return make_question(question, correct_v, options_data, "m/s", scaffold=scaffold,
                         notes=NOTES["waves_speed"], topic="Waves", question_type="Waves Combined", level=level)


def make_find_lam(level="N5"):
    sc = random.choice(SCENARIOS)
    f_Hz, lam_m = sc["f_Hz"], sc["lam_m"]
    T_s = 1 / f_Hz
    T_disp, T_unit = best_period(T_s)
    correct_lam = lam_m

    d1 = round_sf(V_SOUND * T_disp)
    d2 = round_sf(V_SOUND * f_Hz)
    d3 = round_sf(f_Hz)

    lam_m_str = str(round_sf(lam_m))
    T_s_str = sci_latex(T_s) if T_s < 1e-3 else str(round_sf(T_s))
    T_power = PREFIX_POWER.get(T_unit, "")

    steps = [{"type": "text", "content": "Step 1: find frequency from the period."},
             {"type": "latex", "content": r"f = \frac{1}{T}"}]
    if T_unit != "s":
        steps.append({"type": "latex", "content": rf"T = {T_disp} \times {T_power} = {T_s_str}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"f = \frac{{1}}{{{T_s_str}}} = {f_Hz}\ \mathrm{{Hz}}"},
        {"type": "text",  "content": "Step 2: find wavelength."},
        {"type": "latex", "content": r"\lambda = \frac{v}{f}"},
        {"type": "latex", "content": rf"\lambda = \frac{{{V_SOUND}}}{{{f_Hz}}}"},
        {"type": "latex", "content": rf"\lambda = {lam_m_str}\ \mathrm{{m}}"},
    ]
    scaffold = [
        {"question": "Calculate the frequency from the period.", "answer": float(f_Hz), "unit": "Hz"},
        {"question": "Calculate the wavelength.", "answer": float(correct_lam), "unit": "m"},
    ]

    question = f"A sound wave has a period of {T_disp} {T_unit}.\n\nSpeed of sound = 340 m/s\n\nCalculate the wavelength."
    options_data = [
        {"value": correct_lam, "display": f"{lam_m_str} m", "summary": "Correct!", "mistake": None, "working": steps},
        {"value": d1, "display": f"{fmt_val(d1)} m", "summary": "Incorrect.",
         "mistake": f"You used T = {T_disp} as if already in seconds. Convert: {T_disp} {T_unit} = {T_s_str} s, then f = 1/{T_s_str} = {f_Hz} Hz.", "working": steps},
        {"value": d2, "display": f"{fmt_val(d2)} m", "summary": "Incorrect.",
         "mistake": "You multiplied v × f in step 2 instead of dividing. λ = v ÷ f.", "working": steps},
        {"value": d3, "display": f"{fmt_val(d3)} m", "summary": "Incorrect.",
         "mistake": "You only completed step 1 and reported f as λ. You still need λ = v ÷ f.", "working": steps},
    ]
    return make_question(question, correct_lam, options_data, "m", scaffold=scaffold,
                         notes=NOTES["waves_speed"], topic="Waves", question_type="Waves Combined", level=level)


def make_find_T(level="N5"):
    sc = random.choice(SCENARIOS)
    f_Hz, lam_m = sc["f_Hz"], sc["lam_m"]
    lam_disp, lam_unit = sc["lam_disp"], sc["lam_unit"]
    T_s = 1 / f_Hz
    T_disp, T_unit = best_period(T_s)
    T_factor = PREFIX_FACTOR.get(T_unit, 1)

    d1_raw = round_sf(f_Hz * T_factor)
    d1 = d1_raw if round_sf(d1_raw) != round_sf(T_disp) else round_sf(f_Hz / T_factor)
    f_wrong_d2 = V_SOUND * lam_m
    d2 = round_sf(1 / f_wrong_d2 / T_factor) if f_wrong_d2 > 0 else 0
    if lam_unit != "m":
        f_wrong_d3 = round_sf(V_SOUND / lam_disp)
        d3 = round_sf(1 / f_wrong_d3 / T_factor) if f_wrong_d3 > 0 and round_sf(1 / f_wrong_d3 / T_factor) != round_sf(d2) else round_sf(T_disp * 10)
        d3_mistake = (f"You did not convert λ to metres in step 1. {lam_disp} {lam_unit} = {lam_m} m." if d3 != round_sf(T_disp * 10)
                      else "Check your arithmetic — your answer is 10× too large.")
    else:
        d3 = round_sf(f_Hz / V_SOUND)
        d3_mistake = "You divided f by v. Use T = 1/f after finding f = v ÷ λ."

    lam_m_str = str(round_sf(lam_m))
    T_s_str = sci_latex(T_s) if T_s < 1e-3 else str(round_sf(T_s))
    steps = []
    if lam_unit != "m":
        steps.append({"type": "latex", "content": rf"\lambda = {lam_disp} \times {PREFIX_POWER.get(lam_unit, '')} = {lam_m_str}\ \mathrm{{m}}"})
    steps += [
        {"type": "text",  "content": "Step 1: find frequency."},
        {"type": "latex", "content": r"f = \frac{v}{\lambda}"},
        {"type": "latex", "content": rf"f = \frac{{{V_SOUND}}}{{{lam_m_str}}} = {f_Hz}\ \mathrm{{Hz}}"},
        {"type": "text",  "content": "Step 2: find period."},
        {"type": "latex", "content": r"T = \frac{1}{f}"},
        {"type": "latex", "content": rf"T = \frac{{1}}{{{f_Hz}}} = {T_s_str}\ \mathrm{{s}} = {T_disp}\ \mathrm{{{T_unit}}}"},
    ]
    scaffold = [
        {"question": "Calculate the frequency from wavelength and wave speed.", "answer": float(f_Hz), "unit": "Hz"},
        {"question": "Calculate the period.", "answer": float(T_disp), "unit": T_unit},
    ]

    question = f"A sound wave has a wavelength of {lam_disp} {lam_unit}.\n\nSpeed of sound = 340 m/s\n\nCalculate the period of the wave."
    options_data = [
        {"value": T_disp, "display": f"{T_disp} {T_unit}", "summary": "Correct!", "mistake": None, "working": steps},
        {"value": d1, "display": f"{fmt_val(d1)} {T_unit}", "summary": "Incorrect.", "mistake": "You used T = f in step 2 instead of T = 1/f. Period is the reciprocal of frequency.", "working": steps},
        {"value": d2, "display": f"{fmt_val(d2)} {T_unit}", "summary": "Incorrect.", "mistake": "You multiplied v × λ in step 1 instead of dividing. f = v ÷ λ.", "working": steps},
        {"value": d3, "display": f"{fmt_val(d3)} {T_unit}", "summary": "Incorrect.", "mistake": d3_mistake, "working": steps},
    ]
    return make_question(question, T_disp, options_data, T_unit, scaffold=scaffold,
                         notes=NOTES["waves_period"], topic="Waves", question_type="Waves Combined", level=level)


_ALL_GENS = [make_find_v, make_find_lam, make_find_T]


def generate_waves_combined(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
