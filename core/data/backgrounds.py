# Background video links shown to students before they practise each topic.
# Key:   (topic, question_type)  — matches the strings in question_factory.py
# Value: list of {"title": str, "url": str}
#
# For Heat sub-types (Specific Heat Capacity, Specific Latent Heat, etc.)
# the key is ("Properties", "Heat") and applies to all sub-types.

BACKGROUND_VIDEOS = {
    ("Dynamics", "Speed, Distance & Time"): [
        # {"title": "Speed, Distance and Time", "url": "https://..."},
    ],
    ("Dynamics", "Acceleration"): [
        # {"title": "Acceleration", "url": "https://..."},
    ],
    ("Dynamics", "Forces"): [
        # {"title": "Newton's Laws", "url": "https://..."},
    ],
    ("Dynamics", "Weight"): [
        # {"title": "Weight and Gravity", "url": "https://..."},
    ],
    ("Dynamics", "Energy"): [
        # {"title": "Work, KE and GPE", "url": "https://..."},
    ],
    ("Dynamics", "Projectile Motion"): [
        # {"title": "Projectile Motion", "url": "https://..."},
    ],
    ("Dynamics", "Vectors"): [
        # {"title": "Vectors", "url": "https://..."},
    ],
    ("Electricity", "Current"): [
        # {"title": "Electric Current and Charge", "url": "https://..."},
    ],
    ("Electricity", "Ohm's Law"): [
        # {"title": "Ohm's Law", "url": "https://..."},
    ],
    ("Electricity", "Resistors"): [
        # {"title": "Resistors in Series and Parallel", "url": "https://..."},
    ],
    ("Electricity", "Electrical Power"): [
        # {"title": "Electrical Power and Energy", "url": "https://..."},
    ],
    ("Electricity", "Potential Divider"): [
        # {"title": "Potential Dividers", "url": "https://..."},
    ],
    ("Electricity", "Circuits"): [
        # {"title": "Circuit Analysis", "url": "https://..."},
    ],
    ("Radiation", "Dose"): [
        # {"title": "Absorbed and Equivalent Dose", "url": "https://..."},
    ],
    ("Radiation", "Half-Life"): [
        # {"title": "Half-Life", "url": "https://..."},
    ],
    ("Radiation", "Activity"): [
        # {"title": "Activity and Becquerels", "url": "https://..."},
    ],
    ("Waves", "Wave Speed"): [
        # {"title": "Wave Speed", "url": "https://..."},
    ],
    ("Waves", "Period & Frequency"): [
        # {"title": "Period and Frequency", "url": "https://..."},
    ],
    ("Waves", "Waves Combined"): [
        # {"title": "Waves — Combined", "url": "https://..."},
    ],
    ("Properties", "Pressure"): [
        # {"title": "Pressure", "url": "https://..."},
    ],
    ("Properties", "Gas Laws"): [
        # {"title": "Gas Laws", "url": "https://..."},
    ],
    ("Properties", "Heat"): [
        # {"title": "Specific Heat Capacity", "url": "https://..."},
        # {"title": "Specific Latent Heat", "url": "https://..."},
    ],
}


def get_background_videos(topic, question_type):
    return BACKGROUND_VIDEOS.get((topic, question_type), [])
