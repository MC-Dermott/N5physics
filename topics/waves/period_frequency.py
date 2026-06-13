import random
import math
from utils.make_question import make_question
from utils.notes import NOTES


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def sci_latex(val):
    exp = int(math.floor(math.log10(abs(val))))
    m = round(val / 10 ** exp, 2)
    m = int(m) if m == int(m) else m
    return rf"{m} \times 10^{{{exp}}}"


_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


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


PREFIX_POWER = {
    "kHz": r"10^{3}", "MHz": r"10^{6}", "GHz": r"10^{9}",
    "ms": r"10^{-3}", "μs": r"10^{-6}", "ns": r"10^{-9}",
}

PREFIX_FACTOR = {
    "kHz": 1e3, "MHz": 1e6, "GHz": 1e9, "Hz": 1,
    "ms": 1e-3, "μs": 1e-6, "ns": 1e-9, "s": 1,
}


def best_period(T_s):
    if T_s >= 1:
        return round_sf(T_s), "s"
    elif T_s >= 1e-3:
        return round_sf(T_s * 1e3), "ms"
    elif T_s >= 1e-6:
        return round_sf(T_s * 1e6), "μs"
    else:
        return round_sf(T_s * 1e9), "ns"


def best_freq(f_Hz):
    if f_Hz >= 1e9:
        return round_sf(f_Hz / 1e9), "GHz"
    elif f_Hz >= 1e6:
        return round_sf(f_Hz / 1e6), "MHz"
    elif f_Hz >= 1e3:
        return round_sf(f_Hz / 1e3), "kHz"
    else:
        return round_sf(f_Hz), "Hz"


SCENARIOS = [
    (100, "Hz", 100), (200, "Hz", 200), (500, "Hz", 500),
    (1000, "Hz", 1000), (2000, "Hz", 2000),
    (5, "kHz", 5e3), (10, "kHz", 10e3), (50, "kHz", 50e3),
    (1, "MHz", 1e6), (5, "MHz", 5e6), (10, "MHz", 10e6),
    (1, "GHz", 1e9), (2, "GHz", 2e9), (5, "GHz", 5e9),
]

_COUNT = [
    (20, 10, "s", 10), (50, 5, "s", 5), (100, 20, "s", 20),
    (200, 40, "s", 40), (300, 60, "s", 60), (500, 100, "s", 100),
    (60, 1, "minutes", 60), (120, 2, "minutes", 120),
    (300, 5, "minutes", 300), (600, 10, "minutes", 600),
    (30, 10, "s", 10), (80, 20, "s", 20), (250, 50, "s", 50),
]


def make_find_T(level="N5"):
    f_disp, f_unit, f_Hz = random.choice(SCENARIOS)
    T_s = 1 / f_Hz
    T_disp, T_unit = best_period(T_s)
    T_factor = PREFIX_FACTOR.get(T_unit, 1)

    inv_val = round_sf(f_Hz / T_factor)
    sq_val  = round_sf(1 / (f_Hz ** 2) / T_factor)
    if f_unit != "Hz":
        no_conv_val = round_sf((1 / f_disp) / T_factor)
        extra = {"value": no_conv_val, "display": f"{fmt_val(no_conv_val)} {T_unit}",
                 "summary": "Incorrect.",
                 "mistake": f"You used f = {f_disp} without converting to Hz. {f_disp} {f_unit} = {sci_latex(f_Hz) if f_Hz >= 1e6 else f_Hz} Hz."}
    else:
        no_conv_val = round_sf(T_disp * 10)
        extra = {"value": no_conv_val, "display": f"{fmt_val(no_conv_val)} {T_unit}",
                 "summary": "Incorrect.", "mistake": "Check your arithmetic — your answer is 10× too large."}

    f_Hz_str = sci_latex(f_Hz) if f_Hz >= 1e6 else str(f_Hz)
    T_str    = fmt_val(T_disp)
    steps = []
    if f_unit != "Hz":
        steps.append({"type": "latex", "content": rf"f = {f_disp} \times {PREFIX_POWER[f_unit]} = {f_Hz_str}\ \mathrm{{Hz}}"})
    steps += [
        {"type": "latex", "content": r"T = \frac{1}{f}"},
        {"type": "latex", "content": rf"T = \frac{{1}}{{{f_Hz_str}}}"},
        {"type": "latex", "content": rf"T = {T_str}\ \mathrm{{{T_unit}}}"},
    ]

    question = f"A signal has a frequency of {f_disp} {f_unit}.\n\nCalculate the period."
    options_data = [
        {"value": T_disp,   "display": f"{T_str} {T_unit}",         "summary": "Correct!", "mistake": None, "working": steps},
        {"value": inv_val,  "display": f"{fmt_val(inv_val)} {T_unit}", "summary": "Incorrect.", "mistake": "You used T = f instead of T = 1/f. Period is the reciprocal of frequency.", "working": steps},
        {"value": sq_val,   "display": f"{fmt_val(sq_val)} {T_unit}", "summary": "Incorrect.", "mistake": "Check your equation. T = 1 ÷ f.", "working": steps},
        {**extra, "working": steps},
    ]
    return make_question(question, T_disp, options_data, T_unit, notes=NOTES["waves_period"],
                         topic="Waves", question_type="Period & Frequency", level=level)


def make_find_f(level="N5"):
    f_disp_orig, f_unit_orig, f_Hz = random.choice(SCENARIOS)
    T_s = 1 / f_Hz
    T_disp, T_unit = best_period(T_s)
    f_disp, f_unit = best_freq(f_Hz)

    inv_f = T_s
    T_s_str = sci_latex(T_s) if T_s < 1e-3 else str(round_sf(T_s))
    f_str   = sci_latex(f_Hz) if f_Hz >= 1e6 else str(round_sf(f_Hz))

    steps = []
    if T_unit != "s":
        steps.append({"type": "latex", "content": rf"T = {T_disp} \times {PREFIX_POWER[T_unit]} = {T_s_str}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": r"f = \frac{1}{T}"},
        {"type": "latex", "content": rf"f = \frac{{1}}{{{T_s_str}}}"},
        {"type": "latex", "content": rf"f = {f_str}\ \mathrm{{Hz}}"},
    ]

    if T_unit != "s":
        no_conv_f = 1 / T_disp
        extra = {"value": round_sf(no_conv_f), "display": f"{fmt_val(round_sf(no_conv_f))} Hz",
                 "summary": "Incorrect.",
                 "mistake": f"You used T = {T_disp} without converting to seconds. {T_disp} {T_unit} = {T_s_str} s."}
    else:
        extra = {"value": round_sf(f_Hz * 10), "display": f"{fmt_val(round_sf(f_Hz * 10))} Hz",
                 "summary": "Incorrect.", "mistake": "Check your arithmetic — your answer is 10× too large."}

    question = f"A signal has a period of {T_disp} {T_unit}.\n\nCalculate the frequency."
    options_data = [
        {"value": f_Hz,           "display": f"{fmt_val(f_disp)} {f_unit}", "summary": "Correct!", "mistake": None, "working": steps},
        {"value": round_sf(inv_f),"display": f"{fmt_val(round_sf(inv_f))} Hz", "summary": "Incorrect.", "mistake": "You used f = T instead of f = 1/T. Frequency is the reciprocal of period.", "working": steps},
        {**extra, "working": steps},
        {"value": round_sf(f_Hz / 10), "display": f"{fmt_val(round_sf(f_Hz / 10))} Hz",
         "summary": "Incorrect.", "mistake": "Check your arithmetic — your answer is 10× too small.", "working": steps},
    ]
    return make_question(question, f_Hz, options_data, f_unit, notes=NOTES["waves_period"],
                         topic="Waves", question_type="Period & Frequency", level=level)


def make_find_f_from_count(level="N5"):
    N, t_disp, t_unit, t_si = random.choice(_COUNT)
    correct_f = N / t_si
    multiplied = round_sf(N * t_si)
    inverted   = round_sf(t_si / N)

    if t_unit != "s":
        no_conv = round_sf(N / t_disp)
        no_conv_msg = f"You used t = {t_disp} without converting from {t_unit} to seconds. {t_disp} {t_unit} = {t_si} s."
    else:
        no_conv = round_sf(N + t_si)
        no_conv_msg = "You added N and t instead of dividing. f = N ÷ t."

    steps = [{"type": "latex", "content": r"f = \frac{N}{t}"}]
    if t_unit != "s":
        steps.append({"type": "latex", "content": rf"t = {t_disp}\ \mathrm{{{t_unit}}} = {t_si}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"f = \frac{{{N}}}{{{t_si}}}"},
        {"type": "latex", "content": rf"f = {round_sf(correct_f)}\ \mathrm{{Hz}}"},
    ]
    question = f"{N} complete waves pass a point in {t_disp} {t_unit}.\n\nCalculate the frequency."
    options_data = [
        {"value": correct_f, "display": f"{fmt_val(correct_f)} Hz", "summary": "Correct!", "mistake": None, "working": steps},
        {"value": multiplied,"display": f"{fmt_val(multiplied)} Hz","summary": "Incorrect.", "mistake": "You multiplied N × t instead of dividing. f = N ÷ t.", "working": steps},
        {"value": inverted,  "display": f"{fmt_val(inverted)} Hz", "summary": "Incorrect.", "mistake": "You divided t by N instead of N by t. f = N ÷ t.", "working": steps},
        {"value": no_conv,   "display": f"{fmt_val(no_conv)} Hz",  "summary": "Incorrect.", "mistake": no_conv_msg, "working": steps},
    ]
    return make_question(question, correct_f, options_data, "Hz", notes=NOTES["waves_period"],
                         topic="Waves", question_type="Period & Frequency", level=level)


def make_find_N(level="N5"):
    N, t_disp, t_unit, t_si = random.choice(_COUNT)
    f = N / t_si
    f_disp, f_unit = best_freq(f)
    correct = float(N)

    divided  = round_sf(f / t_si)
    inverted = round_sf(t_si / f)

    if f_unit != "Hz":
        no_conv = round_sf(f_disp * t_si)
        no_conv_msg = f"You used f = {f_disp} without converting from {f_unit} to Hz. {f_disp} {f_unit} = {f} Hz."
    elif t_unit != "s":
        no_conv = round_sf(f * t_disp)
        no_conv_msg = f"You used t = {t_disp} without converting from {t_unit} to seconds. {t_disp} {t_unit} = {t_si} s."
    else:
        no_conv = round_sf(f + t_si)
        no_conv_msg = "You added f and t instead of multiplying. N = f × t."

    steps = [{"type": "latex", "content": r"N = ft"}]
    if t_unit != "s":
        steps.append({"type": "latex", "content": rf"t = {t_disp}\ \mathrm{{{t_unit}}} = {t_si}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"N = {f} \times {t_si}"},
        {"type": "latex", "content": rf"N = {int(correct)}\ \mathrm{{waves}}"},
    ]
    question = f"A wave has a frequency of {f_disp} {f_unit}.\n\nHow many complete waves pass a point in {t_disp} {t_unit}?"
    options_data = [
        {"value": correct,  "display": str(int(correct)), "summary": "Correct!", "mistake": None, "working": steps},
        {"value": divided,  "display": str(divided),      "summary": "Incorrect.", "mistake": "You divided f by t instead of multiplying. N = f × t.", "working": steps},
        {"value": inverted, "display": str(inverted),     "summary": "Incorrect.", "mistake": "You divided t by f. N = f × t.", "working": steps},
        {"value": no_conv,  "display": str(no_conv),      "summary": "Incorrect.", "mistake": no_conv_msg, "working": steps},
    ]
    return make_question(question, correct, options_data, "waves", notes=NOTES["waves_period"],
                         topic="Waves", question_type="Period & Frequency", level=level)


_ALL_GENS = [make_find_T, make_find_f, make_find_f_from_count, make_find_N]


def generate_period_frequency(level="N5"):
    return random.choice(_ALL_GENS)(level=level)
