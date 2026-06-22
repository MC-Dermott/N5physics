import random

from core.models.question_model import PhysicsQuestion

_NOTES = """
## Standard Model

### Fundamental Particles

**Fermions** (half-integer spin — matter particles):
- **Quarks**: up (u), down (d), strange (s), charm (c), top (t), bottom (b)
- **Leptons**: electron (e⁻), muon (μ⁻), tau (τ⁻), and their neutrinos (νₑ, νμ, ντ)

**Bosons** (integer spin — force carriers):
- Photon (γ): electromagnetic force
- W⁺, W⁻, Z: weak nuclear force
- Gluon: strong nuclear force

### Composite Particles (Hadrons)

Hadrons are made of quarks and feel the strong nuclear force.

| Type | Composition | Examples |
|---|---|---|
| **Baryon** | 3 quarks | Proton (uud), Neutron (udd) |
| **Meson** | Quark–antiquark pair | π⁺ (ud̄), π⁻ (ūd), π⁰ (uū / dd̄), K⁺ (us̄) |

> **Leptons are not hadrons** — they do not feel the strong nuclear force and are not composed of quarks.

### Particle Masses

| Particle | Mass (kg) |
|---|---|
| Electron (e⁻) | 9.11 × 10⁻³¹ |
| Muon (μ⁻) | 1.88 × 10⁻²⁸ |
| Tau (τ⁻) | 3.17 × 10⁻²⁷ |
| Proton (p) | 1.67 × 10⁻²⁷ |
| Neutron (n) | 1.67 × 10⁻²⁷ |
"""

# ── Particle classification ────────────────────────────────────────────────────

_PARTICLES = [
    {
        "name": "electron",
        "symbol": "e⁻",
        "composition": None,
        "correct": "Fermion and Lepton",
        "distractors": [
            {
                "value": "Boson",
                "mistake": "The electron has half-integer spin — it is a fermion, not a boson. "
                           "Bosons are force-carrying particles such as the photon.",
            },
            {
                "value": "Fermion, Hadron, and Baryon",
                "mistake": "Leptons do not feel the strong nuclear force and are not composed of quarks — "
                           "the electron is not a hadron or baryon.",
            },
            {
                "value": "Hadron and Meson",
                "mistake": "Mesons are quark–antiquark composites. "
                           "The electron is a fundamental lepton with no quark content.",
            },
        ],
    },
    {
        "name": "muon",
        "symbol": "μ⁻",
        "composition": None,
        "correct": "Fermion and Lepton",
        "distractors": [
            {
                "value": "Boson",
                "mistake": "The muon is a matter particle with half-integer spin — it is a fermion, not a boson.",
            },
            {
                "value": "Fermion, Hadron, and Baryon",
                "mistake": "The muon is a lepton. Leptons do not feel the strong force and are not hadrons.",
            },
            {
                "value": "Hadron and Meson",
                "mistake": "Mesons are quark–antiquark pairs. The muon is a fundamental lepton with no quark content.",
            },
        ],
    },
    {
        "name": "tau",
        "symbol": "τ⁻",
        "composition": None,
        "correct": "Fermion and Lepton",
        "distractors": [
            {
                "value": "Boson",
                "mistake": "The tau particle has half-integer spin — it is a fermion, not a boson.",
            },
            {
                "value": "Fermion, Hadron, and Baryon",
                "mistake": "The tau is a lepton. Leptons do not feel the strong force and are not hadrons.",
            },
            {
                "value": "Hadron and Meson",
                "mistake": "The tau is a fundamental lepton, not a quark–antiquark composite.",
            },
        ],
    },
    {
        "name": "electron neutrino",
        "symbol": "νₑ",
        "composition": None,
        "correct": "Fermion and Lepton",
        "distractors": [
            {
                "value": "Boson",
                "mistake": "The neutrino is a matter particle with half-integer spin — it is a fermion, not a boson.",
            },
            {
                "value": "Fermion, Hadron, and Baryon",
                "mistake": "Neutrinos are leptons. They do not feel the strong force and are not hadrons.",
            },
            {
                "value": "Hadron and Meson",
                "mistake": "Neutrinos are fundamental leptons with no quark content — they are not mesons.",
            },
        ],
    },
    {
        "name": "proton",
        "symbol": "p",
        "composition": "uud",
        "correct": "Fermion, Hadron, and Baryon",
        "distractors": [
            {
                "value": "Fermion and Lepton",
                "mistake": "The proton is made of quarks (uud) and feels the strong nuclear force — "
                           "it is a hadron, not a lepton.",
            },
            {
                "value": "Hadron and Meson",
                "mistake": "A meson contains a quark–antiquark pair. "
                           "The proton is made of three quarks (uud), making it a baryon.",
            },
            {
                "value": "Boson",
                "mistake": "The proton is a three-quark composite with half-integer spin — "
                           "it is a fermion (baryon), not a boson.",
            },
        ],
    },
    {
        "name": "neutron",
        "symbol": "n",
        "composition": "udd",
        "correct": "Fermion, Hadron, and Baryon",
        "distractors": [
            {
                "value": "Fermion and Lepton",
                "mistake": "The neutron is made of quarks (udd) and feels the strong nuclear force — "
                           "it is a hadron, not a lepton.",
            },
            {
                "value": "Hadron and Meson",
                "mistake": "A meson contains a quark–antiquark pair. "
                           "The neutron is made of three quarks (udd), so it is a baryon.",
            },
            {
                "value": "Boson",
                "mistake": "The neutron is a three-quark composite with half-integer spin — "
                           "it is a fermion (baryon), not a boson.",
            },
        ],
    },
    {
        "name": "pi-plus meson",
        "symbol": "π⁺",
        "composition": "ud̄",
        "correct": "Hadron and Meson",
        "distractors": [
            {
                "value": "Fermion and Lepton",
                "mistake": "The π⁺ is made of quarks and feels the strong force — it is a hadron, not a lepton.",
            },
            {
                "value": "Fermion, Hadron, and Baryon",
                "mistake": "A baryon contains three quarks. "
                           "The π⁺ contains only a quark–antiquark pair (ud̄), making it a meson.",
            },
            {
                "value": "Boson",
                "mistake": "The π⁺ is classified as a meson and hadron. "
                           "In the Standard Model, bosons refers to force-carrying particles such as the photon.",
            },
        ],
    },
    {
        "name": "pi-minus meson",
        "symbol": "π⁻",
        "composition": "ūd",
        "correct": "Hadron and Meson",
        "distractors": [
            {
                "value": "Fermion and Lepton",
                "mistake": "The π⁻ is a quark composite that feels the strong force — it is a hadron, not a lepton.",
            },
            {
                "value": "Fermion, Hadron, and Baryon",
                "mistake": "Baryons contain three quarks. "
                           "The π⁻ (ūd) is a quark–antiquark pair, making it a meson.",
            },
            {
                "value": "Boson",
                "mistake": "The π⁻ is a meson and hadron — bosons in the Standard Model are force carriers.",
            },
        ],
    },
    {
        "name": "pi-zero meson",
        "symbol": "π⁰",
        "composition": "uū / dd̄",
        "correct": "Hadron and Meson",
        "distractors": [
            {
                "value": "Fermion and Lepton",
                "mistake": "The π⁰ is made of quarks and feels the strong force — it is a hadron, not a lepton.",
            },
            {
                "value": "Fermion, Hadron, and Baryon",
                "mistake": "Baryons contain three quarks; "
                           "the π⁰ is a quark–antiquark superposition (uū / dd̄), so it is a meson.",
            },
            {
                "value": "Boson",
                "mistake": "The π⁰ is a meson and hadron — "
                           "force-carrying particles such as the photon are the bosons of the Standard Model.",
            },
        ],
    },
    {
        "name": "kaon",
        "symbol": "K⁺",
        "composition": "us̄",
        "correct": "Hadron and Meson",
        "distractors": [
            {
                "value": "Fermion and Lepton",
                "mistake": "The kaon is made of quarks (us̄) and feels the strong force — it is a hadron, not a lepton.",
            },
            {
                "value": "Fermion, Hadron, and Baryon",
                "mistake": "Baryons contain three quarks; the K⁺ is a quark–antiquark pair (us̄), making it a meson.",
            },
            {
                "value": "Boson",
                "mistake": "The K⁺ is a meson and hadron — bosons in the Standard Model are force-carrying particles.",
            },
        ],
    },
    {
        "name": "photon",
        "symbol": "γ",
        "composition": None,
        "correct": "Boson",
        "distractors": [
            {
                "value": "Fermion and Lepton",
                "mistake": "The photon carries the electromagnetic force with integer spin — "
                           "it is a boson, not a fermion or lepton.",
            },
            {
                "value": "Fermion, Hadron, and Baryon",
                "mistake": "The photon is a fundamental force carrier — it is a boson, not a hadron or baryon.",
            },
            {
                "value": "Hadron and Meson",
                "mistake": "Hadrons are composed of quarks. The photon is a fundamental force-carrying boson.",
            },
        ],
    },
    {
        "name": "W⁺ boson",
        "symbol": "W⁺",
        "composition": None,
        "correct": "Boson",
        "distractors": [
            {
                "value": "Fermion and Lepton",
                "mistake": "The W⁺ carries the weak nuclear force — it is a boson with integer spin, "
                           "not a fermion or lepton.",
            },
            {
                "value": "Fermion, Hadron, and Baryon",
                "mistake": "Force-carrying particles like the W⁺ are bosons, not hadrons or baryons.",
            },
            {
                "value": "Hadron and Meson",
                "mistake": "The W⁺ is a gauge boson mediating the weak force — "
                           "it is not composed of quarks and is not a hadron.",
            },
        ],
    },
]


def gen_particle_classification(level="Higher"):
    particle = random.choice(_PARTICLES)

    if particle["composition"]:
        q_text = (
            f"Which of the following correctly classifies the "
            f"**{particle['name']}** ({particle['symbol']}, quark content: {particle['composition']})?"
        )
    else:
        q_text = (
            f"Which of the following correctly classifies the "
            f"**{particle['name']}** ({particle['symbol']})?"
        )

    options = [particle["correct"]] + [d["value"] for d in particle["distractors"]]
    random.shuffle(options)

    return PhysicsQuestion(
        question_text=q_text,
        correct_answer=particle["correct"],
        unit="",
        distractors=[
            {"value": d["value"], "mistake": d["mistake"], "working": []}
            for d in particle["distractors"]
        ],
        working=[
            {
                "type": "text",
                "content": f"The {particle['name']} ({particle['symbol']}) is a **{particle['correct']}**.",
            }
        ],
        notes=_NOTES,
        topic="Particles and Waves",
        question_type="Standard Model",
        level=level,
        metadata={"type": "classification", "options": options},
    )


# ── Order of magnitude ─────────────────────────────────────────────────────────

_MASS_PAIRS = [
    {
        "particle_a": "electron",
        "mass_a_str": "9.11 × 10⁻³¹",
        "exp_a": -31,
        "particle_b": "muon",
        "mass_b_str": "1.88 × 10⁻²⁸",
        "exp_b": -28,
    },
    {
        "particle_a": "electron",
        "mass_a_str": "9.11 × 10⁻³¹",
        "exp_a": -31,
        "particle_b": "proton",
        "mass_b_str": "1.67 × 10⁻²⁷",
        "exp_b": -27,
    },
    {
        "particle_a": "electron",
        "mass_a_str": "9.11 × 10⁻³¹",
        "exp_a": -31,
        "particle_b": "tau",
        "mass_b_str": "3.17 × 10⁻²⁷",
        "exp_b": -27,
    },
    {
        "particle_a": "muon",
        "mass_a_str": "1.88 × 10⁻²⁸",
        "exp_a": -28,
        "particle_b": "proton",
        "mass_b_str": "1.67 × 10⁻²⁷",
        "exp_b": -27,
    },
    {
        "particle_a": "muon",
        "mass_a_str": "1.88 × 10⁻²⁸",
        "exp_a": -28,
        "particle_b": "tau",
        "mass_b_str": "3.17 × 10⁻²⁷",
        "exp_b": -27,
    },
    {
        "particle_a": "electron",
        "mass_a_str": "9.11 × 10⁻³¹",
        "exp_a": -31,
        "particle_b": "neutron",
        "mass_b_str": "1.67 × 10⁻²⁷",
        "exp_b": -27,
    },
    {
        "particle_a": "muon",
        "mass_a_str": "1.88 × 10⁻²⁸",
        "exp_a": -28,
        "particle_b": "neutron",
        "mass_b_str": "1.67 × 10⁻²⁷",
        "exp_b": -27,
    },
]


def gen_order_of_magnitude(level="Higher"):
    pair = random.choice(_MASS_PAIRS)
    diff = abs(pair["exp_b"] - pair["exp_a"])

    phrasing = random.choice(["difference", "how_many_more"])

    if phrasing == "how_many_more":
        q_text = (
            f"The mass of the {pair['particle_a']} is {pair['mass_a_str']} kg "
            f"and the mass of the {pair['particle_b']} is {pair['mass_b_str']} kg. "
            f"By how many orders of magnitude is the {pair['particle_b']} more massive than the {pair['particle_a']}?"
        )
    else:
        q_text = (
            f"The mass of the {pair['particle_a']} is {pair['mass_a_str']} kg "
            f"and the mass of the {pair['particle_b']} is {pair['mass_b_str']} kg. "
            f"What is the difference in order of magnitude between these two masses?"
        )

    working = [
        {
            "type": "text",
            "content": "The order of magnitude of a number is the power of 10 "
                       "when written in scientific notation.",
        },
        {
            "type": "text",
            "content": f"Order of magnitude of {pair['particle_a']} mass: {pair['exp_a']}",
        },
        {
            "type": "text",
            "content": f"Order of magnitude of {pair['particle_b']} mass: {pair['exp_b']}",
        },
        {
            "type": "text",
            "content": f"Difference = |{pair['exp_b']} − ({pair['exp_a']})| = {diff}",
        },
    ]

    distractors = []
    for candidate in [diff - 1, diff + 1, diff + 2, diff - 2]:
        if candidate > 0 and candidate != diff:
            distractors.append({
                "value": candidate,
                "mistake": (
                    f"Subtract the powers of 10 directly: "
                    f"|{pair['exp_b']} − ({pair['exp_a']})| = {diff}."
                ),
                "working": working,
            })
        if len(distractors) == 3:
            break

    return PhysicsQuestion(
        question_text=q_text,
        correct_answer=diff,
        unit="",
        distractors=distractors,
        working=working,
        notes=_NOTES,
        topic="Particles and Waves",
        question_type="Standard Model",
        level=level,
        metadata={"type": "order_of_magnitude"},
    )


# ── Public entry points ────────────────────────────────────────────────────────

def generate_standard_model_classification(level="Higher"):
    return gen_particle_classification(level=level)


def generate_standard_model_order_of_magnitude(level="Higher"):
    return gen_order_of_magnitude(level=level)
