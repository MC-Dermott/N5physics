from utils.definitions import make_definition_generators

# Definitions needed for the N5 Properties of Matter unit, worded as accepted
# in SQA marking instructions. See utils/definitions.py for the entry format.
DEFINITIONS = {
    # ── Heat ───────────────────────────────────────────────────────────────────
    "temperature": {
        "group": "Heat",
        "definition": "A measure of the mean kinetic energy of the particles of a substance.",
        "confusables": ["heat", "absolute zero"],
        "traps": [("The total energy of all the particles in a substance.",
                   "Temperature depends on the **mean (average)** kinetic energy of the "
                   "particles, not the total energy.")],
    },
    "heat": {
        "group": "Heat",
        "definition": "Energy transferred from a region of higher temperature to a region of "
                      "lower temperature.",
        "confusables": ["temperature"],
    },
    "specific heat capacity": {
        "group": "Heat",
        "definition": "The energy required to change the temperature of 1 kg of a substance "
                      "by 1 °C.",
        "confusables": ["specific latent heat", "specific latent heat of fusion"],
        "traps": [("The energy required to change the temperature of a substance by 1 °C.",
                   "The definition is for **1 kg** of the substance — that is what 'specific' "
                   "means.")],
    },
    "specific latent heat": {
        "group": "Heat",
        "definition": "The energy required to change the state of 1 kg of a substance without "
                      "a change in temperature.",
        "confusables": ["specific heat capacity"],
    },
    "specific latent heat of fusion": {
        "group": "Heat",
        "definition": "The energy required to change 1 kg of a substance from solid to liquid "
                      "without a change in temperature.",
        "confusables": ["specific latent heat of vaporisation", "specific heat capacity"],
    },
    "specific latent heat of vaporisation": {
        "group": "Heat",
        "definition": "The energy required to change 1 kg of a substance from liquid to gas "
                      "without a change in temperature.",
        "confusables": ["specific latent heat of fusion", "specific heat capacity"],
        "traps": [("The energy required to change 1 kg of a substance from solid to liquid "
                   "without a change in temperature.",
                   "Solid → liquid (melting) is **fusion**. Vaporisation is liquid → gas.")],
    },

    # ── Gases ──────────────────────────────────────────────────────────────────
    "pressure": {
        "group": "Gases",
        "definition": "The force per unit area.",
        "confusables": ["the pascal"],
        "traps": [("The force multiplied by the area it acts on.",
                   "Pressure is force **divided** by area (p = F ÷ A).")],
    },
    "the pascal": {
        "group": "Gases",
        "definition": "A pressure of one newton per square metre.",
        "confusables": ["pressure"],
    },
    "absolute zero": {
        "group": "Gases",
        "definition": "The temperature at which the particles of a substance have no kinetic "
                      "energy (0 K, which is −273 °C).",
        "confusables": ["temperature"],
    },
    "Boyle's law": {
        "group": "Gases",
        "definition": "For a fixed mass of gas at constant temperature, the pressure is "
                      "inversely proportional to the volume.",
        "confusables": ["the pressure law", "Charles' law"],
        "traps": [("For a fixed mass of gas at constant temperature, the pressure is directly "
                   "proportional to the volume.",
                   "Squashing a gas into a **smaller** volume gives a **higher** pressure, so "
                   "they are inversely proportional (pV = constant).")],
    },
    "the pressure law": {
        "group": "Gases",
        "definition": "For a fixed mass of gas at constant volume, the pressure is directly "
                      "proportional to the temperature in kelvin.",
        "confusables": ["Charles' law", "Boyle's law"],
        "traps": [("For a fixed mass of gas at constant volume, the pressure is directly "
                   "proportional to the temperature in degrees Celsius.",
                   "The gas laws only work with temperature in **kelvin**.")],
    },
    "Charles' law": {
        "group": "Gases",
        "definition": "For a fixed mass of gas at constant pressure, the volume is directly "
                      "proportional to the temperature in kelvin.",
        "confusables": ["the pressure law", "Boyle's law"],
    },
}

# One latent-heat definition also fits the others (fusion and vaporisation are
# both changes of state), so they never appear as options together.
OVERLAPS = [
    {"specific latent heat", "specific latent heat of fusion",
     "specific latent heat of vaporisation"},
]

STATEMENTS = [
    # key, statement, correct?, explanation
    ("abs", "Absolute zero is 0 K, which is −273 °C.", True,
     "To convert from °C to kelvin, add 273."),
    ("abs", "At absolute zero the particles of a substance move fastest.", False,
     "At absolute zero the particles have **no** kinetic energy."),
    ("temp", "Increasing the temperature of a gas increases the mean kinetic energy of its "
     "particles.", True,
     "Temperature is a measure of the mean kinetic energy of the particles."),
    ("boyle", "If the volume of a fixed mass of gas at constant temperature is halved, its "
     "pressure doubles.", True,
     "Boyle's law — pressure is inversely proportional to volume."),
    ("boyle", "If the volume of a fixed mass of gas at constant temperature is halved, its "
     "pressure halves.", False,
     "Boyle's law — pressure is **inversely** proportional to volume, so the pressure doubles."),
    ("latent", "During a change of state, the temperature of a substance stays constant.", True,
     "The energy goes into changing the state, not the temperature."),
    ("latent", "The specific latent heat of vaporisation is the energy needed to melt 1 kg of a "
     "substance.", False,
     "Melting is **fusion**. Vaporisation is changing 1 kg from liquid to gas."),
    ("kinetic", "Gas pressure is caused by particles colliding with the walls of the "
     "container.", True,
     "Each collision exerts a force on the wall; force per unit area is pressure."),
    ("kelvin", "The gas laws only work when temperatures are in degrees Celsius.", False,
     "The gas laws need temperatures in **kelvin**."),
    ("shc", "Equal masses of two substances are given the same energy. The one with the higher "
     "specific heat capacity has the smaller temperature rise.", True,
     "ΔT = Eh ÷ (cm), so a larger c gives a smaller ΔT."),
]

GENERATORS = make_definition_generators("Properties", DEFINITIONS, STATEMENTS, OVERLAPS,
                                        title="Properties of Matter Definitions")
