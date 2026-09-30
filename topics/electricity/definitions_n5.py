from utils.definitions import make_definition_generators

# Definitions needed for the N5 Electricity unit, worded as accepted in SQA
# marking instructions. See utils/definitions.py for the entry format.
DEFINITIONS = {
    # ── Charge and current ─────────────────────────────────────────────────────
    "electric current": {
        "group": "Charge and current",
        "definition": "The electric charge transferred per unit time.",
        "confusables": ["electrical power", "potential difference (voltage)"],
        "traps": [("The energy transferred per unit charge.",
                   "That describes **potential difference**. Current is the charge transferred "
                   "per unit time (I = Q ÷ t).")],
    },
    "direct current (d.c.)": {
        "group": "Charge and current",
        "definition": "A current in which the charge carriers flow in one direction only.",
        "confusables": ["alternating current (a.c.)"],
    },
    "alternating current (a.c.)": {
        "group": "Charge and current",
        "definition": "A current in which the charge carriers regularly change their direction "
                      "of flow.",
        "confusables": ["direct current (d.c.)"],
    },
    "electric field": {
        "group": "Charge and current",
        "definition": "A region in which a charged particle experiences a force.",
        "confusables": ["potential difference (voltage)", "electric current"],
    },
    "conductor": {
        "group": "Charge and current",
        "definition": "A material that allows charge (electrons) to move through it easily.",
        "confusables": ["insulator"],
    },
    "insulator": {
        "group": "Charge and current",
        "definition": "A material that does not allow charge to move through it easily.",
        "confusables": ["conductor"],
    },

    # ── Voltage and resistance ─────────────────────────────────────────────────
    "potential difference (voltage)": {
        "group": "Voltage and resistance",
        "definition": "A measure of the energy given to the charge carriers in a circuit "
                      "(1 volt = 1 joule per coulomb).",
        "confusables": ["electric current", "resistance"],
        "traps": [("The charge that flows through a component per second.",
                   "That is **current**. Voltage is the energy given to each coulomb of charge.")],
    },
    "resistance": {
        "group": "Voltage and resistance",
        "definition": "The opposition to the flow of current in a component.",
        "confusables": ["potential difference (voltage)", "insulator"],
    },
    "Ohm's law": {
        "group": "Voltage and resistance",
        "definition": "For a resistor at constant temperature, the current through it is directly "
                      "proportional to the potential difference across it.",
        "confusables": ["resistance"],
        "traps": [("The current through a resistor is inversely proportional to the potential "
                   "difference across it.",
                   "V = IR — for a fixed resistance, doubling V **doubles** I, so they are "
                   "directly proportional.")],
    },
    "series circuit": {
        "group": "Voltage and resistance",
        "definition": "A circuit in which there is only one path for the current.",
        "confusables": ["parallel circuit"],
    },
    "parallel circuit": {
        "group": "Voltage and resistance",
        "definition": "A circuit in which there is more than one path (branch) for the current.",
        "confusables": ["series circuit"],
    },
    "potential divider": {
        "group": "Voltage and resistance",
        "definition": "Two or more resistors connected in series across a supply, so that the "
                      "supply voltage is shared between them.",
        "confusables": ["series circuit"],
    },

    # ── Components ─────────────────────────────────────────────────────────────
    "thermistor": {
        "group": "Components",
        "definition": "A resistor whose resistance decreases as its temperature increases.",
        "confusables": ["light dependent resistor (LDR)"],
    },
    "light dependent resistor (LDR)": {
        "group": "Components",
        "definition": "A resistor whose resistance decreases as the light level increases.",
        "confusables": ["thermistor"],
        "traps": [("A resistor whose resistance increases as the light level increases.",
                   "It is the other way round — **more** light gives **less** resistance.")],
    },
    "transistor": {
        "group": "Components",
        "definition": "An electronic switch that switches on when the voltage across it "
                      "reaches a set value.",
        "confusables": ["fuse", "light emitting diode (LED)"],
    },
    "light emitting diode (LED)": {
        "group": "Components",
        "definition": "A component that gives out light when current flows through it in one "
                      "direction only.",
        "confusables": ["transistor"],
    },
    "fuse": {
        "group": "Components",
        "definition": "A safety device that melts and breaks the circuit if the current becomes "
                      "too large, protecting the flex (cable).",
        "confusables": ["transistor"],
        "traps": [("A safety device that protects the appliance from being damaged by too "
                   "large a voltage.",
                   "A fuse protects the **flex (cable)** — it melts if the **current** becomes "
                   "too large.")],
    },

    # ── Power ──────────────────────────────────────────────────────────────────
    "electrical power": {
        "group": "Power",
        "definition": "The energy transferred per unit time.",
        "confusables": ["electric current", "potential difference (voltage)"],
    },
}

STATEMENTS = [
    # key, statement, correct?, explanation
    ("dc", "In a d.c. circuit the charge carriers flow in one direction only.", True,
     "This is the definition of direct current."),
    ("dc", "The UK mains supply is d.c.", False,
     "The mains supply is **a.c.** — 230 V at a frequency of 50 Hz."),
    ("current", "Current is the electric charge transferred per unit time.", True,
     "I = Q ÷ t."),
    ("current", "Current is the energy given to each coulomb of charge.", False,
     "That describes **potential difference (voltage)**. Current is the charge transferred per "
     "unit time."),
    ("series", "In a series circuit the current is the same at all points.", True,
     "There is only one path, so the same current flows through every component."),
    ("series", "In a series circuit the voltage across each component is the same.", False,
     "In series the supply voltage is **shared** between the components. It is in parallel that "
     "the voltage across each branch is the same."),
    ("parallel", "Adding another resistor in parallel decreases the total resistance.", True,
     "Each extra branch gives the current another path, so the total resistance falls."),
    ("parallel", "Adding another resistor in parallel increases the total resistance.", False,
     "An extra branch gives the current another path, so the total resistance **decreases**."),
    ("sensor", "The resistance of a thermistor decreases as its temperature increases.", True,
     "This is how a thermistor is used as a temperature sensor."),
    ("sensor", "The resistance of an LDR increases as the light level increases.", False,
     "An LDR's resistance **decreases** as the light level increases."),
    ("field", "A charged particle placed in an electric field experiences a force.", True,
     "This is what defines an electric field."),
    ("fuse", "A fuse protects the flex by melting if the current becomes too large.", True,
     "The fuse rating should be just above the normal operating current."),
    ("power", "Power is the energy transferred per unit time.", True,
     "P = E ÷ t, measured in watts (J/s)."),
    ("power", "Power is the energy transferred per unit charge.", False,
     "Energy per unit charge is **voltage**. Power is the energy transferred per unit time."),
]

GENERATORS = make_definition_generators("Electricity", DEFINITIONS, STATEMENTS)
