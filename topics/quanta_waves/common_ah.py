"""Shared helpers and data-sheet constants for the AH Quanta and Waves generators."""
import functools

from topics.rotational_motion import common_ah as _base
from topics.rotational_motion.common_ah import EXPLAIN_TIP, LEVEL, L, T, fmt, ltx, pick_sig, sig, uni

UNIT = "Quanta and Waves"

H = 6.63e-34
C = 3.00e8
E_CHARGE = 1.60e-19
M_E = 9.11e-31
M_P = 1.673e-27
M_N = 1.675e-27
M_ALPHA = 6.645e-27
V_SOUND = 340.0

calc = functools.partial(_base.calc, topic=UNIT)
explain_set = functools.partial(_base.explain_set, topic=UNIT)
