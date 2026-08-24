# Worked examples shown to students before they practise each question type.
#
# Key:   (topic, question_type)                — applies to every sub-type/level
#        (topic, question_type, sub_type)       — applies to one specific sub-type/level
# Value: markdown string (rendered with st.markdown, supports $...$ / $$...$$ LaTeX)
#
# A (topic, question_type, sub_type) key takes priority over the plain
# (topic, question_type) key when both exist.

EXAMPLES = {
    ("Dynamics", "Distance and Displacement", "Level 1 — 1D"): r"""
**Example:** A cyclist travels 15 m east, then 22 m west, then 8 m east.

*(a) Calculate the total distance travelled.*

Distance adds up the magnitude of every leg, regardless of direction:
$$d = 15 + 22 + 8 = 45\ \mathrm{m}$$

*(b) Taking east as positive, calculate the resultant displacement.*

Displacement adds the **signed** values, so legs in opposite directions partly cancel:
$$s = (+15) + (-22) + (+8) = +1\ \mathrm{m}$$

The resultant displacement is **1 m east**.
""",

    ("Dynamics", "Distance and Displacement", "Level 2 — Two Displacements (2D)"): r"""
**Example:** A boat travels 8 km north and 6 km east.

*Calculate the magnitude and bearing of the resultant displacement.*

**Magnitude** — combine the two perpendicular legs with Pythagoras:
$$R = \sqrt{8^2 + 6^2} = \sqrt{100} = 10\ \mathrm{km}$$

**Bearing** — find the angle east of north, then apply the quadrant rule:
$$\theta = \tan^{-1}\left(\frac{6}{8}\right) = 36.9°$$

Both legs are positive (north and east), so the resultant lies in the NE quadrant, where bearing $= \theta$:
$$\text{Bearing} = 037°$$
""",

    ("Dynamics", "Distance and Displacement", "Level 3 — Multiple Displacements (2D)"): r"""
**Example:** A hiker walks 12 km north, then 9 km east, then 4 km south.

*Calculate the magnitude and bearing of the resultant displacement from the start.*

**Step 1 — resolve onto the N/E axes and sum each axis separately:**
$$\Sigma N = 12 - 4 = 8\ \mathrm{km} \qquad \Sigma E = 9\ \mathrm{km}$$

**Step 2 — magnitude** (Pythagoras):
$$R = \sqrt{(\Sigma N)^2 + (\Sigma E)^2} = \sqrt{8^2 + 9^2} = \sqrt{145} = 12.04\ \mathrm{km}$$

**Step 3 — bearing:**
$$\theta = \tan^{-1}\left(\frac{9}{8}\right) = 48.4°$$

$\Sigma N$ and $\Sigma E$ are both positive, so the resultant lies in the NE quadrant, where bearing $= \theta$:
$$\text{Bearing} = 048°$$
""",
}


def get_examples(topic, question_type, sub_type=None):
    if sub_type is not None:
        example = EXAMPLES.get((topic, question_type, sub_type))
        if example is not None:
            return example
    return EXAMPLES.get((topic, question_type))
