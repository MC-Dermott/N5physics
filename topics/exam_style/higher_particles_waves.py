"""Higher Particles and Waves — exam-style multi-part questions, one generator per topic.

Recognised wrong answers follow the Higher marking instructions and course reports: ½ or the square
root dropped from Ek = ½mv², the proton mass used for an electron, nm/mm not converted, the
irradiance ratio not squared or inverted, the work function added instead of subtracted, d taken as
the number of lines per mm, sin used for n the wrong way up, and the critical angle confused with the
angle of refraction.
"""
import math
import random

from topics.exam_style.base import Exam, T, exam_style, fmt, ltx, pick, sig

UNIT = "Particles and Waves"
E = 1.60e-19
H = 6.63e-34
C = 3.00e8
ME = 9.11e-31
MP = 1.67e-27


def _notes(title, body):
    return f"## {title} — exam technique\n\n{body}"


NOTES = {
    "Forces on Charged Particles": _notes("Forces on charged particles", r"""
$W = QV$ and $E_k = \frac{1}{2}mv^2$ → $v = \sqrt{\frac{2QV}{m}}$. Charge on an electron/proton = $1.60\times10^{-19}$ C.

- 1 volt = 1 joule per coulomb.
- A linear accelerator uses an **alternating** p.d. so the field reverses each time the particle is between drift tubes, always accelerating it.
- A magnetic field changes the **direction** of a moving charged particle (circular path in a cyclotron/synchrotron).
"""),
    "Standard Model": _notes("The Standard Model", r"""
Quark charges: up $+\frac{2}{3}$, down $-\frac{1}{3}$, strange $-\frac{1}{3}$ (antiquarks: opposite sign).

- **Baryons**: three quarks (proton uud, neutron udd). **Mesons**: a quark and an antiquark. Both are hadrons.
- Strong force → gluons. Weak force (beta decay) → W and Z bosons. Electromagnetic → photons.
- Beta (β⁻) decay: $n \to p + e^- + \bar{\nu}_e$ — the antineutrino is evidence of the weak force.
"""),
    "Nuclear Reactions": _notes("Nuclear reactions", r"""
$E = mc^2$ — Δm = mass before − mass after (in kg). Number of reactions per second = power ÷ energy per reaction.

- Fusion needs very high temperatures (plasma) so nuclei overcome their electrostatic repulsion; the plasma is contained with magnetic fields.
"""),
    "Inverse Square Law": _notes("Inverse square law", r"""
$I = \frac{P}{A}$ &nbsp; $I_1d_1^2 = I_2d_2^2$ — irradiance in W m⁻².

- Doubling the distance from a **point source** divides the irradiance by 4.
"""),
    "The Photoelectric Effect": _notes("The photoelectric effect", r"""
$E = hf$ &nbsp; $E_k = hf - hf_0$ &nbsp; $v = f\lambda$ — the work function $hf_0$ is the minimum energy needed to free an electron.

- Below the **threshold frequency** no photoelectrons are emitted, however great the irradiance.
- Increasing the irradiance (above $f_0$) increases the **number** of photoelectrons per second, not their maximum Ek.
"""),
    "Interference": _notes("Interference", r"""
Path difference $= n\lambda$ → maximum (constructive); $= (n + \frac{1}{2})\lambda$ → minimum (destructive).
Grating: $d\sin\theta = n\lambda$, with $d = \frac{1}{\text{lines per metre}}$.

- Coherent sources: constant phase relationship (same frequency).
- The highest order: $n < d/\lambda$ (since $\sin\theta \le 1$).
"""),
    "Spectra": _notes("Spectra", r"""
$E_2 - E_1 = hf$ — a photon is emitted when an electron falls to a lower energy level.

- The bigger the energy gap, the higher the frequency (shorter wavelength).
- **Absorption lines** (dark lines in the Sun's spectrum): gases in the cooler outer layers absorb photons of particular frequencies, exciting electrons.
"""),
    "Refraction of Light": _notes("Refraction of light", r"""
$n = \frac{\sin\theta_1}{\sin\theta_2} = \frac{v_1}{v_2} = \frac{\lambda_1}{\lambda_2}$ &nbsp; $\sin\theta_c = \frac{1}{n}$ — $\theta_1$ in air (vacuum).

- Angles are measured from the **normal**. Frequency doesn't change on refraction.
- Total internal reflection when the angle in the denser material is **greater than** the critical angle.
"""),
}


def _ex(qtype, level):
    return Exam(UNIT, qtype, level, NOTES[qtype])


# ════════════════ Forces on Charged Particles ════════════════

def _fcp_electron(level="Higher"):
    ex = _ex("Forces on Charged Particles", level)
    V = pick(1500, 2000, 2500, 3500, 5000)
    W = E * V
    ex.num(f"Calculate the work done on an electron accelerated through {V} V.", W, "J",
           wrong=[(V / E, "W = QV."), (V, "Multiply by the charge.")],
           working=[r"W = QV", rf"W = 1.60\times10^{{-19}} \times {V} = {ltx(W)}\ \text{{J}}"])
    v = math.sqrt(2 * sig(W) / ME)
    ex.num("Calculate the speed of the electron as it reaches the anode (it starts from rest).", v, "m/s",
           wrong=[(math.sqrt(sig(W) / ME), "Ek = ½mv², so v = √(2Ek/m)."), (2 * sig(W) / ME, "Take the square root."),
                  (math.sqrt(2 * sig(W) / MP), "Use the ELECTRON mass (9.11 × 10⁻³¹ kg).")],
           working=[r"E_k = W = \tfrac{1}{2}mv^2", rf"{ltx(W)} = 0.5 \times 9.11\times10^{{-31}} \times v^2", rf"v = {ltx(v)}\ \text{{m/s}}"])
    ex.choice("The p.d. is doubled. What happens to the speed of the electrons at the anode?",
              "It increases by a factor of √2.",
              [("It doubles.", "Ek doubles, and v ∝ √Ek."), ("It increases by a factor of 4.", "v ∝ √V."), ("It stays the same.", "More work is done on each electron.")])
    return ex.build(f"In an electron gun, electrons are accelerated from rest between a cathode and an anode. "
                    f"(e = 1.60 × 10⁻¹⁹ C, mₑ = 9.11 × 10⁻³¹ kg)")


def _fcp_linac(level="Higher"):
    ex = _ex("Forces on Charged Particles", level)
    V, n = pick(20e3, 25e3, 40e3, 50e3), pick(4, 5, 8, 10)
    W = n * E * V
    ex.num(f"Each gap has a p.d. of {fmt(V)} V and the proton crosses {n} gaps. Calculate the total energy gained.", W, "J",
           wrong=[(E * V, f"It gains energy at EACH of the {n} gaps."), (n * V, "W = QV — multiply by the charge.")],
           working=[rf"W = n \times QV = {n} \times 1.60\times10^{{-19}} \times {ltx(V)} = {ltx(W)}\ \text{{J}}"])
    v = math.sqrt(2 * sig(W) / MP)
    ex.num("Calculate the final speed of the proton (it starts from rest).", v, "m/s",
           wrong=[(math.sqrt(sig(W) / MP), "v = √(2Ek/m)."), (math.sqrt(2 * sig(W) / ME), "Use the PROTON mass.")],
           working=[r"\tfrac{1}{2}mv^2 = W", rf"v = \sqrt{{\frac{{2 \times {ltx(W)}}}{{1.67\times10^{{-27}}}}}} = {ltx(v)}\ \text{{m/s}}"])
    ex.choice("Why is an alternating p.d. used in a linear accelerator?",
              "The field reverses direction while the proton is inside a drift tube, so it is accelerated forward at every gap.",
              [("To make the proton travel in a circle.", "That's done by a magnetic field."),
               ("Because protons can only be accelerated by a.c.", "The point is to reverse the field at the right time."),
               ("To slow the proton down between gaps.", "There's no field inside the drift tubes.")])
    return ex.build("Protons are accelerated in a linear accelerator. (e = 1.60 × 10⁻¹⁹ C, mₚ = 1.67 × 10⁻²⁷ kg)")


gen_charged_particles_exam = exam_style(_fcp_electron, _fcp_linac)


# ════════════════ Standard Model ════════════════

_Q = {"u": 2 / 3, "d": -1 / 3, "s": -1 / 3, "ū": -2 / 3, "d̄": 1 / 3, "s̄": 1 / 3}
_HADRONS = [("sigma-plus", "uus", 1, "baryon"), ("lambda", "uds", 0, "baryon"), ("omega-minus", "sss", -1, "baryon"),
            ("delta-plus-plus", "uuu", 2, "baryon"), ("pion-plus", "ud̄", 1, "meson"), ("kaon-minus", "sū", -1, "meson"),
            ("kaon-zero", "ds̄", 0, "meson"), ("xi-minus", "dss", -1, "baryon")]


def _split(quarks):
    out, i = [], 0
    while i < len(quarks):
        if i + 1 < len(quarks) and quarks[i + 1] == "̄":
            out.append(quarks[i:i + 2])
            i += 2
        else:
            out.append(quarks[i])
            i += 1
    return out


def _sm_hadron(level="Higher"):
    ex = _ex("Standard Model", level)
    name, quarks, q, kind = random.choice(_HADRONS)
    parts = _split(quarks)
    total = sum(_Q[p] for p in parts)
    ex.num(f"The {name} particle has the quark composition {quarks}. Calculate its charge, as a multiple of the charge on a proton "
           f"(e.g. +1, 0, −1).", total, "",
           wrong=[(len(parts), "Add the fractional charges of the quarks."), (-total, "Check the signs: up +⅔, down/strange −⅓, antiquarks opposite.")],
           working=[T(" ".join(f"{'+' if _Q[p] > 0 else '−'} {abs(_Q[p]) * 3:g}/3 ({p})" for p in parts) + f" = {q:+d}".replace("+0", "0"))])
    other = "meson" if kind == "baryon" else "baryon"
    ex.choice(f"Is the {name} a baryon or a meson?", f"A {kind} — it is made of {'three quarks' if kind == 'baryon' else 'a quark and an antiquark'}.",
              [(f"A {other} — it is made of {'three quarks' if other == 'baryon' else 'a quark and an antiquark'}.", "Count the quarks/antiquarks."),
               ("A lepton — it is a fundamental particle.", "It's made of quarks, so it's a hadron."),
               ("A boson — it carries a force.", "It's made of quarks, so it's a hadron.")])
    ex.choice("Which boson is associated with the force that holds quarks together?", "The gluon (strong force).",
              [("The photon (electromagnetic force).", "Quarks are held together by the strong force."),
               ("The W boson (weak force).", "W bosons are involved in beta decay."),
               ("The Higgs boson.", "The Higgs boson is associated with mass.")])
    return ex.build("Hadrons are particles made of quarks. Charges: up +⅔e, down −⅓e, strange −⅓e; antiquarks have the opposite charge.")


def _sm_beta(level="Higher"):
    ex = _ex("Standard Model", level)
    ex.num("A neutron is made of one up quark and two down quarks. Calculate its charge as a multiple of e.", 0, "",
           wrong=[(1, "up +⅔, down −⅓: ⅔ − ⅓ − ⅓ = 0."), (-1 / 3, "Include all three quarks.")],
           working=[T("udd: +⅔ − ⅓ − ⅓ = 0")])
    ex.choice("In beta-minus decay, a neutron changes into a proton. Which other particles are produced?",
              "An electron and an electron antineutrino.",
              [("A positron and an electron neutrino.", "That's β⁺ decay."), ("An alpha particle.", "Alpha decay is a different process."),
               ("A gluon and a photon.", "Beta decay produces an electron and an antineutrino.")])
    ex.choice("Which force is responsible for beta decay, and which boson carries it?", "The weak force — W boson.",
              [("The strong force — gluon.", "The strong force doesn't change quark flavour."),
               ("The electromagnetic force — photon.", "Beta decay is a weak interaction."),
               ("Gravity — graviton.", "Gravity isn't involved.")])
    ex.choice("In beta decay, one quark changes. What is the change?", "A down quark changes into an up quark.",
              [("An up quark changes into a down quark.", "Neutron udd → proton uud: a down becomes an up."),
               ("A down quark changes into a strange quark.", "Neutron udd → proton uud."), ("No quark changes.", "udd → uud.")])
    return ex.build("A free neutron decays by beta-minus decay.")


gen_standard_model_exam = exam_style(_sm_hadron, _sm_beta)


# ════════════════ Nuclear Reactions ════════════════

def _nr_fission(level="Higher"):
    ex = _ex("Nuclear Reactions", level)
    m_before = 3.9218e-25 + random.uniform(-0.0003e-25, 0.0003e-25)
    dm = sig(random.uniform(3.0e-28, 3.3e-28), 3)
    m_after = m_before - dm
    ex.num(f"The total mass before the reaction is {m_before:.5e} kg and after is {m_after:.5e} kg. Calculate the decrease in mass.".replace("e-25", " × 10⁻²⁵"),
           dm, "kg", wrong=[(m_before + m_after, "Subtract: mass before − mass after.")],
           working=[rf"\Delta m = {m_before:.5e} - {m_after:.5e} = {ltx(dm)}\ \text{{kg}}".replace("e-25", r"\times10^{-25}")])
    En = dm * C ** 2
    ex.num("Calculate the energy released in one fission.", En, "J",
           wrong=[(dm * C, "E = mc² — square c."), (m_before * C ** 2, "Use the mass DIFFERENCE.")],
           working=[r"E = mc^2", rf"E = {ltx(dm)} \times (3.00\times10^8)^2 = {ltx(En)}\ \text{{J}}"])
    P = pick(1.2e9, 1.5e9, 2.0e9, 3.0e9)
    N = P / sig(En)
    ex.num(f"The reactor's thermal power output is {fmt(P)} W. Calculate the number of fissions per second.", N, "",
           wrong=[(P * sig(En), "N = P ÷ E per fission.")],
           working=[rf"N = \frac{{P}}{{E}} = \frac{{{ltx(P)}}}{{{ltx(En)}}} = {ltx(N)}\ \text{{per second}}"])
    ex.choice("What is meant by induced fission?", "A heavy nucleus splits after absorbing a neutron.",
              [("A heavy nucleus splits on its own, without any outside cause.", "That's spontaneous fission."),
               ("Two light nuclei join to form a heavier nucleus.", "That's fusion."),
               ("A nucleus emits an alpha particle.", "That's alpha decay.")])
    return ex.build("In a nuclear reactor, uranium-235 nuclei undergo induced fission.")


def _nr_fusion(level="Higher"):
    ex = _ex("Nuclear Reactions", level)
    mD, mT, mHe, mn = 3.3436e-27, 5.0083e-27, 6.6465e-27, 1.6749e-27
    dm = (mD + mT) - (mHe + mn)
    ex.num("Calculate the decrease in mass in one fusion reaction.", dm, "kg",
           wrong=[(mD + mT - mHe, "Include the neutron in the mass after."), ((mD + mT) + (mHe + mn), "Subtract the mass after from the mass before.")],
           working=[rf"m_{{before}} = 3.3436\times10^{{-27}} + 5.0083\times10^{{-27}} = {ltx(mD + mT, 5)}\ \text{{kg}}",
                    rf"m_{{after}} = 6.6465\times10^{{-27}} + 1.6749\times10^{{-27}} = {ltx(mHe + mn, 5)}\ \text{{kg}}",
                    rf"\Delta m = {ltx(dm)}\ \text{{kg}}"])
    En = sig(dm) * C ** 2
    ex.num("Calculate the energy released in one reaction.", En, "J",
           wrong=[(sig(dm) * C, "E = mc² — square c.")], working=[rf"E = mc^2 = {ltx(dm)} \times (3.00\times10^8)^2 = {ltx(En)}\ \text{{J}}"])
    P = pick(5e8, 1e9, 2e9)
    ex.num(f"Calculate the number of reactions per second needed for a power output of {fmt(P)} W.", P / sig(En), "",
           wrong=[(P * sig(En), "N = P ÷ E.")], working=[rf"N = \frac{{{ltx(P)}}}{{{ltx(En)}}} = {ltx(P / sig(En))}"])
    ex.choice("Why must the fuel in a fusion reactor be at an extremely high temperature?",
              "The nuclei must move fast enough to overcome their electrostatic repulsion and get close enough to fuse.",
              [("To melt the fuel so it can flow.", "It's about overcoming the repulsion between nuclei."),
               ("To start a chain reaction of neutrons.", "That's fission."),
               ("Because fusion only happens in a vacuum.", "High temperatures give nuclei enough kinetic energy to fuse.")])
    return ex.build("In a fusion reaction, a deuterium nucleus (3.3436 × 10⁻²⁷ kg) fuses with a tritium nucleus (5.0083 × 10⁻²⁷ kg) to form "
                    "a helium nucleus (6.6465 × 10⁻²⁷ kg) and a neutron (1.6749 × 10⁻²⁷ kg).")


gen_nuclear_exam = exam_style(_nr_fission, _nr_fusion)


# ════════════════ Inverse Square Law ════════════════

def _isl_lamp(level="Higher"):
    ex = _ex("Inverse Square Law", level)
    I1, d1 = pick(4.0, 6.4, 8.0, 12.0), pick(0.20, 0.25, 0.30)
    d2 = pick(0.50, 0.60, 0.75, 0.80)
    I2 = I1 * d1 ** 2 / d2 ** 2
    ex.num(f"The irradiance {d1:g} m from the lamp is {I1:g} W m⁻². Calculate the irradiance {d2:g} m from the lamp.", I2, "W/m²",
           wrong=[(I1 * d1 / d2, "Irradiance ∝ 1/d² — square the distances."), (I1 * d2 ** 2 / d1 ** 2, "Further away → SMALLER irradiance.")],
           working=[r"I_1d_1^2 = I_2d_2^2", rf"{I1:g} \times {d1:g}^2 = I_2 \times {d2:g}^2", rf"I_2 = {ltx(I2)}\ \text{{W m}}^{{-2}}"])
    A_cm2 = pick(2.0, 4.0, 5.0)
    P = sig(I2) * A_cm2 * 1e-4
    ex.num(f"The light sensor has an area of {A_cm2:g} cm². Calculate the power incident on it at {d2:g} m.", P, "W",
           wrong=[(sig(I2) * A_cm2, "Convert cm² to m² (× 10⁻⁴)."), (sig(I2) / (A_cm2 * 1e-4), "P = I × A.")],
           working=[r"I = \frac{P}{A} \Rightarrow P = IA", rf"P = {ltx(I2)} \times {A_cm2:g}\times10^{{-4}} = {ltx(P)}\ \text{{W}}"])
    ex.choice("The experiment is carried out in a darkened room with a small lamp. Why?",
              "So only light from the lamp is measured, and the lamp acts as a point source.",
              [("So the lamp's power increases.", "The room doesn't affect the lamp's power."),
               ("So the sensor heats up less.", "It's about stray light and a point source."),
               ("Because irradiance can only be measured in the dark.", "Stray light would add to the readings.")])
    return ex.build("A pupil investigates how the irradiance of light from a small lamp varies with distance.")


def _isl_sun(level="Higher"):
    ex = _ex("Inverse Square Law", level)
    I_E = 1.36e3
    k = pick(1.5, 1.52, 5.2, 0.72)
    I_p = I_E / k ** 2
    ex.num(f"A planet's distance from the Sun is {k:g} times the Earth's distance from the Sun. Calculate the irradiance of sunlight at the planet.", I_p, "W/m²",
           wrong=[(I_E / k, "Square the distance ratio."), (I_E * k ** 2, "Further away → smaller irradiance.")] if k > 1 else
                 [(I_E / k, "Square the distance ratio."), (I_E * k ** 2, "Closer → LARGER irradiance: I₂ = I₁ × (d₁/d₂)².")],
           working=[r"I_1d_1^2 = I_2d_2^2", rf"I_2 = 1.36\times10^3 \times \left(\frac{{1}}{{{k:g}}}\right)^2 = {ltx(I_p)}\ \text{{W m}}^{{-2}}"])
    A, eff = pick(2.0, 4.0, 6.0), pick(18, 20, 25)
    Pout = sig(I_p) * A * eff / 100
    ex.num(f"A probe there uses solar panels of total area {A:g} m² with an efficiency of {eff}%. Calculate their electrical power output.", Pout, "W",
           wrong=[(sig(I_p) * A, f"Only {eff}% is converted to electrical power."), (sig(I_p) / A * eff / 100, "P = I × A.")],
           working=[rf"P = IA = {ltx(I_p)} \times {A:g} = {ltx(sig(I_p) * A)}\ \text{{W}}", rf"P_{{out}} = {eff / 100:g} \times {ltx(sig(I_p) * A)} = {ltx(Pout)}\ \text{{W}}"])
    return ex.build("The irradiance of sunlight at the Earth is 1.36 × 10³ W m⁻².")


gen_isl_exam = exam_style(_isl_lamp, _isl_sun)


# ════════════════ The Photoelectric Effect ════════════════

def _pe_zinc(level="Higher"):
    ex = _ex("The Photoelectric Effect", level)
    lam_nm = pick(200, 220, 240, 250)
    W0 = pick(5.8e-19, 6.0e-19, 6.9e-19)
    f = C / (lam_nm * 1e-9)
    ex.num(f"Ultraviolet radiation of wavelength {lam_nm} nm is shone on the plate. Calculate its frequency.", f, "Hz",
           wrong=[(C / lam_nm, "Convert nm to m (× 10⁻⁹)."), (C * lam_nm * 1e-9, "f = v ÷ λ.")],
           working=[rf"f = \frac{{v}}{{\lambda}} = \frac{{3.00\times10^8}}{{{lam_nm}\times10^{{-9}}}} = {ltx(f)}\ \text{{Hz}}"])
    Eph = H * sig(f)
    ex.num("Calculate the energy of each photon.", Eph, "J",
           wrong=[(H / sig(f), "E = h × f.")], working=[rf"E = hf = 6.63\times10^{{-34}} \times {ltx(f)} = {ltx(Eph)}\ \text{{J}}"])
    Ek = sig(Eph) - W0
    ex.num(f"The work function of the metal is {fmt(W0)} J. Calculate the maximum kinetic energy of the photoelectrons.", Ek, "J",
           wrong=[(sig(Eph) + W0, "Ek = hf − work function: SUBTRACT."), (sig(Eph), "Subtract the work function.")],
           working=[r"E_k = hf - hf_0", rf"E_k = {ltx(Eph)} - {ltx(W0)} = {ltx(Ek)}\ \text{{J}}"])
    v = math.sqrt(2 * sig(Ek) / ME)
    ex.num("Calculate the maximum speed of the photoelectrons.", v, "m/s",
           wrong=[(math.sqrt(sig(Ek) / ME), "v = √(2Ek/m)."), (2 * sig(Ek) / ME, "Take the square root.")],
           working=[rf"v = \sqrt{{\frac{{2E_k}}{{m}}}} = \sqrt{{\frac{{2 \times {ltx(Ek)}}}{{9.11\times10^{{-31}}}}}} = {ltx(v)}\ \text{{m/s}}"])
    return ex.build("A clean metal plate is illuminated with ultraviolet radiation. (h = 6.63 × 10⁻³⁴ J s, mₑ = 9.11 × 10⁻³¹ kg)")


def _pe_threshold(level="Higher"):
    ex = _ex("The Photoelectric Effect", level)
    W0 = pick(3.6e-19, 4.0e-19, 4.3e-19, 7.2e-19)
    f0 = W0 / H
    ex.num(f"The work function of the metal is {fmt(W0)} J. Calculate the threshold frequency.", f0, "Hz",
           wrong=[(W0 * H, "f₀ = work function ÷ h.")], working=[rf"f_0 = \frac{{hf_0}}{{h}} = \frac{{{ltx(W0)}}}{{6.63\times10^{{-34}}}} = {ltx(f0)}\ \text{{Hz}}"])
    lam0 = C / sig(f0)
    ex.num("Calculate the corresponding (maximum) wavelength that can release photoelectrons.", lam0, "m",
           wrong=[(sig(f0) / C, "λ = v ÷ f.")], working=[rf"\lambda_0 = \frac{{c}}{{f_0}} = {ltx(lam0)}\ \text{{m}}"])
    ex.choice("Very bright light with a frequency below the threshold frequency shines on the metal. What happens?",
              "No photoelectrons are emitted — each photon has too little energy, however many there are.",
              [("Photoelectrons are emitted, but slowly.", "Below f₀ NO electrons are emitted."),
               ("Photoelectrons are emitted because the irradiance is high.", "Irradiance doesn't help below f₀ — it's one photon per electron."),
               ("The metal emits light.", "That's not the photoelectric effect.")])
    ex.choice("Light above the threshold frequency is made brighter (greater irradiance). What changes?",
              "More photoelectrons are emitted per second; their maximum kinetic energy is unchanged.",
              [("The photoelectrons' maximum kinetic energy increases.", "Max Ek depends on frequency, not irradiance."),
               ("Fewer photoelectrons are emitted.", "More photons → more photoelectrons."),
               ("The work function decreases.", "The work function is a property of the metal.")])
    return ex.build("A metal plate is used in a photoelectric experiment. (h = 6.63 × 10⁻³⁴ J s)")


gen_photoelectric_exam = exam_style(_pe_zinc, _pe_threshold)


# ════════════════ Interference ════════════════

def _int_grating(level="Higher"):
    ex = _ex("Interference", level)
    N, lam_nm, n = pick(300, 400, 500, 600), pick(532, 633, 650), pick(1, 2)
    d = 1e-3 / N
    lam = lam_nm * 1e-9
    ex.num(f"The grating has {N} lines per mm. Calculate the spacing between the lines, in m.", d, "m",
           wrong=[(1 / N, "Convert lines per mm to lines per m (× 1000) first."), (N * 1e-3, "d = 1 ÷ (lines per metre).")],
           working=[rf"d = \frac{{1}}{{{N} \times 10^3}} = {ltx(d)}\ \text{{m}}"])
    th = math.degrees(math.asin(n * lam / sig(d)))
    ex.num(f"Laser light of wavelength {lam_nm} nm is used. Calculate the angle to the order-{n} maximum, in degrees.", th, "",
           wrong=([(math.degrees(math.asin(lam / sig(d))), "Use n = 2 for the second-order maximum.")] if n == 2 else [])
                 + [(math.degrees(math.atan(n * lam / sig(d))), "d sin θ = nλ — use sin⁻¹."),
                    (math.degrees(math.asin(n * lam * N)), "d is the line SPACING (1 ÷ lines per metre), not the number of lines.")
                    if n * lam * N <= 1 else (n * lam / sig(d), "Take sin⁻¹ to find the angle.")],
           working=[r"d\sin\theta = n\lambda", rf"\sin\theta = \frac{{{n} \times {lam_nm}\times10^{{-9}}}}{{{ltx(d)}}}", rf"\theta = {th:.3g}^\circ"])
    nmax = int(sig(d) / lam)
    ex.num("Calculate the highest order maximum that can be observed.", nmax, "",
           wrong=[(nmax + 1, "sin θ can't exceed 1: n must be LESS than d/λ — round down.")],
           working=[rf"n < \frac{{d}}{{\lambda}} = \frac{{{ltx(d)}}}{{{lam_nm}\times10^{{-9}}}} = {sig(d) / lam:.3g}", rf"n_{{max}} = {nmax}"])
    return ex.build("Laser light passes through a diffraction grating, producing a pattern of maxima on a screen.")


def _int_microwaves(level="Higher"):
    ex = _ex("Interference", level)
    lam_cm = pick(2.8, 3.0, 3.2)
    n = pick(1, 2, 3)
    is_max = random.random() < 0.5
    pdiff = (n if is_max else n + 0.5) * lam_cm
    d1 = pick(40.0, 45.0, 50.0, 55.0)
    d2 = round(d1 + pdiff, 1)
    ex.num(f"Point P is {d1:g} cm from slit S₁ and {d2:g} cm from slit S₂. Calculate the path difference at P.", d2 - d1, "cm",
           wrong=[(d1 + d2, "Path difference = the DIFFERENCE between the distances.")], working=[rf"\Delta = {d2:g} - {d1:g} = {d2 - d1:.3g}\ \text{{cm}}"])
    ex.choice(f"The wavelength of the microwaves is {lam_cm:g} cm. What is detected at P?",
              f"A {'maximum' if is_max else 'minimum'} — the path difference is {'a whole number' if is_max else 'an odd number of half'} wavelengths.",
              [(f"A {'minimum' if is_max else 'maximum'} — the path difference is {'an odd number of half' if is_max else 'a whole number'} wavelengths.",
                f"Path difference ÷ λ = {pdiff / lam_cm:g}."),
               ("A maximum — every point between two sources is a maximum.", "Maxima and minima alternate.")])
    ex.choice("Why does the pattern need coherent sources (here, one source and two slits)?",
              "Coherent waves have a constant phase relationship, so the positions of the maxima and minima stay fixed.",
              [("Coherent waves have different frequencies.", "Coherent waves have the SAME frequency and constant phase difference."),
               ("So the waves have the same amplitude.", "Coherence is about phase, not amplitude."),
               ("So the waves travel at different speeds.", "All microwaves travel at the same speed.")])
    return ex.build("Microwaves from a single transmitter pass through two slits, S₁ and S₂. A detector is moved along a line in front of the slits.")


gen_interference_exam = exam_style(_int_grating, _int_microwaves)


# ════════════════ Spectra ════════════════

_LEVELS = {1: -21.8e-19, 2: -5.45e-19, 3: -2.42e-19, 4: -1.36e-19}


def _sp_levels(level="Higher"):
    ex = _ex("Spectra", level)
    hi, lo = random.choice([(3, 2), (4, 2), (2, 1), (4, 3)])
    dE = _LEVELS[hi] - _LEVELS[lo]
    ex.num(f"An electron falls from E{hi} to E{lo}. Calculate the energy of the photon emitted.", dE, "J",
           wrong=[(_LEVELS[hi] + _LEVELS[lo], "Subtract the energy levels: E_upper − E_lower."), (abs(_LEVELS[lo]), "Find the DIFFERENCE between the two levels.")],
           working=[rf"\Delta E = E_{hi} - E_{lo} = ({ltx(_LEVELS[hi])}) - ({ltx(_LEVELS[lo])}) = {ltx(dE)}\ \text{{J}}"])
    f = sig(dE) / H
    ex.num("Calculate the frequency of the photon.", f, "Hz",
           wrong=[(sig(dE) * H, "f = E ÷ h.")], working=[rf"f = \frac{{E}}{{h}} = \frac{{{ltx(dE)}}}{{6.63\times10^{{-34}}}} = {ltx(f)}\ \text{{Hz}}"])
    lam = C / sig(f)
    ex.num("Calculate the wavelength of the photon.", lam, "m",
           wrong=[(sig(f) / C, "λ = c ÷ f.")], working=[rf"\lambda = \frac{{c}}{{f}} = {ltx(lam)}\ \text{{m}}"])
    ex.choice("Which transition between these four levels emits the photon with the highest frequency?", "E4 to E1",
              [("E4 to E3", "That's the SMALLEST gap — lowest frequency."), ("E2 to E1", "E4 → E1 has a bigger energy gap."),
               ("E1 to E4", "That's an absorption (electron moving UP).")])
    return ex.build("Some energy levels of a hydrogen atom are: E₁ = −21.8 × 10⁻¹⁹ J, E₂ = −5.45 × 10⁻¹⁹ J, E₃ = −2.42 × 10⁻¹⁹ J, "
                    "E₄ = −1.36 × 10⁻¹⁹ J. (h = 6.63 × 10⁻³⁴ J s)")


def _sp_sun(level="Higher"):
    ex = _ex("Spectra", level)
    lam_nm = pick(589, 656, 486, 527)
    Eph = H * C / (lam_nm * 1e-9)
    ex.num(f"One dark line in the Sun's spectrum has a wavelength of {lam_nm} nm. Calculate the energy of a photon of this wavelength.", Eph, "J",
           wrong=[(H * C / lam_nm, "Convert nm to m."), (H * lam_nm * 1e-9 / C, "E = hf = hc/λ.")],
           working=[r"E = hf = \frac{hc}{\lambda}", rf"E = \frac{{6.63\times10^{{-34}} \times 3.00\times10^8}}{{{lam_nm}\times10^{{-9}}}} = {ltx(Eph)}\ \text{{J}}"])
    ex.choice("Explain how the dark (absorption) lines in the Sun's spectrum are produced.",
              "Atoms in the Sun's cooler outer layers absorb photons of particular frequencies, exciting their electrons to higher energy levels.",
              [("The Sun's core doesn't emit those frequencies.", "The core emits a continuous spectrum; the gas around it absorbs."),
               ("The Earth's atmosphere emits extra light at those frequencies.", "Dark lines are ABSORPTION."),
               ("Electrons fall to lower levels, emitting dark light.", "That would be emission lines (bright).")])
    ex.choice("How can the absorption lines be used to identify elements in the Sun?",
              "Each element has its own pattern of energy levels, so its lines match its laboratory emission spectrum.",
              [("Heavier elements give darker lines.", "Line positions (frequencies) identify the element."),
               ("Each element absorbs all frequencies equally.", "Each element absorbs only specific frequencies."),
               ("The lines show the temperature of each element.", "The pattern of lines identifies the element.")])
    return ex.build("The spectrum of sunlight contains dark lines. (h = 6.63 × 10⁻³⁴ J s)")


gen_spectra_exam = exam_style(_sp_levels, _sp_sun)


# ════════════════ Refraction of Light ════════════════

def _ref_block(level="Higher"):
    ex = _ex("Refraction of Light", level)
    n_true = pick(1.45, 1.50, 1.52, 1.55, 1.60)
    th1 = pick(30, 35, 40, 45, 50, 60)
    th2 = round(math.degrees(math.asin(math.sin(math.radians(th1)) / n_true)), 1)
    n = math.sin(math.radians(th1)) / math.sin(math.radians(th2))
    ex.num(f"A ray enters a glass block at an angle of incidence of {th1}° and is refracted at {th2:g}°. Calculate the refractive index of the glass.",
           n, "", wrong=[(1 / n, "n = sin θ(air) ÷ sin θ(glass)."), (th1 / th2, "Use the SINES of the angles.")],
           working=[r"n = \frac{\sin\theta_1}{\sin\theta_2}", rf"n = \frac{{\sin {th1}^\circ}}{{\sin {th2:g}^\circ}} = {ltx(n)}"])
    v = C / sig(n)
    ex.num("Calculate the speed of light in the glass.", v, "m/s",
           wrong=[(C * sig(n), "Light is SLOWER in glass: v = c ÷ n.")], working=[rf"v = \frac{{c}}{{n}} = \frac{{3.00\times10^8}}{{{ltx(n)}}} = {ltx(v)}\ \text{{m/s}}"])
    thc = math.degrees(math.asin(1 / sig(n)))
    ex.num("Calculate the critical angle for the glass, in degrees.", thc, "",
           wrong=[(th2, "That's the angle of refraction. At the critical angle the angle in AIR is 90°: sin θc = 1/n."),
                  (math.degrees(math.acos(1 / sig(n))), "sin θc = 1/n — use sin⁻¹.")],
           working=[r"\sin\theta_c = \frac{1}{n}", rf"\theta_c = \sin^{{-1}}\left(\frac{{1}}{{{ltx(n)}}}\right) = {thc:.3g}^\circ"])
    ex.choice("Inside the glass, light meets the glass–air boundary at an angle greater than the critical angle. What happens?",
              "Total internal reflection — all the light is reflected back into the glass.",
              [("It refracts out along the boundary.", "That happens AT the critical angle."), ("It refracts out, bending towards the normal.", "Going into air it bends AWAY — and here it doesn't leave at all."),
               ("It passes straight through without bending.", "Beyond θc no light leaves.")])
    return ex.build("A pupil measures the refractive index of a glass block using a ray box.")


def _ref_fibre(level="Higher"):
    ex = _ex("Refraction of Light", level)
    n, lam_nm = pick(1.46, 1.48, 1.50, 1.52), pick(633, 850, 1300)
    ex.num(f"The core has a refractive index of {n:g}. Calculate the critical angle for the core–air boundary, in degrees.",
           math.degrees(math.asin(1 / n)), "",
           wrong=[(math.degrees(math.acos(1 / n)), "sin θc = 1/n.")],
           working=[rf"\theta_c = \sin^{{-1}}\left(\frac{{1}}{{{n:g}}}\right) = {math.degrees(math.asin(1 / n)):.3g}^\circ"])
    lam2 = lam_nm / n
    ex.num(f"Light of wavelength {lam_nm} nm in air enters the core. Calculate its wavelength in the core, in nm.", lam2, "nm",
           wrong=[(lam_nm * n, "The wavelength DECREASES in glass: λ₂ = λ₁ ÷ n."), (lam_nm, "The wavelength changes (the frequency doesn't).")],
           working=[r"n = \frac{\lambda_1}{\lambda_2}", rf"\lambda_2 = \frac{{{lam_nm}}}{{{n:g}}} = {ltx(lam2)}\ \text{{nm}}"])
    ex.choice("What happens to the frequency of the light as it enters the core?", "It stays the same.",
              [("It decreases.", "Frequency is set by the source and doesn't change on refraction."), ("It increases.", "Frequency is unchanged."),
               ("It decreases in proportion to n.", "Speed and wavelength decrease; frequency doesn't.")])
    return ex.build("An optical fibre carries signals using light.")


gen_refraction_exam = exam_style(_ref_block, _ref_fibre)


EXAM = {
    "Forces on Charged Particles": gen_charged_particles_exam,
    "Standard Model":              gen_standard_model_exam,
    "Nuclear Reactions":           gen_nuclear_exam,
    "Inverse Square Law":          gen_isl_exam,
    "The Photoelectric Effect":    gen_photoelectric_exam,
    "Interference":                gen_interference_exam,
    "Spectra":                     gen_spectra_exam,
    "Refraction of Light":         gen_refraction_exam,
}
