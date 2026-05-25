from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CaseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str | None = None
    category: str | None = None
    priority: str = "medium"


class CaseProceedRequest(BaseModel):
    """Client formally proceeds with legal services after AI intake."""
    case_id: UUID | None = None
    notes: str | None = None


class CaseResponse(BaseModel):
    id: UUID
    case_number: str
    title: str
    description: str | None
    category: str | None
    priority: str
    status_name: str
    status_display: str
    intake_summary: str | None
    is_actionable: bool | None
    formally_proceeded: bool
    proceeded_at: datetime | None
    client_id: UUID
    assigned_lawyer_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CaseStatusResponse(BaseModel):
    id: UUID
    name: str
    display_name: str
    color: str | None
    is_terminal: bool

    model_config = {"from_attributes": True}
