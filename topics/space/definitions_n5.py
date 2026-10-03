from utils.definitions import make_definition_generators

# Definitions needed for the N5 Space unit (space exploration and cosmology), worded as accepted
# in SQA marking instructions. See utils/definitions.py for the entry format.
DEFINITIONS = {
    # ── Our Universe ───────────────────────────────────────────────────────────
    "planet": {
        "group": "Our Universe",
        "definition": "A large, round body that orbits a star and has cleared its orbit of other objects.",
        "confusables": ["dwarf planet", "moon", "exoplanet"],
    },
    "dwarf planet": {
        "group": "Our Universe",
        "definition": "A round body that orbits the Sun but has not cleared its orbit of other objects (e.g. Pluto).",
        "confusables": ["planet", "asteroid"],
        "traps": [("A small, rocky, irregular-shaped object orbiting the Sun.",
                   "That describes an **asteroid** — a dwarf planet is massive enough to be round (course report 2023).")],
    },
    "moon": {
        "group": "Our Universe",
        "definition": "A natural satellite of a planet (or dwarf planet).",
        "confusables": ["planet", "asteroid"],
        "traps": [("A satellite of a planet.", "The marking instructions require **natural** satellite.")],
    },
    "asteroid": {
        "group": "Our Universe",
        "definition": "A small, rocky, irregular-shaped object orbiting the Sun (mostly between Mars and Jupiter).",
        "confusables": ["dwarf planet", "moon"],
    },
    "star": {
        "group": "Our Universe",
        "definition": "A ball of hot gas (plasma) that produces energy by nuclear fusion, e.g. the Sun.",
        "confusables": ["planet", "galaxy"],
    },
    "solar system": {
        "group": "Our Universe",
        "definition": "A star and all the objects that orbit it (planets, dwarf planets, moons, asteroids, comets).",
        "confusables": ["galaxy", "universe"],
    },
    "exoplanet": {
        "group": "Our Universe",
        "definition": "A planet that orbits a star other than the Sun.",
        "confusables": ["planet", "dwarf planet"],
        "traps": [("A planet that is outside our galaxy.", "An exoplanet is outside our **solar system** — it orbits another star (course report 2024)."),
                  ("A planet that no longer orbits a star.", "It orbits a star other than the Sun (course report 2024).")],
    },
    "galaxy": {
        "group": "Our Universe",
        "definition": "A large collection of stars (billions), e.g. the Milky Way.",
        "confusables": ["solar system", "universe"],
    },
    "universe": {
        "group": "Our Universe",
        "definition": "Everything that exists — all the galaxies, and the space between them.",
        "confusables": ["galaxy", "solar system"],
    },

    # ── Satellites and space travel ────────────────────────────────────────────
    "geostationary satellite": {
        "group": "Satellites and space travel",
        "definition": "A satellite with a period of 24 hours, at an altitude of 36 000 km, which stays above the same point on the Earth's surface.",
        "confusables": ["moon"],
        "traps": [("A satellite that does not move.", "It moves — its period matches the Earth's rotation (course report 2023).")],
    },
    "ion drive": {
        "group": "Satellites and space travel",
        "definition": "An engine producing a small unbalanced force over a very long time, giving a large increase in speed.",
        "confusables": ["gravitational slingshot"],
    },
    "gravitational slingshot": {
        "group": "Satellites and space travel",
        "definition": "Using the gravity of a planet or moon that a spacecraft passes close to, to increase its speed.",
        "confusables": ["ion drive"],
    },

    # ── Cosmology ──────────────────────────────────────────────────────────────
    "light-year": {
        "group": "Cosmology",
        "definition": "The distance travelled by light in one year (about 9.5 × 10¹⁵ m).",
        "confusables": ["the Big Bang theory"],
        "traps": [("The time taken for light to travel from the Sun to the Earth.", "A light-year is a **distance**, not a time (2024 Paper 1 Q8).")],
    },
    "the Big Bang theory": {
        "group": "Cosmology",
        "definition": "The theory that the Universe began about 13.8 billion years ago from a very hot, dense point and has been expanding ever since.",
        "confusables": ["light-year"],
    },
    "continuous spectrum": {
        "group": "Cosmology",
        "definition": "A spectrum containing all colours (wavelengths) with no gaps, e.g. from a hot solid such as a filament lamp.",
        "confusables": ["line spectrum"],
    },
    "line spectrum": {
        "group": "Cosmology",
        "definition": "A spectrum of separate lines of particular wavelengths, unique to each element, e.g. from a hot gas.",
        "confusables": ["continuous spectrum"],
    },
}

STATEMENTS = [
    # key, statement, correct?, explanation
    ("age", "The Universe is approximately 13.8 billion years old.", True, "The accepted estimate from the Big Bang model."),
    ("age", "The Universe is approximately 14 million years old.", False, "It is about 13.8 **billion** years old."),
    ("ly", "A light-year is a unit of distance.", True, "The distance light travels in one year."),
    ("ly", "A light-year is the time taken for light to reach the Earth from the Sun.", False, "It is a **distance**; light takes about 8 minutes from the Sun."),
    ("geo", "All geostationary satellites orbit at the same altitude.", True, "36 000 km, with a period of 24 hours."),
    ("geo", "The greater the altitude of a satellite, the shorter its period.", False, "Higher orbits have **longer** periods."),
    ("weight", "An astronaut's mass is the same on Mars as on Earth.", True, "Mass doesn't change; weight = mg does."),
    ("gravity", "There is no gravity acting on astronauts in the International Space Station.", False,
     "Gravity still acts — the astronauts and the station are in **free fall** around the Earth."),
    ("spectra", "Each element has a unique pattern of lines in its line spectrum.", True, "This is how elements in stars are identified."),
    ("spectra", "Each line in a star's spectrum comes from a different element.", False, "Each element produces **several** lines; the pattern identifies it (course report 2022)."),
]

GENERATORS = make_definition_generators("Space", DEFINITIONS, STATEMENTS)
