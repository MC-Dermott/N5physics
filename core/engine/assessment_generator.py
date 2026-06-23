import random

from topics.electricity_and_energy.electrical_power import generate_electrical_power
from topics.electricity_and_energy.efficiency import generate_efficiency
from topics.electricity_and_energy.knowledge import (
    generate_renewable_energy,
    generate_input_output_devices,
    generate_electromagnets,
)
from topics.electricity.current import generate_current
from topics.electricity.ohms_law import generate_ohms_law

from topics.waves.wave_speed import generate_wave_speed
from topics.radiation.dose import generate_dose
from topics.radiation.half_life import generate_half_life
from topics.radiation.activity import generate_activity

from topics.dynamics.speed_distance_time import generate_sdt
from topics.dynamics.weight import generate_weight
from topics.dynamics.acceleration import generate_acceleration
from topics.properties.pressure import generate_pressure

TOTAL_MARKS = 20
PASS_MARK = 10

# Each entry in a recipe: (generator_fn, topic_label)
_RECIPES = {
    "Electricity and Energy": [
        (generate_renewable_energy,     "Renewable Energy"),
        (generate_renewable_energy,     "Renewable Energy"),
        (generate_renewable_energy,     "Renewable Energy"),
        (generate_electrical_power,     "Electrical Power"),
        (generate_electrical_power,     "Electrical Power"),
        (generate_electrical_power,     "Electrical Power"),
        (generate_electrical_power,     "Electrical Power"),
        (generate_efficiency,           "Efficiency"),
        (generate_efficiency,           "Efficiency"),
        (generate_efficiency,           "Efficiency"),
        (generate_electromagnets,       "Electromagnets"),
        (generate_electromagnets,       "Electromagnets"),
        (generate_current,              "Current"),
        (generate_current,              "Current"),
        (generate_current,              "Current"),
        (generate_ohms_law,             "Ohm's Law"),
        (generate_ohms_law,             "Ohm's Law"),
        (generate_ohms_law,             "Ohm's Law"),
        (generate_input_output_devices, "Input/Output Devices"),
        (generate_input_output_devices, "Input/Output Devices"),
    ],
    "Waves and Radiation": [
        (generate_wave_speed, "Wave Speed"),
        (generate_wave_speed, "Wave Speed"),
        (generate_wave_speed, "Wave Speed"),
        (generate_wave_speed, "Wave Speed"),
        (generate_wave_speed, "Wave Speed"),
        (generate_wave_speed, "Wave Speed"),
        (generate_wave_speed, "Wave Speed"),
        (generate_wave_speed, "Wave Speed"),
        (generate_half_life,  "Half-Life"),
        (generate_half_life,  "Half-Life"),
        (generate_half_life,  "Half-Life"),
        (generate_half_life,  "Half-Life"),
        (generate_half_life,  "Half-Life"),
        (generate_half_life,  "Half-Life"),
        (generate_activity,   "Activity"),
        (generate_activity,   "Activity"),
        (generate_activity,   "Activity"),
        (generate_activity,   "Activity"),
        (generate_dose,       "Dose"),
        (generate_dose,       "Dose"),
    ],
    "Dynamics and Space": [
        (generate_sdt,          "Speed, Distance & Time"),
        (generate_sdt,          "Speed, Distance & Time"),
        (generate_sdt,          "Speed, Distance & Time"),
        (generate_sdt,          "Speed, Distance & Time"),
        (generate_sdt,          "Speed, Distance & Time"),
        (generate_sdt,          "Speed, Distance & Time"),
        (generate_sdt,          "Speed, Distance & Time"),
        (generate_weight,       "Weight"),
        (generate_weight,       "Weight"),
        (generate_weight,       "Weight"),
        (generate_weight,       "Weight"),
        (generate_weight,       "Weight"),
        (generate_acceleration, "Acceleration"),
        (generate_acceleration, "Acceleration"),
        (generate_acceleration, "Acceleration"),
        (generate_acceleration, "Acceleration"),
        (generate_acceleration, "Acceleration"),
        (generate_pressure,     "Pressure"),
        (generate_pressure,     "Pressure"),
        (generate_pressure,     "Pressure"),
    ],
}


def generate_assessment(unit):
    recipe = list(_RECIPES.get(unit, []))
    random.shuffle(recipe)
    questions = []
    for gen_fn, _label in recipe:
        q = gen_fn(level="N4")
        questions.append(q)
    return questions
