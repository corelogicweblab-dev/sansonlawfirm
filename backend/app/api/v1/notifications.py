from fastapi import APIRouter
from sqlalchemy import select

from app.core.dependencies import CurrentUser, DbSession
from app.models.notification import Notification
from app.schemas.common import APIResponse

router = APIRouter()


@router.get("", response_model=APIResponse[list])
async def list_notifications(current_user: CurrentUser, db: DbSession, unread_only: bool = False):
    query = select(Notification).where(Notification.user_id == current_user.id)
    if unread_only:
        query = query.where(Notification.is_read == False)  # noqa: E712
    query = query.order_by(Notification.created_at.desc()).limit(50)
    result = await db.execute(query)
    notifications = result.scalars().all()
    return APIResponse(
        data=[
            {
                "id": str(n.id),
                "type": n.type,
                "title": n.title,
                "body": n.body,
                "data": n.data,
                "is_read": n.is_read,
                "created_at": n.created_at.isoformat(),
            }
            for n in notifications
        ]
    )


@router.patch("/{notification_id}/read", response_model=APIResponse[None])
async def mark_read(notification_id: str, current_user: CurrentUser, db: DbSession):
    from datetime import datetime, timezone
    from uuid import UUID

    result = await db.execute(
        select(Notification).where(
            Notification.id == UUID(notification_id),
            Notification.user_id == current_user.id,
        )
    )
    notification = result.scalar_one_or_none()
    if notification:
        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)
    return APIResponse(message="Notification marked as read")
