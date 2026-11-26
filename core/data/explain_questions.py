"""Real SQA Higher Physics explain and justify questions, for pupils to answer in their own words and then
mark themselves against the marking instructions. The Particles and Waves questions are here; Our Dynamic
Universe and Electricity are in explain_questions_odu_electricity.py, and Advanced Higher is in
explain_questions_ah.py.

Source: the "Higher Physics Past Papers" compilation (Mr Davie / Mr White), September 2026 update,
2015-2026 and the specimen paper (SPQ). Question wording follows the papers; "context" describes in words
whatever the paper sets up or shows in a diagram. Marking points are condensed from the SQA marking
instructions, one entry per mark.

Key: (unit, topic) — the strings used in question_factory.py.
"""
from core.data.explain_questions_ah import AH_EXPLAIN
from core.data.explain_questions_common import _q
from core.data.explain_questions_odu_electricity import EXPLAIN_QUESTIONS_ODU_ELECTRICITY

_SAME_DIRECTION = ("To keep the force on the {p} in the same direction as it crosses each gap, so that it keeps "
                   "accelerating forwards (the electric field is always in the correct direction at each gap).")

_FORCES = [
    _q("2017 Paper 2 Q8(a)(ii)",
       "An X-ray machine contains a linear accelerator that accelerates electrons towards a metal target. The "
       "electrons are accelerated across the gaps between hollow metal tubes by an alternating supply.",
       "Explain why an alternating supply is used in the linear accelerator.",
       [_SAME_DIRECTION.format(p="electron")],
       avoid="'Same direction' must be clearly implied."),
    _q("Specimen Paper 2 Q6(b)(i)",
       "In a linear accelerator, protons are accelerated across the gaps between hollow metal tubes that are "
       "connected to an alternating supply.",
       "Explain why an alternating supply is used in the linear accelerator.",
       [_SAME_DIRECTION.format(p="proton")]),
    _q("Specimen Paper 2 Q6(b)(ii)",
       "In a linear accelerator, protons are accelerated across the gaps between hollow metal tubes. The tubes "
       "get longer along the accelerator.",
       "Suggest one reason why the lengths of the tubes increase along the accelerator.",
       ["As the protons speed up they travel further in the same time (so the alternating supply can keep a "
        "constant frequency)."]),
    _q("2018 Paper 2 Q6(b)",
       "Electrons are accelerated from a cathode to an anode in an evacuated tube, then travel on to a "
       "fluorescent screen that glows where they hit it. A metal cross in their path, connected to the positive "
       "terminal of the supply, stops the electrons that hit it, so its shadow is seen on the screen. The "
       "potential difference between the anode and the cathode is now increased.",
       "Suggest one change that is observed on the screen. You must justify your answer.",
       ["State a correct change: the screen glows more brightly (or the glowing circle is smaller, or the shadow "
        "of the cross is sharper).",
        "Justify it: the electrons gain more energy / move faster, or more electrons arrive each second (for a "
        "smaller circle or sharper shadow: the electrons are attracted more strongly to the cross)."],
       avoid="'The current increases' is not enough on its own.", gate=True),
    _q("2022 Paper 2 Q7(a)",
       "Protons are accelerated by an electric field between two metal plates, A (positive) and B (negative), "
       "in a vacuum.",
       "Explain why the protons are accelerated by the electric field.",
       ["Protons are (positively) charged.",
        "So they experience a force in the electric field."],
       avoid="Without saying protons are charged you can get at most 1 mark."),
    _q("2022 Paper 2 Q7(c)",
       "Protons are accelerated between two metal plates, A and B, in a vacuum. The distance between the plates "
       "is now doubled, with the potential difference unchanged. Another proton, with the same initial speed at "
       "plate A, is accelerated between the plates.",
       "State what effect, if any, this has on the speed of the proton at plate B. You must justify your answer.",
       ["There is no effect on the speed.",
        "The work done on the proton (W = QV), and so its gain in kinetic energy, is the same."],
       avoid="'The charge and p.d. are unchanged' is not enough on its own.", gate=True),
    _q("2023 Paper 2 Q7(b)(ii)",
       "A cyclotron accelerates protons. An alternating voltage is applied across the gap between its two "
       "D-shaped electrodes.",
       "Explain why an alternating voltage is used in the cyclotron.",
       ["To make sure the electric field (the force on the proton) is always in the correct direction each time "
        "it crosses the gap."],
       avoid="'To accelerate the protons in the same direction' is not accepted for a cyclotron — they move in "
             "a spiral."),
    _q("2026 Paper 2 Q6(d)",
       "A charged particle entering a region of uniform magnetic field is deflected.",
       "Explain why a neutron that enters the magnetic field would not be deflected.",
       ["A neutron has no charge (it is neutral).",
        "Only a moving charged particle experiences a force in a magnetic field."],
       avoid="Any mention of the neutron being charged gets 0 marks."),
]

_STANDARD_MODEL = [
    _q("2017 Paper 2 Q7(a)",
       "A diagram of the Standard Model shows: matter → atom → electron and nucleus → proton and neutron → quarks.",
       "Explain why the proton and the neutron are not fundamental particles.",
       ["They are composed of other particles (quarks), but fundamental particles are not."]),
    _q("2017 Paper 2 Q7(b)(i)",
       "A student makes this statement: 'All baryons are hadrons, but not all hadrons are baryons.'",
       "Explain why this statement is correct.",
       ["Baryons are hadrons made of three quarks.",
        "Other hadrons, mesons, are made of a quark–antiquark pair, so they are not baryons."]),
    _q("Specimen Paper 2 Q7(a)",
       "A diagram of the Standard Model shows the fundamental matter particles (leptons and quarks) and the "
       "force-mediating particles.",
       "Explain why particles such as leptons and quarks are known as fundamental particles.",
       ["They cannot be subdivided (they are not made of other particles)."]),
    _q("Specimen Paper 2 Q7(c)",
       "The gluon is associated with the strong force (range 10⁻¹⁵ m). The gravitational force has an infinite "
       "range.",
       "Explain why the gluon cannot be the force-mediating particle for the gravitational force.",
       ["The strong force, mediated by the gluon, has a short range.",
        "Gravity has an infinite range, so it needs a force-mediating particle whose force has infinite range."]),
    _q("2019 Paper 2 Q7(a)(i)",
       "Scientists have discovered a type of particle called a pentaquark. Quarks and leptons are fundamental "
       "particles.",
       "Explain what is meant by the term fundamental particle.",
       ["A particle that is not composed of other particles (it cannot be broken down any further)."]),
    _q("2025 Paper 2 Q6(c)(i)",
       "Quarks are fundamental particles that do not exist by themselves but make up other particles called "
       "hadrons.",
       "Explain what is meant by the term fundamental particle.",
       ["A particle that is not composed of other particles (it cannot be broken down any further)."]),
]

_MASS_TO_ENERGY = "(Some) mass is lost and converted into energy."
_MASS_AVOID = ("'Mass is lost' on its own gets 0 marks, as does 'mass defect'. Mass is converted to energy, "
               "not 'transferred'.")

_NUCLEAR = [
    _q("2016 Paper 2 Q8(a)",
       "In an experimental fusion reactor this reaction takes place: ²₁H + ³₁H → ⁴₂He + ¹₀n. The total mass of "
       "the products is less than the total mass of the reactants.",
       "Explain why energy is released in this reaction.",
       [_MASS_TO_ENERGY], avoid=_MASS_AVOID),
    _q("2016 Paper 2 Q8(c)",
       "In a fusion reactor, magnetic fields are used to contain the plasma.",
       "Explain why it is necessary to use a magnetic field to contain the plasma.",
       ["The plasma is at a very high temperature: if it touched the sides it would melt or damage the "
        "container, or it would cool down and the reaction would stop."]),
    _q("2017 Paper 2 Q9(b)(i)",
       "This fusion reaction takes place: ³₂He + ²₁H → ⁴₂He + ¹₁p.",
       "Explain why energy is released in this reaction.",
       [_MASS_TO_ENERGY], avoid=_MASS_AVOID),
    _q("Specimen Paper 2 Q8(c)",
       "In a fusion reaction hydrogen nuclei join to form helium. Fusion reactors are being developed that use "
       "this type of reaction as an energy source.",
       "Explain why this type of fusion reaction is hard to sustain in these reactors.",
       ["The particles involved in the fusion reaction must be at a very high temperature."]),
    _q("2025 Paper 2 Q6(a)(i)",
       "Americium-241 decays by alpha emission: ²⁴¹₉₅Am → ²³⁷₉₃Np + ⁴₂He.",
       "Explain why energy is released in this decay.",
       [_MASS_TO_ENERGY], avoid=_MASS_AVOID),
]

_INVERSE_SQUARE = [
    _q("2017 Paper 2 Q14(b)(ii)",
       "A lamp shines on a solar cell, which has a maximum power output for a particular irradiance of light. "
       "The lamp is now moved closer to the solar cell.",
       "Explain, in terms of photons, why the maximum output power from the solar cell increases.",
       ["A greater number of photons strike the solar cell each second."],
       avoid="Your answer must give a rate ('per second')."),
    _q("2022 Paper 2 Q8(a)(ii)",
       "A sodium lamp and a collimator produce a parallel beam of light that makes a spot on a screen. When the "
       "screen is moved further from the end of the collimator, the spot has the same radius as before.",
       "Explain why this experimental set-up is not suitable for investigating the inverse square law.",
       ["It is not a point source: the beam does not spread out (diverge), so the irradiance does not change "
        "with distance."],
       avoid="'The sodium lamp is not a point source' on its own gets 0 marks."),
    _q("2023 Paper 2 Q8(c)",
       "The irradiance of light from a point source is measured at different distances from the source.",
       "Explain why the irradiance decreases when the distance from a point source of light increases.",
       ["The area the light is spread over increases.",
        "The power stays the same (so the power per unit area, the irradiance, decreases)."],
       avoid="'The light spreads out' is not enough for 'the area increases'."),
]

_PHOTOELECTRIC = [
    _q("2018 Paper 2 Q7(b)(ii)",
       "Ultraviolet light shining on a metal plate causes photoemission. The irradiance of the light on the "
       "plate is reduced by moving the ultraviolet source further away.",
       "State what effect, if any, this has on the maximum kinetic energy of the photoelectrons. Justify your "
       "answer.",
       ["There is no change to the maximum kinetic energy.",
        "Irradiance does not affect the energy of each photon (E = hf is unchanged)."], gate=True),
    _q("2018 Paper 2 Q7(d)",
       "The photoelectric effect is investigated by shining ultraviolet light onto a metal plate.",
       "Explain why the photoelectric effect provides evidence for the particle nature of light.",
       ["Each photon has a fixed (discrete) amount of energy, or each photon removes one electron. (If light "
        "were only a wave, photoemission would happen at any frequency — it would just take longer.)"],
       avoid="Your answer must show that the energy comes in separate packets."),
    _q("Specimen Paper 2 Q10(b)(i)",
       "A graph of the maximum kinetic energy of electrons leaving a metal plate against the frequency of the "
       "incident radiation is a straight line that meets the frequency axis at f₀.",
       "Explain why no electrons leave the metal plate when the frequency of the incident radiation is below f₀.",
       ["Photons with a frequency below f₀ do not have enough energy to release electrons."]),
    _q("2020 Paper 2 Q8(a)",
       "A metal plate P is in a vacuum tube connected to an ammeter. When white light is incident on plate P the "
       "ammeter reads 0 A. When ultraviolet radiation is incident on plate P the reading is greater than 0 A.",
       "Explain why ultraviolet radiation produces a reading greater than 0 A on the ammeter, but white light "
       "does not.",
       ["The frequency of the UV is greater than the threshold frequency but that of white light is less (or: a "
        "UV photon has more energy than the work function but a white-light photon has less)."],
       avoid="You must refer to both the UV and the white light."),
    _q("2024 Paper 2 Q9(a)(ii)",
       "Ultraviolet radiation of frequency 1.25 × 10¹⁵ Hz is incident on a zinc plate (work function "
       "5.81 × 10⁻¹⁹ J) in a vacuum. A positive wire mesh is in front of the plate, and a current is detected.",
       "Explain why UV radiation with a frequency of 1.25 × 10¹⁵ Hz produces a current in this circuit.",
       ["The energy of each photon is greater than the work function (or the frequency is above the threshold "
        "frequency).",
        "The photoelectrons released move to the positive wire mesh, completing the circuit."], gate=True),
    _q("2024 Paper 2 Q9(b)",
       "UV radiation from a lamp is incident on a zinc plate and a current is produced, as photoelectrons travel "
       "to a positive wire mesh. The lamp is now moved closer.",
       "State whether the current in the circuit increases, decreases, or stays the same. You must justify your "
       "answer.",
       ["The current increases.",
        "More photons are incident on the zinc plate each second (so more photoelectrons are emitted each "
        "second)."], gate=True),
    _q("2025 Paper 2 Q8(a)",
       "Ultraviolet radiation incident on a clean metal plate causes electrons to be emitted: the "
       "photoelectric effect.",
       "Explain why the photoelectric effect provides evidence supporting the particle model of light.",
       ["Each photon has a fixed (discrete) amount of energy, or each photon removes one electron."]),
    _q("2025 Paper 2 Q8(b)(iii)",
       "Ultraviolet radiation causes electrons to be emitted from a metal plate. The ultraviolet lamp is now "
       "moved further from the plate, reducing the irradiance.",
       "State what effect, if any, this has on the maximum kinetic energy of an electron emitted from the metal "
       "plate. You must justify your answer.",
       ["There is no effect on the maximum kinetic energy.",
        "Each photon has the same energy as before (E = hf is unchanged)."], gate=True),
]

_MAXIMUM = "Waves meet in phase (crest to crest or trough to trough; or path difference = mλ)."
_MAXIMUM_AVOID = "'The waves join' or 'merge' is not accepted."
_WHITE_ZERO = "The path difference at the central maximum is zero for every wavelength (colour)."

_INTERFERENCE = [
    _q("2015 Paper 2 Q9(b)(ii)",
       "White light is incident on a grating. The second-order maximum for red light is at 19.0° to the central "
       "maximum.",
       "Explain why the angle to the second-order maximum for blue light is different to that for red light.",
       ["Different colours have different wavelengths.",
        "The grating equation d sin θ = mλ applies (equivalently, path difference = mλ).",
        "For the same m and d (the same order and grating), θ is different for a different λ."],
       avoid="Saying the colours 'diffract (or refract) by different amounts' is wrong physics: 0 marks."),
    _q("2016 Paper 2 Q9(b)",
       "Coherent microwaves pass through two gaps between metal plates. A detector moved across in front of the "
       "gaps finds a series of maxima and minima.",
       "Explain, in terms of waves, how a maximum is produced.",
       [_MAXIMUM], avoid=_MAXIMUM_AVOID),
    _q("2016 Paper 2 Q9(d)",
       "Microwaves pass through two gaps and a second-order maximum is detected. The distance separating the two "
       "gaps is now increased.",
       "State what happens to the path difference to the second-order maximum. Justify your answer.",
       ["The path difference stays the same (it is still 2λ).",
        "The wavelength has not changed."], gate=True),
    _q("2017 Paper 2 Q10(a)",
       "Laser light passes through a grating and a pattern of maxima is formed on a screen.",
       "Explain, in terms of waves, how a maximum is formed.",
       [_MAXIMUM], avoid=_MAXIMUM_AVOID),
    _q("2018 Paper 2 Q8(a)(i)",
       "Laser light of wavelength 630 nm is directed onto a grating and a pattern of bright spots is seen on a "
       "screen.",
       "Explain, in terms of waves, how bright spots are produced on the screen.",
       [_MAXIMUM], avoid=_MAXIMUM_AVOID),
    _q("2018 Paper 2 Q8(a)(iii)",
       "Laser light passes through a grating with 250 lines per millimetre. The grating is now replaced by one "
       "with 600 lines per millimetre.",
       "State the effect of this change on the pattern observed. Justify your answer.",
       ["The spots are further apart (θ is greater; fewer spots are seen).",
        "The slit separation d of the new grating is smaller."], gate=True),
    _q("Specimen Paper 2 Q11(a)",
       "A helium-neon laser beam is directed onto a double slit and a pattern of bright red fringes is seen on a "
       "screen.",
       "Explain, in terms of waves, why bright red fringes are produced.",
       ["Waves meet in phase (crest to crest or trough to trough)."]),
    _q("Specimen Paper 2 Q11(c)",
       "Red light from a helium-neon laser passes through a double slit, producing fringes on a screen. The "
       "laser is replaced by one emitting green light; nothing else changes.",
       "Explain the effect this change has on the separation of the fringes observed on the screen.",
       ["Green light has a shorter wavelength than red light.",
        "So the fringes are closer together."]),
    _q("2019 Paper 2 Q10(a)",
       "Red, green and blue laser beams are directed in turn at the same grating (slit separation "
       "3.3 × 10⁻⁶ m).",
       "State which colour of laser light would produce the smallest angle θ between the central maximum and "
       "the first-order maximum. Justify your answer.",
       ["Blue light.",
        "Blue light has the shortest wavelength.",
        "From d sin θ = mλ (same d and m), the smallest λ gives the smallest sin θ, so the smallest θ."],
       gate=True),
    _q("2019 Paper 2 Q10(b)(iii)",
       "The wavelength of laser light is found from the angle of the first-order maximum using a grating with "
       "slit separation 3.3 × 10⁻⁶ m. A student suggests that a grating with slit separation 5.0 × 10⁻⁶ m "
       "would give a more accurate value.",
       "Explain why this suggestion is incorrect.",
       ["With a larger d the maxima are closer together (θ is smaller).",
        "A smaller angle is harder to measure accurately (it has a greater percentage uncertainty)."]),
    _q("2020 Paper 2 Q5(b)(i)",
       "In an interferometer, coherent laser light is split into two beams. They travel along two arms, reflect "
       "from mirrors and meet to produce an interference pattern.",
       "Explain, in terms of waves, how a minimum is formed in the interference pattern.",
       ["Waves meet exactly (180°) out of phase (crest meets trough; or path difference = (m + ½)λ)."]),
    _q("2020 Paper 2 Q10(a)(iii)",
       "A technician finds the wavelength of laser light using a grating. The experiment is repeated measuring "
       "the angle to the third-order maximum instead of a lower order.",
       "Explain why this gives a more precise value for the wavelength of the light.",
       ["The percentage (fractional) uncertainty in the angle is smaller."],
       avoid="You must say percentage or fractional uncertainty, not just 'uncertainty'."),
    _q("2020 Paper 2 Q10(b)",
       "White light passes through a grating. There is a white central maximum with continuous spectra on each "
       "side.",
       "Explain, in terms of path difference, why the central maximum is white.",
       [_WHITE_ZERO], avoid="You must answer in terms of path difference."),
    _q("2022 Paper 2 Q10(b)",
       "Two loudspeakers connected to the same signal generator emit coherent sound waves. A sound level meter "
       "moved across in front of them detects a series of maxima.",
       "Explain, in terms of waves, how a maximum is produced.",
       [_MAXIMUM], avoid=_MAXIMUM_AVOID),
    _q("2024 Paper 2 Q10(c)",
       "Two loudspeakers connected to the same signal generator produce destructive interference at point P. "
       "One loudspeaker is now disconnected.",
       "State the effect this has on the amplitude of the sound detected at point P. Justify your answer.",
       ["The amplitude increases (it is louder).",
        "Destructive interference no longer takes place."]),
    _q("2025 Paper 2 Q9(a)",
       "Sunlight passes through a grating, giving a white central maximum with spectra on either side.",
       "Explain why the central maximum is white.",
       ["The path difference at the central maximum is zero for every wavelength.",
        "So there is constructive interference for every wavelength, and all the wavelengths combine to give "
        "white light."]),
    _q("2025 Paper 2 Q9(d)",
       "A student uses the first-order spectrum from a grating with 1000 lines per millimetre to find which "
       "wavelengths a sample absorbs, measuring one colour at a time. Another student suggests that a grating "
       "with 250 lines per millimetre would allow this to be done more accurately.",
       "Explain why the student's suggestion is incorrect.",
       ["The slit separation d of the new grating is greater.",
        "So the spectrum is narrower (the colours are closer together), making it harder to place the detector "
        "in one colour of light."],
       avoid="'Fewer lines per millimetre' is not accepted on its own for the first mark."),
    _q("2026 Paper 2 Q8(a)(i)",
       "White light is incident on a grating and maxima are formed on a screen.",
       "Explain, in terms of waves, how a maximum is formed.",
       [_MAXIMUM], avoid=_MAXIMUM_AVOID),
    _q("2026 Paper 2 Q8(a)(ii)",
       "White light is incident on a grating, giving a central maximum and spectra on each side.",
       "Explain, in terms of path difference, why the central maximum is white.",
       [_WHITE_ZERO], avoid="'The path difference is zero' on its own gets 0 marks."),
]

_ABSORPTION_POINTS = ["Photons of particular frequencies (energies / wavelengths) are absorbed",
                      "in the Sun's outer layers (the gases of its upper atmosphere)."]
_BRIGHTER_POINTS = ["For the brighter line, more electrons make that transition each second,",
                    "so more photons of that energy are emitted each second."]
_BRIGHTER_AVOID = ("A brighter line is not caused by photons of greater frequency or energy. 'More electrons "
                   "release more photons' on its own gets at most 1 mark.")

_SPECTRA = [
    _q("2015 Paper 2 Q4(a)",
       "Light from the Sun is used to produce a visible spectrum. A number of dark lines are seen in it.",
       "Explain how these dark lines in the spectrum of sunlight are produced.",
       _ABSORPTION_POINTS, avoid="'In the atmosphere' is too vague — say the Sun's atmosphere."),
    _q("2022 Paper 2 Q8(b)(iii)",
       "The spectrum of a sodium lamp has a yellow line at 589.0 nm that is brighter than another yellow line "
       "at 589.6 nm.",
       "Explain the student's observation that the line at 589.0 nm is brighter.",
       _BRIGHTER_POINTS, avoid=_BRIGHTER_AVOID),
    _q("2023 Paper 2 Q10(b)(i)",
       "A hydrogen discharge lamp produces a line emission spectrum with four lines in the visible region.",
       "Explain how a line emission spectrum is produced.",
       ["Electrons in excited states drop to lower energy levels, emitting photons.",
        "Different transitions produce different lines (photons of different frequencies)."],
       avoid="Describing absorption gets 0 marks."),
    _q("2023 Paper 2 Q10(b)(ii)",
       "In the line emission spectrum of hydrogen, some lines appear brighter than others.",
       "Explain why some of these lines appear brighter than others.",
       _BRIGHTER_POINTS, avoid=_BRIGHTER_AVOID),
    _q("2024 Paper 2 Q11(c)",
       "In the line emission spectrum of hydrogen, the red line is brighter than the others.",
       "Explain why the red emission line is brighter than the others.",
       _BRIGHTER_POINTS, avoid=_BRIGHTER_AVOID),
    _q("2025 Paper 2 Q10(a)",
       "Light from the Sun is a continuous spectrum containing dark lines.",
       "Explain how these dark lines in the spectrum of sunlight are produced.",
       _ABSORPTION_POINTS,
       avoid="'In the atmosphere' is too vague. 'Elements' or 'atoms' on their own are not accepted."),
]

_REFRACTION = [
    _q("2015 Paper 2 Q9(a)(i)",
       "A ray of white light is incident on a glass prism and a spectrum is produced.",
       "Explain why a spectrum is produced in the glass prism.",
       ["Different frequencies (colours) have different refractive indices in glass, so they are refracted "
        "through different angles."],
       avoid="'Bending' or 'different amounts' on their own are not accepted, and 'diffraction' gets 0 marks. "
             "Talk about frequency or colour."),
    _q("2019 Paper 2 Q11(c)",
       "A cut diamond sparkles because of total internal reflection. Moissanite has a greater refractive index "
       "than diamond. A piece of moissanite is made into the same shape as the diamond.",
       "State whether the moissanite sparkles more or less than the diamond. You must justify your answer.",
       ["It sparkles more.",
        "The critical angle for moissanite is smaller than for diamond.",
        "So total internal reflection is more likely in moissanite."], gate=True),
    _q("2020 Paper 2 Q12(c)",
       "Red light is refracted as it passes through a hollow prism filled with sugar solution. The experiment "
       "is repeated with green light entering at the same angle.",
       "Explain the difference in the path taken by the green light compared to the path taken by the red light.",
       ["Green light has a higher frequency than red light.",
        "So the refractive index is greater for green light, and it is refracted more (a smaller angle of "
        "refraction)."],
       avoid="Saying the angle of refraction is greater, or unchanged, gets 0 marks."),
    _q("2026 Paper 2 Q10(b)",
       "Green laser light is refracted by a prism and reaches point Q on a screen, one of a row of points P, Q, "
       "R, S and T in order of increasing deviation from the laser's original direction, labelled from T "
       "(most deviated) to P (least). R is deviated less than Q. The laser is replaced by one emitting red "
       "light; nothing else changes.",
       "State at which point red light would be observed on the screen. Justify your answer.",
       ["At point R (the red light is deviated less than the green).",
        "The refractive index of the prism is smaller for red light than for green light,",
        "because red light has a lower frequency."],
       avoid="Wavelength alone is not accepted for the last mark.", gate=True),
]

EXPLAIN_QUESTIONS = {
    ("Particles", "Forces on Charged Particles"): _FORCES,
    ("Particles", "Standard Model"): _STANDARD_MODEL,
    ("Particles", "Nuclear Reactions"): _NUCLEAR,
    ("Waves", "Inverse Square Law"): _INVERSE_SQUARE,
    ("Waves", "The Photoelectric Effect"): _PHOTOELECTRIC,
    ("Waves", "Interference"): _INTERFERENCE,
    ("Waves", "Spectra"): _SPECTRA,
    ("Waves", "Refraction of Light"): _REFRACTION,
    **EXPLAIN_QUESTIONS_ODU_ELECTRICITY,
}


def get_explain_questions(qualification, unit, topic):
    """The explain questions for a topic (Higher and Advanced Higher)."""
    if qualification == "Advanced Higher":
        return AH_EXPLAIN.get((unit, topic), [])
    if qualification != "Higher":
        return []
    return EXPLAIN_QUESTIONS.get((unit, topic), [])


def explain_score(question, ticked):
    """Marks for a self-marked answer. ticked: one bool per marking point."""
    if question["gate"] and not ticked[0]:
        return 0
    return sum(ticked)
