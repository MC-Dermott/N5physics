from utils.definitions import make_definition_generators

# Definitions for the S3 (BGE) Dynamics units, worded to match the N5 marking-instruction
# wording pupils will meet later. See utils/definitions.py for the entry format.


def _d(group, definition, confusables=(), traps=()):
    return {"group": group, "definition": definition, "confusables": list(confusables), "traps": list(traps)}


MOTION_DEFINITIONS = {
    "speed": _d("Speed", "The distance travelled per unit time (per second).", ["acceleration", "average speed"]),
    "average speed": _d("Speed", "The total distance travelled divided by the total time taken.",
                        ["instantaneous speed", "speed"],
                        [("The speed at one particular instant.", "That is the **instantaneous** speed.")]),
    "instantaneous speed": _d("Speed", "The speed of an object at one particular instant (point in time).",
                              ["average speed"],
                              [("The total distance divided by the total time.", "That is the **average** speed.")]),
    "acceleration": _d("Acceleration", "The change in speed per unit time (per second).", ["speed", "deceleration"],
                       [("How fast an object is moving.", "That is **speed**. Acceleration is how quickly the speed CHANGES.")]),
    "deceleration": _d("Acceleration", "A decrease in speed per unit time — a negative acceleration.", ["acceleration"]),
    "light gate": _d("Measuring speed", "A sensor that times how long a card on a moving object takes to pass through a beam of light.",
                     ["stopwatch"]),
    "stopwatch": _d("Measuring speed", "A hand-operated timer, which includes the reaction time of the person using it.", ["light gate"]),
    "velocity-time graph": _d("Graphs", "A graph showing how an object's speed changes with time; the area under it gives the distance travelled.",
                              ["gradient"]),
    "gradient": _d("Graphs", "The steepness of a line on a graph; on a speed-time graph it gives the acceleration.", ["velocity-time graph"]),
}
MOTION_STATEMENTS = [
    ("avg", "Average speed is total distance divided by total time.", True, "d = v̄t with the whole journey."),
    ("avg", "Average speed is the speed at one particular moment.", False, "That is the **instantaneous** speed."),
    ("gate", "A light gate gives a more accurate time than a stopwatch.", True, "There is no human reaction time."),
    ("gate", "To find instantaneous speed you need the length of the card and the time it takes to pass through the light gate.", True,
     "Instantaneous speed = card length ÷ time in the gate."),
    ("accel", "Acceleration is the change in speed divided by the time taken.", True, "a = Δv ÷ t."),
    ("accel", "An object moving at a steady speed is accelerating.", False, "A steady speed means **no** acceleration."),
    ("area", "The area under a speed-time graph gives the distance travelled.", True, "Area = speed × time."),
    ("area", "The gradient of a speed-time graph gives the distance travelled.", False, "The gradient gives the **acceleration**; the area gives distance."),
    ("unit", "Acceleration is measured in m/s².", True, "Metres per second, per second."),
    ("unit", "Acceleration is measured in m/s.", False, "m/s is the unit of **speed**."),
]

FORCES_DEFINITIONS = {
    "force": _d("Forces", "A push or a pull, measured in newtons (N).", ["weight"]),
    "mass": _d("Mass and weight", "The amount of matter in an object, measured in kilograms (kg).", ["weight"],
               [("The force of gravity acting on an object.", "That is **weight**. Mass is the amount of matter.")]),
    "weight": _d("Mass and weight", "The force of gravity acting on an object, measured in newtons (N).", ["mass", "gravitational field strength"],
                 [("The amount of matter in an object.", "That is **mass**. Weight is a force, measured in N.")]),
    "gravitational field strength": _d("Mass and weight", "The weight per unit mass (the force of gravity on each kilogram).", ["weight"]),
    "friction": _d("Forces", "A force that opposes motion between two surfaces (or through air or water).", ["air resistance"]),
    "air resistance": _d("Forces", "The frictional force on an object moving through air.", ["friction"]),
    "balanced forces": _d("Balanced and unbalanced forces", "Forces that are equal in size and opposite in direction, so there is no overall (unbalanced) force.",
                          ["unbalanced force"],
                          [("Forces that make an object stop moving.", "Balanced forces mean **constant speed** (or staying still), not stopping.")]),
    "unbalanced force": _d("Balanced and unbalanced forces", "The overall force on an object when the forces acting on it do not cancel out; it causes acceleration.",
                           ["balanced forces"]),
}
FORCES_STATEMENTS = [
    ("mass", "An astronaut's mass is the same on the Moon as on Earth.", True, "Mass is the amount of matter — it doesn't change."),
    ("mass", "An astronaut's weight is the same on the Moon as on Earth.", False, "g is smaller on the Moon, so the weight is less."),
    ("weight", "Weight is measured in newtons.", True, "Weight is a force."),
    ("weight", "Weight is measured in kilograms.", False, "**Mass** is measured in kg; weight in N."),
    ("balanced", "When the forces on a moving car are balanced it moves at a constant speed.", True, "Balanced forces — no acceleration."),
    ("balanced", "When the forces on a moving car are balanced it slows down and stops.", False, "Balanced forces mean **constant speed**."),
    ("unbal", "An unbalanced force causes an object to accelerate.", True, "F = ma."),
    ("friction", "Friction always acts in the opposite direction to the motion.", True, "It opposes motion."),
    ("friction", "Streamlining a car increases air resistance.", False, "Streamlining **reduces** air resistance."),
]

MOTION_GENERATORS = make_definition_generators("Dynamics (Motion)", MOTION_DEFINITIONS, MOTION_STATEMENTS,
                                               title="S3 Motion Definitions")
FORCES_GENERATORS = make_definition_generators("Dynamics (Forces)", FORCES_DEFINITIONS, FORCES_STATEMENTS,
                                               title="S3 Forces Definitions")
