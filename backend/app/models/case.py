import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import Client, Lawyer, Paralegal


class CaseStatus(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "case_statuses"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str | None] = mapped_column(String(20))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_terminal: Mapped[bool] = mapped_column(Boolean, default=False)

    cases: Mapped[List["Case"]] = relationship(back_populates="status")


class Case(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "cases"

    case_number: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    client_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id"))
    assigned_lawyer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lawyers.id")
    )
    assigned_paralegal_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("paralegals.id")
    )
    status_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("case_statuses.id"))
    category: Mapped[str | None] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    intake_summary: Mapped[str | None] = mapped_column(Text)
    is_actionable: Mapped[bool | None] = mapped_column(Boolean, default=False)
    formally_proceeded: Mapped[bool] = mapped_column(Boolean, default=False)
    proceeded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    urgency_score: Mapped[int | None] = mapped_column(Integer, default=0)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, default=dict)

    client: Mapped["Client"] = relationship(back_populates="cases")
    status: Mapped["CaseStatus"] = relationship(back_populates="cases")
    assigned_lawyer: Mapped["Lawyer | None"] = relationship(foreign_keys=[assigned_lawyer_id])
    assigned_paralegal: Mapped["Paralegal | None"] = relationship(
        foreign_keys=[assigned_paralegal_id]
    )
    activities: Mapped[List["CaseActivity"]] = relationship(back_populates="case")


class CaseActivity(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "case_activities"

    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id"))
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    case: Mapped["Case"] = relationship(back_populates="activities")
