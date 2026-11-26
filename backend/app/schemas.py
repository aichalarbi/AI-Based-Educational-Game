"""Pydantic request/response models (the public API contract, see contracts/api.md).

JSON field names are camelCase; Python attributes are snake_case.
"""

from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


class HealthResponse(BaseModel):
    status: str


# --- Student-facing (never contains rubric / correct answer) ---------------------------

class OptionOut(ApiModel):
    id: str
    text: str


class ChallengeOut(ApiModel):
    id: str
    concept_id: str
    title: str
    prompt: str
    options: List[OptionOut]


class MissionOut(ApiModel):
    id: str
    title: str
    description: str
    challenges: List[ChallengeOut]


class AttemptIn(ApiModel):
    model_config = ConfigDict(extra="forbid")

    challenge_id: str = Field(min_length=1)
    selected_option_id: str = Field(min_length=1)
    player_id: Optional[str] = Field(default=None, min_length=1, max_length=100)


class AttemptOut(ApiModel):
    id: int
    challenge_id: str
    player_id: Optional[str]
    selected_option_id: str
    is_correct: bool
    feedback_code: str
    feedback_message: str
    next_action: Literal["continue", "review"]
    created_at: datetime


# --- Content import format (authored by P4, contains the answer key) -------------------

class RubricIn(ApiModel):
    model_config = ConfigDict(extra="forbid")

    correct_option_id: str
    correct_feedback_code: str = "CORRECT"
    incorrect_feedback_code: str = "REVIEW_CONCEPT"


class ChallengeIn(ApiModel):
    id: str = Field(min_length=1)
    concept_id: str = Field(min_length=1)
    title: str
    prompt: str
    options: List[OptionOut] = Field(min_length=2)
    rubric: RubricIn
    feedback_messages: Dict[str, str] = {}


class MissionIn(ApiModel):
    id: str = Field(min_length=1)
    title: str
    description: str = ""
    challenges: List[ChallengeIn]


class ContentFile(ApiModel):
    missions: List[MissionIn]
