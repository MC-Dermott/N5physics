_TO_SUPERSCRIPT = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def format_answer(question):
    """A question's correct answer and unit for display: very large or small numbers in
    scientific notation (7.81 × 10¹²) rather than as a raw float."""
    value = question.correct_answer
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        x = float(value)
        if x == 0 or 1e-3 <= abs(x) < 1e6:
            text = f"{x:.6g}"
        else:
            coeff, exp = f"{x:.3e}".split("e")
            text = f"{coeff.rstrip('0').rstrip('.')} × 10{str(int(exp)).translate(_TO_SUPERSCRIPT)}"
    else:
        text = str(value)
    return f"{text} {question.unit}".strip()
