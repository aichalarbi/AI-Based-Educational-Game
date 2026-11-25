# Learning engine

## Multiple-choice scoring

Call the scorer with one selected option and a server-side rubric.

```python
from learning_engine import evaluate_answer

rubric = {
    "valid_option_ids": ["A", "B", "C"],
    "correct_option_id": "B",
    "correct_feedback_code": "CORRECT",
    "incorrect_feedback_code": "REVIEW_CONCEPT",
}

result = evaluate_answer("A", rubric)
# {"is_correct": False, "feedback_code": "REVIEW_CONCEPT", "next_action": "review"}
```

A valid wrong answer returns feedback for review. An unavailable option raises
`InvalidOption`, and a malformed rubric raises `InvalidRubric`.

Run the unit tests from the repository root:

```sh
python3 -B -m unittest discover -s tests -v
```

The example uses sample data. The final rubric format, reviewed content, and
backend integration are pending team confirmation.

## Future feature — Misconception map

After M1, use a graph to connect course concepts to recurring misconceptions and targeted follow-up questions. A valid wrong answer can provide evidence for a misconception. Repeated evidence across different questions can strengthen the signal. Exclude invalid submissions and broken rubrics from the learner's record.

Start with one misconception, two reviewed questions that can reveal it, and one follow-up. For example, choosing badges earned or play frequency as evidence of learning could point to confusion between engagement and learning. Ask the student to propose a task that shows whether a player can apply the concept.

Later, an AI-assisted short-answer evaluator could add evidence to the same map by identifying which rubric criteria the student met, what is missing, and which follow-up question addresses the gap.
