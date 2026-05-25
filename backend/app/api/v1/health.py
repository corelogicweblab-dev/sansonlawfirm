from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.common import APIResponse

router = APIRouter()
settings = get_settings()


@router.get("")
async def health_check():
    return APIResponse(
        success=True,
        message="SANSON Legal OS API is running",
        data={
            "app": settings.app_name,
            "version": settings.app_version,
            "api_version": settings.api_version,
        },
    )
