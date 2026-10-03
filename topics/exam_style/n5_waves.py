"""N5 Waves — exam-style questions that cut across the unit's topics, like SQA paper questions: wave speed, period & frequency, and combined.

Recognised wrong answers follow the N5 marking instructions and course reports: the echo distance
not halved, kHz/MHz/cm not converted, the number of waves miscounted from a diagram (crest to
crest), f and T confused, amplitude measured trough to crest, and f = N/t inverted.
"""
import random

from topics.exam_style.base import Exam, T, fmt, ltx, pick, sig

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

NOTES["Wave Parameters and Behaviours"] = r"""## Wave parameters — exam technique

$d = vt$ &nbsp; $v = f\lambda$ &nbsp; $T = \frac{1}{f}$ &nbsp; $f = \frac{N}{t}$ (t in seconds)

- Transverse: particles vibrate at 90° to the energy direction; longitudinal (sound): parallel to it.
- Amplitude = half the crest-to-trough height. Echoes: the wave goes there **and back**.
- Longer wavelength → more diffraction; diffracted waves keep the same wavelength.
"""
NOTES["Electromagnetic Spectrum"] = r"""## The electromagnetic spectrum — exam technique

Increasing wavelength: gamma, X-rays, ultraviolet, visible, infrared, microwaves, radio. All transverse, all 3.0 × 10⁸ m/s.

- Convert GHz/MHz/nm. Maximum wavelength ↔ minimum frequency.
- Name the **detector** (photodiode, CCD, GM tube, aerial…), not the device that contains it.
"""
NOTES["Refraction of Light"] = r"""## Refraction — exam technique

- Into a denser material: speed ↓, wavelength ↓, **frequency unchanged**, bends **towards** the normal (if the angle of incidence > 0°).
- Angles are measured from the **normal** (at 90° to the surface).
"""


def _ex(level):
    return Exam(UNIT, level, NOTES)


# ════════════════ Sonar: echo depth → frequency/period → wavelength ════════════════

def sonar(level="N5"):
    ex = _ex(level)
    depth = pick(120, 150, 240, 375, 450)
    t = 2 * depth / 1500
    ex.on("Wave Speed").num(f"An ultrasound pulse is sent down from the ship and its echo is received {t:g} s later. Calculate the depth of the sea.",
        depth, "m",
        wrong=[(1500 * t, "The pulse travels down AND back — halve the distance."), (340 * t / 2, "Use the speed of sound in WATER (1500 m/s)."),
               (1500 / t, "d = v × t.")],
        working=[rf"d = vt = 1500 \times {t:g} = {ltx(1500 * t)}\ \text{{m}}", rf"\text{{depth}} = \frac{{{ltx(1500 * t)}}}{{2}} = {depth}\ \text{{m}}"])
    T_us = pick(20, 25, 40, 50)
    f = 1 / (T_us * 1e-6)
    ex.on("Period & Frequency").num(f"Each ultrasound wave has a period of {T_us} μs. Calculate the frequency.", f, "Hz",
        wrong=[(1 / T_us, "Convert μs to s (× 10⁻⁶)."), (T_us * 1e-6, "f = 1 ÷ T.")],
        working=[rf"f = \frac{{1}}{{T}} = \frac{{1}}{{{T_us}\times10^{{-6}}}} = {ltx(f)}\ \text{{Hz}}"])
    lam = 1500 / sig(f)
    ex.on("Wave Speed").num("Calculate the wavelength of the ultrasound in water.", lam, "m",
        wrong=[(1500 * sig(f), "λ = v ÷ f."), (340 / sig(f), "Use 1500 m/s in water.")],
        working=[rf"\lambda = \frac{{v}}{{f}} = \frac{{1500}}{{{ltx(f)}}} = {ltx(lam)}\ \text{{m}}"])
    ex.on("Definitions").choice("What is ultrasound?", "Sound with a frequency above the range of human hearing (above 20 kHz).",
        [("Sound that travels faster than ordinary sound.", "Same speed in the same medium."),
         ("An electromagnetic wave.", "It's a sound wave — longitudinal and needs a medium."),
         ("Sound below 20 Hz.", "That's infrasound.")])
    return ex.build("A ship uses sonar to measure the depth of the sea. Speed of sound in water = 1500 m/s.")


# ════════════════ Radio in a valley: wavelength → period → travel time → diffraction ════════════════

def radio_valley(level="N5"):
    ex = _ex(level)
    f_k = pick(198, 225, 252)
    f = f_k * 1000
    lam = C / f
    ex.on("Wave Speed").num(f"A long-wave radio station broadcasts at {f_k} kHz. Calculate the wavelength.", lam, "m",
        wrong=[(C / f_k, "Convert kHz to Hz."), (C * f, "λ = v ÷ f."), (340 / f, "Radio waves travel at 3 × 10⁸ m/s.")],
        working=[rf"\lambda = \frac{{v}}{{f}} = \frac{{3\times10^8}}{{{f_k}\times10^3}} = {ltx(lam)}\ \text{{m}}"])
    ex.on("Period & Frequency").num("Calculate the period of the radio waves.", 1 / f, "s",
        wrong=[(1 / f_k, "Convert kHz to Hz."), (f, "T = 1 ÷ f.")],
        working=[rf"T = \frac{{1}}{{f}} = \frac{{1}}{{{f_k}\times10^3}} = {ltx(1 / f)}\ \text{{s}}"])
    d = pick(45, 60, 90, 120)
    ex.on("Wave Speed").num(f"The house is {d} km from the transmitter. Calculate the time for the signal to reach it.", d * 1000 / C, "s",
        wrong=[(d / C, "Convert km to m."), (d * 1000 * C, "t = d ÷ v.")],
        working=[rf"t = \frac{{d}}{{v}} = \frac{{{d}\times10^3}}{{3\times10^8}} = {ltx(d * 1000 / C)}\ \text{{s}}"])
    ex.on("Waves Combined").choice("The house is behind a hill and gets good long-wave radio but poor TV reception. Why?",
        "Long-wave radio has a much longer wavelength, so it diffracts more around the hill.",
        [("TV signals travel more slowly.", "All EM waves travel at the same speed."),
         ("Higher-frequency waves diffract more.", "LONGER wavelengths (lower frequency) diffract more."),
         ("TV signals have the longer wavelength.", "TV signals have the shorter wavelength.")])
    return ex.build("A house in a valley receives radio and TV signals from a distant transmitter. Speed of EM waves = 3.0 × 10⁸ m/s.")


# ════════════════ Waves at the beach: f = N/t → T → λ → v → time ════════════════

def beach_waves(level="N5"):
    ex = _ex(level)
    N, t = pick(10, 12, 15, 20), pick(40, 48, 50, 60)
    f = N / t
    ex.on("Period & Frequency").num(f"{N} waves pass the end of a pier in {t} s. Calculate the frequency of the waves.", f, "Hz",
        wrong=[(t / N, "That's the period. f = N ÷ t."), (N * t, "f = N ÷ t.")],
        working=[rf"f = \frac{{N}}{{t}} = \frac{{{N}}}{{{t}}} = {ltx(f)}\ \text{{Hz}}"])
    ex.on("Period & Frequency").num("Calculate the period of the waves.", t / N, "s",
        wrong=[(f, "T = 1 ÷ f.")], working=[rf"T = \frac{{1}}{{f}} = {ltx(t / N)}\ \text{{s}}"])
    n_w, D = pick(3, 4, 5), pick(18, 24, 30, 36)
    lam = D / n_w
    ex.on("Waves Combined").num(f"The distance from the first crest to the last across {n_w} complete waves is {D} m. Calculate the wavelength.",
        lam, "m", wrong=[(D / (n_w + 1), f"{n_w} complete waves span {D} m."), (D, "Divide by the number of waves.")],
        working=[rf"\lambda = \frac{{{D}}}{{{n_w}}} = {ltx(lam)}\ \text{{m}}"])
    v = sig(f) * lam
    ex.on("Wave Speed").num("Calculate the speed of the waves.", v, "m/s",
        wrong=[(sig(f) / lam, "v = f × λ."), (lam / sig(f) if sig(f) != 1 else lam * 2, "v = f × λ.")],
        working=[rf"v = f\lambda = {ltx(f)} \times {ltx(lam)} = {ltx(v)}\ \text{{m/s}}"])
    ex.on("Waves Combined").choice("What do the waves transfer towards the beach?", "Energy",
        [("Water", "The water mostly moves up and down."), ("Mass", "Waves transfer energy, not matter."),
         ("Particles", "Particles oscillate about fixed positions.")])
    return ex.build("Water waves travel towards a beach.")


# ════════════════ Thunderstorm: distance → sound wavelength → wave type ════════════════

def thunderstorm(level="N5"):
    ex = _ex(level)
    t = pick(3, 4.5, 6, 7.5, 9)
    d = 340 * t
    ex.on("Wave Speed").num(f"Thunder is heard {t:g} s after the lightning is seen. Calculate how far away the lightning struck.", d, "m",
        wrong=[(C * t, "The delay is the SOUND's travel time — use 340 m/s."), (340 / t, "d = v × t."), (d / 2, "The sound travels one way only.")],
        working=[rf"d = vt = 340 \times {t:g} = {ltx(d)}\ \text{{m}}"])
    ex.on("Waves Combined").choice("Why is the lightning seen before the thunder is heard?", "Light travels much faster than sound.",
        [("The lightning happens first.", "They happen together."), ("Sound is a transverse wave.", "Not the reason (and it's longitudinal)."),
         ("Light travels slower than sound.", "Light is much faster.")])
    f = pick(50, 85, 100, 170)
    ex.on("Wave Speed").num(f"A rumble of thunder has a frequency of {f} Hz. Calculate its wavelength.", 340 / f, "m",
        wrong=[(340 * f, "λ = v ÷ f."), (C / f, "Sound travels at 340 m/s.")],
        working=[rf"\lambda = \frac{{340}}{{{f}}} = {ltx(340 / f)}\ \text{{m}}"])
    ex.on("Period & Frequency").num("Calculate the period of this sound wave.", 1 / f, "s",
        wrong=[(f, "T = 1 ÷ f.")], working=[rf"T = \frac{{1}}{{{f}}} = {ltx(1 / f)}\ \text{{s}}"])
    ex.on("Waves Combined").choice("Which describes a sound wave?",
        "Longitudinal — the particles vibrate along the direction the wave travels.",
        [("Transverse — the particles vibrate at right angles to the direction of travel.", "That's light or water waves."),
         ("Electromagnetic — it can travel through a vacuum.", "Sound needs a medium."),
         ("It transfers matter from the storm.", "Waves transfer energy.")])
    return ex.build("During a storm, lightning and thunder are produced at the same moment. Speed of sound in air = 340 m/s.")


# ════════════════ Golf rangefinder: EM band → frequency → reflected pulse → refraction in the lens ════════════════

def rangefinder(level="N5"):
    ex = _ex(level)
    nm = pick(850, 905, 940)
    f = C / (nm * 1e-9)
    ex.on("Electromagnetic Spectrum").choice(f"The rangefinder emits radiation of wavelength {nm} nm. Which band is this?", "infrared",
        [("ultraviolet", "UV is shorter than visible light (about 10–400 nm)."), ("microwaves", "Microwaves are mm to cm."), ("visible light", "Visible is about 400–700 nm.")])
    ex.on("Electromagnetic Spectrum").num("Calculate the frequency of this radiation.", f, "Hz",
        wrong=[(C / nm, "Convert nm to m (× 10⁻⁹) — course report 2025."), (340 / (nm * 1e-9), "Use the speed of light.")],
        working=[r"v = f\lambda", rf"f = \frac{{3.0\times10^8}}{{{nm}\times10^{{-9}}}} = {ltx(f)}\ \text{{Hz}}"])
    d = pick(120, 150, 180, 210)
    t = 2 * d / C
    ex.on("Wave Parameters and Behaviours").num(f"A pulse reflects from a flag and returns {fmt(t)} s after it is sent. Calculate the distance to the flag.", d, "m",
        wrong=[(2 * d, "The pulse goes there AND back — halve it (course report 2025)."), (340 * t / 2, "Use the speed of light.")],
        working=[rf"d = vt = 3.0\times10^8 \times {ltx(t)} = {2 * d}\ \text{{m (there and back)}}", rf"\text{{distance}} = {d}\ \text{{m}}"])
    ex.on("Electromagnetic Spectrum").choice("Which is a suitable detector for the rangefinder's radiation?", "a photodiode",
        [("photographic film", "Detects IR, but not suitable for an instant electronic reading (course report 2025)."),
         ("a black-bulb thermometer", "Far too slow for this application."), ("a Geiger-Müller tube", "That detects gamma radiation.")])
    ex.on("Refraction of Light").choice("The pulse passes through the centre of the rangefinder's lens along its axis. Why doesn't its direction change?",
        "It meets the lens surfaces along the normal (angle of incidence 0°), so only its speed changes.",
        [("It does not slow down in the lens.", "It does slow down — only the direction is unchanged (course report 2024)."),
         ("Infrared cannot be refracted.", "All light is refracted."), ("Its frequency changes instead.", "The frequency never changes.")])
    return ex.build("Golfers use an infrared laser rangefinder to measure the distance to the flag. Speed of light = 3.0 × 10⁸ m/s.")


# ════════════════ Ripple tank: f = N/t → wavelength → speed → diffraction ════════════════

def ripple_tank(level="N5"):
    ex = _ex(level)
    N, t = pick((20, 8), (25, 10), (30, 12))
    f = N / t
    ex.on("Wave Parameters and Behaviours").num(f"{N} waves are produced in {t} s. Calculate the frequency of the waves.", f, "Hz",
        wrong=[(t / N, "f = N ÷ t."), (N, "Divide by the time.")], working=[rf"f = \frac{{N}}{{t}} = \frac{{{N}}}{{{t}}} = {fmt(f)}\ \text{{Hz}}"])
    n, L = pick((4, 0.12), (5, 0.20), (6, 0.18))
    lam = L / n
    ex.on("Wave Parameters and Behaviours").num(f"The distance across {n} complete waves is {L:g} m. Calculate the wavelength.", lam, "m",
        wrong=[(L / (n + 1), f"There are exactly {n} wavelengths."), (L * n, "Divide the distance by the number of waves.")],
        working=[rf"\lambda = \frac{{{L:g}}}{{{n}}} = {fmt(lam)}\ \text{{m}}"])
    v = f * lam
    ex.on("Wave Parameters and Behaviours").num("Calculate the speed of the waves.", v, "m/s",
        wrong=[(f / lam, "v = f × λ."), (lam / f, "v = f × λ.")], working=[rf"v = f\lambda = {fmt(f)} \times {fmt(lam)} = {fmt(v)}\ \text{{m/s}}"])
    ex.on("Wave Parameters and Behaviours").choice("The waves pass through a gap about the same size as their wavelength. What do they do?",
        "They spread out in curved wavefronts with the same wavelength.",
        [("They spread out and their wavelength gets shorter.", "The wavelength is unchanged (course reports 2017, 2022)."),
         ("They pass straight through without spreading.", "A gap similar to the wavelength gives a lot of diffraction."),
         ("They slow down and change direction.", "That's refraction.")])
    ex.on("Wave Parameters and Behaviours").choice("Water waves are an example of which type of wave?", "Transverse — the water vibrates at 90° to the direction of energy transfer.",
        [("Longitudinal — the water vibrates along the direction of energy transfer.", "That's sound."),
         ("Transverse — the wave moves up and down.", "Describe the vibration relative to the energy direction (course report 2025)."),
         ("Electromagnetic.", "Water waves are mechanical.")])
    return ex.build("A student investigates water waves in a ripple tank.")


SCENARIOS = {
    "Sonar":            sonar,
    "Radio in a Valley": radio_valley,
    "Waves at the Beach": beach_waves,
    "Thunderstorm":     thunderstorm,
    "Laser Rangefinder": rangefinder,
    "Ripple Tank":       ripple_tank,
}
