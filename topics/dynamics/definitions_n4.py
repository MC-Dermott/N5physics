from utils.definitions import make_definition_generators

# Definitions for the N4 Dynamics and Space unit. See utils/definitions.py for the entry format.


def _d(group, definition, confusables=(), traps=()):
    return {"group": group, "definition": definition, "confusables": list(confusables), "traps": list(traps)}


DEFINITIONS = {
    "average speed": _d("Motion", "The total distance travelled divided by the total time taken.", ["instantaneous speed", "acceleration"]),
    "instantaneous speed": _d("Motion", "The speed at one particular moment.", ["average speed"]),
    "acceleration": _d("Motion", "The change in speed per second.", ["average speed"],
                       [("How fast an object is moving.", "That is **speed**.")]),
    "force": _d("Forces", "A push or a pull, measured in newtons (N).", ["weight"]),
    "mass": _d("Forces", "The amount of matter in an object, measured in kilograms.", ["weight"],
               [("The pull of gravity on an object.", "That is **weight**.")]),
    "weight": _d("Forces", "The force of gravity acting on an object, measured in newtons.", ["mass", "gravitational field strength"]),
    "gravitational field strength": _d("Forces", "The weight per unit mass (N/kg).", ["weight"]),
    "friction": _d("Forces", "A force that opposes motion.", ["force"]),
    "pressure": _d("Forces", "The force acting per unit area.", ["force"], [("The force acting on an object.", "Pressure is force **per unit area**.")]),
    "planet": _d("Space", "A large object that orbits a star.", ["moon", "star"]),
    "moon": _d("Space", "A natural satellite that orbits a planet.", ["planet"]),
    "star": _d("Space", "A large ball of gas that gives out its own light because of nuclear fusion.", ["planet"]),
    "light year": _d("Space", "The distance travelled by light in one year.", ["galaxy"],
                     [("The time it takes light to reach Earth.", "A light year is a **distance**, not a time.")]),
    "galaxy": _d("Space", "A large cluster of stars (plus gas and dust) held together by gravity.", ["star"]),
}
STATEMENTS = [
    ("ly", "A light year is a unit of distance.", True, "The distance light travels in a year."),
    ("ly", "A light year is a unit of time.", False, "It is a **distance**."),
    ("mass", "An astronaut's mass on the Moon is the same as on Earth.", True, "Mass doesn't depend on gravity."),
    ("mass", "An astronaut's weight on the Moon is the same as on Earth.", False, "Weight depends on g, which is smaller on the Moon."),
    ("fric", "Friction always opposes motion.", True, "It acts against the direction of movement."),
    ("bal", "An object moving with balanced forces moves at a constant speed.", True, "No unbalanced force means no acceleration."),
    ("sun", "The Sun is a star.", True, "It gives out its own light."),
    ("sun", "The Moon is a star.", False, "The Moon is a natural satellite; it reflects the Sun's light."),
    ("press", "Pressure increases if the same force acts on a smaller area.", True, "P = F ÷ A."),
    ("accel", "Acceleration is the change in speed per second.", True, "a = (v − u) ÷ t."),
]
GENERATORS = make_definition_generators("Dynamics and Space", DEFINITIONS, STATEMENTS, title="N4 Dynamics and Space Definitions")
