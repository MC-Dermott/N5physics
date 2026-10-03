import functools
import random

from topics.dynamics.speed_distance_time   import generate_sdt
from topics.dynamics.acceleration          import generate_acceleration
from topics.dynamics.acceleration_s3       import (
    gen_initial_final_speed,
    generate_acceleration_basic,
)
from topics.dynamics.acceleration_n5       import (
    generate_acceleration_equation,
    generate_trolley_light_gates,
    generate_trolley_explain,
)
from topics.dynamics.instantaneous_speed_s3 import gen_instantaneous_speed, gen_average_speed_light_gate
from topics.dynamics.vt_graph_distance_s3   import (
    gen_vt_distance_simple,
    gen_vt_distance_trapezium,
    gen_vt_distance_compound,
)
from topics.dynamics.vt_graph_acceleration_s3 import (
    gen_accel_graph_compare,
    gen_accel_graph_basic,
    gen_accel_graph_compound,
)
from topics.dynamics.weight_calculations_s3 import generate_weight_calculations
from topics.dynamics.unbalanced_forces_s3   import (
    gen_horizontal_unbalanced_force,
    generate_unbalanced_forces_s3,
)
from topics.dynamics.forces                import (
    generate_forces,
    gen_compare_forces,
    gen_resultant_force,
    gen_horizontal_forces,
)
from topics.dynamics.vertical_forces       import (
    gen_vertical_forces,
    gen_freefall_acceleration,
    gen_parachute_deceleration,
)
from topics.dynamics.weight                import generate_weight
from topics.dynamics.energy                import (
    generate_energy,
    generate_energy_gpe,
    generate_energy_ke,
    generate_energy_work,
    generate_energy_conservation,
    gen_energy_explain,
)
from topics.dynamics.energy_power          import generate_power_basic, generate_power_exam
from topics.dynamics.projectiles           import (
    generate_projectiles,
    gen_free_fall_velocity_and_height,
    gen_free_fall_time,
    gen_projectile_time_explain,
)
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
    gen_describe_graph_stage,
)
from topics.dynamics.vectors_scalars       import gen_identify, gen_pairs
from topics.dynamics.definitions_n5        import (
    gen_term_to_definition,
    gen_definition_to_term,
    gen_statements,
)
from topics.dynamics.definitions_higher    import (
    PART1_GENERATORS as odu_part1_definitions,
    PART2_GENERATORS as odu_part2_definitions,
)
from topics.dynamics.equations_of_motion   import generate_equations_of_motion
from topics.dynamics.equations_of_motion_vertical import generate_equations_of_motion_vertical
from topics.dynamics.graphs_of_motion      import generate_graphs_of_motion, generate_at_graph_velocity
from topics.dynamics.special_relativity    import (
    generate_special_relativity,
    generate_relativity_velocity,
    generate_relativity_time_dilation,
    generate_relativity_length_contraction,
    generate_relativity_definitions,
)
from topics.dynamics.gravitation           import generate_orbital_gravitation
from topics.dynamics.expanding_universe_higher import (
    gen_eu_doppler,
    gen_eu_doppler_explain,
    gen_eu_redshift,
    gen_eu_hubble,
    gen_eu_evidence,
    gen_eu_stellar,
)
from topics.dynamics.newtons_law_gravitation_higher import (
    gen_grav_force_mass_distance,
    gen_grav_units_centre_distance,
    gen_grav_field_at_height,
    gen_grav_force_change,
)
from topics.dynamics.projectile_higher     import (
    generate_projectile_vertical_displacement,
    generate_projectile_vertical_time_from_top,
    generate_projectile_horizontal,
    generate_projectile_exam_mixed,
    generate_projectile_explain,
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
    gen_ke_lost,
    gen_impulse_explain,
)
from topics.dynamics.energy_work_power_higher import (
    generate_work_done as generate_work_done_higher,
    generate_power as generate_power_higher,
    gen_energy_ep_ek,
    gen_energy_friction_force,
    gen_conservation_power,
)
from topics.dynamics.effective_weight_higher import (
    generate_effective_weight_lifts,
    generate_effective_weight_beyond_lifts,
    gen_ew_explain_freefall,
)

from topics.electricity.current          import generate_current
from topics.electricity.ohms_law         import generate_ohms_law
from topics.electricity.resistors        import generate_resistors
from topics.electricity.power            import generate_power
from topics.electricity.potential_divider import generate_potential_divider
from topics.electricity.circuits         import generate_circuits
from topics.dynamics.definitions_s3 import MOTION_GENERATORS as s3_motion_definitions, FORCES_GENERATORS as s3_forces_definitions
from topics.waves.definitions_s3 import GENERATORS as s3_waves_definitions
from topics.electricity_and_energy.definitions_n4 import GENERATORS as n4_electricity_definitions
from topics.waves.definitions_n4 import GENERATORS as n4_waves_definitions
from topics.dynamics.definitions_n4 import GENERATORS as n4_dynamics_definitions
from topics.skills.definitions_n5 import GENERATORS as skills_n5_definitions
from topics.dynamics.definitions_higher import CRASH_GENERATORS as crash_odu_definitions
from topics.properties.properties_exam_n5 import (
    gen_pm_heat_then_boil, gen_pm_latent_power, gen_pm_heating_curve,
    gen_pm_gas_kelvin, gen_pm_pressure_weight, gen_pm_kinetic_model,
)
from topics.particles_and_waves.particles_waves_higher import (
    gen_pw_charged_speed, gen_pw_accelerators, gen_pw_hadron_charge, gen_pw_bosons,
    gen_pw_mass_energy, gen_pw_reactions_per_second, gen_pw_isl, gen_pw_irradiance,
    gen_pw_photoelectric, gen_pw_pe_effects, gen_pw_grating, gen_pw_path_difference,
    gen_pw_energy_levels, gen_pw_spectra_explain, gen_pw_refraction, gen_pw_refraction_explain,
)
from topics.electricity.electricity_exam_n5 import (
    gen_ec_charge, gen_ec_electrons, gen_ec_ac_dc,
    gen_ec_ew_qv, gen_ec_gradient, gen_ec_voltage_meaning,
    gen_ec_series_parallel, gen_ec_parallel_total_current, gen_ec_circuit_changes,
    gen_ec_led_resistor, gen_ec_divider_switch, gen_ec_transistor_explain,
    gen_ec_fuse, gen_ec_power_i2r, gen_ec_energy_time, gen_ec_toaster_statements,
)
from topics.electricity.electricity_higher import (
    gen_he_peak_rms, gen_he_scope, gen_he_ac_explain,
    gen_he_resistance_power, gen_he_divider, gen_he_circuit_explain,
    gen_he_emf_calc, gen_he_emf_graph, gen_he_emf_explain,
    gen_he_cap_charge, gen_he_cap_energy, gen_he_cap_curves,
    gen_he_led_photon, gen_he_band_explain,
)
from topics.electricity.definitions_n5  import GENERATORS as electricity_n5_definitions
from topics.electricity.definitions_higher import GENERATORS as electricity_higher_definitions

from topics.radiation.dose               import generate_dose
from topics.radiation.half_life          import generate_half_life
from topics.radiation.activity           import generate_activity
from topics.radiation.definitions_n5     import GENERATORS as radiation_n5_definitions
from topics.radiation.radiation_exam_n5  import (
    gen_rd_dose, gen_rd_nature, gen_hl_activity, gen_hl_fission_power, gen_hl_explain,
)
from topics.space.space_n5               import (
    gen_sp_weight, gen_sp_rocket, gen_sp_explain, gen_cs_lightyear, gen_cs_light_time, gen_cs_explain,
)
from topics.space.definitions_n5         import GENERATORS as space_n5_definitions

from topics.waves.wave_speed             import generate_wave_speed
from topics.waves.period_frequency       import generate_period_frequency
from topics.waves.combined               import generate_waves_combined
from topics.waves.definitions_n5         import GENERATORS as waves_n5_definitions
from topics.waves.waves_exam_n5          import (
    gen_wv_echo, gen_wv_parameters, gen_wv_behaviour, gen_em_calc, gen_em_bands, gen_rf_explain, gen_rf_calc,
)

from topics.properties.pressure          import generate_pressure
from topics.properties.gas_laws          import generate_gas_laws
from topics.properties.heat              import (
    generate_heat, generate_heat_shc, generate_heat_latent,
    generate_heat_exam_icemachine,
)
from topics.properties.definitions_n5    import GENERATORS as properties_n5_definitions

from topics.particles_and_waves.standard_model import (
    generate_standard_model_classification,
    generate_standard_model_order_of_magnitude,
)
from topics.particles_and_waves.definitions_higher import (
    GENERATORS as particles_waves_definitions,
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

from topics.exam_style.base import EXAM_STYLE
from utils.diagrams import with_diagram
from utils.light_gate_diagram import light_gate_diagram
from topics.exam_style import (
    n5_dynamics, n5_electricity, n5_radiation, n5_waves, n5_properties, n5_space,
    higher_odu, higher_particles_waves, higher_electricity,
)

from topics.skills.prefixes import (
    gen_name_to_power,
    gen_power_to_name,
    gen_symbol_to_name,
    gen_name_to_symbol,
)

QUAL_REGISTRY = {
    "S3": {
        "Dynamics Part 1 (Motion)": {
            "Speed, Distance & Time": generate_sdt,
            "Acceleration": {
                "Acceleration, Time & Change in Speed": generate_acceleration_basic,
                "Initial & Final Speed":                gen_initial_final_speed,
            },
            "Instantaneous Speed": {
                "Instantaneous Speed at a Point": gen_instantaneous_speed,
                "Average Speed Over the Run":     gen_average_speed_light_gate,
            },
            "V-T Graphs": {
                "Distance — Simple Shapes":    gen_vt_distance_simple,
                "Distance — Trapezium Shapes": gen_vt_distance_trapezium,
                "Distance — Compound Graphs":  gen_vt_distance_compound,
                "Acceleration — Comparing Steepness":   gen_accel_graph_compare,
                "Acceleration — Calculating from a Graph": gen_accel_graph_basic,
                "Acceleration — Compound Graphs":       gen_accel_graph_compound,
            },
            "Definitions": s3_motion_definitions,
        },
        "Dynamics Part 2 (Forces)": {
            "Weight Calculations": generate_weight_calculations,
            "Unbalanced Forces": {
                "Horizontal (driving vs friction)": gen_horizontal_unbalanced_force,
                "Vertical (with weight)":           generate_unbalanced_forces_s3,
            },
            "Definitions": s3_forces_definitions,
        },
        "Waves": {
            "Wave Speed":         generate_wave_speed,
            "Period & Frequency": generate_period_frequency,
            "Waves Combined":     generate_waves_combined,
            "Definitions":        s3_waves_definitions,
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
            "Definitions":          n4_electricity_definitions,
        },
        "Waves and Radiation": {
            "Wave Speed": generate_wave_speed,
            "Dose":       generate_dose,
            "Half-Life":  generate_half_life,
            "Activity":   generate_activity,
            "Definitions": n4_waves_definitions,
        },
        "Dynamics and Space": {
            "Speed, Distance & Time": generate_sdt,
            "Weight":                 generate_weight,
            "Acceleration":           generate_acceleration,
            "Pressure":               generate_pressure,
            "Definitions":            n4_dynamics_definitions,
        },
    },
    "National 5": {
        "Dynamics": {
            "Speed, Distance & Time": generate_sdt,
            "Acceleration": {
                "Using a = (v − u) ÷ t":            generate_acceleration_equation,
                "Trolley on a Slope — Light Gates":  generate_trolley_light_gates,
                "Trolley on a Slope — Method":       generate_trolley_explain,
            },
            "Forces": {
                "Explain — Comparing Forces": gen_compare_forces,
                "Resultant Force at Right Angles": gen_resultant_force,
                "Horizontal Forces":     gen_horizontal_forces,
                "Vertical Forces":       gen_vertical_forces,
            },
            "Vertical Motion": {
                "Free-Fall Acceleration": gen_freefall_acceleration,
                "Parachute Deceleration": gen_parachute_deceleration,
            },
            "Weight":                 generate_weight,
            "Energy": {
                "Gravitational Potential Energy": generate_energy_gpe,
                "Kinetic Energy":                 generate_energy_ke,
                "Conservation of Energy":         generate_energy_conservation,
                "Work Done":                      generate_energy_work,
                "Power — Basic":                  generate_power_basic,
                "Power — Exam-style":             generate_power_exam,
                "Explain":                        gen_energy_explain,
            },
            "Projectile Motion": {
                "Vertical Motion — Velocity & Height Fallen": gen_free_fall_velocity_and_height,
                "Vertical Motion — Time to Fall": gen_free_fall_time,
                "Full Projectile Motion": generate_projectiles,
                "Explain — Time to Hit the Ground": gen_projectile_time_explain,
            },
            "Distance and Displacement": {
                "Level 1 — 1D":                     generate_displacement_l1,
                "Level 2 — Two Displacements (2D)":  generate_displacement_l2,
                "Level 3 — Multiple Displacements (2D)": generate_displacement_l3,
            },
            "Vectors and Scalars": {
                "Identify Scalar or Vector":  gen_identify,
                "Scalar & Vector Pairs":      gen_pairs,
            },
            "Definitions": {
                "Term → Definition":          gen_term_to_definition,
                "Definition → Term":          gen_definition_to_term,
                "Which Statements Are Correct?": gen_statements,
            },
            "Speed and Velocity": {
                "From a Compound Displacement": gen_speed_velocity_from_displacement,
                "Resultant Velocity": generate_resultant_velocity,
            },
            "Velocity-Time Graphs": {
                "Describe Motion from a Graph": gen_describe_graph_stage,
                "Which Graph Matches?": gen_which_graph_matches,
                "Distance and Displacement": gen_distance_displacement,
                "Acceleration from an Interval": gen_acceleration_interval,
            },
        },
        "Electricity": {
            "Current":            generate_current,
            "Ohm's Law":          generate_ohms_law,
            "Resistors":          generate_resistors,
            "Electrical Power":   generate_power,
            "Potential Divider":  generate_potential_divider,
            "Circuits":           generate_circuits,
            "Charge Carriers": {
                "1 — Charge, Current and Time":      gen_ec_charge,
                "2 — Electrons and Sparks":           gen_ec_electrons,
                "3 — a.c., d.c. and Electric Fields": gen_ec_ac_dc,
            },
            "Potential Difference": {
                "1 — Energy and Charge (Ew = QV)":   gen_ec_ew_qv,
                "2 — Resistance from a V–I Gradient": gen_ec_gradient,
                "3 — What a Voltage Means":          gen_ec_voltage_meaning,
            },
            "Circuit Rules": {
                "1 — Series–Parallel Current":       gen_ec_series_parallel,
                "2 — Identical Loads in Parallel":   gen_ec_parallel_total_current,
                "3 — Explain Circuit Changes":       gen_ec_circuit_changes,
            },
            "LEDs and Transistor Switches": {
                "1 — LED Series Resistor":           gen_ec_led_resistor,
                "2 — Sensor Potential Dividers":     gen_ec_divider_switch,
                "3 — Explain a Transistor Switch":   gen_ec_transistor_explain,
            },
            "Power and Fuses": {
                "1 — Energy, Power and Time":        gen_ec_energy_time,
                "2 — Choosing a Fuse":               gen_ec_fuse,
                "3 — P = I²R and P = V²/R":          gen_ec_power_i2r,
                "4 — Power Statements":              gen_ec_toaster_statements,
            },
            "Definitions": electricity_n5_definitions,
        },
        "Radiation": {
            "Dose":      generate_dose,
            "Half-Life": generate_half_life,
            "Activity":  generate_activity,
            "Nuclear Radiation and Dosimetry": {
                "1 — Absorbed and Equivalent Dose":   gen_rd_dose,
                "2 — Radiation, Ionisation and Uses": gen_rd_nature,
            },
            "Half-Life, Fission and Fusion": {
                "1 — Activity and Half-Life":         gen_hl_activity,
                "2 — Power from Fission":             gen_hl_fission_power,
                "3 — Half-Life, Fission and Fusion Explained": gen_hl_explain,
            },
            "Definitions": radiation_n5_definitions,
        },
        "Waves": {
            "Wave Speed":        generate_wave_speed,
            "Period & Frequency": generate_period_frequency,
            "Waves Combined":    generate_waves_combined,
            "Wave Parameters and Behaviours": {
                "1 — Echoes":                         gen_wv_echo,
                "2 — Amplitude, Wavelength and Frequency": gen_wv_parameters,
                "3 — Describing Waves and Diffraction": gen_wv_behaviour,
            },
            "Electromagnetic Spectrum": {
                "1 — Calculations (v = fλ, d = vt)":  gen_em_calc,
                "2 — Bands, Detectors and Uses":      gen_em_bands,
            },
            "Refraction of Light": {
                "1 — Explaining Refraction":          gen_rf_explain,
                "2 — Wavelength in a Medium":         gen_rf_calc,
            },
            "Definitions":       waves_n5_definitions,
        },
        "Space": {
            "Space Exploration": {
                "1 — Weight on Other Planets":        gen_sp_weight,
                "2 — Rocket Launch (F = ma)":         gen_sp_rocket,
                "3 — Satellites and Space Travel":    gen_sp_explain,
            },
            "Cosmology": {
                "1 — Light-Years":                    gen_cs_lightyear,
                "2 — Light Travel Time":              gen_cs_light_time,
                "3 — Big Bang, Telescopes and Spectra": gen_cs_explain,
            },
            "Definitions": space_n5_definitions,
        },
        "Properties": {
            "Pressure": {
                "p = F/A":                        generate_pressure,
                "Weight and Total Contact Area":  gen_pm_pressure_weight,
            },
            "Gas Laws": {
                "Gas Law Calculations":           generate_gas_laws,
                "Kelvin and the Combined Gas Law": gen_pm_gas_kelvin,
                "Kinetic Model and Kelvin":       gen_pm_kinetic_model,
            },
            "Heat": {
                "Specific Heat Capacity": generate_heat_shc,
                "Specific Latent Heat":   generate_heat_latent,
                "Mixed":                  generate_heat,
                "Ice Machine (multi-step)": generate_heat_exam_icemachine,
                "Heating Then Boiling":   gen_pm_heat_then_boil,
                "Latent Heat with Power": gen_pm_latent_power,
                "Heating Curves and Heat Loss": gen_pm_heating_curve,
            },
            "Definitions": properties_n5_definitions,
        },
        "Skills": {
            "Scientific Prefixes": {
                "Name → Power of 10": gen_name_to_power,
                "Power of 10 → Name": gen_power_to_name,
                "Symbol → Name":      gen_symbol_to_name,
                "Name → Symbol":      gen_name_to_symbol,
            },
            "Definitions": skills_n5_definitions,
        },
    },
    "Higher": {
        "Our Dynamic Universe (Part 1)": {
            "Equations of Motion": {
                "Horizontal Motion": generate_equations_of_motion,
                "Vertical Motion":   generate_equations_of_motion_vertical,
            },
            "Graphs of Motion": {
                "Graph Matching":          generate_graphs_of_motion,
                "Velocity from a-t Graph": generate_at_graph_velocity,
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
                "Kinetic Energy Lost — Collisions": gen_ke_lost,
                "Explain — Reducing Injury":    gen_impulse_explain,
            },
            "Energy, Work and Power": {
                "Work Done":                   generate_work_done_higher,
                "Power":                        generate_power_higher,
                "Conservation — Ep and Ek":     gen_energy_ep_ek,
                "Conservation — Frictional Force": gen_energy_friction_force,
                "Conservation — Power":  gen_conservation_power,
            },
            "Effective Weight": {
                "Lifts":                         generate_effective_weight_lifts,
                "Beyond Lifts":                   generate_effective_weight_beyond_lifts,
                "Beyond Lifts — Explain Free Fall": gen_ew_explain_freefall,
            },
            "Definitions": odu_part1_definitions,
        },
        "Our Dynamic Universe (Part 2)": {
            "Projectile Motion": {
                "1 — Vertical Motion: Displacement and Height": generate_projectile_vertical_displacement,
                "2 — Vertical Motion: Time from Highest Point":  generate_projectile_vertical_time_from_top,
                "3 — Horizontal Motion":                         generate_projectile_horizontal,
                "4 — Exam Style (Mixed)":                        generate_projectile_exam_mixed,
                "5 — Explain":                                   generate_projectile_explain,
            },
            "Gravitation": {
                "1 — Force, Mass or Distance":              gen_grav_force_mass_distance,
                "2 — Units and Centre-to-Centre Distance":  gen_grav_units_centre_distance,
                "3 — g at a Height":                        gen_grav_field_at_height,
                "4 — How Does the Force Change?":           gen_grav_force_change,
            },
            "Special Relativity": {
                "Newtonian Relative Velocity": generate_relativity_velocity,
                "Time Dilation":               generate_relativity_time_dilation,
                "Length Contraction":          generate_relativity_length_contraction,
                "Definitions and Explain":     generate_relativity_definitions,
            },
            "The Expanding Universe": {
                "1 — Doppler Effect Calculations":           gen_eu_doppler,
                "2 — Explaining the Doppler Effect":         gen_eu_doppler_explain,
                "3 — Redshift and Recessional Velocity":     gen_eu_redshift,
                "4 — Hubble's Law and the Age of the Universe": gen_eu_hubble,
                "5 — Evidence, Dark Matter and Dark Energy": gen_eu_evidence,
                "6 — Stellar Temperature":                   gen_eu_stellar,
            },
            "Definitions": odu_part2_definitions,
        },
        "Particles and Waves": {
            "Forces on Charged Particles": {
                "1 — Speed After Acceleration (W = QV)": gen_pw_charged_speed,
                "2 — Fields and Accelerators":           gen_pw_accelerators,
            },
            "Standard Model": {
                "Particle Classification": generate_standard_model_classification,
                "Order of Magnitude":     generate_standard_model_order_of_magnitude,
                "Hadron Charges":         gen_pw_hadron_charge,
                "Forces, Bosons and Definitions": gen_pw_bosons,
            },
            "Nuclear Reactions": {
                "1 — Energy Released (E = mc²)":   gen_pw_mass_energy,
                "2 — Reactions per Second":        gen_pw_reactions_per_second,
            },
            "Inverse Square Law": {
                "1 — Irradiance at a New Distance": gen_pw_isl,
                "2 — Irradiance, I = P/A":          gen_pw_irradiance,
            },
            "The Photoelectric Effect": {
                "1 — Ek and Speed of Photoelectrons": gen_pw_photoelectric,
                "2 — Irradiance, Frequency and Definitions": gen_pw_pe_effects,
            },
            "Interference": {
                "1 — Path Difference":              gen_pw_path_difference,
                "2 — Diffraction Gratings":         gen_pw_grating,
            },
            "Spectra": {
                "1 — Energy Levels (E₂ − E₁ = hf)": gen_pw_energy_levels,
                "2 — Explaining Spectra":           gen_pw_spectra_explain,
            },
            "Refraction of Light": {
                "1 — Refractive Index, Speed and Critical Angle": gen_pw_refraction,
                "2 — Explaining Refraction":        gen_pw_refraction_explain,
            },
            "Definitions": particles_waves_definitions,
        },
        "Electricity": {
            "Monitoring and Measuring AC": {
                "1 — Peak and r.m.s. Values":       gen_he_peak_rms,
                "2 — Oscilloscope Traces":          gen_he_scope,
                "3 — Explaining AC":                gen_he_ac_explain,
            },
            "Current, Potential Difference, Power and Resistance": {
                "1 — Resistor Networks and Power":  gen_he_resistance_power,
                "2 — Potential Dividers":           gen_he_divider,
                "3 — Explaining Circuit Changes":   gen_he_circuit_explain,
            },
            "Electrical Sources and Internal Resistance": {
                "1 — E = V + Ir":                   gen_he_emf_calc,
                "2 — V–I Graphs":                   gen_he_emf_graph,
                "3 — e.m.f. and t.p.d. Explained":  gen_he_emf_explain,
            },
            "Capacitors": {
                "1 — Charge and Capacitance":       gen_he_cap_charge,
                "2 — Energy Stored":                gen_he_cap_energy,
                "3 — Charging and Discharging":     gen_he_cap_curves,
            },
            "Semiconductors and p-n Junctions": {
                "1 — LED Photons and Band Gaps":    gen_he_led_photon,
                "2 — Band Theory":                  gen_he_band_explain,
            },
            "Definitions": electricity_higher_definitions,
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
            "Definitions":            crash_odu_definitions,
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
            "Definitions": particles_waves_definitions,
        },
        "Electricity": {
            "Current":           generate_current,
            "Ohm's Law":         generate_ohms_law,
            "Resistors":         generate_resistors,
            "Electrical Power":  generate_power,
            "Potential Divider": generate_potential_divider,
            "Circuits":          generate_circuits,
            "Definitions":       electricity_higher_definitions,
        },
    },
}


# ── Exam Style ────────────────────────────────────────────────────────────────
# Each N5 and Higher unit has an "Exam Style" topic: multi-part questions in the
# style of SQA papers that cut across the unit's topics. Each part is tagged with
# the topic it tests. Unit assessments are drawn from these.

_EXAM_STYLE = {
    "National 5": {
        "Dynamics":    n5_dynamics.SCENARIOS,
        "Electricity": n5_electricity.SCENARIOS,
        "Radiation":   n5_radiation.SCENARIOS,
        "Waves":       n5_waves.SCENARIOS,
        "Space":       n5_space.SCENARIOS,
        "Properties":  n5_properties.SCENARIOS,
    },
    "Higher": {
        "Our Dynamic Universe (Part 1)": higher_odu.SCENARIOS_PART1,
        "Our Dynamic Universe (Part 2)": higher_odu.SCENARIOS_PART2,
        "Particles and Waves":           higher_particles_waves.SCENARIOS,
        "Electricity":                   higher_electricity.SCENARIOS,
    },
}

for _qualification, _units in _EXAM_STYLE.items():
    for _unit, _scenarios in _units.items():
        QUAL_REGISTRY[_qualification][_unit][EXAM_STYLE] = dict(_scenarios)

# ── Light-gate set-up diagrams ──────────────────────────────────────────────
# Any question whose own text mentions a light gate is shown with a diagram of the set-up
# (matched to its wording), whichever generator produced it.

def _with_light_gate_diagram(fn):
    @functools.wraps(fn)
    def generate(level="N5"):
        q = fn(level=level)
        if q.metadata.get("diagram"):
            return q
        text = q.question_text
        if q.is_scenario:
            text = " ".join([q.scenario_context] + [p.question_text for p in q.parts])
        svg = light_gate_diagram(text)
        if svg:
            with_diagram(q, svg)
            for part in q.parts:
                part.metadata["scenario_diagram"] = svg
        return q
    return generate


for _units in QUAL_REGISTRY.values():
    for _topics in _units.values():
        for _name, _entry in _topics.items():
            if isinstance(_entry, dict):
                _topics[_name] = {k: _with_light_gate_diagram(f) for k, f in _entry.items()}
            else:
                _topics[_name] = _with_light_gate_diagram(_entry)

EXAM_TEST_QUESTIONS = 4
UNIT_ASSESSMENT_MAX_QUESTIONS = 6


def get_topics(qualification):
    return list(QUAL_REGISTRY.get(qualification, {}).keys())


def get_question_types(qualification, topic):
    return list(QUAL_REGISTRY.get(qualification, {}).get(topic, {}).keys())


def get_sub_types(qualification, topic, question_type):
    entry = QUAL_REGISTRY.get(qualification, {}).get(topic, {}).get(question_type)
    if isinstance(entry, dict):
        return list(entry.keys())
    return None


_LEVEL_MAP = {"S3": "S3", "National 4": "N4", "National 5": "N5", "Higher": "Higher"}


def is_exam_style_test(qualification, topic, question_type):
    return question_type == EXAM_STYLE and EXAM_STYLE in QUAL_REGISTRY.get(qualification, {}).get(topic, {})


def test_length(qualification, topic, question_type):
    return EXAM_TEST_QUESTIONS if is_exam_style_test(qualification, topic, question_type) else 5


def make_test_generator(qualification, topic, question_type):
    """A generator for Test mode: deals every question style once (in random
    order) before any repeats, so a test covers the whole topic."""
    entry = QUAL_REGISTRY[qualification][topic][question_type]
    if not isinstance(entry, dict):
        return lambda: generate_question(qualification, topic, question_type)
    level = _LEVEL_MAP.get(qualification, "N5")
    deck = []

    def generate():
        if not deck:
            deck.extend(random.sample(list(entry.values()), len(entry)))
        return deck.pop()(level=level)

    return generate


def has_unit_assessment(qualification, unit):
    return EXAM_STYLE in QUAL_REGISTRY.get(qualification, {}).get(unit, {})


def build_unit_assessment(qualification, unit):
    """Exam-style questions from across the unit: scenarios are picked (in random order)
    to cover as many of the unit's topics as possible, up to UNIT_ASSESSMENT_MAX_QUESTIONS."""
    level = _LEVEL_MAP.get(qualification, "N5")
    candidates = [fn(level=level) for fn in QUAL_REGISTRY[qualification][unit][EXAM_STYLE].values()]
    random.shuffle(candidates)
    chosen, covered = [], set()
    while candidates and len(chosen) < UNIT_ASSESSMENT_MAX_QUESTIONS:
        best = max(candidates, key=lambda q: len(set(q.metadata["covers"]) - covered))
        if not set(best.metadata["covers"]) - covered and len(chosen) >= 3:
            break
        candidates.remove(best)
        chosen.append(best)
        covered |= set(best.metadata["covers"])
    return chosen


def generate_question(qualification, topic, question_type, sub_type=None):
    level = _LEVEL_MAP.get(qualification, "N5")
    entry = QUAL_REGISTRY[qualification][topic][question_type]
    if isinstance(entry, dict):
        fn = entry[sub_type] if sub_type in entry else random.choice(list(entry.values()))
    else:
        fn = entry
    q = fn(level=level)
    # Exam-style parts keep the topic each one tests, so attempts are reported against it.
    if sub_type and question_type != EXAM_STYLE:
        q.question_type = sub_type
        if q.is_scenario:
            for part in q.parts:
                if part.metadata.get("type") != "explain":
                    part.question_type = sub_type
    return q
