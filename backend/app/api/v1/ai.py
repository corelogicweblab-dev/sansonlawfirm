from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, DbSession, require_roles
from app.models.user import User
from app.schemas.common import APIResponse

router = APIRouter()


@router.post("/classify", response_model=APIResponse[dict])
async def classify_case(
    db: DbSession,
    current_user: CurrentUser,
    _: User = Depends(require_roles("client", "lawyer", "paralegal", "admin")),
):
    """AI case classifier — Phase 2."""
    return APIResponse(
        data={"category": "civil", "confidence": 0.0, "status": "phase_2_pending"},
        message="Classifier endpoint ready for Phase 2 integration",
    )


@router.post("/summarize", response_model=APIResponse[dict])
async def summarize_case(
    db: DbSession,
    current_user: CurrentUser,
    _: User = Depends(require_roles("lawyer", "paralegal", "admin")),
):
    """AI case summarizer — Phase 2."""
    return APIResponse(
        data={"summary": "", "status": "phase_2_pending"},
        message="Summarizer endpoint ready for Phase 2 integration",
    )
