"""Rearranging relationships: multiple choice, with the relationship shown as it appears on the
SQA relationships sheet and four rearrangements to choose from.

Most relationships are products and quotients of quantities (V = IR, E_k = ½mv², p₁V₁ = p₂V₂…).
Those are written as two `Product`s and solved by the code below, which also builds the worked
solution and wrong answers from the mistakes pupils actually make (upside down, multiplying instead
of dividing, forgetting the square root…). The few with a + or − in them (v = u + at,
E = V + Ir…) are written out by hand in SUMS.

The relationships for each level are listed in RELATIONSHIPS; GENERATORS maps each level to its
groups of relationships, one question style per group.
"""
import random
from dataclasses import dataclass
from fractions import Fraction

from core.models.question_model import PhysicsQuestion

# symbol key: (LaTeX, name). Keys are what the relationships below are written in.
SYMBOLS = {
    "d": ("d", "distance"), "s": ("s", "displacement"), "v": ("v", "speed"), "vbar": (r"\bar{v}", "average speed"),
    "t": ("t", "time"), "a": ("a", "acceleration"), "dv": (r"\Delta v", "change in speed"),
    "u": ("u", "initial speed"), "m": ("m", "mass"), "W": ("W", "weight"), "g": ("g", "gravitational field strength"),
    "F": ("F", "force"), "Ew": ("E_w", "work done"), "Ep": ("E_p", "potential energy"), "h": ("h", "height"),
    "Ek": ("E_k", "kinetic energy"), "E": ("E", "energy"), "P": ("P", "power"), "Q": ("Q", "charge"),
    "I": ("I", "current"), "V": ("V", "voltage"), "R": ("R", "resistance"), "Eh": ("E_h", "heat energy"),
    "c": ("c", "specific heat capacity"), "dT": (r"\Delta T", "change in temperature"),
    "l": ("l", "specific latent heat"), "p": ("p", "pressure"), "A": ("A", "area"),
    "p1": ("p_1", "initial pressure"), "p2": ("p_2", "final pressure"),
    "V1": ("V_1", "initial volume"), "V2": ("V_2", "final volume"),
    "T1": ("T_1", "initial temperature"), "T2": ("T_2", "final temperature"),
    "f": ("f", "frequency"), "lam": (r"\lambda", "wavelength"), "T": ("T", "period"), "N": ("N", "number"),
    "Act": ("A", "activity"), "D": ("D", "absorbed dose"), "H": ("H", "equivalent dose"),
    "wR": ("w_R", "radiation weighting factor"), "Hdot": (r"\dot{H}", "equivalent dose rate"),
    "Vs": ("V_S", "supply voltage"), "R1": ("R_1", "resistance R₁"), "R2": ("R_2", "resistance R₂"),
    "Vr1": ("V_1", "voltage V₁"), "Vr2": ("V_2", "voltage V₂"),
    "mom": ("p", "momentum"), "G": ("G", "gravitational constant"), "m1": ("m_1", "mass m₁"),
    "m2": ("m_2", "mass m₂"), "r": ("r", "distance between centres"), "cl": ("c", "speed of light"),
    "hp": ("h", "Planck's constant"), "z": ("z", "redshift"), "H0": ("H_0", "Hubble's constant"),
    "dist": ("d", "distance"), "gs": ("d", "grating spacing"), "sin": (r"\sin\theta", "the sine of the angle"),
    "order": ("m", "order"), "n": ("n", "refractive index"), "sin1": (r"\sin\theta_1", "the sine of the angle in the first medium"),
    "sin2": (r"\sin\theta_2", "the sine of the angle in the second medium"),
    "sinc": (r"\sin\theta_c", "the sine of the critical angle"),
    "Irr": ("I", "irradiance"), "k": ("k", "constant"), "C": ("C", "capacitance"),
    "Ec": ("E", "energy stored"), "Ir": ("r", "internal resistance"), "emf": ("E", "e.m.f."),
}

# Constants are never asked for (nobody makes G the subject of F = Gm₁m₂/r²).
CONSTANTS = {"G", "cl", "hp"}


def _tex(key):
    return SYMBOLS[key][0]


def _name(key):
    return SYMBOLS[key][1]


@dataclass(frozen=True)
class Product:
    """coef × each factor raised to its power, e.g. ½mv² is Product(½, (("m", 1), ("v", 2)))."""
    factors: tuple = ()
    coef: Fraction = Fraction(1)

    def power(self, key):
        return dict(self.factors).get(key, 0)

    def without(self, key):
        return Product(tuple(f for f in self.factors if f[0] != key), self.coef)


def prod(*factors, coef=1):
    """prod("m", ("v", 2), coef=Fraction(1, 2)) → ½mv²; a negative power puts a factor on the bottom."""
    return Product(tuple((f, 1) if isinstance(f, str) else f for f in factors), Fraction(coef))


def _power_tex(key, p):
    return _tex(key) + (f"^{{{p}}}" if p != 1 else "")


def _product_tex(prod_, with_coef=True):
    """A product as a fraction, e.g. \\dfrac{2E_k}{v^{2}}."""
    coef = prod_.coef if with_coef else Fraction(1)
    top = [str(coef.numerator)] if coef.numerator != 1 else []
    bottom = [str(coef.denominator)] if coef.denominator != 1 else []
    for key, p in prod_.factors:
        if p > 0:
            top.append(_power_tex(key, p))
        elif p < 0:
            bottom.append(_power_tex(key, -p))
    top_tex = " ".join(top) if top else "1"
    if not bottom:
        return top_tex
    return rf"\dfrac{{{top_tex}}}{{{' '.join(bottom)}}}"


def _sheet_tex(side):
    """A side as the relationships sheet writes it: ½mv² keeps its ½ in front."""
    if side.coef.denominator != 1 and side.coef.numerator == 1 and any(p > 0 for _, p in side.factors):
        return rf"\tfrac{{1}}{{{side.coef.denominator}}}" + _product_tex(Product(side.factors), with_coef=False)
    return _product_tex(side)


def _join(*keys):
    return " ".join(_tex(k) for k in keys)


@dataclass(frozen=True)
class Answer:
    """subject = inner, or subject = √inner when root is set."""
    inner: Product
    root: bool = False

    def key(self):
        return (self.inner.coef, tuple(sorted((k, p) for k, p in self.inner.factors if p)), self.root)

    def tex(self, subject):
        body = _product_tex(self.inner)
        return f"{_tex(subject)} = " + (rf"\sqrt{{{body}}}" if self.root else body)


def _flip(prod_):
    return Product(tuple((k, -p) for k, p in prod_.factors), 1 / prod_.coef)


def _solve(lhs, rhs, x):
    """Rearranges lhs = rhs for x. Returns (answer, steps): steps are (text, latex) pairs for the
    worked solution."""
    steps = []
    x_on_left = bool(lhs.power(x))
    side, other = (lhs, rhs) if x_on_left else (rhs, lhs)
    p = side.power(x)
    # x on the bottom: multiply both sides by it, which moves it to the top of the other side.
    if p < 0:
        rest, moved = side.without(x), Product(other.factors + ((x, -p),), other.coef)
        shown = (rest, moved) if x_on_left else (moved, rest)
        steps.append((f"${_tex(x)}$ is on the bottom, so multiply both sides by ${_power_tex(x, -p)}$.",
                      f"{_product_tex(shown[0])} = {_product_tex(shown[1])}"))
        side, other, p = moved, rest, -p
    lhs, rhs = side, other

    # lhs is now coef × x^p × others: divide/multiply the others across.
    others = lhs.without(x)
    inner = Product(tuple(rhs.factors) + tuple((k, -q) for k, q in others.factors), rhs.coef / others.coef)
    # merge any repeated symbols
    merged = {}
    for k, q in inner.factors:
        merged[k] = merged.get(k, 0) + q
    inner = Product(tuple((k, q) for k, q in merged.items() if q), inner.coef)

    ops = []
    divide = [k for k, q in others.factors if q > 0]
    multiply = [k for k, q in others.factors if q < 0]
    if others.coef.denominator != 1:
        ops.append(f"multiply both sides by {others.coef.denominator}")
    if others.coef.numerator != 1:
        ops.append(f"divide both sides by {others.coef.numerator}")
    if divide:
        ops.append("divide both sides by $" + " ".join(_power_tex(k, others.power(k)) for k in divide) + "$")
    if multiply:
        ops.append("multiply both sides by $" + " ".join(_power_tex(k, -others.power(k)) for k in multiply) + "$")
    if ops:
        text = "To get " + f"${_power_tex(x, p)}$ on its own, " + " and ".join(ops) + "."
        steps.append((text, f"{_power_tex(x, p)} = {_product_tex(inner)}"))

    root = p == 2
    if root:
        steps.append(("Take the square root of both sides.", Answer(inner, True).tex(x)))
    return Answer(inner, root), steps


def _has_top(answer):
    return any(p > 0 for _, p in answer.inner.factors)


def _wrong_answers(correct, x):
    """Wrong rearrangements, most likely mistakes first, as (Answer or LaTeX, explanation)."""
    inner, root = correct.inner, correct.root
    subject = f"${_tex(x)}$"
    likely = [(Answer(_flip(inner), root),
               f"This is upside down. Check which quantities should be on the top and which on the bottom "
               f"when {subject} is on its own.")]
    if root:
        likely.append((Answer(inner, False),
                       f"This is the expression for ${_power_tex(x, 2)}$. Take the square root to get {subject}."))
    if inner.coef != 1:
        likely.append((Answer(Product(inner.factors, 1 / inner.coef), root),
                       "The number has been moved to the wrong place. When you divide by a fraction like ½ "
                       "you multiply by 2 (and the other way round)."))
    for i, (k, q) in enumerate(inner.factors):
        changed = inner.factors[:i] + ((k, -q),) + inner.factors[i + 1:]
        side = "top" if q < 0 else "bottom"
        likely.append((Answer(Product(changed, inner.coef), root),
                       f"${_tex(k)}$ should be on the {'bottom' if side == 'top' else 'top'}, not the {side}. "
                       "When a quantity moves to the other side, multiplying becomes dividing (and dividing "
                       "becomes multiplying)."))
    likely.append((Answer(Product(tuple((k, abs(q)) for k, q in inner.factors), max(inner.coef, 1 / inner.coef)), root),
                   "Everything has been multiplied together. Quantities that are multiplied on one side are "
                   "divided on the other side."))
    tops = [k for k, q in inner.factors if q == 1]
    bottoms = [k for k, q in inner.factors if q == -1]
    if not root and inner.coef == 1 and len(tops) == 1 and len(bottoms) == 1 and len(inner.factors) == 2:
        likely.append((f"{_tex(x)} = {_tex(tops[0])} - {_tex(bottoms[0])}",
                       "The quantities in this relationship are multiplied or divided, not added or "
                       "subtracted, so undo them by dividing or multiplying."))
    if not root:
        likely.append((Answer(inner, True),
                       f"There is no square in the relationship for {subject}, so there's no square root."))
    # Answers like 1/(Fa), with nothing but a number on top, are mistakes nobody makes: use them last.
    unlikely = [w for w in likely if isinstance(w[0], Answer) and _has_top(correct) and not _has_top(w[0])]
    likely = [w for w in likely if w not in unlikely]
    return [(a if isinstance(a, str) else a.tex(x), why) for a, why in likely + unlikely]


def _options(correct_tex, wrong):
    """Up to three distinct wrong answers, keeping the most likely mistakes."""
    seen, chosen = {correct_tex}, []
    for tex, why in wrong:
        if tex not in seen:
            seen.add(tex)
            chosen.append({"value": f"${tex}$", "mistake": why, "working": []})
        if len(chosen) == 3:
            break
    return chosen


_NOTES = r"""
## Skills: Rearranging Relationships

To make a quantity the **subject**, get it on its own on one side of the equals sign.
Whatever you do to one side, do the same to the other.

| If the quantity is… | …undo it by |
|---|---|
| multiplied by something | dividing both sides by it |
| divided by something | multiplying both sides by it |
| added to something | subtracting it from both sides |
| squared | taking the square root of both sides |

**Example:** make $m$ the subject of $E_k = \tfrac{1}{2}mv^2$

$$2E_k = mv^2 \quad\text{(multiply both sides by 2)}$$
$$m = \dfrac{2E_k}{v^2} \quad\text{(divide both sides by } v^2\text{)}$$

> **Check:** the quantity you want should end up on the **top** of a fraction, on its own.
"""


def _question(sheet_tex, subject_tex, subject_name, answer_tex, wrong, steps, level):
    distractors = _options(answer_tex, wrong)
    options = [f"${answer_tex}$"] + [d["value"] for d in distractors]
    random.shuffle(options)
    working = [{"type": "latex", "content": sheet_tex}]
    for text, tex in steps:
        working.append({"type": "text", "content": text})
        working.append({"type": "latex", "content": tex})
    return PhysicsQuestion(
        question_text=(f"Rearrange this relationship to make ${subject_tex}$ ({subject_name}) the subject.\n\n"
                       rf"$$\large\boxed{{\;{sheet_tex}\;}}$$"),
        correct_answer=f"${answer_tex}$",
        unit="",
        distractors=distractors,
        working=working,
        notes=_NOTES,
        topic="Skills",
        question_type="Rearranging Relationships",
        level=level,
        # Side by side, so the stacked fractions don't crowd each other
        metadata={"type": "classification", "options": options, "horizontal": True},
    )


def _product_question(rel, level, x=None):
    lhs, rhs = rel
    candidates = [k for side in (lhs, rhs) for k, _ in side.factors if k not in CONSTANTS]
    # The subject already on its own is not a rearrangement.
    if not lhs.factors[1:] and lhs.coef == 1 and lhs.factors[0][1] == 1:
        candidates = [k for k in candidates if k != lhs.factors[0][0]]
    x = x or random.choice(candidates)
    sheet_tex = f"{_sheet_tex(lhs)} = {_sheet_tex(rhs)}"
    answer, steps = _solve(lhs, rhs, x)
    wrong = _wrong_answers(answer, x)
    # A last resort for short relationships like T = 1/f, which have few other mistakes to make.
    wrong.append((rf"{_tex(x)} = \left({_product_tex(answer.inner)}\right)^{{2}}",
                  "There is no square root in the relationship, so nothing needs squaring."))
    return _question(sheet_tex, _tex(x), _name(x), answer.tex(x), wrong, steps, level)


# ── Relationships with a + or − (hand-written) ────────────────────────────────
# sheet: the relationship as on the sheet; targets: subject → (answer, steps, [(wrong, why)]).

_SWAP = "Subtract the same thing from both sides, then divide."

SUMS = {
    "a=(v-u)/t": {
        "sheet": r"a = \dfrac{v - u}{t}",
        "targets": {
            "v": (r"v = u + at",
                  [("Multiply both sides by $t$.", r"at = v - u"), ("Add $u$ to both sides.", r"v = u + at")],
                  [(r"v = \dfrac{a}{t} + u", "$t$ is dividing on the right, so it should multiply $a$ when it moves."),
                   (r"v = at - u", "$u$ was subtracted from $v$, so it is added when it moves to the other side."),
                   (r"v = u + \dfrac{t}{a}", "Multiply both sides by $t$ first: $at = v - u$.")]),
            "u": (r"u = v - at",
                  [("Multiply both sides by $t$.", r"at = v - u"), ("Rearrange for $u$.", r"u = v - at")],
                  [(r"u = at - v", "Check the signs: $at = v - u$, so $u = v - at$."),
                   (r"u = v + at", "From $at = v - u$, $u$ and $at$ swap sides, so $at$ is subtracted."),
                   (r"u = v - \dfrac{a}{t}", "$t$ is dividing on the right, so it should multiply $a$.")]),
            "t": (r"t = \dfrac{v - u}{a}",
                  [("Multiply both sides by $t$.", r"at = v - u"), ("Divide both sides by $a$.", r"t = \dfrac{v - u}{a}")],
                  [(r"t = \dfrac{a}{v - u}", "This is upside down. $t$ is on the bottom, so it ends up dividing into $v - u$."),
                   (r"t = a(v - u)", "Multiplying by $t$ gives $at = v - u$; then divide by $a$."),
                   (r"t = \dfrac{v}{a} - u", "The whole of $v - u$ is divided by $a$, not just $v$.")]),
        },
    },
    "v=u+at": {
        "sheet": r"v = u + at",
        "targets": {
            "u": (r"u = v - at", [("Subtract $at$ from both sides.", r"u = v - at")],
                  [(r"u = v + at", "$at$ is added to $u$, so it is subtracted when it moves."),
                   (r"u = at - v", "Check the signs: $u = v - at$."),
                   (r"u = \dfrac{v}{at}", "$u$ and $at$ are added, not multiplied, so subtract $at$.")]),
            "a": (r"a = \dfrac{v - u}{t}",
                  [("Subtract $u$ from both sides.", r"v - u = at"), ("Divide both sides by $t$.", r"a = \dfrac{v - u}{t}")],
                  [(r"a = \dfrac{v}{t} - u", "Subtract $u$ first, then divide all of $v - u$ by $t$."),
                   (r"a = \dfrac{t}{v - u}", "This is upside down: divide $v - u$ by $t$."),
                   (r"a = \dfrac{v + u}{t}", "$u$ is added on the right, so it is subtracted when it moves.")]),
            "t": (r"t = \dfrac{v - u}{a}",
                  [("Subtract $u$ from both sides.", r"v - u = at"), ("Divide both sides by $a$.", r"t = \dfrac{v - u}{a}")],
                  [(r"t = \dfrac{v}{a} - u", "Subtract $u$ first, then divide all of $v - u$ by $a$."),
                   (r"t = \dfrac{a}{v - u}", "This is upside down: divide $v - u$ by $a$."),
                   (r"t = \dfrac{v + u}{a}", "$u$ is added on the right, so it is subtracted when it moves.")]),
        },
    },
    "v2=u2+2as": {
        "sheet": r"v^2 = u^2 + 2as",
        "targets": {
            "s": (r"s = \dfrac{v^2 - u^2}{2a}",
                  [("Subtract $u^2$ from both sides.", r"v^2 - u^2 = 2as"), ("Divide both sides by $2a$.", r"s = \dfrac{v^2 - u^2}{2a}")],
                  [(r"s = \dfrac{v^2 + u^2}{2a}", "$u^2$ is added on the right, so it is subtracted when it moves."),
                   (r"s = \dfrac{v - u}{2a}", "The speeds are squared in the relationship; keep the squares."),
                   (r"s = \dfrac{2a}{v^2 - u^2}", "This is upside down: divide $v^2 - u^2$ by $2a$.")]),
            "a": (r"a = \dfrac{v^2 - u^2}{2s}",
                  [("Subtract $u^2$ from both sides.", r"v^2 - u^2 = 2as"), ("Divide both sides by $2s$.", r"a = \dfrac{v^2 - u^2}{2s}")],
                  [(r"a = \dfrac{v^2 - u^2}{s}", "Divide by $2s$, not just $s$: the 2 is part of $2as$."),
                   (r"a = \dfrac{v - u}{2s}", "The speeds are squared in the relationship; keep the squares."),
                   (r"a = \dfrac{v^2 + u^2}{2s}", "$u^2$ is added on the right, so it is subtracted when it moves.")]),
            "u": (r"u = \sqrt{v^2 - 2as}",
                  [("Subtract $2as$ from both sides.", r"u^2 = v^2 - 2as"), ("Take the square root of both sides.", r"u = \sqrt{v^2 - 2as}")],
                  [(r"u = v - \sqrt{2as}", "Take the square root of the whole of $v^2 - 2as$, not each part."),
                   (r"u = v^2 - 2as", "This is $u^2$. Take the square root to get $u$."),
                   (r"u = \sqrt{v^2 + 2as}", "$2as$ is added on the right, so it is subtracted when it moves.")]),
        },
    },
    "E=V+Ir": {
        "sheet": r"E = V + Ir",
        "targets": {
            "V": (r"V = E - Ir", [("Subtract $Ir$ from both sides.", r"V = E - Ir")],
                  [(r"V = E + Ir", "$Ir$ is added to $V$, so it is subtracted when it moves."),
                   (r"V = Ir - E", "Check the signs: $V = E - Ir$."),
                   (r"V = \dfrac{E}{Ir}", "$V$ and $Ir$ are added, not multiplied, so subtract $Ir$.")]),
            "r": (r"r = \dfrac{E - V}{I}",
                  [("Subtract $V$ from both sides.", r"E - V = Ir"), ("Divide both sides by $I$.", r"r = \dfrac{E - V}{I}")],
                  [(r"r = \dfrac{E}{I} - V", "Subtract $V$ first, then divide all of $E - V$ by $I$."),
                   (r"r = \dfrac{E + V}{I}", "$V$ is added on the right, so it is subtracted when it moves."),
                   (r"r = \dfrac{I}{E - V}", "This is upside down: divide $E - V$ by $I$.")]),
            "I": (r"I = \dfrac{E - V}{r}",
                  [("Subtract $V$ from both sides.", r"E - V = Ir"), ("Divide both sides by $r$.", r"I = \dfrac{E - V}{r}")],
                  [(r"I = \dfrac{E}{r} - V", "Subtract $V$ first, then divide all of $E - V$ by $r$."),
                   (r"I = \dfrac{E + V}{r}", "$V$ is added on the right, so it is subtracted when it moves."),
                   (r"I = \dfrac{r}{E - V}", "This is upside down: divide $E - V$ by $r$.")]),
        },
    },
    "E2-E1=hf": {
        "sheet": r"E_2 - E_1 = hf",
        "targets": {
            "f": (r"f = \dfrac{E_2 - E_1}{h}", [("Divide both sides by $h$.", r"f = \dfrac{E_2 - E_1}{h}")],
                  [(r"f = \dfrac{h}{E_2 - E_1}", "This is upside down: divide $E_2 - E_1$ by $h$."),
                   (r"f = h(E_2 - E_1)", "$h$ multiplies $f$, so divide by $h$ when it moves."),
                   (r"f = \dfrac{E_2}{h} - E_1", "Divide the whole of $E_2 - E_1$ by $h$.")]),
            "E2": (r"E_2 = hf + E_1", [("Add $E_1$ to both sides.", r"E_2 = hf + E_1")],
                   [(r"E_2 = hf - E_1", "$E_1$ is subtracted from $E_2$, so it is added when it moves."),
                    (r"E_2 = E_1 - hf", "Check the signs: $E_2 = hf + E_1$."),
                    (r"E_2 = \dfrac{hf}{E_1}", "$E_1$ is subtracted, not multiplied, so add it to the other side.")]),
        },
    },
    "Ft=mv-mu": {
        "sheet": r"Ft = mv - mu",
        "targets": {
            "F": (r"F = \dfrac{mv - mu}{t}", [("Divide both sides by $t$.", r"F = \dfrac{mv - mu}{t}")],
                  [(r"F = \dfrac{t}{mv - mu}", "This is upside down: divide $mv - mu$ by $t$."),
                   (r"F = t(mv - mu)", "$t$ multiplies $F$, so divide by $t$ when it moves."),
                   (r"F = \dfrac{mv}{t} - mu", "Divide the whole of $mv - mu$ by $t$.")]),
            "t": (r"t = \dfrac{mv - mu}{F}", [("Divide both sides by $F$.", r"t = \dfrac{mv - mu}{F}")],
                  [(r"t = \dfrac{F}{mv - mu}", "This is upside down: divide $mv - mu$ by $F$."),
                   (r"t = F(mv - mu)", "$F$ multiplies $t$, so divide by $F$ when it moves."),
                   (r"t = \dfrac{mv}{F} - mu", "Divide the whole of $mv - mu$ by $F$.")]),
        },
    },
}

# Subjects whose name differs from SYMBOLS in these relationships
_SUM_NAMES = {
    ("a=(v-u)/t", "v"): ("v", "final speed"),
    ("E=V+Ir", "V"): ("V", "terminal potential difference"),
    ("E=V+Ir", "r"): ("r", "internal resistance"),
    ("E2-E1=hf", "E2"): ("E_2", "energy of the higher level"),
}


def _sum_question(key, level):
    rel = SUMS[key]
    x = random.choice(list(rel["targets"]))
    answer, steps, wrong = rel["targets"][x]
    tex, name = _SUM_NAMES.get((key, x)) or SYMBOLS[x]
    return _question(rel["sheet"], tex, name, answer, wrong, steps, level)


# ── The relationships for each level ─────────────────────────────────────────
# Each is (lhs, rhs) as Products, or a key into SUMS.

HALF = Fraction(1, 2)
REL = {
    "d=vt":      (prod("d"), prod("v", "t")),
    "d=vbar t":  (prod("d"), prod("vbar", "t")),
    "a=dv/t":    (prod("a"), prod("dv", ("t", -1))),
    "W=mg":      (prod("W"), prod("m", "g")),
    "F=ma":      (prod("F"), prod("m", "a")),
    "Ew=Fd":     (prod("Ew"), prod("F", "d")),
    "Ep=mgh":    (prod("Ep"), prod("m", "g", "h")),
    "Ek=1/2mv2": (prod("Ek"), prod("m", ("v", 2), coef=HALF)),
    "P=E/t":     (prod("P"), prod("E", ("t", -1))),
    "Q=It":      (prod("Q"), prod("I", "t")),
    "V=IR":      (prod("V"), prod("I", "R")),
    "P=IV":      (prod("P"), prod("I", "V")),
    "P=I2R":     (prod("P"), prod(("I", 2), "R")),
    "P=V2/R":    (prod("P"), prod(("V", 2), ("R", -1))),
    "Ew=QV":     (prod("Ew"), prod("Q", "V")),
    "Eh=cmdT":   (prod("Eh"), prod("c", "m", "dT")),
    "Eh=ml":     (prod("Eh"), prod("m", "l")),
    "p=F/A":     (prod("p"), prod("F", ("A", -1))),
    "p1V1=p2V2": (prod("p1", "V1"), prod("p2", "V2")),
    "p1/T1=p2/T2": (prod("p1", ("T1", -1)), prod("p2", ("T2", -1))),
    "V1/T1=V2/T2": (prod("V1", ("T1", -1)), prod("V2", ("T2", -1))),
    "v=f lam":   (prod("v"), prod("f", "lam")),
    "T=1/f":     (prod("T"), prod(("f", -1))),
    "f=N/t":     (prod("f"), prod("N", ("t", -1))),
    "A=N/t":     (prod("Act"), prod("N", ("t", -1))),
    "D=E/m":     (prod("D"), prod("E", ("m", -1))),
    "H=DwR":     (prod("H"), prod("D", "wR")),
    "Hdot=H/t":  (prod("Hdot"), prod("H", ("t", -1))),
    "V1/V2=R1/R2": (prod("Vr1", ("Vr2", -1)), prod("R1", ("R2", -1))),
    "p=mv":      (prod("mom"), prod("m", "v")),
    "F=Gm1m2/r2": (prod("F"), prod("G", "m1", "m2", ("r", -2))),
    "W=QV":      (prod("Ew"), prod("Q", "V")),
    "E=mc2":     (prod("E"), prod("m", ("cl", 2))),
    "E=hf":      (prod("E"), prod("hp", "f")),
    "z=v/c":     (prod("z"), prod("v", ("cl", -1))),
    "v=H0d":     (prod("v"), prod("H0", "dist")),
    "dsin=m lam": (prod("gs", "sin"), prod("order", "lam")),
    "n=sin1/sin2": (prod("n"), prod("sin1", ("sin2", -1))),
    "sinc=1/n":  (prod("sinc"), prod(("n", -1))),
    "I=k/d2":    (prod("Irr"), prod("k", ("dist", -2))),
    "I=P/A":     (prod("Irr"), prod("P", ("A", -1))),
    "C=Q/V":     (prod("C"), prod("Q", ("V", -1))),
    "E=1/2QV":   (prod("Ec"), prod("Q", "V", coef=HALF)),
    "E=1/2CV2":  (prod("Ec"), prod("C", ("V", 2), coef=HALF)),
    "E=1/2Q2/C": (prod("Ec"), prod(("Q", 2), ("C", -1), coef=HALF)),
}

# Level → group (one question style each) → relationships
RELATIONSHIPS = {
    "S3": {
        "Motion and Forces": ["d=vt", "a=dv/t", "W=mg", "F=ma"],
        "Waves":             ["v=f lam", "T=1/f", "f=N/t"],
        "Electricity and Energy": ["V=IR", "P=IV", "P=E/t", "Q=It", "Ew=Fd"],
    },
    "N4": {
        "Dynamics and Space":     ["d=vt", "a=dv/t", "W=mg", "F=ma", "Ew=Fd", "p=F/A"],
        "Electricity and Energy": ["V=IR", "P=IV", "P=E/t", "Q=It", "Eh=cmdT"],
        "Waves and Radiation":    ["v=f lam", "T=1/f", "f=N/t", "A=N/t", "H=DwR"],
    },
    "N5": {
        "Dynamics":    ["d=vbar t", "a=(v-u)/t", "W=mg", "F=ma", "Ew=Fd", "Ep=mgh", "Ek=1/2mv2", "P=E/t"],
        "Electricity": ["Q=It", "V=IR", "P=IV", "P=I2R", "P=V2/R", "Ew=QV", "V1/V2=R1/R2"],
        "Properties":  ["Eh=cmdT", "Eh=ml", "p=F/A", "p1V1=p2V2", "p1/T1=p2/T2", "V1/T1=V2/T2"],
        "Waves and Radiation": ["v=f lam", "T=1/f", "f=N/t", "A=N/t", "D=E/m", "H=DwR", "Hdot=H/t"],
    },
    "Higher": {
        "Our Dynamic Universe": ["d=vbar t", "v=u+at", "v2=u2+2as", "F=ma", "Ep=mgh", "Ek=1/2mv2",
                                 "p=mv", "Ft=mv-mu", "F=Gm1m2/r2", "z=v/c", "v=H0d"],
        "Particles and Waves":  ["W=QV", "E=mc2", "E=hf", "E2-E1=hf", "v=f lam", "dsin=m lam",
                                 "n=sin1/sin2", "sinc=1/n", "I=k/d2", "I=P/A"],
        "Electricity":          ["V=IR", "P=I2R", "P=V2/R", "E=V+Ir", "C=Q/V", "E=1/2QV", "E=1/2CV2", "E=1/2Q2/C"],
    },
}


def question_for(key, level, x=None):
    if key in SUMS:
        return _sum_question(key, level)
    return _product_question(REL[key], level, x=x)


def _group_generator(keys):
    def generate(level="N5"):
        return question_for(random.choice(keys), level)
    return generate


GENERATORS = {
    level: {group: _group_generator(keys) for group, keys in groups.items()}
    for level, groups in RELATIONSHIPS.items()
}
