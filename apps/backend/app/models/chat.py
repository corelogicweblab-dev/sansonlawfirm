import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Chat(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "chats"

    client_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id"))
    case_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id"))
    title: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, default=dict)

    messages: Mapped[List["ChatMessage"]] = relationship(back_populates="chat")


class ChatMessage(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "chat_messages"

    chat_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chats.id"))
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, default=dict)
    tokens_used: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    chat: Mapped["Chat"] = relationship(back_populates="messages")


class AISummary(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "ai_summaries"

    case_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id"))
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id")
    )
    summary_type: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    key_facts: Mapped[list | None] = mapped_column(JSONB, default=list)
    parties: Mapped[list | None] = mapped_column(JSONB, default=list)
    evidence_refs: Mapped[list | None] = mapped_column(JSONB, default=list)
    model_used: Mapped[str | None] = mapped_column(String(50))
    tokens_used: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
