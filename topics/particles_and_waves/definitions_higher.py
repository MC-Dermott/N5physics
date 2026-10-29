from utils.definitions import make_definition_generators

# Definitions needed for Higher Particles and Waves, worded as accepted in SQA
# marking instructions. See utils/definitions.py for the entry format.
DEFINITIONS = {
    # ── The standard model ─────────────────────────────────────────────────────
    "fermion": {
        "group": "The standard model",
        "definition": "A matter particle — the quarks and the leptons.",
        "confusables": ["boson", "hadron"],
    },
    "boson": {
        "group": "The standard model",
        "definition": "A force-mediating (exchange) particle, e.g. the photon, gluon, W and Z.",
        "confusables": ["fermion"],
    },
    "lepton": {
        "group": "The standard model",
        "definition": "A fundamental matter particle that is not affected by the strong force, "
                      "e.g. the electron and the neutrino.",
        "confusables": ["hadron", "meson"],
        "traps": [("A particle made up of quarks, e.g. the electron.",
                   "Leptons are **fundamental** — they are not made of anything smaller.")],
    },
    "hadron": {
        "group": "The standard model",
        "definition": "A particle made up of quarks.",
        "confusables": ["lepton", "boson"],
    },
    "baryon": {
        "group": "The standard model",
        "definition": "A hadron made up of three quarks, e.g. the proton and the neutron.",
        "confusables": ["meson", "lepton"],
        "traps": [("A hadron made up of a quark and an antiquark.",
                   "That is a **meson**. Baryons are made of three quarks.")],
    },
    "meson": {
        "group": "The standard model",
        "definition": "A hadron made up of a quark and an antiquark.",
        "confusables": ["baryon", "lepton"],
    },
    "antiparticle": {
        "group": "The standard model",
        "definition": "A particle with the same mass as its matter particle but the opposite "
                      "charge.",
        "confusables": ["fermion"],
    },

    # ── Electric fields ────────────────────────────────────────────────────────
    "electric field": {
        "group": "Electric fields",
        "definition": "A region in which a charged particle experiences a force.",
        "confusables": ["potential difference"],
    },
    "potential difference": {
        "group": "Electric fields",
        "definition": "The work done in moving one coulomb of charge between two points.",
        "confusables": ["electric field", "work function"],
    },

    # ── Photoelectric effect and spectra ───────────────────────────────────────
    "photon": {
        "group": "Photoelectric effect and spectra",
        "definition": "A packet (quantum) of electromagnetic energy.",
        "confusables": ["boson", "irradiance"],
    },
    "photoelectric effect": {
        "group": "Photoelectric effect and spectra",
        "definition": "The emission of electrons from a metal surface when electromagnetic "
                      "radiation of high enough frequency is incident on it.",
        "confusables": ["threshold frequency", "work function"],
    },
    "threshold frequency": {
        "group": "Photoelectric effect and spectra",
        "definition": "The minimum frequency of radiation that will cause photoelectrons to be "
                      "emitted from a particular metal.",
        "confusables": ["work function"],
        "traps": [("The minimum irradiance of radiation that will cause photoelectrons to be "
                   "emitted from a particular metal.",
                   "Emission depends on the **frequency**, not the irradiance — below the "
                   "threshold frequency no electrons are emitted however bright the light.")],
    },
    "work function": {
        "group": "Photoelectric effect and spectra",
        "definition": "The minimum energy needed to release an electron from the surface of a "
                      "metal.",
        "confusables": ["threshold frequency", "ionisation level"],
    },
    "irradiance": {
        "group": "Photoelectric effect and spectra",
        "definition": "The power per unit area incident on a surface.",
        "confusables": ["photon"],
        "traps": [("The energy per unit area incident on a surface.",
                   "Irradiance is **power** per unit area (I = P ÷ A), measured in W/m².")],
    },
    "ground state": {
        "group": "Photoelectric effect and spectra",
        "definition": "The lowest energy level of an atom.",
        "confusables": ["ionisation level"],
    },
    "ionisation level": {
        "group": "Photoelectric effect and spectra",
        "definition": "The energy level (zero energy) at which an electron is free from the atom.",
        "confusables": ["ground state", "work function"],
    },
    "absorption spectrum": {
        "group": "Photoelectric effect and spectra",
        "definition": "A continuous spectrum crossed by dark lines, where certain frequencies "
                      "have been absorbed by a cooler gas.",
        "confusables": ["emission line spectrum"],
    },
    "emission line spectrum": {
        "group": "Photoelectric effect and spectra",
        "definition": "A series of bright lines of particular frequencies, emitted when "
                      "electrons in excited atoms fall to lower energy levels.",
        "confusables": ["absorption spectrum"],
    },

    # ── Interference ───────────────────────────────────────────────────────────
    "coherent sources": {
        "group": "Interference",
        "definition": "Sources of waves that have a constant phase difference.",
        "confusables": ["constructive interference"],
        "traps": [("Sources of waves that have the same amplitude.",
                   "Coherent sources must have a **constant phase difference** (and so the same "
                   "frequency) — equal amplitude isn't required.")],
    },
    "constructive interference": {
        "group": "Interference",
        "definition": "When waves meet in phase, producing a maximum.",
        "confusables": ["destructive interference", "coherent sources"],
    },
    "destructive interference": {
        "group": "Interference",
        "definition": "When waves meet exactly out of phase, producing a minimum.",
        "confusables": ["constructive interference", "coherent sources"],
    },

    # ── Refraction ─────────────────────────────────────────────────────────────
    "refractive index": {
        "group": "Refraction",
        "definition": "The ratio of the speed of light in a vacuum (air) to the speed of light "
                      "in the material.",
        "confusables": ["critical angle"],
    },
    "critical angle": {
        "group": "Refraction",
        "definition": "The angle of incidence that produces an angle of refraction of 90°.",
        "confusables": ["total internal reflection", "refractive index"],
        "traps": [("The angle of refraction that is produced by an angle of incidence of 90°.",
                   "It is the other way round — the critical angle is the angle of "
                   "**incidence** that gives a refraction angle of 90°.")],
    },
    "total internal reflection": {
        "group": "Refraction",
        "definition": "When all the light is reflected back into the denser material, because "
                      "the angle of incidence is greater than the critical angle.",
        "confusables": ["critical angle"],
    },
}

# A baryon or meson is also a hadron, and a lepton is also a fermion, so the
# more general definition would fit too.
OVERLAPS = [
    {"hadron", "baryon"},
    {"hadron", "meson"},
    {"fermion", "lepton"},
]

STATEMENTS = [
    # key, statement, correct?, explanation
    ("baryon", "A proton is a baryon made up of three quarks.", True,
     "A proton is two up quarks and one down quark (uud)."),
    ("baryon", "A meson is made up of three quarks.", False,
     "Mesons are a quark–antiquark pair. **Baryons** are made of three quarks."),
    ("lepton", "The electron is a lepton.", True,
     "Leptons include the electron, muon, tau and their neutrinos."),
    ("lepton", "Leptons are made up of quarks.", False,
     "Leptons are **fundamental** particles. Hadrons are made of quarks."),
    ("gluon", "The gluon is the force-mediating boson for the strong force.", True,
     "Gluons hold quarks together."),
    ("gluon", "The photon is the force-mediating boson for the strong force.", False,
     "The photon mediates the **electromagnetic** force; the gluon mediates the strong force."),
    ("photo", "Photoelectrons are only emitted if the frequency of the radiation is at or above "
     "the threshold frequency.", True,
     "Each photon must have at least the work function's worth of energy (hf₀ = W)."),
    ("photo", "Increasing the irradiance of radiation below the threshold frequency will cause "
     "photoelectrons to be emitted.", False,
     "Below the threshold frequency **no** photoelectrons are emitted, however large the "
     "irradiance."),
    ("coherent", "Coherent sources have a constant phase difference.", True,
     "This is the definition of coherent sources."),
    ("tir", "Total internal reflection occurs when the angle of incidence is greater than the "
     "critical angle.", True,
     "All the light is then reflected back into the denser material."),
    ("refr", "When light passes from air into glass, its frequency stays the same.", True,
     "Only the speed and wavelength change."),
    ("refr", "When light passes from air into glass, its wavelength increases.", False,
     "The light slows down with the same frequency, so its wavelength **decreases** (v = fλ)."),
    ("spectra", "Dark lines in the spectrum of a star are caused by certain frequencies being "
     "absorbed in the star's cooler outer atmosphere.", True,
     "This produces an absorption spectrum."),
    ("field", "A charged particle placed in an electric field experiences a force.", True,
     "This is what defines an electric field."),
    ("magfield", "A charged particle moving parallel to a magnetic field experiences no force.", True,
     "A force acts only on a charge moving **across** the field lines."),
    ("magfield", "A charged particle moving parallel to a magnetic field is deflected.", False,
     "There is **no** force on a charge moving parallel to the field, so it carries straight on."),
    ("magdir", "The force on an electron in a magnetic field is in the opposite direction to the force on a proton moving the same way.", True,
     "The charges have opposite signs, so the forces are opposite."),
    ("magdir", "A neutron is deflected by a magnetic field.", False,
     "A neutron has no charge, so a magnetic field has no effect on it."),
    ("wire", "A current-carrying wire is surrounded by a magnetic field.", True,
     "A moving charge produces a magnetic field, and a current is moving charge."),
    ("wire", "The magnetic field around a long straight wire is in straight lines parallel to the wire.", False,
     "The field forms **circles** around the wire."),
    ("wire", "When the current in a wire is reversed, the direction of the magnetic field around it is reversed.", True,
     "The field direction depends on the direction of the current."),
    ("wire", "The direction of the magnetic field around a wire is found from the direction in which the electrons flow.", False,
     "The grip rule uses the **conventional current**, which is opposite to the electron flow."),
    ("barmagnet", "Outside a bar magnet, the magnetic field lines run from the north pole to the south pole.", True,
     "By convention the arrows on field lines point from **N to S** outside a magnet."),
    ("barmagnet", "Outside a bar magnet, the magnetic field lines run from the south pole to the north pole.", False,
     "Outside a magnet the field lines run from **north to south**."),
    ("fieldlines", "The magnetic field is stronger where the field lines are closer together.", True,
     "Field lines are closest together where the field is strongest, for example at the poles of a bar magnet."),
    ("fieldlines", "The magnetic field is weaker where the field lines are closer together.", False,
     "Field lines are **closest** together where the field is **strongest**."),
    ("likepoles", "The magnetic field lines between two like poles run straight from one pole to the other.", False,
     "Like poles repel: the lines **curve away from each other** and never join up. Lines only run between a north pole and a south pole."),
    ("likepoles", "The magnetic field lines between a north pole and a south pole run from the north pole to the south pole.", True,
     "Lines only run **between unlike poles**, from N to S."),
    ("wirefield", "The magnetic field around a long straight wire gets weaker as the distance from the wire increases.", True,
     "The field is strongest close to the wire, so the circular field lines are further apart the further out they are."),
    ("wirefield", "The magnetic field around a long straight wire is the same strength at every distance from the wire.", False,
     "The field gets **weaker** with distance from the wire."),
    ("linac", "The tubes in a linear accelerator get longer because the particles are moving faster.", True,
     "The particles must spend the same time in each tube, so faster particles need longer tubes."),
    ("linac", "The tubes in a linear accelerator get longer because the particles slow down.", False,
     "The particles **speed up** along the accelerator — that is why the tubes lengthen."),
    ("linac", "There is no electric field inside the tubes of a linear accelerator.", True,
     "The particles are accelerated across the gaps between the tubes."),
    ("linac", "The particles in a linear accelerator are accelerated by the electric field inside each tube.", False,
     "The metal tube shields the particles — the acceleration happens in the gaps."),
]

GENERATORS = make_definition_generators("Particles and Waves", DEFINITIONS, STATEMENTS, OVERLAPS)
