import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import Client, Role, User
from app.schemas.auth import RegisterRequest, TokenResponse, UserResponse
from app.services.audit_service import AuditService

settings = get_settings()


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.audit = AuditService(db)

    async def register(self, data: RegisterRequest) -> tuple[User, TokenResponse]:
        existing = await self.db.execute(select(User).where(User.email == data.email))
        if existing.scalar_one_or_none():
            raise ValueError("Email already registered")

        role_result = await self.db.execute(select(Role).where(Role.name == data.role))
        role = role_result.scalar_one_or_none()
        if not role:
            role_result = await self.db.execute(select(Role).where(Role.name == "client"))
            role = role_result.scalar_one()

        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            role_id=role.id,
            is_active=True,
        )
        self.db.add(user)
        await self.db.flush()

        if data.role == "client":
            self.db.add(Client(user_id=user.id))

        await self.db.refresh(user, ["role"])
        tokens = await self._issue_tokens(user)
        await self.audit.log(user.id, "user.register", "users", user.id)
        return user, tokens

    async def login(self, email: str, password: str) -> tuple[User, TokenResponse]:
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.email == email, User.deleted_at.is_(None))
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Account is deactivated")

        user.last_login_at = datetime.now(timezone.utc)
        tokens = await self._issue_tokens(user)
        await self.audit.log(user.id, "user.login", "users", user.id)
        return user, tokens

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.id == UUID(payload["sub"]), User.deleted_at.is_(None))
        )
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise ValueError("User not found")

        return await self._issue_tokens(user)

    async def _issue_tokens(self, user: User) -> TokenResponse:
        access = create_access_token(
            user.id,
            extra={"role": user.role.name if user.role else "client", "email": user.email},
        )
        refresh = create_refresh_token(user.id)
        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.jwt_access_token_expire_minutes * 60,
        )

    @staticmethod
    def to_user_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            phone=user.phone,
            avatar_url=user.avatar_url,
            role=user.role.name if user.role else "",
            role_display=user.role.display_name if user.role else "",
            is_active=user.is_active,
            is_verified=user.is_verified,
            locale=user.locale,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
        )
