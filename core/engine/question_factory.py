import random

from topics.dynamics.speed_distance_time   import generate_sdt
from topics.dynamics.acceleration          import generate_acceleration
from topics.dynamics.forces                import generate_forces
from topics.dynamics.weight                import generate_weight
from topics.dynamics.energy                import generate_energy
from topics.dynamics.projectiles           import generate_projectiles
from topics.dynamics.vectors               import generate_vectors
from topics.dynamics.equations_of_motion   import generate_equations_of_motion
from topics.dynamics.special_relativity    import generate_special_relativity
from topics.dynamics.gravitation           import generate_orbital_gravitation

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

from topics.particles_and_waves.standard_model import (
    generate_standard_model_classification,
    generate_standard_model_order_of_magnitude,
)

from topics.electricity_and_energy.electrical_power import generate_electrical_power
from topics.electricity_and_energy.efficiency       import (
    generate_efficiency,
    generate_power_efficiency_scenario,
)
from topics.electricity_and_energy.knowledge        import (
    generate_renewable_energy,
    generate_input_output_devices,
    generate_electromagnets,
)

QUAL_REGISTRY = {
    "National 4": {
        "Electricity and Energy": {
            "Electrical Power":     generate_electrical_power,
            "Efficiency":           generate_efficiency,
            "Power and Efficiency": generate_power_efficiency_scenario,
            "Renewable Energy":     generate_renewable_energy,
            "Input/Output Devices": generate_input_output_devices,
            "Electromagnets":       generate_electromagnets,
            "Current":              generate_current,
            "Ohm's Law":            generate_ohms_law,
        },
        "Waves and Radiation": {
            "Wave Speed": generate_wave_speed,
            "Dose":       generate_dose,
            "Half-Life":  generate_half_life,
            "Activity":   generate_activity,
        },
        "Dynamics and Space": {
            "Speed, Distance & Time": generate_sdt,
            "Weight":                 generate_weight,
            "Acceleration":           generate_acceleration,
            "Pressure":               generate_pressure,
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
        "Our Dynamic Universe": {
            "Equations of Motion": generate_equations_of_motion,
            "Special Relativity":  generate_special_relativity,
            "Gravitation":         generate_orbital_gravitation,
        },
        "Particles and Waves": {
            "Standard Model": {
                "Particle Classification": generate_standard_model_classification,
                "Order of Magnitude":     generate_standard_model_order_of_magnitude,
            },
        },
        "Electricity": {
        },
    },
    "Crash Higher": {
        "Our Dynamic Universe": {
            "Speed, Distance & Time": generate_sdt,
            "Acceleration":           generate_acceleration,
            "Forces":                 generate_forces,
            "Weight":                 generate_weight,
            "Energy":                 generate_energy,
            "Projectile Motion":      generate_projectiles,
            "Vectors":                generate_vectors,
        },
        "Particles and Waves": {
            "Wave Speed":         generate_wave_speed,
            "Period & Frequency": generate_period_frequency,
            "Waves Combined":     generate_waves_combined,
            "Energy":             generate_energy,
            "Standard Model": {
                "Particle Classification": generate_standard_model_classification,
                "Order of Magnitude":     generate_standard_model_order_of_magnitude,
            },
        },
        "Electricity": {
            "Current":           generate_current,
            "Ohm's Law":         generate_ohms_law,
            "Resistors":         generate_resistors,
            "Electrical Power":  generate_power,
            "Potential Divider": generate_potential_divider,
            "Circuits":          generate_circuits,
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
    q = fn(level=level)
    if sub_type:
        q.question_type = sub_type
        if q.is_scenario:
            for part in q.parts:
                if part.metadata.get("type") != "explain":
                    part.question_type = sub_type
    return q
