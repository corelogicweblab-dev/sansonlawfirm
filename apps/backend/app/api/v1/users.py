from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.dependencies import CurrentUser, DbSession, require_roles
from app.models.user import Role, User
from app.schemas.auth import UserResponse
from app.schemas.common import APIResponse, PaginatedResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_users(
    db: DbSession,
    _: User = Depends(require_roles("admin")),
    page: int = 1,
    page_size: int = 20,
):
    offset = (page - 1) * page_size
    result = await db.execute(
        select(User)
        .options(selectinload(User.role))
        .where(User.deleted_at.is_(None))
        .offset(offset)
        .limit(page_size)
    )
    users = result.scalars().all()
    service = AuthService(db)
    return PaginatedResponse(
        data=[service.to_user_response(u) for u in users],
        total=len(users),
        page=page,
        page_size=page_size,
    )


@router.get("/roles", response_model=APIResponse[list])
async def list_roles(db: DbSession, _: User = Depends(require_roles("admin"))):
    result = await db.execute(select(Role).where(Role.deleted_at.is_(None)))
    roles = result.scalars().all()
    return APIResponse(
        data=[
            {
                "id": str(r.id),
                "name": r.name,
                "display_name": r.display_name,
                "permissions": r.permissions,
            }
            for r in roles
        ]
    )


@router.patch("/{user_id}/deactivate", response_model=APIResponse[None])
async def deactivate_user(
    user_id: str,
    db: DbSession,
    current_user: CurrentUser,
    _: User = Depends(require_roles("admin")),
):
    from uuid import UUID

    result = await db.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
    user.is_active = False
    return APIResponse(message="User deactivated")
