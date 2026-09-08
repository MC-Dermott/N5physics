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
#     "answer_images": ["<path>", ...],     # answer key (mcq) or marking
#                                            # instructions (extended)
#   }
#
# Image paths are relative to core/data/past_paper_assets/.

PAST_PAPERS = {
}


def get_past_paper_entries(topic, question_type):
    return PAST_PAPERS.get((topic, question_type), [])


def has_past_papers(topic, question_type):
    return bool(PAST_PAPERS.get((topic, question_type)))
