# Real SQA Higher Physics past-paper questions, shown in "Past Paper Questions"
# mode. Sourced from the "Higher Physics Past Papers" compilation (Mr Davie /
# Mr White), covering 2015-2025.
#
# Key:   (topic, question_type)  — matches the strings in question_factory.py
#        (topic is the Unit, e.g. "Our Dynamic Universe"; question_type is
#        what the app's "Topic" dropdown shows, e.g. "Special Relativity")
# Value: list of entries, each:
#   {
#     "year": "2015",            # or "SPQ" for the specimen paper
#     "paper": "P1" | "P2",      # P1 = multiple choice, P2 = extended response
#     "qnum": "7",                # question label as printed in the paper
#     "kind": "mcq" | "extended",
#     "question_images": ["<path>", ...],   # PNG(s) of the question, in order
#     "answer_images": ["<path>", ...],     # marking instructions (extended
#                                            # response questions only)
#     "answer_text": "C",                   # correct option letter, from the
#                                            # paper's own answer key (mcq only)
#   }
#
# Image paths are relative to core/data/past_paper_assets/.

import re


def _mcq(dir_, year, paper, qnum, page, answer):
    return {"year": year, "paper": paper, "qnum": qnum, "kind": "mcq",
            "question_images": [f"{dir_}/{page}.png"], "answer_text": answer}


def _extended(dir_, year, paper, qnum, pages, answer_pages):
    return {"year": year, "paper": paper, "qnum": qnum, "kind": "extended",
            "question_images": [f"{dir_}/{p}.png" for p in pages],
            "answer_images": [f"{dir_}/{p}.png" for p in answer_pages]}


_SPECIAL_RELATIVITY_DIR = "special_relativity"

_SPECIAL_RELATIVITY = [
    _mcq(_SPECIAL_RELATIVITY_DIR, "2015", "P1", "7", "2015_P1_q7", "C"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2017", "P1", "4", "2017_P1_q4", "B"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2018", "P1", "6", "2018_P1_q6", "C"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2018", "P1", "7", "2018_P1_q7", "D"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "SPQ", "P1", "9", "SPQ_P1_q9", "C"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2019", "P1", "8", "2019_P1_q8", "C"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2020", "P1", "9", "2020_P1_q9", "C"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2020", "P1", "10", "2020_P1_q10", "B"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2022", "P1", "7", "2022_P1_q7", "C"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2023", "P1", "7", "2023_P1_q7", "D"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2024", "P1", "7", "2024_P1_q7", "D"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2024", "P1", "8", "2024_P1_q8", "C"),
    _mcq(_SPECIAL_RELATIVITY_DIR, "2025", "P1", "8", "2025_P1_q8", "B"),

    _extended(_SPECIAL_RELATIVITY_DIR, "2016", "P2", "4",
              ["2016_P2_q4_1", "2016_P2_q4_2"], ["2016_P2_q4_answer"]),
    _extended(_SPECIAL_RELATIVITY_DIR, "2017", "P2", "7",
              ["2017_P2_q7_1", "2017_P2_q7_2"], ["2017_P2_q7_answer"]),
    _extended(_SPECIAL_RELATIVITY_DIR, "SPQ", "P2", "4",
              ["SPQ_P2_q4_1", "SPQ_P2_q4_2"], ["SPQ_P2_q4_answer"]),
    _extended(_SPECIAL_RELATIVITY_DIR, "2019", "P2", "7",
              ["2019_P2_q7_1", "2019_P2_q7_2", "2019_P2_q7_3"], ["2019_P2_q7_answer"]),
    _extended(_SPECIAL_RELATIVITY_DIR, "2020", "P2", "7",
              ["2020_P2_q7_1", "2020_P2_q7_2", "2020_P2_q7_3"], ["2020_P2_q7_answer"]),
    _extended(_SPECIAL_RELATIVITY_DIR, "2023", "P2", "4",
              ["2023_P2_q4_1", "2023_P2_q4_2"], ["2023_P2_q4_answer"]),
    _extended(_SPECIAL_RELATIVITY_DIR, "2025", "P2", "4",
              ["2025_P2_q4_1", "2025_P2_q4_2"], ["2025_P2_q4_answer"]),
]

_GRAVITATION_DIR = "gravitation"

_GRAVITATION = [
    _mcq(_GRAVITATION_DIR, "2016", "P1", "5", "2016_P1_q5", "C"),
    _mcq(_GRAVITATION_DIR, "2018", "P1", "5", "2018_P1_q5", "A"),
    _mcq(_GRAVITATION_DIR, "SPQ", "P1", "8", "SPQ_P1_q8", "B"),
    _mcq(_GRAVITATION_DIR, "2020", "P1", "8", "2020_P1_q8", "D"),
    _mcq(_GRAVITATION_DIR, "2023", "P1", "6", "2023_P1_q6", "A"),
    _mcq(_GRAVITATION_DIR, "2025", "P1", "25", "2025_P1_q25", "C"),

    _extended(_GRAVITATION_DIR, "2015", "P2", "3",
              ["2015_P2_q3"], ["2015_P2_q3_answer"]),
    _extended(_GRAVITATION_DIR, "2017", "P2", "5",
              ["2017_P2_q5_1", "2017_P2_q5_2"], ["2017_P2_q5_answer"]),
    _extended(_GRAVITATION_DIR, "2019", "P2", "4",
              ["2019_P2_q4_1", "2019_P2_q4_2"], ["2019_P2_q4_answer"]),
    _extended(_GRAVITATION_DIR, "2022", "P2", "5",
              ["2022_P2_q5_1", "2022_P2_q5_2", "2022_P2_q5_3", "2022_P2_q5_4"],
              ["2022_P2_q5_answer"]),
    _extended(_GRAVITATION_DIR, "2024", "P2", "4",
              ["2024_P2_q4_1", "2024_P2_q4_2", "2024_P2_q4_3"], ["2024_P2_q4_answer"]),
    _extended(_GRAVITATION_DIR, "2025", "P2", "5",
              ["2025_P2_q5_1", "2025_P2_q5_2", "2025_P2_q5_3", "2025_P2_q5_4"],
              ["2025_P2_q5_answer_1", "2025_P2_q5_answer_2"]),
]

_STANDARD_MODEL_DIR = "standard_model"

_STANDARD_MODEL = [
    _mcq(_STANDARD_MODEL_DIR, "2016", "P1", "8", "2016_P1_q8", "A"),
    _mcq(_STANDARD_MODEL_DIR, "2018", "P1", "8", "2018_P1_q8", "B"),
    _mcq(_STANDARD_MODEL_DIR, "2018", "P1", "9", "2018_P1_q9", "E"),
    _mcq(_STANDARD_MODEL_DIR, "SPQ", "P1", "14", "SPQ_P1_q14", "E"),
    _mcq(_STANDARD_MODEL_DIR, "2020", "P1", "14", "2020_P1_q14", "D"),
    _mcq(_STANDARD_MODEL_DIR, "2020", "P1", "15", "2020_P1_q15", "E"),
    _mcq(_STANDARD_MODEL_DIR, "2022", "P1", "11", "2022_P1_q11", "B"),
    _mcq(_STANDARD_MODEL_DIR, "2023", "P1", "11", "2023_P1_q11", "C"),
    _mcq(_STANDARD_MODEL_DIR, "2024", "P1", "10", "2024_P1_q10", "E"),

    _extended(_STANDARD_MODEL_DIR, "2015", "P2", "6",
              ["2015_P2_q6"], ["2015_P2_q6_answer"]),
    _extended(_STANDARD_MODEL_DIR, "2017", "P2", "7",
              ["2017_P2_q7_1", "2017_P2_q7_2"], ["2017_P2_q7_answer"]),
    _extended(_STANDARD_MODEL_DIR, "SPQ", "P2", "7",
              ["SPQ_P2_q7_1", "SPQ_P2_q7_2"], ["SPQ_P2_q7_answer"]),
    _extended(_STANDARD_MODEL_DIR, "2025", "P2", "6",
              ["2025_P2_q6_1", "2025_P2_q6_2", "2025_P2_q6_3", "2025_P2_q6_4"],
              ["2025_P2_q6_answer_1", "2025_P2_q6_answer_2"]),
]

_MOMENTUM_IMPULSE_DIR = "momentum_impulse"

_MOMENTUM_IMPULSE = [
    _mcq(_MOMENTUM_IMPULSE_DIR, "2016", "P1", "4", "2016_P1_q4", "C"),
    _mcq(_MOMENTUM_IMPULSE_DIR, "2019", "P1", "6", "2019_P1_q6", "E"),
    _mcq(_MOMENTUM_IMPULSE_DIR, "SPQ", "P1", "5", "SPQ_P1_q5", "C"),
    _mcq(_MOMENTUM_IMPULSE_DIR, "SPQ", "P1", "6", "SPQ_P1_q6", "C"),
    _mcq(_MOMENTUM_IMPULSE_DIR, "2023", "P1", "3", "2023_P1_q3", "B"),
    _mcq(_MOMENTUM_IMPULSE_DIR, "2025", "P1", "7", "2025_P1_q7", "B"),

    _extended(_MOMENTUM_IMPULSE_DIR, "2016", "P2", "3",
              ["2016_P2_q3_1", "2016_P2_q3_2"], ["2016_P2_q3_answer"]),
    _extended(_MOMENTUM_IMPULSE_DIR, "2017", "P2", "2",
              ["2017_P2_q2_1", "2017_P2_q2_2"], ["2017_P2_q2_answer"]),
    _extended(_MOMENTUM_IMPULSE_DIR, "2018", "P2", "3",
              ["2018_P2_q3_1", "2018_P2_q3_2", "2018_P2_q3_3"], ["2018_P2_q3_answer"]),
    _extended(_MOMENTUM_IMPULSE_DIR, "SPQ", "P2", "3",
              ["SPQ_P2_q3_1", "SPQ_P2_q3_2"], ["SPQ_P2_q3_answer"]),
    _extended(_MOMENTUM_IMPULSE_DIR, "2019", "P2", "1",
              ["2019_P2_q1_1", "2019_P2_q1_2", "2019_P2_q1_3", "2019_P2_q1_4"],
              ["2019_P2_q1_answer_1", "2019_P2_q1_answer_2", "2019_P2_q1_answer_3"]),
    _extended(_MOMENTUM_IMPULSE_DIR, "2020", "P2", "3",
              ["2020_P2_q3_1", "2020_P2_q3_2"], ["2020_P2_q3_answer"]),
    _extended(_MOMENTUM_IMPULSE_DIR, "2022", "P2", "3",
              ["2022_P2_q3_1", "2022_P2_q3_2"],
              ["2022_P2_q3_answer_1", "2022_P2_q3_answer_2"]),
    _extended(_MOMENTUM_IMPULSE_DIR, "2023", "P2", "3",
              ["2023_P2_q3_1", "2023_P2_q3_2", "2023_P2_q3_3"], ["2023_P2_q3_answer"]),
    _extended(_MOMENTUM_IMPULSE_DIR, "2025", "P2", "2",
              ["2025_P2_q2_1", "2025_P2_q2_2"], ["2025_P2_q2_answer"]),
]

_EQUATIONS_OF_MOTION_DIR = "equations_of_motion"

_EQUATIONS_OF_MOTION = [
    _mcq(_EQUATIONS_OF_MOTION_DIR, "2015", "P1", "2", "2015_P1_q2", "B"),
    _mcq(_EQUATIONS_OF_MOTION_DIR, "2016", "P1", "1", "2016_P1_q1", "B"),
    _mcq(_EQUATIONS_OF_MOTION_DIR, "2018", "P1", "1", "2018_P1_q1", "C"),
    _mcq(_EQUATIONS_OF_MOTION_DIR, "2020", "P1", "1", "2020_P1_q1", "B"),
    _mcq(_EQUATIONS_OF_MOTION_DIR, "2022", "P1", "2", "2022_P1_q2", "A"),
    _mcq(_EQUATIONS_OF_MOTION_DIR, "2024", "P1", "1", "2024_P1_q1", "B"),
    _mcq(_EQUATIONS_OF_MOTION_DIR, "2025", "P1", "1", "2025_P1_q1", "C"),

    _extended(_EQUATIONS_OF_MOTION_DIR, "2017", "P2", "1",
              ["2017_P2_q1"], ["2017_P2_q1_answer"]),
    _extended(_EQUATIONS_OF_MOTION_DIR, "2022", "P2", "2",
              ["2022_P2_q2_1", "2022_P2_q2_2"], ["2022_P2_q2_answer"]),
    _extended(_EQUATIONS_OF_MOTION_DIR, "2023", "P2", "1",
              ["2023_P2_q1_1", "2023_P2_q1_2"], ["2023_P2_q1_answer"]),
    _extended(_EQUATIONS_OF_MOTION_DIR, "2025", "P2", "1",
              ["2025_P2_q1_1", "2025_P2_q1_2"], ["2025_P2_q1_answer"]),
]

_GRAPHS_OF_MOTION_DIR = "graphs_of_motion"

_GRAPHS_OF_MOTION = [
    _mcq(_GRAPHS_OF_MOTION_DIR, "2015", "P1", "1", "2015_P1_q1", "C"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2016", "P1", "2", "2016_P1_q2", "A"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2017", "P1", "1", "2017_P1_q1", "A"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2018", "P1", "2", "2018_P1_q2", "D"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2019", "P1", "1", "2019_P1_q1", "E"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2019", "P1", "4", "2019_P1_q4", "A"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2020", "P1", "2", "2020_P1_q2", "E"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2020", "P1", "3", "2020_P1_q3", "A"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2022", "P1", "1", "2022_P1_q1", "A"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2023", "P1", "1", "2023_P1_q1", "A"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2024", "P1", "2", "2024_P1_q2", "A"),
    _mcq(_GRAPHS_OF_MOTION_DIR, "2025", "P1", "2", "2025_P1_q2", "A"),

    _extended(_GRAPHS_OF_MOTION_DIR, "2017", "P2", "3",
              ["2017_P2_q3_1", "2017_P2_q3_2"],
              ["2017_P2_q3_answer_1", "2017_P2_q3_answer_2"]),
    _extended(_GRAPHS_OF_MOTION_DIR, "SPQ", "P2", "1",
              ["SPQ_P2_q1_1", "SPQ_P2_q1_2", "SPQ_P2_q1_3"], ["SPQ_P2_q1_answer"]),
    _extended(_GRAPHS_OF_MOTION_DIR, "2019", "P2", "1",
              ["2019_P2_q1_1", "2019_P2_q1_2", "2019_P2_q1_3", "2019_P2_q1_4"],
              ["2019_P2_q1_answer_1", "2019_P2_q1_answer_2", "2019_P2_q1_answer_3"]),
]

_TOWING_DIR = "towing"

_TOWING = [
    _mcq(_TOWING_DIR, "2015", "P1", "5", "2015_P1_q5", "C"),
    _mcq(_TOWING_DIR, "2018", "P1", "3", "2018_P1_q3", "A"),
    _mcq(_TOWING_DIR, "2019", "P1", "5", "2019_P1_q5", "B"),
    _mcq(_TOWING_DIR, "2022", "P1", "4", "2022_P1_q4", "E"),

    _extended(_TOWING_DIR, "2020", "P2", "2",
              ["2020_P2_q2"], ["2020_P2_q2_answer"]),
    _extended(_TOWING_DIR, "2023", "P2", "2",
              ["2023_P2_q2_1", "2023_P2_q2_2"], ["2023_P2_q2_answer"]),
    _extended(_TOWING_DIR, "2024", "P2", "2",
              ["2024_P2_q2_1", "2024_P2_q2_2", "2024_P2_q2_3"], ["2024_P2_q2_answer"]),
]

_EFFECTIVE_WEIGHT_DIR = "effective_weight"

_EFFECTIVE_WEIGHT = [
    _mcq(_EFFECTIVE_WEIGHT_DIR, "2015", "P1", "4", "2015_P1_q4", "D"),
    _mcq(_EFFECTIVE_WEIGHT_DIR, "2018", "P1", "4", "2018_P1_q4", "B"),
    _mcq(_EFFECTIVE_WEIGHT_DIR, "2022", "P1", "5", "2022_P1_q5", "D"),
]

_ENERGY_WORK_POWER_DIR = "energy_work_power"

_ENERGY_WORK_POWER = [
    _mcq(_ENERGY_WORK_POWER_DIR, "2015", "P1", "6", "2015_P1_q6", "B"),
    _mcq(_ENERGY_WORK_POWER_DIR, "2022", "P1", "6", "2022_P1_q6", "B"),
    _mcq(_ENERGY_WORK_POWER_DIR, "2024", "P1", "5", "2024_P1_q5", "C"),

    _extended(_ENERGY_WORK_POWER_DIR, "2016", "P2", "2",
              ["2016_P2_q2_1", "2016_P2_q2_2"],
              ["2016_P2_q2_answer_1", "2016_P2_q2_answer_2"]),
]

_COMPONENTS_OF_VECTORS_DIR = "components_of_vectors"

_COMPONENTS_OF_VECTORS = [
    _mcq(_COMPONENTS_OF_VECTORS_DIR, "2015", "P1", "3", "2015_P1_q3", "A"),
    _mcq(_COMPONENTS_OF_VECTORS_DIR, "2017", "P1", "2", "2017_P1_q2", "B"),
    _mcq(_COMPONENTS_OF_VECTORS_DIR, "2022", "P1", "3", "2022_P1_q3", "B"),
    _mcq(_COMPONENTS_OF_VECTORS_DIR, "2025", "P1", "4", "2025_P1_q4", "D"),

    _extended(_COMPONENTS_OF_VECTORS_DIR, "2019", "P2", "2",
              ["2019_P2_q2_1", "2019_P2_q2_2"], ["2019_P2_q2_answer"]),
]

_PROJECTILE_MOTION_DIR = "projectile_motion"

_PROJECTILE_MOTION = [
    _mcq(_PROJECTILE_MOTION_DIR, "2024", "P1", "4", "2024_P1_q4", "A"),

    _extended(_PROJECTILE_MOTION_DIR, "2015", "P2", "1",
              ["2015_P2_q1_1", "2015_P2_q1_2", "2015_P2_q1_3"],
              ["2015_P2_q1_answer_1", "2015_P2_q1_answer_2"]),
    _extended(_PROJECTILE_MOTION_DIR, "2020", "P2", "1",
              ["2020_P2_q1_1", "2020_P2_q1_2"], ["2020_P2_q1_answer"]),
]


_N5_DYNAMICS_DIR = "n5_dynamics"
_N5_ELECTRICITY_DIR = "n5_electricity"
_N5_RADIATION_DIR = "n5_radiation"
_N5_WAVES_DIR = "n5_waves"
_N5_PROPERTIES_DIR = "n5_properties"

# ── National 5 past papers ──────────────────────────────────────────────────
# Sourced from the "National 5 Physics Past Papers" compilation (Mr Davie /
# Mr White), covering 2014-2025 (2020/2021 omitted: SQA cancelled those exam
# diets). MCQ (Section 1) only.

_N5_DYNAMICS_ACCELERATION = [
    _mcq(_N5_DYNAMICS_DIR, "2014", "P1", "15", "2014_P1_q15", "E"),
    _mcq(_N5_DYNAMICS_DIR, "2015", "P1", "14", "2015_P1_q14", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2016", "P1", "16", "2016_P1_q16", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2017", "P1", "16", "2017_P1_q16", "E"),
    _mcq(_N5_DYNAMICS_DIR, "SPQ", "P1", "2", "SPQ_P1_q2", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2019", "P1", "3", "2019_P1_q3", "B"),
    _mcq(_N5_DYNAMICS_DIR, "2022", "P1", "2", "2022_P1_q2", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2023", "P1", "2", "2023_P1_q2", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2024", "P1", "2", "2024_P1_q2", "B"),
    _mcq(_N5_DYNAMICS_DIR, "2025", "P1", "3", "2025_P1_q3", "D"),
]

_N5_DYNAMICS_ENERGY = [
    _mcq(_N5_DYNAMICS_DIR, "2014", "P1", "16", "2014_P1_q16", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2017", "P1", "1", "2017_P1_q1", "A"),
    _mcq(_N5_DYNAMICS_DIR, "SPQ", "P1", "5", "SPQ_P1_q5", "C"),
    _mcq(_N5_DYNAMICS_DIR, "SPQ", "P1", "6", "SPQ_P1_q6", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2018", "P1", "4", "2018_P1_q4", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2022", "P1", "5", "2022_P1_q5", "B"),
    _mcq(_N5_DYNAMICS_DIR, "2022", "P1", "18", "2022_P1_q18", "E"),
    _mcq(_N5_DYNAMICS_DIR, "2023", "P1", "5", "2023_P1_q5", "B"),
    _mcq(_N5_DYNAMICS_DIR, "2025", "P1", "5", "2025_P1_q5", "E"),
]

_N5_DYNAMICS_FORCES = [
    _mcq(_N5_DYNAMICS_DIR, "2015", "P1", "16", "2015_P1_q16", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2015", "P1", "17", "2015_P1_q17", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2015", "P1", "18", "2015_P1_q18", "B"),
    _mcq(_N5_DYNAMICS_DIR, "2016", "P1", "15", "2016_P1_q15", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2017", "P1", "14", "2017_P1_q14", "C"),
    _mcq(_N5_DYNAMICS_DIR, "SPQ", "P1", "3", "SPQ_P1_q3", "B"),
    _mcq(_N5_DYNAMICS_DIR, "SPQ", "P1", "4", "SPQ_P1_q4", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2019", "P1", "4", "2019_P1_q4", "B"),
    _mcq(_N5_DYNAMICS_DIR, "2023", "P1", "4", "2023_P1_q4", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2025", "P1", "4", "2025_P1_q4", "A"),
]

_N5_DYNAMICS_PROJECTILE_MOTION = [
    _mcq(_N5_DYNAMICS_DIR, "2014", "P1", "4", "2014_P1_q4", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2014", "P1", "17", "2014_P1_q17", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2014", "P1", "19", "2014_P1_q19", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2016", "P1", "18", "2016_P1_q18", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2018", "P1", "3", "2018_P1_q3", "E"),
    _mcq(_N5_DYNAMICS_DIR, "2019", "P1", "5", "2019_P1_q5", "D"),
]

_N5_DYNAMICS_SPACE_EXPLORATION = [
    _mcq(_N5_DYNAMICS_DIR, "2014", "P1", "18", "2014_P1_q18", "E"),
    _mcq(_N5_DYNAMICS_DIR, "2015", "P1", "19", "2015_P1_q19", "E"),
    _mcq(_N5_DYNAMICS_DIR, "2016", "P1", "17", "2016_P1_q17", "E"),
    _mcq(_N5_DYNAMICS_DIR, "2016", "P1", "20", "2016_P1_q20", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2017", "P1", "15", "2017_P1_q15", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2017", "P1", "17", "2017_P1_q17", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2017", "P1", "18", "2017_P1_q18", "B"),
    _mcq(_N5_DYNAMICS_DIR, "SPQ", "P1", "7", "SPQ_P1_q7", "D"),
    _mcq(_N5_DYNAMICS_DIR, "SPQ", "P1", "8", "SPQ_P1_q8", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2018", "P1", "5", "2018_P1_q5", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2018", "P1", "6", "2018_P1_q6", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2018", "P1", "7", "2018_P1_q7", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2018", "P1", "8", "2018_P1_q8", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2018", "P1", "9", "2018_P1_q9", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2019", "P1", "2", "2019_P1_q2", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2019", "P1", "6", "2019_P1_q6", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2019", "P1", "7", "2019_P1_q7", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2019", "P1", "8", "2019_P1_q8", "B"),
    _mcq(_N5_DYNAMICS_DIR, "2022", "P1", "6", "2022_P1_q6", "B"),
    _mcq(_N5_DYNAMICS_DIR, "2022", "P1", "7", "2022_P1_q7", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2022", "P1", "8", "2022_P1_q8", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2022", "P1", "9", "2022_P1_q9", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2022", "P1", "10", "2022_P1_q10", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2023", "P1", "6", "2023_P1_q6", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2023", "P1", "7", "2023_P1_q7", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2023", "P1", "8", "2023_P1_q8", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2024", "P1", "3", "2024_P1_q3", "E"),
    _mcq(_N5_DYNAMICS_DIR, "2024", "P1", "5", "2024_P1_q5", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2024", "P1", "7", "2024_P1_q7", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2024", "P1", "8", "2024_P1_q8", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2024", "P1", "18", "2024_P1_q18", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2025", "P1", "7", "2025_P1_q7", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2025", "P1", "8", "2025_P1_q8", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2025", "P1", "9", "2025_P1_q9", "E"),
]

_N5_DYNAMICS_VECTORS_AND_SCALARS = [
    _mcq(_N5_DYNAMICS_DIR, "2014", "P1", "14", "2014_P1_q14", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2016", "P1", "14", "2016_P1_q14", "E"),
    _mcq(_N5_DYNAMICS_DIR, "SPQ", "P1", "1", "SPQ_P1_q1", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2018", "P1", "1", "2018_P1_q1", "E"),
    _mcq(_N5_DYNAMICS_DIR, "2018", "P1", "2", "2018_P1_q2", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2019", "P1", "1", "2019_P1_q1", "A"),
    _mcq(_N5_DYNAMICS_DIR, "2022", "P1", "1", "2022_P1_q1", "E"),
    _mcq(_N5_DYNAMICS_DIR, "2023", "P1", "1", "2023_P1_q1", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2024", "P1", "1", "2024_P1_q1", "E"),
    _mcq(_N5_DYNAMICS_DIR, "2025", "P1", "1", "2025_P1_q1", "B"),
]

_N5_DYNAMICS_VELOCITY_TIME_GRAPHS = [
    _mcq(_N5_DYNAMICS_DIR, "2015", "P1", "15", "2015_P1_q15", "B"),
    _mcq(_N5_DYNAMICS_DIR, "2022", "P1", "3", "2022_P1_q3", "D"),
    _mcq(_N5_DYNAMICS_DIR, "2023", "P1", "3", "2023_P1_q3", "C"),
    _mcq(_N5_DYNAMICS_DIR, "2025", "P1", "2", "2025_P1_q2", "A"),
]

_N5_ELECTRICITY_CIRCUITS = [
    _mcq(_N5_ELECTRICITY_DIR, "2014", "P1", "2", "2014_P1_q2", "D"),
    _mcq(_N5_ELECTRICITY_DIR, "2014", "P1", "3", "2014_P1_q3", "B"),
    _mcq(_N5_ELECTRICITY_DIR, "2015", "P1", "1", "2015_P1_q1", "A"),
    _mcq(_N5_ELECTRICITY_DIR, "2015", "P1", "2", "2015_P1_q2", "A"),
    _mcq(_N5_ELECTRICITY_DIR, "2016", "P1", "3", "2016_P1_q3", "D"),
    _mcq(_N5_ELECTRICITY_DIR, "2017", "P1", "2", "2017_P1_q2", "D"),
    _mcq(_N5_ELECTRICITY_DIR, "2017", "P1", "3", "2017_P1_q3", "A"),
    _mcq(_N5_ELECTRICITY_DIR, "2017", "P1", "4", "2017_P1_q4", "E"),
    _mcq(_N5_ELECTRICITY_DIR, "SPQ", "P1", "12", "SPQ_P1_q12", "D"),
    _mcq(_N5_ELECTRICITY_DIR, "2018", "P1", "11", "2018_P1_q11", "E"),
    _mcq(_N5_ELECTRICITY_DIR, "2019", "P1", "11", "2019_P1_q11", "D"),
    _mcq(_N5_ELECTRICITY_DIR, "2019", "P1", "13", "2019_P1_q13", "A"),
    _mcq(_N5_ELECTRICITY_DIR, "2022", "P1", "12", "2022_P1_q12", "D"),
    _mcq(_N5_ELECTRICITY_DIR, "2023", "P1", "10", "2023_P1_q10", "C"),
    _mcq(_N5_ELECTRICITY_DIR, "2023", "P1", "11", "2023_P1_q11", "D"),
    _mcq(_N5_ELECTRICITY_DIR, "2023", "P1", "12", "2023_P1_q12", "A"),
    _mcq(_N5_ELECTRICITY_DIR, "2024", "P1", "11", "2024_P1_q11", "E"),
    _mcq(_N5_ELECTRICITY_DIR, "2025", "P1", "11", "2025_P1_q11", "E"),
    _mcq(_N5_ELECTRICITY_DIR, "2025", "P1", "13", "2025_P1_q13", "D"),
]

_N5_ELECTRICITY_CURRENT = [
    _mcq(_N5_ELECTRICITY_DIR, "2016", "P1", "2", "2016_P1_q2", "A"),
    _mcq(_N5_ELECTRICITY_DIR, "SPQ", "P1", "9", "SPQ_P1_q9", "B"),
    _mcq(_N5_ELECTRICITY_DIR, "SPQ", "P1", "10", "SPQ_P1_q10", "A"),
    _mcq(_N5_ELECTRICITY_DIR, "2018", "P1", "12", "2018_P1_q12", "D"),
    _mcq(_N5_ELECTRICITY_DIR, "2023", "P1", "9", "2023_P1_q9", "E"),
    _mcq(_N5_ELECTRICITY_DIR, "2024", "P1", "9", "2024_P1_q9", "A"),
    _mcq(_N5_ELECTRICITY_DIR, "2025", "P1", "12", "2025_P1_q12", "A"),
]

_N5_ELECTRICITY_ELECTRICAL_POWER = [
    _mcq(_N5_ELECTRICITY_DIR, "2014", "P1", "1", "2014_P1_q1", "D"),
    _mcq(_N5_ELECTRICITY_DIR, "2018", "P1", "15", "2018_P1_q15", "B"),
    _mcq(_N5_ELECTRICITY_DIR, "2019", "P1", "10", "2019_P1_q10", "E"),
    _mcq(_N5_ELECTRICITY_DIR, "2022", "P1", "11", "2022_P1_q11", "C"),
    _mcq(_N5_ELECTRICITY_DIR, "2023", "P1", "14", "2023_P1_q14", "E"),
    _mcq(_N5_ELECTRICITY_DIR, "2023", "P1", "15", "2023_P1_q15", "C"),
    _mcq(_N5_ELECTRICITY_DIR, "2024", "P1", "4", "2024_P1_q4", "B"),
    _mcq(_N5_ELECTRICITY_DIR, "2024", "P1", "10", "2024_P1_q10", "B"),
    _mcq(_N5_ELECTRICITY_DIR, "2024", "P1", "14", "2024_P1_q14", "C"),
    _mcq(_N5_ELECTRICITY_DIR, "2025", "P1", "15", "2025_P1_q15", "A"),
    _mcq(_N5_ELECTRICITY_DIR, "2025", "P1", "16", "2025_P1_q16", "B"),
]

_N5_ELECTRICITY_OHMS_LAW = [
    _mcq(_N5_ELECTRICITY_DIR, "2015", "P1", "4", "2015_P1_q4", "E"),
    _mcq(_N5_ELECTRICITY_DIR, "SPQ", "P1", "11", "SPQ_P1_q11", "C"),
]

_N5_ELECTRICITY_POTENTIAL_DIVIDER = [
    _mcq(_N5_ELECTRICITY_DIR, "2016", "P1", "1", "2016_P1_q1", "C"),
    _mcq(_N5_ELECTRICITY_DIR, "2018", "P1", "13", "2018_P1_q13", "A"),
    _mcq(_N5_ELECTRICITY_DIR, "2022", "P1", "14", "2022_P1_q14", "B"),
    _mcq(_N5_ELECTRICITY_DIR, "2023", "P1", "13", "2023_P1_q13", "C"),
    _mcq(_N5_ELECTRICITY_DIR, "2024", "P1", "12", "2024_P1_q12", "A"),
]

_N5_ELECTRICITY_RESISTORS = [
    _mcq(_N5_ELECTRICITY_DIR, "2015", "P1", "3", "2015_P1_q3", "C"),
    _mcq(_N5_ELECTRICITY_DIR, "2016", "P1", "4", "2016_P1_q4", "C"),
    _mcq(_N5_ELECTRICITY_DIR, "SPQ", "P1", "14", "SPQ_P1_q14", "C"),
    _mcq(_N5_ELECTRICITY_DIR, "2018", "P1", "14", "2018_P1_q14", "C"),
    _mcq(_N5_ELECTRICITY_DIR, "2019", "P1", "12", "2019_P1_q12", "E"),
    _mcq(_N5_ELECTRICITY_DIR, "2022", "P1", "13", "2022_P1_q13", "E"),
    _mcq(_N5_ELECTRICITY_DIR, "2024", "P1", "13", "2024_P1_q13", "B"),
    _mcq(_N5_ELECTRICITY_DIR, "2025", "P1", "14", "2025_P1_q14", "D"),
]

_N5_PROPERTIES_GAS_LAWS = [
    _mcq(_N5_PROPERTIES_DIR, "2014", "P1", "5", "2014_P1_q5", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2014", "P1", "6", "2014_P1_q6", "A"),
    _mcq(_N5_PROPERTIES_DIR, "2015", "P1", "5", "2015_P1_q5", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2015", "P1", "6", "2015_P1_q6", "D"),
    _mcq(_N5_PROPERTIES_DIR, "2016", "P1", "7", "2016_P1_q7", "A"),
    _mcq(_N5_PROPERTIES_DIR, "SPQ", "P1", "16", "SPQ_P1_q16", "C"),
    _mcq(_N5_PROPERTIES_DIR, "2018", "P1", "17", "2018_P1_q17", "C"),
    _mcq(_N5_PROPERTIES_DIR, "2018", "P1", "19", "2018_P1_q19", "E"),
    _mcq(_N5_PROPERTIES_DIR, "2019", "P1", "17", "2019_P1_q17", "E"),
    _mcq(_N5_PROPERTIES_DIR, "2022", "P1", "4", "2022_P1_q4", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2023", "P1", "19", "2023_P1_q19", "A"),
    _mcq(_N5_PROPERTIES_DIR, "2023", "P1", "20", "2023_P1_q20", "C"),
    _mcq(_N5_PROPERTIES_DIR, "2025", "P1", "20", "2025_P1_q20", "D"),
]

_N5_PROPERTIES_HEAT = [
    _mcq(_N5_PROPERTIES_DIR, "2014", "P1", "7", "2014_P1_q7", "A"),
    _mcq(_N5_PROPERTIES_DIR, "2014", "P1", "20", "2014_P1_q20", "D"),
    _mcq(_N5_PROPERTIES_DIR, "2016", "P1", "19", "2016_P1_q19", "D"),
    _mcq(_N5_PROPERTIES_DIR, "2017", "P1", "5", "2017_P1_q5", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2017", "P1", "7", "2017_P1_q7", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2017", "P1", "19", "2017_P1_q19", "B"),
    _mcq(_N5_PROPERTIES_DIR, "SPQ", "P1", "13", "SPQ_P1_q13", "B"),
    _mcq(_N5_PROPERTIES_DIR, "SPQ", "P1", "15", "SPQ_P1_q15", "B"),
    _mcq(_N5_PROPERTIES_DIR, "SPQ", "P1", "17", "SPQ_P1_q17", "A"),
    _mcq(_N5_PROPERTIES_DIR, "2018", "P1", "16", "2018_P1_q16", "C"),
    _mcq(_N5_PROPERTIES_DIR, "2018", "P1", "18", "2018_P1_q18", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2019", "P1", "14", "2019_P1_q14", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2019", "P1", "15", "2019_P1_q15", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2019", "P1", "18", "2019_P1_q18", "A"),
    _mcq(_N5_PROPERTIES_DIR, "2022", "P1", "15", "2022_P1_q15", "D"),
    _mcq(_N5_PROPERTIES_DIR, "2022", "P1", "16", "2022_P1_q16", "D"),
    _mcq(_N5_PROPERTIES_DIR, "2023", "P1", "16", "2023_P1_q16", "C"),
    _mcq(_N5_PROPERTIES_DIR, "2023", "P1", "17", "2023_P1_q17", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2024", "P1", "15", "2024_P1_q15", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2024", "P1", "16", "2024_P1_q16", "D"),
    _mcq(_N5_PROPERTIES_DIR, "2025", "P1", "6", "2025_P1_q6", "D"),
    _mcq(_N5_PROPERTIES_DIR, "2025", "P1", "17", "2025_P1_q17", "C"),
    _mcq(_N5_PROPERTIES_DIR, "2025", "P1", "18", "2025_P1_q18", "C"),
]

_N5_PROPERTIES_PRESSURE = [
    _mcq(_N5_PROPERTIES_DIR, "2016", "P1", "5", "2016_P1_q5", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2016", "P1", "6", "2016_P1_q6", "C"),
    _mcq(_N5_PROPERTIES_DIR, "2017", "P1", "6", "2017_P1_q6", "D"),
    _mcq(_N5_PROPERTIES_DIR, "2019", "P1", "16", "2019_P1_q16", "D"),
    _mcq(_N5_PROPERTIES_DIR, "2022", "P1", "17", "2022_P1_q17", "E"),
    _mcq(_N5_PROPERTIES_DIR, "2023", "P1", "18", "2023_P1_q18", "B"),
    _mcq(_N5_PROPERTIES_DIR, "2024", "P1", "17", "2024_P1_q17", "D"),
    _mcq(_N5_PROPERTIES_DIR, "2025", "P1", "19", "2025_P1_q19", "D"),
]

_N5_RADIATION_ACTIVITY = [
    _mcq(_N5_RADIATION_DIR, "2015", "P1", "12", "2015_P1_q12", "A"),
    _mcq(_N5_RADIATION_DIR, "SPQ", "P1", "23", "SPQ_P1_q23", "E"),
    _mcq(_N5_RADIATION_DIR, "2019", "P1", "24", "2019_P1_q24", "D"),
    _mcq(_N5_RADIATION_DIR, "2022", "P1", "23", "2022_P1_q23", "A"),
    _mcq(_N5_RADIATION_DIR, "2023", "P1", "24", "2023_P1_q24", "E"),
    _mcq(_N5_RADIATION_DIR, "2024", "P1", "23", "2024_P1_q23", "E"),
    _mcq(_N5_RADIATION_DIR, "2025", "P1", "23", "2025_P1_q23", "E"),
]

_N5_RADIATION_DOSE = [
    _mcq(_N5_RADIATION_DIR, "2014", "P1", "11", "2014_P1_q11", "E"),
    _mcq(_N5_RADIATION_DIR, "2015", "P1", "10", "2015_P1_q10", "E"),
    _mcq(_N5_RADIATION_DIR, "2015", "P1", "11", "2015_P1_q11", "E"),
    _mcq(_N5_RADIATION_DIR, "2017", "P1", "13", "2017_P1_q13", "B"),
    _mcq(_N5_RADIATION_DIR, "SPQ", "P1", "24", "SPQ_P1_q24", "B"),
    _mcq(_N5_RADIATION_DIR, "2018", "P1", "23", "2018_P1_q23", "A"),
    _mcq(_N5_RADIATION_DIR, "2019", "P1", "25", "2019_P1_q25", "A"),
    _mcq(_N5_RADIATION_DIR, "2024", "P1", "24", "2024_P1_q24", "C"),
    _mcq(_N5_RADIATION_DIR, "2025", "P1", "24", "2025_P1_q24", "A"),
]

_N5_RADIATION_HALF_LIFE = [
    _mcq(_N5_RADIATION_DIR, "2014", "P1", "12", "2014_P1_q12", "A"),
    _mcq(_N5_RADIATION_DIR, "2018", "P1", "24", "2018_P1_q24", "B"),
    _mcq(_N5_RADIATION_DIR, "2022", "P1", "24", "2022_P1_q24", "D"),
    _mcq(_N5_RADIATION_DIR, "2022", "P1", "25", "2022_P1_q25", "C"),
    _mcq(_N5_RADIATION_DIR, "2024", "P1", "25", "2024_P1_q25", "B"),
]

_N5_RADIATION_NUCLEAR_RADIATION = [
    _mcq(_N5_RADIATION_DIR, "2014", "P1", "10", "2014_P1_q10", "B"),
    _mcq(_N5_RADIATION_DIR, "2014", "P1", "13", "2014_P1_q13", "E"),
    _mcq(_N5_RADIATION_DIR, "2015", "P1", "9", "2015_P1_q9", "C"),
    _mcq(_N5_RADIATION_DIR, "2015", "P1", "13", "2015_P1_q13", "E"),
    _mcq(_N5_RADIATION_DIR, "2016", "P1", "12", "2016_P1_q12", "B"),
    _mcq(_N5_RADIATION_DIR, "2016", "P1", "13", "2016_P1_q13", "B"),
    _mcq(_N5_RADIATION_DIR, "SPQ", "P1", "22", "SPQ_P1_q22", "A"),
    _mcq(_N5_RADIATION_DIR, "SPQ", "P1", "25", "SPQ_P1_q25", "E"),
    _mcq(_N5_RADIATION_DIR, "2018", "P1", "25", "2018_P1_q25", "B"),
    _mcq(_N5_RADIATION_DIR, "2019", "P1", "22", "2019_P1_q22", "D"),
    _mcq(_N5_RADIATION_DIR, "2019", "P1", "23", "2019_P1_q23", "A"),
    _mcq(_N5_RADIATION_DIR, "2022", "P1", "22", "2022_P1_q22", "E"),
    _mcq(_N5_RADIATION_DIR, "2023", "P1", "25", "2023_P1_q25", "B"),
    _mcq(_N5_RADIATION_DIR, "2024", "P1", "22", "2024_P1_q22", "B"),
    _mcq(_N5_RADIATION_DIR, "2025", "P1", "25", "2025_P1_q25", "B"),
]

_N5_WAVES_ELECTROMAGNETIC_SPECTRUM = [
    _mcq(_N5_WAVES_DIR, "2014", "P1", "9", "2014_P1_q9", "B"),
    _mcq(_N5_WAVES_DIR, "2015", "P1", "8", "2015_P1_q8", "A"),
    _mcq(_N5_WAVES_DIR, "2017", "P1", "10", "2017_P1_q10", "C"),
    _mcq(_N5_WAVES_DIR, "2017", "P1", "11", "2017_P1_q11", "B"),
    _mcq(_N5_WAVES_DIR, "SPQ", "P1", "20", "SPQ_P1_q20", "A"),
    _mcq(_N5_WAVES_DIR, "2018", "P1", "20", "2018_P1_q20", "B"),
    _mcq(_N5_WAVES_DIR, "2018", "P1", "21", "2018_P1_q21", "A"),
    _mcq(_N5_WAVES_DIR, "2022", "P1", "19", "2022_P1_q19", "A"),
    _mcq(_N5_WAVES_DIR, "2022", "P1", "20", "2022_P1_q20", "D"),
    _mcq(_N5_WAVES_DIR, "2022", "P1", "21", "2022_P1_q21", "C"),
    _mcq(_N5_WAVES_DIR, "2024", "P1", "20", "2024_P1_q20", "C"),
    _mcq(_N5_WAVES_DIR, "2025", "P1", "22", "2025_P1_q22", "B"),
]

_N5_WAVES_PERIOD_AND_FREQUENCY = [
    _mcq(_N5_WAVES_DIR, "2014", "P1", "8", "2014_P1_q8", "C"),
    _mcq(_N5_WAVES_DIR, "2016", "P1", "8", "2016_P1_q8", "A"),
    _mcq(_N5_WAVES_DIR, "2016", "P1", "10", "2016_P1_q10", "C"),
    _mcq(_N5_WAVES_DIR, "2017", "P1", "9", "2017_P1_q9", "C"),
    _mcq(_N5_WAVES_DIR, "SPQ", "P1", "18", "SPQ_P1_q18", "B"),
    _mcq(_N5_WAVES_DIR, "SPQ", "P1", "19", "SPQ_P1_q19", "A"),
    _mcq(_N5_WAVES_DIR, "2018", "P1", "22", "2018_P1_q22", "C"),
    _mcq(_N5_WAVES_DIR, "2019", "P1", "19", "2019_P1_q19", "A"),
    _mcq(_N5_WAVES_DIR, "2023", "P1", "21", "2023_P1_q21", "B"),
    _mcq(_N5_WAVES_DIR, "2024", "P1", "19", "2024_P1_q19", "C"),
    _mcq(_N5_WAVES_DIR, "2025", "P1", "21", "2025_P1_q21", "B"),
]

_N5_WAVES_REFRACTION_OF_LIGHT = [
    _mcq(_N5_WAVES_DIR, "2016", "P1", "11", "2016_P1_q11", "A"),
    _mcq(_N5_WAVES_DIR, "2017", "P1", "12", "2017_P1_q12", "A"),
    _mcq(_N5_WAVES_DIR, "SPQ", "P1", "21", "SPQ_P1_q21", "E"),
    _mcq(_N5_WAVES_DIR, "2019", "P1", "20", "2019_P1_q20", "C"),
    _mcq(_N5_WAVES_DIR, "2019", "P1", "21", "2019_P1_q21", "C"),
    _mcq(_N5_WAVES_DIR, "2023", "P1", "22", "2023_P1_q22", "E"),
    _mcq(_N5_WAVES_DIR, "2023", "P1", "23", "2023_P1_q23", "A"),
    _mcq(_N5_WAVES_DIR, "2024", "P1", "21", "2024_P1_q21", "A"),
]

_N5_WAVES_WAVE_SPEED = [
    _mcq(_N5_WAVES_DIR, "2024", "P1", "6", "2024_P1_q6", "D"),
]

_N5_WAVES_WAVES_COMBINED = [
    _mcq(_N5_WAVES_DIR, "2015", "P1", "7", "2015_P1_q7", "D"),
    _mcq(_N5_WAVES_DIR, "2015", "P1", "20", "2015_P1_q20", "D"),
    _mcq(_N5_WAVES_DIR, "2016", "P1", "9", "2016_P1_q9", "E"),
    _mcq(_N5_WAVES_DIR, "2017", "P1", "8", "2017_P1_q8", "E"),
    _mcq(_N5_WAVES_DIR, "2017", "P1", "20", "2017_P1_q20", "D"),
    _mcq(_N5_WAVES_DIR, "2018", "P1", "10", "2018_P1_q10", "C"),
    _mcq(_N5_WAVES_DIR, "2019", "P1", "9", "2019_P1_q9", "C"),
    _mcq(_N5_WAVES_DIR, "2025", "P1", "10", "2025_P1_q10", "C"),
]

N5_PAST_PAPERS_ENTRIES = {
    ("Dynamics", "Acceleration"): _N5_DYNAMICS_ACCELERATION,
    ("Dynamics", "Energy"): _N5_DYNAMICS_ENERGY,
    ("Dynamics", "Forces"): _N5_DYNAMICS_FORCES,
    ("Dynamics", "Projectile Motion"): _N5_DYNAMICS_PROJECTILE_MOTION,
    ("Dynamics", "Space Exploration"): _N5_DYNAMICS_SPACE_EXPLORATION,
    ("Dynamics", "Vectors and Scalars"): _N5_DYNAMICS_VECTORS_AND_SCALARS,
    ("Dynamics", "Velocity-Time Graphs"): _N5_DYNAMICS_VELOCITY_TIME_GRAPHS,
    ("Electricity", "Circuits"): _N5_ELECTRICITY_CIRCUITS,
    ("Electricity", "Current"): _N5_ELECTRICITY_CURRENT,
    ("Electricity", "Electrical Power"): _N5_ELECTRICITY_ELECTRICAL_POWER,
    ("Electricity", "Ohm's Law"): _N5_ELECTRICITY_OHMS_LAW,
    ("Electricity", "Potential Divider"): _N5_ELECTRICITY_POTENTIAL_DIVIDER,
    ("Electricity", "Resistors"): _N5_ELECTRICITY_RESISTORS,
    ("Properties", "Gas Laws"): _N5_PROPERTIES_GAS_LAWS,
    ("Properties", "Heat"): _N5_PROPERTIES_HEAT,
    ("Properties", "Pressure"): _N5_PROPERTIES_PRESSURE,
    ("Radiation", "Activity"): _N5_RADIATION_ACTIVITY,
    ("Radiation", "Dose"): _N5_RADIATION_DOSE,
    ("Radiation", "Half-Life"): _N5_RADIATION_HALF_LIFE,
    ("Radiation", "Nuclear Radiation"): _N5_RADIATION_NUCLEAR_RADIATION,
    ("Waves", "Electromagnetic Spectrum"): _N5_WAVES_ELECTROMAGNETIC_SPECTRUM,
    ("Waves", "Period & Frequency"): _N5_WAVES_PERIOD_AND_FREQUENCY,
    ("Waves", "Refraction of Light"): _N5_WAVES_REFRACTION_OF_LIGHT,
    ("Waves", "Wave Speed"): _N5_WAVES_WAVE_SPEED,
    ("Waves", "Waves Combined"): _N5_WAVES_WAVES_COMBINED,
}


PAST_PAPERS = {
    ("Our Dynamic Universe", "Special Relativity"): _SPECIAL_RELATIVITY,
    ("Our Dynamic Universe", "Gravitation"): _GRAVITATION,
    ("Particles and Waves", "Standard Model"): _STANDARD_MODEL,
    ("Our Dynamic Universe", "Momentum and Impulse"): _MOMENTUM_IMPULSE,
    ("Our Dynamic Universe", "Energy, Work and Power"): _ENERGY_WORK_POWER,
    ("Our Dynamic Universe", "Equations of Motion"): _EQUATIONS_OF_MOTION,
    ("Our Dynamic Universe", "Graphs of Motion"): _GRAPHS_OF_MOTION,
    ("Our Dynamic Universe", "Towing"): _TOWING,
    ("Our Dynamic Universe", "Effective Weight"): _EFFECTIVE_WEIGHT,
    ("Our Dynamic Universe", "Components of Vectors"): _COMPONENTS_OF_VECTORS,
    ("Our Dynamic Universe", "Projectile Motion"): _PROJECTILE_MOTION,
    **N5_PAST_PAPERS_ENTRIES,
}


def get_past_paper_entries(topic, question_type):
    return PAST_PAPERS.get((canonical_unit(topic), question_type), [])


def has_past_papers(topic, question_type):
    return bool(get_past_paper_entries(topic, question_type))


# ── Unit-level MCQ quiz ─────────────────────────────────────────────────────
# Pools every past-paper MCQ across all topics within a unit, for the "Past
# Paper Quiz" mode. Scoped per qualification (rather than trusting unit names
# to be unique) since e.g. "Electricity" is a unit in both National 5 and
# Higher.

PAST_PAPER_UNITS = {
    "Higher": ["Our Dynamic Universe", "Particles and Waves"],
    "National 5": ["Dynamics", "Electricity", "Radiation", "Waves", "Properties"],
}


def get_past_paper_units(qualification):
    """Units with a (possibly empty, for now) past-paper quiz for this qualification."""
    return PAST_PAPER_UNITS.get(qualification, [])


def canonical_unit(unit):
    """Strip an app-UI " (Part N)" suffix (e.g. Higher's pacing split of "Our
    Dynamic Universe") — the quiz always pools/tracks against the whole real unit."""
    return re.sub(r"\s*\(Part\s*\d+\)\s*$", "", unit or "").strip()


def get_unit_mcqs(qualification, unit):
    """All past-paper MCQ entries across every topic in `unit`, each tagged with
    its own topic/question_type so results can still be tracked per sub-topic."""
    canonical = canonical_unit(unit)
    if canonical not in PAST_PAPER_UNITS.get(qualification, []):
        return []
    mcqs = []
    for (topic, question_type), entries in PAST_PAPERS.items():
        if topic != canonical:
            continue
        for e in entries:
            if e["kind"] == "mcq":
                mcqs.append({**e, "topic": topic, "question_type": question_type})
    return mcqs
