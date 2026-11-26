"""Definitions bank for AH Rotational Motion and Astrophysics. See utils/definitions.py for the format."""
from utils.definitions import make_definition_generators

DEFINITIONS = {
    # ── Rotational motion ──
    "moment of inertia": {
        "group": "Rotational motion",
        "definition": "A measure of an object's resistance to angular acceleration about a given axis.",
        "confusables": ["torque", "angular momentum", "angular acceleration"],
        "traps": [("A measure of an object's resistance to linear acceleration.",
                   "That is the role of mass. Moment of inertia is about **angular** acceleration about an axis.")],
    },
    "torque": {
        "group": "Rotational motion",
        "definition": "The turning effect of a force: the perpendicular force multiplied by the distance from the axis.",
        "confusables": ["moment of inertia", "angular momentum", "centripetal force"],
    },
    "angular velocity": {
        "group": "Rotational motion",
        "definition": "The rate of change of angular displacement.",
        "confusables": ["angular acceleration", "angular displacement"],
    },
    "angular acceleration": {
        "group": "Rotational motion",
        "definition": "The rate of change of angular velocity.",
        "confusables": ["angular velocity", "centripetal acceleration"],
    },
    "angular displacement": {
        "group": "Rotational motion",
        "definition": "The angle turned through about an axis, measured in radians.",
        "confusables": ["angular velocity"],
    },
    "angular momentum": {
        "group": "Rotational motion",
        "definition": "The product of an object's moment of inertia and its angular velocity.",
        "confusables": ["moment of inertia", "torque"],
    },
    "conservation of angular momentum": {
        "group": "Rotational motion",
        "definition": "The total angular momentum is conserved in the absence of external torques.",
        "confusables": [],
        "traps": [("The total angular momentum of a system is always conserved.",
                   "The condition is needed: **in the absence of external torques**.")],
    },
    "centripetal force": {
        "group": "Rotational motion",
        "definition": "The force towards the centre needed to keep an object moving in a circle.",
        "confusables": ["torque", "centripetal acceleration"],
        "traps": [("The force acting outwards on an object moving in a circle.",
                   "The force needed for circular motion is **towards the centre**.")],
    },
    "centripetal acceleration": {
        "group": "Rotational motion",
        "definition": "The acceleration towards the centre of an object moving in a circle.",
        "confusables": ["angular acceleration", "centripetal force"],
    },
    # ── Gravitation ──
    "gravitational field strength": {
        "group": "Gravitation",
        "definition": "The gravitational force acting on a unit mass.",
        "confusables": ["gravitational potential", "escape velocity"],
    },
    "gravitational potential": {
        "group": "Gravitation",
        "definition": "The work done in moving unit mass from infinity to that point.",
        "confusables": ["gravitational field strength", "escape velocity"],
        "traps": [("The work done in moving unit mass from that point to infinity.",
                   "The direction matters: **from infinity to the point**.")],
    },
    "escape velocity": {
        "group": "Gravitation",
        "definition": "The minimum velocity that allows a mass to escape a gravitational field to infinity.",
        "confusables": ["gravitational potential", "gravitational field strength"],
        "traps": [("The velocity needed for a mass to stay in a circular orbit.",
                   "That is the orbital velocity. Escape velocity takes the mass to infinity.")],
    },
    # ── General relativity ──
    "equivalence principle": {
        "group": "General relativity",
        "definition": "An observer cannot distinguish between the effects of a uniform gravitational field and a constant acceleration.",
        "confusables": ["spacetime"],
        "traps": [("An observer cannot distinguish between a uniform gravitational field and a constant velocity.",
                   "It is a constant **acceleration**.")],
    },
    "inertial frame of reference": {
        "group": "General relativity",
        "definition": "A frame of reference which is not accelerating.",
        "confusables": ["non-inertial frame of reference"],
    },
    "non-inertial frame of reference": {
        "group": "General relativity",
        "definition": "A frame of reference which is accelerating.",
        "confusables": ["inertial frame of reference"],
    },
    "spacetime": {
        "group": "General relativity",
        "definition": "A unified representation of three dimensions of space and one dimension of time.",
        "confusables": ["geodesic", "world line"],
    },
    "geodesic": {
        "group": "General relativity",
        "definition": "The shortest path between two points in spacetime.",
        "confusables": ["world line", "spacetime"],
    },
    "world line": {
        "group": "General relativity",
        "definition": "The path of an object drawn on a spacetime diagram.",
        "confusables": ["geodesic"],
    },
    "Schwarzschild radius": {
        "group": "General relativity",
        "definition": "The distance from the centre (singularity) of a black hole to its event horizon.",
        "confusables": ["event horizon"],
        "traps": [("The radius of the singularity at the centre of a black hole.",
                   "It is the distance from the singularity to the **event horizon**.")],
    },
    "event horizon": {
        "group": "General relativity",
        "definition": "The boundary around a black hole at which the escape velocity equals the speed of light.",
        "confusables": ["Schwarzschild radius"],
    },
    # ── Stellar physics ──
    "luminosity": {
        "group": "Stellar physics",
        "definition": "The total power radiated by a star.",
        "confusables": ["apparent brightness", "black body"],
    },
    "apparent brightness": {
        "group": "Stellar physics",
        "definition": "The power per unit area received from a star at the observer.",
        "confusables": ["luminosity"],
        "traps": [("The total power emitted by a star.",
                   "That is the **luminosity**. Apparent brightness is power per unit area at the observer.")],
    },
    "black body": {
        "group": "Stellar physics",
        "definition": "An ideal object which absorbs all the radiation that falls on it.",
        "confusables": ["luminosity"],
    },
    "light-year": {
        "group": "Stellar physics",
        "definition": "The distance travelled by light in one year.",
        "confusables": ["astronomical unit"],
    },
    "astronomical unit": {
        "group": "Stellar physics",
        "definition": "A unit of distance equal to the mean distance from the Earth to the Sun.",
        "confusables": ["light-year"],
    },
}

STATEMENTS = [
    ("moi", "Moment of inertia depends on the mass of an object and how that mass is distributed about the axis.", True,
     "both the mass and its distribution matter."),
    ("moi", "The moment of inertia of an object is the same about any axis.", False,
     "it depends on the axis, e.g. a rod about its centre and about its end."),
    ("torque", "An unbalanced torque produces an angular acceleration.", True, "τ = Iα."),
    ("torque", "An unbalanced torque is needed to keep an object rotating at constant angular velocity.", False,
     "at constant angular velocity the unbalanced torque is zero."),
    ("centre", "The centripetal force on an object in circular motion acts towards the centre of the circle.", True,
     "it causes the centripetal acceleration."),
    ("centre", "An object moving in a circle at constant speed has no acceleration.", False,
     "its direction is changing, so it is accelerating towards the centre."),
    ("potential", "Gravitational potential is zero at infinity.", True, "this is the chosen zero."),
    ("potential", "Gravitational potential increases to large positive values close to a planet.", False,
     "it is negative, and more negative closer to the planet."),
    ("path", "The energy needed to move a mass between two points in a gravitational field does not depend on the path.", True,
     "only the end points matter."),
    ("escape", "The escape velocity from a planet depends on the mass of the escaping object.", False,
     "the object's mass cancels."),
    ("escape", "At the event horizon of a black hole the escape velocity equals the speed of light.", True,
     "this defines the event horizon."),
    ("frames", "General relativity deals with non-inertial frames of reference.", True, "special relativity deals with inertial frames."),
    ("clock", "A clock runs more slowly lower in a gravitational field.", True, "a consequence of the equivalence principle."),
    ("clock", "A clock runs more slowly higher in a gravitational field.", False, "it runs faster higher up."),
    ("hr", "On a Hertzsprung–Russell diagram, surface temperature increases from left to right.", False,
     "temperature decreases from left to right."),
    ("fusion", "Main sequence stars fuse hydrogen in their cores.", True, "this is what puts them on the main sequence."),
    ("lifetime", "A more massive star has a longer lifetime than a less massive one.", False,
     "it uses its fuel much faster, so its lifetime is shorter."),
]

rotational_motion_ah_definitions = make_definition_generators(
    "Rotational Motion and Astrophysics", DEFINITIONS, STATEMENTS)
