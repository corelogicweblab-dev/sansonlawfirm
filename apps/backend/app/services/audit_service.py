from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.misc import AuditLog


class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(
        self,
        user_id: UUID | None,
        action: str,
        resource: str | None = None,
        resource_id: UUID | None = None,
        old_values: dict | None = None,
        new_values: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        metadata: dict | None = None,
    ) -> AuditLog:
        from datetime import datetime, timezone

        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata_=metadata or {},
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(entry)
        return entry
