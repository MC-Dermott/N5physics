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
}


def get_past_paper_entries(topic, question_type):
    return PAST_PAPERS.get((topic, question_type), [])


def has_past_papers(topic, question_type):
    return bool(PAST_PAPERS.get((topic, question_type)))
