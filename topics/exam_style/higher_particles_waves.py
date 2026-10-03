"""Higher Particles and Waves — exam-style questions that cut across the unit's topics, like SQA paper questions.

Recognised wrong answers follow the Higher marking instructions and course reports: ½ or the square
root dropped from Ek = ½mv², the proton mass used for an electron, nm/mm not converted, the
irradiance ratio not squared or inverted, the work function added instead of subtracted, d taken as
the number of lines per mm, sin used for n the wrong way up, and the critical angle confused with the
angle of refraction.
"""
import math
import random

from topics.exam_style.base import Exam, T, fmt, ltx, pick, sig

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


def _ex(level):
    return Exam(UNIT, level, NOTES)


# ════════════════ Fusion reactor: accelerated ions → Δm → E → reactions per second → quarks ════════════════

def fusion_reactor(level="Higher"):
    ex = _ex(level)
    mD, mT, mHe, mn = 3.3436e-27, 5.0083e-27, 6.6465e-27, 1.6749e-27
    V = pick(20e3, 40e3, 50e3, 80e3)
    W = E * V
    ex.on("Forces on Charged Particles").num(f"Deuterium ions (charge 1.60 × 10⁻¹⁹ C) are accelerated through {fmt(V)} V to heat the plasma. "
        f"Calculate the energy gained by each ion.", W, "J",
        wrong=[(V / E, "W = QV."), (V, "Multiply by the charge.")], working=[rf"W = QV = 1.60\times10^{{-19}} \times {ltx(V)} = {ltx(W)}\ \text{{J}}"])
    v = math.sqrt(2 * sig(W) / mD)
    ex.on("Forces on Charged Particles").num("Calculate the speed of a deuterium ion after acceleration (it starts from rest).", v, "m/s",
        wrong=[(math.sqrt(sig(W) / mD), "v = √(2W/m)."), (math.sqrt(2 * sig(W) / ME), "Use the mass of the deuterium nucleus.")],
        working=[rf"v = \sqrt{{\frac{{2W}}{{m}}}} = \sqrt{{\frac{{2 \times {ltx(W)}}}{{3.3436\times10^{{-27}}}}}} = {ltx(v)}\ \text{{m/s}}"])
    dm = (mD + mT) - (mHe + mn)
    ex.on("Nuclear Reactions").num("Calculate the decrease in mass in one fusion reaction.", dm, "kg",
        wrong=[(mD + mT - mHe, "Include the neutron in the mass after.")],
        working=[rf"\Delta m = (3.3436 + 5.0083)\times10^{{-27}} - (6.6465 + 1.6749)\times10^{{-27}} = {ltx(dm)}\ \text{{kg}}"])
    En = sig(dm) * C ** 2
    ex.on("Nuclear Reactions").num("Calculate the energy released in one reaction.", En, "J",
        wrong=[(sig(dm) * C, "E = mc² — square c.")], working=[rf"E = mc^2 = {ltx(dm)} \times (3.00\times10^8)^2 = {ltx(En)}\ \text{{J}}"])
    P = pick(5e8, 1e9, 2e9)
    ex.on("Nuclear Reactions").num(f"Calculate the number of reactions per second for a power output of {fmt(P)} W.", P / sig(En), "",
        wrong=[(P * sig(En), "N = P ÷ E.")], working=[rf"N = \frac{{P}}{{E}} = {ltx(P / sig(En))}"])
    ex.on("Standard Model").choice("A neutron (udd) is produced in each reaction. Which force holds its quarks together, and what is its exchange particle?",
        "The strong force — gluons.", [("The weak force — W bosons.", "The weak force causes beta decay."),
                                       ("The electromagnetic force — photons.", "The strong force binds quarks."),
                                       ("Gravity — gravitons.", "Gravity is far too weak.")])
    return ex.build("In a fusion reactor, deuterium (3.3436 × 10⁻²⁷ kg) and tritium (5.0083 × 10⁻²⁷ kg) fuse to form helium "
                    "(6.6465 × 10⁻²⁷ kg) and a neutron (1.6749 × 10⁻²⁷ kg).")


# ════════════════ Photocell: inverse square → photons → photoelectrons ════════════════

def photocell(level="Higher"):
    ex = _ex(level)
    I1, d1, d2 = pick(8.0, 12.0, 16.0), pick(0.20, 0.25), pick(0.40, 0.50, 0.60)
    I2 = I1 * d1 ** 2 / d2 ** 2
    ex.on("Inverse Square Law").num(f"The irradiance {d1:g} m from a UV lamp is {I1:g} W m⁻². Calculate the irradiance at {d2:g} m.", I2, "W/m²",
        wrong=[(I1 * d1 / d2, "Square the distances."), (I1 * d2 ** 2 / d1 ** 2, "Further away → smaller irradiance.")],
        working=[r"I_1d_1^2 = I_2d_2^2", rf"I_2 = \frac{{{I1:g} \times {d1:g}^2}}{{{d2:g}^2}} = {ltx(I2)}\ \text{{W m}}^{{-2}}"])
    A_cm2 = pick(2.0, 4.0, 5.0)
    P = sig(I2) * A_cm2 * 1e-4
    ex.on("Inverse Square Law").num(f"The photocell has an area of {A_cm2:g} cm². Calculate the power incident on it.", P, "W",
        wrong=[(sig(I2) * A_cm2, "Convert cm² to m² (× 10⁻⁴).")], working=[rf"P = IA = {ltx(I2)} \times {A_cm2:g}\times10^{{-4}} = {ltx(P)}\ \text{{W}}"])
    lam = pick(220, 250, 280)
    Eph = H * C / (lam * 1e-9)
    ex.on("The Photoelectric Effect").num(f"The UV has a wavelength of {lam} nm. Calculate the energy of each photon.", Eph, "J",
        wrong=[(H * C / lam, "Convert nm to m."), (H * lam * 1e-9 / C, "E = hc/λ.")],
        working=[rf"E = \frac{{hc}}{{\lambda}} = \frac{{6.63\times10^{{-34}} \times 3.00\times10^8}}{{{lam}\times10^{{-9}}}} = {ltx(Eph)}\ \text{{J}}"])
    ex.on("The Photoelectric Effect").num("Calculate the number of photons hitting the photocell each second.", sig(P) / sig(Eph), "",
        wrong=[(sig(P) * sig(Eph), "N = P ÷ E per photon.")], working=[rf"N = \frac{{P}}{{E}} = \frac{{{ltx(P)}}}{{{ltx(Eph)}}} = {ltx(sig(P) / sig(Eph))}"])
    W0 = pick(4.3e-19, 5.8e-19, 6.0e-19)
    Ek = sig(Eph) - W0
    ex.on("The Photoelectric Effect").num(f"The metal's work function is {fmt(W0)} J. Calculate the maximum kinetic energy of a photoelectron.", Ek, "J",
        wrong=[(sig(Eph) + W0, "Ek = hf − work function: subtract.")], working=[rf"E_k = {ltx(Eph)} - {ltx(W0)} = {ltx(Ek)}\ \text{{J}}"])
    ex.on("The Photoelectric Effect").choice("The lamp is moved closer to the photocell. What changes?",
        "More photoelectrons are emitted per second; their maximum kinetic energy is unchanged.",
        [("The maximum kinetic energy increases.", "Ek depends on frequency, not irradiance."),
         ("Fewer photoelectrons are emitted.", "Greater irradiance → more photons → more photoelectrons."),
         ("The work function decreases.", "The work function is a property of the metal.")])
    return ex.build("A UV lamp shines on a photocell. (h = 6.63 × 10⁻³⁴ J s)")


# ════════════════ Hydrogen lamp: energy levels → wavelength → diffraction grating ════════════════

_LEVELS = {1: -21.8e-19, 2: -5.45e-19, 3: -2.42e-19, 4: -1.36e-19}


def hydrogen_lamp(level="Higher"):
    ex = _ex(level)
    hi = pick(3, 4)
    dE = _LEVELS[hi] - _LEVELS[2]
    ex.on("Spectra").num(f"An electron falls from E{hi} to E2. Calculate the energy of the photon emitted.", dE, "J",
        wrong=[(_LEVELS[hi] + _LEVELS[2], "Subtract the levels: E_upper − E_lower."), (abs(_LEVELS[2]), "Find the DIFFERENCE.")],
        working=[rf"\Delta E = ({ltx(_LEVELS[hi])}) - ({ltx(_LEVELS[2])}) = {ltx(dE)}\ \text{{J}}"])
    lam = H * C / sig(dE)
    ex.on("Spectra").num("Calculate the wavelength of this light.", lam, "m",
        wrong=[(sig(dE) / H, "That's the frequency; λ = c/f = hc/E."), (H * sig(dE) / C, "λ = hc/E.")],
        working=[rf"\lambda = \frac{{hc}}{{E}} = {ltx(lam)}\ \text{{m}}"])
    N = pick(300, 400, 500, 600)
    d = 1e-3 / N
    th = math.degrees(math.asin(sig(lam) / d))
    ex.on("Interference").num(f"The light passes through a grating with {N} lines per mm. Calculate the angle to the first-order maximum, in degrees.", th, "",
        wrong=[(math.degrees(math.atan(sig(lam) / d)), "d sin θ = nλ — use sin⁻¹."), (math.degrees(math.asin(min(1, 2 * sig(lam) / d))), "First order: n = 1.")],
        working=[rf"d = \frac{{1}}{{{N}\times10^3}} = {ltx(d)}\ \text{{m}}", rf"\sin\theta = \frac{{{ltx(lam)}}}{{{ltx(d)}}}", rf"\theta = {th:.3g}^\circ"])
    ex.on("Spectra").choice("Dark lines at the same wavelengths appear in the Sun's spectrum. Why?",
        "Hydrogen in the Sun's cooler outer layers absorbs photons of exactly these energies, exciting electrons to higher levels.",
        [("The Sun's core doesn't emit these wavelengths.", "The core emits a continuous spectrum; the outer gas absorbs."),
         ("Earth's atmosphere emits extra light at these wavelengths.", "Dark lines are absorption."),
         ("Electrons fall to lower levels, giving dark light.", "That would be bright emission lines.")])
    return ex.build("A hydrogen discharge lamp is viewed through a spectrometer. Energy levels: E₁ = −21.8 × 10⁻¹⁹ J, E₂ = −5.45 × 10⁻¹⁹ J, "
                    "E₃ = −2.42 × 10⁻¹⁹ J, E₄ = −1.36 × 10⁻¹⁹ J. (h = 6.63 × 10⁻³⁴ J s)")


# ════════════════ Laser and optical fibre: grating → photon energy → refraction ════════════════

def laser_fibre(level="Higher"):
    ex = _ex(level)
    lam_nm, N = pick(532, 633, 650), pick(300, 500, 600)
    d = 1e-3 / N
    th = math.degrees(math.asin(2 * lam_nm * 1e-9 / d))
    ex.on("Interference").num(f"The laser light is shone through a grating with {N} lines per mm. Calculate the angle to the second-order maximum, in degrees.",
        th, "", wrong=[(math.degrees(math.asin(lam_nm * 1e-9 / d)), "Second order: n = 2."), (math.degrees(math.atan(2 * lam_nm * 1e-9 / d)), "Use sin⁻¹.")],
        working=[rf"d\sin\theta = n\lambda", rf"\sin\theta = \frac{{2 \times {lam_nm}\times10^{{-9}}}}{{{ltx(d)}}}", rf"\theta = {th:.3g}^\circ"])
    ex.on("Spectra").num("Calculate the energy of one photon of the laser light.", H * C / (lam_nm * 1e-9), "J",
        wrong=[(H * C / lam_nm, "Convert nm to m.")], working=[rf"E = \frac{{hc}}{{\lambda}} = {ltx(H * C / (lam_nm * 1e-9))}\ \text{{J}}"])
    n = pick(1.46, 1.48, 1.50, 1.52)
    ex.on("Refraction of Light").num(f"The light enters an optical fibre with a refractive index of {n:g}. Calculate its speed in the fibre.", C / n, "m/s",
        wrong=[(C * n, "Light is slower in glass: v = c ÷ n.")], working=[rf"v = \frac{{c}}{{n}} = \frac{{3.00\times10^8}}{{{n:g}}} = {ltx(C / n)}\ \text{{m/s}}"])
    ex.on("Refraction of Light").num("Calculate the wavelength of the light in the fibre, in nm.", lam_nm / n, "nm",
        wrong=[(lam_nm * n, "λ decreases in glass: λ₂ = λ₁ ÷ n."), (lam_nm, "The wavelength changes; the frequency doesn't.")],
        working=[rf"\lambda_2 = \frac{{{lam_nm}}}{{{n:g}}} = {ltx(lam_nm / n)}\ \text{{nm}}"])
    thc = math.degrees(math.asin(1 / n))
    ex.on("Refraction of Light").num("Calculate the critical angle for the fibre–air boundary, in degrees.", thc, "",
        wrong=[(math.degrees(math.acos(1 / n)), "sin θc = 1/n.")], working=[rf"\theta_c = \sin^{{-1}}\left(\frac{{1}}{{{n:g}}}\right) = {thc:.3g}^\circ"])
    ex.on("Refraction of Light").choice("Why does the light stay inside the fibre?",
        "It meets the boundary at more than the critical angle, so it is totally internally reflected.",
        [("It meets the boundary at less than the critical angle.", "Below θc light refracts out."), ("The fibre absorbs light that reaches the edge.", "It's total internal reflection."),
         ("Light can't travel from glass into air.", "It can, below the critical angle.")])
    return ex.build(f"A laser emits light of wavelength {lam_nm} nm. (h = 6.63 × 10⁻³⁴ J s)")


# ════════════════ Particle accelerator: accelerating protons → hadrons → mass-energy ════════════════

def particle_accelerator(level="Higher"):
    ex = _ex(level)
    V, n = pick(25e3, 40e3, 50e3), pick(5, 8, 10)
    W = n * E * V
    ex.on("Forces on Charged Particles").num(f"A proton crosses {n} gaps, each with a p.d. of {fmt(V)} V. Calculate the total energy it gains.", W, "J",
        wrong=[(E * V, f"It gains energy at each of the {n} gaps."), (n * V, "W = QV — multiply by the charge.")],
        working=[rf"W = n \times QV = {n} \times 1.60\times10^{{-19}} \times {ltx(V)} = {ltx(W)}\ \text{{J}}"])
    v = math.sqrt(2 * sig(W) / MP)
    ex.on("Forces on Charged Particles").num("Calculate the speed of the proton (starting from rest).", v, "m/s",
        wrong=[(math.sqrt(sig(W) / MP), "v = √(2W/m)."), (math.sqrt(2 * sig(W) / ME), "Use the PROTON mass.")],
        working=[rf"v = \sqrt{{\frac{{2 \times {ltx(W)}}}{{1.67\times10^{{-27}}}}}} = {ltx(v)}\ \text{{m/s}}"])
    ex.on("Forces on Charged Particles").choice("In a circular accelerator, what is the magnetic field used for?",
        "To change the direction of the protons so they follow a circular path.",
        [("To increase the protons' speed.", "The electric field accelerates; the magnetic field steers."),
         ("To slow the protons down between collisions.", "It steers them."), ("To give the protons their charge.", "Protons are already charged.")])
    name, quarks, q = random.choice([("π⁺", "u d̄", "+1"), ("K⁻", "s ū", "−1"), ("Σ⁺", "u u s", "+1"), ("Λ⁰", "u d s", "0")])
    kind = "meson" if len(quarks.split()) == 2 else "baryon"
    ex.on("Standard Model").choice(f"Collisions produce a {name} particle with quark composition {quarks}. What is its charge, and what type of hadron is it?",
        f"{q}, a {kind}", [(f"{q}, a {'baryon' if kind == 'meson' else 'meson'}", "Baryons have three quarks; mesons a quark and an antiquark."),
                           (f"{'0' if q != '0' else '+1'}, a {kind}", "Add the quark charges: u +⅔, d and s −⅓, antiquarks opposite."),
                           ("−2, a lepton", "It's made of quarks, so it's a hadron.")])
    m_pi = 2.49e-28
    ex.on("Nuclear Reactions").num("A π⁺ has a mass of 2.49 × 10⁻²⁸ kg. Calculate the energy equivalent of this mass.", m_pi * C ** 2, "J",
        wrong=[(m_pi * C, "E = mc² — square c.")], working=[rf"E = mc^2 = 2.49\times10^{{-28}} \times (3.00\times10^8)^2 = {ltx(m_pi * C ** 2)}\ \text{{J}}"])
    return ex.build("Protons are accelerated in a particle accelerator. (e = 1.60 × 10⁻¹⁹ C, mₚ = 1.67 × 10⁻²⁷ kg)")


# ════════════════ The Sun: mass–energy → irradiance → spectrum ════════════════

def the_sun(level="Higher"):
    ex = _ex(level)
    P = 3.8e26
    ex.on("Nuclear Reactions").num("The Sun's power output is 3.8 × 10²⁶ W. Calculate the mass converted to energy each second.", P / C ** 2, "kg",
        wrong=[(P / C, "m = E ÷ c² — square c."), (P * C ** 2, "m = E ÷ c².")],
        working=[rf"m = \frac{{E}}{{c^2}} = \frac{{3.8\times10^{{26}}}}{{(3.00\times10^8)^2}} = {ltx(P / C ** 2)}\ \text{{kg}}"])
    d = pick(1.08e11, 1.50e11, 2.28e11)
    A = 4 * math.pi * d ** 2
    I = P / A
    ex.on("Inverse Square Law").num(f"Calculate the irradiance of sunlight at a distance of {fmt(d)} m from the Sun (area of a sphere = 4πr²).", I, "W/m²",
        wrong=[(P / (4 * math.pi * d), "Square r: A = 4πr²."), (P / d ** 2, "Divide by the sphere's AREA, 4πr².")],
        working=[rf"I = \frac{{P}}{{A}} = \frac{{3.8\times10^{{26}}}}{{4\pi({ltx(d)})^2}} = {ltx(I)}\ \text{{W m}}^{{-2}}"])
    ex.on("Inverse Square Law").num("Calculate the irradiance at twice this distance.", I / 4, "W/m²",
        wrong=[(I / 2, "Irradiance ∝ 1/d²: doubling d divides I by 4.")], working=[rf"I = \frac{{{ltx(I)}}}{{2^2}} = {ltx(I / 4)}\ \text{{W m}}^{{-2}}"])
    lam = pick(589, 656, 486)
    ex.on("Spectra").num(f"One absorption line in the Sun's spectrum is at {lam} nm. Calculate the energy of a photon at this wavelength.", H * C / (lam * 1e-9), "J",
        wrong=[(H * C / lam, "Convert nm to m.")], working=[rf"E = \frac{{hc}}{{\lambda}} = {ltx(H * C / (lam * 1e-9))}\ \text{{J}}"])
    ex.on("Spectra").choice("How are absorption lines used to identify the elements in the Sun?",
        "Each element absorbs only particular frequencies set by its energy levels, matching its lab emission spectrum.",
        [("Heavier elements give darker lines.", "It's the positions of the lines that identify the element."),
         ("Every element absorbs all frequencies.", "Each absorbs only specific frequencies."),
         ("The lines show each element's temperature.", "The pattern identifies the element.")])
    return ex.build("The Sun is powered by nuclear fusion. (h = 6.63 × 10⁻³⁴ J s)")


SCENARIOS = {
    "Fusion Reactor":       fusion_reactor,
    "Photocell":            photocell,
    "Hydrogen Lamp":        hydrogen_lamp,
    "Laser and Optical Fibre": laser_fibre,
    "Particle Accelerator": particle_accelerator,
    "The Sun":              the_sun,
}
