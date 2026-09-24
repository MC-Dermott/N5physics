"""Higher ODU — The Expanding Universe.

Mirrors Hphys_Expanding_Universe_Worksheet.docx, one generator per worksheet type:
  1  Doppler effect calculations (frequency heard, or speed of the source)
  2  Explaining the Doppler effect (wavefronts)
  3  Redshift and recessional velocity (z, v, or λ_observed)
  4  Hubble's law and the age of the Universe
  5  Evidence for the Big Bang, dark matter and dark energy
  6  Stellar temperature and radiation curves

Distractors are the errors named in SQA marking instructions and course reports: wrong sign in the
Doppler relationship, λ_observed as the redshift denominator, z used as v in Hubble's law, age of
the Universe left in seconds, km s⁻¹ not converted, dark matter/dark energy confused, colour
explained by redshift rather than temperature.
"""
import math
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

TOPIC = "Our Dynamic Universe"
QTYPE = "The Expanding Universe"
V_SOUND = 340.0
C = 3.00e8
H0 = 2.3e-18
YEAR = 365 * 24 * 3600
WIEN = 2.9e-3

_NOTES = r"""
## The Expanding Universe

**Relationships (as on the relationships sheet):**
$$f_o = f_s\left(\frac{v}{v \pm v_s}\right) \qquad z = \frac{\lambda_{observed} - \lambda_{rest}}{\lambda_{rest}} \qquad z = \frac{v}{c} \qquad v = H_0 d$$

Data sheet: speed of sound $v = 3.40 \times 10^{2}\ \mathrm{m\,s^{-1}}$, $c = 3.00 \times 10^{8}\ \mathrm{m\,s^{-1}}$,
$H_0 = 2.3 \times 10^{-18}\ \mathrm{s^{-1}}$.

**Common errors (from SQA marking instructions and course reports):**
- **Doppler sign:** source approaching → $v - v_s$ (higher frequency); moving away → $v + v_s$ (lower).
  The source's own frequency never changes — only the frequency *heard*.
- Explanations must be in terms of **wavefronts** (closer together / further apart → more / fewer per second).
- **Redshift:** always divide by $\lambda_{rest}$. Recessional velocity needs the second step $z = v/c$.
- **Hubble's law** needs $v$ in m s⁻¹ — find it from $z$ first, and convert "0.30c" or km s⁻¹.
- **Age of the Universe** $= 1/H_0$ is in **seconds** — divide by $3.15 \times 10^{7}$ for years.
- **Dark matter** ↔ extra mass of galaxies (orbital speeds of stars). **Dark energy** ↔ accelerating expansion.
- Evidence for the Big Bang: redshift/Hubble's law, **cosmic microwave background radiation**, abundance of H and He,
  Olbers' paradox. Don't restate the evidence already given in the question.
- A **hotter** star: peak at a **shorter** wavelength and **more** energy per second per unit area at every
  wavelength. A star's colour is due to its **temperature**, not redshift.
"""

_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _sig(x, sf=3):
    return float(f"{x:.{sf}g}")


def _txt(x, sf=3):
    x = _sig(x, sf)
    if 0.01 <= abs(x) < 1e4:
        return f"{x:g}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    return f"{coeff} × 10{str(int(exp)).translate(_SUP)}"


def _ltx(x, sf=3):
    x = _sig(x, sf)
    if 0.01 <= abs(x) < 1e4:
        return f"{x:g}"
    coeff, exp = f"{x:.{sf - 1}e}".split("e")
    return rf"{coeff} \times 10^{{{int(exp)}}}"


def _L(s):
    return {"type": "latex", "content": s}


def _T(s):
    return {"type": "text", "content": s}


def _q(text, answer, unit, options, scaffold=None):
    # drop any distractor within 2 % of the answer (or of another option) — indistinguishable in practice
    kept = []
    for o in options:
        if all(abs(o["value"] - k["value"]) > 0.02 * max(abs(o["value"]), abs(k["value"])) for k in kept):
            kept.append(o)
    options = kept
    return make_question(text, answer, options, unit, scaffold=scaffold, notes=_NOTES,
                         topic=TOPIC, question_type=QTYPE, level="Higher")


def _choice(text, correct, wrong):
    """wrong: list of (option text, why it's wrong)."""
    distractors = [{"value": w, "mistake": why, "working": []} for w, why in wrong]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(question_text=text, correct_answer=correct, unit="", distractors=distractors,
                           working=[], notes=_NOTES, topic=TOPIC, question_type=QTYPE, level="Higher",
                           metadata={"type": "classification", "options": options})


# ── Type 1: Doppler calculations ────────────────────────────────────────────
# (source, noise, speed lo, speed hi, frequency lo, frequency hi)
_SOURCES = [
    ("An ambulance", "siren", 15, 30, 600, 1000),
    ("A police car", "siren", 15, 35, 500, 900),
    ("A motorbike", "horn", 20, 40, 300, 500),
    ("A train", "horn", 20, 45, 300, 600),
]
# Slow sources (a buzzer on a trolley, a ferry) shift the frequency by < 2 %, which makes the
# wrong-sign answer indistinguishable from the right one — they're kept for the explain type only.


def gen_eu_doppler(level="Higher"):
    src, noise, vlo, vhi, flo, fhi = random.choice(_SOURCES)
    vs = round(random.uniform(vlo, vhi), 1 if vhi < 10 else 0)
    fs = int(round(random.uniform(flo, fhi), -1))
    approaching = random.choice([True, False])
    sign = "-" if approaching else "+"
    towards = "towards" if approaching else "away from"
    fo = _sig(fs * V_SOUND / (V_SOUND - vs if approaching else V_SOUND + vs))
    wrong_sign = _sig(fs * V_SOUND / (V_SOUND + vs if approaching else V_SOUND - vs))
    inverted = _sig(fs * (V_SOUND - vs if approaching else V_SOUND + vs) / V_SOUND)
    if random.random() < 0.6:
        text = (f"{src} moves {towards} a stationary observer at {vs:g} m s⁻¹. Its {noise} emits sound of frequency "
                f"{fs} Hz. The speed of sound in air is 340 m s⁻¹. Calculate the frequency heard by the observer.")
        work = [_L(r"f_o = f_s\left(\frac{v}{v \pm v_s}\right)"),
                _T(f"The source is moving {towards} the observer, so use v {sign} vₛ."),
                _L(rf"f_o = {fs} \times \left(\frac{{340}}{{340 {sign} {vs:g}}}\right)"),
                _L(rf"f_o = {fo:g}\ \mathrm{{Hz}}")]
        opts = [{"value": fo, "mistake": None, "working": work},
                {"value": wrong_sign, "mistake": f"Wrong sign — a source moving {towards} the observer needs v {sign} vₛ.", "working": work},
                {"value": inverted, "mistake": "You've written the fraction upside down — it's v ÷ (v ± vₛ).", "working": work},
                {"value": float(fs), "mistake": "The frequency heard changes when the source moves — only the emitted frequency stays the same.", "working": work}]
        scaffold = [{"question": f"What is v {sign} vₛ, in m s⁻¹?", "answer": V_SOUND - vs if approaching else V_SOUND + vs},
                    {"question": "What is the frequency heard, in Hz?", "answer": fo}]
        return _q(text, fo, "Hz", opts, scaffold)
    # rearrange for the speed of the source
    fo_r = int(round(fs * V_SOUND / (V_SOUND - vs if approaching else V_SOUND + vs)))
    vs_ans = _sig(V_SOUND - fs * V_SOUND / fo_r if approaching else fs * V_SOUND / fo_r - V_SOUND)
    text = (f"{src}'s {noise} emits sound of frequency {fs} Hz. A stationary observer hears a frequency of {fo_r} Hz "
            f"as it moves {towards} them. The speed of sound in air is 340 m s⁻¹. Calculate the speed of the source.")
    denom = _sig(fs * V_SOUND / fo_r)
    work = [_L(r"f_o = f_s\left(\frac{v}{v \pm v_s}\right)"),
            _L(rf"{fo_r} = {fs} \times \left(\frac{{340}}{{340 {sign} v_s}}\right)"),
            _L(rf"340 {sign} v_s = \frac{{{fs} \times 340}}{{{fo_r}}} = {denom:g}"),
            _L(rf"v_s = {vs_ans:g}\ \mathrm{{m\,s^{{-1}}}}")]
    opts = [{"value": vs_ans, "mistake": None, "working": work},
            {"value": _sig(abs(V_SOUND - fo_r * V_SOUND / fs)), "mistake": "You swapped fₒ and fₛ when rearranging.", "working": work},
            {"value": _sig(denom), "mistake": f"That's 340 {sign} vₛ — you still need to {'subtract it from' if approaching else 'take 340 away from it to find'} vₛ.", "working": work}]
    scaffold = [{"question": f"What is 340 {sign} vₛ, in m s⁻¹?", "answer": denom},
                {"question": "What is the speed of the source vₛ, in m s⁻¹?", "answer": vs_ans}]
    return _q(text, vs_ans, "m s⁻¹", opts, scaffold)


# ── Type 2: explaining the Doppler effect ───────────────────────────────────
_EXPLAIN = [
    ("An ambulance approaches a pedestrian with its siren sounding. Why is the frequency heard by the pedestrian "
     "higher than the frequency emitted by the siren?",
     "The wavefronts in front of the moving ambulance are closer together, so more wavefronts reach the pedestrian "
     "each second.",
     [("The siren emits a higher frequency while the ambulance is moving towards the pedestrian.",
       "The emitted frequency never changes — it's the frequency heard that changes, because of the wavefronts."),
      ("The sound travels faster because the ambulance is moving.",
       "The speed of sound in air doesn't depend on the speed of the source."),
      ("The wavefronts in front of the ambulance are further apart, so fewer reach the pedestrian each second.",
       "That describes the sound behind a source moving away — ahead of it the wavefronts are bunched up.")]),
    ("A car sounds its horn as it moves away from a stationary observer. Why is the frequency heard lower than the "
     "frequency emitted?",
     "The wavefronts behind the moving car are further apart, so fewer wavefronts reach the observer each second.",
     [("The horn emits a lower frequency once the car has passed.",
       "The horn's frequency is constant — the observed frequency changes because of wavefront spacing."),
      ("The wavefronts behind the car are closer together, so fewer reach the observer each second.",
       "Closer wavefronts would mean more per second, not fewer — behind the car they are spread out."),
      ("The sound loses energy as the car moves away, which lowers its frequency.",
       "Getting quieter (less energy) doesn't change the frequency — the Doppler effect is about wavefront spacing.")]),
    ("A passenger sits on a bus travelling at constant speed while the driver sounds the horn. What frequency does "
     "the passenger hear?",
     "The same frequency as the horn emits — the passenger moves with the same velocity as the horn, so there is no "
     "relative motion between source and observer.",
     [("A higher frequency, because the bus is moving forwards.",
       "The Doppler effect needs relative motion between source and observer — the passenger moves with the horn."),
      ("A lower frequency, because the sound has to travel back through the bus.",
       "There's no relative motion between the horn and the passenger, so the frequency is unchanged.")]),
]


def gen_eu_doppler_explain(level="Higher"):
    q, correct, wrong = random.choice(_EXPLAIN)
    return _choice(q, correct, wrong)


# ── Type 3: redshift and recessional velocity ──────────────────────────────
_LINES = [("hydrogen", 656), ("hydrogen", 486), ("hydrogen", 434), ("hydrogen", 410), ("sodium", 589)]


def gen_eu_redshift(level="Higher"):
    element, lr = random.choice(_LINES)
    z = round(random.uniform(0.03, 0.12), 3)
    lo = round(lr * (1 + z))
    kind = random.choice(["z", "v", "lambda"])
    if kind == "z":
        zz = _sig((lo - lr) / lr)
        text = (f"A {element} spectral line has a wavelength of {lr} nm in the laboratory. In the light from a distant "
                f"galaxy the same line is observed at {lo} nm. Calculate the redshift of the galaxy.")
        work = [_L(r"z = \frac{\lambda_{observed} - \lambda_{rest}}{\lambda_{rest}}"),
                _L(rf"z = \frac{{{lo} - {lr}}}{{{lr}}}"), _L(rf"z = {zz:g}")]
        opts = [{"value": zz, "mistake": None, "working": work},
                {"value": _sig((lo - lr) / lo), "mistake": "You divided by λ_observed — the denominator is always λ_rest.", "working": work},
                {"value": _sig(lo / lr), "mistake": "That's λ_observed ÷ λ_rest — subtract λ_rest first.", "working": work}]
        return _q(text, zz, "", opts, None)
    if kind == "v":
        zz = (lo - lr) / lr
        v = _sig(zz * C)
        text = (f"A {element} spectral line has a wavelength of {lr} nm in the laboratory. In the light from a distant "
                f"galaxy the same line is observed at {lo} nm. Calculate the recessional velocity of the galaxy.")
        work = [_L(r"z = \frac{\lambda_{observed} - \lambda_{rest}}{\lambda_{rest}}"),
                _L(rf"z = \frac{{{lo} - {lr}}}{{{lr}}} = {_sig(zz):g}"), _L(r"z = \frac{v}{c}"),
                _L(rf"{_sig(zz):g} = \frac{{v}}{{3.00 \times 10^{{8}}}}"), _L(rf"v = {_ltx(v)}\ \mathrm{{m\,s^{{-1}}}}")]
        opts = [{"value": v, "mistake": None, "working": work},
                {"value": _sig((lo - lr) / lo * C), "mistake": "You divided by λ_observed when finding z — use λ_rest.", "working": work},
                {"value": _sig(zz), "mistake": "That's the redshift z — use z = v/c to find the velocity.", "working": work}]
        scaffold = [{"question": "What is the redshift z?", "answer": _sig(zz)},
                    {"question": "What is the recessional velocity, in m s⁻¹?", "answer": v}]
        return _q(text, v, "m s⁻¹", opts, scaffold)
    v = _sig(z * C, 2)
    zz = v / C
    lo2 = _sig(lr * (1 + zz))
    text = (f"A galaxy has a recessional velocity of {_txt(v, 2)} m s⁻¹. A {element} spectral line has a wavelength of "
            f"{lr} nm in the laboratory. Determine the wavelength of this line in the light from the galaxy as observed on Earth.")
    work = [_L(r"z = \frac{v}{c}"), _L(rf"z = \frac{{{_ltx(v, 2)}}}{{3.00 \times 10^{{8}}}} = {_sig(zz):g}"),
            _L(r"z = \frac{\lambda_{observed} - \lambda_{rest}}{\lambda_{rest}}"),
            _L(rf"{_sig(zz):g} = \frac{{\lambda_{{observed}} - {lr}}}{{{lr}}}"),
            _L(rf"\lambda_{{observed}} = {lo2:g}\ \mathrm{{nm}}")]
    opts = [{"value": lo2, "mistake": None, "working": work},
            {"value": _sig(zz * lr), "mistake": "That's the shift (z × λ_rest) — add it to λ_rest to get λ_observed.", "working": work},
            {"value": _sig(lr * (1 - zz)), "mistake": "A receding galaxy's light is redshifted — λ_observed is longer, not shorter.", "working": work}]
    scaffold = [{"question": "What is the redshift z?", "answer": _sig(zz)},
                {"question": "What is λ_observed, in nm?", "answer": lo2}]
    return _q(text, lo2, "nm", opts, scaffold)


# ── Type 4: Hubble's law and the age of the Universe ───────────────────────

def gen_eu_hubble(level="Higher"):
    kind = random.choice(["d_from_v", "d_from_z", "d_from_c", "v_from_d", "age"])
    if kind == "age":
        h = round(random.uniform(1.9, 2.6), 1) * 1e-18
        t_s = 1 / h
        t_y = _sig(t_s / YEAR)
        text = (f"A student obtains a value of {_txt(h, 2)} s⁻¹ for the Hubble constant. Using age = 1/H₀, calculate "
                f"the age of the Universe in years.")
        work = [_L(r"\text{age} = \frac{1}{H_0}"), _L(rf"\text{{age}} = \frac{{1}}{{{_ltx(h, 2)}}} = {_ltx(t_s)}\ \mathrm{{s}}"),
                _L(rf"\text{{age}} = \frac{{{_ltx(t_s)}}}{{3.15 \times 10^{{7}}}} = {_ltx(t_y)}\ \text{{years}}")]
        opts = [{"value": t_y, "mistake": None, "working": work},
                {"value": _sig(t_s), "mistake": "That's the age in seconds — H₀ is in s⁻¹. Divide by 3.15 × 10⁷ s per year.", "working": work},
                {"value": _sig(t_s / (365 * 24)), "mistake": "Seconds → years means dividing by 365 × 24 × 60 × 60, not just 365 × 24.", "working": work}]
        scaffold = [{"question": "What is 1/H₀, in seconds?", "answer": _sig(t_s)},
                    {"question": "What is the age of the Universe, in years?", "answer": t_y}]
        return _q(text, t_y, "years", opts, scaffold)
    if kind == "v_from_d":
        d = _sig(10 ** random.uniform(23.5, 25.5), 2)
        v = _sig(H0 * d)
        text = f"A galaxy is {_txt(d, 2)} m from the Earth. Calculate its recessional velocity."
        work = [_L(r"v = H_0 d"), _L(rf"v = 2.3 \times 10^{{-18}} \times {_ltx(d, 2)}"), _L(rf"v = {_ltx(v)}\ \mathrm{{m\,s^{{-1}}}}")]
        opts = [{"value": v, "mistake": None, "working": work},
                {"value": _sig(d / H0), "mistake": "You divided by H₀ — v = H₀d, so multiply.", "working": work},
                {"value": _sig(H0 * d / C), "mistake": "That's v ÷ c (the redshift) — the question asks for the velocity.", "working": work}]
        return _q(text, v, "m s⁻¹", opts, None)
    if kind == "d_from_v":
        v = _sig(random.uniform(1.0e6, 3.0e7), 2)
        d = _sig(v / H0)
        text = f"A galaxy has a recessional velocity of {_txt(v, 2)} m s⁻¹. Calculate the distance to the galaxy."
        work = [_L(r"v = H_0 d"), _L(rf"{_ltx(v, 2)} = 2.3 \times 10^{{-18}} \times d"), _L(rf"d = {_ltx(d)}\ \mathrm{{m}}")]
        opts = [{"value": d, "mistake": None, "working": work},
                {"value": _sig(v * H0), "mistake": "You multiplied by H₀ — rearrange v = H₀d for d.", "working": work},
                {"value": _sig(v / 1000 / H0), "mistake": "Use v in m s⁻¹, not km s⁻¹.", "working": work}]
        return _q(text, d, "m", opts, None)
    if kind == "d_from_c":
        frac = round(random.uniform(0.05, 0.40), 2)
        v = frac * C
        d = _sig(v / H0)
        text = f"A distant galaxy has a recessional velocity of {frac:g}c. Calculate the approximate distance to the galaxy."
        work = [_L(rf"v = {frac:g} \times 3.00 \times 10^{{8}} = {_ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"),
                _L(r"v = H_0 d"), _L(rf"{_ltx(v)} = 2.3 \times 10^{{-18}} \times d"), _L(rf"d = {_ltx(d)}\ \mathrm{{m}}")]
        opts = [{"value": d, "mistake": None, "working": work},
                {"value": _sig(frac / H0), "mistake": f"Convert {frac:g}c to m s⁻¹ first: {frac:g} × 3.00 × 10⁸.", "working": work},
                {"value": _sig(C / H0), "mistake": "You used c itself — the galaxy moves at a fraction of c.", "working": work}]
        scaffold = [{"question": "What is the recessional velocity, in m s⁻¹?", "answer": _sig(v)},
                    {"question": "What is the distance to the galaxy, in m?", "answer": d}]
        return _q(text, d, "m", opts, scaffold)
    z = round(random.uniform(0.005, 0.10), 3)
    v = z * C
    d = _sig(v / H0)
    text = f"The light from a distant galaxy has a redshift of {z:g}. Calculate the approximate distance to the galaxy."
    work = [_L(r"z = \frac{v}{c}"), _L(rf"{z:g} = \frac{{v}}{{3.00 \times 10^{{8}}}}"), _L(rf"v = {_ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"),
            _L(r"v = H_0 d"), _L(rf"{_ltx(v)} = 2.3 \times 10^{{-18}} \times d"), _L(rf"d = {_ltx(d)}\ \mathrm{{m}}")]
    opts = [{"value": d, "mistake": None, "working": work},
            {"value": _sig(z / H0), "mistake": "You used the redshift as the velocity — find v from z = v/c first.", "working": work},
            {"value": _sig(C / H0), "mistake": "You used c as the recessional velocity — v = z × c.", "working": work}]
    scaffold = [{"question": "What is the recessional velocity v, in m s⁻¹?", "answer": _sig(v)},
                {"question": "What is the distance d, in m?", "answer": d}]
    return _q(text, d, "m", opts, scaffold)


# ── Type 5: evidence, dark matter and dark energy ──────────────────────────
_EVIDENCE = [
    ("Measurements show that the rate of expansion of the Universe is increasing. What do physicists think is responsible?",
     "Dark energy.",
     [("Dark matter.", "Dark matter explains the extra mass of galaxies — the accelerating expansion is attributed to dark energy."),
      ("Gravity.", "Gravity acts against the expansion — it would slow it down, not speed it up."),
      ("Cosmic microwave background radiation.", "CMBR is evidence for the Big Bang, not the cause of the accelerating expansion.")]),
    ("The mass of a galaxy estimated from the orbital speeds of its stars is much greater than the mass of its visible "
     "matter. What does this provide evidence for?",
     "Dark matter.",
     [("Dark energy.", "Dark energy is linked to the accelerating expansion — extra unseen mass in galaxies is dark matter."),
      ("The expansion of the Universe.", "Orbital speeds within one galaxy tell us about its mass, not about the expansion."),
      ("The Big Bang.", "This is evidence of unseen mass (dark matter), not of the Big Bang.")]),
    ("Redshift of light from distant galaxies is evidence for the expanding Universe. Which of these is another piece of evidence?",
     "Cosmic microwave background radiation.",
     [("Light from distant galaxies is shifted to longer wavelengths.", "That's redshift again — the question asks for another piece of evidence."),
      ("The orbital speeds of stars in galaxies.", "That's evidence for dark matter, not for the expansion."),
      ("Stars have different colours.", "Stars' colours depend on their temperatures — not evidence for expansion.")]),
    ("How does the dark night sky (Olbers' paradox) support the idea of an expanding Universe?",
     "In an infinite, static Universe every line of sight would end on a star and the sky would be bright; it is dark "
     "because the Universe is expanding and has a finite age, so light from distant galaxies is redshifted out of the "
     "visible spectrum or has not yet reached us.",
     [("The night sky is dark because the Sun is on the other side of the Earth.",
       "That explains night-time, not why the sky between stars is dark — Olbers' paradox is about an infinite, static Universe."),
      ("The night sky is dark because dark matter blocks the light from distant stars.",
       "Dark matter doesn't block light — the dark sky is explained by expansion and the Universe's finite age.")]),
    ("Which force acts against the expansion of the Universe?",
     "Gravity.",
     [("Dark energy.", "Dark energy is thought to drive the accelerating expansion, not oppose it."),
      ("The strong force.", "The strong force only acts over nuclear distances.")]),
]


def gen_eu_evidence(level="Higher"):
    q, correct, wrong = random.choice(_EVIDENCE)
    return _choice(q, correct, wrong)


# ── Type 6: stellar temperature and radiation curves ────────────────────────
_STARS = [("a red dwarf", 2500, 3800), ("the Sun-like star", 5200, 6200), ("a white star", 7500, 10000),
          ("a blue giant", 12000, 30000)]


def gen_eu_stellar(level="Higher"):
    if random.random() < 0.3:
        return _choice(
            "Star X has a higher surface temperature than the Sun. How does its graph of energy emitted per second per "
            "unit area against wavelength compare with the Sun's?",
            "Its peak is at a shorter wavelength, and the curve is higher than the Sun's at every wavelength.",
            [("Its peak is at a longer wavelength, and the curve is higher at every wavelength.",
              "Hotter stars have a shorter peak wavelength (towards blue)."),
             ("Its peak is at a shorter wavelength, but the curve is lower than the Sun's at long wavelengths.",
              "A hotter star emits more at every wavelength — its curve never crosses the Sun's (2019 and 2025 course reports)."),
             ("Its curve is the same shape but shifted to longer wavelengths because its light is redshifted.",
              "The shape depends on temperature — redshift is about motion, not temperature.")])
    name, lo, hi = random.choice(_STARS)
    T = int(round(random.uniform(lo, hi), -2))
    lam = WIEN / T
    if random.random() < 0.5:
        text = (f"The surface temperature of {name} is {T} K. Using T = 2.9 × 10⁻³ / λ_peak, calculate the peak "
                f"wavelength of the radiation it emits.")
        ans = _sig(lam)
        work = [_L(r"T = \frac{2.9 \times 10^{-3}}{\lambda_{peak}}"), _L(rf"{T} = \frac{{2.9 \times 10^{{-3}}}}{{\lambda_{{peak}}}}"),
                _L(rf"\lambda_{{peak}} = {_ltx(ans)}\ \mathrm{{m}}")]
        opts = [{"value": ans, "mistake": None, "working": work},
                {"value": _sig(WIEN * T), "mistake": "You multiplied — rearrange for λ_peak = 2.9 × 10⁻³ ÷ T.", "working": work},
                {"value": _sig(T / WIEN), "mistake": "The fraction is upside down — λ_peak = 2.9 × 10⁻³ ÷ T.", "working": work}]
        return _q(text, ans, "m", opts, None)
    lam_nm = int(round(lam * 1e9))
    ans = _sig(WIEN / (lam_nm * 1e-9))
    text = (f"The radiation emitted by {name} has a peak wavelength of {lam_nm} nm. Using T = 2.9 × 10⁻³ / λ_peak, "
            f"calculate the surface temperature of the star.")
    work = [_T(f"λ_peak = {lam_nm} nm = {_txt(lam_nm * 1e-9)} m"), _L(r"T = \frac{2.9 \times 10^{-3}}{\lambda_{peak}}"),
            _L(rf"T = \frac{{2.9 \times 10^{{-3}}}}{{{_ltx(lam_nm * 1e-9)}}}"), _L(rf"T = {ans:g}\ \mathrm{{K}}")]
    opts = [{"value": ans, "mistake": None, "working": work},
            {"value": _sig(WIEN / lam_nm), "mistake": "Convert nm to m first — the constant is in m K.", "working": work},
            {"value": _sig(WIEN * lam_nm * 1e-9), "mistake": "You multiplied — T = 2.9 × 10⁻³ ÷ λ_peak.", "working": work}]
    scaffold = [{"question": "What is λ_peak in metres?", "answer": _sig(lam_nm * 1e-9)},
                {"question": "What is the surface temperature T, in K?", "answer": ans}]
    return _q(text, ans, "K", opts, scaffold)
