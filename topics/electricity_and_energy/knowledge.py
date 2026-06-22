import random
from core.models.question_model import PhysicsQuestion

_NOTES = """
## Electricity and Energy: Key Knowledge

### Renewable and Non-Renewable Energy

**Renewable** sources will not run out and do not burn fuel:
wind, solar, hydroelectric, wave, tidal, geothermal, biomass

**Non-renewable** sources will eventually run out:
coal, oil, natural gas, nuclear

| Source | Advantage | Disadvantage |
|---|---|---|
| Wind | Free fuel; no CO₂ emissions | Unreliable — depends on wind speed |
| Solar | Free fuel; no CO₂ emissions | Only works in daylight / clear conditions |
| Hydroelectric | Reliable; can generate on demand | High setup cost; flooding of valley |
| Wave | Free fuel; no CO₂ emissions | High setup cost; affects marine environment |

### Input and Output Devices

| Type | Description | Examples |
|---|---|---|
| Digital input | Has only two states (on/off) | switch, push switch |
| Analogue input | Gives a continuous range of values | LDR, thermistor, microphone |
| Digital output | Operates in two states only | relay, LED |
| Analogue output | Produces a continuous range | loudspeaker, lamp, motor, buzzer |

### Electromagnets
- An electromagnet can be **switched on and off** (a permanent magnet cannot).
- Used in scrapyards: switched off to **release** the lifted materials.
- Components needed: **battery + coils of wire + switch**
"""


def _make_classification(question_text, correct, distractors, notes=_NOTES,
                         topic="Electricity and Energy", question_type="", level="N4"):
    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)
    return PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        distractors=[{"value": d["value"], "mistake": d["mistake"], "working": []} for d in distractors],
        working=[{"type": "text", "content": f"The correct answer is: **{correct}**"}],
        notes=notes,
        topic=topic,
        question_type=question_type,
        level=level,
        metadata={"type": "classification", "options": options},
    )


# ── Renewable Energy ───────────────────────────────────────────────────────────

_RENEWABLES = ["wind", "solar", "hydroelectric", "wave", "tidal", "geothermal"]
_NON_RENEWABLES = ["coal", "oil", "natural gas", "nuclear"]

_SOURCE_DATA = [
    {
        "name": "wind",
        "advantage": "The fuel (wind) is free and produces no CO₂ emissions",
        "disadvantage": "Output is unreliable as it depends on wind speed",
        "fake_advantages": [
            "It generates electricity at a constant rate at all times",
            "It has very low initial construction costs",
        ],
        "fake_disadvantages": [
            "It produces large amounts of CO₂",
            "The fuel is expensive and will eventually run out",
        ],
    },
    {
        "name": "solar",
        "advantage": "The fuel is free and produces no greenhouse gas emissions",
        "disadvantage": "It only generates electricity during daylight hours in clear conditions",
        "fake_advantages": [
            "It generates electricity equally well at night and during the day",
            "It has the lowest setup cost of all energy sources",
        ],
        "fake_disadvantages": [
            "It burns fossil fuels to produce electricity",
            "It produces radioactive waste that must be stored safely",
        ],
    },
    {
        "name": "hydroelectric",
        "advantage": "It can reliably generate electricity on demand",
        "disadvantage": "Construction costs are high and building the dam floods the surrounding valley",
        "fake_advantages": [
            "It can be built in any location without affecting the environment",
            "It has zero initial setup costs",
        ],
        "fake_disadvantages": [
            "It burns coal or gas to generate electricity",
            "The output is unreliable because water flow is unpredictable",
        ],
    },
    {
        "name": "wave",
        "advantage": "The energy source is free and produces no CO₂ emissions",
        "disadvantage": "Setup costs are high and generators can affect marine wildlife",
        "fake_advantages": [
            "The output is perfectly constant in all sea conditions",
            "It has very low setup costs compared to other sources",
        ],
        "fake_disadvantages": [
            "It produces carbon dioxide when generating electricity",
            "The fuel will run out within the next 50 years",
        ],
    },
]


def gen_identify_renewable(level="N4"):
    renewable = random.choice(_RENEWABLES)
    non_renewables = random.sample(_NON_RENEWABLES, 3)
    distractors = [
        {"value": nr, "mistake": f"{nr.capitalize()} is a non-renewable source — it will eventually run out."}
        for nr in non_renewables
    ]
    return _make_classification(
        "Which of the following is a **renewable** source of energy?",
        renewable, distractors,
        question_type="Renewable Energy", level=level,
    )


def gen_identify_non_renewable(level="N4"):
    non_renewable = random.choice(_NON_RENEWABLES)
    renewables = random.sample(_RENEWABLES, 3)
    distractors = [
        {"value": r, "mistake": f"{r.capitalize()} is a renewable source — it will not run out."}
        for r in renewables
    ]
    return _make_classification(
        "Which of the following is a **non-renewable** source of energy?",
        non_renewable, distractors,
        question_type="Renewable Energy", level=level,
    )


def gen_renewable_advantage(level="N4"):
    source = random.choice(_SOURCE_DATA)
    fake_adv = random.choice(source["fake_advantages"])
    other_source = random.choice([s for s in _SOURCE_DATA if s["name"] != source["name"]])
    distractors = [
        {"value": source["disadvantage"],
         "mistake": f"This is a disadvantage of {source['name']} energy, not an advantage."},
        {"value": fake_adv,
         "mistake": f"This statement about {source['name']} energy is not correct."},
        {"value": other_source["disadvantage"],
         "mistake": f"This is a disadvantage of {other_source['name']} energy."},
    ]
    return _make_classification(
        f"Which of the following is an **advantage** of **{source['name']}** energy?",
        source["advantage"], distractors,
        question_type="Renewable Energy", level=level,
    )


def gen_renewable_disadvantage(level="N4"):
    source = random.choice(_SOURCE_DATA)
    fake_dis = random.choice(source["fake_disadvantages"])
    other_source = random.choice([s for s in _SOURCE_DATA if s["name"] != source["name"]])
    distractors = [
        {"value": source["advantage"],
         "mistake": f"This is an advantage of {source['name']} energy, not a disadvantage."},
        {"value": fake_dis,
         "mistake": f"This statement about {source['name']} energy is not correct."},
        {"value": other_source["advantage"],
         "mistake": f"This is an advantage of {other_source['name']} energy."},
    ]
    return _make_classification(
        f"Which of the following is a **disadvantage** of **{source['name']}** energy?",
        source["disadvantage"], distractors,
        question_type="Renewable Energy", level=level,
    )


_RENEWABLE_GENS = [
    gen_identify_renewable,
    gen_identify_non_renewable,
    gen_renewable_advantage,
    gen_renewable_disadvantage,
]


def generate_renewable_energy(level="N4"):
    return random.choice(_RENEWABLE_GENS)(level=level)


# ── Input / Output Devices ─────────────────────────────────────────────────────

_DIGITAL_INPUTS  = ["switch", "push switch"]
_ANALOGUE_INPUTS = ["LDR (light dependent resistor)", "thermistor", "microphone"]
_DIGITAL_OUTPUTS = ["relay", "LED"]
_ANALOGUE_OUTPUTS = ["loudspeaker", "lamp", "motor", "buzzer"]

_DEVICE_TYPE_LABELS = {
    "digital input":   "a digital input device",
    "analogue input":  "an analogue input device",
    "digital output":  "a digital output device",
    "analogue output": "an analogue output device",
}

_DEVICE_MISTAKES = {
    "digital input":   "Digital inputs have only two states (on/off), such as a switch.",
    "analogue input":  "Analogue inputs give a continuous range of values, such as an LDR.",
    "digital output":  "Digital outputs operate in two states only, such as a relay.",
    "analogue output": "Analogue outputs produce a continuous range, such as a loudspeaker.",
}

_ALL_DEVICES = {
    "digital input":   _DIGITAL_INPUTS,
    "analogue input":  _ANALOGUE_INPUTS,
    "digital output":  _DIGITAL_OUTPUTS,
    "analogue output": _ANALOGUE_OUTPUTS,
}


def gen_input_output(level="N4"):
    target_type = random.choice(list(_ALL_DEVICES.keys()))
    correct = random.choice(_ALL_DEVICES[target_type])

    distractors = []
    other_types = [t for t in _ALL_DEVICES if t != target_type]
    random.shuffle(other_types)
    for ot in other_types[:3]:
        wrong_device = random.choice(_ALL_DEVICES[ot])
        distractors.append({
            "value": wrong_device,
            "mistake": f"A {wrong_device} is {_DEVICE_TYPE_LABELS[ot]}. {_DEVICE_MISTAKES[target_type]}",
        })

    label = _DEVICE_TYPE_LABELS[target_type]
    return _make_classification(
        f"Which of the following is **{label}**?",
        correct, distractors,
        question_type="Input/Output Devices", level=level,
    )


def generate_input_output_devices(level="N4"):
    return gen_input_output(level=level)


# ── Electromagnets ─────────────────────────────────────────────────────────────

def gen_electromagnet_advantage(level="N4"):
    return _make_classification(
        "Large electromagnets are used in scrapyards to move metal objects. "
        "Which of the following explains why an electromagnet is used rather than a permanent magnet?",
        "An electromagnet can be switched off to release the metal objects",
        [
            {"value": "An electromagnet does not require any electricity to operate",
             "mistake": "Electromagnets require an electric current — that is what makes them magnetic."},
            {"value": "An electromagnet is always stronger than a permanent magnet",
             "mistake": "The key advantage is that it can be switched off, not that it is always stronger."},
            {"value": "An electromagnet is cheaper to make than a permanent magnet",
             "mistake": "The key advantage is that it can be switched off to release the materials."},
        ],
        question_type="Electromagnets", level=level,
    )


def gen_electromagnet_components(level="N4"):
    return _make_classification(
        "Which set of components is needed to make a working model electromagnet?",
        "Battery, coils of wire, and switch",
        [
            {"value": "Battery, resistor, and LED",
             "mistake": "An electromagnet needs coils of wire to create the magnetic field — an LED does not produce magnetism."},
            {"value": "Coils of wire, motor, and capacitor",
             "mistake": "A power source (battery) is needed. A motor and capacitor are not required for an electromagnet."},
            {"value": "Switch, thermistor, and lamp",
             "mistake": "An electromagnet needs a battery and coils of wire to create a magnetic field."},
        ],
        question_type="Electromagnets", level=level,
    )


_ELECTROMAGNET_GENS = [gen_electromagnet_advantage, gen_electromagnet_components]


def generate_electromagnets(level="N4"):
    return random.choice(_ELECTROMAGNET_GENS)(level=level)
