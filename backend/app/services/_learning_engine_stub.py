"""STUB – placeholder for learning_engine.evaluate_answer().

!!! Not the real learning engine. Owned by P3 (branch feature/p3-learning-engine). !!!
Only used while `learning_engine` on the current branch has no evaluate_answer()
(e.g. before P3's work is merged into main). Mirrors P3's signature and result shape
so the backend works unchanged once the real engine is available. Delete after merge.
"""

from collections.abc import Mapping


class InvalidRubric(ValueError):
    pass


class InvalidOption(ValueError):
    pass


def evaluate_answer(selected_option_id: str, rubric: Mapping) -> dict:
    option_ids = rubric.get("valid_option_ids") or []
    correct = rubric.get("correct_option_id")
    if correct not in option_ids:
        raise InvalidRubric("correct_option_id must match one of the valid options")
    if selected_option_id not in option_ids:
        raise InvalidOption("Selected option ID is not available for this question")
    is_correct = selected_option_id == correct
    return {
        "is_correct": is_correct,
        "feedback_code": rubric["correct_feedback_code" if is_correct else "incorrect_feedback_code"],
        "next_action": "continue" if is_correct else "review",
    }
