"""Pydantic request/response models (the public API contract)."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
