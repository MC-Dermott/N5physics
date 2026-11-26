"""AH — Kinematic relationships: calculus and motion graphs."""
import random

from topics.rotational_motion.common_ah import L, T, calc, ltx, sig, uni

QT = "Kinematic Relationships"

NOTES = r"""
## Kinematic relationships

$$v = \frac{ds}{dt} \qquad a = \frac{dv}{dt} = \frac{d^2s}{dt^2}$$

$$v = u + at \qquad s = ut + \tfrac{1}{2}at^2 \qquad v^2 = u^2 + 2as$$

- The three equations of motion apply **only when the acceleration is constant**. If $a$, $v$ or $s$
  is given as a function of $t$, use calculus.
- Differentiate: $s \to v \to a$. Integrate: $a \to v \to s$.
- Every integration needs a **constant of integration** (or limits). Find it from the starting conditions.
- The gradient of an s–t graph is the velocity; the gradient of a v–t graph is the acceleration.
- The area under an a–t graph is the change in velocity; under a v–t graph it is the displacement.
"""


def gen_differentiate(level="AH"):
    a, b, c = uni(0.20, 0.90, 2), uni(1.0, 4.0), uni(1.0, 9.0)
    t = uni(2.0, 6.0)
    eq = f"s = {a:g}t³ + {b:g}t² + {c:g}t"
    stem = (f"The displacement s, in metres, of an object moving in a straight line is given by "
            f"**{eq}**, where t is in seconds. ")
    v = 3 * a * t**2 + 2 * b * t + c
    acc = 6 * a * t + 2 * b
    v_expr = rf"v = \frac{{ds}}{{dt}} = {sig(3*a):g}t^2 + {sig(2*b):g}t + {c:g}"
    if random.random() < 0.5:
        return calc(QT, stem + f"Calculate the velocity of the object at t = {t:g} s.", v, "m s⁻¹",
                    [v_expr, rf"v = {sig(3*a):g}({t:g})^2 + {sig(2*b):g}({t:g}) + {c:g}",
                     rf"v = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[((a * t**3 + b * t**2 + c * t) / t,
                            "That is s ÷ t, the average velocity. Differentiate s to get the velocity at an instant."),
                           (acc, "That is the acceleration — differentiate only once for velocity.")],
                    scaffold=[("What is the coefficient of t² in ds/dt?", 3 * a),
                              ("What is the velocity?", v, "m s⁻¹")], notes=NOTES)
    return calc(QT, stem + f"Calculate the acceleration of the object at t = {t:g} s.", acc, "m s⁻²",
                [v_expr, rf"a = \frac{{dv}}{{dt}} = {sig(6*a):g}t + {sig(2*b):g}",
                 rf"a = {sig(6*a):g}({t:g}) + {sig(2*b):g} = {ltx(acc)}\ \mathrm{{m\,s^{{-2}}}}"],
                wrong=[(v, "That is the velocity — differentiate a second time for acceleration."),
                       (v / t, "a is not v ÷ t when the acceleration changes. Differentiate v.")],
                scaffold=[("What is the coefficient of t in d²s/dt²?", 6 * a),
                          ("What is the acceleration?", acc, "m s⁻²")], notes=NOTES)


def gen_integrate(level="AH"):
    p, q = uni(0.20, 0.90, 2), uni(1.0, 3.0)
    u, t = uni(2.0, 8.0), uni(3.0, 6.0)
    stem = (f"The acceleration a, in m s⁻², of a vehicle is given by **a = {p:g}t + {q:g}**, "
            f"where t is in seconds. At t = 0 the velocity is {u:g} m s⁻¹ and the displacement is zero. ")
    v = p * t**2 / 2 + q * t + u
    v_expr = rf"v = \int a\,dt = {sig(p/2):g}t^2 + {q:g}t + c \qquad c = {u:g}"
    if random.random() < 0.5:
        return calc(QT, stem + f"Calculate the velocity of the vehicle at t = {t:g} s.", v, "m s⁻¹",
                    [v_expr, rf"v = {sig(p/2):g}({t:g})^2 + {q:g}({t:g}) + {u:g} = {ltx(v)}\ \mathrm{{m\,s^{{-1}}}}"],
                    wrong=[(v - u, "You left out the constant of integration — at t = 0 the velocity is not zero."),
                           (u + (p * t + q) * t,
                            "v = u + at only works for constant acceleration. Integrate a(t).")],
                    scaffold=[("What is the constant of integration?", u, "m s⁻¹"),
                              ("What is the velocity?", v, "m s⁻¹")], notes=NOTES)
    s = p * t**3 / 6 + q * t**2 / 2 + u * t
    return calc(QT, stem + f"Calculate the displacement of the vehicle at t = {t:g} s.", s, "m",
                [v_expr, rf"s = \int v\,dt = {ltx(p/6)}t^3 + {sig(q/2):g}t^2 + {u:g}t \quad (c = 0)",
                 rf"s = {ltx(s)}\ \mathrm{{m}}"],
                wrong=[(s - u * t, "You lost the initial velocity: the first constant of integration is u."),
                       (u * t + 0.5 * (p * t + q) * t**2,
                        "s = ut + ½at² only works for constant acceleration. Integrate twice.")],
                scaffold=[("What is the velocity at that time?", v, "m s⁻¹"),
                          ("What is the displacement?", s, "m")], notes=NOTES)


def gen_graphs(level="AH"):
    k, m = uni(0.20, 0.80, 2), uni(1.0, 4.0)
    t1 = random.randint(1, 3)
    t2 = t1 + random.randint(2, 4)
    if random.random() < 0.5:
        grad = 2 * k * t2 + m
        return calc(QT, (f"The velocity–time graph of a trolley is the curve **v = {k:g}t² + {m:g}t** "
                         f"(v in m s⁻¹, t in s). Determine the gradient of the tangent to the graph at t = {t2} s, "
                         f"the instantaneous acceleration."), grad, "m s⁻²",
                    [rf"a = \frac{{dv}}{{dt}} = {sig(2*k):g}t + {m:g}",
                     rf"a = {ltx(grad)}\ \mathrm{{m\,s^{{-2}}}}"],
                    wrong=[(k * t2 + m, "v ÷ t is the gradient from the origin, not the gradient of the tangent.")],
                    notes=NOTES)
    area = k * (t2**3 - t1**3) / 3 + m * (t2**2 - t1**2) / 2
    whole = k * t2**3 / 3 + m * t2**2 / 2
    v1, v2 = k * t1**2 + m * t1, k * t2**2 + m * t2
    return calc(QT, (f"The velocity of a trolley is given by **v = {k:g}t² + {m:g}t** (v in m s⁻¹, t in s). "
                     f"By finding the area under the velocity–time graph, calculate the displacement of the "
                     f"trolley between t = {t1} s and t = {t2} s."), area, "m",
                [rf"s = \int_{{{t1}}}^{{{t2}}} ({k:g}t^2 + {m:g}t)\,dt",
                 rf"s = \left[{ltx(k/3)}t^3 + {sig(m/2):g}t^2\right]_{{{t1}}}^{{{t2}}}",
                 rf"s = {ltx(area)}\ \mathrm{{m}}"],
                wrong=[(whole, "That is the displacement from t = 0. Subtract the value at the lower limit."),
                       ((v1 + v2) / 2 * (t2 - t1),
                        "The graph is a curve, so a trapezium is only an approximation. Integrate between the limits.")],
                notes=NOTES)
