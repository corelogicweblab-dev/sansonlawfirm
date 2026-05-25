from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, DbSession, require_roles
from app.models.user import User
from app.schemas.common import APIResponse

router = APIRouter()


@router.get("/dashboard", response_model=APIResponse[dict])
async def dashboard_analytics(
    db: DbSession,
    current_user: CurrentUser,
    _: User = Depends(require_roles("admin")),
):
    from sqlalchemy import func, select
    from app.models.case import Case
    from app.models.user import User as UserModel

    cases_count = await db.execute(select(func.count(Case.id)).where(Case.deleted_at.is_(None)))
    users_count = await db.execute(
        select(func.count(UserModel.id)).where(UserModel.deleted_at.is_(None))
    )

    return APIResponse(
        data={
            "total_cases": cases_count.scalar() or 0,
            "total_users": users_count.scalar() or 0,
            "active_cases": 0,
            "pending_reviews": 0,
            "ai_usage_tokens": 0,
        },
        message="Analytics retrieved",
    )
