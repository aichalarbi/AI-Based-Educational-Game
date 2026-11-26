"""Adapter to the learning engine (P3). The backend contains no scoring logic itself."""

import logging

try:
    from learning_engine import InvalidOption, InvalidRubric, evaluate_answer

    USING_STUB = False
except ImportError:  # learning_engine not merged yet on this branch
    from ._learning_engine_stub import InvalidOption, InvalidRubric, evaluate_answer

    USING_STUB = True
    logging.getLogger(__name__).warning(
        "learning_engine.evaluate_answer not found – using backend STUB scorer"
    )

__all__ = ["InvalidOption", "InvalidRubric", "evaluate_answer", "USING_STUB"]
