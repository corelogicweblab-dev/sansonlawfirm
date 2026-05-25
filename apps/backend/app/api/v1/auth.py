from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUser, DbSession
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse, UserResponse
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=APIResponse[dict])
async def register(data: RegisterRequest, db: DbSession):
    try:
        service = AuthService(db)
        user, tokens = await service.register(data)
        return APIResponse(
            success=True,
            message="Registration successful",
            data={"user": service.to_user_response(user), "tokens": tokens},
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=APIResponse[dict])
async def login(data: LoginRequest, db: DbSession):
    try:
        service = AuthService(db)
        user, tokens = await service.login(data.email, data.password)
        return APIResponse(
            success=True,
            message="Login successful",
            data={"user": service.to_user_response(user), "tokens": tokens},
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", response_model=APIResponse[TokenResponse])
async def refresh_token(data: RefreshRequest, db: DbSession):
    try:
        service = AuthService(db)
        tokens = await service.refresh(data.refresh_token)
        return APIResponse(success=True, message="Token refreshed", data=tokens)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=APIResponse[UserResponse])
async def get_me(current_user: CurrentUser, db: DbSession):
    service = AuthService(db)
    return APIResponse(
        success=True,
        message="User profile retrieved",
        data=service.to_user_response(current_user),
    )


@router.post("/logout", response_model=APIResponse[None])
async def logout(current_user: CurrentUser):
    return APIResponse(success=True, message="Logged out successfully")
