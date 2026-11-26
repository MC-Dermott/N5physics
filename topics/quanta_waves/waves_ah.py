"""AH — Waves: travelling waves, phase, energy and stationary waves."""
import math
import random

from topics.quanta_waves.common_ah import L, T, V_SOUND, calc, explain_set, fmt, ltx, pick_sig, sig, uni

QT = "Waves"

NOTES = r"""
## Waves

$$y = A\sin 2\pi\left(ft - \frac{x}{\lambda}\right) \qquad \phi = \frac{2\pi x}{\lambda} \qquad
E = kA^2 \quad \text{or} \quad \frac{E_1}{A_1^2} = \frac{E_2}{A_2^2} \qquad v = f\lambda$$

- Compare a given equation term by term: the number multiplying t inside 2π( ) is f; the number
  multiplying x is 1/λ. Multiply out first if the 2π has been taken inside.
- A wave moving in the **negative** x direction has a **+** sign between the t and x terms.
- Phase angle is in radians (unit **rad**).
- **Stationary waves** are formed by the interference of two waves of the same frequency and amplitude
  travelling in opposite directions. Nodes: always zero displacement. Antinodes: maximum amplitude.
  Node to next node = λ/2.
"""


def gen_travelling_wave(level="AH"):
    A = uni(0.020, 0.300, 3)
    f = uni(2.0, 25.0)
    lam = uni(0.20, 2.50, 2)
    k = sig(1 / lam, 3)
    lam = 1 / k
    A_txt = f"{A:g}"
    if random.random() < 0.5:
        eq = f"y = {A_txt} sin 2π({f:g}t − {k:g}x)"
        take = [r"y = A\sin 2\pi\left(ft - \frac{x}{\lambda}\right)", rf"f = {f:g}\ \mathrm{{Hz}} \qquad \frac{{1}}{{\lambda}} = {k:g}"]
    else:
        a, b = sig(2 * math.pi * f, 3), sig(2 * math.pi * k, 3)
        f, lam = a / (2 * math.pi), 2 * math.pi / b
        eq = f"y = {A_txt} sin({a:g}t − {b:g}x)"
        take = [r"y = A\sin 2\pi\left(ft - \frac{x}{\lambda}\right)", rf"2\pi f = {a:g} \qquad \frac{{2\pi}}{{\lambda}} = {b:g}"]
    stem = f"A travelling wave is described by **{eq}**, where all quantities are in SI units. "
    kind = random.choice(["f", "lam", "v"])
    if kind == "f":
        return calc(QT, stem + "Determine the frequency of the wave.", f, "Hz", take + [rf"f = {ltx(f)}\ \mathrm{{Hz}}"],
                    wrong=[(f * 2 * math.pi, "Compare with y = A sin 2π(ft − x/λ): take the 2π out."),
                           (f / (2 * math.pi), "Check whether the 2π is already outside the bracket.")], notes=NOTES)
    if kind == "lam":
        return calc(QT, stem + "Determine the wavelength of the wave.", lam, "m", take + [rf"\lambda = {ltx(lam)}\ \mathrm{{m}}"],
                    wrong=[(1 / lam, "The number multiplying x is 1/λ."), (lam / (2 * math.pi), "Check where the 2π is.")], notes=NOTES)
    return calc(QT, stem + "Calculate the speed of the wave.", f * lam, "m s⁻¹",
                take + [rf"f = {ltx(f)}\ \mathrm{{Hz}} \qquad \lambda = {ltx(lam)}\ \mathrm{{m}}", r"v = f\lambda",
                        rf"v = {ltx(f*lam)}\ \mathrm{{m\,s^{{-1}}}}"],
                wrong=[(f / lam, "v = fλ. The number multiplying x is 1/λ, not λ.")],
                scaffold=[("What is f?", f, "Hz"), ("What is λ?", lam, "m"), ("What is v?", f * lam, "m s⁻¹")], notes=NOTES)


def gen_phase(level="AH"):
    f = random.randrange(150, 1200, 10)
    lam = V_SOUND / f
    x = sig(lam * uni(0.12, 0.90, 2), 2)
    phi = 2 * math.pi * x / lam
    if random.random() < 0.6:
        return calc(QT, f"A sound wave of frequency {f} Hz travels at 340 m s⁻¹. Calculate the phase difference between "
                        f"two points {x:g} m apart along the direction of travel.", phi, "rad",
                    [r"v = f\lambda", rf"\lambda = {ltx(lam)}\ \mathrm{{m}}", r"\phi = \frac{2\pi x}{\lambda}",
                     rf"\phi = {ltx(phi)}\ \mathrm{{rad}}"],
                    wrong=[(360 * x / lam, "That is in degrees. φ = 2πx/λ gives radians."), (x / lam, "Multiply by 2π.")],
                    scaffold=[("What is the wavelength?", lam, "m"), ("What is the phase difference?", phi, "rad")], notes=NOTES)
    lam = uni(0.30, 2.0, 2)
    ph = uni(0.60, 5.5)
    ans = ph * lam / (2 * math.pi)
    return calc(QT, f"Two points on a wave of wavelength {lam:g} m have a phase difference of {ph:g} rad. Calculate the "
                    f"smallest distance between them.", ans, "m",
                [r"\phi = \frac{2\pi x}{\lambda}", rf"{ph:g} = \frac{{2\pi x}}{{{lam:g}}}", rf"x = {ltx(ans)}\ \mathrm{{m}}"],
                wrong=[(ph * lam, "Divide by 2π.")], notes=NOTES)


def gen_wave_energy(level="AH"):
    A1, E1 = uni(0.020, 0.090, 3), uni(2.0, 20.0)
    if random.random() < 0.5:
        A2 = sig(A1 * uni(1.4, 3.5), 2)
        E2 = E1 * (A2 / A1) ** 2
        return calc(QT, f"A wave of amplitude {A1:g} m transfers {E1:g} J of energy in a certain time. Calculate the "
                        f"energy transferred in the same time when the amplitude is {A2:g} m.", E2, "J",
                    [r"\frac{E_1}{A_1^2} = \frac{E_2}{A_2^2}", rf"\frac{{{E1:g}}}{{{A1:g}^2}} = \frac{{E_2}}{{{A2:g}^2}}",
                     rf"E_2 = {ltx(E2)}\ \mathrm{{J}}"],
                    wrong=[(E1 * A2 / A1, "Energy is proportional to amplitude squared.")], notes=NOTES)
    E2 = sig(E1 * uni(0.15, 0.70, 2), 2)
    A2 = A1 * math.sqrt(E2 / E1)
    return calc(QT, f"A wave of amplitude {A1:g} m has energy {E1:g} J. Calculate its amplitude when its energy has "
                    f"fallen to {E2:g} J.", A2, "m",
                [r"\frac{E_1}{A_1^2} = \frac{E_2}{A_2^2}", rf"A_2 = {ltx(A2)}\ \mathrm{{m}}"],
                wrong=[(A1 * E2 / E1, "Take the square root: E ∝ A²."), (A2**2, "That is A² — take the square root.")], notes=NOTES)


def gen_stationary(level="AH"):
    kind = random.choice(["sound", "string", "harmonic"])
    if kind == "sound":
        f = random.randrange(1500, 4200, 100)
        n = random.randint(3, 8)
        lam = V_SOUND / f * random.uniform(0.98, 1.02)
        d = sig(n * lam / 2, 3)
        lam = 2 * d / n
        v = f * lam
        return calc(QT, f"A stationary sound wave is set up using a {f} Hz source and a reflector. A microphone moves "
                        f"{d:g} m from one node, passing through {n} node spacings, to another node. Calculate the speed of sound.", v, "m s⁻¹",
                    [rf"\frac{{\lambda}}{{2}} = \frac{{{d:g}}}{{{n}}}", rf"\lambda = {ltx(lam)}\ \mathrm{{m}}", r"v = f\lambda",
                     rf"v = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(v / 2, "Node to node is half a wavelength."), (f * d, "First find the wavelength from the node spacing.")],
                    scaffold=[("What is the wavelength?", lam, "m"), ("What is the speed?", v, "m s⁻¹")], notes=NOTES)
    length = uni(0.50, 1.80, 2)
    n = random.randint(2, 5)
    lam = 2 * length / n
    if kind == "string":
        return calc(QT, f"A string fixed at both ends, {length:g} m long, vibrates with a stationary wave of {n} loops. "
                        f"Calculate the wavelength.", lam, "m",
                    [T("Each loop is half a wavelength."), rf"{n} \times \frac{{\lambda}}{{2}} = {length:g}", rf"\lambda = {ltx(lam)}\ \mathrm{{m}}"],
                    wrong=[(length / n, "Each loop is half a wavelength, not a whole one.")], notes=NOTES)
    f1 = random.randrange(55, 220, 5)
    return calc(QT, f"The fundamental frequency of a string fixed at both ends is {f1} Hz. Determine the frequency of the "
                    f"stationary wave with {n} loops.", n * f1, "Hz",
                [T("The fundamental has one loop. With n loops the wavelength is 1/n as long and v is unchanged."),
                 rf"f = {n} \times {f1} = {n*f1}\ \mathrm{{Hz}}"],
                wrong=[(f1 / n, "More loops mean a shorter wavelength and a higher frequency.")], notes=NOTES)


_EXPLAIN = [
    ("How is a stationary wave formed?",
     "By the interference of two waves of the same frequency and amplitude travelling in opposite directions.",
     [("By two waves of different frequencies travelling in the same direction.", "That does not give fixed nodes."),
      ("When a wave loses all its energy and stops moving.", "A stationary wave is a superposition of two moving waves."),
      ("By two waves of the same frequency travelling in the same direction.", "They must travel in opposite directions.")],
     "Often a wave and its reflection."),
    ("A student moves a detector between a microwave source and a metal plate and finds maxima and minima. Why?",
     "The reflected wave interferes with the incident wave: antinodes where they interfere constructively and nodes where destructively.",
     [("The microwaves are absorbed at regular distances in the air.", "Air does not absorb at regular intervals."),
      ("The detector blocks the wave at some positions.", "The pattern comes from interference."),
      ("The source changes its frequency as the detector moves.", "The frequency is constant.")],
     "Name the two interfering waves."),
    ("What is meant by an antinode in a stationary wave?",
     "A position where the amplitude of oscillation is a maximum.",
     [("A position where the displacement is always zero.", "That is a node."),
      ("A position where the displacement is always at its maximum value.", "The displacement still oscillates."),
      ("A position where the wave is reflected.", "Reflection happens at a boundary.")],
     "The amplitude, not the displacement, is a maximum."),
    ("In y = A sin 2π(ft + x/λ), in which direction does the wave travel?",
     "In the negative x direction.",
     [("In the positive x direction.", "That has a minus sign between the terms."),
      ("It is a stationary wave.", "A stationary wave is the sum of two travelling waves."),
      ("In the y direction.", "y is the displacement of the medium.")],
     "The sign between the t and x terms gives the direction."),
    ("The amplitude of a wave is halved. What happens to the energy it transfers each second?",
     "It falls to one quarter, because E = kA².",
     [("It halves.", "E is proportional to A², not A."), ("It is unchanged.", "Energy depends on amplitude."),
      ("It doubles.", "A smaller amplitude means less energy.")],
     "State the relationship."),
]
gen_waves_explain = explain_set(QT, _EXPLAIN, NOTES)
