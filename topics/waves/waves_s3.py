"""S3 (BGE) Waves question generators — match the S3 Wave Characteristics worksheets.

Equations are only those on the S3 relationships sheet: f = N/t, T = 1/f, v = d/t, v = fλ.
Every context is a tuple so the object and its numbers always go together, and every number is
chosen so the answer is clean (no unit prefixes, no e-notation)."""
import math
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question
from utils.notes import NOTES

TOPIC = "Waves"


# ── helpers ──────────────────────────────────────────────────────────────────
def _n(x):
    """Pupil-facing number: no e-notation, spaces in thousands, trailing zeros trimmed."""
    x = float(x)
    if abs(x - round(x)) < 1e-9:
        v = int(round(x))
        return f"{v:,}".replace(",", " ") if abs(v) >= 10000 else str(v)
    return format(round(x, 6), "f").rstrip("0").rstrip(".")


def _nl(x):
    return _n(x).replace(" ", r"\ ")


def _lt(s):
    return {"type": "latex", "content": s}


def _numeric(question, correct, wrong, unit, working, qtype, scaffold=None, notes="waves_s3", level="S3"):
    """wrong: list of (value, mistake). Builds the options, drops duplicates / non-positive values and pads to 3 distractors."""
    correct = float(correct)
    opts = [{"value": correct, "display": f"{_n(correct)} {unit}".strip(), "mistake": None, "working": working}]

    def clash(v):
        return any(math.isclose(v, float(o["value"]), rel_tol=1e-4) for o in opts)

    for v, why in wrong:
        v = round(float(v), 6)
        if v > 0 and not clash(v):
            opts.append({"value": v, "display": f"{_n(v)} {unit}".strip(), "mistake": why, "working": working})
    for v, why in ((correct * 2, "Check your arithmetic: this is double the correct value."),
                   (correct / 2, "Check your arithmetic: this is half the correct value."),
                   (correct * 10, "Check your arithmetic: this is 10 times too big."),
                   (correct / 10, "Check your arithmetic: this is 10 times too small.")):
        v = round(v, 6)
        if len(opts) < 4 and v > 0 and not clash(v):
            opts.append({"value": v, "display": f"{_n(v)} {unit}".strip(), "mistake": why, "working": working})
    return make_question(question, correct, opts, unit, scaffold=scaffold, notes=NOTES[notes],
                         topic=TOPIC, question_type=qtype, level=level)


def _mc(text, correct, wrong, qtype, notes="waves_s3", level="S3"):
    """Multiple-choice (word answers): wrong = [(option, why it's wrong), ...]."""
    distractors = [{"value": w, "mistake": why, "working": []} for w, why in wrong]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(question_text=text, correct_answer=correct, unit="", distractors=distractors, working=[],
                           notes=NOTES[notes], topic=TOPIC, question_type=qtype, level=level,
                           metadata={"type": "classification", "options": options})


# ═════════════════════════════════════════════════════════════════════════════
# Wave Properties
# ═════════════════════════════════════════════════════════════════════════════
_PROP = [
    ("a water wave in a ripple tank", "cm", [1, 2, 3, 4, 5]),
    ("a wave on a rope", "cm", [2, 3, 4, 5, 10]),
    ("a wave on a slinky spring", "cm", [2, 4, 6, 8]),
    ("a wave at sea off the Butt of Lewis", "m", [1, 2, 3, 4, 5]),
]


def gen_amplitude_from_crest_to_trough(level="S3"):
    obj, unit, amps = random.choice(_PROP)
    A = random.choice(amps)
    ctt = 2 * A
    q = (f"The vertical distance from a crest to a trough on {obj} is {_n(ctt)} {unit}.\n\n"
         f"What is the amplitude of the wave?")
    working = [{"type": "text", "content": "The amplitude is HALF the vertical distance from a crest to a trough."},
               _lt(rf"A = \frac{{{_n(ctt)}}}{{2}} = {_n(A)}\ \mathrm{{{unit}}}")]
    wrong = [(ctt, "You gave the whole crest-to-trough distance. The amplitude is only half of it."),
             (ctt * 2, "You doubled the distance. The amplitude is half of the crest-to-trough distance."),
             (A / 2, "You halved it twice. The amplitude is half the crest-to-trough distance (halve once).")]
    return _numeric(q, A, wrong, unit, working, "Wave Properties")


def gen_crest_to_trough_from_amplitude(level="S3"):
    obj, unit, amps = random.choice(_PROP)
    A = random.choice(amps)
    ctt = 2 * A
    q = (f"{obj[0].upper() + obj[1:]} has an amplitude of {_n(A)} {unit}.\n\n"
         f"What is the vertical distance from a crest to a trough?")
    working = [{"type": "text", "content": "The crest-to-trough distance is TWICE the amplitude."},
               _lt(rf"{_n(A)} \times 2 = {_n(ctt)}\ \mathrm{{{unit}}}")]
    wrong = [(A, "You gave the amplitude. The crest-to-trough distance is twice the amplitude."),
             (A * 4, "You multiplied by 4. The crest-to-trough distance is twice the amplitude."),
             (A / 2, "You halved the amplitude. Double it to get the crest-to-trough distance.")]
    return _numeric(q, ctt, wrong, unit, working, "Wave Properties")


_WL = [("a rope", "cm", [10, 12, 15, 20, 25]), ("a ripple tank", "cm", [2, 3, 4, 5, 6]),
       ("a slinky spring", "cm", [4, 5, 6, 8]), ("a pond", "m", [1, 2, 3, 4])]


def gen_wavelength_from_several_waves(level="S3"):
    obj, unit, wls = random.choice(_WL)
    lam = random.choice(wls)
    n = random.choice([2, 3, 4, 5, 6])
    L = lam * n
    q = (f"{n} complete waves on {obj} measure {_n(L)} {unit} from one end of the wave pattern to the other.\n\n"
         f"Calculate the wavelength of the waves.")
    working = [_lt(rf"\lambda = \frac{{\text{{length}}}}{{\text{{number of waves}}}} = \frac{{{_n(L)}}}{{{n}}} = {_n(lam)}\ \mathrm{{{unit}}}")]
    wrong = [(L, "You gave the length of the whole pattern. Divide by the number of waves."),
             (L * n, "You multiplied. Divide the length by the number of waves."),
             (L / (n + 1), f"You divided by {n + 1}. Divide by the number of complete waves ({n}).")]
    return _numeric(q, lam, wrong, unit, working, "Wave Properties")


_UNITS = [("frequency", "hertz (Hz)"), ("wavelength", "metre (m)"), ("amplitude", "metre (m)"),
          ("period", "second (s)"), ("wave speed", "metres per second (m/s)")]


def gen_unit_of_quantity(level="S3"):
    qty, unit = random.choice(_UNITS)
    pool = ["hertz (Hz)", "metre (m)", "second (s)", "metres per second (m/s)"]
    wrong_units = [u for u in pool if u != unit]
    why = {"hertz (Hz)": "Hertz is the unit of frequency (waves per second).",
           "metre (m)": "Metres measure a distance such as wavelength or amplitude.",
           "second (s)": "Seconds measure time, such as the period.",
           "metres per second (m/s)": "Metres per second is the unit of speed."}
    return _mc(f"What is the unit of {qty}?", unit, [(u, why[u]) for u in wrong_units], "Wave Properties")


_FACTS = [
    ("Which of these is a longitudinal wave?", "Sound",
     [("Light", "Light is a transverse wave."), ("Water waves", "Water waves are transverse."), ("A wave on a rope shaken up and down", "That is a transverse wave.")]),
    ("Which of these is a transverse wave?", random.choice(["Light", "Water waves", "A wave on a rope shaken up and down"]),
     [("Sound", "Sound is longitudinal."), ("A sound wave from a loudspeaker", "Sound is longitudinal."), ("A wave on a slinky pushed back and forth along its length", "That is longitudinal.")]),
    ("In a transverse wave the oscillations are…", "perpendicular (at right angles) to the direction the wave travels",
     [("parallel to the direction the wave travels", "That describes a longitudinal wave."), ("in a circle around the direction of travel", "Transverse oscillations are at right angles to the direction of travel."), ("in the same direction as the energy transfer", "That is longitudinal: transverse oscillations are perpendicular.")]),
    ("In a longitudinal wave the oscillations are…", "parallel to the direction the wave travels",
     [("perpendicular to the direction the wave travels", "That describes a transverse wave."), ("always up and down", "Longitudinal oscillations are back and forth along the direction of travel."), ("too small to measure", "They are not small: they are parallel to the direction of travel.")]),
    ("A wave transfers…", "energy from one place to another",
     [("matter from one place to another", "Waves transfer energy, not matter."), ("particles from one place to another", "The particles only oscillate around a fixed point."), ("water from one place to another", "A cork floats in place as a wave passes: the water is not carried along.")]),
    ("A cork floats on the sea. As waves pass it bobs up and down but stays in about the same place. This shows that waves transfer…", "energy but not matter",
     [("matter and energy", "The cork (matter) is not carried along."), ("matter but not energy", "Waves do transfer energy."), ("neither matter nor energy", "Waves transfer energy.")]),
    ("Which of these is the amplitude of a wave?", "half the vertical distance from a crest to a trough",
     [("the distance from one crest to the next crest", "That is the wavelength."), ("the vertical distance from a crest to a trough", "That is twice the amplitude."), ("the number of waves each second", "That is the frequency.")]),
    ("Which of these is the wavelength of a wave?", "the distance from one crest to the next crest",
     [("half the vertical distance from a crest to a trough", "That is the amplitude."), ("the time to make one complete wave", "That is the period."), ("the number of waves each second", "That is the frequency.")]),
    ("What is the frequency of a wave?", "the number of waves each second",
     [("the time taken for one wave", "That is the period."), ("the distance from crest to crest", "That is the wavelength."), ("the distance the wave travels each second", "That is the wave speed.")]),
    ("What is the highest point of a transverse wave called?", "a crest",
     [("a trough", "A trough is the lowest point."), ("the amplitude", "Amplitude is a distance, not a point."), ("the wavelength", "Wavelength is a distance, not a point.")]),
]


def gen_wave_facts(level="S3"):
    text, correct, wrong = random.choice(_FACTS)
    if text.startswith("Which of these is a transverse"):
        correct = random.choice(["Light", "Water waves", "A wave on a rope shaken up and down"])
    return _mc(text, correct, wrong, "Wave Properties")


# ═════════════════════════════════════════════════════════════════════════════
# Period & Frequency   (f = N/t,  T = 1/f)
# ═════════════════════════════════════════════════════════════════════════════
# (phrase for "N ___ in t seconds", plural noun, frequencies, times) — every f x t gives a whole number of waves
_COUNT = [
    ("waves break on the beach at Luskentyre", [0.25, 0.5, 1, 2], [20, 40, 60, 100]),
    ("waves pass the pier at Tarbert", [0.2, 0.25, 0.5, 1], [20, 40, 60, 100]),
    ("waves pass a buoy in Stornoway harbour", [0.2, 0.5, 1], [10, 20, 40, 60]),
    ("waves are made by a dipper in a ripple tank", [5, 10, 15, 20], [10, 20, 30, 60]),
    ("waves are made on a rope", [2, 2.5, 4, 5], [10, 12, 20, 30]),
    ("waves are made by a vibrating string", [100, 250, 400, 500], [2, 4, 5, 10]),
]


def _draw_count():
    phrase, fs, ts = random.choice(_COUNT)
    for _ in range(50):
        f, t = random.choice(fs), random.choice(ts)
        N = f * t
        if abs(N - round(N)) < 1e-9 and N >= 2:
            return phrase, f, t, int(round(N))
    return phrase, fs[0], ts[0], int(round(fs[0] * ts[0]))


def gen_find_frequency(level="S3"):
    phrase, f, t, N = _draw_count()
    q = f"{N} {phrase} in {_n(t)} seconds.\n\nCalculate the frequency of the waves."
    working = [_lt(r"f = \frac{N}{t}"), _lt(rf"f = \frac{{{N}}}{{{_n(t)}}}"), _lt(rf"f = {_n(f)}\ \mathrm{{Hz}}")]
    wrong = [(t / N, "You divided time by the number of waves. Frequency = N ÷ t."), (N * t, "You multiplied. Frequency = N ÷ t."),
             (N + t, "You added. Frequency = N ÷ t.")]
    return _numeric(q, f, wrong, "Hz", working, "Period & Frequency")


def gen_find_number_of_waves(level="S3"):
    phrase, f, t, N = _draw_count()
    q = f"The frequency of the waves is {_n(f)} Hz. How many waves are made in {_n(t)} seconds?"
    working = [_lt(r"f = \frac{N}{t}"), _lt(rf"{_n(f)} = \frac{{N}}{{{_n(t)}}}"), _lt(rf"N = {_n(f)} \times {_n(t)} = {N}")]
    wrong = [(f / t, "You divided. Rearrange f = N ÷ t to N = f × t."), (t / f, "You divided time by frequency. N = f × t."), (f + t, "You added. N = f × t.")]
    return _numeric(q, N, wrong, "waves", working, "Period & Frequency")


def gen_find_time(level="S3"):
    phrase, f, t, N = _draw_count()
    q = f"The frequency of some waves is {_n(f)} Hz. How long does it take for {N} waves to pass?"
    working = [_lt(r"f = \frac{N}{t}"), _lt(rf"{_n(f)} = \frac{{{N}}}{{t}}"), _lt(rf"t = \frac{{{N}}}{{{_n(f)}}} = {_n(t)}\ \mathrm{{s}}")]
    wrong = [(f / N, "You divided f by N. Rearrange f = N ÷ t to t = N ÷ f."), (N * f, "You multiplied. t = N ÷ f."), (N - f, "You subtracted. t = N ÷ f.")]
    return _numeric(q, t, wrong, "s", working, "Period & Frequency")


_PERIOD_F = [(0.5, "a wave"), (2, "a wave"), (4, "a water wave"), (5, "a wave on a rope"), (10, "a vibrating tuning fork"),
             (20, "a wave on a string"), (25, "a vibrating string"), (50, "the mains electricity supply"), (100, "a vibrating tuning fork"),
             (250, "a sound wave"), (500, "a sound wave")]


def gen_find_period(level="S3"):
    f, obj = random.choice(_PERIOD_F)
    T = 1 / f
    q = f"{obj[0].upper() + obj[1:]} has a frequency of {_n(f)} Hz.\n\nCalculate its period."
    working = [_lt(r"T = \frac{1}{f}"), _lt(rf"T = \frac{{1}}{{{_n(f)}}}"), _lt(rf"T = {_n(T)}\ \mathrm{{s}}")]
    wrong = [(f, "You used T = f. The period is 1 ÷ the frequency."), (T * 10, "Check your arithmetic: this is 10 times too big."),
             (T / 10, "Check your arithmetic: this is 10 times too small.")]
    return _numeric(q, T, wrong, "s", working, "Period & Frequency")


_PERIOD_T = [(0.5, "a wave"), (0.25, "a water wave"), (0.2, "a wave on a rope"), (0.1, "a wave on a string"), (0.05, "a wave"),
             (0.02, "the mains electricity supply"), (0.01, "a vibrating string"), (0.004, "a sound wave"), (0.002, "a tuning fork")]


def gen_find_frequency_from_period(level="S3"):
    T, obj = random.choice(_PERIOD_T)
    f = 1 / T
    q = f"{obj[0].upper() + obj[1:]} has a period of {_n(T)} s.\n\nCalculate its frequency."
    working = [_lt(r"T = \frac{1}{f}"), _lt(rf"{_n(T)} = \frac{{1}}{{f}}"), _lt(rf"f = \frac{{1}}{{{_n(T)}}} = {_n(f)}\ \mathrm{{Hz}}")]
    wrong = [(T, "You used f = T. Rearrange T = 1 ÷ f to f = 1 ÷ T."), (f * 10, "Check your arithmetic: this is 10 times too big."),
             (f / 10, "Check your arithmetic: this is 10 times too small.")]
    return _numeric(q, f, wrong, "Hz", working, "Period & Frequency")


def gen_period_from_count(level="S3"):
    phrase, f, t, N = _draw_count()
    T = 1 / f
    q = f"{N} {phrase} in {_n(t)} seconds.\n\nCalculate the period of the waves."
    working = [_lt(r"f = \frac{N}{t}"), _lt(rf"f = \frac{{{N}}}{{{_n(t)}}} = {_n(f)}\ \mathrm{{Hz}}"), _lt(r"T = \frac{1}{f}"),
               _lt(rf"T = \frac{{1}}{{{_n(f)}}} = {_n(T)}\ \mathrm{{s}}")]
    wrong = [(f, "You stopped at the frequency. The question asks for the period: T = 1 ÷ f."), (N * t, "You multiplied N × t. First find f = N ÷ t, then T = 1 ÷ f."),
             (T * 10, "Check your arithmetic: this is 10 times too big.")]
    sc = [{"question": "What is the frequency f of the waves?", "answer": f, "unit": "Hz"}, {"question": "What is the period T?", "answer": T, "unit": "s"}]
    return _numeric(q, T, wrong, "s", working, "Period & Frequency", scaffold=sc)


def gen_waves_in_time_from_period(level="S3"):
    f, obj = random.choice([(2, "a wave"), (4, "a water wave"), (5, "a wave on a rope"), (10, "a vibrating string"), (20, "a wave on a string"), (50, "a vibrating string")])
    T = 1 / f
    t = random.choice([10, 20, 30, 60])
    N = f * t
    q = f"{obj[0].upper() + obj[1:]} has a period of {_n(T)} s.\n\nHow many waves pass a point in {t} seconds?"
    working = [_lt(r"T = \frac{1}{f}"), _lt(rf"{_n(T)} = \frac{{1}}{{f}} \Rightarrow f = {_n(f)}\ \mathrm{{Hz}}"), _lt(r"f = \frac{N}{t}"),
               _lt(rf"N = {_n(f)} \times {t} = {_n(N)}")]
    wrong = [(T * t, "You multiplied the period by the time. Find f = 1 ÷ T first, then N = f × t."), (f, "You stopped at the frequency. N = f × t."),
             (t / f, "You divided t by f. N = f × t.")]
    sc = [{"question": "What is the frequency f?", "answer": f, "unit": "Hz"}, {"question": "How many waves pass in the time?", "answer": N, "unit": "waves"}]
    return _numeric(q, N, wrong, "waves", working, "Period & Frequency", scaffold=sc)


# ═════════════════════════════════════════════════════════════════════════════
# Wave Speed   (v = d/t,  v = fλ)
# ═════════════════════════════════════════════════════════════════════════════
# (object, speeds, times) — d = v t
_DT = [
    ("A ripple on a pond", [0.5, 1, 1.5, 2], [4, 8, 10, 20]),
    ("A wave on a rope", [2, 4, 5, 10], [2, 3, 5, 6]),
    ("A water wave heading for the harbour wall at Scalpay", [2, 3, 4, 5], [10, 20, 30, 60]),
    ("A sound wave in air", [340], [2, 3, 4, 5]),
    ("A wave on a slinky spring", [1, 2, 4], [2, 3, 5]),
]


def _draw_dt():
    obj, vs, ts = random.choice(_DT)
    v, t = random.choice(vs), random.choice(ts)
    return obj, v, t, v * t


def gen_speed_from_distance_time(level="S3"):
    obj, v, t, d = _draw_dt()
    q = f"{obj} travels {_n(d)} m in {_n(t)} seconds.\n\nCalculate the speed of the wave."
    working = [_lt(r"v = \frac{d}{t}"), _lt(rf"v = \frac{{{_n(d)}}}{{{_n(t)}}}"), _lt(rf"v = {_n(v)}\ \mathrm{{m/s}}")]
    wrong = [(t / d, "You divided time by distance. v = d ÷ t."), (d * t, "You multiplied. v = d ÷ t."), (d + t, "You added. v = d ÷ t.")]
    return _numeric(q, v, wrong, "m/s", working, "Wave Speed")


def gen_distance_from_speed_time(level="S3"):
    obj, v, t, d = _draw_dt()
    q = f"{obj} travels at {_n(v)} m/s. Calculate the distance it travels in {_n(t)} seconds."
    working = [_lt(r"v = \frac{d}{t}"), _lt(rf"{_n(v)} = \frac{{d}}{{{_n(t)}}}"), _lt(rf"d = {_n(v)} \times {_n(t)} = {_n(d)}\ \mathrm{{m}}")]
    wrong = [(v / t, "You divided. Rearrange v = d ÷ t to d = v × t."), (t / v, "You divided time by speed. d = v × t."), (v + t, "You added. d = v × t.")]
    return _numeric(q, d, wrong, "m", working, "Wave Speed")


def gen_time_from_distance_speed(level="S3"):
    obj, v, t, d = _draw_dt()
    q = f"{obj} travels at {_n(v)} m/s. Calculate the time it takes to travel {_n(d)} m."
    working = [_lt(r"v = \frac{d}{t}"), _lt(rf"{_n(v)} = \frac{{{_n(d)}}}{{t}}"), _lt(rf"t = \frac{{{_n(d)}}}{{{_n(v)}}} = {_n(t)}\ \mathrm{{s}}")]
    wrong = [(v / d, "You divided speed by distance. t = d ÷ v."), (d * v, "You multiplied. t = d ÷ v."), (d - v, "You subtracted. t = d ÷ v.")]
    return _numeric(q, t, wrong, "s", working, "Wave Speed")


# (object, frequencies, wavelengths, speed note) — f × λ is a sensible speed for the object
_FL = [
    ("A wave on a rope", [2, 4, 5, 10, 20], [0.5, 1, 2], ""),
    ("A water wave at the Butt of Lewis", [0.25, 0.5, 1, 2], [2, 4, 8], ""),
    ("A water wave in a ripple tank", [5, 10, 20], [0.1, 0.2, 0.5], ""),
    ("A sound wave in air", [170, 340, 680, 850, 1700], None, " Speed of sound in air = 340 m/s."),
    ("A radio wave", [60_000_000, 100_000_000, 150_000_000, 300_000_000], None, " Speed of radio waves = 300 000 000 m/s."),
]


def _draw_fl():
    obj, fs, lams, note = random.choice(_FL)
    f = random.choice(fs)
    if "sound" in obj:
        v = 340
    elif "radio" in obj:
        v = 300_000_000
    else:
        lam = random.choice(lams)
        return obj, f, lam, f * lam, note
    return obj, f, v / f, v, note


def gen_speed_from_f_lambda(level="S3"):
    obj, f, lam, v, note = _draw_fl()
    q = f"{obj} has a frequency of {_n(f)} Hz and a wavelength of {_n(lam)} m.\n\nCalculate the speed of the wave."
    working = [_lt(r"v = f\lambda"), _lt(rf"v = {_nl(f)} \times {_nl(lam)}"), _lt(rf"v = {_nl(v)}\ \mathrm{{m/s}}")]
    wrong = [(f / lam, "You divided. v = f × λ."), (lam / f, "You divided λ by f. v = f × λ."), (f + lam, "You added. v = f × λ.")]
    return _numeric(q, v, wrong, "m/s", working, "Wave Speed")


def gen_wavelength_from_v_f(level="S3"):
    obj, f, lam, v, note = _draw_fl()
    q = f"{obj} has a speed of {_n(v)} m/s and a frequency of {_n(f)} Hz.\n\nCalculate the wavelength of the wave."
    working = [_lt(r"v = f\lambda"), _lt(rf"{_nl(v)} = {_nl(f)} \times \lambda"), _lt(rf"\lambda = \frac{{{_nl(v)}}}{{{_nl(f)}}} = {_nl(lam)}\ \mathrm{{m}}")]
    wrong = [(v * f, "You multiplied. Rearrange v = fλ to λ = v ÷ f."), (f / v, "You divided f by v. λ = v ÷ f."), (v - f, "You subtracted. λ = v ÷ f.")]
    return _numeric(q, lam, wrong, "m", working, "Wave Speed")


def gen_frequency_from_v_lambda(level="S3"):
    obj, f, lam, v, note = _draw_fl()
    q = f"{obj} has a speed of {_n(v)} m/s and a wavelength of {_n(lam)} m.\n\nCalculate the frequency of the wave."
    working = [_lt(r"v = f\lambda"), _lt(rf"{_nl(v)} = f \times {_nl(lam)}"), _lt(rf"f = \frac{{{_nl(v)}}}{{{_nl(lam)}}} = {_nl(f)}\ \mathrm{{Hz}}")]
    wrong = [(v * lam, "You multiplied. Rearrange v = fλ to f = v ÷ λ."), (lam / v, "You divided λ by v. f = v ÷ λ."), (v - lam, "You subtracted. f = v ÷ λ.")]
    return _numeric(q, f, wrong, "Hz", working, "Wave Speed")


# ═════════════════════════════════════════════════════════════════════════════
# Waves Combined   (two equations in one question)
# ═════════════════════════════════════════════════════════════════════════════
_COMB = [
    ("water waves", [0.5, 1, 2], [2, 4, 6], [20, 30, 60]),
    ("waves on a rope", [2, 4, 5], [0.5, 1, 1.5, 2], [10, 20, 30]),
    ("waves in a ripple tank", [5, 10], [0.1, 0.2, 0.5], [10, 20, 30]),
]


def _draw_comb():
    obj, fs, lams, ts = random.choice(_COMB)
    f, lam, t = random.choice(fs), random.choice(lams), random.choice(ts)
    return obj, f, lam, t, int(round(f * t)), f * lam


def gen_speed_from_count_wavelength(level="S3"):
    obj, f, lam, t, N, v = _draw_comb()
    q = f"{N} {obj} pass a point in {_n(t)} seconds. The wavelength of the waves is {_n(lam)} m.\n\nCalculate the speed of the waves."
    working = [_lt(r"f = \frac{N}{t}"), _lt(rf"f = \frac{{{N}}}{{{_n(t)}}} = {_n(f)}\ \mathrm{{Hz}}"), _lt(r"v = f\lambda"),
               _lt(rf"v = {_n(f)} \times {_n(lam)} = {_n(v)}\ \mathrm{{m/s}}")]
    wrong = [(f, "You stopped at the frequency. Now use v = fλ."), (N * lam, "You used N × λ. Find f = N ÷ t first, then v = fλ."),
             (lam / f, "You divided λ by f. v = f × λ.")]
    sc = [{"question": "What is the frequency f?", "answer": f, "unit": "Hz"}, {"question": "What is the wave speed v?", "answer": v, "unit": "m/s"}]
    return _numeric(q, v, wrong, "m/s", working, "Waves Combined", scaffold=sc)


def gen_speed_from_period_wavelength(level="S3"):
    f, lam, obj = random.choice([(2, 3, "A wave"), (4, 0.5, "A water wave"), (5, 0.4, "A wave on a rope"), (10, 0.2, "A wave in a ripple tank"),
                                 (500, 0.68, "A sound wave"), (100, 3.4, "A sound wave"), (0.5, 4, "A sea wave")])
    T = 1 / f
    v = f * lam
    q = f"{obj} has a period of {_n(T)} s and a wavelength of {_n(lam)} m.\n\nCalculate the speed of the wave."
    working = [_lt(r"T = \frac{1}{f}"), _lt(rf"{_n(T)} = \frac{{1}}{{f}} \Rightarrow f = {_n(f)}\ \mathrm{{Hz}}"), _lt(r"v = f\lambda"),
               _lt(rf"v = {_n(f)} \times {_n(lam)} = {_n(v)}\ \mathrm{{m/s}}")]
    wrong = [(T * lam, "You multiplied the period by λ. Find f = 1 ÷ T first, then v = fλ."), (f, "You stopped at the frequency. Now use v = fλ."),
             (lam + f, "You added. v = f × λ.")]
    sc = [{"question": "What is the frequency f?", "answer": f, "unit": "Hz"}, {"question": "What is the wave speed v?", "answer": v, "unit": "m/s"}]
    return _numeric(q, v, wrong, "m/s", working, "Waves Combined", scaffold=sc)


def gen_wavelength_from_count_speed(level="S3"):
    obj, f, lam, t, N, v = _draw_comb()
    q = f"{obj[0].upper() + obj[1:]} travel at {_n(v)} m/s. {N} waves pass a point in {_n(t)} seconds.\n\nCalculate the wavelength of the waves."
    working = [_lt(r"f = \frac{N}{t}"), _lt(rf"f = \frac{{{N}}}{{{_n(t)}}} = {_n(f)}\ \mathrm{{Hz}}"), _lt(r"v = f\lambda"),
               _lt(rf"{_n(v)} = {_n(f)} \times \lambda \Rightarrow \lambda = {_n(lam)}\ \mathrm{{m}}")]
    wrong = [(f, "You stopped at the frequency. Now use v = fλ to find λ."), (v * f, "You multiplied v × f. Rearrange v = fλ to λ = v ÷ f."),
             (f / v, "You divided f by v. λ = v ÷ f.")]
    sc = [{"question": "What is the frequency f?", "answer": f, "unit": "Hz"}, {"question": "What is the wavelength λ?", "answer": lam, "unit": "m"}]
    return _numeric(q, lam, wrong, "m", working, "Waves Combined", scaffold=sc)


def gen_wavelength_from_distance_time_frequency(level="S3"):
    obj, f, lam, t, N, v = _draw_comb()
    t2 = random.choice([2, 4, 5, 10])
    d = v * t2
    q = f"A wave on a rope travels {_n(d)} m in {_n(t2)} seconds. Its frequency is {_n(f)} Hz.\n\nCalculate the wavelength of the wave."
    working = [_lt(r"v = \frac{d}{t}"), _lt(rf"v = \frac{{{_n(d)}}}{{{_n(t2)}}} = {_n(v)}\ \mathrm{{m/s}}"), _lt(r"v = f\lambda"),
               _lt(rf"{_n(v)} = {_n(f)} \times \lambda \Rightarrow \lambda = {_n(lam)}\ \mathrm{{m}}")]
    wrong = [(v, "You stopped at the speed. Now use v = fλ to find λ."), (v * f, "You multiplied v × f. λ = v ÷ f."), (f / v, "You divided f by v. λ = v ÷ f.")]
    sc = [{"question": "What is the wave speed v?", "answer": v, "unit": "m/s"}, {"question": "What is the wavelength λ?", "answer": lam, "unit": "m"}]
    return _numeric(q, lam, wrong, "m", working, "Waves Combined", scaffold=sc)


def gen_new_wavelength_when_frequency_changes(level="S3"):
    f, lam = random.choice([(2, 4), (4, 2), (5, 1), (10, 0.5), (20, 0.2), (50, 0.4)])
    k = random.choice([2, 4])
    v = f * lam
    new_f = f * k
    new_lam = v / new_f
    q = (f"Waves in a ripple tank have a frequency of {_n(f)} Hz and a wavelength of {_n(lam)} m. "
         f"The frequency of the dipper is then increased to {_n(new_f)} Hz. The speed of the waves stays the same.\n\n"
         f"Calculate the new wavelength.")
    working = [_lt(r"v = f\lambda"), _lt(rf"v = {_n(f)} \times {_n(lam)} = {_n(v)}\ \mathrm{{m/s}}"),
               _lt(rf"{_n(v)} = {_n(new_f)} \times \lambda"), _lt(rf"\lambda = \frac{{{_n(v)}}}{{{_n(new_f)}}} = {_n(new_lam)}\ \mathrm{{m}}")]
    wrong = [(lam * k, "The wavelength gets SMALLER when the frequency goes up (the speed stays the same)."), (lam, "The wavelength changes: v = fλ with v constant means λ falls when f rises."),
             (v, "You stopped at the speed. Use v = fλ with the new frequency to find λ.")]
    sc = [{"question": "What is the speed v of the waves?", "answer": v, "unit": "m/s"}, {"question": "What is the new wavelength?", "answer": new_lam, "unit": "m"}]
    return _numeric(q, new_lam, wrong, "m", working, "Waves Combined", scaffold=sc)


# ── pick-one generators for the registry ─────────────────────────────────────
def generate_period_frequency_s3(level="S3"):
    return random.choice([gen_find_frequency, gen_find_number_of_waves, gen_find_time, gen_find_period,
                          gen_find_frequency_from_period, gen_period_from_count, gen_waves_in_time_from_period])(level)


def generate_wave_speed_s3(level="S3"):
    return random.choice([gen_speed_from_distance_time, gen_distance_from_speed_time, gen_time_from_distance_speed,
                          gen_speed_from_f_lambda, gen_wavelength_from_v_f, gen_frequency_from_v_lambda])(level)


def generate_waves_combined_s3(level="S3"):
    return random.choice([gen_speed_from_count_wavelength, gen_speed_from_period_wavelength, gen_wavelength_from_count_speed,
                          gen_wavelength_from_distance_time_frequency, gen_new_wavelength_when_frequency_changes])(level)
