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

_TOPIC = ("Our Dynamic Universe", "Special Relativity")
_DIR = "special_relativity"

PAST_PAPERS = {
    _TOPIC: [
        {"year": "2015", "paper": "P1", "qnum": "7", "kind": "mcq",
         "question_images": [f"{_DIR}/2015_P1_q7.png"], "answer_text": "C"},
        {"year": "2017", "paper": "P1", "qnum": "4", "kind": "mcq",
         "question_images": [f"{_DIR}/2017_P1_q4.png"], "answer_text": "B"},
        {"year": "2018", "paper": "P1", "qnum": "6", "kind": "mcq",
         "question_images": [f"{_DIR}/2018_P1_q6.png"], "answer_text": "C"},
        {"year": "2018", "paper": "P1", "qnum": "7", "kind": "mcq",
         "question_images": [f"{_DIR}/2018_P1_q7.png"], "answer_text": "D"},
        {"year": "SPQ", "paper": "P1", "qnum": "9", "kind": "mcq",
         "question_images": [f"{_DIR}/SPQ_P1_q9.png"], "answer_text": "C"},
        {"year": "2019", "paper": "P1", "qnum": "8", "kind": "mcq",
         "question_images": [f"{_DIR}/2019_P1_q8.png"], "answer_text": "C"},
        {"year": "2020", "paper": "P1", "qnum": "9", "kind": "mcq",
         "question_images": [f"{_DIR}/2020_P1_q9.png"], "answer_text": "C"},
        {"year": "2020", "paper": "P1", "qnum": "10", "kind": "mcq",
         "question_images": [f"{_DIR}/2020_P1_q10.png"], "answer_text": "B"},
        {"year": "2022", "paper": "P1", "qnum": "7", "kind": "mcq",
         "question_images": [f"{_DIR}/2022_P1_q7.png"], "answer_text": "C"},
        {"year": "2023", "paper": "P1", "qnum": "7", "kind": "mcq",
         "question_images": [f"{_DIR}/2023_P1_q7.png"], "answer_text": "D"},
        {"year": "2024", "paper": "P1", "qnum": "7", "kind": "mcq",
         "question_images": [f"{_DIR}/2024_P1_q7.png"], "answer_text": "D"},
        {"year": "2024", "paper": "P1", "qnum": "8", "kind": "mcq",
         "question_images": [f"{_DIR}/2024_P1_q8.png"], "answer_text": "C"},
        {"year": "2025", "paper": "P1", "qnum": "8", "kind": "mcq",
         "question_images": [f"{_DIR}/2025_P1_q8.png"], "answer_text": "B"},

        {"year": "2016", "paper": "P2", "qnum": "4", "kind": "extended",
         "question_images": [f"{_DIR}/2016_P2_q4_1.png", f"{_DIR}/2016_P2_q4_2.png"],
         "answer_images": [f"{_DIR}/2016_P2_q4_answer.png"]},
        {"year": "2017", "paper": "P2", "qnum": "7", "kind": "extended",
         "question_images": [f"{_DIR}/2017_P2_q7_1.png", f"{_DIR}/2017_P2_q7_2.png"],
         "answer_images": [f"{_DIR}/2017_P2_q7_answer.png"]},
        {"year": "SPQ", "paper": "P2", "qnum": "4", "kind": "extended",
         "question_images": [f"{_DIR}/SPQ_P2_q4_1.png", f"{_DIR}/SPQ_P2_q4_2.png"],
         "answer_images": [f"{_DIR}/SPQ_P2_q4_answer.png"]},
        {"year": "2019", "paper": "P2", "qnum": "7", "kind": "extended",
         "question_images": [f"{_DIR}/2019_P2_q7_1.png", f"{_DIR}/2019_P2_q7_2.png", f"{_DIR}/2019_P2_q7_3.png"],
         "answer_images": [f"{_DIR}/2019_P2_q7_answer.png"]},
        {"year": "2020", "paper": "P2", "qnum": "7", "kind": "extended",
         "question_images": [f"{_DIR}/2020_P2_q7_1.png", f"{_DIR}/2020_P2_q7_2.png", f"{_DIR}/2020_P2_q7_3.png"],
         "answer_images": [f"{_DIR}/2020_P2_q7_answer.png"]},
        {"year": "2023", "paper": "P2", "qnum": "4", "kind": "extended",
         "question_images": [f"{_DIR}/2023_P2_q4_1.png", f"{_DIR}/2023_P2_q4_2.png"],
         "answer_images": [f"{_DIR}/2023_P2_q4_answer.png"]},
        {"year": "2025", "paper": "P2", "qnum": "4", "kind": "extended",
         "question_images": [f"{_DIR}/2025_P2_q4_1.png", f"{_DIR}/2025_P2_q4_2.png"],
         "answer_images": [f"{_DIR}/2025_P2_q4_answer.png"]},
    ],
}


def get_past_paper_entries(topic, question_type):
    return PAST_PAPERS.get((topic, question_type), [])


def has_past_papers(topic, question_type):
    return bool(PAST_PAPERS.get((topic, question_type)))
