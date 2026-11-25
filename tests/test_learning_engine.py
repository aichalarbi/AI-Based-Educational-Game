import unittest

from learning_engine import InvalidOption, InvalidRubric, evaluate_answer


class EvaluateAnswerTests(unittest.TestCase):
    def setUp(self):
        self.rubric = {
            "valid_option_ids": ["A", "B", "C"],
            "correct_option_id": "B",
            "correct_feedback_code": "CORRECT",
            "incorrect_feedback_code": "REVIEW_CONCEPT",
        }

    def test_correct_answer(self):
        self.assertEqual(
            evaluate_answer("B", self.rubric),
            {
                "is_correct": True,
                "feedback_code": "CORRECT",
                "next_action": "continue",
            },
        )

    def test_incorrect_answer(self):
        self.assertEqual(
            evaluate_answer("A", self.rubric),
            {
                "is_correct": False,
                "feedback_code": "REVIEW_CONCEPT",
                "next_action": "review",
            },
        )

    def test_unknown_option(self):
        with self.assertRaises(InvalidOption):
            evaluate_answer("Z", self.rubric)

    def test_invalid_answer_key(self):
        self.rubric["correct_option_id"] = "D"
        with self.assertRaises(InvalidRubric):
            evaluate_answer("A", self.rubric)

    def test_missing_feedback_code(self):
        del self.rubric["incorrect_feedback_code"]
        with self.assertRaises(InvalidRubric):
            evaluate_answer("B", self.rubric)

    def test_rubric_is_not_a_mapping(self):
        for rubric in (None, []):
            with self.subTest(rubric=rubric):
                with self.assertRaises(InvalidRubric):
                    evaluate_answer("B", rubric)

    def test_duplicate_option_ids(self):
        self.rubric["valid_option_ids"] = ["A", "B", "B"]
        with self.assertRaises(InvalidRubric):
            evaluate_answer("B", self.rubric)

    def test_blank_option_id(self):
        self.rubric["valid_option_ids"] = ["A", "B", "   "]
        with self.assertRaises(InvalidRubric):
            evaluate_answer("B", self.rubric)
