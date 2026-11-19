"""Higher Interference prerequisites — question types mirroring the Hphys_Interference_Prerequisites worksheet.

Five generators: wave speed and period (T = 1/f, v = fλ, d = vt then v = fλ), units and grating spacing,
path difference and phase, waves meeting and diffraction (state/explain as multiple choice), and sine.
Recognised wrong answers follow the course reports: nm not converted to metres, lines per mm used as d,
f used as the period, distances added instead of subtracted, in phase and out of phase swapped, a wider
gap thought to give more diffraction, and the calculator left in radian mode.
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


# ════════════════ 2 — Units and grating spacing ════════════════
def gen_ip_units(level="Higher"):
    kind = random.choice(["nm", "nm", "spacing", "spacing", "lines", "freq"])
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
    if kind == "spacing":
        lpm = random.choice([100, 250, 300, 400, 500, 600])
        d = 1 / (lpm * 1000)
        text = f"A grating has {lpm} lines per millimetre. Calculate the spacing between neighbouring lines, in metres."
        work = [_L(rf"{lpm}\ \text{{lines per mm}} = {lpm * 1000}\ \text{{lines per m}}"), _L(rf"d = \frac{{1}}{{{lpm * 1000}}} = {_ltx(d)}\ \mathrm{{m}}")]
        opts = [{"value": d, "mistake": None, "working": work},
                {"value": 1 / lpm, "mistake": "Change lines per mm to lines per m (× 1000) first.", "working": work},
                {"value": float(lpm), "mistake": "The number of lines per mm is not the spacing — d = 1 ÷ lines per metre.", "working": work},
                {"value": 1 / (lpm * 100), "mistake": "There are 1000 mm in a metre, not 100.", "working": work}]
        scaffold = [{"question": "How many lines per metre?", "answer": float(lpm * 1000)}]
        return _q(text, d, "m", opts, QT, scaffold, level)
    d = random.choice([1.6e-6, 2.0e-6, 2.5e-6, 4.0e-6, 5.0e-6])
    lpmm = 1e-3 / d
    text = f"The spacing between neighbouring lines of a grating is {_txt(d)} m. Calculate the number of lines per millimetre."
    work = [_L(rf"\text{{lines per m}} = \frac{{1}}{{{_ltx(d)}}} = {_ltx(1 / d)}"), _L(rf"\text{{lines per mm}} = {_ltx(lpmm)}")]
    opts = [{"value": lpmm, "mistake": None, "working": work},
            {"value": 1 / d, "mistake": "That is lines per METRE — divide by 1000 for lines per mm.", "working": work},
            {"value": d * 1e3, "mistake": "Lines per metre = 1 ÷ d.", "working": work},
            {"value": lpmm / 10, "mistake": "There are 1000 mm in a metre.", "working": work}]
    scaffold = [{"question": "How many lines per metre?", "answer": _sig(1 / d)}]
    return _q(text, lpmm, "lines per mm", opts, QT, scaffold, level)


# ════════════════ 3 — Path difference and phase ════════════════
def gen_ip_path_phase(level="Higher"):
    lam = random.choice([0.20, 0.40, 0.50])   # pd = kλ stays exact at 2 d.p. and v/λ is a whole number
    k = random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    pd = k * lam
    d2 = random.choice([1.50, 1.70, 2.00, 2.30, 3.00, 3.20])
    d1 = d2 + pd
    kind = random.choice(["pd", "number", "phase", "sound"])
    base = f"Two sources emit waves of wavelength {_txt(lam)} m. Point P is {_txt(d1, 3)} m from one source and {_txt(d2, 3)} m from the other."
    if kind == "pd":
        text = base + " Calculate the path difference at P."
        work = [_L(rf"{_ltx(d1)} - {_ltx(d2)} = {_ltx(pd)}\ \mathrm{{m}}")]
        opts = [{"value": pd, "mistake": None, "working": work},
                {"value": _sig(d1 + d2), "mistake": "The path difference is the DIFFERENCE — subtract, don't add.", "working": work},
                {"value": _sig(d1 / d2), "mistake": "Subtract the distances; don't divide them.", "working": work}]
        return _q(text, pd, "m", opts, QT, None, level)
    if kind == "number":
        text = base + " Calculate the number of wavelengths in the path difference."
        work = [_L(rf"\text{{path difference}} = {_ltx(d1)} - {_ltx(d2)} = {_ltx(pd)}\ \mathrm{{m}}"), _L(rf"\frac{{{_ltx(pd)}}}{{{_ltx(lam)}}} = {k:g}")]
        opts = [{"value": k, "mistake": None, "working": work},
                {"value": _sig((d1 + d2) / lam), "mistake": "Subtract the distances to get the path difference, then divide by λ.", "working": work},
                {"value": _sig(lam / pd), "mistake": "Number of wavelengths = path difference ÷ λ (you have it upside down).", "working": work},
                {"value": _sig(pd * lam), "mistake": "Divide the path difference by λ; don't multiply.", "working": work}]
        scaffold = [{"question": "What is the path difference, in m?", "answer": _sig(pd)}]
        return _q(text, k, "wavelengths", opts, QT, scaffold, level)
    if kind == "sound":
        v = 340.0
        f = v / lam
        text = (f"Two loudspeakers emit sound of frequency {_txt(f)} Hz (speed of sound 340 m/s). A microphone is {_txt(d1, 3)} m from one "
                f"speaker and {_txt(d2, 3)} m from the other. How many wavelengths are there in the path difference?")
        work = [_L(rf"\lambda = \frac{{v}}{{f}} = {_ltx(lam)}\ \mathrm{{m}}"), _L(rf"\text{{path difference}} = {_ltx(pd)}\ \mathrm{{m}}"), _L(rf"\frac{{{_ltx(pd)}}}{{{_ltx(lam)}}} = {k:g}")]
        opts = [{"value": k, "mistake": None, "working": work},
                {"value": _sig((d1 + d2) / lam), "mistake": "The path difference is the difference of the distances, not their sum.", "working": work},
                {"value": _sig(pd / (v * f)), "mistake": "Find λ = v ÷ f first, then divide the path difference by λ.", "working": work},
                {"value": _sig(pd * f / 1.0), "mistake": "Divide the path difference by the wavelength.", "working": work}]
        scaffold = [{"question": "What is the wavelength, in m?", "answer": _sig(lam)}, {"question": "What is the path difference, in m?", "answer": _sig(pd)}]
        return _q(text, k, "wavelengths", opts, QT, scaffold, level)
    inphase = float(k).is_integer()
    ans = "In phase — a whole number of wavelengths." if inphase else "Out of phase — a whole number + ½ wavelengths."
    wrong = [("Out of phase — a whole number + ½ wavelengths." if inphase else "In phase — a whole number of wavelengths.", "Whole number of wavelengths → in phase; whole number + ½ → out of phase."),
             ("In phase — the distances are different so the waves are in step." if not inphase else "Out of phase — the distances are different.", "Compare the path difference with λ; different distances don't by themselves mean out of phase.")]
    text = base + " State whether the waves arrive at P in phase or out of phase."
    return _choice(text, ans, wrong, QT, level)


# ════════════════ 4 — Waves meeting and diffraction ════════════════
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


# ════════════════ 5 — Sine and angles ════════════════
def gen_ip_sine(level="Higher"):
    kind = random.choice(["angle", "opposite", "solve", "solve"])
    if kind == "angle":
        th = random.choice([15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 55.0])
        s = round(math.sin(math.radians(th)), 3)
        ans = round(math.degrees(math.asin(s)), 1)
        text = f"In a right-angled triangle sin θ = {s:g}. Calculate the angle θ, in degrees."
        work = [_L(rf"\theta = \sin^{{-1}}({s:g}) = {ans:g}^\circ")]
        opts = [{"value": ans, "mistake": None, "working": work},
                {"value": round(math.asin(s), 3), "mistake": "Your calculator is in radian mode — set it to degrees.", "working": work},
                {"value": round(math.degrees(math.acos(s)), 1), "mistake": "Use sin⁻¹ (not cos⁻¹).", "working": work},
                {"value": round(s, 3), "mistake": "That is sin θ — you need the angle: θ = sin⁻¹(sin θ).", "working": work}]
        return _q(text, ans, "°", opts, QT, None, level)
    if kind == "opposite":
        h = random.choice([1.5, 2.0, 2.4, 3.0, 5.0])
        th = random.choice([20.0, 30.0, 40.0, 50.0])
        o = h * math.sin(math.radians(th))
        text = f"In a right-angled triangle the hypotenuse is {h:g} m and the angle θ is {th:g}°. Calculate the length of the side opposite θ."
        work = [_L(r"\sin\theta = \frac{\text{opposite}}{\text{hypotenuse}}"), _L(rf"\text{{opposite}} = {h:g} \times \sin {th:g}^\circ = {_ltx(o)}\ \mathrm{{m}}")]
        opts = [{"value": o, "mistake": None, "working": work},
                {"value": _sig(h / math.sin(math.radians(th))), "mistake": "opposite = hypotenuse × sin θ (multiply).", "working": work},
                {"value": _sig(h * math.cos(math.radians(th))), "mistake": "Opposite uses sin θ; cos θ gives the adjacent side.", "working": work},
                {"value": _sig(h * math.sin(th)), "mistake": "Your calculator is in radian mode — set it to degrees.", "working": work}]
        return _q(text, o, "m", opts, QT, None, level)
    a = random.choice([2.0, 2.5, 4.0, 5.0])
    b = round(a * random.choice([0.34, 0.5, 0.64, 0.77]), 1)
    s = b / a
    ans = round(math.degrees(math.asin(s)), 1)
    text = f"Calculate the angle θ in the equation  {_txt(a)} × 10⁻⁶ × sin θ = {_txt(b)} × 10⁻⁶."
    work = [_L(rf"\sin\theta = \frac{{{b:g}\times10^{{-6}}}}{{{a:g}\times10^{{-6}}}} = {_ltx(s)}"), _L(rf"\theta = {ans:g}^\circ")]
    opts = [{"value": ans, "mistake": None, "working": work},
            {"value": round(math.degrees(math.asin(min(1.0, a / b))) if a <= b else round(math.degrees(math.asin(min(1.0, s * s))), 1), 1), "mistake": "sin θ = (right-hand side) ÷ (number multiplying sin θ).", "working": work},
            {"value": round(math.asin(s), 3), "mistake": "Your calculator is in radian mode — set it to degrees.", "working": work},
            {"value": round(s, 3), "mistake": "That is sin θ — now take sin⁻¹ to find θ.", "working": work}]
    scaffold = [{"question": "What is sin θ?", "answer": _sig(s)}]
    return _q(text, ans, "°", opts, QT, scaffold, level)
