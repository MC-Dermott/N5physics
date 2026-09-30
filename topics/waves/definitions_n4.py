from utils.definitions import make_definition_generators

# Definitions for the N4 Waves and Radiation unit. See utils/definitions.py for the entry format.


def _d(group, definition, confusables=(), traps=()):
    return {"group": group, "definition": definition, "confusables": list(confusables), "traps": list(traps)}


DEFINITIONS = {
    "wave": _d("Waves", "A way of transferring energy without transferring matter."),
    "frequency": _d("Waves", "The number of waves passing a point per second.", ["wavelength", "amplitude"],
                    [("The time taken for one wave to pass a point.", "That is the **period**.")]),
    "wavelength": _d("Waves", "The distance between one crest and the next crest.", ["amplitude"]),
    "amplitude": _d("Waves", "The height of a wave from the rest position to a crest.", ["wavelength"]),
    "transverse wave": _d("Waves", "A wave where the vibrations are at right angles to the direction of travel.", ["longitudinal wave"]),
    "longitudinal wave": _d("Waves", "A wave where the vibrations are along (parallel to) the direction of travel.", ["transverse wave"]),
    "electromagnetic spectrum": _d("Light and the EM spectrum", "The family of transverse waves that all travel at the speed of light, from radio waves to gamma rays.",
                                   ["wave"]),
    "ionisation": _d("Nuclear radiation", "When an atom gains or loses electrons and becomes charged.", ["activity"],
                     [("When a nucleus splits into two.", "That is **fission**. Ionisation involves electrons.")]),
    "half-life": _d("Nuclear radiation", "The time taken for the activity of a radioactive source to fall to half its original value.",
                    ["activity"], [("Half the time taken for a source to stop being radioactive.", "It is the time for the **activity to halve**.")]),
    "activity": _d("Nuclear radiation", "The number of nuclei that decay per second, measured in becquerels (Bq).", ["half-life"]),
    "background radiation": _d("Nuclear radiation", "Radiation that is around us all the time from natural and man-made sources.", ["ionisation"]),
    "absorbed dose": _d("Nuclear radiation", "The energy absorbed per kilogram of absorbing material, measured in grays (Gy).", ["equivalent dose"]),
    "equivalent dose": _d("Nuclear radiation", "A measure of the biological effect of radiation, measured in sieverts (Sv).", ["absorbed dose"]),
}
STATEMENTS = [
    ("em", "All electromagnetic waves travel at the same speed in air.", True, "The speed of light, 3 × 10⁸ m/s."),
    ("em", "Gamma rays travel faster than radio waves.", False, "All EM waves travel at the **same** speed."),
    ("sound", "Sound is a longitudinal wave.", True, "The vibrations are along the direction of travel."),
    ("alpha", "Alpha radiation is stopped by a sheet of paper.", True, "It is the least penetrating."),
    ("alpha", "Gamma radiation is stopped by a sheet of paper.", False, "Gamma needs thick lead or concrete to reduce it."),
    ("ion", "Alpha radiation causes the most ionisation.", True, "It has the greatest charge and mass."),
    ("hl", "After two half-lives the activity has fallen to a quarter of its original value.", True, "½ × ½ = ¼."),
    ("hl", "After two half-lives the source is no longer radioactive.", False, "The activity is a **quarter** of the original, not zero."),
    ("bg", "Background radiation comes from natural and man-made sources.", True, "Rocks, cosmic rays, medical sources…"),
    ("act", "Activity is measured in becquerels.", True, "1 Bq = one decay per second."),
]
GENERATORS = make_definition_generators("Waves and Radiation", DEFINITIONS, STATEMENTS, title="N4 Waves and Radiation Definitions")
