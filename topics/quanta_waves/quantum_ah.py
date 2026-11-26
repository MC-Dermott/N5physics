"""AH — Introduction to quantum theory."""
import math
import random

from topics.quanta_waves.common_ah import (
    C, E_CHARGE, H, M_E, M_N, M_P, L, T, calc, explain_set, fmt, ltx, pick_sig, sig, uni,
)

QT = "Introduction to Quantum Theory"

NOTES = r"""
## Introduction to quantum theory

$$E = hf \qquad mvr = \frac{nh}{2\pi} \qquad \lambda = \frac{h}{p} \qquad
\Delta x\,\Delta p_x \geq \frac{h}{4\pi} \qquad \Delta E\,\Delta t \geq \frac{h}{4\pi}$$

- Classical physics cannot explain **black-body radiation curves** (the ultraviolet catastrophe),
  **emission and absorption spectra** or the **photoelectric effect**.
- **Bohr model:** the angular momentum of an electron is quantised. n is the principal quantum number.
  Each allowed orbit is a fixed energy state; a spectral line is a photon emitted or absorbed when an
  electron moves between states.
- Evidence for **particle** behaviour of waves: photoelectric effect, Compton scattering.
  Evidence for **wave** behaviour of particles: electron diffraction.
- **Heisenberg uncertainty principle:** the precise position of a particle and its momentum cannot both
  be known at the same instant. The same applies to its energy change and lifetime.
- **Quantum tunnelling:** a quantum particle can exist in a position that, according to classical
  physics, it has insufficient energy to occupy.
"""


def gen_photon_energy(level="AH"):
    nm = random.randrange(250, 750, 5)
    lam = nm * 1e-9
    f = C / lam
    E = H * f
    kind = random.choice(["E", "f", "lam"])
    if kind == "E":
        return calc(QT, f"Calculate the energy of a photon of light of wavelength {nm} nm.", E, "J",
                    [r"v = f\lambda", rf"3.00 \times 10^8 = f \times {nm} \times 10^{{-9}}",
                     r"E = hf", rf"E = {ltx(E)}\ \mathrm{{J}}"],
                    wrong=[(H * C / nm, "Convert nanometres to metres (× 10⁻⁹)."), (H * lam, "E = hf: find the frequency first.")],
                    scaffold=[("What is the frequency?", f, "Hz"), ("What is the photon energy?", E, "J")], notes=NOTES)
    Eg = sig(E, 3)
    if kind == "f":
        return calc(QT, f"A photon has energy {fmt(Eg)} J. Calculate its frequency.", Eg / H, "Hz",
                    [r"E = hf", rf"{ltx(Eg)} = 6.63 \times 10^{{-34}} \times f", rf"f = {ltx(Eg/H)}\ \mathrm{{Hz}}"],
                    wrong=[(Eg * H, "Rearrange: f = E/h.")], notes=NOTES)
    ans = H * C / Eg
    return calc(QT, f"A photon has energy {fmt(Eg)} J. Calculate its wavelength.", ans, "m",
                [r"E = hf", rf"f = {ltx(Eg/H)}\ \mathrm{{Hz}}", r"v = f\lambda", rf"\lambda = {ltx(ans)}\ \mathrm{{m}}"],
                wrong=[(Eg / H, "That is the frequency. Now use v = fλ.")],
                scaffold=[("What is the frequency?", Eg / H, "Hz"), ("What is the wavelength?", ans, "m")], notes=NOTES)


def gen_bohr(level="AH"):
    n = random.randint(1, 5)
    r = sig(5.29e-11 * n**2, 3)
    mom = n * H / (2 * math.pi)
    v = mom / (M_E * r)
    kind = random.choice(["momentum", "speed", "radius"])
    if kind == "momentum":
        n = random.randint(2, 7)
        mom = n * H / (2 * math.pi)
        return calc(QT, f"Using the Bohr model, calculate the angular momentum of an electron with principal "
                        f"quantum number n = {n}.", mom, "kg m² s⁻¹",
                    [r"mvr = \frac{nh}{2\pi}", rf"mvr = \frac{{{n} \times 6.63 \times 10^{{-34}}}}{{2\pi}} = {ltx(mom)}\ \mathrm{{kg\,m^2\,s^{{-1}}}}"],
                    wrong=[(n * H, "Divide by 2π."), (H / (2 * math.pi), "Include the principal quantum number n.")], notes=NOTES)
    if kind == "speed":
        return calc(QT, f"In the Bohr model, an electron in the n = {n} orbit of hydrogen has an orbit radius of "
                        f"{fmt(r)} m. Calculate its speed.", v, "m s⁻¹",
                    [r"mvr = \frac{nh}{2\pi}",
                     rf"9.11 \times 10^{{-31}} \times v \times {ltx(r)} = \frac{{{n} \times 6.63 \times 10^{{-34}}}}{{2\pi}}",
                     rf"v = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(v * 2 * math.pi, "Divide nh by 2π.")], notes=NOTES)
    vg = sig(v, 3)
    ans = mom / (M_E * vg)
    return calc(QT, f"In the Bohr model, an electron with principal quantum number n = {n} has a speed of "
                    f"{fmt(vg)} m s⁻¹. Calculate the radius of its orbit.", ans, "m",
                [r"mvr = \frac{nh}{2\pi}", rf"r = {ltx(ans)}\ \mathrm{{m}}"],
                wrong=[(ans * 2 * math.pi, "Divide nh by 2π.")], notes=NOTES)


def gen_de_broglie(level="AH"):
    name, m = random.choice([("an electron", M_E), ("a proton", M_P), ("a neutron", M_N)])
    v = sig(uni(1.0, 9.0) * (1e6 if m == M_E else 1e4), 2)
    lam = H / (m * v)
    kind = random.choice(["lam", "speed", "momentum"])
    if kind == "lam":
        return calc(QT, f"Calculate the de Broglie wavelength of {name} travelling at {fmt(v, 2)} m s⁻¹.", lam, "m",
                    [rf"p = mv = {ltx(m*v)}\ \mathrm{{kg\,m\,s^{{-1}}}}", r"\lambda = \frac{h}{p}", rf"\lambda = {ltx(lam)}\ \mathrm{{m}}"],
                    wrong=[(H / v, "p = mv — include the mass."), (m * v / H, "λ = h/p, not p/h.")],
                    scaffold=[("What is the momentum?", m * v, "kg m s⁻¹"), ("What is the wavelength?", lam, "m")], notes=NOTES)
    lg = sig(lam, 3)
    if kind == "speed":
        ans = H / (m * lg)
        return calc(QT, f"The de Broglie wavelength of {name} is {fmt(lg)} m. Calculate its speed.", ans, "m s⁻¹",
                    [r"\lambda = \frac{h}{p}", rf"p = {ltx(H/lg)}\ \mathrm{{kg\,m\,s^{{-1}}}}", r"p = mv",
                     rf"v = {ltx(ans)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(H / lg, "That is the momentum. Divide by the mass.")],
                    scaffold=[("What is the momentum?", H / lg, "kg m s⁻¹"), ("What is the speed?", ans, "m s⁻¹")], notes=NOTES)
    nm = random.randrange(300, 700, 5)
    p = H / (nm * 1e-9)
    return calc(QT, f"Calculate the momentum of a photon of wavelength {nm} nm.", p, "kg m s⁻¹",
                [r"\lambda = \frac{h}{p}", rf"p = {ltx(p)}\ \mathrm{{kg\,m\,s^{{-1}}}}"],
                wrong=[(H / nm, "Convert nanometres to metres."), (H * nm * 1e-9, "Rearrange: p = h/λ.")], notes=NOTES)


def gen_uncertainty(level="AH"):
    kind = random.choice(["dp", "dv", "dE", "dt"])
    if kind in ("dp", "dv"):
        dx = sig(uni(1.0, 9.0) * 1e-11, 2)
        dp = H / (4 * math.pi * dx)
        if kind == "dp":
            return calc(QT, f"The uncertainty in the position of an electron is {fmt(dx, 2)} m. Calculate the minimum "
                            f"uncertainty in its momentum.", dp, "kg m s⁻¹",
                        [r"\Delta x\,\Delta p_x \geq \frac{h}{4\pi}",
                         rf"\Delta p_{{x\,min}} = \frac{{6.63 \times 10^{{-34}}}}{{4\pi \times {ltx(dx, 2)}}} = {ltx(dp)}\ \mathrm{{kg\,m\,s^{{-1}}}}"],
                        wrong=[(H / dx, "Divide by 4π as well."), (H / (4 * math.pi) * dx, "Divide by Δx.")], notes=NOTES)
        dv = dp / M_E
        return calc(QT, f"The uncertainty in the position of an electron is {fmt(dx, 2)} m. Calculate the minimum "
                        f"uncertainty in its velocity.", dv, "m s⁻¹",
                    [r"\Delta x\,\Delta p_x \geq \frac{h}{4\pi}",
                     rf"\Delta p_{{x\,min}} = {ltx(dp)}\ \mathrm{{kg\,m\,s^{{-1}}}}",
                     rf"\Delta v_{{min}} = \frac{{\Delta p}}{{m}} = {ltx(dv)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(dp, "That is the uncertainty in momentum. Divide by the electron mass.")],
                    scaffold=[("What is the minimum uncertainty in momentum?", dp, "kg m s⁻¹"),
                              ("What is the minimum uncertainty in velocity?", dv, "m s⁻¹")], notes=NOTES)
    if kind == "dE":
        t = sig(uni(1.0, 9.0) * 10.0 ** random.choice([-8, -9, -23]), 2)
        dE = H / (4 * math.pi * t)
        return calc(QT, f"A particle has a lifetime of {fmt(t, 2)} s. Calculate the minimum uncertainty in its energy.",
                    dE, "J",
                    [T("The lifetime is taken as the uncertainty in time."), r"\Delta E\,\Delta t \geq \frac{h}{4\pi}",
                     rf"\Delta E_{{min}} = {ltx(dE)}\ \mathrm{{J}}"],
                    wrong=[(H / t, "Divide by 4π as well.")], notes=NOTES)
    dE = sig(uni(1.0, 9.0) * 10.0 ** random.choice([-26, -27, -11]), 2)
    t = H / (4 * math.pi * dE)
    return calc(QT, f"The minimum uncertainty in the energy of an excited state is {fmt(dE, 2)} J. Calculate the "
                    f"lifetime of the state.", t, "s",
                [r"\Delta E\,\Delta t \geq \frac{h}{4\pi}", rf"\Delta t = {ltx(t)}\ \mathrm{{s}}"],
                wrong=[(H / dE, "Divide by 4π as well.")], notes=NOTES)


_EXPLAIN = [
    ("Which observation led to the 'ultraviolet catastrophe' of classical physics?",
     "The black-body radiation curve: classical physics predicts ever-increasing intensity at short wavelengths, which is not observed.",
     [("The photoelectric effect: ultraviolet light destroys the metal.", "The catastrophe is about black-body radiation."),
      ("Line spectra: only ultraviolet lines are ever emitted.", "Spectra are a different failure of classical physics."),
      ("Black-body curves: classical physics predicts no ultraviolet radiation at all.", "It predicts far too much.")],
     "Compare the classical prediction with the measured curve."),
    ("Which is experimental evidence for the particle-like behaviour of light?",
     "Light above a threshold frequency ejects electrons from a metal surface (the photoelectric effect).",
     [("Light produces fringes after passing through two slits.", "That is wave behaviour."),
      ("Light can be plane polarised.", "That is wave behaviour."),
      ("Electrons produce a ring pattern after passing through graphite.", "That is wave behaviour of particles.")],
     "Compton scattering is another example. Describe the evidence, not just the name."),
    ("Which is experimental evidence for the wave-like behaviour of particles?",
     "A beam of electrons passing through a crystal produces a diffraction pattern.",
     [("Electrons are deflected by an electric field.", "A charged particle would be deflected."),
      ("Photons scattered from electrons change wavelength.", "That is particle behaviour of waves."),
      ("Light ejects electrons from a metal surface.", "That is particle behaviour of light.")],
     "Diffraction and interference are wave properties."),
    ("What does the Heisenberg uncertainty principle say about a quantum particle?",
     "Its precise position and its momentum cannot both be known at the same instant.",
     [("Its position and momentum can never be measured accurately with present equipment.",
       "It is a fundamental limit, not a limit of equipment, and it concerns precision."),
      ("Either its position or its momentum can be measured, but never the other.", "Both can be known, but not both precisely."),
      ("Its mass and charge cannot be known at the same instant.", "The pairs are position-momentum and energy-time.")],
     "'At the same instant' is required."),
    ("What is meant by quantum tunnelling?",
     "A quantum particle can exist in a position that, according to classical physics, it has insufficient energy to occupy.",
     [("A particle gains enough energy to climb over a potential barrier.", "It does not gain the energy to go over the barrier."),
      ("A particle drills a hole through a barrier.", "The barrier is not damaged."),
      ("A particle travels through a barrier faster than light.", "Nothing in this involves exceeding c.")],
     "Compare with the classical prediction."),
    ("An alpha particle can escape from a nucleus even though, classically, it does not have enough energy. How does "
     "the uncertainty principle allow this?",
     "Its position is not known precisely, so there is a probability that it exists outside the nucleus.",
     [("The uncertainty in its mass lets it become light enough to escape.", "The principle is not about mass here."),
      ("It collides with other particles until it has enough energy.", "That is a classical explanation."),
      ("The strong force switches off at random.", "The forces do not switch off.")],
     "An energy-time argument is also valid: for a short enough time the energy is very uncertain."),
    ("How does the Bohr model explain the line emission spectrum of an element?",
     "Electrons have discrete energy states; a photon of one specific frequency is emitted when an electron drops between two of them.",
     [("Electrons can have any energy, but only some colours escape the atom.", "The energy states are discrete."),
      ("Electrons emit light continuously as they orbit.", "In allowed orbits electrons do not radiate."),
      ("Each line is produced by a different electron mass.", "All electrons are identical.")],
     "Quantised angular momentum → discrete energy states → E = hf for each transition."),
    ("In the wave model of the Bohr atom, why are only some orbit radii allowed?",
     "The orbit circumference must equal a whole number (a positive integer) of de Broglie wavelengths.",
     [("The circumference must be a multiple of the de Broglie wavelength.", "Incomplete: the multiple must be a positive integer."),
      ("The radius must equal one de Broglie wavelength.", "It is the circumference, and any positive integer number."),
      ("Only some radii give the electron zero momentum.", "The electron has momentum in every orbit.")],
     "2πr = nλ, which leads to mvr = nh/2π."),
]
gen_quantum_explain = explain_set(QT, _EXPLAIN, NOTES)
