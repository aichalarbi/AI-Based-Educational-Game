from collections.abc import Mapping
from typing import Literal, TypedDict


class LearningResult(TypedDict):
    is_correct: bool
    feedback_code: str
    next_action: Literal["continue", "review"]


class InvalidRubric(ValueError):
    """The approved rubric has missing or inconsistent fields."""


class InvalidOption(ValueError):
    """The selected option is not available for the question."""


def evaluate_answer(
    selected_option_id: str, rubric: Mapping[str, object]
) -> LearningResult:
    """Score one answer using a server-side multiple-choice rubric."""
    if not isinstance(rubric, Mapping):
        raise InvalidRubric("Rubric must be a mapping")

    option_ids = rubric.get("valid_option_ids")
    if not isinstance(option_ids, (list, tuple)) or not option_ids:
        raise InvalidRubric("valid_option_ids must contain at least one option ID")
    if any(not isinstance(option, str) or not option.strip() for option in option_ids):
        raise InvalidRubric("Each option ID must be a nonempty string")
    if len(set(option_ids)) != len(option_ids):
        raise InvalidRubric("Option IDs must be unique")

    correct_option = rubric.get("correct_option_id")
    if not isinstance(correct_option, str) or correct_option not in option_ids:
        raise InvalidRubric("correct_option_id must match one of the valid options")

    correct_feedback = rubric.get("correct_feedback_code")
    incorrect_feedback = rubric.get("incorrect_feedback_code")
    if not isinstance(correct_feedback, str) or not correct_feedback.strip():
        raise InvalidRubric("correct_feedback_code must be a nonempty string")
    if not isinstance(incorrect_feedback, str) or not incorrect_feedback.strip():
        raise InvalidRubric("incorrect_feedback_code must be a nonempty string")

    if not isinstance(selected_option_id, str) or selected_option_id not in option_ids:
        raise InvalidOption("Selected option ID is not available for this question")

    is_correct = selected_option_id == correct_option
    return {
        "is_correct": is_correct,
        "feedback_code": correct_feedback if is_correct else incorrect_feedback,
        "next_action": "continue" if is_correct else "review",
    }
