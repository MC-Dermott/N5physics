NOTES = {

    "speed_distance_time": """
## Speed, Distance and Time — $d = vt$

**Definition:** Speed is the distance travelled per unit of time.

**Key equation:**
$$d = vt$$

| Symbol | Quantity | Unit |
|---|---|---|
| d | Distance | m (metres) |
| v | Speed (or average speed $\\bar{v}$) | m/s |
| t | Time | s (seconds) |

**Rearrangements:**
$$v = \\frac{d}{t} \\qquad t = \\frac{d}{v}$$

**Unit conversions:**

| To convert | Multiply by |
|---|---|
| km → m | × 1000 |
| minutes → s | × 60 |
| hours → s | × 3600 |

**Worked Example:** A car travels at 15 m/s for 20 s. Calculate the distance travelled.
$$d = vt = 15 \\times 20 = 300\\ \\mathrm{m}$$

> **Important:** Always convert distance to metres and time to seconds before substituting.
""",

    "resistor_combinations": """
## Resistor Combinations

**Definition:** The total (equivalent) resistance of a combination of resistors is the single
resistance that would draw the same current for the same supply voltage.

**Series** (resistors in a single chain):
$$R_T = R_1 + R_2 + R_3$$

**Parallel** (resistors across the same two points):
$$\\frac{1}{R_T} = \\frac{1}{R_1} + \\frac{1}{R_2} + \\frac{1}{R_3}$$

For two resistors in parallel this simplifies to:
$$R_T = \\frac{R_1 \\times R_2}{R_1 + R_2}$$

| Symbol | Quantity | Unit |
|---|---|---|
| $R_T$ | Total (equivalent) resistance | Ω (Ohms) |
| $R_1, R_2, R_3$ | Individual resistances | Ω (Ohms) |

**Mixed circuits — work step by step:**
1. Identify the pair that is combined first (series or parallel)
2. Replace that pair with its equivalent resistance $R_{ab}$
3. Combine $R_{ab}$ with the remaining resistor using the appropriate formula

| Arrangement | Step 1 | Step 2 |
|---|---|---|
| $(R_1 + R_2) \\parallel R_3$ | $R_{12} = R_1 + R_2$ | $R_T = \\frac{R_{12} \\times R_3}{R_{12} + R_3}$ |
| $(R_1 \\parallel R_2) + R_3$ | $R_{12} = \\frac{R_1 R_2}{R_1 + R_2}$ | $R_T = R_{12} + R_3$ |

**Worked Example:** A 4 Ω resistor and a 12 Ω resistor are connected in parallel. Calculate the total resistance.
$$R_T = \\frac{R_1 \\times R_2}{R_1 + R_2} = \\frac{4 \\times 12}{4 + 12} = \\frac{48}{16} = 3\\ \\Omega$$

> **Important:** In parallel, the total resistance is always **less** than the smallest individual resistor.
""",

    "ohms_law": """
## Ohm's Law — $V = IR$

**Definitions:**
- Current is the rate of flow of electric charge per unit time.
- Voltage (potential difference) is the energy transferred per unit charge.
- Resistance is a measure of how strongly a component opposes the flow of current.

**Key equation:**
$$V = IR$$

| Symbol | Quantity | Unit |
|---|---|---|
| V | Voltage (potential difference) | V (Volts) |
| I | Current | A (Amperes) |
| R | Resistance | Ω (Ohms) |

**Rearrangements:**
$$I = \\frac{V}{R} \\qquad R = \\frac{V}{I}$$

**Prefix conversions:**

| Prefix | Symbol | Factor |
|---|---|---|
| milli | mA, mV | $\\times 10^{-3}$ |
| kilo | kΩ | $\\times 10^{3}$ |

**Worked Example:** A 6 Ω resistor has a current of 2 A flowing through it. Calculate the voltage across it.
$$V = IR = 2 \\times 6 = 12\\ \\mathrm{V}$$

> **Important:** Convert mA to A (÷ 1000) and kΩ to Ω (× 1000) before substituting.
""",

    "radiation_activity": """
## Activity — $A = \\frac{N}{t}$

**Definition:** Activity is the number of nuclear decays per unit time (per second).

**Key equation:**
$$A = \\frac{N}{t}$$

| Symbol | Quantity | Unit |
|---|---|---|
| A | Activity | Bq (Becquerels) |
| N | Number of nuclear decays | (none) |
| t | Time | s (seconds) |

**Rearrangements:**
$$N = At \\qquad t = \\frac{N}{A}$$

**Time conversions:**
$$1\\ \\text{minute} = 60\\ \\text{s} \\qquad 1\\ \\text{hour} = 3600\\ \\text{s}$$

**Worked Example:** A source undergoes 3000 nuclear decays in 60 s. Calculate its activity.
$$A = \\frac{N}{t} = \\frac{3000}{60} = 50\\ \\mathrm{Bq}$$

> **Important:** One Becquerel = one decay per second. Always convert time to seconds.
""",

    "instantaneous_speed_s3": """
## Instantaneous Speed — using a light gate

**Definitions:**
- **Average speed** is the total distance travelled divided by the total time taken — it tells you
  nothing about the speed at any one moment.
- **Instantaneous speed** is the speed of an object at one exact point/moment in time.

**Same equation as average speed, applied over a very short distance:**
$$v = \\frac{d}{t}$$

A light gate measures instantaneous speed by timing how long a small interrupt card (or the object
itself, e.g. a ball bearing) takes to block the beam. Because this width and time are so small, the
speed barely changes while it passes through — so $d \\div t$ over the *gate* width and *gate* time
gives a close approximation to the speed at that exact point.

| Symbol | Quantity | Unit |
|---|---|---|
| d | Card/object width (**convert to metres**) | m |
| t | Light gate blocking time | s |
| v | Instantaneous speed | m/s |

**Worked Example:** A 6.0 cm wide card blocks a light gate beam for 0.12 s.
$$v = \\frac{d}{t} = \\frac{0.06}{0.12} = 0.5\\ \\mathrm{m/s}$$

> **Important:** Never use the total release-to-gate distance/time to find the instantaneous speed —
> that only gives the *average* speed over the whole run. If the object is accelerating (e.g. rolling
> down a slope), the instantaneous speed at the gate will be different from the average speed. Always
> convert the card/object width from cm/mm to metres before dividing.
""",

    "acceleration_s3": """
## Acceleration — $a = \\frac{v - u}{t}$

**Definitions:**
- Acceleration is the change in speed of an object per second.
- A **positive** acceleration means the object is speeding up; a **negative** acceleration means
  it is slowing down (decelerating).

**Key equation:**
$$a = \\frac{v - u}{t}$$

| Symbol | Quantity | Unit |
|---|---|---|
| a | Acceleration | m/s² |
| u | Initial speed | m/s |
| v | Final speed | m/s |
| t | Time | s |

**Rearrangements:**
$$v - u = at \\qquad v = u + at \\qquad u = v - at$$

**Worked Example:** A car speeds up from 5 m/s to 20 m/s in 5 s. Calculate its acceleration.
$$a = \\frac{v - u}{t} = \\frac{20 - 5}{5} = 3\\ \\mathrm{m/s^2}$$

> **Important:** The change in speed is $v - u$. If the acceleration is negative, the final
> speed will be lower than the initial speed.
""",

    "dynamics_newton": """
## Newton's Second Law — F = ma

**Definitions:**
- Force is a push or pull, measured in Newtons, that can change an object's speed, direction of
  motion, or shape.
- Acceleration is the change in speed (velocity) per second.

**Key equation:**
$$F = ma$$

| Symbol | Quantity | Unit |
|---|---|---|
| F | Force (unbalanced/resultant) | N (Newtons) |
| m | Mass | kg (kilograms) |
| a | Acceleration | m/s² |

**Rearrangements:**
$$a = \\frac{F}{m} \\qquad m = \\frac{F}{a}$$

**Worked Example:** Calculate the force needed to accelerate an 8 kg object at 3 m/s².
$$F = ma = 8 \\times 3 = 24\\ \\mathrm{N}$$

> **Important:** Use the *resultant* (unbalanced) force — the net force after subtracting friction from driving force.
""",

    "dynamics_weight": """
## Weight — W = mg

**Definition:** Weight is the force of gravity acting on an object's mass.

**Key equation:**
$$W = mg$$

| Symbol | Quantity | Unit |
|---|---|---|
| W | Weight | N (Newtons) |
| m | Mass | kg (kilograms) |
| g | Gravitational field strength | N/kg |

**Rearrangements:**
$$m = \\frac{W}{g} \\qquad g = \\frac{W}{m}$$

**Worked Example:** Calculate the weight of a 5 kg object on Earth ($g = 9.8$ N/kg).
$$W = mg = 5 \\times 9.8 = 49\\ \\mathrm{N}$$

> **Important:** On Earth, $g = 9.81$ N/kg. Always check which planet/body you are on. Convert grams to kilograms before substituting ($\\div 1000$).
""",

    "energy_gpe": """
## Gravitational Potential Energy — $E_p = mgh$

**Definition:** Gravitational potential energy is the energy an object has because of its height
above a reference level (e.g. the ground).

**Key equation:**
$$E_p = mgh$$

| Symbol | Quantity | Unit |
|---|---|---|
| $E_p$ | Gravitational potential energy | J (Joules) |
| m | Mass | kg |
| g | Gravitational field strength | N/kg |
| h | Height | m |

**Rearrangements:**
$$m = \\frac{E_p}{gh} \\qquad h = \\frac{E_p}{mg}$$

**Worked Example:** A 2 kg object is raised 10 m ($g = 9.8$ N/kg). Calculate the gain in gravitational potential energy.
$$E_p = mgh = 2 \\times 9.8 \\times 10 = 196\\ \\mathrm{J}$$

> **Important:** Convert grams to kg ($\\div 1000$). Use $g = 9.8$ or $10$ N/kg as given.
""",

    "energy_ke": """
## Kinetic Energy — $E_k = \\frac{1}{2}mv^2$

**Definition:** Kinetic energy is the energy an object has because of its motion.

**Key equation:**
$$E_k = \\frac{1}{2}mv^2$$

| Symbol | Quantity | Unit |
|---|---|---|
| $E_k$ | Kinetic energy | J (Joules) |
| m | Mass | kg |
| v | Speed/velocity | m/s |

**Rearrangements:**
$$m = \\frac{2E_k}{v^2} \\qquad v = \\sqrt{\\frac{2E_k}{m}}$$

**Worked Example:** A 3 kg ball moves at 4 m/s. Calculate its kinetic energy.
$$E_k = \\frac{1}{2}mv^2 = \\frac{1}{2} \\times 3 \\times 4^2 = 24\\ \\mathrm{J}$$

> **Important:** Don't forget the $\\frac{1}{2}$ factor. Square root when finding $v$.
""",

    "energy_work": """
## Work Done — $E_W = Fd$

**Definition:** Work done is the energy transferred when a force moves an object through a
distance.

**Key equation:**
$$E_W = Fd$$

| Symbol | Quantity | Unit |
|---|---|---|
| $E_W$ | Work done (energy transferred) | J (Joules) |
| F | Force | N (Newtons) |
| d | Distance moved in direction of force | m |

**Rearrangements:**
$$F = \\frac{E_W}{d} \\qquad d = \\frac{E_W}{F}$$

**Worked Example:** A 50 N force pushes an object 4 m in the direction of the force. Calculate the work done.
$$E_W = Fd = 50 \\times 4 = 200\\ \\mathrm{J}$$

> **Important:** The distance must be in the same direction as the force.
""",

    "waves_speed": """
## Wave Speed — $v = f\\lambda$

**Definitions:**
- Wave speed is the distance travelled by a wave per unit of time.
- Frequency is the number of complete waves passing a point per second.
- Wavelength is the distance from one point on a wave to the identical point on the next wave
  (e.g. crest to crest).

**Key equation:**
$$v = f\\lambda$$

| Symbol | Quantity | Unit |
|---|---|---|
| v | Wave speed | m/s |
| f | Frequency | Hz |
| $\\lambda$ | Wavelength | m |

**Rearrangements:**
$$f = \\frac{v}{\\lambda} \\qquad \\lambda = \\frac{v}{f}$$

**Key values:**
- Speed of light (all EM waves): $c = 3 \\times 10^8$ m/s
- Speed of sound in air: $v \\approx 340$ m/s

**Worked Example:** A wave has a frequency of 50 Hz and a wavelength of 2 m. Calculate its speed.
$$v = f\\lambda = 50 \\times 2 = 100\\ \\mathrm{m/s}$$

> **Important:** Convert all units to SI before substituting (nm → m, MHz → Hz, etc.).
""",

    "waves_period": """
## Period and Frequency — $T = \\frac{1}{f}$

**Definitions:**
- Period is the time taken for one complete wave (cycle).
- Frequency is the number of complete waves (cycles) per second.

**Key equation:**
$$T = \\frac{1}{f} \\qquad f = \\frac{1}{T}$$

| Symbol | Quantity | Unit |
|---|---|---|
| T | Period (time for one complete wave) | s |
| f | Frequency (waves per second) | Hz |

**Prefix conversions:**
| Prefix | Symbol | Factor |
|---|---|---|
| kilo | kHz | $\\times 10^3$ |
| mega | MHz | $\\times 10^6$ |
| giga | GHz | $\\times 10^9$ |
| milli | ms | $\\times 10^{-3}$ |
| micro | μs | $\\times 10^{-6}$ |

**Worked Example:** A wave has a frequency of 25 Hz. Calculate its period.
$$T = \\frac{1}{f} = \\frac{1}{25} = 0.04\\ \\mathrm{s}$$

> **Important:** Period and frequency are reciprocals of each other. Convert to base SI units (Hz, s) before calculating.
""",

    "electricity_current": """
## Electric Current — $I = \\frac{Q}{t}$

**Definition:** Current is the rate of flow of electric charge per unit time (charge passing a
point per second).

**Key equation:**
$$I = \\frac{Q}{t}$$

| Symbol | Quantity | Unit |
|---|---|---|
| I | Current | A (Amperes) |
| Q | Charge | C (Coulombs) |
| t | Time | s (seconds) |

**Rearrangements:**
$$Q = It \\qquad t = \\frac{Q}{I}$$

**Worked Example:** 12 C of charge flows past a point in 4 s. Calculate the current.
$$I = \\frac{Q}{t} = \\frac{12}{4} = 3\\ \\mathrm{A}$$

> **Important:** Convert time to seconds before substituting (minutes $\\times 60$).
""",

    "electricity_power": """
## Electrical Power

**Definition:** Power is the rate at which energy is transferred (the energy transferred per unit
time, per second).

**Three forms of the power equation:**

$$P = VI \\qquad P = \\frac{V^2}{R} \\qquad P = I^2 R$$

| Symbol | Quantity | Unit |
|---|---|---|
| P | Power | W (Watts) |
| V | Voltage (potential difference) | V (Volts) |
| I | Current | A (Amperes) |
| R | Resistance | Ω (Ohms) |

**Useful rearrangements:**

From $P = VI$:
$$V = \\frac{P}{I} \\qquad I = \\frac{P}{V}$$

From $P = \\frac{V^2}{R}$:
$$V = \\sqrt{PR} \\qquad R = \\frac{V^2}{P}$$

From $P = I^2 R$:
$$I = \\sqrt{\\frac{P}{R}} \\qquad R = \\frac{P}{I^2}$$

**Prefix conversions:**

| Prefix | Symbol | Factor |
|---|---|---|
| milli | mW, mV, mA | $\\times 10^{-3}$ |
| kilo | kW, kV, kΩ | $\\times 10^{3}$ |
| mega | MW | $\\times 10^{6}$ |

**Worked Example:** A device operates at 230 V with a current of 4 A. Calculate its power.
$$P = VI = 230 \\times 4 = 920\\ \\mathrm{W}$$

> **Important:** Convert all values to SI units (W, V, A, Ω) before substituting into equations.
""",

    "electricity_power_energy": """
## Power from Energy — $P = \\frac{E}{t}$

**Definition:** Power is the rate at which energy is transferred — the energy transferred per
unit time (per second).

**Key equation:**
$$P = \\frac{E}{t}$$

| Symbol | Quantity | Unit |
|---|---|---|
| P | Power | W (Watts) |
| E | Energy | J (Joules) |
| t | Time | s (seconds) |

**Rearrangements:**
$$E = Pt \\qquad t = \\frac{E}{P}$$

**Prefix conversions:**

| Prefix | Symbol | Factor |
|---|---|---|
| kilo | kJ, kW | $\\times 10^{3}$ |
| mega | MJ, MW | $\\times 10^{6}$ |

**Time conversions:**
$$1\\ \\text{minute} = 60\\ \\text{s} \\qquad 1\\ \\text{hour} = 3600\\ \\text{s}$$

**Worked Example:** A 100 W device runs for 60 s. Calculate the energy it transfers.
$$E = Pt = 100 \\times 60 = 6000\\ \\mathrm{J}$$

> **Important:** Always convert energy to Joules, time to seconds, and power to Watts before substituting.
""",

    "radiation_doses": """
## Radiation Dose Equations

**Definitions:**
- Absorbed dose is the energy absorbed per unit mass of tissue.
- Equivalent dose is the absorbed dose adjusted for how harmful the type of radiation is (using
  the radiation weighting factor).
- Equivalent dose rate is the equivalent dose received per unit time.

**Absorbed dose:**
$$D = \\frac{E}{m} \\quad \\text{(unit: Gray, Gy = J/kg)}$$

**Equivalent dose:**
$$H = D \\times w_R \\quad \\text{(unit: Sievert, Sv)}$$

**Equivalent dose rate:**
$$\\dot{H} = \\frac{H}{t} \\quad \\text{(unit: Sv/h)}$$

| Symbol | Quantity | Unit |
|---|---|---|
| D | Absorbed dose | Gy (Gray) |
| E | Energy absorbed | J |
| m | Mass of tissue | kg |
| H | Equivalent dose | Sv (Sievert) |
| $w_R$ | Radiation weighting factor | (none) |
| $\\dot{H}$ | Equivalent dose rate | Sv/h |

**Radiation weighting factors:**

| Type of radiation | $w_R$ |
|---|---|
| Alpha particles | 20 |
| Beta particles | 1 |
| Gamma rays | 1 |
| Fast neutrons | 20 |
| Slow neutrons | 3 |
| X-rays | 1 |

**Worked Example:** A patient absorbs a dose of 0.5 Gy of alpha particles ($w_R = 20$). Calculate the equivalent dose.
$$H = D \\times w_R = 0.5 \\times 20 = 10\\ \\mathrm{Sv}$$

> **Important:** Absorbed dose uses Gray (Gy); equivalent dose uses Sievert (Sv). Don't mix them up.
""",

    "radiation_half_life": """
## Half-Life

**Definition:** Half-life is the time taken for the activity (or the number of undecayed nuclei)
of a radioactive source to fall to half of its original value.

**Key relationships:**

Number of half-lives:
$$n = \\frac{t}{T_{1/2}}$$

Activity after $n$ half-lives:
$$A = A_0 \\times \\left(\\frac{1}{2}\\right)^n$$

| Symbol | Quantity | Unit |
|---|---|---|
| $T_{1/2}$ | Half-life | s, min, h, days, years |
| t | Total time elapsed | same as $T_{1/2}$ |
| n | Number of half-lives | (none) |
| $A_0$ | Initial activity | Bq (Becquerels) |
| A | Activity after time t | Bq |

**Activity halving rule:**
- Each half-life → divide activity by 2
- Going backwards in time → multiply activity by 2

**Worked Example:** A source has an initial activity of 800 Bq and a half-life of 2 hours. Calculate its activity after 6 hours.
$$n = \\frac{t}{T_{1/2}} = \\frac{6}{2} = 3 \\text{ half-lives}$$
$$A = A_0 \\times \\left(\\frac{1}{2}\\right)^n = 800 \\times \\left(\\frac{1}{2}\\right)^3 = 100\\ \\mathrm{Bq}$$

> **Important:** Activity is measured in Becquerels (Bq). The half-life is the time for activity to halve — not fall to zero.
""",

    "gas_laws": """
## Gas Laws

**Definitions:**
- Pressure is the force exerted per unit area.
- Volume is the amount of space a gas occupies.
- Temperature (in Kelvin) is a measure of the average kinetic energy of the gas particles.

**Boyle's Law** (constant temperature):
$$P_1 V_1 = P_2 V_2$$

**Charles's Law** (constant pressure):
$$\\frac{V_1}{T_1} = \\frac{V_2}{T_2}$$

**Gay-Lussac's Law** (constant volume):
$$\\frac{P_1}{T_1} = \\frac{P_2}{T_2}$$

| Symbol | Quantity | Unit |
|---|---|---|
| P | Pressure | Pa or kPa |
| V | Volume | m³, cm³, mL, L (consistent units) |
| T | Temperature | **K (Kelvin)** |

**Temperature conversion:**
$$T(K) = T(°C) + 273$$

**Worked Example:** A gas at 100 kPa occupies 2 m³. It is compressed at constant temperature to 1 m³. Calculate the new pressure.
$$P_1 V_1 = P_2 V_2 \\quad\\Rightarrow\\quad P_2 = \\frac{P_1 V_1}{V_2} = \\frac{100 \\times 2}{1} = 200\\ \\mathrm{kPa}$$

> **Important:** Temperature MUST be in Kelvin for Charles's and Gay-Lussac's laws. Adding 273, not subtracting.
""",

    "pressure": """
## Pressure — $P = \\frac{F}{A}$

**Definition:** Pressure is the force exerted per unit area.

**Key equations:**
$$P = \\frac{F}{A} \\qquad W = mg$$

| Symbol | Quantity | Unit |
|---|---|---|
| P | Pressure | Pa (Pascals) |
| F | Force (weight) | N (Newtons) |
| A | Area | m² |
| W | Weight | N |
| m | Mass | kg |
| g | Gravitational field strength | 9.8 N/kg |

**Rearrangements:**
$$F = PA \\qquad A = \\frac{F}{P}$$

**Worked Example:** A force of 800 N acts on an area of 2 m². Calculate the pressure.
$$P = \\frac{F}{A} = \\frac{800}{2} = 400\\ \\mathrm{Pa}$$

> **Important:** The force exerted by a stationary object on the ground equals its weight ($W = mg$). Total contact area = number of tyres × area per tyre.
""",

    "heat_shc": """
## Specific Heat Capacity & Latent Heat

**Definitions:**
- Specific heat capacity is the energy needed to raise the temperature of 1 kg of a substance by
  1°C.
- Specific latent heat is the energy needed to change the state of 1 kg of a substance without
  changing its temperature.

**Specific heat capacity (temperature change):**
$$E_H = mc\\Delta T$$

**Latent heat (change of state):**
$$E_H = mL$$

| Symbol | Quantity | Unit |
|---|---|---|
| $E_H$ | Energy transferred | J |
| m | Mass | kg |
| c | Specific heat capacity | J/kg°C |
| $\\Delta T$ | Temperature change | °C |
| L | Specific latent heat | J/kg |

**Key values for water:**
- $c = 4200$ J/kg°C (specific heat capacity)
- $L_{fusion} = 334\\,000$ J/kg (melting/freezing)
- $L_{vaporisation} = 2\\,260\\,000$ J/kg (boiling/condensing)

**Worked Example:** 2 kg of water is heated so its temperature rises by 10°C ($c = 4200$ J/kg°C). Calculate the energy transferred.
$$E_H = mc\\Delta T = 2 \\times 4200 \\times 10 = 84\\,000\\ \\mathrm{J}$$

> **Important:** $\\Delta T = T_2 - T_1$ (the change, not the final temperature). Convert grams to kg. During a change of state, temperature stays constant.
""",

    "vectors": """
## Vectors — Resultant & Bearing

**Definitions:**
- Distance is the total length of the path travelled — a *scalar*, so direction doesn't matter.
- Displacement is how far and in what direction an object ends up from its starting point — a
  *vector*.

**Distance vs displacement (1D):**
- **Distance**: just add up the magnitude of every leg of the journey.
- **Displacement**: along a single straight line, pick one direction as positive and the opposite
  as negative, then add the signed values (legs in opposite directions partly cancel out).

**Magnitude of resultant** (Pythagoras):
$$R = \\sqrt{a^2 + b^2}$$

**Direction (bearing):**
$$\\theta = \\tan^{-1}\\left(\\frac{\\text{opposite}}{\\text{adjacent}}\\right)$$

**Quadrant rules for bearing:**

| Quadrant | Direction | Bearing |
|---|---|---|
| Q1 | N of E | $\\theta$ |
| Q2 | N of W | $360° - \\theta$ |
| Q3 | S of W | $180° + \\theta$ |
| Q4 | S of E | $180° - \\theta$ |

**Worked Example:** A boat travels 3 km east and 4 km north. Calculate the magnitude and bearing of the resultant displacement.
$$R = \\sqrt{3^2 + 4^2} = \\sqrt{25} = 5\\ \\mathrm{km}$$
$$\\theta = \\tan^{-1}\\left(\\frac{3}{4}\\right) = 36.9°$$
Both legs are positive (N and E), so the bearing is $\\theta$: **037°**.

> **Important:** Don't add or subtract components — use Pythagoras. Bearings are measured clockwise from North (000° to 360°).
""",

    "vectors_scalars": """
## Vectors and Scalars

**Definitions:**
- A **scalar** quantity has magnitude (size) only.
- A **vector** quantity has both magnitude **and direction**.

| Scalar quantities | Vector quantities |
|---|---|
| Distance | Displacement |
| Speed | Velocity |
| Mass | Force |
| Energy (kinetic, potential, etc.) | Weight |
| Work done | Acceleration |

**Worked Example:** Is mass a scalar or a vector? A 5 kg mass has a size (5 kg) but no direction, so **mass is a scalar**.
Is velocity a scalar or a vector? "5 m/s north" has both a size (5 m/s) and a direction (north), so **velocity is a vector**.

> **Important:** Similar-sounding quantities can be different types — distance (scalar) vs
> displacement (vector), speed (scalar) vs velocity (vector). Weight is a force, so it is always
> a vector.
""",

    "projectiles": """
## Projectile Motion

**Definition:** A projectile is an object given an initial velocity and then left to move under
gravity alone — it has **independent** horizontal and vertical motion.

**Horizontal** (constant velocity):
$$s_H = v_H \\times t$$

**Vertical** (acceleration due to gravity, $g = 9.8$ m/s²):

Velocity at time $t$: $\\quad v_v = gt$ (initial vertical velocity = 0)

Height fallen: $\\quad s = \\frac{1}{2}gt^2$

| Symbol | Quantity | Unit |
|---|---|---|
| $v_H$ | Horizontal velocity | m/s |
| $t$ | Time of flight | s |
| $s_H$ | Horizontal range | m |
| $v_v$ | Vertical velocity | m/s |
| s | Height fallen | m |
| g | Gravitational acceleration | 9.8 m/s² |

**Worked Example:** An object is launched horizontally at 10 m/s and falls for 2 s ($g = 9.8$ m/s²). Calculate the height fallen and the horizontal range.
$$s = \\frac{1}{2}gt^2 = \\frac{1}{2} \\times 9.8 \\times 2^2 = 19.6\\ \\mathrm{m}$$
$$s_H = v_H \\times t = 10 \\times 2 = 20\\ \\mathrm{m}$$

> **Important:** Horizontal speed stays constant throughout. Vertical speed starts at 0 and increases. Use area under v-t graph (triangle) for height: $s = \\frac{1}{2} \\times t \\times v_v$.
""",
}
