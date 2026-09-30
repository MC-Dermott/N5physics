from utils.definitions import make_definition_generators

# Definitions for the S3 (BGE) Waves unit. See utils/definitions.py for the entry format.


def _d(group, definition, confusables=(), traps=()):
    return {"group": group, "definition": definition, "confusables": list(confusables), "traps": list(traps)}


DEFINITIONS = {
    "wave": _d("Waves", "A way of transferring energy from one place to another without transferring matter."),
    "transverse wave": _d("Types of wave", "A wave in which the particles vibrate at right angles to the direction the wave travels.",
                          ["longitudinal wave"]),
    "longitudinal wave": _d("Types of wave", "A wave in which the particles vibrate parallel to the direction the wave travels.",
                            ["transverse wave"]),
    "frequency": _d("Describing waves", "The number of waves passing a point per second, measured in hertz (Hz).", ["period"],
                    [("The time taken for one wave to pass a point.", "That is the **period**; frequency is waves per second.")]),
    "period": _d("Describing waves", "The time taken for one complete wave to pass a point.", ["frequency"]),
    "wavelength": _d("Describing waves", "The distance between one crest and the next crest.", ["amplitude"],
                     [("The distance between a crest and a trough.", "That is only **half** a wavelength.")]),
    "amplitude": _d("Describing waves", "The height of a wave from its rest position to a crest (or trough).", ["wavelength"],
                    [("The height from a trough to a crest.", "That is **twice** the amplitude.")]),
    "wave speed": _d("Describing waves", "The distance travelled by a wave per second.", ["frequency"]),
    "crest": _d("Parts of a wave", "The highest point of a transverse wave.", ["trough"]),
    "trough": _d("Parts of a wave", "The lowest point of a transverse wave.", ["crest"]),
}
STATEMENTS = [
    ("energy", "Waves transfer energy without transferring matter.", True, "That is what a wave does."),
    ("sound", "Sound is a longitudinal wave.", True, "The air particles vibrate back and forth along the direction of travel."),
    ("sound", "Sound is a transverse wave.", False, "Sound is **longitudinal**."),
    ("light", "Light is a transverse wave.", True, "All electromagnetic waves are transverse."),
    ("freq", "Frequency is the number of waves per second.", True, "Measured in Hz."),
    ("freq", "Frequency is measured in metres.", False, "Frequency is in hertz; **wavelength** is in metres."),
    ("amp", "The amplitude is measured from the rest position to a crest.", True, "Not crest to trough."),
    ("amp", "The amplitude is the distance from a crest to a trough.", False, "That is twice the amplitude."),
    ("speed", "Wave speed = frequency × wavelength.", True, "v = fλ."),
    ("period", "The period is the time for one wave to pass a point.", True, "T = 1 ÷ f."),
]
GENERATORS = make_definition_generators("Waves", DEFINITIONS, STATEMENTS, title="S3 Waves Definitions")
