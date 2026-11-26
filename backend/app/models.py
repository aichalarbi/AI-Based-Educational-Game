"""SQLAlchemy ORM models."""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")

    challenges: Mapped[List["Challenge"]] = relationship(
        back_populates="mission",
        order_by="Challenge.position",
        cascade="all, delete-orphan",
    )


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id"), index=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
    concept_id: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(200))
    prompt: Mapped[str] = mapped_column(Text)
    # [{"id": "A", "text": "..."}, ...] – safe to send to students.
    options: Mapped[list] = mapped_column(JSON)
    # SERVER-SIDE ONLY: rubric in the format of learning_engine.evaluate_answer().
    rubric: Mapped[dict] = mapped_column(JSON)
    # {feedback_code: message shown to the student}
    feedback_messages: Mapped[dict] = mapped_column(JSON, default=dict)

    mission: Mapped[Mission] = relationship(back_populates="challenges")


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    challenge_id: Mapped[str] = mapped_column(ForeignKey("challenges.id"), index=True)
    player_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    selected_option_id: Mapped[str] = mapped_column(String(100))
    is_correct: Mapped[bool] = mapped_column(Boolean)
    feedback_code: Mapped[str] = mapped_column(String(100))
    next_action: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    challenge: Mapped[Challenge] = relationship()
