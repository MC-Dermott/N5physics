import random

from topics.dynamics.speed_distance_time import generate_sdt
from topics.dynamics.acceleration        import generate_acceleration
from topics.dynamics.forces              import generate_forces
from topics.dynamics.weight              import generate_weight
from topics.dynamics.energy              import generate_energy
from topics.dynamics.projectiles         import generate_projectiles
from topics.dynamics.vectors             import generate_vectors

from topics.electricity.current          import generate_current
from topics.electricity.ohms_law         import generate_ohms_law
from topics.electricity.resistors        import generate_resistors
from topics.electricity.power            import generate_power
from topics.electricity.potential_divider import generate_potential_divider
from topics.electricity.circuits         import generate_circuits

from topics.radiation.dose               import generate_dose
from topics.radiation.half_life          import generate_half_life
from topics.radiation.activity           import generate_activity

from topics.waves.wave_speed             import generate_wave_speed
from topics.waves.period_frequency       import generate_period_frequency
from topics.waves.combined               import generate_waves_combined

from topics.properties.pressure          import generate_pressure
from topics.properties.gas_laws          import generate_gas_laws
from topics.properties.heat              import (
    generate_heat, generate_heat_shc, generate_heat_latent,
    generate_heat_exam_icemachine,
)

QUAL_REGISTRY = {
    "National 4": {
        "Dynamics": {
            "Speed, Distance & Time": generate_sdt,
            "Weight":                 generate_weight,
        },
        "Electricity": {
            "Current":   generate_current,
            "Ohm's Law": generate_ohms_law,
        },
        "Waves": {
            "Wave Speed": generate_wave_speed,
        },
        "Properties": {
            "Pressure": generate_pressure,
        },
    },
    "National 5": {
        "Dynamics": {
            "Speed, Distance & Time": generate_sdt,
            "Acceleration":           generate_acceleration,
            "Forces":                 generate_forces,
            "Weight":                 generate_weight,
            "Energy":                 generate_energy,
            "Projectile Motion":      generate_projectiles,
            "Vectors":                generate_vectors,
        },
        "Electricity": {
            "Current":            generate_current,
            "Ohm's Law":          generate_ohms_law,
            "Resistors":          generate_resistors,
            "Electrical Power":   generate_power,
            "Potential Divider":  generate_potential_divider,
            "Circuits":           generate_circuits,
        },
        "Radiation": {
            "Dose":      generate_dose,
            "Half-Life": generate_half_life,
            "Activity":  generate_activity,
        },
        "Waves": {
            "Wave Speed":        generate_wave_speed,
            "Period & Frequency": generate_period_frequency,
            "Waves Combined":    generate_waves_combined,
        },
        "Properties": {
            "Pressure": generate_pressure,
            "Gas Laws": generate_gas_laws,
            "Heat": {
                "Specific Heat Capacity": generate_heat_shc,
                "Specific Latent Heat":   generate_heat_latent,
                "Mixed":                  generate_heat,
                "Exam Style":             generate_heat_exam_icemachine,
            },
        },
    },
    "Higher": {
        "Dynamics": {
            "Speed, Distance & Time": generate_sdt,
            "Acceleration":           generate_acceleration,
            "Forces":                 generate_forces,
            "Weight":                 generate_weight,
            "Energy":                 generate_energy,
            "Projectile Motion":      generate_projectiles,
            "Vectors":                generate_vectors,
        },
        "Electricity": {
            "Current":            generate_current,
            "Ohm's Law":          generate_ohms_law,
            "Resistors":          generate_resistors,
            "Electrical Power":   generate_power,
            "Potential Divider":  generate_potential_divider,
            "Circuits":           generate_circuits,
        },
        "Radiation": {
            "Dose":      generate_dose,
            "Half-Life": generate_half_life,
            "Activity":  generate_activity,
        },
        "Waves": {
            "Wave Speed":         generate_wave_speed,
            "Period & Frequency": generate_period_frequency,
            "Waves Combined":     generate_waves_combined,
        },
        "Properties": {
            "Pressure": generate_pressure,
            "Gas Laws": generate_gas_laws,
            "Heat": {
                "Specific Heat Capacity": generate_heat_shc,
                "Specific Latent Heat":   generate_heat_latent,
                "Mixed":                  generate_heat,
                "Exam Style":             generate_heat_exam_icemachine,
            },
        },
    },
}


def get_topics(qualification):
    return list(QUAL_REGISTRY.get(qualification, {}).keys())


def get_question_types(qualification, topic):
    return list(QUAL_REGISTRY.get(qualification, {}).get(topic, {}).keys())


def get_sub_types(qualification, topic, question_type):
    entry = QUAL_REGISTRY.get(qualification, {}).get(topic, {}).get(question_type)
    if isinstance(entry, dict):
        return list(entry.keys())
    return None


def generate_question(qualification, topic, question_type, sub_type=None):
    level_map = {"National 4": "N4", "National 5": "N5", "Higher": "Higher"}
    level = level_map.get(qualification, "N5")
    entry = QUAL_REGISTRY[qualification][topic][question_type]
    if isinstance(entry, dict):
        fn = entry[sub_type] if sub_type in entry else random.choice(list(entry.values()))
    else:
        fn = entry
    return fn(level=level)
