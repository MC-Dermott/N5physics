import random
import math
from utils.make_question import make_question
from utils.notes import NOTES

C = 3e8
V_SOUND = 340


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
    "nm": r"10^{-9}", "μm": r"10^{-6}", "mm": r"10^{-3}", "cm": r"10^{-2}",
    "MHz": r"10^{6}", "GHz": r"10^{9}", "kHz": r"10^{3}",
}


def _conv_latex(disp, unit, si_val):
    si_str = sci_latex(si_val) if abs(si_val) < 0.001 or abs(si_val) >= 1e6 else str(round_sf(si_val))
    power = PREFIX_POWER.get(unit)
    if power:
        return rf"{disp} \times {power} = {si_str}"
    return si_str


EM_FIND_F = [
    {"type": "radio wave",    "lam_disp": 30,   "lam_unit": "cm", "lam_m": 0.30},
    {"type": "microwave",     "lam_disp": 10,   "lam_unit": "cm", "lam_m": 0.10},
    {"type": "microwave",     "lam_disp": 6,    "lam_unit": "cm", "lam_m": 0.06},
    {"type": "infrared",      "lam_disp": 10,   "lam_unit": "μm", "lam_m": 10e-6},
    {"type": "visible light", "lam_disp": 700,  "lam_unit": "nm", "lam_m": 700e-9},
    {"type": "visible light", "lam_disp": 600,  "lam_unit": "nm", "lam_m": 600e-9},
    {"type": "visible light", "lam_disp": 500,  "lam_unit": "nm", "lam_m": 500e-9},
    {"type": "visible light", "lam_disp": 400,  "lam_unit": "nm", "lam_m": 400e-9},
    {"type": "ultraviolet",   "lam_disp": 300,  "lam_unit": "nm", "lam_m": 300e-9},
    {"type": "X-ray",         "lam_disp": 1,    "lam_unit": "nm", "lam_m": 1e-9},
    {"type": "gamma ray",     "lam_disp": 0.01, "lam_unit": "nm", "lam_m": 0.01e-9},
]

EM_FIND_LAM = [
    {"type": "radio wave",  "f_disp": 100, "f_unit": "MHz", "f_Hz": 100e6},
    {"type": "radio wave",  "f_disp": 300, "f_unit": "MHz", "f_Hz": 300e6},
    {"type": "radio wave",  "f_disp": 1,   "f_unit": "GHz", "f_Hz": 1e9},
    {"type": "radio wave",  "f_disp": 2,   "f_unit": "GHz", "f_Hz": 2e9},
    {"type": "microwave",   "f_disp": 3,   "f_unit": "GHz", "f_Hz": 3e9},
    {"type": "microwave",   "f_disp": 5,   "f_unit": "GHz", "f_Hz": 5e9},
    {"type": "microwave",   "f_disp": 10,  "f_unit": "GHz", "f_Hz": 10e9},
]

SOUND = [
    {"f_Hz": 100,  "f_disp": 100,  "f_unit": "Hz",  "lam_disp": 3.4, "lam_unit": "m",  "lam_m": 3.4},
    {"f_Hz": 200,  "f_disp": 200,  "f_unit": "Hz",  "lam_disp": 1.7, "lam_unit": "m",  "lam_m": 1.7},
    {"f_Hz": 680,  "f_disp": 680,  "f_unit": "Hz",  "lam_disp": 0.5, "lam_unit": "m",  "lam_m": 0.5},
    {"f_Hz": 1000, "f_disp": 1000, "f_unit": "Hz",  "lam_disp": 34,  "lam_unit": "cm", "lam_m": 0.34},
    {"f_Hz": 1700, "f_disp": 1700, "f_unit": "Hz",  "lam_disp": 20,  "lam_unit": "cm", "lam_m": 0.20},
    {"f_Hz": 3400, "f_disp": 3400, "f_unit": "Hz",  "lam_disp": 10,  "lam_unit": "cm", "lam_m": 0.10},
    {"f_Hz": 17000,"f_disp": 17,   "f_unit": "kHz", "lam_disp": 2,   "lam_unit": "cm", "lam_m": 0.02},
]


def make_find_f_em(level="N5"):
    sc = random.choice(EM_FIND_F)
    em_type, lam_disp, lam_unit, lam_m = sc["type"], sc["lam_disp"], sc["lam_unit"], sc["lam_m"]
    correct_f = C / lam_m
    no_conv   = C / lam_disp
    wrong_v   = V_SOUND / lam_m
    mult_err  = C * lam_m
    if round_sf(no_conv) == round_sf(mult_err):
        mult_err = round_sf(C / (lam_m * 1000))

    lam_m_str = sci_latex(lam_m) if abs(lam_m) < 0.001 else str(round_sf(lam_m))
    f_str = sci_latex(correct_f)
    steps = [
        {"type": "text",  "content": f"Convert wavelength to metres: {lam_disp} {lam_unit} = {sci_latex(lam_m) if abs(lam_m)<0.001 else round_sf(lam_m)} m"},
        {"type": "text",  "content": "All EM waves travel at the speed of light: v = 3 × 10⁸ m/s"},
        {"type": "latex", "content": r"f = \frac{v}{\lambda}"},
        {"type": "latex", "content": rf"f = \frac{{3 \times 10^8}}{{{lam_m_str}}}"},
        {"type": "latex", "content": rf"f = {f_str}\ \mathrm{{Hz}}"},
    ]
    question = f"A {em_type} has a wavelength of {lam_disp} {lam_unit}.\n\nSpeed of light = 3 × 10⁸ m/s\n\nCalculate the frequency."
    options_data = [
        {"value": correct_f, "display": f"{fmt_val(correct_f)} Hz", "summary": "Correct!", "mistake": None, "working": steps},
        {"value": no_conv,   "display": f"{fmt_val(no_conv)} Hz",   "summary": "Incorrect.", "mistake": f"You used λ = {lam_disp} without converting to metres. {lam_disp} {lam_unit} = {sci_latex(lam_m)} m.", "working": steps},
        {"value": wrong_v,   "display": f"{fmt_val(wrong_v)} Hz",   "summary": "Incorrect.", "mistake": "You used v = 340 m/s (speed of sound). All EM waves travel at 3 × 10⁸ m/s.", "working": steps},
        {"value": mult_err,  "display": f"{fmt_val(mult_err)} Hz",  "summary": "Incorrect.", "mistake": "You multiplied v × λ instead of dividing. f = v ÷ λ.", "working": steps},
    ]
    return make_question(question, correct_f, options_data, "Hz", notes=NOTES["waves_speed"],
                         topic="Waves", question_type="Wave Speed", level=level)


def make_find_lam_em(level="N5"):
    sc = random.choice(EM_FIND_LAM)
    em_type, f_disp, f_unit, f_Hz = sc["type"], sc["f_disp"], sc["f_unit"], sc["f_Hz"]
    correct_lam = C / f_Hz
    no_conv     = C / f_disp
    wrong_v     = V_SOUND / f_Hz
    mult_err    = C * f_Hz

    f_Hz_str  = sci_latex(f_Hz)
    lam_str   = sci_latex(correct_lam)
    steps = [
        {"type": "text",  "content": f"Convert frequency to Hz: {f_disp} {f_unit} = {sci_latex(f_Hz)} Hz"},
        {"type": "text",  "content": "All EM waves travel at the speed of light: v = 3 × 10⁸ m/s"},
        {"type": "latex", "content": r"\lambda = \frac{v}{f}"},
        {"type": "latex", "content": rf"\lambda = \frac{{3 \times 10^8}}{{{f_Hz_str}}}"},
        {"type": "latex", "content": rf"\lambda = {lam_str}\ \mathrm{{m}}"},
    ]
    question = f"A {em_type} has a frequency of {f_disp} {f_unit}.\n\nSpeed of light = 3 × 10⁸ m/s\n\nCalculate the wavelength."
    options_data = [
        {"value": correct_lam, "display": f"{fmt_val(correct_lam)} m", "summary": "Correct!", "mistake": None, "working": steps},
        {"value": no_conv,     "display": f"{fmt_val(no_conv)} m",     "summary": "Incorrect.", "mistake": f"You used f = {f_disp} without converting to Hz. {f_disp} {f_unit} = {sci_latex(f_Hz)} Hz.", "working": steps},
        {"value": wrong_v,     "display": f"{fmt_val(wrong_v)} m",     "summary": "Incorrect.", "mistake": "You used v = 340 m/s (speed of sound). All EM waves travel at 3 × 10⁸ m/s.", "working": steps},
        {"value": mult_err,    "display": f"{fmt_val(mult_err)} m",    "summary": "Incorrect.", "mistake": "You multiplied v × f instead of dividing. λ = v ÷ f.", "working": steps},
    ]
    return make_question(question, correct_lam, options_data, "m", notes=NOTES["waves_speed"],
                         topic="Waves", question_type="Wave Speed", level=level)


def make_find_v_sound(level="N5"):
    sc = random.choice(SOUND)
    f_Hz, f_disp, f_unit = sc["f_Hz"], sc["f_disp"], sc["f_unit"]
    lam_disp, lam_unit, lam_m = sc["lam_disp"], sc["lam_unit"], sc["lam_m"]
    correct_v = round_sf(f_Hz * lam_m)
    div_err   = round_sf(f_Hz / lam_m)
    conv_err  = round_sf(f_Hz * lam_disp) if lam_unit != "m" else round_sf(lam_m / f_Hz)
    if round_sf(div_err) == round_sf(conv_err):
        conv_err = round_sf(lam_m / f_Hz)

    lam_m_str = str(round_sf(lam_m))
    steps = []
    if lam_unit != "m":
        steps.append({"type": "text", "content": f"Convert wavelength: {lam_disp} {lam_unit} = {lam_m} m"})
    steps += [
        {"type": "latex", "content": r"v = f\lambda"},
        {"type": "latex", "content": rf"v = {f_Hz} \times {lam_m_str}"},
        {"type": "latex", "content": rf"v = {correct_v}\ \mathrm{{m/s}}"},
    ]
    question = f"A sound wave has a frequency of {f_disp} {f_unit} and a wavelength of {lam_disp} {lam_unit}.\n\nCalculate the wave speed."
    options_data = [
        {"value": correct_v, "display": f"{fmt_val(correct_v)} m/s", "summary": "Correct!", "mistake": None, "working": steps},
        {"value": div_err,   "display": f"{fmt_val(div_err)} m/s",   "summary": "Incorrect.", "mistake": "You divided f by λ instead of multiplying. v = f × λ.", "working": steps},
        {"value": conv_err,  "display": f"{fmt_val(conv_err)} m/s",  "summary": "Incorrect.",
         "mistake": (f"You used λ = {lam_disp} without converting to metres. {lam_disp} {lam_unit} = {lam_m} m." if lam_unit != "m" else "You divided λ by f instead of multiplying. v = f × λ."), "working": steps},
        {"value": round_sf(f_Hz + lam_m), "display": f"{round_sf(f_Hz + lam_m)} m/s", "summary": "Incorrect.", "mistake": "You added f and λ instead of multiplying. v = f × λ.", "working": steps},
    ]
    return make_question(question, correct_v, options_data, "m/s", notes=NOTES["waves_speed"],
                         topic="Waves", question_type="Wave Speed", level=level)


def make_find_f_sound(level="N5"):
    sc = random.choice(SOUND)
    lam_disp, lam_unit, lam_m = sc["lam_disp"], sc["lam_unit"], sc["lam_m"]
    correct_f = round_sf(V_SOUND / lam_m)
    inv_f     = round_sf(lam_m / V_SOUND)
    mult_f    = round_sf(V_SOUND * lam_m)
    no_conv   = round_sf(V_SOUND / lam_disp) if lam_unit != "m" else round_sf(correct_f * 10)
    no_conv_msg = (f"You used λ = {lam_disp} without converting to metres. {lam_disp} {lam_unit} = {lam_m} m." if lam_unit != "m" else "Check your arithmetic.")

    lam_m_str = str(round_sf(lam_m))
    steps = []
    if lam_unit != "m":
        steps.append({"type": "text", "content": f"Convert wavelength: {lam_disp} {lam_unit} = {lam_m} m"})
    steps += [
        {"type": "latex", "content": r"f = \frac{v}{\lambda}"},
        {"type": "latex", "content": rf"f = \frac{{340}}{{{lam_m_str}}}"},
        {"type": "latex", "content": rf"f = {correct_f}\ \mathrm{{Hz}}"},
    ]
    question = f"A sound wave has a wavelength of {lam_disp} {lam_unit}.\n\nSpeed of sound = 340 m/s\n\nCalculate the frequency."
    options_data = [
        {"value": correct_f, "display": f"{fmt_val(correct_f)} Hz", "summary": "Correct!", "mistake": None, "working": steps},
        {"value": inv_f,     "display": f"{fmt_val(inv_f)} Hz",     "summary": "Incorrect.", "mistake": "You divided λ by v instead of v by λ. f = v ÷ λ.", "working": steps},
        {"value": mult_f,    "display": f"{fmt_val(mult_f)} Hz",    "summary": "Incorrect.", "mistake": "You multiplied v × λ instead of dividing. f = v ÷ λ.", "working": steps},
        {"value": no_conv,   "display": f"{fmt_val(no_conv)} Hz",   "summary": "Incorrect.", "mistake": no_conv_msg, "working": steps},
    ]
    return make_question(question, correct_f, options_data, "Hz", notes=NOTES["waves_speed"],
                         topic="Waves", question_type="Wave Speed", level=level)


def make_find_lam_sound(level="N5"):
    sc = random.choice(SOUND)
    f_Hz, f_disp, f_unit = sc["f_Hz"], sc["f_disp"], sc["f_unit"]
    correct_lam = round_sf(V_SOUND / f_Hz)
    inv_lam     = round_sf(f_Hz / V_SOUND)
    mult_lam    = round_sf(V_SOUND * f_Hz)
    fallback    = round_sf(correct_lam * 100)
    if round_sf(fallback) == round_sf(inv_lam):
        fallback = round_sf(correct_lam / 10)
    no_conv     = round_sf(V_SOUND / f_disp) if f_unit != "Hz" else fallback
    no_conv_msg = (f"You used f = {f_disp} without converting to Hz. {f_disp} {f_unit} = {f_Hz} Hz." if f_unit != "Hz" else "Check your arithmetic.")

    steps = [
        {"type": "latex", "content": r"\lambda = \frac{v}{f}"},
        {"type": "latex", "content": rf"\lambda = \frac{{340}}{{{f_Hz}}}"},
        {"type": "latex", "content": rf"\lambda = {correct_lam}\ \mathrm{{m}}"},
    ]
    question = f"A sound wave has a frequency of {f_disp} {f_unit}.\n\nSpeed of sound = 340 m/s\n\nCalculate the wavelength."
    options_data = [
        {"value": correct_lam, "display": f"{fmt_val(correct_lam)} m", "summary": "Correct!", "mistake": None, "working": steps},
        {"value": inv_lam,     "display": f"{fmt_val(inv_lam)} m",     "summary": "Incorrect.", "mistake": "You divided f by v instead of v by f. λ = v ÷ f.", "working": steps},
        {"value": mult_lam,    "display": f"{fmt_val(mult_lam)} m",    "summary": "Incorrect.", "mistake": "You multiplied v × f instead of dividing. λ = v ÷ f.", "working": steps},
        {"value": no_conv,     "display": f"{fmt_val(no_conv)} m",     "summary": "Incorrect.", "mistake": no_conv_msg, "working": steps},
    ]
    return make_question(question, correct_lam, options_data, "m", notes=NOTES["waves_speed"],
                         topic="Waves", question_type="Wave Speed", level=level)


_N4_GENS  = [make_find_v_sound, make_find_f_sound, make_find_lam_sound]
_ALL_GENS = [make_find_f_em, make_find_lam_em, make_find_v_sound, make_find_f_sound, make_find_lam_sound]


def generate_wave_speed(level="N5"):
    gens = _N4_GENS if level == "N4" else _ALL_GENS
    return random.choice(gens)(level=level)
