import random

from topics.dynamics.speed_distance_time   import generate_sdt
from topics.dynamics.acceleration          import generate_acceleration
from topics.dynamics.acceleration_s3       import gen_change_in_speed, gen_initial_final_speed
from topics.dynamics.instantaneous_speed_s3 import gen_instantaneous_speed, gen_average_speed_light_gate
from topics.dynamics.forces                import generate_forces
from topics.dynamics.weight                import generate_weight
from topics.dynamics.energy                import generate_energy
from topics.dynamics.projectiles           import generate_projectiles
from topics.dynamics.displacement          import (
    generate_vectors,
    generate_displacement_l1,
    generate_displacement_l2,
    generate_displacement_l3,
    gen_speed_velocity_from_displacement,
    generate_resultant_velocity,
)
from topics.dynamics.velocity_time_graphs  import (
    gen_which_graph_matches,
    gen_distance_displacement,
    gen_acceleration_interval,
)
from topics.dynamics.vectors_scalars       import gen_identify, gen_pairs
from topics.dynamics.equations_of_motion   import generate_equations_of_motion
from topics.dynamics.equations_of_motion_vertical import generate_equations_of_motion_vertical
from topics.dynamics.graphs_of_motion      import generate_graphs_of_motion, generate_at_graph_velocity
from topics.dynamics.special_relativity    import generate_special_relativity
from topics.dynamics.gravitation           import generate_orbital_gravitation
from topics.dynamics.projectile_higher     import (
    generate_projectile_l1,
    generate_projectile_l2,
    generate_projectile_max_height,
    generate_projectile_exam_style,
)
from topics.dynamics.towing                import (
    gen_l1_one_trailer_no_friction,
    gen_l2_one_trailer_friction,
    gen_l3_multi_trailer_no_friction,
    gen_l4_multi_trailer_friction,
    gen_exam_style as gen_towing_exam_style,
)
from topics.dynamics.resolving_forces_higher import (
    gen_rf_l1_components,
    gen_rf_l2_balancing_and_accel,
    gen_rf_l3_weight_on_slope,
    gen_rf_l4_slope_dynamics,
    gen_rf_l5_up_slope,
    gen_rf_l6_explain_angle,
)
from topics.dynamics.momentum_impulse      import (
    generate_momentum_basic,
    gen_stick_together,
    gen_separate,
    gen_explosion,
    generate_impulse_basic,
    gen_impulse_graph,
    gen_elastic_inelastic,
)
from topics.dynamics.energy_work_power_higher import (
    generate_work_done as generate_work_done_higher,
    generate_gpe as generate_gpe_higher,
    generate_ke as generate_ke_higher,
    generate_power as generate_power_higher,
    gen_energy_freefall_speed,
    gen_energy_max_height,
    gen_energy_friction_force,
    gen_energy_lift_power,
    gen_energy_engine_power,
)
from topics.dynamics.effective_weight_higher import (
    generate_effective_weight_lifts,
    gen_ew_constant_velocity,
    generate_effective_weight_beyond_lifts,
    gen_ew_explain_freefall,
)

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
    "S3": {
        "Dynamics": {
            "Speed, Distance & Time": generate_sdt,
            "Acceleration": {
                "Change in Speed":         gen_change_in_speed,
                "Initial & Final Speed":   gen_initial_final_speed,
            },
            "Instantaneous Speed": {
                "Instantaneous Speed at a Point": gen_instantaneous_speed,
                "Average Speed Over the Run":     gen_average_speed_light_gate,
            },
        },
        "Waves": {
            "Wave Speed":         generate_wave_speed,
            "Period & Frequency": generate_period_frequency,
            "Waves Combined":     generate_waves_combined,
        },
    },
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
            "Distance and Displacement": {
                "Level 1 — 1D":                     generate_displacement_l1,
                "Level 2 — Two Displacements (2D)":  generate_displacement_l2,
                "Level 3 — Multiple Displacements (2D)": generate_displacement_l3,
            },
            "Vectors and Scalars": {
                "Identify Scalar or Vector":  gen_identify,
                "Scalar & Vector Pairs":      gen_pairs,
            },
            "Speed and Velocity": {
                "From a Compound Displacement": gen_speed_velocity_from_displacement,
                "Resultant Velocity": generate_resultant_velocity,
                "Which v-t Graph Matches?": gen_which_graph_matches,
                "v-t Graphs — Distance and Displacement": gen_distance_displacement,
                "v-t Graphs — Acceleration from an Interval": gen_acceleration_interval,
            },
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
            "Equations of Motion": {
                "Horizontal Motion": generate_equations_of_motion,
                "Vertical Motion":   generate_equations_of_motion_vertical,
            },
            "Graphs of Motion": {
                "Graph Matching":          generate_graphs_of_motion,
                "Velocity from a-t Graph": generate_at_graph_velocity,
            },
            "Special Relativity":  generate_special_relativity,
            "Gravitation":         generate_orbital_gravitation,
            "Projectile Motion": {
                "Level 1 — Same Height":      generate_projectile_l1,
                "Level 2 — Different Height": generate_projectile_l2,
                "Time to Maximum Height":     generate_projectile_max_height,
                "Level 3 — Exam Style":       generate_projectile_exam_style,
            },
            "Towing": {
                "Level 1 — One Trailer, No Friction":        gen_l1_one_trailer_no_friction,
                "Level 2 — One Trailer, With Friction":      gen_l2_one_trailer_friction,
                "Level 3 — Multiple Trailers, No Friction":  gen_l3_multi_trailer_no_friction,
                "Level 4 — Multiple Trailers, With Friction": gen_l4_multi_trailer_friction,
                "Level 5 — Exam Style":                      gen_towing_exam_style,
            },
            "Components of Vectors": {
                "Level 1 — Finding Components":                              gen_rf_l1_components,
                "Level 2 — Balancing Forces and Force from Acceleration":    gen_rf_l2_balancing_and_accel,
                "Level 3 — Weight on a Slope":                               gen_rf_l3_weight_on_slope,
                "Level 4 — Acceleration, Force and Angle on a Slope":        gen_rf_l4_slope_dynamics,
                "Level 5 — Sliding Up a Slope With Friction":                gen_rf_l5_up_slope,
                "Level 6 — Explain: Effect of Angle":                        gen_rf_l6_explain_angle,
            },
            "Momentum and Impulse": {
                "Momentum":                    generate_momentum_basic,
                "Collisions — Stick Together":  gen_stick_together,
                "Collisions — Separate":        gen_separate,
                "Explosions and Recoil":        gen_explosion,
                "Impulse":                      generate_impulse_basic,
                "Impulse from a Force-Time Graph": gen_impulse_graph,
                "Elastic and Inelastic Collisions": gen_elastic_inelastic,
            },
            "Energy, Work and Power": {
                "Work Done":                   generate_work_done_higher,
                "Gravitational Potential Energy": generate_gpe_higher,
                "Kinetic Energy":               generate_ke_higher,
                "Power":                        generate_power_higher,
                "Conservation — Free-Fall Speed": gen_energy_freefall_speed,
                "Conservation — Maximum Height": gen_energy_max_height,
                "Conservation — Frictional Force": gen_energy_friction_force,
                "Conservation — Useful Power":  gen_energy_lift_power,
                "Conservation — Engine Power":  gen_energy_engine_power,
            },
            "Effective Weight": {
                "Lifts":                         generate_effective_weight_lifts,
                "Lifts — Constant Velocity":      gen_ew_constant_velocity,
                "Beyond Lifts":                   generate_effective_weight_beyond_lifts,
                "Beyond Lifts — Explain Free Fall": gen_ew_explain_freefall,
            },
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
    level_map = {"S3": "S3", "National 4": "N4", "National 5": "N5", "Higher": "Higher"}
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
