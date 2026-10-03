"""N5 Waves — exam-style question types from the past-paper/course-report worksheets.

Mirrors the three N5phys Waves worksheets (Wave Parameters and Behaviours; Electromagnetic Spectrum;
Refraction of Light). The older generators (wave_speed, period_frequency, combined) drill the basic
one-step calculations; these add the question styles SQA actually sets, with distractors that are
the errors named in the N5 course reports 2015–2025 and marking instructions: echoes not halved, the
crest-to-trough height taken as the amplitude, compressions counted instead of the gaps between them,
time left in minutes in f = N/t, the speed of sound used for electromagnetic waves, prefixes (GHz, nm)
not converted, the maximum wavelength found from the maximum frequency, neighbouring bands swapped,
a device named instead of a detector, angles measured from the surface, and the frequency said to
change on refraction.
"""
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

TOPIC = "Waves"
WPB = "Wave Parameters and Behaviours"
EMS = "Electromagnetic Spectrum"
REF = "Refraction of Light"
C = 3.0e8
VS = 340
_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

_NOTES = r"""
## N5 Waves — exam technique

**Relationships (as on the relationships sheet):**
$$d = vt \quad v = f\lambda \quad T = \frac{1}{f} \quad f = \frac{N}{t}$$

Speed of sound in air = 340 m/s; speed of light = 3.0 × 10⁸ m/s.

**Common errors (SQA course reports and marking instructions):**
- **Transverse**: particles vibrate at 90° to the direction of energy transfer (water waves, all EM waves). **Longitudinal**: particles vibrate parallel to it (sound).
- **Amplitude** is half the crest-to-trough height. On a longitudinal diagram, count the **gaps** between compressions.
- In f = N/t the time must be in **seconds** — show the conversion in a "show that".
- **Echoes**: the wave goes there **and back** — halve the distance.
- Longer wavelength → **more diffraction**. Diffracted waves keep the **same wavelength**.
- EM spectrum (increasing wavelength): **gamma, X-rays, ultraviolet, visible, infrared, microwaves, radio**. All transverse, all 3.0 × 10⁸ m/s.
- Convert **GHz, MHz, nm**. Maximum wavelength ↔ **minimum** frequency. Name the **detector**, not the device.
- Refraction: speed and wavelength change, **frequency never changes**. Angles are measured from the **normal**. Direction only changes if the angle of incidence is **greater than 0°**.
"""


def _sig(x, sf=3):
    return float(f"{x:.{sf}g}")


def _txt(x, sf=3):
    x = _sig(x, sf)
    if x == 0 or 0.01 <= abs(x) < 1e5:
        return f"{x:g}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    return f"{coeff} × 10{str(int(exp)).translate(_SUP)}"


def _ltx(x, sf=3):
    x = _sig(x, sf)
    if x == 0 or 0.01 <= abs(x) < 1e5:
        return f"{x:g}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    return rf"{coeff} \times 10^{{{int(exp)}}}"


def _L(s):
    return {"type": "latex", "content": s}


def _q(text, answer, unit, options, qtype, scaffold=None, level="N5"):
    kept = []
    for o in options:
        o["value"] = _sig(o["value"])
        o.setdefault("display", f"{_txt(o['value'])} {unit}".strip())
        if all(abs(o["value"] - k["value"]) > 0.02 * max(abs(o["value"]), abs(k["value"])) for k in kept):
            kept.append(o)
    return make_question(text, _sig(answer), kept, unit, scaffold=scaffold, notes=_NOTES,
                         topic=TOPIC, question_type=qtype, level=level)


def _choice(text, correct, wrong, qtype, level="N5"):
    distractors = [{"value": w, "mistake": why, "working": []} for w, why in wrong]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(question_text=text, correct_answer=correct, unit="", distractors=distractors,
                           working=[], notes=_NOTES, topic=TOPIC, question_type=qtype, level=level,
                           metadata={"type": "classification", "options": options})


def _opts(work, right, *wrong):
    return [{"value": right, "mistake": None, "working": work}] + [{"value": v, "mistake": m, "working": work} for v, m in wrong]


# ════════════════ Wave parameters and behaviours ════════════════
# (context, speed m/s, time range s) — echoes tied to the medium
_ECHOES = [("A student claps in front of a cliff", VS, [0.30, 0.40, 0.50, 0.60, 0.80], "cliff"),
           ("A fishing boat's sonar pulse reflects from a shoal of fish", 1500, [0.080, 0.10, 0.12, 0.16], "shoal"),
           ("A CalMac ferry's echo sounder pulse reflects from the sea bed", 1500, [0.040, 0.060, 0.080, 0.10], "sea bed"),
           ("A car's parking sensor sends ultrasound to a wall", VS, [0.0030, 0.0035, 0.0050, 0.0080], "wall")]


def gen_wv_echo(level="N5"):
    ctx, v, ts, target = random.choice(_ECHOES)
    t = random.choice(ts)
    d = v * t / 2
    text = f"{ctx}. The echo returns {_txt(t)} s later. The speed of the wave is {v} m/s. Calculate the distance to the {target}."
    work = [_L(r"d = vt"), _L(rf"d = {v} \times {_ltx(t)} = {_ltx(v * t)}\ \mathrm{{m}}\ \text{{(there and back)}}"),
            _L(rf"\text{{distance}} = {_ltx(d)}\ \mathrm{{m}}")]
    scaffold = [{"question": "What is the total distance travelled by the pulse (there and back), in m?", "answer": _sig(v * t)},
                {"question": f"What is the distance to the {target}, in m?", "answer": _sig(d)}]
    wrong = [(v * t, "The wave travels there AND back — halve the distance (course reports 2015–2025).")]
    if v == 1500:
        wrong.append((VS * t / 2, "Use the speed of sound in WATER (1500 m/s), as given."))
    else:
        wrong.append((C * t / 2, "This is sound — use 340 m/s, not the speed of light."))
    return _q(text, d, "m", _opts(work, d, *wrong), WPB, scaffold, level)


def gen_wv_parameters(level="N5"):
    kind = random.choice(["amplitude", "longitudinal", "fNt", "lambda_from_N"])
    if kind == "amplitude":
        h = random.choice([0.40, 0.60, 0.80, 1.2, 3.0])
        text = f"The vertical distance from the top of a crest to the bottom of a trough of a wave is {h:g} m. State the amplitude of the wave."
        work = [_L(rf"\text{{amplitude}} = \frac{{{h:g}}}{{2}} = {_ltx(h / 2)}\ \mathrm{{m}}")]
        return _q(text, h / 2, "m", _opts(work, h / 2, (h, "Amplitude is from the rest position to a crest — HALF the crest-to-trough height (course report 2024)."),
                                          (h / 4, "Halve the crest-to-trough height once.")), WPB, None, level)
    if kind == "longitudinal":
        n = random.choice([3, 4, 5, 6])
        L = random.choice([1.2, 1.5, 2.1, 2.4, 3.0])
        lam = L / (n - 1)
        text = f"In a diagram of a sound wave, the distance from the first compression to the last of {n} compressions is {L:g} m. Determine the wavelength."
        work = [_L(rf"{n}\ \text{{compressions}} \Rightarrow {n - 1}\ \text{{wavelengths}}"), _L(rf"\lambda = \frac{{{L:g}}}{{{n - 1}}} = {_ltx(lam)}\ \mathrm{{m}}")]
        return _q(text, lam, "m", _opts(work, lam, (L / n, f"{n} compressions enclose {n - 1} wavelengths — count the gaps (course report 2018).")), WPB, None, level)
    if kind == "fNt":
        N = random.choice([18, 24, 36, 45, 60, 120])
        mins = random.choice([1.5, 2.0, 3.0, 4.0])
        f = N / (mins * 60)
        text = f"{N} waves pass a buoy in {mins:g} minutes. Calculate the frequency of the waves."
        work = [_L(r"f = \frac{N}{t}"), _L(rf"f = \frac{{{N}}}{{{mins:g} \times 60}} = {_ltx(f)}\ \mathrm{{Hz}}")]
        return _q(text, f, "Hz", _opts(work, f, (N / mins, "Convert minutes to seconds."), (mins * 60 / N, "That's the period: f = N ÷ t.")), WPB, None, level)
    N = random.choice([20, 25, 30, 40])
    t = random.choice([8, 10, 12, 16, 20])
    v = random.choice([0.10, 0.20, 1.5, 2.0, 3.0])
    f = N / t
    lam = v / f
    text = f"{N} water waves are produced in {t} s. The waves travel at {v:g} m/s. Calculate their wavelength."
    work = [_L(rf"f = \frac{{N}}{{t}} = \frac{{{N}}}{{{t}}} = {_ltx(f)}\ \mathrm{{Hz}}"), _L(r"v = f\lambda"), _L(rf"\lambda = \frac{{{v:g}}}{{{_ltx(f)}}} = {_ltx(lam)}\ \mathrm{{m}}")]
    scaffold = [{"question": "What is the frequency, in Hz?", "answer": _sig(f)}, {"question": "What is the wavelength, in m?", "answer": _sig(lam)}]
    return _q(text, lam, "m", _opts(work, lam, (v * f, "λ = v ÷ f."), (v / N, "Find the frequency first: f = N ÷ t.")), WPB, scaffold, level)


def gen_wv_behaviour(level="N5"):
    kind = random.choice(["transverse", "longitudinal", "diffract", "diffract_wl", "amplitude", "accuracy", "firework"])
    if kind == "transverse":
        return _choice("What is meant by a transverse wave?", "The particles vibrate at 90° to the direction in which the energy travels.",
                       [("A wave that moves up and down.", "Describe the particle vibration compared with the direction of energy transfer (course reports 2024, 2025)."),
                        ("The particles vibrate parallel to the direction of energy travel.", "That's a longitudinal wave."),
                        ("A wave that needs a medium to travel through.", "Light is transverse and travels through a vacuum.")], WPB, level)
    if kind == "longitudinal":
        return _choice("Which is an example of a longitudinal wave?", "Sound",
                       [("Light", "All electromagnetic waves are transverse."), ("A water wave", "Water waves are transverse."),
                        ("Microwaves", "Electromagnetic — transverse.")], WPB, level)
    if kind == "diffract":
        return _choice("What is diffraction?", "The spreading out of waves as they pass through a gap or around an obstacle.",
                       [("The change in speed of a wave as it enters a new material.", "That's refraction (course report 2018)."),
                        ("The bouncing of waves off a barrier.", "That's reflection."),
                        ("The change in wavelength as waves pass through a gap.", "The wavelength stays the same.")], WPB, level)
    if kind == "diffract_wl":
        return _choice("A house behind a hill gets good long-wave radio but poor TV reception. Why?",
                       "Radio waves have a longer wavelength, so they diffract more round the hill.",
                       [("TV waves have a longer wavelength, so they diffract more.", "TV (UHF) waves have a SHORTER wavelength."),
                        ("Radio waves travel faster than TV waves.", "All EM waves travel at the same speed."),
                        ("Radio waves have a higher frequency.", "Longer wavelength = LOWER frequency.")], WPB, level)
    if kind == "amplitude":
        return _choice("An echo of a firework bang has a smaller amplitude than the original bang. Why?",
                       "The echo carries less energy — smaller energy gives a smaller amplitude.",
                       [("The echo has a lower frequency.", "Reflection doesn't change the frequency."),
                        ("The echo travels more slowly.", "Sound travels at the same speed."),
                        ("The echo has a shorter wavelength.", "The wavelength is unchanged — it's the energy (course report 2024).")], WPB, level)
    if kind == "accuracy":
        return _choice("How could the accuracy of a frequency found by timing 10 waves with a stopwatch be improved?",
                       "Time more waves, and repeat the timing and calculate an average.",
                       [("Repeat the measurement.", "Must also say the results are AVERAGED (course reports 2017, 2024)."),
                        ("Use a ruler to measure the waves.", "That measures wavelength, not frequency."),
                        ("Time fewer waves.", "Fewer waves → larger reaction-time uncertainty.")], WPB, level)
    return _choice("A firework is seen to explode and the bang is heard 1.5 s later. What is needed to calculate how far away it was?",
                   "Only the speed of sound — the light arrives almost instantly.",
                   [("The speed of light and the speed of sound.", "The light's travel time is negligible (course report 2024)."),
                    ("Only the speed of light.", "It's the SOUND that takes 1.5 s."),
                    ("The frequency of the sound.", "d = vt needs the speed, not the frequency.")], WPB, level)


# ════════════════ Electromagnetic spectrum ════════════════
_BANDS = ["gamma rays", "X-rays", "ultraviolet", "visible light", "infrared", "microwaves", "radio waves"]
# (context, value, prefix multiplier, prefix text, band)
_SOURCES = [("Wireless headphones receive signals at", 2.42, 1e9, "GHz", "microwaves"),
            ("A mobile phone mast transmits at", 1.8, 1e9, "GHz", "microwaves"),
            ("A Stornoway radio station broadcasts at", 103.4, 1e6, "MHz", "radio waves"),
            ("Long-wave radio is broadcast at", 198, 1e3, "kHz", "radio waves"),
            ("A microwave oven operates at", 2.45, 1e9, "GHz", "microwaves")]
_WAVELENGTHS = [("An infrared laser rangefinder emits radiation of wavelength", 905, "infrared"),
                ("A red laser emits light of wavelength", 650, "visible light"),
                ("A UV lamp used to sterilise water emits radiation of wavelength", 254, "ultraviolet"),
                ("A TV remote control emits infrared of wavelength", 940, "infrared")]


def gen_em_calc(level="N5"):
    kind = random.choice(["lambda", "freq", "max", "signal"])
    if kind == "lambda":
        ctx, val, mult, pre, band = random.choice(_SOURCES)
        f = val * mult
        lam = C / f
        text = f"{ctx} {val:g} {pre}. Calculate the wavelength of the waves."
        work = [_L(r"v = f\lambda"), _L(rf"3.0\times10^8 = {val:g}\times10^{{{len(str(int(mult))) - 1}}} \times \lambda"), _L(rf"\lambda = {_ltx(lam)}\ \mathrm{{m}}")]
        return _q(text, lam, "m", _opts(work, lam, (C / val, f"Convert {pre} to Hz."), (VS / f, "Electromagnetic waves travel at 3.0 × 10⁸ m/s, not 340 m/s."),
                                        (f / C, "λ = v ÷ f.")), EMS, None, level)
    if kind == "freq":
        ctx, nm, band = random.choice(_WAVELENGTHS)
        f = C / (nm * 1e-9)
        text = f"{ctx} {nm} nm. Calculate its frequency."
        work = [_L(r"v = f\lambda"), _L(rf"3.0\times10^8 = f \times {nm}\times10^{{-9}}"), _L(rf"f = {_ltx(f)}\ \mathrm{{Hz}}")]
        return _q(text, f, "Hz", _opts(work, f, (C / nm, "Convert nm to m (× 10⁻⁹) — course report 2025."), (VS / (nm * 1e-9), "Use the speed of light.")), EMS, None, level)
    if kind == "max":
        lo, hi = random.choice([(2.0, 6.0), (0.5, 2.5), (1.0, 4.0)])
        lam = C / (lo * 1e9)
        text = f"A communications link uses microwaves with frequencies from {lo:g} GHz to {hi:g} GHz. Calculate the MAXIMUM wavelength used."
        work = [_L(r"\lambda_{max}\ \text{uses}\ f_{min}"), _L(rf"3.0\times10^8 = {lo:g}\times10^9 \times \lambda"), _L(rf"\lambda = {_ltx(lam)}\ \mathrm{{m}}")]
        return _q(text, lam, "m", _opts(work, lam, (C / (hi * 1e9), "The maximum wavelength comes from the MINIMUM frequency (course report 2022)."),
                                        (C / lo, "Convert GHz to Hz.")), EMS, None, level)
    ctx, d, reflect = random.choice([("A GPS satellite is directly overhead at an altitude of 20 200 km.", 20200e3, False),
                                     ("A TV satellite is 36 000 km above the equator.", 36000e3, False),
                                     ("An infrared rangefinder pulse reflects from a flag 180 m away.", 180.0, True),
                                     ("A radar pulse reflects from an aircraft 30 km away.", 30e3, True)])
    path = 2 * d if reflect else d
    t = path / C
    q = "Calculate the time between the pulse being sent and received." if reflect else "Calculate the time for a signal to travel between the satellite and the ground."
    work = [_L(r"d = vt"), _L(rf"{_ltx(path)} = 3.0\times10^8 \times t"), _L(rf"t = {_ltx(t)}\ \mathrm{{s}}")]
    wrong = [(d / C, "The pulse travels there AND back.")] if reflect else [(d / 1e3 / C, "Convert km to m.")]
    return _q(f"{ctx} {q}", t, "s", _opts(work, t, *wrong, (path / VS, "Use the speed of light.")), EMS, None, level)


def gen_em_bands(level="N5"):
    kind = random.choice(["order", "highest", "detector", "use", "property", "ir_vs_visible"])
    if kind == "order":
        i = random.randint(1, 5)
        return _choice(f"Which band lies between {_BANDS[i - 1]} and {_BANDS[i + 1]} in the electromagnetic spectrum?", _BANDS[i],
                       [(b, "Learn the order: gamma, X-rays, ultraviolet, visible, infrared, microwaves, radio (course report 2023: bands often swapped).")
                        for b in random.sample([b for j, b in enumerate(_BANDS) if j != i], 3)], EMS, level)
    if kind == "highest":
        return _choice("Which band of the electromagnetic spectrum has the longest wavelength and the lowest frequency?", "radio waves",
                       [("gamma rays", "Gamma rays have the SHORTEST wavelength."), ("microwaves", "Radio waves are longer still."),
                        ("infrared", "Infrared is shorter than microwaves and radio.")], EMS, level)
    if kind == "detector":
        band, right, wrongs = random.choice([
            ("infrared", "photodiode", [("infrared camera", "A camera CONTAINS a detector — name the detector (course report 2016)."),
                                        ("Geiger-Müller tube", "That detects gamma rays."), ("aerial", "Aerials detect radio waves and microwaves.")]),
            ("ultraviolet", "fluorescent paint", [("aerial", "Aerials detect radio waves."), ("thermometer", "Thermometers detect infrared."),
                                                  ("a sunbed", "That's a SOURCE of ultraviolet.")]),
            ("gamma rays", "Geiger-Müller tube", [("aerial", "Aerials detect radio waves."), ("the eye", "The eye detects visible light."),
                                                  ("thermistor", "A thermistor detects infrared (heat).")]),
            ("visible light (in a telescope)", "CCD (charge-coupled device)", [("camera", "A camera contains a detector — name it (course report 2017)."),
                                                                               ("aerial", "Aerials detect radio waves."), ("Geiger-Müller tube", "That detects gamma rays.")])])
        return _choice(f"Which is a detector of {band}?", right, wrongs, EMS, level)
    if kind == "use":
        band, right, wrongs = random.choice([
            ("ultraviolet", "detecting forged banknotes", [("cooking food", "Microwaves."), ("imaging bones", "X-rays."), ("broadcasting TV", "Radio waves.")]),
            ("gamma rays", "sterilising surgical instruments", [("TV remote controls", "Infrared."), ("satellite communication", "Microwaves."), ("tanning", "Ultraviolet.")]),
            ("microwaves", "satellite communication and GPS", [("treating cancer", "Gamma rays."), ("thermal imaging", "Infrared."), ("imaging bones", "X-rays.")]),
            ("infrared", "thermal imaging cameras", [("sterilising water", "Ultraviolet."), ("airport scanners", "X-rays."), ("radio broadcasting", "Radio waves.")])])
        return _choice(f"Which is a use of {band}?", right, wrongs, EMS, level)
    if kind == "property":
        return _choice("Which statement is true for ALL electromagnetic waves?", "They are transverse and travel at 3.0 × 10⁸ m/s in a vacuum.",
                       [("They are longitudinal.", "All EM waves are transverse."), ("They need a medium to travel through.", "They travel through a vacuum."),
                        ("Higher-frequency waves travel faster.", "All travel at the same speed.")], EMS, level)
    return _choice("How does infrared compare with visible light?", "Longer wavelength, same speed, and it diffracts more.",
                   [("Longer wavelength, same speed, and it diffracts less.", "Longer wavelength diffracts MORE (course report 2024)."),
                    ("Shorter wavelength, same speed.", "Infrared has a LONGER wavelength."),
                    ("Longer wavelength and slower.", "All EM waves travel at the same speed.")], EMS, level)


# ════════════════ Refraction of light ════════════════

def gen_rf_explain(level="N5"):
    kind = random.choice(["into_glass", "out_of_glass", "normal_angle", "zero", "frequency", "surface_angle", "semicircle"])
    if kind == "into_glass":
        return _choice("Light passes from air into glass. What happens to its speed, wavelength and frequency?",
                       "speed decreases, wavelength decreases, frequency stays the same",
                       [("speed decreases, wavelength stays the same, frequency decreases", "The frequency NEVER changes on refraction (course reports 2018, 2024)."),
                        ("speed increases, wavelength increases, frequency stays the same", "Light slows down entering glass."),
                        ("speed decreases, wavelength increases, frequency stays the same", "Slower at the same frequency → SHORTER wavelength (course report 2022).")], REF, level)
    if kind == "out_of_glass":
        return _choice("A ray passes from glass into air at an angle of incidence of 25°. How does it bend?",
                       "Away from the normal, because it speeds up.",
                       [("Towards the normal, because it speeds up.", "Speeding up → bends AWAY from the normal."),
                        ("Away from the normal, because it slows down.", "It speeds up entering air."),
                        ("It does not bend.", "It only goes straight through if the angle of incidence is 0°.")], REF, level)
    if kind == "normal_angle":
        return _choice("Where are the angle of incidence and the angle of refraction measured from?", "The normal — a line at 90° to the surface.",
                       [("The surface of the block.", "Angles are measured from the NORMAL (course report 2018)."),
                        ("The incident ray.", "Measure from the normal."), ("The bottom of the block.", "Measure from the normal.")], REF, level)
    if kind == "zero":
        return _choice("Light enters a glass block along the normal (angle of incidence 0°). What happens?",
                       "It slows down but does not change direction.",
                       [("Nothing — there is no refraction.", "It still slows down; only the direction is unchanged (course report 2025)."),
                        ("It bends towards the normal.", "Direction only changes if the angle of incidence is greater than 0°."),
                        ("It is reflected back.", "It passes into the glass.")], REF, level)
    if kind == "frequency":
        return _choice("Red light in air has a frequency of 4.6 × 10¹⁴ Hz. What is its frequency in glass?", "4.6 × 10¹⁴ Hz",
                       [("less than 4.6 × 10¹⁴ Hz", "The frequency is unchanged (course report 2024)."),
                        ("more than 4.6 × 10¹⁴ Hz", "The frequency is unchanged."),
                        ("zero — light stops in glass", "Light travels through glass, just more slowly.")], REF, level)
    if kind == "surface_angle":
        a = random.choice([20, 25, 30, 35, 40])
        return _choice(f"A ray meets a glass block at {a}° to the SURFACE. What is the angle of incidence?", f"{90 - a}°",
                       [(f"{a}°", "Angles are measured from the normal: 90° − angle to the surface."),
                        (f"{180 - a}°", "Measure from the normal (90°)."), (f"{90 + a}°", "Subtract from 90°, don't add.")], REF, level)
    return _choice("A ray enters the curved face of a semicircular block heading for the centre of the flat face. What happens at the curved face?",
                   "It does not change direction, because it travels along the normal (a radius).",
                   [("It bends towards the normal.", "Along a radius the angle of incidence is 0° — no change in direction (course report 2022)."),
                    ("It bends away from the normal.", "No change of direction along the normal."),
                    ("It is totally internally reflected.", "Not at the curved face.")], REF, level)


def gen_rf_calc(level="N5"):
    colour, lam_nm = random.choice([("Red", 650), ("Green", 540), ("Blue", 470), ("Yellow", 590)])
    v_glass, medium = random.choice([(2.0e8, "glass"), (2.25e8, "water"), (1.9e8, "Perspex")])
    f = C / (lam_nm * 1e-9)
    lam2 = v_glass / _sig(f)
    text = (f"{colour} light has a wavelength of {lam_nm} nm in air. It enters {medium}, where its speed is {_txt(v_glass)} m/s. "
            f"Calculate its wavelength in the {medium}.")
    work = [_L(rf"f = \frac{{3.0\times10^8}}{{{lam_nm}\times10^{{-9}}}} = {_ltx(f)}\ \mathrm{{Hz}}\ \text{{(unchanged)}}"), _L(r"v = f\lambda"),
            _L(rf"\lambda = \frac{{{_ltx(v_glass)}}}{{{_ltx(f)}}} = {_ltx(lam2)}\ \mathrm{{m}}")]
    scaffold = [{"question": "What is the frequency of the light, in Hz?", "answer": _sig(f)},
                {"question": f"What is the wavelength in the {medium}, in m?", "answer": _sig(lam2)}]
    return _q(text, lam2, "m", _opts(work, lam2, (lam_nm * 1e-9, "The wavelength changes — the speed is less in the medium."),
                                     (lam_nm * 1e-9 * C / v_glass, "Slower → SHORTER wavelength.")), REF, scaffold, level)
