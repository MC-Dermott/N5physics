"""Units that have been renamed or split. Assignments, test results, revision-guide rows and tracker exports
made before a split still carry the old unit name, so it is translated when read; nothing stored is changed."""

SPLIT_UNITS = {
    ("Higher", "Particles and Waves"): ("Particles", "Waves"),
    ("Crash Higher", "Particles and Waves"): ("Particles", "Waves"),
}


def unit_names(qualification, unit):
    """Every name results for this unit may be stored under: its own, then any older one."""
    return [unit] + [old for (qual, old), new in SPLIT_UNITS.items() if qual == qualification and unit in new]


def current_unit(registry, qualification, unit, question_type):
    """Today's unit for a stored (unit, topic). A topic found in both halves goes to the first."""
    for new in SPLIT_UNITS.get((qualification, unit), ()):
        if question_type in registry.get(qualification, {}).get(new, {}):
            return new
    return unit


def unit_entries(registry, qualification, unit):
    """A unit's {topic: generator(s)}. An old, split unit gives both halves together, so that work set
    before the split can still be taken."""
    units = registry.get(qualification, {})
    if unit in units or (qualification, unit) not in SPLIT_UNITS:
        return units.get(unit, {})
    merged = {}
    for new in SPLIT_UNITS[(qualification, unit)]:
        for topic, entry in units[new].items():
            if topic not in merged:
                merged[topic] = dict(entry) if isinstance(entry, dict) else entry
            elif isinstance(entry, dict):     # Definitions and Exam Style are in both halves
                for style, fn in entry.items():
                    merged[topic][f"{new}: {style}" if style in merged[topic] else style] = fn
    return merged
