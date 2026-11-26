"""Definitions bank for AH Quanta and Waves. See utils/definitions.py for the format."""
from utils.definitions import make_definition_generators

DEFINITIONS = {
    # ── Quantum theory and particles from space ──
    "Heisenberg uncertainty principle": {
        "group": "Quantum theory",
        "definition": "The precise position of a particle and its momentum cannot both be known at the same instant.",
        "confusables": ["quantum tunnelling"],
        "traps": [("The position and momentum of a particle cannot be measured accurately.",
                   "It is about **precision**, and the two cannot both be known **at the same instant**. "
                   "Mixing up accuracy and precision scores nothing.")],
    },
    "quantum tunnelling": {
        "group": "Quantum theory",
        "definition": "A quantum particle existing in a position that, according to classical physics, it has insufficient energy to occupy.",
        "confusables": ["Heisenberg uncertainty principle"],
    },
    "photoelectric effect": {
        "group": "Quantum theory",
        "definition": "The emission of electrons from a surface when light of high enough frequency shines on it.",
        "confusables": ["Compton scattering", "electron diffraction"],
    },
    "Compton scattering": {
        "group": "Quantum theory",
        "definition": "The change in wavelength of a photon when it scatters from an electron.",
        "confusables": ["photoelectric effect", "electron diffraction"],
    },
    "electron diffraction": {
        "group": "Quantum theory",
        "definition": "The spreading of a beam of electrons into a diffraction pattern, showing their wave-like behaviour.",
        "confusables": ["photoelectric effect", "Compton scattering"],
    },
    "ultraviolet catastrophe": {
        "group": "Quantum theory",
        "definition": "The failure of classical physics to predict black-body radiation curves at short wavelengths.",
        "confusables": ["photoelectric effect"],
    },
    "solar wind": {
        "group": "Particles from space",
        "definition": "A flow of charged particles from the Sun in the form of plasma.",
        "confusables": ["cosmic rays", "plasma"],
    },
    "cosmic rays": {
        "group": "Particles from space",
        "definition": "Very high energy particles that reach the Earth from sources such as the Sun, stars and black holes.",
        "confusables": ["solar wind"],
    },
    "plasma": {
        "group": "Particles from space",
        "definition": "A state of matter made up of charged particles, such as ions and free electrons.",
        "confusables": ["solar wind"],
    },
    # ── Oscillations and waves ──
    "simple harmonic motion": {
        "group": "Oscillations",
        "definition": "Motion in which the unbalanced force is proportional to, and in the opposite direction to, the displacement from the rest position.",
        "confusables": ["critical damping"],
        "traps": [("Motion in which the force is proportional to the displacement from the rest position.",
                   "The direction is missing: **in the opposite direction to** the displacement.")],
    },
    "underdamping": {
        "group": "Oscillations",
        "definition": "Damping in which the system oscillates with a decreasing amplitude.",
        "confusables": ["critical damping", "overdamping"],
    },
    "critical damping": {
        "group": "Oscillations",
        "definition": "Damping in which the system returns to rest in the shortest time without oscillating.",
        "confusables": ["underdamping", "overdamping"],
    },
    "overdamping": {
        "group": "Oscillations",
        "definition": "Damping in which the system takes longer than the minimum time to return to rest, without oscillating.",
        "confusables": ["critical damping", "underdamping"],
    },
    "stationary wave": {
        "group": "Waves",
        "definition": "The wave formed by the interference of two waves of the same frequency and amplitude travelling in opposite directions.",
        "confusables": ["node", "antinode"],
    },
    "node": {
        "group": "Waves",
        "definition": "A position in a stationary wave where the displacement is always zero.",
        "confusables": ["antinode"],
    },
    "antinode": {
        "group": "Waves",
        "definition": "A position in a stationary wave where the amplitude of oscillation is a maximum.",
        "confusables": ["node"],
    },
    # ── Interference and polarisation ──
    "coherent waves": {
        "group": "Interference and polarisation",
        "definition": "Waves which have a constant phase relationship.",
        "confusables": ["plane-polarised light"],
        "traps": [("Waves which are always in phase.", "The phase difference only has to be **constant**.")],
    },
    "plane-polarised light": {
        "group": "Interference and polarisation",
        "definition": "Light in which the electric field vector oscillates in one plane only.",
        "confusables": ["coherent waves"],
        "traps": [("Light which travels in one plane only.",
                   "'Travels', 'direction' and 'axis' are not accepted: the field **oscillates** in one **plane**.")],
    },
    "interference by division of amplitude": {
        "group": "Interference and polarisation",
        "definition": "Interference between parts of a wave separated by partial reflection and transmission, as in a thin film.",
        "confusables": ["interference by division of wavefront"],
    },
    "interference by division of wavefront": {
        "group": "Interference and polarisation",
        "definition": "Interference between waves taken from different parts of the same wavefront, as with Young's slits.",
        "confusables": ["interference by division of amplitude"],
    },
}

STATEMENTS = [
    ("hup", "The precise position of a quantum particle and its momentum cannot both be known at the same instant.", True,
     "this is the Heisenberg uncertainty principle."),
    ("hup", "The Heisenberg uncertainty principle only exists because measuring instruments are not good enough.", False,
     "it is a fundamental limit."),
    ("evidence", "Electron diffraction is evidence for the wave-like behaviour of particles.", True, "diffraction is a wave property."),
    ("evidence", "The photoelectric effect is evidence for the wave-like behaviour of light.", False, "it shows particle-like behaviour."),
    ("bohr", "In the Bohr model the angular momentum of an electron is quantised.", True, "mvr = nh/2π."),
    ("solar", "The solar wind consists of charged particles in the form of plasma.", True, "mostly protons and electrons."),
    ("helix", "A charged particle's velocity component parallel to a magnetic field is unaffected by the field.", True,
     "there is no force from this component."),
    ("helix", "A charged particle moving parallel to a magnetic field moves in a circle.", False, "there is no force on it."),
    ("shm", "In SHM the acceleration is in the opposite direction to the displacement.", True, "a = −ω²y."),
    ("shm", "In SHM the acceleration is greatest at the rest position.", False, "it is zero there."),
    ("energy", "The energy of a wave is proportional to the square of its amplitude.", True, "E = kA²."),
    ("stationary", "The distance between neighbouring nodes in a stationary wave is half a wavelength.", True, "node to node is λ/2."),
    ("phase", "Light reflecting from an interface with a more dense medium has a phase change of π radians.", True,
     "this is needed when applying the interference conditions."),
    ("phase", "Light reflecting from an interface with a less dense medium has a phase change of π radians.", False,
     "there is no phase change."),
    ("polar", "Sound waves can be plane-polarised.", False, "sound is longitudinal."),
    ("brewster", "At Brewster's angle the reflected light is plane-polarised.", True, "and n = tan iP."),
]

quanta_waves_ah_definitions = make_definition_generators("Quanta and Waves", DEFINITIONS, STATEMENTS)
