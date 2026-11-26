"""AH — Interference by division of amplitude and division of wavefront."""
import math
import random

from topics.quanta_waves.common_ah import L, T, calc, explain_set, fmt, ltx, pick_sig, sig, uni

QT = "Interference"

NOTES = r"""
## Interference

$$opd = n \times gpd \qquad opd = m\lambda \ \text{ or } \left(m+\tfrac{1}{2}\right)\lambda \qquad
\Delta x = \frac{\lambda l}{2d} \qquad d = \frac{\lambda}{4n} \qquad \Delta x = \frac{\lambda D}{d}$$

- **Coherent** waves have a **constant phase relationship**.
- Constructive interference: two coherent waves meet **in phase**. Destructive: they meet exactly out of phase.
- Reflecting off a **more dense** medium (from a less dense one): phase change of **π rad**. Reflecting off a
  less dense medium: **no** phase change. Check each reflection before choosing mλ or (m + ½)λ.
- **Division of amplitude:** thin films, wedge fringes, coated lenses. **Division of wavefront:** Young's slits.
- Wedge: Δx = λl/2d, where l is the length of the wedge and d its separation at the open end.
- Young's slits: Δx = λD/d, where D is the slit-to-screen distance and d the slit separation.
- A non-reflective coating gives **destructive** interference of the reflected light for one wavelength.
"""


def gen_optical_path(level="AH"):
    name, n = random.choice([("glass", 1.51), ("water", 1.33), ("Perspex", 1.49), ("glycerol", 1.47), ("diamond", 2.42)])
    g = sig(uni(1.0, 9.0) * 10.0 ** random.choice([-3, -6]), 2)
    if random.random() < 0.6:
        return calc(QT, f"Light travels a geometrical path of {fmt(g, 2)} m in {name} (refractive index {n}). Calculate the "
                        f"optical path.", n * g, "m",
                    [r"opd = n \times gpd", rf"opd = {n} \times {ltx(g, 2)} = {ltx(n*g)}\ \mathrm{{m}}"],
                    wrong=[(g / n, "Multiply by n.")], notes=NOTES)
    extra = sig((n - 1) * g, 3)
    return calc(QT, f"A thin sheet of {name} (refractive index {n}) and thickness {fmt(g, 2)} m is placed in one of two "
                    f"identical paths in air. Calculate the optical path difference this introduces.", (n - 1) * g, "m",
                [rf"opd = n \times gpd - gpd = ({n} - 1) \times {ltx(g, 2)}", rf"opd = {ltx((n-1)*g)}\ \mathrm{{m}}"],
                wrong=[(n * g, "Subtract the optical path of the same distance in air.")], notes=NOTES)


def gen_thin_film(level="AH"):
    nm = random.randrange(420, 700, 5)
    lam = nm * 1e-9
    kind = random.choice(["d", "lam", "n", "soap"])
    n = 1.38
    d = lam / (4 * n)
    if kind == "d":
        return calc(QT, f"A glass lens is coated with magnesium fluoride (refractive index 1.38) to be non-reflecting at "
                        f"{nm} nm. Calculate the minimum thickness of the coating.", d, "m",
                    [r"d = \frac{\lambda}{4n}", rf"d = \frac{{{nm} \times 10^{{-9}}}}{{4 \times 1.38}} = {ltx(d)}\ \mathrm{{m}}"],
                    wrong=[(lam / (2 * n), "The relationship is d = λ/4n."), (lam / 4, "Include the refractive index of the coating."),
                           (lam / (4 * 1.51), "Use the refractive index of the coating, not the glass.")], notes=NOTES)
    dg = sig(d, 3)
    if kind == "lam":
        ans = 4 * n * dg
        return calc(QT, f"A lens has a magnesium fluoride coating (refractive index 1.38) of thickness {fmt(dg)} m. "
                        f"Calculate the wavelength for which it is non-reflecting.", ans, "m",
                    [r"d = \frac{\lambda}{4n}", rf"\lambda = 4nd = {ltx(ans)}\ \mathrm{{m}}"],
                    wrong=[(2 * n * dg, "λ = 4nd.")], notes=NOTES)
    if kind == "n":
        n2 = random.choice([1.25, 1.30, 1.34, 1.42])
        d2 = sig(lam / (4 * n2), 3)
        return calc(QT, f"A coating of thickness {fmt(d2)} m makes a lens non-reflecting at {nm} nm. Calculate the "
                        f"refractive index of the coating.", lam / (4 * d2), "",
                    [r"d = \frac{\lambda}{4n}", rf"n = {ltx(lam/(4*d2))}"],
                    wrong=[(lam / (2 * d2), "d = λ/4n.")], notes=NOTES)
    ns, m = 1.33, random.randint(0, 3)
    t = (m + 0.5) * lam / (2 * ns)
    return calc(QT, f"A soap film in air (refractive index 1.33) is viewed by reflection at normal incidence in light of "
                    f"wavelength {nm} nm. Calculate the thickness of the film which gives constructive interference "
                    f"with m = {m}.", t, "m",
                [T("There is a π phase change at the first surface only, so constructive interference needs opd = (m + ½)λ."),
                 rf"opd = 2nt = \left({m} + \tfrac{{1}}{{2}}\right)\lambda", rf"t = {ltx(t)}\ \mathrm{{m}}"],
                wrong=[(max(m, 1) * lam / (2 * ns), "Only one reflection has a phase change, so use (m + ½)λ for constructive interference."),
                       (2 * t, "The light crosses the film twice: opd = 2nt."), (t * ns, "Include the refractive index in the optical path.")],
                notes=NOTES)


def gen_wedge(level="AH"):
    nm = random.choice([486, 509, 589, 633, 656])
    lam = nm * 1e-9
    length = uni(0.050, 0.120, 3)
    d = sig(uni(2.0, 9.0) * 1e-5, 2)
    dx = lam * length / (2 * d)
    N = random.choice([10, 20])
    if random.random() < 0.5:
        return calc(QT, f"Two glass slides {length:g} m long form an air wedge, separated at one end by a foil of thickness "
                        f"{fmt(d, 2)} m. The wedge is lit by light of wavelength {nm} nm. Calculate the fringe separation.", dx, "m",
                    [r"\Delta x = \frac{\lambda l}{2d}", rf"\Delta x = {ltx(dx)}\ \mathrm{{m}}"],
                    wrong=[(lam * length / d, "The wedge relationship has 2d: Δx = λl/2d.")], notes=NOTES)
    total = sig(N * dx, 3)
    dxm = total / N
    ans = lam * length / (2 * dxm)
    return calc(QT, f"A hair is placed between the ends of two glass slides to form an air wedge {length:g} m long. With "
                    f"light of wavelength {nm} nm, {N} fringe spacings measure {fmt(total)} m. Determine the thickness of the hair.", ans, "m",
                [rf"\Delta x = \frac{{{ltx(total)}}}{{{N}}} = {ltx(dxm)}\ \mathrm{{m}}", r"\Delta x = \frac{\lambda l}{2d}",
                 rf"d = {ltx(ans)}\ \mathrm{{m}}"],
                wrong=[(lam * length / (2 * total), f"Divide the distance by {N} to get one fringe spacing."),
                       (2 * ans, "The wedge relationship has 2d.")],
                scaffold=[("What is the fringe separation?", dxm, "m"), ("What is the thickness?", ans, "m")], notes=NOTES)


def gen_young(level="AH"):
    nm = random.choice([486, 509, 589, 633, 656])
    lam = nm * 1e-9
    D = uni(1.2, 4.5)
    d = sig(uni(0.15, 0.80, 2) * 1e-3, 2)
    dx = lam * D / d
    kind = random.choice(["dx", "lam", "d"])
    if kind == "dx":
        return calc(QT, f"Light of wavelength {nm} nm passes through two slits {fmt(d, 2)} m apart on to a screen {D:g} m "
                        f"away. Calculate the fringe separation.", dx, "m",
                    [r"\Delta x = \frac{\lambda D}{d}", rf"\Delta x = {ltx(dx)}\ \mathrm{{m}}"],
                    wrong=[(dx / 2, "The 2d belongs to the wedge relationship. Young's slits: Δx = λD/d."),
                           (lam * d / D, "D is the slit-to-screen distance and d the slit separation.")], notes=NOTES)
    dxg = sig(dx, 3)
    if kind == "lam":
        N = 10
        total = sig(N * dx, 3)
        ans = total / N * d / D
        return calc(QT, f"In a Young's slits experiment the slits are {fmt(d, 2)} m apart and the screen is {D:g} m away. "
                        f"The distance across {N} fringe spacings is {fmt(total)} m. Calculate the wavelength.", ans, "m",
                    [rf"\Delta x = {ltx(total/N)}\ \mathrm{{m}}", r"\Delta x = \frac{\lambda D}{d}", rf"\lambda = {ltx(ans)}\ \mathrm{{m}}"],
                    wrong=[(total * d / D, f"Divide by {N} to find one fringe spacing.")],
                    scaffold=[("What is the fringe separation?", total / N, "m"), ("What is the wavelength?", ans, "m")], notes=NOTES)
    ans = lam * D / dxg
    return calc(QT, f"Light of wavelength {nm} nm gives fringes {fmt(dxg)} m apart on a screen {D:g} m from a double slit. "
                    f"Calculate the slit separation.", ans, "m",
                [r"\Delta x = \frac{\lambda D}{d}", rf"d = {ltx(ans)}\ \mathrm{{m}}"],
                wrong=[(ans / 2, "Young's slits: Δx = λD/d, with no 2.")], notes=NOTES)


_EXPLAIN = [
    ("What two conditions are needed for waves to produce constructive interference at a point?",
     "The waves must be coherent and must meet in phase.",
     [("The waves must be monochromatic and meet in phase.", "The condition needed is coherence."),
      ("The waves must be coherent and have the same amplitude.", "Both conditions needed are coherence and meeting in phase."),
      ("The waves must travel at the same speed and be polarised.", "Neither is the required condition.")],
     "State both conditions."),
    ("What is meant by two waves being coherent?",
     "They have a constant phase relationship.",
     [("They are always in phase.", "The phase difference need only be constant."),
      ("They have the same amplitude.", "Amplitude is not the condition."),
      ("They have the same speed.", "Speed alone does not fix the phase relationship.")],
     "Constant phase relationship."),
    ("Why does a Young's double slit arrangement produce a series of bright fringes?",
     "The slits act as coherent sources; a bright fringe is where the light from them meets in phase and interferes constructively.",
     [("Each slit focuses the light into a series of bright lines.", "The fringes come from interference between the two slits."),
      ("The light from each slit has a different wavelength.", "The sources are coherent, from one wavefront."),
      ("Bright fringes are where the light has travelled the shortest distance.", "It depends on the path difference.")],
     "Use the terms coherent and in phase."),
    ("Which describes interference in a thin oil film on water?",
     "Division of amplitude: each ray is partly reflected at the top surface and partly at the bottom surface.",
     [("Division of wavefront: different parts of the wavefront pass through different slits.", "That describes Young's slits."),
      ("Diffraction: light spreads as it passes through the film.", "The effect is interference between reflected rays."),
      ("Division of wavelength: the film separates the colours by refraction.", "Colours come from interference.")],
     "Thin films, wedges and coatings are division of amplitude."),
    ("Light in air reflects from the surface of glass. What is the phase change on reflection?",
     "π rad, because the light reflects from an interface with a more dense medium.",
     [("Zero, because the light stays in air.", "Reflection off a more dense medium gives π."),
      ("2π rad.", "The change is π."),
      ("π/2 rad.", "The change is π.")],
     "Less dense to more dense boundary: π."),
    ("Why does a coated camera lens often look purple?",
     "The coating cancels reflections near one wavelength in the middle of the spectrum, so more red and blue light is reflected.",
     [("The coating absorbs all the green light.", "The reflected green light is cancelled by interference."),
      ("Magnesium fluoride is a purple material.", "It is transparent."),
      ("The coating gives constructive interference for green light.", "It gives destructive interference of the reflections.")],
     "It is non-reflecting for one wavelength only."),
    ("In a Young's slits experiment, red light replaces green light. What happens to the fringe separation, and why?",
     "It increases, because λ is greater while D and d are constant, and Δx = λD/d.",
     [("It decreases, because red light has a lower frequency.", "Δx is proportional to λ."),
      ("It is unchanged, because the slits are unchanged.", "Δx depends on λ."),
      ("It increases, because red light is brighter.", "Brightness does not set the spacing.")],
     "Say what stays constant and give the relationship."),
    ("Why does a student measure the distance across ten fringes instead of one?",
     "To reduce the percentage (fractional) uncertainty in the fringe separation.",
     [("To reduce the scale reading uncertainty of the ruler.", "The scale reading uncertainty of the ruler is unchanged."),
      ("To reduce the absolute uncertainty of the measuring instrument.", "That is not changed by measuring a longer distance."),
      ("To make the fringes brighter.", "It does not change the light.")],
     "Percentage or fractional uncertainty."),
]
gen_interference_explain = explain_set(QT, _EXPLAIN, NOTES)
