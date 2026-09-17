import random

from core.models.question_model import PhysicsQuestion

_SUPERSCRIPT = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
                "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "-": "⁻"}


def _fmt_power(power):
    return "10" + "".join(_SUPERSCRIPT[c] for c in str(power))


_PREFIXES = [
    {"name": "tera",  "symbol": "T", "power": 12},
    {"name": "giga",  "symbol": "G", "power": 9},
    {"name": "mega",  "symbol": "M", "power": 6},
    {"name": "kilo",  "symbol": "k", "power": 3},
    {"name": "centi", "symbol": "c", "power": -2},
    {"name": "milli", "symbol": "m", "power": -3},
    {"name": "micro", "symbol": "μ", "power": -6},
    {"name": "nano",  "symbol": "n", "power": -9},
    {"name": "pico",  "symbol": "p", "power": -12},
]

_NOTES = """
## Skills: Scientific Prefixes

Prefixes let us write very large or very small quantities using a convenient unit,
instead of a long string of zeros. Each prefix multiplies the base unit by a power of 10.

| Prefix | Symbol | Value | Example |
|---|---|---|---|
| tera  | T | ×10¹²  | 1 TW = 1 000 000 000 000 W |
| giga  | G | ×10⁹   | 1 GW = 1 000 000 000 W |
| mega  | M | ×10⁶   | 1 MW = 1 000 000 W |
| kilo  | k | ×10³   | 1 km = 1000 m |
| centi | c | ×10⁻²  | 1 cm = 0.01 m |
| milli | m | ×10⁻³  | 1 mA = 0.001 A |
| micro | μ | ×10⁻⁶  | 1 μs = 0.000001 s |
| nano  | n | ×10⁻⁹  | 1 ns = 0.000000001 s |
| pico  | p | ×10⁻¹² | 1 pF = 0.000000000001 F |

> Tip: prefixes above ×1 (tera, giga, mega, kilo) are **upper-case or 'k'**;
> prefixes below ×1 (milli, micro, nano, pico) are **lower-case**, except centi.
"""


def _make_classification(question_text, correct, distractors, level="N5"):
    options = [correct] + [d["value"] for d in distractors]
    random.shuffle(options)
    return PhysicsQuestion(
        question_text=question_text,
        correct_answer=correct,
        unit="",
        distractors=[{"value": d["value"], "mistake": d["mistake"], "working": []} for d in distractors],
        working=[{"type": "text", "content": f"The correct answer is: **{correct}**"}],
        notes=_NOTES,
        topic="Skills",
        question_type="Scientific Prefixes",
        level=level,
        metadata={"type": "classification", "options": options},
    )


def _other_prefixes(exclude_name, n=3):
    return random.sample([p for p in _PREFIXES if p["name"] != exclude_name], n)


def gen_name_to_power(level="N5"):
    prefix = random.choice(_PREFIXES)
    correct = _fmt_power(prefix["power"])
    distractors = [
        {
            "value": _fmt_power(other["power"]),
            "mistake": f"{_fmt_power(other['power'])} is the value of '{other['name']}', not "
                       f"'{prefix['name']}'. '{prefix['name']}' means ×{correct}.",
        }
        for other in _other_prefixes(prefix["name"])
    ]
    return _make_classification(
        f"Which power of 10 does the prefix **'{prefix['name']}'** ({prefix['symbol']}) represent?",
        correct, distractors, level=level,
    )


def gen_power_to_name(level="N5"):
    prefix = random.choice(_PREFIXES)
    correct = prefix["name"]
    distractors = [
        {
            "value": other["name"],
            "mistake": f"'{other['name']}' means ×{_fmt_power(other['power'])}, not "
                       f"×{_fmt_power(prefix['power'])}. The prefix for ×{_fmt_power(prefix['power'])} "
                       f"is '{prefix['name']}'.",
        }
        for other in _other_prefixes(prefix["name"])
    ]
    return _make_classification(
        f"Which prefix represents a value of **×{_fmt_power(prefix['power'])}**?",
        correct, distractors, level=level,
    )


def gen_symbol_to_name(level="N5"):
    prefix = random.choice(_PREFIXES)
    correct = prefix["name"]
    distractors = [
        {
            "value": other["name"],
            "mistake": f"'{other['symbol']}' is the symbol for '{other['name']}'. "
                       f"The symbol '{prefix['symbol']}' stands for '{prefix['name']}'.",
        }
        for other in _other_prefixes(prefix["name"])
    ]
    return _make_classification(
        f"In physics units, what does the symbol **'{prefix['symbol']}'** stand for? "
        f"(e.g. {prefix['symbol']}A, {prefix['symbol']}s)",
        correct, distractors, level=level,
    )


def gen_name_to_symbol(level="N5"):
    prefix = random.choice(_PREFIXES)
    correct = prefix["symbol"]
    distractors = [
        {
            "value": other["symbol"],
            "mistake": f"'{other['symbol']}' is the symbol for '{other['name']}'. "
                       f"The symbol for '{prefix['name']}' is '{prefix['symbol']}'.",
        }
        for other in _other_prefixes(prefix["name"])
    ]
    return _make_classification(
        f"What is the symbol for the prefix **'{prefix['name']}'**?",
        correct, distractors, level=level,
    )
