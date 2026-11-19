"""Higher Interference prerequisites — question types mirroring the Hphys_Interference_Prerequisites worksheet.

Three generators: wave speed and period (T = 1/f, v = fλ, d = vt then v = fλ), units of wavelength (nm to m,
then v = fλ), and waves meeting and diffraction (state/explain as multiple choice). Path difference, grating
spacing and sine were left off the worksheet on 2026-11-19 so they are not here.
Recognised wrong answers follow the course reports: nm not converted to metres, f used as the period,
in phase and out of phase swapped, and a wider gap thought to give more diffraction.
"""
import math
import random

from topics.particles_and_waves.particles_waves_higher import _q, _choice, _txt, _ltx, _sig, _L, _T

QT = "Interference Prerequisites"
C = 3.00e8


# ════════════════ 1 — Wave speed and period ════════════════
# tied context: (name, speed in m/s, frequencies in Hz)
_WAVES = [("sound", 340.0, [170, 340, 425, 680, 850, 1700]),
          ("water ripples", 1.5, [1.5, 2.0, 3.0, 5.0]),
          ("microwaves", C, [2.45e9, 1.0e10, 1.5e10]),
          ("red light", C, [4.6e14, 4.8e14, 5.0e14])]
_ROPE = [("A wave on a rope", [2.0, 3.0, 4.0], [0.25, 0.50, 0.40], [2.0, 4.0, 5.0]),
         ("Ripples on a pond", [1.2, 1.5, 2.0], [0.10, 0.15, 0.20], [2.0, 3.0, 4.0])]


def gen_ip_wave_speed(level="Higher"):
    kind = random.choice(["period", "freq", "lambda", "speed", "twostep", "twostep"])
    if kind in ("period", "freq"):
        f = random.choice([2.0, 4.0, 5.0, 8.0, 20.0, 50.0, 250.0, 400.0])
        T = 1 / f
        if kind == "period":
            text = f"A wave has a frequency of {_txt(f)} Hz. Calculate its period."
            work = [_L(r"T = \frac{1}{f}"), _L(rf"T = \frac{{1}}{{{_ltx(f)}}} = {_ltx(T)}\ \mathrm{{s}}")]
            opts = [{"value": T, "mistake": None, "working": work},
                    {"value": f, "mistake": "The period is T = 1/f, not f.", "working": work},
                    {"value": _sig(T * 1000), "mistake": "T = 1/f is in seconds — don't multiply by 1000.", "working": work}]
            return _q(text, T, "s", opts, QT, None, level)
        text = f"A wave has a period of {_txt(T)} s. Calculate its frequency."
        work = [_L(r"T = \frac{1}{f}"), _L(rf"f = \frac{{1}}{{{_ltx(T)}}} = {_ltx(f)}\ \mathrm{{Hz}}")]
        opts = [{"value": f, "mistake": None, "working": work},
                {"value": T, "mistake": "f = 1/T, not T.", "working": work}]
        return _q(text, f, "Hz", opts, QT, None, level)
    if kind == "twostep":
        name, vs, lams, ts = random.choice(_ROPE)
        v, lam, t = random.choice(vs), random.choice(lams), random.choice(ts)
        d, f = v * t, v / lam
        text = f"{name} travels {_txt(d)} m in {_txt(t)} s. The wavelength is {_txt(lam)} m. Calculate the frequency."
        work = [_L(r"d = vt"), _L(rf"{_ltx(d)} = v \times {_ltx(t)} \Rightarrow v = {_ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"),
                _L(r"v = f\lambda"), _L(rf"{_ltx(v)} = f \times {_ltx(lam)} \Rightarrow f = {_ltx(f)}\ \mathrm{{Hz}}")]
        opts = [{"value": f, "mistake": None, "working": work},
                {"value": _sig(d / lam), "mistake": "The distance travelled is not the wave speed — use d = vt first.", "working": work},
                {"value": _sig(v * lam), "mistake": "v = fλ, so f = v ÷ λ.", "working": work},
                {"value": _sig(d * t / lam), "mistake": "v = d ÷ t (divide, don't multiply).", "working": work}]
        scaffold = [{"question": "What is the wave speed, in m/s?", "answer": _sig(v)}]
        return _q(text, f, "Hz", opts, QT, scaffold, level)
    name, v, fs = random.choice(_WAVES)
    f = random.choice(fs)
    lam = v / f
    if kind == "lambda":
        text = f"{name.capitalize()} of frequency {_txt(f)} Hz travel at {_txt(v)} m/s. Calculate the wavelength."
        work = [_L(r"v = f\lambda"), _L(rf"{_ltx(v)} = {_ltx(f)} \times \lambda"), _L(rf"\lambda = {_ltx(lam)}\ \mathrm{{m}}")]
        opts = [{"value": lam, "mistake": None, "working": work},
                {"value": _sig(v * f), "mistake": "λ = v ÷ f, not v × f.", "working": work},
                {"value": _sig(f / v), "mistake": "λ = v ÷ f — you have it upside down.", "working": work}]
        return _q(text, lam, "m", opts, QT, None, level)
    if kind == "speed":
        text = f"{name.capitalize()} have a frequency of {_txt(f)} Hz and a wavelength of {_txt(lam)} m. Calculate the wave speed."
        work = [_L(r"v = f\lambda"), _L(rf"v = {_ltx(f)} \times {_ltx(lam)} = {_ltx(v)}\ \mathrm{{m\,s^{{-1}}}}")]
        opts = [{"value": v, "mistake": None, "working": work},
                {"value": _sig(f / lam), "mistake": "v = f × λ (multiply).", "working": work},
                {"value": _sig(f + lam), "mistake": "v = f × λ, not f + λ.", "working": work}]
        return _q(text, v, "m/s", opts, QT, None, level)
    text = f"{name.capitalize()} of wavelength {_txt(lam)} m travel at {_txt(v)} m/s. Calculate the frequency."
    work = [_L(r"v = f\lambda"), _L(rf"{_ltx(v)} = f \times {_ltx(lam)}"), _L(rf"f = {_ltx(f)}\ \mathrm{{Hz}}")]
    opts = [{"value": f, "mistake": None, "working": work},
            {"value": _sig(v * lam), "mistake": "f = v ÷ λ, not v × λ.", "working": work},
            {"value": _sig(lam / v), "mistake": "f = v ÷ λ — you have it upside down.", "working": work}]
    return _q(text, f, "Hz", opts, QT, None, level)


# ════════════════ 2 — Units of wavelength ════════════════
def gen_ip_units(level="Higher"):
    kind = random.choice(["nm", "nm", "freq"])
    lam_nm = random.choice([405, 450, 532, 589, 633, 650])
    if kind == "nm":
        ans = lam_nm * 1e-9
        text = f"Light has a wavelength of {lam_nm} nm. Write this wavelength in metres."
        work = [_T("1 nm = 1 × 10⁻⁹ m"), _L(rf"{lam_nm} \times 10^{{-9}} = {_ltx(ans)}\ \mathrm{{m}}")]
        opts = [{"value": ans, "mistake": None, "working": work},
                {"value": lam_nm * 1e-6, "mistake": "nano means 10⁻⁹, not 10⁻⁶ (that is micro).", "working": work},
                {"value": lam_nm * 1e-3, "mistake": "nano means 10⁻⁹.", "working": work},
                {"value": lam_nm * 1e-10, "mistake": "nano means 10⁻⁹, not 10⁻¹⁰.", "working": work}]
        return _q(text, ans, "m", opts, QT, None, level)
    if kind == "freq":
        f = C / (lam_nm * 1e-9)
        text = f"Light of wavelength {lam_nm} nm travels through air at 3.00 × 10⁸ m/s. Calculate its frequency."
        work = [_L(rf"\lambda = {lam_nm} \times 10^{{-9}} = {_ltx(lam_nm * 1e-9)}\ \mathrm{{m}}"), _L(r"v = f\lambda"),
                _L(rf"f = \frac{{3.00\times10^8}}{{{_ltx(lam_nm * 1e-9)}}} = {_ltx(f)}\ \mathrm{{Hz}}")]
        opts = [{"value": f, "mistake": None, "working": work},
                {"value": C / lam_nm, "mistake": "Convert the wavelength from nm to metres first.", "working": work},
                {"value": C * lam_nm * 1e-9, "mistake": "f = v ÷ λ, not v × λ.", "working": work}]
        scaffold = [{"question": "What is the wavelength in metres?", "answer": _sig(lam_nm * 1e-9)}]
        return _q(text, f, "Hz", opts, QT, scaffold, level)
    raise ValueError(kind)


# ════════════════ 3 — Waves meeting and diffraction ════════════════
def gen_ip_meeting(level="Higher"):
    A = random.choice([2.0, 3.0, 4.0, 5.0])
    gap = random.choice([2.0, 5.0, 10.0])
    bank = [
        (f"Two waves, each of amplitude {A:g} cm, meet in phase. State the amplitude of the resultant wave.", f"{2 * A:g} cm",
         [("0 cm", "In phase the displacements add; they only cancel when out of phase."), (f"{A:g} cm", "The displacements add: A + A."), (f"{A / 2:g} cm", "The displacements add, they aren't averaged.")]),
        (f"Two waves, each of amplitude {A:g} cm, meet exactly out of phase. State the amplitude of the resultant wave.", "0 cm",
         [(f"{2 * A:g} cm", "That is for waves in phase — out of phase they cancel."), (f"{A:g} cm", "Equal and opposite displacements cancel completely.")]),
        ("Two loudspeakers connected to the same signal generator emit the same note. A listener at point X hears almost no sound. Why?",
         "The waves arrive at X out of phase (crest meets trough) and cancel — destructive interference.",
         [("The waves arrive at X in phase and cancel.", "Waves in phase add — they cancel only when out of phase."),
          ("The waves from the two speakers are absorbed before they reach X.", "The quiet point is due to interference, not absorption."),
          ("The waves arrive at X in phase, so the amplitude doubles.", "Doubling is for in phase — a quiet point needs out of phase.")]),
        (f"Water waves of wavelength 1.0 cm reach a barrier with a gap. For which gap width is the diffraction greatest?", "1.0 cm — about the same size as the wavelength.",
         [(f"{gap * 5:g} cm — a wider gap lets more of the wave through.", "Diffraction is greatest when the gap is about the same size as the wavelength."),
          ("It is the same for every gap width.", "Diffraction depends on the gap compared with the wavelength.")]),
        ("Which statement describes diffraction?", "The spreading out of waves as they pass through a gap or round an obstacle.",
         [("The change of direction of a wave when its speed changes.", "That is refraction."), ("The reflection of a wave from a surface.", "That is reflection."),
          ("Two waves adding as they meet.", "That is interference (superposition).")]),
        ("Waves meet 'in phase'. Which description is correct?", "A crest meets a crest — the displacements add — constructive interference.",
         [("A crest meets a trough — the displacements cancel.", "That is out of phase (destructive)."), ("The waves have different frequencies.", "In phase describes the alignment of the waves.")]),
    ]
    text, ans, wrong = random.choice(bank)
    return _choice(text, ans, wrong, QT, level)
