from dataclasses import dataclass, field
from typing import Any
import random


@dataclass
class PhysicsQuestion:
    question_text: str
    correct_answer: Any
    unit: str
    topic: str
    question_type: str
    level: str                          # "N4", "N5", "Higher"
    qid: int = field(default_factory=lambda: random.randint(10000, 99999))
    distractors: list = field(default_factory=list)
    # Each distractor: {"value": float, "mistake": str, "working": [...]}
    working: list = field(default_factory=list)
    # Each working step: {"type": "text"|"latex", "content": str}
    scaffold: list = field(default_factory=list)
    # Each scaffold step: {"prompt": str, "answer": float}
    notes: str = ""
    is_scenario: bool = False
    scenario_context: str = ""          # shared preamble shown above all parts
    parts: list = field(default_factory=list)   # list[PhysicsQuestion] for scenarios
    metadata: dict = field(default_factory=dict)
