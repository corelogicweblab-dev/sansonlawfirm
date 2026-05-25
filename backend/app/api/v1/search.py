from fastapi import APIRouter, Depends, Query

from app.core.dependencies import CurrentUser, DbSession, require_roles
from app.models.user import User
from app.schemas.common import APIResponse

router = APIRouter()


@router.get("/semantic", response_model=APIResponse[list])
async def semantic_search(
    q: str = Query(..., min_length=2),
    db: DbSession = None,
    current_user: CurrentUser = None,
    _: User = Depends(require_roles("lawyer", "paralegal", "admin")),
):
    """Semantic vector search — Phase 3."""
    return APIResponse(
        data=[],
        message=f"Semantic search for '{q}' — Phase 3 Qdrant integration pending",
    )
