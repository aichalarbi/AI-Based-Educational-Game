from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Attempt, Challenge, Mission
from ..schemas import AttemptOut, MissionOut
from .attempts import to_attempt_out

router = APIRouter(prefix="/missions", tags=["missions"])


def _get_mission_or_404(db: Session, mission_id: str) -> Mission:
    mission = db.get(Mission, mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail=f"Mission '{mission_id}' not found")
    return mission


@router.get("/{mission_id}", response_model=MissionOut)
def get_mission(mission_id: str, db: Session = Depends(get_db)) -> Mission:
    # MissionOut/ChallengeOut only declare student-safe fields; the rubric is never serialised.
    return _get_mission_or_404(db, mission_id)


@router.get("/{mission_id}/attempts", response_model=List[AttemptOut])
def list_mission_attempts(
    mission_id: str,
    player_id: Optional[str] = Query(default=None, alias="playerId"),
    db: Session = Depends(get_db),
) -> List[AttemptOut]:
    _get_mission_or_404(db, mission_id)
    query = (
        select(Attempt)
        .join(Challenge)
        .where(Challenge.mission_id == mission_id)
        .order_by(Attempt.id)
    )
    if player_id is not None:
        query = query.where(Attempt.player_id == player_id)
    return [to_attempt_out(attempt) for attempt in db.scalars(query)]
