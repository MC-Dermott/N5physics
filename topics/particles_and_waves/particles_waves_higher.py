"""Higher Particles and Waves — exam-style question types.

Mirrors the eight Hphys Particles and Waves worksheets (Forces on Charged Particles, The Standard
Model, Nuclear Reactions, Inverse Square Law, The Photoelectric Effect, Interference, Spectra,
Refraction of Light), two generators each. Equations are written as on the Higher relationships
sheet. Distractors are the errors named in the SQA course reports 2015–2025 and marking
instructions: kV not converted and the square root forgotten; the initial Ek not added; antiquark
charges not reversed; the product mass used instead of the mass lost and c not squared; distances
not squared; photon energy given as Ek; lines per mm used as d; the central maximum not counted;
energy levels added instead of subtracted; angles measured from the surface; v × n instead of v ÷ n.
"""
import math
import random

from core.models.question_model import PhysicsQuestion
from utils.make_question import make_question

TOPIC = "Particles and Waves"
E = 1.60e-19
H = 6.63e-34
C = 3.00e8
ME = 9.11e-31
MP = 1.673e-27
_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

_NOTES = r"""
## Higher Particles and Waves

**Relationships (as on the relationships sheet):**
$$W = QV \quad E_k = \tfrac12 mv^2 \quad E = mc^2 \quad E = hf \quad E_k = hf - hf_0 \quad E_2 - E_1 = hf$$
$$v = f\lambda \quad d\sin\theta = m\lambda \quad n = \frac{\sin\theta_1}{\sin\theta_2} = \frac{\lambda_1}{\lambda_2} = \frac{v_1}{v_2} \quad \sin\theta_c = \frac1n \quad I = \frac{k}{d^2} \quad I = \frac{P}{A}$$

Data sheet: $e = 1.60\times10^{-19}$ C, $h = 6.63\times10^{-34}$ J s, $c = 3.00\times10^{8}$ m s⁻¹,
$m_e = 9.11\times10^{-31}$ kg, $m_p = 1.673\times10^{-27}$ kg.

**Common errors (SQA course reports and marking instructions):**
- Convert kV → V; after $E_k = \tfrac12 mv^2$ **take the square root**; if the particle was already moving, **add** its initial $E_k$.
- An **antiquark** has the opposite charge. A meson is a quark–antiquark pair.
- $E = mc^2$ uses the **mass lost** (before − after), and $c$ is **squared**. Don't round the masses before subtracting.
- Inverse square law: **square** the distances. A point source spreads over $4\pi r^2$.
- $E = hf$ is the photon energy; the photoelectron's $E_k = hf - hf_0$. More irradiance → more photons per second, **same** $E_k$.
- Coherent = **constant phase relationship**. $d$ = 1 ÷ (lines per metre). Count the **central maximum**.
- Energy levels are negative: $E_2 - E_1 = (-1.36) - (-5.45)$. Brighter line = more photons per second. Give the **direction** of a transition.
- Angles are from the **normal**. $v_2 = v_1 / n$. The frequency never changes. Critical angle: angle of incidence giving refraction at **90°**.
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


def _T(s):
    return {"type": "text", "content": s}


def _q(text, answer, unit, options, qtype, scaffold=None, level="Higher"):
    kept = []
    for o in options:
        o.setdefault("display", f"{_txt(o['value'])} {unit}".strip())
        if all(abs(o["value"] - k["value"]) > 0.02 * max(abs(o["value"]), abs(k["value"])) for k in kept):
            kept.append(o)
    return make_question(text, answer, kept, unit, scaffold=scaffold, notes=_NOTES,
                         topic=TOPIC, question_type=qtype, level=level)


def _choice(text, correct, wrong, qtype, level="Higher"):
    distractors = [{"value": w, "mistake": why, "working": []} for w, why in wrong]
    options = [correct] + [w for w, _ in wrong]
    random.shuffle(options)
    return PhysicsQuestion(question_text=text, correct_answer=correct, unit="", distractors=distractors,
                           working=[], notes=_NOTES, topic=TOPIC, question_type=qtype, level=level,
                           metadata={"type": "classification", "options": options})


# ════════════════ Forces on charged particles ════════════════
# (particle, charge, mass, p.d. choices (kV))
_PARTICLES = [("An electron", E, ME, [0.25, 0.60, 1.5, 2.4, 3.0]),
              ("A proton", E, MP, [2.5, 10, 25, 50]),
              ("An alpha particle", 2 * E, 6.64e-27, [1.5, 2.0, 5.0])]


def gen_pw_charged_speed(level="Higher"):
    name, q, m, vs = random.choice(_PARTICLES)
    kv = random.choice(vs)
    V = kv * 1000
    W = q * V
    moving = name == "A proton" and random.random() < 0.4
    if moving:
        u = random.choice([2.0e6, 3.0e6, 4.0e6])
        Ek0 = 0.5 * m * u * u
        v = math.sqrt(2 * (Ek0 + W) / m)
        text = (f"{name} travelling at {_txt(u, 2)} m s⁻¹ is accelerated through a potential difference of {kv:g} kV. "
                f"Calculate its speed afterwards.")
        work = [_L(rf"E_{{k,initial}} = \tfrac12 mv^2 = {_ltx(Ek0)}\ \mathrm{{J}}"), _L(rf"W = QV = {_ltx(W)}\ \mathrm{{J}}"),
                _L(rf"E_{{k,final}} = {_ltx(Ek0 + W)}\ \mathrm{{J}}"), _L(rf"v = \sqrt{{\frac{{2E_k}}{{m}}}} = {_ltx(v)}\ \mathrm{{m\,s^{{-1}}}}")]
        opts = [{"value": _sig(v), "mistake": None, "working": work},
                {"value": _sig(math.sqrt(2 * W / m)), "mistake": "The particle was already moving — add its initial Ek to the work done (course report 2022).", "working": work},
                {"value": _sig(u + math.sqrt(2 * W / m)), "mistake": "Speeds don't add — add the ENERGIES, then find v.", "working": work}]
        scaffold = [{"question": "What is the initial kinetic energy, in J?", "answer": _sig(Ek0)},
                    {"question": "What is the work done by the field, in J?", "answer": _sig(W)},
                    {"question": "What is the final speed, in m s⁻¹?", "answer": _sig(v)}]
        return _q(text, _sig(v), "m s⁻¹", opts, "Forces on Charged Particles", scaffold, level)
    v = math.sqrt(2 * W / m)
    text = f"{name} is accelerated from rest through a potential difference of {kv:g} kV. Calculate its final speed."
    work = [_L(r"W = QV"), _L(rf"W = {_ltx(q)} \times {V:g} = {_ltx(W)}\ \mathrm{{J}}"), _L(r"E_k = \tfrac12 mv^2"),
            _L(rf"{_ltx(W)} = \tfrac12 \times {_ltx(m)} \times v^2"), _L(rf"v = {_ltx(v)}\ \mathrm{{m\,s^{{-1}}}}")]
    opts = [{"value": _sig(v), "mistake": None, "working": work},
            {"value": _sig(2 * W / m), "mistake": "That's v² — take the square root.", "working": work},
            {"value": _sig(math.sqrt(2 * q * kv / m)), "mistake": "The p.d. must be in volts: kV × 1000.", "working": work},
            {"value": _sig(math.sqrt(2 * W / (ME if m != ME else MP))), "mistake": "Wrong mass — check which particle is being accelerated.", "working": work}]
    scaffold = [{"question": "What is the work done on the particle, in J?", "answer": _sig(W)},
                {"question": "What is v², in m² s⁻²?", "answer": _sig(2 * W / m)},
                {"question": "What is the final speed, in m s⁻¹?", "answer": _sig(v)}]
    return _q(text, _sig(v), "m s⁻¹", opts, "Forces on Charged Particles", scaffold, level)


def gen_pw_accelerators(level="Higher"):
    kind = random.choice(["cyclotron", "linac", "synchrotron", "field"])
    if kind == "cyclotron":
        return _choice("Why is an alternating voltage used in a cyclotron?",
                       "It switches so that the force on the particle is in the correct direction each time it crosses the gap.",
                       [("It keeps the force on the particle in the same direction.", "The particle reverses direction each half-turn — it's the CORRECT direction, not the same (course report 2023)."),
                        ("It makes the particles travel in a circle.", "The magnetic field bends the particles."),
                        ("It slows the particles down between gaps.", "The electric field accelerates them at each gap.")], "Forces on Charged Particles", level)
    if kind == "linac":
        return _choice("Why do the drift tubes in a linear accelerator get longer along the accelerator?",
                       "The particles are moving faster, so longer tubes keep the time in each tube matched to the a.c. supply.",
                       [("The particles need more room as they gain mass.", "It's the speed that increases, not (at these energies) the mass."),
                        ("Longer tubes provide a stronger electric field.", "There is no field inside the tubes; acceleration happens at the gaps."),
                        ("To slow the particles down before they collide.", "The linac accelerates particles.")], "Forces on Charged Particles", level)
    if kind == "synchrotron":
        return _choice("In a synchrotron, what are the roles of the electric and magnetic fields?",
                       "Electric fields accelerate the particles; magnetic fields bend them round the ring.",
                       [("Magnetic fields accelerate the particles; electric fields bend them.", "It is the other way round."),
                        ("Both fields only bend the particles.", "The electric fields do work on the particles and speed them up."),
                        ("The magnetic field is kept constant as the particles speed up.", "It must increase to keep faster particles on the same path.")], "Forces on Charged Particles", level)
    return _choice("Which describes the electric field between a positive plate (top) and a negative plate (bottom)?",
                   "Evenly spaced parallel lines with arrows pointing downwards, from + to −.",
                   [("Evenly spaced parallel lines with arrows pointing upwards, from − to +.", "Field lines point from positive to negative (course report 2024)."),
                    ("Radial lines spreading out from the centre.", "That's the field of a point charge."),
                    ("Curved lines bulging outwards between the plates.", "Between parallel plates the field is uniform (apart from the edges).")], "Forces on Charged Particles", level)


# ════════════════ Standard Model ════════════════
_Q = {"u": 2 / 3, "d": -1 / 3, "s": -1 / 3, "c": 2 / 3, "b": -1 / 3, "t": 2 / 3}
_NAME = {"u": "up", "d": "down", "s": "strange", "c": "charm", "b": "bottom", "t": "top"}


def _frac(x):
    from fractions import Fraction
    fr = Fraction(x).limit_denominator(3)
    if fr == 0:
        return "0"
    sign = "+" if fr > 0 else "−"
    fr = abs(fr)
    return f"{sign}{fr.numerator}" if fr.denominator == 1 else f"{sign}{fr.numerator}/{fr.denominator}"


def gen_pw_hadron_charge(level="Higher"):
    meson = random.random() < 0.5
    if meson:
        parts = [(random.choice("udsc"), False), (random.choice("udsc"), True)]
    else:
        parts = [(random.choice("udsc"), random.random() < 0.15) for _ in range(3)]
    charges = [-_Q[q] if anti else _Q[q] for q, anti in parts]
    charge = round(sum(charges))
    naive = sum(_Q[q] for q, _ in parts)
    words = ", ".join(("anti-" if anti else "") + _NAME[q] for q, anti in parts)
    text = f"A {'meson' if meson else 'particle'} is made of the following quarks: {words}. Determine its charge, in units of e."
    work = [_T("Add the quark charges; an antiquark has the opposite charge to its quark."),
            _T(" + ".join(f"({_frac(c)})" for c in charges) + f" = {_frac(charge)}e")]
    opts = [{"value": float(charge), "mistake": None, "working": work, "display": f"{_frac(charge)}e"}]
    for val, why in [(naive, "An antiquark's charge is the opposite of its quark's."),
                     (charge + 1, "Add the fractions carefully: up-type +⅔, down-type −⅓."),
                     (charge - 1, "Add the fractions carefully: up-type +⅔, down-type −⅓.")]:
        if all(abs(val - o["value"]) > 1e-6 for o in opts):
            opts.append({"value": float(val), "mistake": why, "working": work, "display": f"{_frac(val)}e"})
    return make_question(text, float(charge), opts[:4], "e", scaffold=None, notes=_NOTES,
                         topic=TOPIC, question_type="The Standard Model", level=level)


def gen_pw_bosons(level="Higher"):
    kind = random.choice(["strong", "weak", "neutrino", "meson", "fundamental"])
    if kind == "strong":
        return _choice("Which particle mediates the strong force?", "the gluon",
                       [("the W boson", "W and Z bosons mediate the weak force (course report 2019)."), ("the photon", "Photons mediate the electromagnetic force."),
                        ("the graviton", "The (hypothetical) graviton would mediate gravity.")], "The Standard Model", level)
    if kind == "weak":
        return _choice("Which force is associated with beta decay, and which bosons mediate it?", "the weak force — W and Z bosons",
                       [("the strong force — gluons", "Beta decay is a weak-force process."), ("the electromagnetic force — photons", "Beta decay is a weak-force process."),
                        ("the weak force — gluons", "Gluons mediate the strong force.")], "The Standard Model", level)
    if kind == "neutrino":
        return _choice("What evidence led to the neutrino being proposed?", "Beta particles are emitted with a range of kinetic energies.",
                       [("Alpha decay produces particles of a single energy.", "It was BETA decay (course report 2019)."),
                        ("Gamma rays have no charge.", "Unrelated to the neutrino."), ("Protons are made of three quarks.", "Unrelated to the neutrino.")], "The Standard Model", level)
    if kind == "meson":
        return _choice("What is a meson?", "a hadron made of a quark and an antiquark",
                       [("a particle made of two quarks", "Must be a quark and an ANTIquark (MI)."), ("a hadron made of three quarks", "That's a baryon."),
                        ("a fundamental particle like the electron", "Mesons are made of quarks; electrons are leptons.")], "The Standard Model", level)
    return _choice("What is meant by a fundamental particle?", "a particle that cannot be broken down into smaller particles",
                   [("a very small particle", "Size isn't the definition — it can't be subdivided."), ("a particle made of quarks", "Hadrons are made of quarks and are NOT fundamental."),
                    ("a particle that carries a force", "That describes a boson.")], "The Standard Model", level)


# ════════════════ Nuclear reactions ════════════════
# (reaction text, masses before (kg), masses after (kg))
_REACTIONS = [
    ("²H + ³H → ⁴He + n", [3.3436e-27, 5.0082e-27], [6.6465e-27, 1.6749e-27]),
    ("²H + ²H → ³He + n", [3.3436e-27, 3.3436e-27], [5.0064e-27, 1.6749e-27]),
    ("4 ¹H → ⁴He + 2e⁺", [1.6726e-27] * 4, [6.6447e-27]),
    ("²³⁵U + n → ¹⁴¹Ba + ⁹²Kr + 3n", [390.2997e-27, 1.6749e-27], [233.9719e-27, 152.5997e-27, 3 * 1.6749e-27]),
]


def gen_pw_mass_energy(level="Higher"):
    rx, before, after = random.choice(_REACTIONS)
    mb, ma = sum(before), sum(after)
    dm = mb - ma
    En = dm * C * C
    text = (f"In the reaction {rx}, the total mass before is {mb * 1e27:.4f} × 10⁻²⁷ kg and the total mass after is "
            f"{ma * 1e27:.4f} × 10⁻²⁷ kg. Calculate the energy released.")
    work = [_L(rf"\Delta m = {mb * 1e27:.4f}\times10^{{-27}} - {ma * 1e27:.4f}\times10^{{-27}} = {_ltx(dm)}\ \mathrm{{kg}}"),
            _L(r"E = mc^2"), _L(rf"E = {_ltx(dm)} \times (3.00\times10^{{8}})^2"), _L(rf"E = {_ltx(En)}\ \mathrm{{J}}")]
    opts = [{"value": _sig(En), "mistake": None, "working": work},
            {"value": _sig(ma * C * C), "mistake": "Use the mass LOST (before − after), not the mass of the products.", "working": work},
            {"value": _sig(dm * C), "mistake": "c must be squared.", "working": work}]
    scaffold = [{"question": "What is the mass lost, in kg?", "answer": _sig(dm)}, {"question": "What is the energy released, in J?", "answer": _sig(En)}]
    return _q(text, _sig(En), "J", opts, "Nuclear Reactions", scaffold, level)


def gen_pw_reactions_per_second(level="Higher"):
    ctx = random.choice([("A nuclear power station", 1.0e9, 3.0e9, 3.2e-11), ("The Sun", 3.8e26, 3.8e26, 4.1e-12),
                         ("A fusion test reactor", 1.0e7, 5.0e7, 2.8e-12)])
    name, plo, phi, Er = ctx
    P = _sig(random.uniform(plo, phi), 2)
    n = P / Er
    text = f"{name} has a power output of {_txt(P, 2)} W. Each reaction releases {_txt(Er, 2)} J. Calculate the number of reactions each second."
    work = [_T("number per second = energy per second ÷ energy per reaction"), _L(rf"n = \frac{{{_ltx(P, 2)}}}{{{_ltx(Er, 2)}}} = {_ltx(n)}")]
    opts = [{"value": _sig(n), "mistake": None, "working": work},
            {"value": _sig(P * Er), "mistake": "Divide the power by the energy per reaction.", "working": work},
            {"value": _sig(Er / P), "mistake": "The fraction is upside down.", "working": work}]
    return _q(text, _sig(n), "reactions per second", opts, "Nuclear Reactions", None, level)


# ════════════════ Inverse square law ════════════════
def gen_pw_isl(level="Higher"):
    d1 = random.choice([0.40, 0.50, 0.80, 1.5, 2.0, 3.0, 4.0])
    I1 = random.choice([12, 18, 20, 32, 40, 50])
    if random.random() < 0.6:
        k = random.choice([1.5, 2, 2.5, 3, 4])
        d2 = _sig(d1 * k, 3)
        I2 = I1 * d1 ** 2 / d2 ** 2
        text = f"The irradiance of light from a point source is {I1} W m⁻² at {d1:g} m. Calculate the irradiance at {d2:g} m."
        work = [_L(r"I_1d_1^2 = I_2d_2^2"), _L(rf"{I1} \times {d1:g}^2 = I_2 \times {d2:g}^2"), _L(rf"I_2 = {_ltx(I2)}\ \mathrm{{W\,m^{{-2}}}}")]
        opts = [{"value": _sig(I2), "mistake": None, "working": work},
                {"value": _sig(I1 * d1 / d2), "mistake": "Square the distances — it is an inverse SQUARE law.", "working": work},
                {"value": _sig(I1 * d2 ** 2 / d1 ** 2), "mistake": "Irradiance DEcreases further away — the ratio is upside down.", "working": work},
                {"value": _sig(I1 * d1 ** 2 / d2), "mistake": "Square BOTH distances.", "working": work}]
        return _q(text, _sig(I2), "W m⁻²", opts, "Inverse Square Law", None, level)
    f = random.choice([4, 9, 16, 0.25])
    I2 = I1 * f
    d2 = d1 / math.sqrt(f)
    text = f"The irradiance of light from a point source is {I1} W m⁻² at {d1:g} m. At what distance is it {_txt(I2)} W m⁻²?"
    work = [_L(r"I_1d_1^2 = I_2d_2^2"), _L(rf"{I1} \times {d1:g}^2 = {_ltx(I2)} \times d_2^2"), _L(rf"d_2^2 = {_ltx(d2 ** 2)}"), _L(rf"d_2 = {_ltx(d2)}\ \mathrm{{m}}")]
    opts = [{"value": _sig(d2), "mistake": None, "working": work},
            {"value": _sig(d2 ** 2), "mistake": "That's d₂² — take the square root.", "working": work},
            {"value": _sig(d1 / f), "mistake": "Irradiance ∝ 1/d², so the distance changes by √ of the factor.", "working": work},
            {"value": _sig(d1 * math.sqrt(f)), "mistake": "A higher irradiance means CLOSER to the source.", "working": work}]
    scaffold = [{"question": "What is d₂², in m²?", "answer": _sig(d2 ** 2)}, {"question": "What is d₂, in m?", "answer": _sig(d2)}]
    return _q(text, _sig(d2), "m", opts, "Inverse Square Law", scaffold, level)


def gen_pw_irradiance(level="Higher"):
    if random.random() < 0.5:
        P = random.choice([12, 24, 40, 60, 100])
        r = random.choice([1.0, 1.5, 2.0, 2.5, 3.0])
        A = 4 * math.pi * r * r
        I = P / A
        text = f"A {P} W lamp can be treated as a point source. Calculate the irradiance {r:g} m from the lamp."
        work = [_L(rf"A = 4\pi r^2 = 4\pi \times {r:g}^2 = {_ltx(A)}\ \mathrm{{m^2}}"), _L(r"I = \frac{P}{A}"), _L(rf"I = {_ltx(I)}\ \mathrm{{W\,m^{{-2}}}}")]
        opts = [{"value": _sig(I), "mistake": None, "working": work},
                {"value": _sig(P / (r * r)), "mistake": "The light spreads over a SPHERE: A = 4πr² (course report 2015).", "working": work},
                {"value": _sig(P / (math.pi * r * r)), "mistake": "A point source spreads over a sphere (4πr²), not a circle.", "working": work}]
        scaffold = [{"question": "What is the area of the sphere, in m²?", "answer": _sig(A)}, {"question": "What is the irradiance, in W m⁻²?", "answer": _sig(I)}]
        return _q(text, _sig(I), "W m⁻²", opts, "Inverse Square Law", scaffold, level)
    Pmw = random.choice([1.0, 3.0, 5.0])
    dmm = random.choice([1.0, 2.0, 3.0, 4.0])
    r = dmm / 2 * 1e-3
    A = math.pi * r * r
    I = Pmw * 1e-3 / A
    text = f"A {Pmw:g} mW laser makes a circular spot of diameter {dmm:g} mm. Calculate the irradiance of the spot."
    work = [_L(rf"A = \pi r^2 = \pi \times ({_ltx(r)})^2 = {_ltx(A)}\ \mathrm{{m^2}}"), _L(r"I = \frac{P}{A}"), _L(rf"I = {_ltx(I)}\ \mathrm{{W\,m^{{-2}}}}")]
    opts = [{"value": _sig(I), "mistake": None, "working": work},
            {"value": _sig(Pmw * 1e-3 / (math.pi * (dmm * 1e-3) ** 2)), "mistake": "The radius is half the diameter.", "working": work},
            {"value": _sig(Pmw / A), "mistake": "The power must be in watts: mW × 10⁻³.", "working": work}]
    scaffold = [{"question": "What is the area of the spot, in m²?", "answer": _sig(A)}, {"question": "What is the irradiance, in W m⁻²?", "answer": _sig(I)}]
    return _q(text, _sig(I), "W m⁻²", opts, "Inverse Square Law", scaffold, level)


# ════════════════ Photoelectric effect ════════════════
_METALS = [("potassium", 3.7e-19), ("calcium", 4.6e-19), ("zinc", 5.81e-19), ("aluminium", 6.6e-19), ("copper", 7.5e-19)]


def gen_pw_photoelectric(level="Higher"):
    metal, wf = random.choice(_METALS)
    lam_nm = random.choice([150, 180, 200, 220, 250])
    f = C / (lam_nm * 1e-9)
    Eph = H * f
    if Eph <= wf * 1.05:
        lam_nm = 150; f = C / 150e-9; Eph = H * f
    Ek = Eph - wf
    if random.random() < 0.5:
        text = f"UV radiation of wavelength {lam_nm} nm falls on {metal} (work function {_txt(wf, 3)} J). Calculate the maximum kinetic energy of the photoelectrons."
        work = [_L(rf"f = \frac{{v}}{{\lambda}} = {_ltx(f)}\ \mathrm{{Hz}}"), _L(r"E_k = hf - hf_0"), _L(rf"E_k = (6.63\times10^{{-34}} \times {_ltx(f)}) - {_ltx(wf)}"),
                _L(rf"E_k = {_ltx(Ek)}\ \mathrm{{J}}")]
        opts = [{"value": _sig(Ek), "mistake": None, "working": work},
                {"value": _sig(Eph), "mistake": "That's the photon energy — subtract the work function (course report 2025).", "working": work},
                {"value": _sig(Eph + wf), "mistake": "Ek = hf − hf₀: subtract the work function.", "working": work}]
        scaffold = [{"question": "What is the frequency of the radiation, in Hz?", "answer": _sig(f)},
                    {"question": "What is the energy of each photon, in J?", "answer": _sig(Eph)},
                    {"question": "What is the maximum Ek, in J?", "answer": _sig(Ek)}]
        return _q(text, _sig(Ek), "J", opts, "The Photoelectric Effect", scaffold, level)
    v = math.sqrt(2 * Ek / ME)
    text = f"UV radiation of wavelength {lam_nm} nm falls on {metal} (work function {_txt(wf, 3)} J). Calculate the maximum speed of the photoelectrons."
    work = [_L(rf"E = hf = {_ltx(Eph)}\ \mathrm{{J}}"), _L(rf"E_k = {_ltx(Eph)} - {_ltx(wf)} = {_ltx(Ek)}\ \mathrm{{J}}"), _L(rf"v = \sqrt{{\frac{{2E_k}}{{m}}}} = {_ltx(v)}\ \mathrm{{m\,s^{{-1}}}}")]
    opts = [{"value": _sig(v), "mistake": None, "working": work},
            {"value": _sig(math.sqrt(2 * Eph / ME)), "mistake": "Use Ek = hf − hf₀, not the photon energy.", "working": work},
            {"value": _sig(2 * Ek / ME), "mistake": "That's v² — take the square root.", "working": work}]
    scaffold = [{"question": "What is the energy of each photon, in J?", "answer": _sig(Eph)},
                {"question": "What is the maximum Ek of the photoelectrons, in J?", "answer": _sig(Ek)},
                {"question": "What is the maximum speed, in m s⁻¹?", "answer": _sig(v)}]
    return _q(text, _sig(v), "m s⁻¹", opts, "The Photoelectric Effect", scaffold, level)


def gen_pw_pe_effects(level="Higher"):
    kind = random.choice(["irradiance", "frequency_same_I", "closer", "workfunction", "evidence"])
    if kind == "irradiance":
        return _choice("The irradiance of UV on a metal is increased; the frequency is unchanged. What happens?",
                       "More photoelectrons per second; the same maximum Ek.",
                       [("Fewer photoelectrons, each with more Ek.", "Each photon's energy is unchanged, so Ek max is unchanged."),
                        ("The same number of photoelectrons, each with more Ek.", "One photon releases one electron: brighter means more photons, not more energetic ones."),
                        ("No photoelectrons are emitted.", "The frequency is still above the threshold.")], "The Photoelectric Effect", level)
    if kind == "frequency_same_I":
        return _choice("The frequency of the radiation is increased but the irradiance is kept the same. What happens?",
                       "The maximum Ek increases and fewer photoelectrons are emitted per second.",
                       [("The maximum Ek increases and the number per second is unchanged.", "Same irradiance, more energy per photon ⇒ fewer photons per second (course report 2017)."),
                        ("The maximum Ek is unchanged and more photoelectrons are emitted.", "Higher frequency means more energy per photon."),
                        ("Nothing changes.", "Ek max depends on frequency.")], "The Photoelectric Effect", level)
    if kind == "closer":
        return _choice("A UV lamp is moved closer to a zinc plate. Why does the current increase?",
                       "More photons per second reach the plate, so more photoelectrons are emitted per second.",
                       [("Each photon has more energy.", "Moving the lamp changes the irradiance, not the photon energy (course report 2024)."),
                        ("The work function of zinc decreases.", "The work function is a property of the metal."),
                        ("The electrons move faster.", "Ek max depends only on the frequency.")], "The Photoelectric Effect", level)
    if kind == "workfunction":
        return _choice("What is meant by the work function of a metal?", "The minimum energy needed to release an electron from its surface.",
                       [("The energy needed to release an electron.", "Must say MINIMUM (course report 2025)."),
                        ("The frequency below which no electrons are emitted.", "That's the threshold frequency."),
                        ("The kinetic energy of the emitted electrons.", "Ek = hf − hf₀.")], "The Photoelectric Effect", level)
    return _choice("Why is the photoelectric effect evidence for the particle model of light?",
                   "One photon releases one electron; below the threshold frequency no electrons are emitted however intense the light.",
                   [("Light forms interference patterns.", "Interference is evidence for the WAVE model."),
                    ("Brighter light gives faster electrons.", "It doesn't — that's the point."),
                    ("Light travels at 3.00 × 10⁸ m s⁻¹.", "True of both models; not evidence for particles.")], "The Photoelectric Effect", level)


# ════════════════ Interference ════════════════
def gen_pw_grating(level="Higher"):
    lpm = random.choice([100, 250, 300, 400, 500, 600])
    lam_nm = random.choice([405, 450, 532, 589, 633, 650])
    d = 1 / (lpm * 1000)
    mmax = int(d / (lam_nm * 1e-9))
    kind = random.choice(["angle", "angle", "count"])
    if kind == "angle":
        m = random.randint(1, max(1, min(3, mmax)))
        s = m * lam_nm * 1e-9 / d
        th = math.degrees(math.asin(s))
        text = f"Light of wavelength {lam_nm} nm passes through a grating with {lpm} lines per mm. Calculate the angle to the order {m} maximum."
        work = [_L(rf"d = \frac{{1}}{{{lpm} \times 10^3}} = {_ltx(d)}\ \mathrm{{m}}"), _L(r"d\sin\theta = m\lambda"),
                _L(rf"{_ltx(d)} \times \sin\theta = {m} \times {lam_nm}\times10^{{-9}}"), _L(rf"\theta = {th:.1f}^\circ")]
        opts = [{"value": round(th, 1), "mistake": None, "working": work},
                {"value": round(math.degrees(math.asin(min(1, lam_nm * 1e-9 / d))), 1) if m != 1 else round(th * 2, 1), "mistake": "Include the order m in mλ." if m != 1 else "Check the order and the arithmetic.", "working": work},
                {"value": round(math.degrees(math.asin(min(0.999, s / 2))), 1), "mistake": "d = 1 ÷ lines per METRE — check the conversion.", "working": work},
                {"value": round(math.asin(s), 3), "mistake": "Your calculator is in radian mode — set it to degrees.", "working": work}]
        scaffold = [{"question": "What is the slit separation d, in m?", "answer": _sig(d)}, {"question": "What is sin θ?", "answer": _sig(s)},
                    {"question": "What is θ, in degrees?", "answer": round(th, 1)}]
        return _q(text, round(th, 1), "°", opts, "Interference", scaffold, level)
    total = 2 * mmax + 1
    text = f"Light of wavelength {lam_nm} nm passes through a grating with {lpm} lines per mm. Determine the total number of maxima on the screen."
    work = [_L(rf"d = {_ltx(d)}\ \mathrm{{m}}"), _L(rf"m_{{max}} = \frac{{d}}{{\lambda}} = {d / (lam_nm * 1e-9):.2f} \Rightarrow {mmax}"),
            _T(f"{mmax} on each side + the central maximum = {total}")]
    opts = [{"value": float(total), "mistake": None, "working": work},
            {"value": float(2 * mmax), "mistake": "Don't forget the central maximum (course report 2023).", "working": work},
            {"value": float(mmax), "mistake": "There are maxima on BOTH sides of the centre.", "working": work}]
    return _q(text, float(total), "maxima", opts, "Interference", None, level)


def gen_pw_path_difference(level="Higher"):
    lam = random.choice([0.20, 0.25, 0.40, 0.50])
    maxmin = random.choice(["maximum", "minimum"])
    m = random.randint(1, 3)
    ordinal = {1: "first", 2: "second", 3: "third"}
    if maxmin == "maximum":
        pd = m * lam
        text = f"Two loudspeakers emit coherent sound. At the {ordinal[m]}-order maximum the path difference is {pd:g} m. Calculate the wavelength."
        wrong = pd / (m + 0.5)
        work = [_L(r"\text{path difference} = m\lambda"), _L(rf"{pd:g} = {m} \times \lambda"), _L(rf"\lambda = {lam:g}\ \mathrm{{m}}")]
        opts = [{"value": lam, "mistake": None, "working": work},
                {"value": _sig(wrong), "mistake": "A MAXIMUM uses mλ; (m + ½)λ is for a minimum.", "working": work},
                {"value": pd, "mistake": "Divide by the order m.", "working": work},
                {"value": _sig(pd * m), "mistake": "path difference = mλ, so λ = path difference ÷ m.", "working": work},
                {"value": _sig(pd / (m + 1)), "mistake": "The central maximum is m = 0, so the first-order maximum is m = 1.", "working": work}]
    else:
        pd = (m - 1 + 0.5) * lam
        text = f"Two loudspeakers emit coherent sound. At the {ordinal[m]} minimum from the centre the path difference is {_txt(pd)} m. Calculate the wavelength."
        work = [_L(r"\text{path difference} = (m + \tfrac12)\lambda"), _T(f"The {ordinal[m]} minimum has m = {m - 1}."),
                _L(rf"{_ltx(pd)} = {m - 0.5:g} \times \lambda"), _L(rf"\lambda = {lam:g}\ \mathrm{{m}}")]
        opts = [{"value": lam, "mistake": None, "working": work},
                {"value": _sig(pd / m), "mistake": "A minimum uses (m + ½)λ, and the first minimum is m = 0.", "working": work},
                {"value": _sig(pd / (m + 0.5)), "mistake": f"The {ordinal[m]} minimum has m = {m - 1}, not m = {m}.", "working": work},
                {"value": _sig(pd * (m - 0.5)), "mistake": "Divide the path difference by (m + ½), don't multiply.", "working": work}]
    return _q(text, lam, "m", opts, "Interference", None, level)


# ════════════════ Spectra ════════════════
_LEVELS = [("E₄", -0.871e-19), ("E₃", -1.36e-19), ("E₂", -2.42e-19), ("E₁", -5.45e-19), ("E₀", -21.8e-19)]
_LV_TXT = ", ".join(f"{n} = {_txt(v, 3)} J" for n, v in _LEVELS)


def gen_pw_energy_levels(level="Higher"):
    i, j = sorted(random.sample(range(5), 2))
    (nu, Eu), (nl, El) = _LEVELS[i], _LEVELS[j]
    dE = Eu - El
    f = dE / H
    lam = C / f
    if random.random() < 0.5:
        text = f"Energy levels of hydrogen: {_LV_TXT}. An electron falls from {nu} to {nl}. Calculate the frequency of the photon emitted."
        work = [_L(r"E_2 - E_1 = hf"), _L(rf"{_ltx(Eu)} - ({_ltx(El)}) = 6.63\times10^{{-34}} \times f"), _L(rf"f = {_ltx(f)}\ \mathrm{{Hz}}")]
        opts = [{"value": _sig(f), "mistake": None, "working": work},
                {"value": _sig(abs(Eu + El) / H), "mistake": "The levels have been added — subtract: E_upper − E_lower.", "working": work},
                {"value": _sig(abs(Eu) / H), "mistake": "Use the DIFFERENCE between the two levels.", "working": work}]
        scaffold = [{"question": "What is the energy difference, in J?", "answer": _sig(dE)}, {"question": "What is the frequency, in Hz?", "answer": _sig(f)}]
        return _q(text, _sig(f), "Hz", opts, "Spectra", scaffold, level)
    text = f"Energy levels of hydrogen: {_LV_TXT}. An electron falls from {nu} to {nl}. Calculate the wavelength of the photon emitted."
    work = [_L(rf"\Delta E = {_ltx(dE)}\ \mathrm{{J}}"), _L(rf"f = \frac{{\Delta E}}{{h}} = {_ltx(f)}\ \mathrm{{Hz}}"), _L(rf"\lambda = \frac{{v}}{{f}} = {_ltx(lam)}\ \mathrm{{m}}")]
    opts = [{"value": _sig(lam), "mistake": None, "working": work},
            {"value": _sig(f), "mistake": "That's the frequency — use v = fλ for the wavelength.", "working": work},
            {"value": _sig(C / (abs(Eu + El) / H)), "mistake": "Subtract the energy levels, don't add them.", "working": work}]
    scaffold = [{"question": "What is the energy difference, in J?", "answer": _sig(dE)}, {"question": "What is the frequency, in Hz?", "answer": _sig(f)},
                {"question": "What is the wavelength, in m?", "answer": _sig(lam)}]
    return _q(text, _sig(lam), "m", opts, "Spectra", scaffold, level)


def gen_pw_spectra_explain(level="Higher"):
    kind = random.choice(["emission", "absorption", "bright", "bohr"])
    if kind == "emission":
        return _choice("How is a line emission spectrum produced?",
                       "Electrons fall from higher to lower energy levels, emitting photons of specific frequencies.",
                       [("Electrons absorb photons and move to higher levels.", "That describes absorption (course report 2023)."),
                        ("Photons move between energy levels.", "It is the ELECTRONS that move between levels."),
                        ("White light passes through a cool gas.", "That produces an absorption spectrum.")], "Spectra", level)
    if kind == "absorption":
        return _choice("Why are there dark lines in the spectrum of sunlight?",
                       "Certain frequencies are absorbed by gases in the Sun's outer layers as electrons move to higher levels.",
                       [("Light is absorbed by the atmosphere.", "Must say CERTAIN frequencies, in the Sun's outer layers (MI)."),
                        ("Electrons fall to lower levels and emit photons.", "That's emission (course report 2025)."),
                        ("Some colours are not made by the Sun.", "The missing frequencies are absorbed.")], "Spectra", level)
    if kind == "bright":
        return _choice("Why is one line in an emission spectrum brighter than the others?",
                       "More electrons make that transition per second, so more photons of that frequency are emitted per second.",
                       [("Its photons have more energy.", "Brightness depends on the NUMBER of photons per second (course reports 2022–2024)."),
                        ("That transition has the largest energy gap.", "A larger gap gives a higher frequency, not a brighter line."),
                        ("Its electrons move faster.", "Brightness is about photons per second.")], "Spectra", level)
    return _choice("Which is a feature of the Bohr model of the atom?",
                   "Electrons occupy discrete energy levels around a positive nucleus.",
                   [("The atom is mostly empty space with a dense nucleus.", "That's Rutherford's model (course report 2018)."),
                    ("Electrons are spread through a positive sphere.", "That's the plum-pudding model."),
                    ("Electrons can have any energy.", "In the Bohr model the energies are discrete.")], "Spectra", level)


# ════════════════ Refraction ════════════════
def _sind(a):
    return math.sin(math.radians(a))


def gen_pw_refraction(level="Higher"):
    kind = random.choice(["n", "theta2", "speed", "critical"])
    n = random.choice([1.33, 1.47, 1.50, 1.53, 1.54, 2.42])
    if kind == "n":
        t1 = random.choice([30, 35, 40, 45, 50, 55])
        t2 = math.degrees(math.asin(_sind(t1) / n))
        t2r = round(t2, 1)
        nn = _sind(t1) / _sind(t2r)
        surf = random.random() < 0.4
        if surf:
            text = (f"A ray of light passes from air into a block. The angle between the incident ray and the SURFACE is {90 - t1}° and the angle "
                    f"between the refracted ray and the surface is {round(90 - t2r, 1):g}°. Calculate the refractive index.")
        else:
            text = f"A ray passes from air into a material. The angle of incidence is {t1}° and the angle of refraction is {t2r:g}°. Calculate the refractive index."
        work = ([_T(f"Angles to the normal: θ₁ = 90 − {90 - t1} = {t1}°, θ₂ = {t2r:g}°")] if surf else []) + \
               [_L(r"n = \frac{\sin\theta_1}{\sin\theta_2}"), _L(rf"n = \frac{{\sin {t1}^\circ}}{{\sin {t2r:g}^\circ}}"), _L(rf"n = {nn:.2f}")]
        opts = [{"value": round(nn, 2), "mistake": None, "working": work},
                {"value": round(_sind(t2r) / _sind(t1), 2), "mistake": "The ratio is upside down: sin θ(air) ÷ sin θ(material).", "working": work},
                {"value": round(t1 / t2r, 2), "mistake": "Use the SINES of the angles.", "working": work}]
        if surf:
            opts.append({"value": round(_sind(90 - t1) / _sind(90 - t2r), 2), "mistake": "Angles must be measured from the NORMAL, not the surface.", "working": work})
        return _q(text, round(nn, 2), "", opts, "Refraction of Light", None, level)
    if kind == "theta2":
        t1 = random.choice([30, 36, 40, 45, 49, 55])
        t2 = math.degrees(math.asin(_sind(t1) / n))
        text = f"A ray enters a material of refractive index {n} at an angle of incidence of {t1}°. Calculate the angle of refraction."
        work = [_L(r"n = \frac{\sin\theta_1}{\sin\theta_2}"), _L(rf"{n} = \frac{{\sin {t1}^\circ}}{{\sin\theta_2}}"), _L(rf"\theta_2 = {t2:.1f}^\circ")]
        opts = [{"value": round(t2, 1), "mistake": None, "working": work},
                {"value": round(t1 / n, 1), "mistake": "Divide the SINE of the angle by n, then take sin⁻¹.", "working": work},
                {"value": round(90 - t2, 1), "mistake": "That's the angle to the SURFACE — angles are measured from the normal.", "working": work}]
        if _sind(t1) * n < 1:
            opts.append({"value": round(math.degrees(math.asin(_sind(t1) * n)), 1), "mistake": "The ray bends TOWARDS the normal in the denser material: sin θ₂ = sin θ₁ ÷ n.", "working": work})
        scaffold = [{"question": "What is sin θ₂?", "answer": _sig(_sind(t1) / n)}, {"question": "What is θ₂, in degrees?", "answer": round(t2, 1)}]
        return _q(text, round(t2, 1), "°", opts, "Refraction of Light", scaffold, level)
    if kind == "speed":
        v = C / n
        text = f"The refractive index of a material is {n}. Calculate the speed of light in the material."
        work = [_L(r"n = \frac{v_1}{v_2}"), _L(rf"{n} = \frac{{3.00\times10^8}}{{v_2}}"), _L(rf"v_2 = {_ltx(v)}\ \mathrm{{m\,s^{{-1}}}}")]
        opts = [{"value": _sig(v), "mistake": None, "working": work},
                {"value": _sig(C * n), "mistake": "Light is SLOWER in the material: divide by n.", "working": work},
                {"value": _sig(C / n ** 2), "mistake": "n = v₁ / v₂ — divide by n once.", "working": work}]
        return _q(text, _sig(v), "m s⁻¹", opts, "Refraction of Light", None, level)
    tc = math.degrees(math.asin(1 / n))
    text = f"Calculate the critical angle for a material of refractive index {n}."
    work = [_L(r"\sin\theta_c = \frac{1}{n}"), _L(rf"\sin\theta_c = \frac{{1}}{{{n}}}"), _L(rf"\theta_c = {tc:.1f}^\circ")]
    opts = [{"value": round(tc, 1), "mistake": None, "working": work},
            {"value": round(math.degrees(math.acos(1 / n)), 1), "mistake": "Use sin⁻¹, not cos⁻¹.", "working": work},
            {"value": round(90 / n, 1), "mistake": "sin θc = 1/n — take sin⁻¹ of 1/n.", "working": work}]
    scaffold = [{"question": "What is sin θc?", "answer": _sig(1 / n)}, {"question": "What is θc, in degrees?", "answer": round(tc, 1)}]
    return _q(text, round(tc, 1), "°", opts, "Refraction of Light", scaffold, level)


def gen_pw_refraction_explain(level="Higher"):
    kind = random.choice(["critical", "frequency", "process", "tir"])
    if kind == "critical":
        return _choice("What is meant by the critical angle?", "The angle of incidence that produces an angle of refraction of 90°.",
                       [("The angle at which total internal reflection happens.", "Must be defined by the refraction angle of 90° (course report 2023)."),
                        ("The largest angle of refraction possible.", "It is an angle of INCIDENCE."), ("The angle between the ray and the surface.", "Angles are from the normal.")],
                       "Refraction of Light", level)
    if kind == "frequency":
        return _choice("Light passes from air into glass. What happens to its speed, frequency and wavelength?",
                       "speed decreases, frequency stays the same, wavelength decreases",
                       [("speed decreases, frequency decreases, wavelength stays the same", "The frequency NEVER changes on refraction."),
                        ("speed stays the same, frequency increases, wavelength decreases", "The speed changes; the frequency doesn't."),
                        ("speed increases, frequency stays the same, wavelength increases", "Glass is denser — light slows down.")], "Refraction of Light", level)
    if kind == "process":
        return _choice("How should several measured pairs of angles be processed to find the refractive index reliably?",
                       "Plot sin θ₁ against sin θ₂; the refractive index is the gradient.",
                       [("Calculate n for each pair and take the average.", "Invalid averaging — use the gradient (course report 2024)."),
                        ("Plot θ₁ against θ₂ and use the gradient.", "It is the SINES that are proportional."),
                        ("Use only the largest angle.", "Use all the data via a graph.")], "Refraction of Light", level)
    return _choice("A ray inside a Perspex block (critical angle 41.8°) meets the flat face at 50° to the normal. What happens?",
                   "It is totally internally reflected at 50° to the normal.",
                   [("It refracts out into the air, bending away from the normal.", "50° is above the critical angle (course report 2024)."),
                    ("It travels along the surface at 90°.", "That only happens exactly AT the critical angle."),
                    ("It passes straight through without bending.", "It meets the boundary at a large angle — TIR.")], "Refraction of Light", level)
