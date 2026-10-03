from utils.definitions import make_definition_generators

# Definitions needed for the N5 Waves unit, worded as accepted in SQA marking
# instructions. See utils/definitions.py for the entry format.
DEFINITIONS = {
    # ── Wave properties ────────────────────────────────────────────────────────
    "wave": {
        "group": "Wave properties",
        "definition": "A way of transferring energy from one place to another without "
                      "transferring matter.",
        "confusables": ["wave speed"],
    },
    "transverse wave": {
        "group": "Wave properties",
        "definition": "A wave in which the particles vibrate at right angles to the direction "
                      "the wave travels.",
        "confusables": ["longitudinal wave"],
    },
    "longitudinal wave": {
        "group": "Wave properties",
        "definition": "A wave in which the particles vibrate parallel to the direction the wave "
                      "travels.",
        "confusables": ["transverse wave"],
    },
    "frequency": {
        "group": "Wave properties",
        "definition": "The number of waves passing a point per second.",
        "confusables": ["period", "wave speed"],
        "traps": [("The time taken for one complete wave to pass a point.",
                   "That is the **period**. Frequency is the number of waves per second "
                   "(f = 1 ÷ T).")],
    },
    "period": {
        "group": "Wave properties",
        "definition": "The time taken for one complete wave to pass a point.",
        "confusables": ["frequency"],
    },
    "wavelength": {
        "group": "Wave properties",
        "definition": "The distance between one crest and the next crest (or between two "
                      "corresponding points) of a wave.",
        "confusables": ["amplitude"],
        "traps": [("The distance between a crest and the next trough.",
                   "Crest to next trough is only **half** a wavelength.")],
    },
    "amplitude": {
        "group": "Wave properties",
        "definition": "The maximum displacement of a particle from its rest position.",
        "confusables": ["wavelength"],
        "traps": [("The vertical distance from a crest to a trough.",
                   "Crest to trough is **twice** the amplitude — amplitude is measured from the "
                   "rest position.")],
    },
    "wave speed": {
        "group": "Wave properties",
        "definition": "The distance travelled by a wave per unit time.",
        "confusables": ["frequency"],
    },
    "diffraction": {
        "group": "Wave properties",
        "definition": "The bending of waves around an obstacle or through a gap.",
        "confusables": ["refraction"],
        "traps": [("The bending of a wave as it passes from one material into another.",
                   "That is **refraction**. Diffraction is waves bending round obstacles or "
                   "spreading out through gaps.")],
    },

    # ── Light and the EM spectrum ──────────────────────────────────────────────
    "electromagnetic spectrum": {
        "group": "Light and the electromagnetic spectrum",
        "definition": "The family of transverse waves that all travel at 3.0 × 10⁸ m/s in a "
                      "vacuum, arranged in order of wavelength.",
        "confusables": ["transverse wave"],
    },
    "refraction": {
        "group": "Light and the electromagnetic spectrum",
        "definition": "The change in speed of a wave as it passes from one medium into another.",
        "confusables": ["diffraction"],
    },
    "normal": {
        "group": "Light and the electromagnetic spectrum",
        "definition": "A line drawn at 90° to a boundary at the point where a ray meets it.",
        "confusables": ["angle of incidence", "angle of refraction"],
    },
    "angle of incidence": {
        "group": "Light and the electromagnetic spectrum",
        "definition": "The angle between the incident ray and the normal.",
        "confusables": ["angle of refraction", "normal"],
        "traps": [("The angle between the incident ray and the surface of the boundary.",
                   "Angles in ray diagrams are always measured from the **normal**, not the "
                   "surface.")],
    },
    "angle of refraction": {
        "group": "Light and the electromagnetic spectrum",
        "definition": "The angle between the refracted ray and the normal.",
        "confusables": ["angle of incidence", "normal"],
    },
}

STATEMENTS = [
    # key, statement, correct?, explanation
    ("type", "Sound is a longitudinal wave.", True,
     "The air particles vibrate parallel to the direction the sound travels."),
    ("type", "Light is a longitudinal wave.", False,
     "Light — like all electromagnetic waves — is a **transverse** wave."),
    ("em", "All electromagnetic waves travel at 3.0 × 10⁸ m/s in a vacuum.", True,
     "They all travel at the speed of light in a vacuum."),
    ("em", "Radio waves have a higher frequency than X-rays.", False,
     "Radio waves have the **lowest** frequency (longest wavelength) in the EM spectrum."),
    ("diffraction", "Long wavelength waves diffract more than short wavelength waves.", True,
     "This is why long-wave radio signals bend round hills better than short-wave signals."),
    ("refraction", "When light travels from air into glass, its speed decreases.", True,
     "Light slows down in the denser material."),
    ("refraction", "When light refracts, its frequency changes.", False,
     "The frequency stays the **same** — it is the speed and wavelength that change."),
    ("period", "The period is the time taken for one complete wave to pass a point.", True,
     "T = 1 ÷ f."),
    ("energy", "Waves transfer energy without transferring matter.", True,
     "This is what a wave is."),
    ("amplitude", "The amplitude of a wave is the distance from a crest to a trough.", False,
     "Crest to trough is twice the amplitude. Amplitude is measured from the **rest position**."),
    ("normal", "The angle of refraction is measured between the refracted ray and the "
     "normal.", True,
     "All angles in ray diagrams are measured from the normal."),
    ("normal", "The angle of refraction is measured between the refracted ray and the surface "
     "of the glass.", False,
     "Angles are measured from the **normal**, not the surface."),
    ("refr_freq", "When light passes from air into glass its frequency stays the same.", True,
     "Only the speed and wavelength change on refraction (course reports 2018, 2024)."),
    ("refr_freq", "When light passes from air into glass its frequency decreases.", False,
     "The frequency **never** changes on refraction — the speed and wavelength decrease."),
    ("diff_wl", "Radio waves diffract more than microwaves around a hill.", True,
     "Radio waves have the longer wavelength, and longer wavelengths diffract more."),
    ("em_speed", "In a vacuum, gamma rays travel faster than radio waves.", False,
     "All electromagnetic waves travel at the same speed, 3.0 × 10⁸ m/s."),
]

GENERATORS = make_definition_generators("Waves", DEFINITIONS, STATEMENTS)
