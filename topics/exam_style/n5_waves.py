"""N5 Waves — exam-style multi-part questions: wave speed, period & frequency, and combined.

Recognised wrong answers follow the N5 marking instructions and course reports: the echo distance
not halved, kHz/MHz/cm not converted, the number of waves miscounted from a diagram (crest to
crest), f and T confused, amplitude measured trough to crest, and f = N/t inverted.
"""
import random

from topics.exam_style.base import Exam, T, exam_style, fmt, ltx, pick, sig

UNIT = "Waves"
C = 3e8

NOTES = {
    "Wave Speed": r"""## Wave speed — exam technique

$v = f\lambda$ &nbsp; $d = vt$ &nbsp; $f = \frac{N}{t}$

- Echoes: the sound travels **there and back** — halve the distance (or double it).
- Convert kHz (× 10³), MHz (× 10⁶), GHz (× 10⁹) and cm → m.
- All electromagnetic waves travel at $3 \times 10^8$ m/s in a vacuum. Speed of sound in air ≈ 340 m/s, in water ≈ 1500 m/s.
""",
    "Period & Frequency": r"""## Period and frequency — exam technique

$T = \frac{1}{f}$ &nbsp; $f = \frac{N}{t}$ &nbsp; $v = f\lambda$

- **Frequency** = number of waves per second (Hz). **Period** = time for one wave (s).
- **Amplitude** = height from the middle (rest position) to a crest — not crest to trough.
- **Wavelength** = distance between successive crests.
""",
    "Waves Combined": r"""## Waves — exam technique

$v = f\lambda$ &nbsp; $d = vt$ &nbsp; $f = \frac{N}{t}$ &nbsp; $T = \frac{1}{f}$

- Transverse: vibrations at right angles to the direction of travel (water, light). Longitudinal: vibrations along the direction of travel (sound).
- **Diffraction**: waves spread out around obstacles / through gaps. **Longer** wavelengths diffract **more**.
- Waves transfer **energy** (not matter).
""",
}


def _ex(qtype, level):
    return Exam(UNIT, qtype, level, NOTES[qtype])


# ════════════════ Wave Speed ════════════════

def _ws_sonar(level="N5"):
    ex = _ex("Wave Speed", level)
    depth = pick(120, 150, 240, 375, 450, 600)
    t = 2 * depth / 1500
    ex.num(f"A pulse of ultrasound is sent down from the ship. The echo from the sea bed is received {t:g} s later. "
           f"Calculate the depth of the water.", depth, "m",
           wrong=[(1500 * t, "The pulse travels down AND back — halve the distance."), (1500 / t, "d = v × t."),
                  (340 * t / 2, "Use the speed of sound in WATER (1500 m/s).")],
           working=[r"d = vt", rf"d = 1500 \times {t:g} = {ltx(1500 * t)}\ \text{{m}}", rf"\text{{depth}} = \frac{{{ltx(1500 * t)}}}{{2}} = {depth}\ \text{{m}}"])
    f_k = pick(25, 30, 40, 50)
    lam = 1500 / (f_k * 1000)
    ex.num(f"The ultrasound has a frequency of {f_k} kHz. Calculate its wavelength in water.", lam, "m",
           wrong=[(1500 / f_k, "Convert kHz to Hz (× 1000)."), (1500 * f_k * 1000, "λ = v ÷ f.")],
           working=[r"v = f\lambda \Rightarrow \lambda = \frac{v}{f}", rf"\lambda = \frac{{1500}}{{{f_k} \times 10^3}} = {ltx(lam)}\ \text{{m}}"])
    ex.choice("What is ultrasound?", "Sound with a frequency above the range of human hearing (above 20 kHz).",
              [("Sound that travels faster than normal sound.", "It travels at the same speed in the same medium."),
               ("An electromagnetic wave used for imaging.", "Ultrasound is a sound (longitudinal, mechanical) wave."),
               ("Sound with a frequency below 20 Hz.", "That's infrasound.")])
    return ex.build("A ship uses sonar to measure the depth of the sea. The speed of sound in water is 1500 m/s.")


def _ws_radio(level="N5"):
    ex = _ex("Wave Speed", level)
    f_M = pick(88.6, 93.5, 97.4, 100.2, 105.8)
    lam = C / (f_M * 1e6)
    ex.num(f"A radio station broadcasts at {f_M:g} MHz. Calculate the wavelength of the radio waves.", lam, "m",
           wrong=[(C / f_M, "Convert MHz to Hz (× 10⁶)."), (C * f_M * 1e6, "λ = v ÷ f."), (340 / (f_M * 1e6), "Radio waves travel at 3 × 10⁸ m/s.")],
           working=[r"\lambda = \frac{v}{f}", rf"\lambda = \frac{{3 \times 10^8}}{{{f_M:g} \times 10^6}} = {ltx(lam)}\ \text{{m}}"])
    d_km = pick(36, 72, 150, 240)
    t = d_km * 1000 / C
    ex.num(f"Calculate the time taken for the signal to reach a radio {d_km} km from the transmitter.", t, "s",
           wrong=[(d_km / C, "Convert km to m."), (d_km * 1000 * C, "t = d ÷ v.")],
           working=[r"t = \frac{d}{v}", rf"t = \frac{{{d_km} \times 10^3}}{{3 \times 10^8}} = {ltx(t)}\ \text{{s}}"])
    ex.choice("Microwaves from the same transmitter have a much higher frequency. How does their speed compare with the radio waves?",
              "The same — all electromagnetic waves travel at the same speed in air (a vacuum).",
              [("Faster — higher frequency means higher speed.", "v = fλ: a higher f means a shorter λ, same v."),
               ("Slower — they have a shorter wavelength.", "All EM waves have the same speed in a vacuum."),
               ("Faster — microwaves have more energy.", "Energy depends on frequency; speed doesn't.")])
    return ex.build("Radio and microwave signals are sent from a transmitter mast. Speed of electromagnetic waves = 3.0 × 10⁸ m/s.")


def _ws_ripple(level="N5", qtype="Wave Speed"):
    ex = _ex(qtype, level)
    N, t = pick(12, 15, 20, 24, 30), pick(4, 5, 6, 8, 10)
    f = N / t
    n_w, d_cm = pick(3, 4, 5), pick(18, 24, 30, 36)
    lam = d_cm / 100 / n_w
    ex.num(f"{N} waves pass a point in {t} s. Calculate the frequency of the waves.", f, "Hz",
           wrong=[(t / N, "f = N ÷ t (that's the period)."), (N * t, "f = N ÷ t.")],
           working=[r"f = \frac{N}{t}", rf"f = \frac{{{N}}}{{{t}}} = {ltx(f)}\ \text{{Hz}}"])
    ex.num(f"The distance across {n_w} complete waves is {d_cm} cm. Calculate the wavelength, in metres.", lam, "m",
           wrong=[(d_cm / n_w, "Convert cm to m."), (d_cm / 100 / (n_w - 1), f"There are {n_w} complete waves in {d_cm} cm."),
                  (d_cm / 100, "Divide by the number of waves.")],
           working=[rf"\lambda = \frac{{{d_cm / 100:g}}}{{{n_w}}} = {ltx(lam)}\ \text{{m}}"])
    v = sig(f) * sig(lam)
    ex.num("Calculate the speed of the waves.", v, "m/s",
           wrong=[(sig(f) / sig(lam), "v = f × λ."), (sig(f) * d_cm / n_w, "Use the wavelength in metres.")],
           working=[r"v = f\lambda", rf"v = {ltx(f)} \times {ltx(lam)} = {ltx(v)}\ \text{{m/s}}"])
    return ex.build("A wave machine produces waves in a ripple tank.")


gen_wave_speed_exam = exam_style(_ws_sonar, _ws_radio, _ws_ripple)


# ════════════════ Period & Frequency ════════════════

def _pf_buoy(level="N5"):
    ex = _ex("Period & Frequency", level)
    N, t = pick(10, 12, 15, 20), pick(40, 48, 50, 60)
    f = N / t
    T_ = t / N
    ex.num(f"The buoy moves up and down {N} times in {t} s. Calculate the frequency of the waves.", f, "Hz",
           wrong=[(T_, "That's the period. f = N ÷ t."), (N * t, "f = N ÷ t.")],
           working=[rf"f = \frac{{N}}{{t}} = \frac{{{N}}}{{{t}}} = {ltx(f)}\ \text{{Hz}}"])
    ex.num("Calculate the period of the waves.", T_, "s",
           wrong=[(f, "T = 1 ÷ f."), (1 / T_ * 2, "T = 1 ÷ f.")],
           working=[rf"T = \frac{{1}}{{f}} = \frac{{1}}{{{ltx(f)}}} = {ltx(T_)}\ \text{{s}}"])
    lam = pick(6, 8, 10, 12, 15)
    v = lam / T_
    ex.num(f"The distance between neighbouring crests is {lam} m. Calculate the speed of the waves.", v, "m/s",
           wrong=[(lam * T_, "v = λ ÷ T (or v = fλ)."), (lam / f, "v = f × λ.")],
           working=[rf"v = f\lambda = {ltx(f)} \times {lam} = {ltx(v)}\ \text{{m/s}}"])
    ex.choice("What does the wave transfer from one place to another?", "Energy",
              [("Water", "The water mostly moves up and down — the buoy isn't carried along."), ("Mass", "Waves transfer energy, not matter."),
               ("Particles", "The particles oscillate about fixed positions.")])
    return ex.build("Water waves pass a buoy floating at sea.")


def _pf_trace(level="N5"):
    ex = _ex("Period & Frequency", level)
    T_ms = pick(2.0, 2.5, 4.0, 5.0, 8.0)
    T_ = T_ms / 1000
    f = 1 / T_
    ex.num(f"One complete wave on the display takes {T_ms:g} ms. Calculate the frequency of the sound.", f, "Hz",
           wrong=[(1 / T_ms, "Convert ms to s first."), (T_, "f = 1 ÷ T.")],
           working=[rf"T = {T_ms:g}\ \text{{ms}} = {ltx(T_)}\ \text{{s}}", rf"f = \frac{{1}}{{T}} = {ltx(f)}\ \text{{Hz}}"])
    lam = 340 / f
    ex.num("Calculate the wavelength of the sound in air (speed of sound = 340 m/s).", lam, "m",
           wrong=[(340 * f, "λ = v ÷ f."), (3e8 / f, "Sound travels at 340 m/s, not 3 × 10⁸ m/s.")],
           working=[rf"\lambda = \frac{{v}}{{f}} = \frac{{340}}{{{ltx(f)}}} = {ltx(lam)}\ \text{{m}}"])
    amp = pick(1.5, 2.0, 2.5, 3.0)
    ex.num(f"The trace measures {2 * amp:g} cm from the bottom of a trough to the top of a crest. State the amplitude of the trace, in cm.",
           amp, "cm", wrong=[(2 * amp, "Amplitude is measured from the middle (rest) line to a crest — half this.")],
           working=[rf"A = \frac{{{2 * amp:g}}}{{2}} = {amp:g}\ \text{{cm}}"])
    ex.choice("The sound is made louder but its pitch stays the same. What changes on the trace?",
              "The amplitude increases; the period (and frequency) stay the same.",
              [("The frequency increases.", "Pitch is set by frequency, which stays the same."),
               ("The period decreases.", "A shorter period would be a higher pitch."),
               ("The wavelength increases.", "Louder = bigger amplitude, not a longer wavelength.")])
    return ex.build("A microphone connected to an oscilloscope displays the sound wave from a tuning fork.")


gen_period_frequency_exam = exam_style(_pf_buoy, _pf_trace)


# ════════════════ Waves Combined ════════════════

def _wc_hills(level="N5"):
    ex = _ex("Waves Combined", level)
    f_lw = pick(198, 225, 252)
    lam = C / (f_lw * 1000)
    ex.num(f"A long-wave radio station broadcasts at {f_lw} kHz. Calculate the wavelength.", lam, "m",
           wrong=[(C / f_lw, "Convert kHz to Hz."), (C * f_lw * 1000, "λ = v ÷ f.")],
           working=[rf"\lambda = \frac{{v}}{{f}} = \frac{{3 \times 10^8}}{{{f_lw} \times 10^3}} = {ltx(lam)}\ \text{{m}}"])
    d = pick(45, 60, 90, 120)
    t = d * 1000 / C
    ex.num(f"The house is {d} km from the transmitter. Calculate the time for the signal to reach it.", t, "s",
           wrong=[(d / C, "Convert km to m.")],
           working=[rf"t = \frac{{d}}{{v}} = \frac{{{d} \times 10^3}}{{3 \times 10^8}} = {ltx(t)}\ \text{{s}}"])
    ex.choice("The house is behind a hill. It receives long-wave radio well but has poor TV reception. Why?",
              "Long-wave radio has a much longer wavelength, so it diffracts more around the hill.",
              [("TV signals travel slower than radio signals.", "All EM waves travel at the same speed."),
               ("Radio waves have a higher frequency, so they diffract more.", "Longer WAVELENGTH (lower frequency) diffracts more."),
               ("TV signals have a longer wavelength, so they can't bend.", "TV signals have the SHORTER wavelength.")])
    return ex.build("A house in a valley receives radio and television signals from a distant transmitter.")


def _wc_thunder(level="N5"):
    ex = _ex("Waves Combined", level)
    t = pick(3, 4.5, 6, 7.5, 9)
    d = 340 * t
    ex.num(f"A pupil hears thunder {t:g} s after seeing the lightning. Calculate how far away the storm is.", d, "m",
           wrong=[(3e8 * t, "The delay is due to the SOUND — use 340 m/s."), (340 / t, "d = v × t."), (d / 2, "The sound only travels one way — no halving.")],
           working=[r"d = vt", rf"d = 340 \times {t:g} = {ltx(d)}\ \text{{m}}"])
    ex.choice("Why is the lightning seen before the thunder is heard?",
              "Light travels much faster than sound.",
              [("The lightning happens first.", "They happen at the same time."), ("Sound is a transverse wave.", "Sound is longitudinal — but that's not the reason."),
               ("Light travels slower than sound.", "Light is far faster (3 × 10⁸ m/s).")])
    ex.choice("Which statement describes a sound wave?",
              "A longitudinal wave — the particles vibrate along the direction the wave travels.",
              [("A transverse wave — the particles vibrate at right angles to the direction of travel.", "That describes light or water waves."),
               ("An electromagnetic wave that can travel through a vacuum.", "Sound needs a medium."),
               ("A wave that transfers matter.", "Waves transfer energy.")])
    return ex.build("During a thunderstorm, lightning and thunder are produced at the same time. Speed of sound in air = 340 m/s.")


def _wc_ripple(level="N5"):
    return _ws_ripple(level, qtype="Waves Combined")


gen_waves_combined_exam = exam_style(_wc_hills, _wc_thunder, _wc_ripple)


EXAM = {
    "Wave Speed":         gen_wave_speed_exam,
    "Period & Frequency": gen_period_frequency_exam,
    "Waves Combined":     gen_waves_combined_exam,
}
