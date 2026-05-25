from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.dependencies import CurrentUser, DbSession, require_roles
from app.models.user import User
from app.schemas.common import APIResponse

router = APIRouter()


@router.get("", response_model=APIResponse[list])
async def list_chats(
    current_user: CurrentUser,
    db: DbSession,
    _: User = Depends(require_roles("client")),
):
    return APIResponse(data=[], message="Chat sessions retrieved")


@router.post("/message")
async def send_message(
    current_user: CurrentUser,
    db: DbSession,
    _: User = Depends(require_roles("client")),
):
    """Streaming AI chat endpoint — Phase 2 implementation."""
    raise HTTPException(status_code=501, detail="AI chat streaming available in Phase 2")


@router.post("/message/stream")
async def stream_message(
    current_user: CurrentUser,
    db: DbSession,
    _: User = Depends(require_roles("client")),
):
    from app.services.ai_service import AIService

    async def generate():
        service = AIService(db)
        async for chunk in service.stream_intake_response("Hello"):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
