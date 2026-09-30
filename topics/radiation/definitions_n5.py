from utils.definitions import make_definition_generators

# Definitions needed for the N5 Radiation unit, worded as accepted in SQA
# marking instructions. See utils/definitions.py for the entry format.
DEFINITIONS = {
    # ── Types of radiation ─────────────────────────────────────────────────────
    "alpha particle": {
        "group": "Types of radiation",
        "definition": "A helium nucleus — two protons and two neutrons.",
        "confusables": ["beta particle", "gamma ray"],
    },
    "beta particle": {
        "group": "Types of radiation",
        "definition": "A fast-moving electron emitted from the nucleus.",
        "confusables": ["alpha particle", "gamma ray"],
    },
    "gamma ray": {
        "group": "Types of radiation",
        "definition": "A high-frequency electromagnetic wave emitted from the nucleus.",
        "confusables": ["alpha particle", "beta particle"],
        "traps": [("A fast-moving neutron emitted from the nucleus.",
                   "Gamma radiation is not a particle — it is an **electromagnetic wave**.")],
    },
    "ionisation": {
        "group": "Types of radiation",
        "definition": "The gain or loss of electrons by an atom.",
        "confusables": ["alpha particle"],
        "traps": [("The gain or loss of protons by an atom.",
                   "Ionisation involves **electrons** — the nucleus is unchanged.")],
    },
    "background radiation": {
        "group": "Types of radiation",
        "definition": "Radiation that is always present in the environment, from both natural "
                      "and man-made sources.",
        "confusables": ["equivalent dose rate"],
    },

    # ── Activity and half-life ─────────────────────────────────────────────────
    "activity": {
        "group": "Activity and half-life",
        "definition": "The number of nuclei that decay per second.",
        "confusables": ["half-life", "equivalent dose rate"],
    },
    "the becquerel": {
        "group": "Activity and half-life",
        "definition": "An activity of one decay per second.",
        "confusables": ["half-life"],
    },
    "half-life": {
        "group": "Activity and half-life",
        "definition": "The time taken for the activity of a radioactive source to fall to half "
                      "its original value.",
        "confusables": ["activity"],
        "traps": [("Half the time taken for a radioactive source to stop being radioactive.",
                   "A source never fully stops decaying — half-life is the time for the "
                   "**activity to halve**.")],
    },

    # ── Dosimetry ──────────────────────────────────────────────────────────────
    "absorbed dose": {
        "group": "Dosimetry",
        "definition": "The energy absorbed per unit mass of the absorbing material.",
        "confusables": ["equivalent dose", "activity"],
        "traps": [("The energy absorbed per unit time by the absorbing material.",
                   "Absorbed dose is energy per unit **mass** (D = E ÷ m), measured in grays.")],
    },
    "equivalent dose": {
        "group": "Dosimetry",
        "definition": "The absorbed dose multiplied by the radiation weighting factor.",
        "confusables": ["absorbed dose", "radiation weighting factor"],
    },
    "radiation weighting factor": {
        "group": "Dosimetry",
        "definition": "A number that takes account of the type of radiation and the biological "
                      "harm it causes.",
        "confusables": ["equivalent dose", "absorbed dose"],
    },
    "equivalent dose rate": {
        "group": "Dosimetry",
        "definition": "The equivalent dose received per unit time.",
        "confusables": ["equivalent dose", "activity"],
    },

    # ── Nuclear energy ─────────────────────────────────────────────────────────
    "nuclear fission": {
        "group": "Nuclear energy",
        "definition": "A large nucleus splits into two smaller nuclei, releasing neutrons and "
                      "energy.",
        "confusables": ["nuclear fusion", "chain reaction"],
    },
    "nuclear fusion": {
        "group": "Nuclear energy",
        "definition": "Two small nuclei combine to form a larger nucleus, releasing energy.",
        "confusables": ["nuclear fission"],
    },
    "chain reaction": {
        "group": "Nuclear energy",
        "definition": "Neutrons released by a fission reaction go on to cause further fission "
                      "reactions.",
        "confusables": ["nuclear fission"],
    },
}

STATEMENTS = [
    # key, statement, correct?, explanation
    ("alpha", "Alpha radiation is the most ionising of the three types of radiation.", True,
     "Alpha particles are large and charged, so they cause the most ionisation."),
    ("alpha", "Alpha radiation can pass through a thin sheet of aluminium.", False,
     "Alpha is stopped by a sheet of paper (or a few cm of air). Beta is stopped by a few mm "
     "of aluminium."),
    ("gamma", "Gamma radiation is an electromagnetic wave.", True,
     "Gamma rays are high-frequency electromagnetic waves emitted from the nucleus."),
    ("gamma", "Gamma radiation is a helium nucleus.", False,
     "That is an **alpha particle**. Gamma is an electromagnetic wave."),
    ("halflife", "After two half-lives the activity of a source has fallen to one quarter of "
     "its original value.", True,
     "It halves, then halves again: ½ × ½ = ¼."),
    ("halflife", "After two half-lives a source is no longer radioactive.", False,
     "After two half-lives the activity has fallen to a **quarter** — it keeps halving."),
    ("dose", "Equivalent dose takes account of the type of radiation absorbed.", True,
     "H = D × w_R — the radiation weighting factor depends on the type of radiation."),
    ("fission", "Nuclear fission can be induced by a neutron being absorbed by a large nucleus.",
     True, "The nucleus becomes unstable and splits, releasing more neutrons and energy."),
    ("fission", "In nuclear fusion a large nucleus splits into two smaller nuclei.", False,
     "That is **fission**. In fusion two small nuclei combine to form a larger nucleus."),
    ("background", "Background radiation comes from both natural and man-made sources.", True,
     "e.g. radon gas and cosmic rays (natural); medical X-rays and nuclear waste (man-made)."),
    ("ionisation", "Ionisation is when an atom gains or loses electrons.", True,
     "This is the definition of ionisation."),
    ("activity", "The activity of a source is measured in sieverts.", False,
     "Activity is measured in **becquerels** (Bq). The sievert is the unit of equivalent dose."),
]

GENERATORS = make_definition_generators("Radiation", DEFINITIONS, STATEMENTS)
