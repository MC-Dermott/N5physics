from utils.definitions import make_definition_generators

# Definitions for the N4 Electricity and Energy unit. See utils/definitions.py for the entry format.


def _d(group, definition, confusables=(), traps=()):
    return {"group": group, "definition": definition, "confusables": list(confusables), "traps": list(traps)}


DEFINITIONS = {
    "conservation of energy": _d("Energy", "Energy cannot be created or destroyed, only changed from one form into another.", ["efficiency"]),
    "efficiency": _d("Energy", "The percentage of the input energy (or power) that is transferred into useful output energy.",
                     ["power", "conservation of energy"],
                     [("The total output energy of a device.", "Efficiency compares the USEFUL output with the INPUT.")]),
    "power": _d("Energy", "The energy transferred per second.", ["efficiency", "energy"], [("The total energy used by a device.", "Power is energy **per second**.")]),
    "renewable energy source": _d("Generating electricity", "An energy source that will not run out, such as wind, solar or hydroelectric.",
                                  ["non-renewable energy source"]),
    "non-renewable energy source": _d("Generating electricity", "An energy source that will run out, such as coal, oil, gas or nuclear fuel.",
                                      ["renewable energy source"]),
    "current": _d("Circuits", "The flow of charge (electrons) around a circuit, measured in amperes (A).", ["voltage", "resistance"]),
    "voltage": _d("Circuits", "A measure of the energy given to the charges in a circuit, measured in volts (V).", ["current"]),
    "resistance": _d("Circuits", "The opposition to the flow of current in a circuit, measured in ohms (Ω).", ["current"]),
    "series circuit": _d("Circuits", "A circuit with only one path for the current.", ["parallel circuit"]),
    "parallel circuit": _d("Circuits", "A circuit with more than one path (branch) for the current.", ["series circuit"]),
    "input device": _d("Electronics", "A component that changes a physical quantity (e.g. light, heat) into an electrical signal.", ["output device"]),
    "output device": _d("Electronics", "A component that changes an electrical signal into another form of energy (e.g. light, sound, movement).",
                        ["input device"]),
    "electromagnet": _d("Electromagnetism", "A coil of wire, usually round an iron core, that becomes magnetic when a current flows through it.", ["current"]),
}
STATEMENTS = [
    ("cons", "Energy cannot be created or destroyed.", True, "Conservation of energy."),
    ("eff", "No real device can be 100% efficient.", True, "Some energy is always wasted, usually as heat."),
    ("eff", "An efficient device wastes a lot of energy as heat.", False, "An efficient device wastes **little** energy."),
    ("renew", "Wind and solar power are renewable energy sources.", True, "They won't run out."),
    ("renew", "Coal is a renewable energy source.", False, "Fossil fuels will run out — non-renewable."),
    ("series", "In a series circuit the current is the same at all points.", True, "There is only one path."),
    ("par", "In a parallel circuit the voltage across each branch is the same as the supply voltage.", True, "Each branch connects directly across the supply."),
    ("meter", "An ammeter is connected in series with a component.", True, "Current flows through it."),
    ("meter", "A voltmeter is connected in series with a component.", False, "A voltmeter goes in **parallel** (across the component)."),
    ("emag", "Increasing the current makes an electromagnet stronger.", True, "So does adding more turns of wire."),
    ("ldr", "An LDR is an input device.", True, "It responds to light."),
    ("ldr", "An LED is an input device.", False, "An LED gives out light — an **output** device."),
]
GENERATORS = make_definition_generators("Electricity and Energy", DEFINITIONS, STATEMENTS, title="N4 Electricity and Energy Definitions")
