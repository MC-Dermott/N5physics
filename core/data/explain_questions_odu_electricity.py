"""Real SQA Higher Physics explain and justify questions for the Our Dynamic Universe and Electricity units.
Same source, format and conventions as explain_questions.py, which merges these in.

Key: (unit, topic) — the strings used in question_factory.py.
"""
from core.data.explain_questions_common import _q

ODU1 = "Our Dynamic Universe (Part 1)"
ODU2 = "Our Dynamic Universe (Part 2)"
ELEC = "Electricity"


# ════════════════════════════ Our Dynamic Universe (Part 1) ════════════════════════════

_TOWING = [
    _q("2023 Paper 2 Q2(c)",
       "A bike tows a trailer along a road. As their speed increases, the frictional forces on both the bike and "
       "the trailer increase. The acceleration of the bike and trailer stays the same.",
       "State whether the tension in the tow bar increases, decreases, or stays the same. Justify your answer.",
       ["The tension increases.",
        "The friction on the trailer increases but the unbalanced (resultant) force on the trailer stays the "
        "same."],
       avoid="It must be clear that it is the unbalanced force that stays constant."),
]

_VECTORS = [
    _q("Specimen Paper 2 Q3(b)",
       "A gymnast hangs from two wooden rings, each suspended by a rope. At first the ropes are vertical. The "
       "gymnast then stretches out their arms until each rope makes an angle of 10° with the vertical.",
       "Explain why the tension in each rope increases as the gymnast stretches out their arms.",
       ["The tension in each rope now has a horizontal component.",
        "The vertical component of the tension in the rope is unchanged."],
       avoid="Talk about the forces on (the tension in) the ropes, not the force applied by the gymnast."),
    _q("2019 Paper 2 Q2(c)",
       "A student abseils down the side of a building, supported by a rope. As the student goes down, the angle "
       "the rope makes with the building decreases.",
       "State whether the tension in the rope increases, decreases or stays the same. Justify your answer.",
       ["The tension decreases.",
        "As the angle decreases, the cosine of the angle increases (or: the horizontal component of the force "
        "decreases)."],
       gate=True),
    _q("2026 Paper 2 Q4(c)",
       "A boat is raised out of the water by four cables attached to an electric motor. As the boat is raised, "
       "the angle between each cable and the horizontal decreases.",
       "State whether the tension in each cable decreases, stays the same, or increases. You must justify your "
       "answer.",
       ["The tension increases.",
        "The sine of the angle decreases, so a larger tension is needed for the same vertical component (or: the "
        "horizontal component of the tension increases)."],
       avoid="Do not say or imply that the vertical component decreases."),
    _q("2026 Paper 2 Q2(c)",
       "A trolley is released from rest at a point P on a straight slope and its acceleration is measured. It is "
       "then released from rest from a position further down the same slope.",
       "State whether the acceleration of the trolley is greater than, the same as, or less than the "
       "acceleration when released from P. You must justify your answer.",
       ["The acceleration is the same.",
        "The unbalanced force on the trolley is unchanged (the angle of the slope is the same)."]),
]

_MOMENTUM = [
    _q("2025 Paper 2 Q2(a)",
       "Two vehicles on a linear air track are used to investigate collisions.",
       "State the law of conservation of momentum.",
       ["The total momentum before a collision is equal to the total momentum after it, in the absence of "
        "external forces (in an isolated system)."],
       avoid="Abbreviations such as 'TMB = TMA' are not accepted."),
    _q("2018 Paper 2 Q3(c)",
       "A student measures the masses of two vehicles and their velocities before and after they collide on an "
       "air track.",
       "Explain how the student would determine whether the collision was elastic or inelastic.",
       ["Calculate the total kinetic energy before the collision and the total kinetic energy after it.",
        "If they are equal the collision is elastic; if the total kinetic energy before is greater than after, "
        "it is inelastic."],
       avoid="You must say 'total' (both objects) kinetic energy.", gate=True),
    _q("2020 Paper 2 Q3(c)",
       "A ball is dropped onto a spectacle lens to test its strength. The collision between the ball and the "
       "lens is inelastic.",
       "Explain what is meant by an inelastic collision.",
       ["One in which kinetic energy is lost (the total kinetic energy before is greater than after)."],
       avoid="'Kinetic energy is not conserved' or 'Ek before does not equal Ek after' are not accepted."),
    _q("2020 Paper 2 Q3(d)",
       "A ball is dropped onto a spectacle lens to test its strength. The test is repeated with a second lens "
       "made of a softer material.",
       "Explain why this would make the lens less likely to break.",
       ["The softer material increases the time of contact.",
        "This decreases the (average / maximum) force on the lens."]),
    _q("2023 Paper 2 Q3(d)",
       "One safety feature on Formula 1 racetracks is the use of tyre walls on bends, to protect the driver if "
       "their car leaves the track.",
       "Explain how tyre walls protect the driver.",
       ["During a collision the tyre wall increases the time of contact between the car and the wall.",
        "This reduces the force on the driver."]),
    _q("2024 Paper 2 Q1(b)(ii)",
       "A foam ball with a circuit board inside it is swung along a rope between two students. It collides with "
       "the handles held by one student and comes to rest.",
       "Explain how the foam ball protects the circuit board during the collision.",
       ["The foam increases the time of contact.",
        "So the force on the circuit board is smaller."]),
]

_ENERGY = [
    _q("Specimen Paper 2 Q1(c)(ii)",
       "A motorcycle accelerates from rest along a straight, level road with a constant acceleration. As its "
       "speed increases, the driving force has to change.",
       "Explain why the driving force must be increased with time to maintain a constant acceleration.",
       ["The frictional force (air resistance) increases as the speed increases.",
        "So the driving force must increase to keep the unbalanced force constant."]),
    _q("2020 Paper 2 Q15(a)",
       "A student measures the terminal velocity of ball bearings falling through glycerol in a long tube.",
       "Explain, in terms of the forces acting on the ball bearing, why it reaches its terminal velocity.",
       ["The frictional force (drag) on the ball bearing increases as its speed increases.",
        "Eventually the frictional force and the weight become balanced."]),
    _q("2018 Paper 2 Q2(a)(iii)",
       "A drone is lowering a package on a cable at a steady speed. While the package is being lowered the cable "
       "breaks. The upward force produced by the drone stays the same.",
       "Describe the vertical motion of the drone immediately after the cable breaks. Justify your answer.",
       ["The drone accelerates upwards.",
        "The upward force is now greater than the weight (the weight supported has decreased, so the forces are "
        "no longer balanced)."],
       gate=True),
]


# ════════════════════════════ Our Dynamic Universe (Part 2) ════════════════════════════

_PROJECTILE = [
    _q("2015 Paper 2 Q1(b)",
       "An athlete throws a shot. A graph shows that, as the angle of projection increases, the speed at which "
       "the athlete can release the shot decreases.",
       "Using information from the graph, explain the effect of increasing the angle of projection on the "
       "kinetic energy of the shot at release.",
       ["The kinetic energy is less.",
        "As the angle increases, the speed of release decreases."],
       gate=True),
    _q("2018 Paper 2 Q1(b)",
       "A student throws a sponge at a teacher, at an angle above the horizontal. The student says: 'If the sponge "
       "is thrown with a higher speed at the same angle from the same height then it would take a shorter time to "
       "hit the teacher in the same place.'",
       "Explain why the student's statement is incorrect.",
       ["The initial horizontal (and vertical) speed is greater.",
        "So the sponge is higher than before when it has travelled the same horizontal distance (it would not hit "
        "the teacher in the same place)."],
       gate=True),
    _q("2020 Paper 2 Q1(d)",
       "A skier leaves a ramp at an angle above the horizontal and lands on ground that is lower than the end of "
       "the ramp. Air resistance can be ignored.",
       "State how the kinetic energy of the skier just before landing compares to their kinetic energy as they "
       "leave the ramp. Justify your answer.",
       ["It is greater.",
        "The skier has a greater speed as they land (potential energy has been converted to kinetic energy)."]),
    _q("2022 Paper 2 Q1(b)",
       "A competitor kicks a football at 17.0 m/s at 24.0° to the horizontal, and it hits the crossbar at its "
       "maximum height. Next time they kick it at the same angle with a smaller initial speed.",
       "State whether the football hits the crossbar, passes over it, or passes under it. Justify your answer.",
       ["It passes under the crossbar.",
        "The ball has a smaller initial vertical component of velocity (so it never reaches the same height)."]),
    _q("2026 Paper 2 Q1(b)",
       "An athlete throws a shot from a certain height. A second, taller athlete releases the shot from a greater "
       "height, with the same initial speed and angle.",
       "State what effect, if any, this has on the horizontal distance travelled by the shot. You must justify "
       "your answer.",
       ["The horizontal distance increases.",
        "Because the time of flight is greater."]),
]

_GRAVITATION = [
    _q("2019 Paper 2 Q4(d)",
       "A satellite orbits the Earth. A second satellite has a quarter of the mass of the first, and its distance "
       "from the centre of the Earth is half that of the first.",
       "State how the gravitational force between the second satellite and the Earth compares with that between "
       "the first satellite and the Earth. Justify your answer.",
       ["The force is the same.",
        "A quarter of the mass quarters the force.",
        "Half the distance (from the centre of the Earth) makes the force four times bigger."],
       avoid="You can also justify the last two marks by calculation.", gate=True),
]

_RELATIVITY = [
    _q("2016 Paper 2 Q4(b)(i)",
       "A plane travels at 0.8c relative to a stationary observer. It emits a beam of light towards the observer.",
       "State the speed of the emitted light as measured by the observer. Justify your answer.",
       ["3 × 10⁸ m/s (c).",
        "The speed of light is the same for all observers (in all inertial frames of reference)."],
       gate=True),
    _q("2016 Paper 2 Q4(b)(iii)",
       "A plane travels at a relativistic speed. A student on board says that the clocks on the plane will run "
       "slower.",
       "Explain whether or not this statement is correct.",
       ["The judgement is tied to a frame of reference: correct for a stationary observer, who measures time "
        "dilation; incorrect for people on the plane, who are in the same frame as the clock (or: it cannot be "
        "decided because no frame of reference is given)."],
       avoid="Your answer must state or clearly imply a frame of reference."),
    _q("Specimen Paper 2 Q4(c)",
       "Muons are produced high in the Earth's atmosphere and travel towards the ground at 0.995c. Their mean "
       "lifetime, measured in their own frame of reference, is very short.",
       "Explain why a greater number of muons are detected on the surface of the Earth than would be expected if "
       "relativistic effects were not taken into account.",
       ["In the Earth's frame of reference the mean lifetime of a muon is greater (or: in the muon's frame of "
        "reference the distance to travel is shorter)."],
       avoid="You must name the frame of reference."),
    _q("2022 Paper 2 Q6(d)",
       "Pions travel at 0.95c between two detectors 30.0 m apart in a laboratory. Pions have a mean lifetime of "
       "26 ns in their own frame of reference.",
       "Explain why a greater number of pions are detected at the second detector than would be expected if "
       "relativistic effects are not taken into account.",
       ["For a stationary observer the mean lifetime of the pion is greater than 26 ns (or: in the pion's frame "
        "of reference the distance is shorter than 30.0 m)."],
       avoid="You must name the frame of reference."),
    _q("2025 Paper 2 Q4(c)",
       "A student says: 'Train drivers who travel at speeds of 80 m/s over large distances will have to reset "
       "their watches frequently, as they spend so many hours travelling at high speeds.'",
       "State whether the student is correct. Justify your answer.",
       ["The student is incorrect.",
        "The train does not travel at a relativistic speed (80 m/s is far less than c, so time dilation is "
        "negligible)."]),
]

_UNIVERSE = [
    _q("2015 Paper 2 Q4(b)(i)",
       "The position of one hydrogen line in a visible spectrum is shown for the Sun, a nearby galaxy and a "
       "distant galaxy. For the nearby galaxy the line is at a longer wavelength than for the Sun, and for the "
       "distant galaxy it is longer still.",
       "Explain why the position of the line is different in each of the spectra.",
       ["The light from the galaxies is redshifted (its wavelength has increased).",
        "Because the galaxies are moving away from the Sun (further galaxies have a greater recessional "
        "velocity)."],
       avoid="Saying the light is blueshifted, or 'becomes red', gets 0 marks."),
    _q("2016 Paper 2 Q5(a)(ii)",
       "Students model the expanding Universe with knots tied along a piece of elastic cord. When the cord is "
       "stretched steadily, knots further from a chosen knot move away from it at a greater average speed.",
       "Explain why this model is a good simulation of the expansion of the Universe.",
       ["More distant galaxies are moving away at a greater (recessional) velocity."],
       avoid="References to planets or stars alone get 0 marks."),
    _q("2017 Paper 2 Q1(b)(ii)",
       "A train sounds its horn as it approaches, passes under and then moves away from a bridge, where a person "
       "is standing.",
       "Explain why the frequency of the sound heard by the person decreases as the train passes under the bridge "
       "and then moves away.",
       ["Fewer wavefronts reach the person each second (the wavefronts are further apart / the wavelength is "
        "longer)."],
       avoid="Do not imply that the frequency or wavelength produced by the horn itself changes."),
    _q("Specimen Paper 2 Q5(a)(i)",
       "Spectrum P shows lines in the hydrogen emission spectrum from a laboratory source. Spectrum Q shows the "
       "same lines from a distant galaxy, all at longer wavelengths.",
       "Explain why the lines on spectrum Q are in a different position to those on spectrum P.",
       ["The galaxy is moving away from the Earth.",
        "So the observed wavelengths have increased (the observed frequencies are lower / the light is "
        "redshifted)."]),
    _q("2020 Paper 2 Q2(b)(ii)",
       "A train driver sounds a whistle as the train approaches students standing on a bridge. A student suggests "
       "that a passenger sitting in the carriage behind the engine will hear a lower frequency than the frequency "
       "emitted by the whistle.",
       "State whether the student is correct. You must justify your answer.",
       ["The student is not correct.",
        "The passenger is travelling at the same velocity as the whistle (the distance between them is "
        "constant)."]),
    _q("2020 Paper 2 Q6(c)",
       "The light from the majority of galaxies in the Universe is redshifted.",
       "Explain how this evidence supports the Big Bang theory.",
       ["Redshift is evidence that the Universe is expanding (galaxies are moving away from each other).",
        "An expanding Universe is evidence supporting the Big Bang theory."]),
    _q("2022 Paper 2 Q5(a)",
       "A teacher swings a buzzer on a string in a horizontal circle. The buzzer makes a sound of constant "
       "frequency. Students stand to one side.",
       "Explain, in terms of wavefronts, why the frequency heard by the students is lower as the buzzer moves "
       "away from them than when it is moving towards them.",
       ["Moving away: the wavefronts are further apart (fewer wavefronts arrive each second).",
        "Moving towards: the wavefronts are closer together (more wavefronts arrive each second)."],
       avoid="You must refer to wavefronts, wavelengths or waves."),
    _q("2023 Paper 2 Q5(a)(ii)",
       "A police car with its siren on approaches a person standing at the side of the road, then passes at a "
       "constant speed.",
       "State whether the frequency heard as the police car moves away is greater than, the same as, or less than "
       "the frequency heard as it approached. You must justify your answer.",
       ["It is less.",
        "Fewer wavefronts arrive each second (the wavefronts are further apart / the wavelength is longer)."],
       avoid="Do not imply that the frequency or wavelength produced by the siren itself changes."),
    _q("2024 Paper 2 Q5(b)",
       "In a model of light from a star, students leave the 'star' at equal time intervals and walk at a steady "
       "speed towards an observer; each student is a wavefront. When the demonstration is repeated with the "
       "'star' moving, the students end up further apart than before.",
       "State whether the 'star' is moving towards or away from the observer. You must justify your answer.",
       ["The star is moving away from the observer.",
        "The observed wavelength has increased (fewer wavefronts pass the observer each second / the observed "
        "frequency has decreased)."],
       avoid="Do not imply that the frequency or wavelength emitted by the star itself changes."),
    _q("2024 Paper 2 Q5(c)(i)",
       "Redshift is one piece of evidence for the expanding Universe. Another is Olbers' paradox, also called the "
       "dark sky paradox.",
       "Explain how Olbers' paradox supports the concept of the expanding Universe.",
       ["State the paradox: if the Universe were static (infinite and unchanging), the night sky would be bright, "
        "but it is dark.",
        "In an expanding Universe the light from galaxies moving away is redshifted out of the visible range, or "
        "light from distant objects has not had time to reach us, so the sky is dark."]),
    _q("2025 Paper 2 Q2(d)(ii)",
       "A vehicle carrying a buzzer moves along an air track towards a microphone. The frequency detected by the "
       "microphone is greater than the frequency emitted by the buzzer.",
       "Explain, in terms of wavefronts, why the detected frequency is greater than the emitted frequency.",
       ["More wavefronts arrive at the microphone each second (the wavefronts ahead of the buzzer are closer "
        "together)."],
       avoid="You must refer to wavefronts or waves; do not imply the buzzer's own frequency changes."),
    _q("2025 Paper 2 Q5(b)(ii)",
       "Stars emit radiation with a range of wavelengths. One star, star 1, appears more red than the Sun.",
       "Explain why star 1 appears more red than the Sun.",
       ["It has a lower surface temperature (so its peak wavelength is longer than the Sun's)."]),
]


# ════════════════════════════ Electricity ════════════════════════════

_AC = [
    _q("2020 Paper 2 Q13(a)",
       "A student connects a signal generator, which provides an alternating current, to an oscilloscope.",
       "State what is meant by an alternating current.",
       ["A current that changes direction and (instantaneous) value with time."]),
    _q("2023 Paper 2 Q5(b)(ii)",
       "The emergency lights on a police car are red LEDs and blue LEDs connected to the same a.c. supply, with "
       "the red LEDs facing the opposite way round to the blue LEDs.",
       "Explain why the red LEDs and the blue LEDs do not light at the same time.",
       ["When the red LEDs are forward biased the blue LEDs are reverse biased (they are connected the opposite "
        "way round).",
        "LEDs only light when forward biased (they only conduct in one direction)."],
       avoid="'They are in different directions' is not enough on its own."),
    _q("2018 Paper 2 Q12(a)(iii)",
       "A signal generator is connected through an ammeter to a red LED and a green LED, in parallel and facing "
       "opposite ways. The frequency is low. The red LED is only lit when the ammeter reading is positive and the "
       "green LED only when it is negative.",
       "Explain these observations.",
       ["LEDs light (conduct) only when forward biased, in one direction.",
        "The current keeps changing direction, so each LED is forward biased in a different half of the cycle."],
       avoid="'Different direction' is not enough on its own."),
]

_CIRCUITS = [
    _q("2025 Paper 2 Q11(c)",
       "A resistor R is connected in series with a 1.8 kΩ resistor, an ammeter and an a.c. supply of negligible "
       "internal resistance. An oscilloscope is connected across R. Switch S, which is open, can connect a "
       "second 1.8 kΩ resistor in parallel with the first 1.8 kΩ resistor. Switch S is now closed.",
       "State whether the amplitude of the trace on the oscilloscope increases, stays the same, or decreases. "
       "You must justify your answer.",
       ["The amplitude increases.",
        "The total resistance of the circuit (the resistance of the parallel part) decreases.",
        "So the current in R increases and the voltage across R increases (the voltage across the parallel part "
        "decreases)."],
       avoid="'Voltage through' or 'current across' gets 0 marks."),
    _q("2015 Paper 2 Q10(a)(iii)",
       "A car battery of low internal resistance is connected to an electric motor, which needs a large current.",
       "Suggest why the connecting wires used in this circuit have a large diameter.",
       ["Thick wires have a low resistance, or this prevents them overheating (melting)."],
       avoid="'The motor needs a large current' or 'the wires will melt' are not enough on their own."),
]

_INTERNAL_RESISTANCE = [
    _q("2015 Paper 2 Q10(a)(i)",
       "A car battery has an e.m.f. of 12.8 V and an internal resistance.",
       "State what is meant by an e.m.f. of 12.8 V.",
       ["12.8 J of energy is supplied to each coulomb of charge passing through the battery."]),
    _q("2015 Paper 2 Q10(b)(iii)(B)",
       "A run-down car battery is connected to a battery charger of constant e.m.f. 15.0 V. The two e.m.f.s oppose "
       "each other. The charging current decreases as the battery charges.",
       "Explain why the charging current decreases as the battery charges.",
       ["The e.m.f. of the battery increases.",
        "So the difference between the two e.m.f.s decreases."]),
    _q("2016 Paper 2 Q12(a)(ii)",
       "A car battery with internal resistance is connected in series with an ammeter, a 4.8 Ω resistor and a "
       "lamp. A second identical lamp is in parallel with the first, with switch S in series with it. A voltmeter "
       "is across the lamps. Switch S, which was open, is now closed.",
       "State the effect this has on the reading on the voltmeter. Justify your answer.",
       ["The reading decreases.",
        "The total resistance decreases, so the current increases.",
        "The lost volts increase (so the terminal p.d. decreases)."],
       gate=True),
    _q("2019 Paper 2 Q12(a)(iii)",
       "A voltmeter is connected across a cell with internal resistance. A resistor and an open switch S are also "
       "connected to the cell. When S is closed the voltmeter reading falls.",
       "Explain why the reading on the voltmeter decreases when the switch is closed.",
       ["When the switch is closed there is a current in the circuit.",
        "So there is a voltage (lost volts) across the internal resistance."],
       avoid="'Lost volts' on its own is not enough; 'the current increases' on its own is not accepted."),
    _q("2020 Paper 2 Q14(c)",
       "Four identical cells, each with internal resistance, supply a motor and a variable resistor in series. A "
       "voltmeter is across the cells. The resistance of the variable resistor is now increased.",
       "State what happens to the reading on the voltmeter. Justify your answer.",
       ["The reading increases.",
        "The current is less.",
        "So the lost volts (Ir) decrease."],
       gate=True),
    _q("2022 Paper 2 Q12(d)",
       "A battery with internal resistance is connected to a variable resistor, with a voltmeter across the "
       "battery. The resistance of the variable resistor is decreased.",
       "Explain why the terminal potential difference of the battery decreases.",
       ["The current increases.",
        "So the lost volts increase (and the terminal p.d. decreases)."]),
    _q("2023 Paper 2 Q12(b)",
       "A 12 V battery with internal resistance first supplies a circuit in which two 16 Ω resistors in parallel "
       "are in series with a third. The circuit is then rearranged so that all three 16 Ω resistors are in "
       "series.",
       "State whether the power dissipated by the internal resistance is greater than, equal to, or less than "
       "before. You must justify your answer.",
       ["The power is less.",
        "The current decreases (the lost volts decrease) while the internal resistance stays the same."]),
]

_CAPACITORS = [
    _q("2015 Paper 2 Q11(c)(ii)",
       "A defibrillator discharges a capacitor through a patient. The patient's resistance stays the same during "
       "the discharge, and the current decreases with time.",
       "Explain why the current decreases with time.",
       ["The voltage (across the capacitor) decreases."]),
    _q("2016 Paper 2 Q13(c)",
       "A charged capacitor is discharged through a lamp, which stays lit for a short time. The 150 mF capacitor "
       "is replaced by one of 47 mF, charged from the same supply.",
       "State the effect this change has on the time the lamp stays lit. You must justify your answer.",
       ["The lamp stays lit for a shorter time.",
        "The smaller capacitance means less energy (less charge) is stored."],
       gate=True),
    _q("2017 Paper 2 Q13(b)",
       "An uncharged 220 µF capacitor charges from a 12 V battery through a 6800 Ω resistor. It is then "
       "discharged. Switch S₂ is closed, which connects a second 6800 Ω resistor in parallel with the first, and "
       "the capacitor is charged again.",
       "Explain why the time for the capacitor to fully charge is now less than before.",
       ["The total resistance of the circuit is less.",
        "So the initial charging current is greater."],
       avoid="'The current is greater' on its own is not enough for the second mark."),
    _q("2019 Paper 2 Q13(c)",
       "A 47 µF capacitor is charged from a supply through a resistor.",
       "Suggest an alteration the student could make to this circuit to increase the maximum energy stored by "
       "the capacitor.",
       ["Increase the supply voltage."],
       avoid="'Increase the voltage across the capacitor' on its own is not accepted."),
    _q("2025 Paper 2 Q12(b)(i)",
       "A student charges a capacitor from a 9.0 V supply through a variable resistor, adjusting the resistor to "
       "keep the charging current constant. The capacitor is initially uncharged.",
       "State whether the student should increase or decrease the resistance to keep the charging current "
       "constant. Justify your answer.",
       ["Decrease the resistance.",
        "As the capacitor charges, the voltage across R falls, so without this change the current would "
        "decrease."]),
    _q("2026 Paper 2 Q13(c)",
       "A capacitor takes 30 ms to charge fully through a resistor. It is discharged, the resistor is replaced by "
       "one of greater resistance, and it is charged again.",
       "State whether the time to charge fully is now greater than, equal to, or less than 30 ms. Justify your "
       "answer.",
       ["Greater than 30 ms.",
        "The initial (average) current is less."],
       avoid="'The current is less' on its own is not enough."),
]

_SEMICONDUCTORS = [
    _q("2016 Paper 2 Q12(b)(i)",
       "An LED is made from doped semiconductor material with a p-n junction. A voltage is applied so that it is "
       "forward biased and emits light.",
       "Using band theory, explain how the LED emits light.",
       ["Electrons move from the conduction band of the n-type towards the conduction band of the p-type.",
        "Electrons fall from the conduction band to the valence band.",
        "A photon is emitted when an electron falls."],
       avoid="Name the conduction and valence bands correctly. 'Holes and electrons recombine' with no band "
             "theory gets 0 marks."),
    _q("2018 Paper 2 Q11(c)",
       "A potato battery will light a red LED but not a blue LED, although both are forward biased. LEDs emit "
       "light when electrons fall from the conduction band into the valence band of the p-type.",
       "Explain, using band theory, why the blue LED will not operate with this battery.",
       ["The electrons do not gain enough energy to move into the conduction band of the p-type."]),
    _q("2019 Paper 2 Q14(b)",
       "The electrical conductivity of solids can be explained using band theory.",
       "Using band theory, explain why conduction can take place in a semiconductor at room temperature.",
       ["The band gap between the valence and conduction bands is small.",
        "Some electrons have enough energy to move from the valence band to the conduction band."],
       avoid="Write 'valence band', not 'valency band', and make the direction of movement clear."),
    _q("2022 Paper 2 Q3(d)(ii)",
       "A light gate contains a lamp and a photodiode. A photodiode is a p-n junction that produces a potential "
       "difference when photons of light are incident on it.",
       "Using band theory, explain how a potential difference is produced when photons are incident on the "
       "photodiode.",
       ["Electrons gain energy by absorbing photons.",
        "Electrons move from the valence band to the conduction band.",
        "Electrons move towards the n-type semiconductor (producing a potential difference)."],
       avoid="You must refer to the conduction and valence bands, named correctly, or you get 0 marks."),
    _q("2023 Paper 2 Q5(b)(iii)(B)",
       "Red LEDs and blue LEDs each emit a photon when an electron falls across the energy band gap.",
       "Explain, in terms of the energy band gaps, the difference between the photons emitted by the red LEDs and "
       "by the blue LEDs.",
       ["The band gap in a blue LED is greater.",
        "So photons of blue light have more energy (a higher frequency / shorter wavelength)."],
       avoid="With no mention of the band gap you get 0 marks."),
]

EXPLAIN_QUESTIONS_ODU_ELECTRICITY = {
    (ODU1, "Towing"): _TOWING,
    (ODU1, "Components of Vectors"): _VECTORS,
    (ODU1, "Momentum and Impulse"): _MOMENTUM,
    (ODU1, "Energy, Work and Power"): _ENERGY,
    (ODU2, "Projectile Motion"): _PROJECTILE,
    (ODU2, "Gravitation"): _GRAVITATION,
    (ODU2, "Special Relativity"): _RELATIVITY,
    (ODU2, "The Expanding Universe"): _UNIVERSE,
    (ELEC, "Monitoring and Measuring AC"): _AC,
    (ELEC, "Current, Potential Difference, Power and Resistance"): _CIRCUITS,
    (ELEC, "Electrical Sources and Internal Resistance"): _INTERNAL_RESISTANCE,
    (ELEC, "Capacitors"): _CAPACITORS,
    (ELEC, "Semiconductors and p-n Junctions"): _SEMICONDUCTORS,
}
