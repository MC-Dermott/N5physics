"""AH Quanta and Waves — exam-style multi-part scenarios in the style of SQA papers.

"Show" questions are asked as calculations of the shown value, so they can be marked.
"""
import math

from topics.exam_style.base import Exam, fmt, ltx, pick, sig
from topics.quanta_waves.common_ah import C, E_CHARGE, H, LEVEL, M_E, M_P, UNIT, uni
from topics.quanta_waves.interference_ah import NOTES as INT_N
from topics.quanta_waves.polarisation_ah import NOTES as POL_N
from topics.quanta_waves.quantum_ah import NOTES as QU_N
from topics.quanta_waves.shm_ah import NOTES as SHM_N
from topics.quanta_waves.space_particles_ah import NOTES as SP_N
from topics.quanta_waves.waves_ah import NOTES as WAVE_N

_QU, _SP, _SHM = "Introduction to Quantum Theory", "Particles from Space", "Simple Harmonic Motion"
_WAVE, _INT, _POL = "Waves", "Interference", "Polarisation"
_NOTES = {_QU: QU_N, _SP: SP_N, _SHM: SHM_N, _WAVE: WAVE_N, _INT: INT_N, _POL: POL_N}


def _exam():
    return Exam(UNIT, LEVEL, _NOTES)


def _electron_beam(level=LEVEL):
    ex = _exam()
    v = sig(uni(2.0, 9.0) * 1e6, 2)
    dx = pick(1.0e-10, 2.0e-10, 5.0e-10)
    p = M_E * v
    lam = H / sig(p)
    dp = H / (4 * math.pi * dx)
    ex.on(_QU).num("Calculate the de Broglie wavelength of the electrons.", lam, "m",
                   wrong=[(H / v, "p = mv — include the electron mass.")],
                   working=[r"p = mv", r"\lambda = \frac{h}{p}", rf"\lambda = {ltx(lam)}\ \mathrm{{m}}"],
                   scaffold=[("What is the momentum?", p, "kg m s⁻¹")])
    ex.choice("The electrons produce a pattern of bright and dark rings after passing through a thin crystal. What "
              "does this show?", "Electrons can behave as waves: the pattern is produced by diffraction and interference.",
              [("Electrons behave only as particles that bounce off atoms.", "Rings are an interference pattern."),
               ("The electrons have been converted into photons.", "They are still electrons."),
               ("The crystal emits light of different colours.", "The pattern is formed by the electrons.")])
    ex.num(f"At one point the uncertainty in the position of an electron is {fmt(dx)} m. Calculate the minimum "
           f"uncertainty in its momentum.", dp, "kg m s⁻¹",
           wrong=[(H / dx, "Divide by 4π.")],
           working=[r"\Delta x\,\Delta p_x \geq \frac{h}{4\pi}", rf"\Delta p_{{min}} = {ltx(dp)}\ \mathrm{{kg\,m\,s^{{-1}}}}"])
    ex.choice("The position is then determined more precisely. What is the consequence?",
              "The minimum uncertainty in the momentum increases.",
              [("The minimum uncertainty in the momentum decreases.", "Δx Δp has a minimum value."),
               ("The momentum becomes zero.", "The principle says nothing of the kind."),
               ("Both can now be known precisely.", "They cannot both be known precisely.")])
    return ex.build(f"In an electron tube, electrons travel at {fmt(v, 2)} m s⁻¹.")


def _hydrogen_atom(level=LEVEL):
    ex = _exam()
    n = pick(2, 3, 4)
    r = sig(5.29e-11 * n**2)
    mom = n * H / (2 * math.pi)
    v = mom / (M_E * r)
    nm = {2: 122, 3: 656, 4: 486}[n]
    lower = 1 if n == 2 else 2
    ex.on(_QU).num(f"Calculate the speed of the electron in this orbit.", v, "m s⁻¹",
                   wrong=[(v * 2 * math.pi, "mvr = nh/2π.")],
                   working=[r"mvr = \frac{nh}{2\pi}", rf"v = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num("Calculate the de Broglie wavelength of the electron.", H / (M_E * sig(v)), "m",
           working=[r"\lambda = \frac{h}{p}", rf"\lambda = {ltx(H/(M_E*sig(v)))}\ \mathrm{{m}}"])
    ex.num(f"The electron drops to the n = {lower} orbit, emitting a photon of wavelength {nm} nm. Calculate the "
           f"energy of the photon.", H * C / (nm * 1e-9), "J",
           wrong=[(H * C / nm, "Convert nm to m.")],
           working=[r"v = f\lambda \qquad E = hf", rf"E = {ltx(H*C/(nm*1e-9))}\ \mathrm{{J}}"])
    ex.choice("How does the Bohr model explain why hydrogen emits only certain wavelengths?",
              "The electron has discrete energy states, so only certain photon energies can be emitted.",
              [("The electron can lose any amount of energy.", "That would give a continuous spectrum."),
               ("Only certain wavelengths can pass through the atom.", "This is about emission."),
               ("The electron's mass changes between orbits.", "The mass is constant.")])
    return ex.build(f"In the Bohr model of the hydrogen atom, the electron is in the n = {n} orbit, of radius {fmt(r)} m.")


def _aurora(level=LEVEL):
    ex = _exam()
    v = sig(uni(3.0, 8.0) * 1e5, 2)
    B = sig(uni(3.0, 6.0) * 1e-5, 2)
    ang = pick(30, 40, 50, 60)
    perp = v * math.sin(math.radians(ang))
    par = v * math.cos(math.radians(ang))
    r = M_P * perp / (E_CHARGE * B)
    T_ = 2 * math.pi * M_P / (E_CHARGE * B)
    ex.on(_SP).choice("The proton is part of the solar wind. What is the solar wind?",
                      "A flow of charged particles from the Sun in the form of plasma.",
                      [("A flow of photons from the Sun.", "It is charged particles."),
                       ("Air in the upper atmosphere moved by sunlight.", "It comes from the Sun."),
                       ("Cosmic rays from distant galaxies.", "It comes from the Sun.")])
    ex.num("Calculate the component of the proton's velocity perpendicular to the field.", perp, "m s⁻¹",
           wrong=[(par, "That is the parallel component.")],
           working=[rf"v_\perp = v\sin\theta = {ltx(perp)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num("Calculate the radius of the helical path.", M_P * sig(perp) / (E_CHARGE * B), "m",
           wrong=[(M_P * v / (E_CHARGE * B), "Use v sin θ.")],
           working=[r"qvB = \frac{mv^2}{r}", rf"r = {ltx(r)}\ \mathrm{{m}}"])
    ex.num("Calculate the distance the proton travels along the field in one revolution.", par * T_, "m",
           wrong=[(perp * T_, "Along the field use v cos θ.")],
           working=[rf"T = \frac{{2\pi r}}{{v_\perp}} = {ltx(T_)}\ \mathrm{{s}}", rf"d = v_\parallel T = {ltx(par*T_)}\ \mathrm{{m}}"],
           scaffold=[("What is the time for one revolution?", T_, "s")])
    ex.choice("Why is the path helical?",
              "The velocity component parallel to the field is unaffected; the perpendicular component gives circular motion.",
              [("The horizontal component is unaffected and the vertical component gives circular motion.", "Say parallel and perpendicular to the field."),
               ("The field does work on the proton, so it spirals.", "A magnetic field does no work."),
               ("Gravity pulls the proton into a spiral.", "The path is due to the magnetic force.")])
    return ex.build(f"A proton from the Sun enters a region of the Earth's magnetic field of magnetic induction "
                    f"{fmt(B, 2)} T. It travels at {fmt(v, 2)} m s⁻¹ at {ang}° to the field.")


def _cosmic_ray(level=LEVEL):
    ex = _exam()
    v = sig(uni(1.5, 4.0) * 1e6, 2)
    r = sig(uni(2.0, 9.0) * 1e2, 2)
    q = 2 * E_CHARGE
    m = 6.645e-27
    B = m * v / (q * r)
    tau = pick(2.2e-6, 2.6e-8, 8.4e-17)
    ex.on(_SP).num("Calculate the magnetic induction of the field.", B, "T",
                   wrong=[(m * v / (E_CHARGE * r), "An alpha particle has charge 3.20 × 10⁻¹⁹ C.")],
                   working=[r"qvB = \frac{mv^2}{r}", rf"B = {ltx(B)}\ \mathrm{{T}}"])
    ex.num("Calculate the force on the alpha particle.", q * v * sig(B), "N",
           working=[r"F = qvB", rf"F = {ltx(q*v*sig(B))}\ \mathrm{{N}}"])
    ex.choice("Which is a source of cosmic rays?", "Stars, including the Sun.",
              [("The solar wind.", "'Solar wind' is not accepted as an origin."),
               ("The Earth's magnetic field.", "It only deflects particles."),
               ("The ozone layer.", "Cosmic rays come from space.")])
    ex.on(_QU).num(f"In the atmosphere a particle is produced with a lifetime of {fmt(tau, 2)} s. Calculate the minimum "
                   f"uncertainty in its energy.", H / (4 * math.pi * tau), "J",
                   wrong=[(H / tau, "Divide by 4π.")],
                   working=[r"\Delta E\,\Delta t \geq \frac{h}{4\pi}", rf"\Delta E = {ltx(H/(4*math.pi*tau))}\ \mathrm{{J}}"])
    return ex.build(f"A cosmic ray alpha particle (mass 6.645 × 10⁻²⁷ kg, charge 3.20 × 10⁻¹⁹ C) moves at "
                    f"{fmt(v, 2)} m s⁻¹ at right angles to a magnetic field, in a circle of radius {fmt(r, 2)} m.")


def _spring(level=LEVEL):
    ex = _exam()
    m, k, A = uni(0.20, 0.80, 2), pick(12, 18, 24, 32, 45), uni(0.030, 0.090, 3)
    w = math.sqrt(k / m)
    ws = sig(w)
    y = sig(A * pick(0.4, 0.5, 0.6), 2)
    ex.on(_SHM).num("Calculate the angular frequency of the oscillation.", w, "rad s⁻¹",
                    wrong=[(k / m, "ω² = k/m.")],
                    working=[r"ma = -ky \quad a = -\omega^2 y", rf"\omega = \sqrt{{\frac{{k}}{{m}}}} = {ltx(w)}\ \mathrm{{rad\,s^{{-1}}}}"])
    ex.num("Calculate the period of the oscillation.", 2 * math.pi / ws, "s",
           working=[r"\omega = \frac{2\pi}{T}", rf"T = {ltx(2*math.pi/ws)}\ \mathrm{{s}}"])
    ex.num(f"Calculate the speed of the mass when its displacement is {y:g} m.", ws * math.sqrt(A**2 - y**2), "m s⁻¹",
           wrong=[(ws * A, "That is the maximum speed.")],
           working=[r"v = \pm\omega\sqrt{A^2 - y^2}", rf"v = {ltx(ws*math.sqrt(A**2-y**2))}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num("Calculate the maximum kinetic energy of the mass.", 0.5 * m * ws**2 * A**2, "J",
           working=[r"E_k = \tfrac{1}{2}m\omega^2(A^2 - y^2)", rf"E_k = {ltx(0.5*m*ws**2*A**2)}\ \mathrm{{J}}"])
    ex.choice("The mass is now immersed in oil and returns to rest in the shortest time without oscillating. Which "
              "type of damping is this?", "Critical damping.",
              [("Underdamping.", "It would oscillate."), ("Overdamping.", "It would take longer."),
               ("Resistive damping.", "Use under-, critical or over-damping.")])
    return ex.build(f"A {m:g} kg mass hangs from a spring of spring constant {k} N m⁻¹. It is pulled {A:g} m below its "
                    f"rest position and released. Damping is negligible.")


def _speaker(level=LEVEL):
    ex = _exam()
    f = pick(180, 250, 320, 440)
    A = pick(0.40e-3, 0.65e-3, 0.80e-3, 1.2e-3)
    w = 2 * math.pi * f
    lam = 340 / f
    x = sig(lam * pick(0.30, 0.45, 0.70), 2)
    k = pick(0.5, 0.64, 0.8)
    ex.on(_SHM).num("Calculate the maximum acceleration of the cone.", w**2 * A, "m s⁻²",
                    wrong=[(f**2 * A, "ω = 2πf.")],
                    working=[r"\omega = 2\pi f \qquad a = -\omega^2 y", rf"a_{{max}} = {ltx(w**2*A)}\ \mathrm{{m\,s^{{-2}}}}"])
    ex.num("Calculate the maximum speed of the cone.", w * A, "m s⁻¹",
           working=[r"v = \pm\omega\sqrt{A^2 - y^2}", rf"v_{{max}} = {ltx(w*A)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.on(_WAVE).num(f"The speed of sound is 340 m s⁻¹. Calculate the phase difference between two points {x:g} m apart "
                     f"in line with the loudspeaker.", 2 * math.pi * x / lam, "rad",
                     wrong=[(360 * x / lam, "That is in degrees.")],
                     working=[r"v = f\lambda \qquad \phi = \frac{2\pi x}{\lambda}", rf"\phi = {ltx(2*math.pi*x/lam)}\ \mathrm{{rad}}"],
                     scaffold=[("What is the wavelength?", lam, "m")])
    ex.num(f"The amplitude of the sound at one point falls to {k:g} of its original value. What fraction of the original "
           f"energy does the wave now have there?", k**2, "",
           wrong=[(k, "E is proportional to A².")],
           working=[r"E = kA^2", rf"\frac{{E_2}}{{E_1}} = {k:g}^2 = {ltx(k**2)}"])
    return ex.build(f"A loudspeaker cone moves with simple harmonic motion of frequency {f} Hz and amplitude {fmt(A, 2)} m.")


def _travelling(level=LEVEL):
    ex = _exam()
    A, f, k = uni(0.040, 0.120, 3), uni(3.0, 9.0), uni(0.50, 1.60, 2)
    lam = 1 / k
    x = sig(lam * pick(0.25, 0.35, 0.60), 2)
    ex.on(_WAVE).num("Determine the speed of the wave.", f / k, "m s⁻¹",
                     wrong=[(f * k, "The number multiplying x is 1/λ.")],
                     working=[rf"f = {f:g} \qquad \lambda = \frac{{1}}{{{k:g}}}", r"v = f\lambda", rf"v = {ltx(f/k)}\ \mathrm{{m\,s^{{-1}}}}"])
    ex.num(f"Calculate the phase difference between two points on the wave {x:g} m apart.", 2 * math.pi * x * k, "rad",
           working=[r"\phi = \frac{2\pi x}{\lambda}", rf"\phi = {ltx(2*math.pi*x*k)}\ \mathrm{{rad}}"])
    ex.choice("A second wave of the same frequency and amplitude travels in the opposite direction. Which equation "
              "describes it?", f"y = {A:g} sin 2π({f:g}t + {k:g}x)",
              [(f"y = {A:g} sin 2π({f:g}t − {k:g}x)", "That travels in the same direction."),
               (f"y = −{A:g} sin 2π({f:g}t − {k:g}x)", "This is only inverted; it travels the same way."),
               (f"y = {A:g} sin 2π({k:g}t + {f:g}x)", "f multiplies t.")])
    ex.num("The two waves form a stationary wave. Calculate the distance between neighbouring nodes.", lam / 2, "m",
           wrong=[(lam, "Node to node is half a wavelength.")],
           working=[r"\frac{\lambda}{2}", rf"{ltx(lam/2)}\ \mathrm{{m}}"])
    ex.on(_SHM).num("A particle of the medium moves with SHM. Calculate its maximum speed due to the original wave alone.",
                    2 * math.pi * f * A, "m s⁻¹", wrong=[(f * A, "ω = 2πf.")],
                    working=[r"v_{max} = \omega A", rf"v_{{max}} = {ltx(2*math.pi*f*A)}\ \mathrm{{m\,s^{{-1}}}}"])
    return ex.build(f"A wave is described by **y = {A:g} sin 2π({f:g}t − {k:g}x)**, in SI units.")


def _microwaves(level=LEVEL):
    ex = _exam()
    f = pick(9.4e9, 10.0e9, 10.5e9, 11.0e9)
    lam = C / f
    n_spaces = pick(5, 6, 8)
    ex.on(_WAVE).num(f"The metal plate reflects the microwaves, producing a stationary wave. Calculate the distance moved "
                     f"by the detector through {n_spaces} node spacings.", n_spaces * lam / 2, "m",
                     wrong=[(n_spaces * lam, "Node to node is half a wavelength.")],
                     working=[r"v = f\lambda", rf"\lambda = {ltx(lam)}\ \mathrm{{m}}", rf"{n_spaces} \times \frac{{\lambda}}{{2}} = {ltx(n_spaces*lam/2)}\ \mathrm{{m}}"])
    ex.choice("How are the maxima and minima produced?",
              "The reflected wave interferes with the incident wave, constructively at antinodes and destructively at nodes.",
              [("The plate absorbs some waves at regular positions.", "It reflects them."),
               ("The detector changes the wavelength.", "The wavelength is constant."),
               ("The microwaves slow down near the plate.", "Their speed is unchanged.")])
    d, D = pick(0.060, 0.075, 0.090), pick(0.60, 0.80, 1.0)
    ex.on(_INT).num(f"The plate is replaced by a metal sheet with two slits {d:g} m apart, with the detector moved along a "
                    f"line {D:g} m beyond them. Estimate the separation of neighbouring maxima.", sig(lam) * D / d, "m",
                    working=[r"\Delta x = \frac{\lambda D}{d}", rf"\Delta x = {ltx(sig(lam)*D/d)}\ \mathrm{{m}}"])
    ex.choice("What two conditions are needed for constructive interference at a maximum?",
              "The waves are coherent and meet in phase.",
              [("The waves are polarised and have equal amplitudes.", "Coherent and in phase."),
               ("The waves meet in phase and have different frequencies.", "They must be coherent."),
               ("The waves are coherent and meet exactly out of phase.", "That gives destructive interference.")])
    ex.on(_POL).choice("The transmitter produces plane-polarised microwaves. What happens to the detector reading as the "
                       "receiver aerial is rotated through 90° from the position of maximum signal?",
                       "It decreases gradually to a minimum (zero).",
                       [("It stays the same.", "The waves are polarised."),
                        ("It suddenly falls to zero at 45°.", "The change is gradual."),
                        ("It increases.", "It starts at a maximum.")])
    return ex.build(f"A microwave transmitter of frequency {fmt(f)} Hz points at a flat metal plate. A small detector is "
                    f"moved between them.")


def _laser_slits(level=LEVEL):
    ex = _exam()
    nm, d = pick(532, 633, 650), pick(0.20e-3, 0.25e-3, 0.40e-3)
    D = uni(2.0, 4.0)
    lam = nm * 1e-9
    dx = lam * D / d
    ex.on(_INT).num("Calculate the separation of the bright fringes.", dx, "m",
                    wrong=[(dx / 2, "Young's slits: Δx = λD/d.")],
                    working=[r"\Delta x = \frac{\lambda D}{d}", rf"\Delta x = {ltx(dx)}\ \mathrm{{m}}"])
    ex.choice("How are the bright fringes produced?",
              "The slits act as coherent sources, and the light meets in phase at the bright fringes.",
              [("Each slit produces light of a different colour.", "The light is from one laser."),
               ("The light travels furthest to the bright fringes.", "It is the path difference that matters."),
               ("The slits act as lenses.", "They are sources of interfering light.")])
    ex.choice("The screen is moved further away. What is one advantage when finding the wavelength?",
              "The fringe separation is larger, so its percentage uncertainty is smaller.",
              [("The scale reading uncertainty of the ruler is smaller.", "The ruler is unchanged."),
               ("The fringes become brighter.", "They become dimmer."),
               ("The wavelength becomes longer.", "The wavelength is unchanged.")])
    ex.on(_QU).num("Calculate the energy of one photon of the laser light.", H * C / lam, "J",
                   wrong=[(H * C / nm, "Convert nm to m.")],
                   working=[r"v = f\lambda \qquad E = hf", rf"E = {ltx(H*C/lam)}\ \mathrm{{J}}"])
    ex.num("Calculate the momentum of one photon.", H / lam, "kg m s⁻¹",
           working=[r"\lambda = \frac{h}{p}", rf"p = {ltx(H/lam)}\ \mathrm{{kg\,m\,s^{{-1}}}}"])
    return ex.build(f"Light from a laser of wavelength {nm} nm passes through two slits {fmt(d, 2)} m apart. Fringes are "
                    f"seen on a screen {D:g} m away.")


def _wedge(level=LEVEL):
    ex = _exam()
    nm, length = pick(589, 633, 509), uni(0.060, 0.110, 3)
    d = sig(uni(4.0, 9.0) * 1e-5, 2)
    lam = nm * 1e-9
    N = pick(10, 20)
    dx = sig(lam * length / (2 * d))
    total = sig(N * dx)
    ans = lam * length / (2 * total / N)
    ex.on(_INT).num("Determine the thickness of the wire.", ans, "m",
                    wrong=[(lam * length / (2 * total), f"Divide the measured distance by {N}."), (2 * ans, "Δx = λl/2d.")],
                    working=[rf"\Delta x = {ltx(total/N)}\ \mathrm{{m}}", r"\Delta x = \frac{\lambda l}{2d}", rf"d = {ltx(ans)}\ \mathrm{{m}}"],
                    scaffold=[("What is the fringe separation?", total / N, "m")])
    ex.choice("Is this interference by division of amplitude or of wavefront?",
              "Amplitude: light is partly reflected from each side of the air wedge.",
              [("Wavefront: the wire splits the wavefront in two.", "The two rays come from partial reflection."),
               ("Wavefront: the slides act as two slits.", "There are no slits."),
               ("Neither: it is diffraction by the wire.", "It is thin-film interference.")])
    ex.choice("The wire is heated and its diameter increases. What happens to the fringe separation, and why?",
              "It decreases, because d increases while λ and l are constant, and Δx = λl/2d.",
              [("It increases, because the wedge is thicker.", "Δx is inversely proportional to d."),
               ("It is unchanged, because the light is the same.", "Δx depends on d."),
               ("It decreases, because the wavelength decreases.", "The wavelength is unchanged.")])
    ex.on(_POL).num("Calculate Brewster's angle for the glass of the slides (refractive index 1.51).",
                    math.degrees(math.atan(1.51)), "°",
                    wrong=[(math.degrees(math.asin(1 / 1.51)), "That is the critical angle.")],
                    working=[r"n = \tan i_P", rf"i_P = {ltx(math.degrees(math.atan(1.51)))}^\circ"])
    return ex.build(f"Two glass slides {length:g} m long are in contact at one end and separated by a thin wire at the "
                    f"other. In light of wavelength {nm} nm, {N} fringe spacings measure {fmt(total)} m.")


def _coated_lens(level=LEVEL):
    ex = _exam()
    nm = pick(520, 550, 580)
    d = nm * 1e-9 / (4 * 1.38)
    ex.on(_INT).choice("What is the phase change when light in air reflects from the coating?",
                       "π rad, as the coating is more dense than air.",
                       [("Zero.", "Reflection from a more dense medium gives π."), ("2π rad.", "It is π."), ("π/2 rad.", "It is π.")])
    ex.num("Calculate the minimum thickness of coating that makes the lens non-reflecting at this wavelength.", d, "m",
           wrong=[(nm * 1e-9 / (4 * 1.51), "Use the index of the coating."), (nm * 1e-9 / (2 * 1.38), "d = λ/4n.")],
           working=[r"d = \frac{\lambda}{4n}", rf"d = {ltx(d)}\ \mathrm{{m}}"])
    ex.num("Calculate the optical path difference between the ray reflected from the top of the coating and the ray "
           "reflected from the glass, at this thickness.", 2 * 1.38 * sig(d), "m",
           wrong=[(1.38 * sig(d), "The second ray crosses the coating twice."), (2 * sig(d), "opd = n × gpd.")],
           working=[r"opd = n \times gpd", rf"opd = 1.38 \times 2d = {ltx(2*1.38*sig(d))}\ \mathrm{{m}}"])
    ex.choice("Why does the coating make the lens non-reflecting at this wavelength?",
              "The two reflected rays interfere destructively.",
              [("The coating absorbs that wavelength.", "It is an interference effect."),
               ("The two reflected rays interfere constructively.", "That would increase reflection."),
               ("The coating stops light entering the lens.", "More light is transmitted.")])
    ex.on(_POL).num("Light in air reflects from the coating (refractive index 1.38). Calculate the angle of incidence for "
                    "which the reflected light is plane-polarised.", math.degrees(math.atan(1.38)), "°",
                    working=[r"n = \tan i_P", rf"i_P = {ltx(math.degrees(math.atan(1.38)))}^\circ"])
    return ex.build(f"A glass lens (refractive index 1.51) is coated with magnesium fluoride (refractive index 1.38). It "
                    f"is designed to be non-reflecting for light of wavelength {nm} nm.")


def _reflection(level=LEVEL):
    ex = _exam()
    ip = pick(51.8, 53.1, 55.2, 56.5)
    n = math.tan(math.radians(ip))
    ex.on(_POL).num("Calculate the refractive index of the block.", n, "",
                    wrong=[(1 / math.sin(math.radians(ip)), "n = tan iP.")],
                    working=[r"n = \tan i_P", rf"n = {ltx(n)}"])
    ex.num("Determine the angle of refraction at this angle of incidence.", 90 - ip, "°",
           wrong=[(ip, "The reflected and refracted rays are at 90°.")],
           working=[rf"90 - {ip:g} = {ltx(90-ip)}^\circ"])
    ex.choice("What is meant by plane-polarised light?",
              "The electric field vector oscillates in one plane only.",
              [("The light travels in one plane only.", "'Travels' is not accepted."),
               ("The electric field vector oscillates in one direction only.", "Say plane."),
               ("The light has one frequency only.", "That is monochromatic.")])
    ex.choice("How could a student confirm that the reflected light is plane-polarised?",
              "Look at it through a rotating analyser: the intensity changes, falling to zero.",
              [("Pass it through a polariser and then rotate an analyser.", "The first polariser would polarise any light."),
               ("Look at it through a stationary analyser.", "It must be rotated."),
               ("Measure its wavelength with a grating.", "Wavelength does not show polarisation.")])
    return ex.build(f"Unpolarised light reflects from a transparent block in air. The reflected light is completely "
                    f"plane-polarised when the angle of incidence is {ip:g}°.")


SCENARIOS = {
    "Electron Beam": _electron_beam,
    "Hydrogen Atom": _hydrogen_atom,
    "Solar Wind Proton": _aurora,
    "Cosmic Ray": _cosmic_ray,
    "Mass on a Spring": _spring,
    "Loudspeaker": _speaker,
    "Travelling and Stationary Waves": _travelling,
    "Microwaves": _microwaves,
    "Laser and Double Slit": _laser_slits,
    "Air Wedge": _wedge,
    "Coated Lens": _coated_lens,
    "Polarisation by Reflection": _reflection,
}
