from utils.definitions import make_definition_generators

# Definitions needed for Higher Electricity, worded as accepted in SQA marking
# instructions. See utils/definitions.py for the entry format.
DEFINITIONS = {
    # ── Alternating current ────────────────────────────────────────────────────
    "alternating current": {
        "group": "Alternating current",
        "definition": "A current that changes direction and instantaneous value with time.",
        "confusables": ["r.m.s. value", "peak value"],
    },
    "peak value": {
        "group": "Alternating current",
        "definition": "The maximum value of an alternating voltage or current.",
        "confusables": ["r.m.s. value"],
    },
    "r.m.s. value": {
        "group": "Alternating current",
        "definition": "The value of direct current (or voltage) that would produce the same "
                      "power as the alternating current (or voltage).",
        "confusables": ["peak value"],
        "traps": [("The average value of the alternating current over one cycle.",
                   "The average of a symmetrical a.c. over one cycle is **zero**. The r.m.s. "
                   "value is the d.c. equivalent that gives the same power.")],
    },

    # ── Internal resistance ────────────────────────────────────────────────────
    "electromotive force (e.m.f.)": {
        "group": "Internal resistance",
        "definition": "The electrical energy supplied to each coulomb of charge passing through "
                      "the source.",
        "confusables": ["terminal potential difference", "lost volts"],
        "traps": [("The potential difference across the terminals of a source when it is "
                   "supplying a current.",
                   "That is the **terminal potential difference**. The e.m.f. is the energy "
                   "given to each coulomb — it equals the t.p.d. only when no current flows.")],
    },
    "internal resistance": {
        "group": "Internal resistance",
        "definition": "The resistance of the source itself.",
        "confusables": ["lost volts"],
    },
    "terminal potential difference": {
        "group": "Internal resistance",
        "definition": "The potential difference across the terminals of a source when it is "
                      "supplying a current (V = E − Ir).",
        "confusables": ["electromotive force (e.m.f.)", "lost volts"],
    },
    "lost volts": {
        "group": "Internal resistance",
        "definition": "The potential difference across the internal resistance of the source "
                      "(Ir).",
        "confusables": ["terminal potential difference", "internal resistance"],
    },
    "short-circuit current": {
        "group": "Internal resistance",
        "definition": "The maximum current from a source, when the external resistance is zero "
                      "(E ÷ r).",
        "confusables": ["lost volts"],
    },

    # ── Capacitors ─────────────────────────────────────────────────────────────
    "capacitance": {
        "group": "Capacitors",
        "definition": "The charge stored per unit potential difference (C = Q ÷ V).",
        "confusables": ["the farad"],
        "traps": [("The charge stored multiplied by the potential difference across the "
                   "capacitor.",
                   "Capacitance is charge **divided** by potential difference. ½QV is the "
                   "energy stored.")],
    },
    "the farad": {
        "group": "Capacitors",
        "definition": "The capacitance of a capacitor that stores 1 coulomb of charge for each "
                      "volt of potential difference across it.",
        "confusables": ["capacitance"],
    },

    # ── Semiconductors ─────────────────────────────────────────────────────────
    "conductor": {
        "group": "Semiconductors",
        "definition": "A material whose conduction band is partly filled (or overlaps the "
                      "valence band), so electrons are free to move.",
        "confusables": ["insulator", "semiconductor"],
    },
    "insulator": {
        "group": "Semiconductors",
        "definition": "A material whose valence band is full and whose conduction band is empty, "
                      "with a large gap between them.",
        "confusables": ["conductor", "semiconductor"],
    },
    "semiconductor": {
        "group": "Semiconductors",
        "definition": "A material with a small gap between the valence and conduction bands, so "
                      "some electrons can gain enough energy to move into the conduction band.",
        "confusables": ["insulator", "conductor"],
    },
    "doping": {
        "group": "Semiconductors",
        "definition": "Adding impurity atoms to a semiconductor to increase its conductivity.",
        "confusables": ["n-type semiconductor", "p-type semiconductor"],
    },
    "n-type semiconductor": {
        "group": "Semiconductors",
        "definition": "A doped semiconductor in which the majority charge carriers are "
                      "electrons.",
        "confusables": ["p-type semiconductor"],
        "traps": [("A doped semiconductor with an overall negative charge.",
                   "Doped semiconductors are electrically **neutral** — 'n' refers to the "
                   "majority charge carriers being negative electrons.")],
    },
    "p-type semiconductor": {
        "group": "Semiconductors",
        "definition": "A doped semiconductor in which the majority charge carriers are "
                      "positive holes.",
        "confusables": ["n-type semiconductor"],
    },
    "forward bias": {
        "group": "Semiconductors",
        "definition": "A p–n junction connected with the p-type to the positive terminal, so "
                      "current flows across the junction.",
        "confusables": ["reverse bias"],
    },
    "reverse bias": {
        "group": "Semiconductors",
        "definition": "A p–n junction connected with the p-type to the negative terminal, so "
                      "the depletion layer widens and almost no current flows.",
        "confusables": ["forward bias"],
    },
    "light emitting diode (LED)": {
        "group": "Semiconductors",
        "definition": "A forward-biased p–n junction that emits photons when electrons and "
                      "holes recombine at the junction.",
        "confusables": ["photovoltaic mode", "forward bias"],
    },
    "photovoltaic mode": {
        "group": "Semiconductors",
        "definition": "A p–n junction with no bias, in which absorbed photons create "
                      "electron–hole pairs that produce a potential difference (e.g. a solar cell).",
        "confusables": ["light emitting diode (LED)"],
    },
}

STATEMENTS = [
    # key, statement, correct?, explanation
    ("rms", "The r.m.s. voltage is equal to the peak voltage divided by √2.", True,
     "V_rms = V_peak ÷ √2."),
    ("rms", "The peak voltage is equal to the r.m.s. voltage divided by √2.", False,
     "It is the other way round — V_peak = √2 × V_rms, so the peak is **larger**."),
    ("emf", "When a cell supplies a current, its terminal potential difference is less than "
     "its e.m.f.", True,
     "Some energy is lost in the internal resistance: V = E − Ir."),
    ("lost", "The lost volts decrease as the current from a cell increases.", False,
     "Lost volts = Ir, so they **increase** as the current increases."),
    ("cap", "Capacitance is the charge stored per unit potential difference.", True,
     "C = Q ÷ V."),
    ("cap", "The energy stored in a capacitor is equal to QV.", False,
     "The energy stored is **½QV**."),
    ("charging", "As a capacitor charges through a resistor, the current is largest at the "
     "start.", True,
     "The capacitor is uncharged, so the whole supply voltage is across the resistor."),
    ("ntype", "An n-type semiconductor has an overall negative charge.", False,
     "It is electrically **neutral** — its majority charge carriers are electrons."),
    ("ntype", "In an n-type semiconductor the majority charge carriers are electrons.", True,
     "This is what 'n-type' means."),
    ("bands", "In an insulator the valence band is full and the conduction band is empty.", True,
     "The large band gap means no electrons can move into the conduction band."),
    ("led", "An LED emits light when it is reverse biased.", False,
     "An LED emits light when **forward** biased — electrons and holes recombine at the "
     "junction."),
    ("semi_temp", "Increasing the temperature of a pure semiconductor decreases its resistance.",
     True, "More electrons gain enough energy to move into the conduction band."),
]

GENERATORS = make_definition_generators("Electricity", DEFINITIONS, STATEMENTS)
