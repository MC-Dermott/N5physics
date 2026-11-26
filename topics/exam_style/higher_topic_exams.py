"""Higher Particles and Waves — single-topic exam-style questions, each modelled on an SQA Paper 2 question
(named above each one), with new numbers each time. They sit alongside the single-topic scenarios in
higher_particles_waves.py, and join each unit's exam-style pool.
"""
import math
import random

from topics.exam_style.base import fmt, ltx, pick, sig
from topics.exam_style.higher_particles_waves import C, E, H, ME, MP, _ex

_QUARK_CHARGE = r"Quark charges: u, c, t $+\tfrac23 e$; d, s, b $-\tfrac13 e$. An antiquark has the opposite charge."


# ════════════════ Forces: protons between plates (2022 Paper 2 Q7) ════════════════

def proton_plates(level="Higher"):
    ex = _ex(level).on("Forces on Charged Particles")
    u, kv = pick(2.4e5, 3.8e5, 5.2e5), pick(1.5, 2.2, 2.8, 3.6)
    V = kv * 1e3
    Ek0, W = 0.5 * MP * u * u, E * V
    ex.num("Calculate the kinetic energy of a proton as it passes plate A.", Ek0, "J",
           wrong=[(MP * u * u, "Ek = ½mv² — don't leave out the ½."), (0.5 * MP * u, "Square the speed."),
                  (0.5 * ME * u * u, "Use the mass of a PROTON.")],
           working=[rf"E_k = \tfrac12 mv^2 = \tfrac12 \times 1.673\times10^{{-27}} \times ({ltx(u)})^2 = {ltx(Ek0)}\ \text{{J}}"])
    ex.num("Calculate the work done on the proton by the electric field as it moves from plate A to plate B.", W, "J",
           wrong=[(E * kv, "Convert kV to V."), (V / E, "W = QV — multiply by the charge.")],
           working=[rf"W = QV = 1.60\times10^{{-19}} \times {ltx(V)} = {ltx(W)}\ \text{{J}}"])
    v = math.sqrt(2 * (Ek0 + W) / MP)
    ex.num("Calculate the speed of the proton at plate B.", v, "m/s",
           wrong=[(math.sqrt(2 * W / MP), "Add the work done to the kinetic energy the proton already had."),
                  (u + math.sqrt(2 * W / MP), "Add the energies, not the speeds.")],
           working=[rf"E_{{k,B}} = {ltx(Ek0)} + {ltx(W)} = {ltx(Ek0 + W)}\ \text{{J}}",
                    rf"v = \sqrt{{\frac{{2E_k}}{{m}}}} = {ltx(v)}\ \text{{m/s}}"],
           scaffold=[("What is the kinetic energy at plate B, in J?", Ek0 + W, "J")])
    ex.choice("Why are the protons accelerated by the electric field?",
              "Protons are positively charged, so they experience a force in the electric field.",
              [("Protons have mass, so the electric field exerts a force on them.", "The force is there because they are charged."),
               ("Protons are neutral, so nothing opposes their motion.", "Protons are positively charged."),
               ("The electric field produces a magnetic force on stationary protons.", "A charge in an electric field feels an electric force.")])
    ex.choice("The distance between the plates is doubled and the p.d. is unchanged. What is the effect on the speed of a proton at plate B?",
              "No effect: the work done (QV), and so the gain in kinetic energy, is the same.",
              [("It increases: the proton accelerates over a longer distance.", "The field is weaker over the longer distance; W = QV is unchanged."),
               ("It decreases: the electric field is weaker.", "The weaker force acts over a longer distance, so the work done is the same."),
               ("It doubles: twice as much work is done.", "W = QV does not depend on the distance.")])
    return ex.build(f"Protons are accelerated by an electric field between metal plates A and B in a vacuum. The p.d. "
                    f"between the plates is {kv} kV and the protons pass plate A at {fmt(u, 2)} m/s. "
                    "(e = 1.60 × 10⁻¹⁹ C, mₚ = 1.673 × 10⁻²⁷ kg)")


# ════════════════ Standard Model: pentaquark (2019 Paper 2 Q7) ════════════════

def pentaquark(level="Higher"):
    ex = _ex(level).on("Standard Model")
    quarks, charge = random.choice([("u u d c c̄", 1), ("u d d c c̄", 0), ("u d s c c̄", 0), ("u u s c c̄", 1),
                                    ("u u d d s̄", 1)])
    label = {1: "+1e", 0: "0", -1: "−1e", 2: "+2e"}
    ex.choice(f"One pentaquark contains the quarks {quarks} (a bar means an antiquark). Determine its total charge.",
              label[charge], [(label[q], "Add the five quark charges, reversing the sign for the antiquark.")
                              for q in (1, 0, -1, 2) if q != charge], working=[{"type": "text", "content": _QUARK_CHARGE}])
    ex.choice("Quarks and leptons are fundamental particles. What is meant by a fundamental particle?",
              "A particle that is not made up of other particles.",
              [("A particle that is found in every atom.", "Many fundamental particles are not found in atoms."),
               ("A particle with no charge.", "Quarks and electrons are charged."),
               ("A particle made of exactly three quarks.", "That is a baryon, which is not fundamental.")])
    ex.choice("What name is given to the group of matter particles that contains the quarks and the leptons?", "Fermions",
              [("Bosons", "Bosons are the force-mediating particles."), ("Hadrons", "Hadrons are made of quarks."),
               ("Baryons", "Baryons are hadrons made of three quarks.")])
    ex.choice("Particle X is made of one charm quark and one anticharm quark. What type of particle is X?", "A meson",
              [("A baryon", "A baryon is made of three quarks."), ("A lepton", "Leptons are not made of quarks."),
               ("A boson that mediates the strong force", "The gluon mediates the strong force.")])
    ex.choice("Which force holds the quarks together, and which particle mediates it?", "The strong force, mediated by gluons.",
              [("The weak force, mediated by W and Z bosons.", "The weak force is involved in beta decay."),
               ("The electromagnetic force, mediated by photons.", "It is the strong force that binds quarks."),
               ("The gravitational force, mediated by photons.", "Gravity is far too weak, and photons mediate electromagnetism.")])
    return ex.build("Scientists have discovered short-lived particles called pentaquarks, which contain five quarks.\n\n"
                    + _QUARK_CHARGE)


# ════════════════ Standard Model: sigma particles and forces (2017 Paper 2 Q7, specimen Q7) ════════════════

def sigma_particles(level="Higher"):
    ex = _ex(level).on("Standard Model")
    name, quarks, total = random.choice([("sigma plus", "up, up, strange", "+1e"), ("sigma minus", "down, down, strange", "−1e")])
    others = "two up quarks, each of charge +⅔e" if "up" in quarks else "two down quarks, each of charge −⅓e"
    ex.choice(f"The {name} particle (charge {total}) contains {others}, and one strange quark. Determine the charge on the strange quark.",
              "−⅓e", [("+⅓e", "The three charges must add to the particle's charge — check the sign."),
                      ("+⅔e", "Subtract the other two quarks' charges from the total."),
                      ("−⅔e", "Subtract the other two quarks' charges from the total.")])
    ex.choice("Why are the proton and the neutron not fundamental particles?", "They are made up of other particles (quarks).",
              [("They are found in the nucleus.", "Where a particle is found doesn't decide this."),
               ("They have mass.", "Fundamental particles can have mass."),
               ("They can be deflected by fields.", "The neutron is not deflected, and this doesn't decide it.")])
    strong, other_name, other = pick((38, "weak nuclear force", 25), (38, "electromagnetic force", 36))
    ex.num(f"The relative strength of the strong force is 10^{strong} and of the {other_name} is 10^{other}. "
           f"By how many orders of magnitude is the strong force greater than the {other_name}?", strong - other, "",
           wrong=[(strong + other, "Subtract the powers of ten.")],
           working=[rf"\frac{{10^{{{strong}}}}}{{10^{{{other}}}}} = 10^{{{strong - other}}}"])
    ex.choice("The gluon has a range of about 10⁻¹⁵ m for its force. Why can it not be the force-mediating particle for gravity?",
              "The strong force has a short range, but gravity has an infinite range.",
              [("The strong force is much weaker than gravity.", "The strong force is far stronger; the issue is range."),
               ("Gluons only exist inside electrons.", "Gluons act between quarks."),
               ("Gravity has a short range, but the strong force has an infinite range.", "It is the other way round.")])
    ex.choice("A neutron decays: n → p + e⁻ + antineutrino. What is this type of decay, and which force is responsible?",
              "Beta decay, caused by the weak force.",
              [("Alpha decay, caused by the strong force.", "An electron is emitted, so this is beta decay."),
               ("Beta decay, caused by the electromagnetic force.", "Beta decay is caused by the weak force."),
               ("Gamma decay, caused by the weak force.", "No gamma ray is shown; an electron is emitted.")])
    return ex.build(f"Sigma particles are made up of three quarks. The {name} particle is made of the quarks {quarks}.")


# ════════════════ Photoelectric: UV on a metal plate (2024 Paper 2 Q9, 2025 Q8) ════════════════

def uv_plate(level="Higher"):
    ex = _ex(level).on("The Photoelectric Effect")
    metal, W0 = random.choice([("zinc", 5.81e-19), ("metal X", 5.89e-19), ("metal Y", 6.10e-19)])
    f = pick(1.20e15, 1.25e15, 1.30e15, 1.45e15)
    Eph = H * f
    ex.num("Calculate the energy of one photon of the ultraviolet radiation.", Eph, "J",
           wrong=[(H / f, "E = hf — multiply.")], working=[rf"E = hf = 6.63\times10^{{-34}} \times {ltx(f)} = {ltx(Eph)}\ \text{{J}}"])
    Ek = sig(Eph) - W0
    ex.num("Calculate the maximum kinetic energy of an electron emitted from the plate.", Ek, "J",
           wrong=[(sig(Eph) + W0, "Ek = hf − hf₀: subtract the work function."), (sig(Eph), "Subtract the work function.")],
           working=[rf"E_k = hf - hf_0 = {ltx(Eph)} - {ltx(W0)} = {ltx(Ek)}\ \text{{J}}"])
    v = math.sqrt(2 * sig(Ek) / ME)
    ex.num("Calculate the maximum speed of an emitted electron.", v, "m/s",
           wrong=[(math.sqrt(sig(Ek) / ME), "v = √(2Ek/m).")],
           working=[rf"v = \sqrt{{\frac{{2E_k}}{{m_e}}}} = {ltx(v)}\ \text{{m/s}}"])
    ex.choice("Why does the photoelectric effect support the particle model of light?",
              "Light arrives as photons with a fixed amount of energy, and each photon can free only one electron.",
              [("Light diffracts as it passes the wire mesh.", "Diffraction is evidence for waves."),
               ("A brighter light always gives faster electrons.", "Irradiance does not change the maximum kinetic energy."),
               ("Any frequency of light frees electrons if you wait long enough.", "Below the threshold frequency none are emitted.")])
    closer = random.random() < 0.5
    ex.choice(f"The lamp is moved {'closer to' if closer else 'further from'} the plate. What happens to the current and to the maximum kinetic energy of the electrons?",
              f"The current {'increases' if closer else 'decreases'}; the maximum kinetic energy is unchanged.",
              [(f"The current {'increases' if closer else 'decreases'}; the maximum kinetic energy {'increases' if closer else 'decreases'}.",
                "Each photon still has energy hf, so the maximum Ek is unchanged."),
               ("The current is unchanged; the maximum kinetic energy is unchanged.", "The number of photons reaching the plate each second changes."),
               (f"The current is unchanged; the maximum kinetic energy {'increases' if closer else 'decreases'}.", "Irradiance changes the number of photons per second, not their energy.")])
    return ex.build(f"Ultraviolet radiation of frequency {fmt(f)} Hz is incident on a plate made of {metal} (work function "
                    f"{fmt(W0)} J) in a vacuum. A positive wire mesh in front of the plate collects the electrons, and "
                    "a current is measured. (h = 6.63 × 10⁻³⁴ J s, mₑ = 9.11 × 10⁻³¹ kg)")


# ════════════════ Inverse square law: lamp data (2023 Paper 2 Q8) ════════════════

def lamp_data(level="Higher"):
    ex = _ex(level).on("Inverse Square Law")
    k = pick(5.68, 7.20, 9.00, 12.6)
    distances = [0.200, 0.300, 0.400, 0.500]
    table = "| Distance d (m) | " + " | ".join(f"{d:.3f}" for d in distances) + " |\n|---|---|---|---|---|\n" + \
            "| Irradiance I (W m⁻²) | " + " | ".join(f"{sig(k / d ** 2):g}" for d in distances) + " |"
    ex.choice("Using all of the data, which relationship between I and d is correct?", "I × d² is constant, so I ∝ 1/d².",
              [("I × d is constant, so I ∝ 1/d.", "Calculate I × d for each pair: it changes."),
               ("I ÷ d is constant, so I ∝ d.", "I falls as d increases."),
               ("I ÷ d² is constant, so I ∝ d².", "I falls as d increases.")],
              working=[rf"I d^2 = {ltx(k)}\ \text{{for every pair of readings}}"])
    d = pick(0.600, 0.750, 0.800, 1.20)
    ex.num(f"Calculate the irradiance at a distance of {d:g} m from the lamp.", k / d ** 2, "W/m²",
           wrong=[(k / d, "Divide by d², not d."), (k * d ** 2, "I = k ÷ d².")],
           working=[rf"I = \frac{{k}}{{d^2}} = \frac{{{ltx(k)}}}{{{d:g}^2}} = {ltx(k / d ** 2)}\ \text{{W m}}^{{-2}}"])
    I = pick(2.00, 4.00, 25.0, 50.0)
    ex.num(f"At what distance from the lamp is the irradiance {I:g} W m⁻²?", math.sqrt(k / I), "m",
           wrong=[(k / I, "That is d² — take the square root.")],
           working=[rf"d = \sqrt{{\frac{{k}}{{I}}}} = {ltx(math.sqrt(k / I))}\ \text{{m}}"])
    ex.choice("Why does the irradiance decrease as the distance from a point source increases?",
              "The same power is spread over a larger area.",
              [("The photons lose energy as they travel.", "Photon energy depends only on frequency."),
               ("The power of the source decreases.", "The source's power is unchanged."),
               ("The light travels more slowly further away.", "The speed of light in air doesn't change.")])
    ex.choice("Which change would make this experiment unsuitable for showing the inverse square law?",
              "Replacing the small lamp with a laser.",
              [("Darkening the room.", "That improves the experiment."), ("Taking readings at more distances.", "That improves the experiment."),
               ("Using a smaller lamp.", "A smaller lamp is closer to a point source.")])
    return ex.build("A student measures the irradiance of light at different distances from a small lamp in a darkened "
                    "room.\n\n" + table)


# ════════════════ Inverse square law: parallel beam and point source (2022 Paper 2 Q8(a)) ════════════════

def beam_spot(level="Higher"):
    ex = _ex(level).on("Inverse Square Law")
    r_mm, I = pick(12, 15, 18, 20), pick(11.0, 17.0, 23.0)
    r = r_mm * 1e-3
    P = I * math.pi * r * r
    ex.num("Calculate the power of the beam of light.", P, "W",
           wrong=[(I * math.pi * r_mm ** 2, "Convert mm to m."), (I / (math.pi * r * r), "P = I × A."),
                  (I * 2 * math.pi * r, "Use the AREA of the spot, πr².")],
           working=[rf"A = \pi r^2 = \pi \times ({ltx(r)})^2 = {ltx(math.pi * r * r)}\ \text{{m}}^2",
                    rf"P = IA = {I:g} \times {ltx(math.pi * r * r)} = {ltx(P)}\ \text{{W}}"],
           scaffold=[("What is the area of the spot, in m²?", math.pi * r * r, "m²")])
    ex.choice("The screen is moved further away. The spot stays the same size. Why can this set-up not be used to investigate the inverse square law?",
              "The beam does not spread out, so it is not behaving as a point source and the irradiance doesn't change.",
              [("The lamp only gives out one colour.", "The colour doesn't matter."),
               ("The irradiance falls too quickly to measure.", "With the same power and area, the irradiance is unchanged."),
               ("The inverse square law only works for sunlight.", "It applies to any point source.")])
    d1, I1, n = pick(0.40, 0.50, 0.80), pick(12.0, 18.0, 36.0), pick(2, 3, 4)
    d2 = d1 * n
    ex.num(f"The collimator is removed, leaving a lamp that acts as a point source. The irradiance {d1:g} m from it is "
           f"{I1:g} W m⁻². Calculate the irradiance {fmt(d2)} m from it.", I1 / n ** 2, "W/m²",
           wrong=[(I1 / n, "Square the ratio of the distances."), (I1 * n ** 2, "Irradiance decreases further away.")],
           working=[rf"I_2 = \frac{{I_1 d_1^2}}{{d_2^2}} = \frac{{{I1:g} \times {d1:g}^2}}{{{ltx(d2)}^2}} = {ltx(I1 / n ** 2)}\ \text{{W m}}^{{-2}}"])
    ex.choice("What is meant by irradiance?", "The power per unit area incident on a surface.",
              [("The energy of each photon hitting a surface.", "That is E = hf."),
               ("The total power given out by a source.", "Irradiance is power per unit AREA."),
               ("The number of photons given out each second.", "Irradiance is power per unit area.")])
    return ex.build(f"A lamp and a collimator produce a parallel beam of light. It makes a circular spot of radius "
                    f"{r_mm} mm on a screen, where the irradiance is {I:g} W m⁻².")


# ════════════════ Interference: laser and grating (2018 Paper 2 Q8) ════════════════

def laser_grating(level="Higher"):
    ex = _ex(level).on("Interference")
    lam_nm, N, m = pick(532, 633, 650), pick(250, 300), pick(2, 3)
    lam, d = lam_nm * 1e-9, 1e-3 / N
    ex.choice("In terms of waves, how is a bright spot produced on the screen?", "Waves meet in phase.",
              [("Waves meet 180° out of phase.", "That gives a minimum."), ("Photons collide and release energy.", "Answer in terms of waves."),
               ("The grating focuses the light to a point.", "A maximum is due to waves meeting in phase.")])
    ex.num("Calculate the separation of the slits on the grating.", d, "m",
           wrong=[(N, "d is the distance between slits: 1 ÷ (lines per metre)."), (1 / N, "The lines are per millimetre — convert to metres.")],
           working=[rf"d = \frac{{1 \times 10^{{-3}}}}{{{N}}} = {ltx(d)}\ \text{{m}}"])
    th = math.degrees(math.asin(m * lam / d))
    ordinal = {2: "second", 3: "third"}[m]
    ex.num(f"Calculate the angle between the central maximum and the {ordinal} order maximum, in degrees.", th, "",
           wrong=[(math.degrees(math.asin(lam / d)), f"For the {ordinal} order, m = {m}."), (m * lam / d, "That is sin θ — find the angle.")],
           working=[r"d\sin\theta = m\lambda", rf"\sin\theta = \frac{{{m} \times {ltx(lam)}}}{{{ltx(d)}}}", rf"\theta = {ltx(th)}^\circ"])
    N2 = pick(500, 600)
    ex.choice(f"The grating is replaced by one with {N2} lines per millimetre. What happens to the pattern, and why?",
              "The spots are further apart, because the slit separation d is smaller.",
              [("The spots are closer together, because the slit separation d is smaller.", "From sin θ = mλ/d, a smaller d gives a larger θ."),
               ("The spots are closer together, because the slit separation d is larger.", "More lines per mm means a smaller d."),
               ("The pattern is unchanged, because the wavelength is unchanged.", "θ depends on d as well as λ.")])
    ex.choice("The laser light is coherent. What is meant by coherent?",
              "The waves have a constant phase relationship (and the same frequency, wavelength and speed).",
              [("The waves are always in phase.", "'In phase' is not enough: the phase difference must be constant."),
               ("The waves have the same amplitude.", "Coherence is about phase, not amplitude."),
               ("The waves all travel in the same direction.", "Coherence is about a constant phase relationship.")])
    return ex.build(f"A student shines laser light of wavelength {lam_nm} nm onto a grating with {N} lines per "
                    "millimetre. A pattern of bright spots is seen on a screen.")


# ════════════════ Interference: two sources (2016 Q9, 2022 Q10, 2024 Q10) ════════════════

def two_loudspeakers(level="Higher"):
    ex = _ex(level).on("Interference")
    f = pick(850, 1360, 1700)
    lam = 340 / f
    ex.num("Calculate the wavelength of the sound.", lam, "m",
           wrong=[(f / 340, "λ = v ÷ f."), (C / f, "Use the speed of SOUND.")],
           working=[rf"\lambda = \frac{{v}}{{f}} = \frac{{340}}{{{f}}} = {ltx(lam)}\ \text{{m}}"])
    m, far = pick(2, 3), pick(4.00, 5.00, 6.00)
    near = far - m * lam
    ordinal = {2: "second", 3: "third"}[m]
    ex.num(f"Point P is the {ordinal} order maximum from the centre. It is {far:.2f} m from loudspeaker 1 and closer "
           "to loudspeaker 2. Calculate the distance from loudspeaker 2 to P.", near, "m",
           wrong=[(far + m * lam, "P is closer to loudspeaker 2, so subtract the path difference."),
                  (far - lam, f"For the {ordinal} order, path difference = {m}λ."),
                  (far - (m + 0.5) * lam, "A maximum has a path difference of mλ.")],
           working=[rf"\text{{path difference}} = m\lambda = {m} \times {ltx(lam)} = {ltx(m * lam)}\ \text{{m}}",
                    rf"\text{{distance}} = {far:.2f} - {ltx(m * lam)} = {ltx(near)}\ \text{{m}}"])
    k = pick(1, 2)
    diff = (k + 0.5) * lam
    ex.choice(f"At point Q the path difference from the two loudspeakers is {fmt(diff)} m. What is detected at Q?",
              "A minimum: the path difference is (m + ½)λ, so the waves meet out of phase.",
              [("A maximum: the path difference is a whole number of wavelengths.", "Divide the path difference by λ."),
               ("A maximum: the waves meet in phase.", "Divide the path difference by λ: it is not a whole number."),
               ("Nothing can be predicted from the path difference.", "The path difference decides the interference.")],
              working=[rf"\frac{{{ltx(diff)}}}{{{ltx(lam)}}} = {k + 0.5}"])
    ex.choice("One loudspeaker is disconnected while the microphone is at Q. What happens to the amplitude of the sound detected?",
              "It increases, because destructive interference no longer takes place.",
              [("It decreases, because there is only half as much sound.", "At Q the two waves were cancelling."),
               ("It stays the same, because the path difference is unchanged.", "There is no longer a second wave to interfere."),
               ("It falls to zero.", "One loudspeaker is still producing sound.")])
    ex.choice("What does the pattern of maxima and minima show about sound?", "That sound behaves as a wave, because interference occurs.",
              [("That sound is made of photons.", "Interference is a wave property."),
               ("That sound can travel through a vacuum.", "Sound needs a medium."),
               ("That sound travels at the speed of light.", "The speed of sound in air is 340 m/s.")])
    return ex.build(f"Two loudspeakers are connected to the same signal generator, set to {f} Hz. A microphone moved in "
                    "front of them detects a series of maxima and minima. (speed of sound = 340 m/s)")


# ════════════════ Spectra: hydrogen energy levels (2023 Paper 2 Q10, 2024 Q11) ════════════════

_LEVELS = {0: -21.8e-19, 1: -5.45e-19, 2: -2.42e-19, 3: -1.36e-19, 4: -0.871e-19}
_LEVEL_TABLE = "| Level | E₄ | E₃ | E₂ | E₁ | E₀ |\n|---|---|---|---|---|---|\n" \
               "| Energy (× 10⁻¹⁹ J) | −0.871 | −1.36 | −2.42 | −5.45 | −21.8 |"


def hydrogen_levels(level="Higher"):
    ex = _ex(level).on("Spectra")
    top = pick(3, 4)
    lines = top * (top + 1) // 2
    ex.num(f"Considering only the levels E₀ to E{'₀₁₂₃₄'[top]}, how many different lines could be produced in the emission spectrum?",
           lines, "", wrong=[(top, "Electrons can fall between ANY pair of levels, not just to the next one."),
                             (top + 1, "That is the number of levels; count the possible downward transitions.")],
           working=[{"type": "text", "content": f"Count every pair of the {top + 1} levels: {lines}."}])
    hi, lo = random.choice([(2, 1), (3, 1), (4, 1)])
    dE = _LEVELS[hi] - _LEVELS[lo]
    sub = "₀₁₂₃₄"
    freq = dE / H
    ex.num(f"Calculate the frequency of the photon emitted when an electron moves from E{sub[hi]} to E{sub[lo]}.", freq, "Hz",
           wrong=[(abs(_LEVELS[hi]) / H, "Use the DIFFERENCE between the two energy levels."),
                  (abs(_LEVELS[hi] + _LEVELS[lo]) / H, "Subtract the energies — don't add them.")],
           working=[r"E_2 - E_1 = hf", rf"{ltx(dE)} = 6.63\times10^{{-34}} \times f", rf"f = {ltx(freq)}\ \text{{Hz}}"],
           scaffold=[("What is the energy of the photon, in J?", dE, "J")])
    lam = C / sig(freq)
    ex.num("Calculate the wavelength of this light.", lam, "m",
           wrong=[(sig(freq) / C, "λ = v ÷ f.")], working=[rf"\lambda = \frac{{v}}{{f}} = {ltx(lam)}\ \text{{m}}"])
    ex.choice("How is a line emission spectrum produced?",
              "Electrons fall to lower energy levels, emitting photons; different transitions give different frequencies.",
              [("Electrons absorb photons and move to higher energy levels.", "That is absorption."),
               ("Electrons leave the atom and give out all frequencies.", "Only particular frequencies are emitted."),
               ("A prism adds energy to some wavelengths.", "The lines come from electron transitions.")])
    ex.choice("One line in the spectrum is brighter than the others. Why?",
              "More electrons make that transition each second, so more of those photons are emitted each second.",
              [("Its photons each have more energy.", "Brightness here depends on the number of photons per second."),
               ("Its light has a higher frequency.", "Frequency sets the colour, not the brightness."),
               ("Its electrons fall from the highest level.", "What matters is how many electrons make the transition each second.")])
    return ex.build("Some of the energy levels of a hydrogen atom are shown. (h = 6.63 × 10⁻³⁴ J s)\n\n" + _LEVEL_TABLE)


# ════════════════ Spectra: dark lines in sunlight (2025 Paper 2 Q10) ════════════════

def sunlight_lines(level="Higher"):
    ex = _ex(level).on("Spectra")
    lam_nm, colour, hi = random.choice([(656, "red", 2), (486, "blue-green", 3), (434, "blue-violet", 4)])
    ex.choice("How are the dark lines in the spectrum of sunlight produced?",
              "Photons of particular frequencies are absorbed by gases in the Sun's outer layers.",
              [("Photons of particular frequencies are emitted by gases in the Sun's outer layers.", "Dark lines mean light is missing: it has been absorbed."),
               ("All frequencies are absorbed by the Earth's atmosphere in narrow bands of time.", "Only particular frequencies are absorbed, in the Sun's outer layers."),
               ("The Sun's core does not produce any light at all.", "The core's radiation passes through the outer layers, where some is absorbed.")])
    f = C / (lam_nm * 1e-9)
    ex.num(f"One dark line matches the {colour} line of hydrogen, at {lam_nm} nm. Calculate its frequency.", f, "Hz",
           wrong=[(C / lam_nm, "Convert nm to m."), (lam_nm * 1e-9 / C, "f = v ÷ λ.")],
           working=[rf"f = \frac{{v}}{{\lambda}} = \frac{{3.00\times10^8}}{{{lam_nm}\times10^{{-9}}}} = {ltx(f)}\ \text{{Hz}}"])
    En = H * sig(f)
    ex.num("Calculate the energy of a photon of this frequency.", En, "J",
           wrong=[(H / sig(f), "E = hf — multiply.")], working=[rf"E = hf = {ltx(En)}\ \text{{J}}"])
    names = {2: "From E₁ to E₂", 3: "From E₁ to E₃", 4: "From E₁ to E₄"}
    wrong = [(names[k], "Compare the photon energy with the difference between the two levels.") for k in names if k != hi]
    wrong.append((f"From E{'₀₁₂₃₄'[hi]} to E₁", "That direction EMITS a photon; this line is due to absorption."))
    ex.choice("Using the energy levels, which electron transition in hydrogen causes this dark line?", names[hi], wrong)
    return ex.build("Light from the Sun gives a continuous spectrum crossed by dark lines. Some energy levels of hydrogen "
                    "are shown. (h = 6.63 × 10⁻³⁴ J s)\n\n" + _LEVEL_TABLE)


# ════════════════ Refraction: prism (specimen Q12, 2026 Q10) ════════════════

def glass_prism(level="Higher"):
    ex = _ex(level).on("Refraction of Light")
    a1, n_true, lam_nm = pick(30.0, 40.0, 47.0, 50.0), pick(1.40, 1.46, 1.52, 1.60), 532
    a2 = round(math.degrees(math.asin(math.sin(math.radians(a1)) / n_true)), 1)
    n = math.sin(math.radians(a1)) / math.sin(math.radians(a2))
    ex.num("Calculate the refractive index of the glass for this light.", n, "",
           wrong=[(1 / n, "n = sin θ (in air) ÷ sin θ (in glass)."), (a1 / a2, "Use the sines of the angles.")],
           working=[rf"n = \frac{{\sin\theta_1}}{{\sin\theta_2}} = \frac{{\sin {a1:g}^\circ}}{{\sin {a2:g}^\circ}} = {ltx(n)}"])
    v = C / sig(n)
    ex.num("Calculate the speed of the light in the glass.", v, "m/s",
           wrong=[(C * sig(n), "Light is slower in glass: v = c ÷ n.")], working=[rf"v = \frac{{c}}{{n}} = {ltx(v)}\ \text{{m/s}}"])
    ex.num(f"The wavelength of the light in air is {lam_nm} nm. Calculate its wavelength in the glass, in nm.", lam_nm / sig(n), "nm",
           wrong=[(lam_nm * sig(n), "The wavelength gets shorter in glass: divide by n.")],
           working=[rf"\lambda_2 = \frac{{\lambda_1}}{{n}} = {ltx(lam_nm / sig(n))}\ \text{{nm}}"])
    ex.choice("What happens to the frequency of the light as it enters the glass?", "It stays the same.",
              [("It decreases.", "The speed and wavelength decrease; the frequency doesn't change."),
               ("It increases.", "The frequency doesn't change on refraction.")])
    ex.choice("The green laser is replaced by a red one at the same angle of incidence. Compared with the green light, what happens to the red light in the glass?",
              "It is refracted less, because the refractive index is smaller for its lower frequency.",
              [("It is refracted more, because the refractive index is greater for its lower frequency.", "A lower frequency has a smaller refractive index."),
               ("It follows the same path, because the glass is unchanged.", "The refractive index depends on frequency."),
               ("It is refracted less, because it has a higher frequency than green light.", "Red light has a LOWER frequency than green.")])
    return ex.build(f"A ray of green laser light in air enters a glass prism. The angle of incidence is {a1:g}° and the angle "
                    f"of refraction is {a2:g}°.")


# ════════════════ Refraction: gemstones (2019 Paper 2 Q11) ════════════════

def gemstone(level="Higher"):
    ex = _ex(level).on("Refraction of Light")
    name, n = random.choice([("diamond", 2.42), ("sapphire", 1.77), ("cubic zirconia", 2.15)])
    a1 = pick(30.0, 40.0, 49.0, 60.0)
    a2 = math.degrees(math.asin(math.sin(math.radians(a1)) / n))
    ex.num(f"Light in air hits the surface of the {name} at an angle of incidence of {a1:g}°. Calculate the angle of refraction, in degrees.", a2, "",
           wrong=[(a1 / n, "Use n = sin θ₁ ÷ sin θ₂, with the sines of the angles.")],
           working=[rf"\sin\theta_2 = \frac{{\sin {a1:g}^\circ}}{{{n}}}", rf"\theta_2 = {ltx(a2)}^\circ"])
    tc = math.degrees(math.asin(1 / n))
    ex.num(f"Calculate the critical angle for {name}, in degrees.", tc, "",
           wrong=[(1 / n, "That is sin θc — find the angle.")],
           working=[rf"\sin\theta_c = \frac{{1}}{{n}} = \frac{{1}}{{{n}}}", rf"\theta_c = {ltx(tc)}^\circ"])
    inside = round(tc + pick(5, 8, 12))
    ex.choice(f"Inside the {name}, light meets a face at an angle of incidence of {inside}°. What happens?",
              "It is totally internally reflected, because the angle is greater than the critical angle.",
              [("It refracts out into the air, because the angle is greater than the critical angle.", "Above the critical angle no light is refracted out."),
               ("It refracts out into the air, because the angle is less than the critical angle.", "Compare the angle with your critical angle."),
               ("It is absorbed by the face.", "It is totally internally reflected.")])
    ex.choice(f"A second material, with a refractive index greater than {n}, is cut to the same shape. Will it sparkle more or less, and why?",
              "More: its critical angle is smaller, so total internal reflection is more likely.",
              [("Less: its critical angle is smaller, so less light is reflected inside.", "A smaller critical angle makes total internal reflection MORE likely."),
               ("More: its critical angle is larger, so total internal reflection is more likely.", "A greater n gives a smaller critical angle."),
               ("The same: the shape is unchanged.", "The critical angle depends on the material.")])
    return ex.build(f"A cut {name} (refractive index {n}) sparkles because light is reflected inside it.")


TOPIC_SCENARIOS_PARTICLES = {
    "Protons Between Plates": proton_plates,
    "Pentaquark":             pentaquark,
    "Sigma Particles":        sigma_particles,
}

TOPIC_SCENARIOS_WAVES = {
    "Ultraviolet on a Plate": uv_plate,
    "Lamp Irradiance Data":   lamp_data,
    "Beam and Point Source":  beam_spot,
    "Laser and Grating":      laser_grating,
    "Two Loudspeakers":       two_loudspeakers,
    "Hydrogen Energy Levels": hydrogen_levels,
    "Lines in Sunlight":      sunlight_lines,
    "Glass Prism":            glass_prism,
    "Gemstone":               gemstone,
}
