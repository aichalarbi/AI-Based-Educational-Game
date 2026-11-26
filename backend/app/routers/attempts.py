import logging
from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Attempt, Challenge
from ..schemas import AttemptIn, AttemptOut
from ..services.evaluation import InvalidOption, InvalidRubric, evaluate_answer

router = APIRouter(prefix="/attempts", tags=["attempts"])
logger = logging.getLogger(__name__)


def to_attempt_out(attempt: Attempt) -> AttemptOut:
    messages = attempt.challenge.feedback_messages or {}
    created_at = attempt.created_at
    if created_at.tzinfo is None:  # SQLite drops the timezone; values are stored as UTC
        created_at = created_at.replace(tzinfo=timezone.utc)
    return AttemptOut(
        id=attempt.id,
        challenge_id=attempt.challenge_id,
        player_id=attempt.player_id,
        selected_option_id=attempt.selected_option_id,
        is_correct=attempt.is_correct,
        feedback_code=attempt.feedback_code,
        feedback_message=messages.get(attempt.feedback_code, ""),
        next_action=attempt.next_action,
        created_at=created_at,
    )


@router.post("", response_model=AttemptOut, status_code=201)
def create_attempt(body: AttemptIn, db: Session = Depends(get_db)) -> AttemptOut:
    challenge = db.get(Challenge, body.challenge_id)
    if challenge is None:
        raise HTTPException(status_code=404, detail=f"Challenge '{body.challenge_id}' not found")

    try:
        result = evaluate_answer(body.selected_option_id, challenge.rubric)
    except InvalidOption:
        raise HTTPException(
            status_code=422,
            detail=f"Option '{body.selected_option_id}' is not available for this challenge",
        )
    except InvalidRubric:
        logger.exception("Broken rubric for challenge %s", challenge.id)
        raise HTTPException(status_code=500, detail="Challenge content is misconfigured")

    attempt = Attempt(
        challenge=challenge,
        player_id=body.player_id,
        selected_option_id=body.selected_option_id,
        is_correct=result["is_correct"],
        feedback_code=result["feedback_code"],
        next_action=result["next_action"],
    )
    db.add(attempt)
    db.commit()
    return to_attempt_out(attempt)
