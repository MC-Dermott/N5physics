"""AH — Simple harmonic motion."""
import math
import random

from topics.quanta_waves.common_ah import L, T, calc, explain_set, fmt, ltx, pick_sig, sig, uni

QT = "Simple Harmonic Motion"

NOTES = r"""
## Simple harmonic motion

**SHM:** the unbalanced force (and acceleration) is proportional to, and in the opposite direction to,
the displacement from the rest position.

$$F = -ky \qquad a = \frac{d^2y}{dt^2} = -\omega^2 y \qquad \omega = 2\pi f = \frac{2\pi}{T}$$

$$y = A\cos\omega t \ \text{ or }\ y = A\sin\omega t \qquad v = \pm\omega\sqrt{A^2 - y^2}$$

$$E_k = \tfrac{1}{2}m\omega^2(A^2 - y^2) \qquad E_P = \tfrac{1}{2}m\omega^2 y^2$$

- Use y = A sin ωt if y = 0 at t = 0, and y = A cos ωt if y = A at t = 0. **Radians** mode.
- For a mass on a spring, ma = −ky gives ω² = k/m.
- **Damping:** underdamping (oscillates with decreasing amplitude), critical damping (returns to rest in
  the shortest time without oscillating), overdamping (returns slowly without oscillating).
"""


def gen_shm_motion(level="AH"):
    A = uni(0.020, 0.150, 3)
    f = uni(0.50, 5.0)
    w = 2 * math.pi * f
    kind = random.choice(["vmax", "amax", "a", "y", "freq"])
    stem = f"An object moves with simple harmonic motion of amplitude {A:g} m and frequency {f:g} Hz. "
    om = [r"\omega = 2\pi f", rf"\omega = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"]
    if kind == "vmax":
        return calc(QT, stem + "Calculate its maximum speed.", w * A, "m s⁻¹",
                    om + [r"v = \pm\omega\sqrt{A^2 - y^2} \quad \text{with } y = 0", rf"v_{{max}} = {ltx(w*A)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(f * A, "ω = 2πf."), (w**2 * A, "That is the maximum acceleration.")],
                    scaffold=[("What is ω?", w, "rad s⁻¹"), ("What is the maximum speed?", w * A, "m s⁻¹")], notes=NOTES)
    if kind == "amax":
        return calc(QT, stem + "Calculate the magnitude of its maximum acceleration.", w**2 * A, "m s⁻²",
                    om + [r"a = -\omega^2 y", rf"a_{{max}} = \omega^2 A = {ltx(w**2*A)}\ \mathrm{{m\,s^{{-2}}}}"],
                    wrong=[(w * A, "ω must be squared."), (f**2 * A, "ω = 2πf.")],
                    scaffold=[("What is ω?", w, "rad s⁻¹"), ("What is the maximum acceleration?", w**2 * A, "m s⁻²")], notes=NOTES)
    if kind == "a":
        y = sig(A * uni(0.20, 0.80, 2), 2)
        return calc(QT, stem + f"Calculate the magnitude of its acceleration when the displacement is {y:g} m.", w**2 * y, "m s⁻²",
                    om + [r"a = -\omega^2 y", rf"|a| = {ltx(w**2*y)}\ \mathrm{{m\,s^{{-2}}}}"],
                    wrong=[(w**2 * A, "Use the displacement given, not the amplitude."), (w * y, "ω must be squared.")], notes=NOTES)
    if kind == "y":
        t = sig(uni(0.10, 0.90, 2) / f, 2)
        y = A * math.sin(w * t)
        if abs(y) < 0.1 * A:
            t = sig(0.2 / f, 2)
            y = A * math.sin(w * t)
        return calc(QT, stem + f"The displacement is zero at t = 0 and increasing. Calculate the displacement at t = {t:g} s.", y, "m",
                    om + [r"y = A\sin\omega t", rf"y = {A:g}\sin({ltx(w)} \times {t:g}) = {ltx(y)}\ \mathrm{{m}}"],
                    wrong=[(A * math.sin(math.radians(w * t)), "Your calculator is in degrees. ωt is in radians."),
                           (A * math.cos(w * t), "y = 0 at t = 0, so use sine.")], notes=NOTES)
    amax = sig(w**2 * A, 3)
    ans = math.sqrt(amax / A) / (2 * math.pi)
    return calc(QT, f"An object in SHM of amplitude {A:g} m has a maximum acceleration of {fmt(amax)} m s⁻². "
                    f"Calculate the frequency of the motion.", ans, "Hz",
                [r"a = -\omega^2 y", rf"\omega = {ltx(math.sqrt(amax/A))}\ \mathrm{{rad\,s^{{-1}}}}", r"\omega = 2\pi f",
                 rf"f = {ltx(ans)}\ \mathrm{{Hz}}"],
                wrong=[(math.sqrt(amax / A), "That is ω. Divide by 2π.")],
                scaffold=[("What is ω?", math.sqrt(amax / A), "rad s⁻¹"), ("What is f?", ans, "Hz")], notes=NOTES)


def gen_shm_energy(level="AH"):
    m, A = uni(0.10, 2.0, 2), uni(0.040, 0.200, 3)
    w = uni(3.0, 15.0)
    y = sig(A * uni(0.30, 0.75, 2), 2)
    stem = (f"A {m:g} kg mass moves with SHM of amplitude {A:g} m and angular frequency {w:g} rad s⁻¹. ")
    kind = random.choice(["v", "ek", "ep", "max"])
    if kind == "v":
        v = w * math.sqrt(A**2 - y**2)
        return calc(QT, stem + f"Calculate its speed when the displacement is {y:g} m.", v, "m s⁻¹",
                    [r"v = \pm\omega\sqrt{A^2 - y^2}", rf"v = {w:g}\sqrt{{{A:g}^2 - {y:g}^2}} = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(w * (A - y), "Square each term before subtracting: √(A² − y²)."), (w * A, "That is the maximum speed.")], notes=NOTES)
    ek = 0.5 * m * w**2 * (A**2 - y**2)
    ep = 0.5 * m * w**2 * y**2
    total = 0.5 * m * w**2 * A**2
    if kind == "ek":
        return calc(QT, stem + f"Calculate its kinetic energy when the displacement is {y:g} m.", ek, "J",
                    [r"E_k = \tfrac{1}{2}m\omega^2(A^2 - y^2)", rf"E_k = {ltx(ek)}\ \mathrm{{J}}"],
                    wrong=[(ep, "That is the potential energy."), (0.5 * m * w**2 * (A - y)**2, "(A² − y²) is not (A − y)².")], notes=NOTES)
    if kind == "ep":
        return calc(QT, stem + f"Calculate its potential energy when the displacement is {y:g} m.", ep, "J",
                    [r"E_P = \tfrac{1}{2}m\omega^2 y^2", rf"E_P = {ltx(ep)}\ \mathrm{{J}}"],
                    wrong=[(ek, "That is the kinetic energy."), (0.5 * m * w * y**2, "ω must be squared.")], notes=NOTES)
    return calc(QT, stem + "Calculate its maximum potential energy.", total, "J",
                [r"E_P = \tfrac{1}{2}m\omega^2 y^2 \quad \text{with } y = A", rf"E_P = {ltx(total)}\ \mathrm{{J}}"],
                wrong=[(0.5 * m * w**2 * A, "A must be squared.")], notes=NOTES)


def gen_mass_spring(level="AH"):
    m = uni(0.10, 1.5, 2)
    k = random.randrange(8, 120, 2)
    w = math.sqrt(k / m)
    period = 2 * math.pi / w
    kind = random.choice(["T", "k", "force"])
    if kind == "T":
        return calc(QT, f"A {m:g} kg mass oscillates on a spring of spring constant {k} N m⁻¹. Calculate the period.", period, "s",
                    [r"ma = -ky \quad \text{and} \quad a = -\omega^2 y \;\Rightarrow\; \omega^2 = \frac{k}{m}",
                     rf"\omega = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}", r"\omega = \frac{2\pi}{T}", rf"T = {ltx(period)}\ \mathrm{{s}}"],
                    wrong=[(2 * math.pi / (k / m), "ω² = k/m — take the square root."), (1 / w, "T = 2π/ω.")],
                    scaffold=[("What is ω?", w, "rad s⁻¹"), ("What is T?", period, "s")], notes=NOTES)
    if kind == "k":
        pg = sig(period, 3)
        wg = 2 * math.pi / pg
        ans = m * wg**2
        return calc(QT, f"A {m:g} kg mass on a spring oscillates with SHM with a period of {fmt(pg)} s. "
                        f"Calculate the spring constant.", ans, "N m⁻¹",
                    [r"\omega = \frac{2\pi}{T}", rf"\omega = {ltx(wg)}\ \mathrm{{rad\,s^{{-1}}}}",
                     r"k = m\omega^2", rf"k = {ltx(ans)}\ \mathrm{{N\,m^{{-1}}}}"],
                    wrong=[(m * wg, "ω must be squared.")],
                    scaffold=[("What is ω?", wg, "rad s⁻¹"), ("What is k?", ans, "N m⁻¹")], notes=NOTES)
    y = uni(0.015, 0.090, 3)
    return calc(QT, f"A spring of spring constant {k} N m⁻¹ is stretched {y:g} m from its rest position. Calculate the "
                    f"magnitude of the restoring force.", k * y, "N",
                [r"F = -ky", rf"|F| = {k} \times {y:g} = {ltx(k*y)}\ \mathrm{{N}}"],
                wrong=[(k / y, "F = ky.")], notes=NOTES)


_EXPLAIN = [
    ("What is meant by simple harmonic motion?",
     "Motion in which the acceleration is proportional to, and in the opposite direction to, the displacement from the rest position.",
     [("Motion in which the restoring force is proportional to the displacement.", "The direction is missing: it must be **opposite** to the displacement."),
      ("Motion which repeats itself with a constant period.", "Not all periodic motion is SHM."),
      ("Motion in which the velocity is proportional to the displacement.", "It is the acceleration (or unbalanced force).")],
     "State both proportionality and direction."),
    ("A displacement is given by y = A cos ωt. Which working shows that this is consistent with SHM?",
     "Differentiate twice to get d²y/dt² = −ω²A cos ωt, substitute y to get d²y/dt² = −ω²y, and say this is the SHM form.",
     [("Differentiate once to get dy/dt = −ωA sin ωt, which has a negative sign, so it is SHM.", "SHM is defined by the second derivative."),
      ("Substitute t = 0 to show that y = A.", "That shows only the starting position."),
      ("Integrate y twice to show the result is proportional to y.", "Differentiate with respect to t.")],
     "Differentiate with respect to t, substitute back, and state the significance of the result."),
    ("A child bouncing on a trampoline leaves the surface during each bounce. Why is the motion no longer approximately SHM?",
     "While the child is in the air the unbalanced force and acceleration are not proportional to the displacement.",
     [("The amplitude is too large to be measured.", "Size of measurement is not the point."),
      ("The period is no longer constant, because the child gets tired.", "Address proportionality of force and displacement."),
      ("Energy is no longer conserved in the air.", "Energy conservation is not the definition of SHM.")],
     "Answer in terms of proportionality of force (or acceleration) and displacement."),
    ("An oscillating system returns to its rest position in the shortest possible time without overshooting. What type of damping is this?",
     "Critical damping.",
     [("Underdamping.", "An underdamped system oscillates."),
      ("Overdamping.", "An overdamped system returns more slowly."),
      ("Total damping.", "The three types are under-, critical and over-damping.")],
     "Only three types of damping are needed."),
    ("A damped oscillation shows several cycles, each with a smaller amplitude than the one before. Which change would make it die away more quickly?",
     "Use an arrangement that increases the resistive force, such as a more viscous oil.",
     [("Increase the initial amplitude.", "This does not increase the damping."),
      ("Decrease the resistive force.", "That reduces the damping."),
      ("Remove energy from the system before releasing it.", "This only changes the starting amplitude.")],
     "Suggest a practical change, not just 'more resistive force'."),
    ("A mass on a spring is replaced with a stiffer spring. What happens to the angular frequency, and why?",
     "It increases, because k is greater while the mass is constant, and ω² = k/m.",
     [("It decreases, because the spring is harder to stretch.", "A greater k gives a greater restoring force and acceleration."),
      ("It is unchanged, because the mass is the same.", "ω also depends on k."),
      ("It increases, because the amplitude must be smaller.", "In SHM ω does not depend on amplitude.")],
     "Say what stays constant and give the relationship."),
    ("Where in its motion does an object in SHM have maximum kinetic energy?",
     "At the rest position, where y = 0 and the potential energy is zero.",
     [("At maximum displacement.", "The speed is zero there."),
      ("Half way between rest and maximum displacement.", "Ek is greatest at y = 0."),
      ("Ek is the same everywhere.", "Only the total energy is constant without damping.")],
     "Ek = ½mω²(A² − y²)."),
]
gen_shm_explain = explain_set(QT, _EXPLAIN, NOTES)
