"""Import missions/challenges from a content JSON file into the database (upsert by id)."""

import json
from pathlib import Path
from typing import Tuple

from sqlalchemy.orm import Session

from ..models import Challenge, Mission
from ..schemas import ChallengeIn, ContentFile


class ContentError(ValueError):
    pass


def build_rubric(challenge: ChallengeIn) -> dict:
    """Translate the authored rubric into the format expected by learning_engine."""
    option_ids = [option.id for option in challenge.options]
    if len(set(option_ids)) != len(option_ids):
        raise ContentError(f"Challenge {challenge.id}: option ids must be unique")
    if challenge.rubric.correct_option_id not in option_ids:
        raise ContentError(f"Challenge {challenge.id}: correctOptionId is not one of the options")
    return {
        "valid_option_ids": option_ids,
        "correct_option_id": challenge.rubric.correct_option_id,
        "correct_feedback_code": challenge.rubric.correct_feedback_code,
        "incorrect_feedback_code": challenge.rubric.incorrect_feedback_code,
    }


def import_content(db: Session, content: ContentFile) -> Tuple[int, int]:
    """Insert or update all missions and challenges. Returns (missions, challenges)."""
    n_challenges = 0
    for mission_in in content.missions:
        mission = db.get(Mission, mission_in.id) or Mission(id=mission_in.id)
        mission.title = mission_in.title
        mission.description = mission_in.description
        db.add(mission)
        for position, challenge_in in enumerate(mission_in.challenges):
            challenge = db.get(Challenge, challenge_in.id) or Challenge(id=challenge_in.id)
            challenge.mission_id = mission.id
            challenge.position = position
            challenge.concept_id = challenge_in.concept_id
            challenge.title = challenge_in.title
            challenge.prompt = challenge_in.prompt
            challenge.options = [option.model_dump() for option in challenge_in.options]
            challenge.rubric = build_rubric(challenge_in)
            challenge.feedback_messages = challenge_in.feedback_messages
            db.add(challenge)
            n_challenges += 1
    db.commit()
    return len(content.missions), n_challenges


def load_content_file(path: Path) -> ContentFile:
    return ContentFile.model_validate(json.loads(path.read_text(encoding="utf-8")))
