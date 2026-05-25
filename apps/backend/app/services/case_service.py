from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.case import Case, CaseActivity, CaseStatus
from app.models.user import Client
from app.schemas.case import CaseCreate, CaseResponse


class CaseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _generate_case_number(self) -> str:
        year = datetime.now(timezone.utc).year
        count_result = await self.db.execute(select(func.count(Case.id)))
        count = (count_result.scalar() or 0) + 1
        return f"SLF-{year}-{count:05d}"

    async def create_intake_case(
        self, client_id: UUID, data: CaseCreate, intake_summary: str | None = None
    ) -> Case:
        status_result = await self.db.execute(
            select(CaseStatus).where(CaseStatus.name == "ai_intake")
        )
        status = status_result.scalar_one()

        case = Case(
            case_number=await self._generate_case_number(),
            client_id=client_id,
            status_id=status.id,
            title=data.title,
            description=data.description,
            category=data.category,
            priority=data.priority,
            intake_summary=intake_summary,
            formally_proceeded=False,
        )
        self.db.add(case)
        await self.db.flush()

        activity = CaseActivity(
            case_id=case.id,
            action="case.created",
            description="Case created via AI intake",
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(activity)
        return case

    async def proceed_with_legal_action(self, case_id: UUID, user_id: UUID) -> Case:
        result = await self.db.execute(
            select(Case)
            .options(selectinload(Case.status))
            .where(Case.id == case_id, Case.deleted_at.is_(None))
        )
        case = result.scalar_one_or_none()
        if not case:
            raise ValueError("Case not found")

        status_result = await self.db.execute(
            select(CaseStatus).where(CaseStatus.name == "pending_review")
        )
        pending_status = status_result.scalar_one()

        case.formally_proceeded = True
        case.proceeded_at = datetime.now(timezone.utc)
        case.status_id = pending_status.id
        case.is_actionable = True

        activity = CaseActivity(
            case_id=case.id,
            user_id=user_id,
            action="case.proceeded",
            description="Client formally proceeded with legal services",
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(activity)
        await self.db.flush()
        await self.db.refresh(case, ["status"])
        return case

    async def get_client_cases(self, user_id: UUID) -> list[Case]:
        client_result = await self.db.execute(select(Client).where(Client.user_id == user_id))
        client = client_result.scalar_one_or_none()
        if not client:
            return []

        result = await self.db.execute(
            select(Case)
            .options(selectinload(Case.status))
            .where(Case.client_id == client.id, Case.deleted_at.is_(None))
            .order_by(Case.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_lawyer_cases(self, user_id: UUID) -> list[Case]:
        from app.models.user import Lawyer

        lawyer_result = await self.db.execute(select(Lawyer).where(Lawyer.user_id == user_id))
        lawyer = lawyer_result.scalar_one_or_none()
        if not lawyer:
            return []

        result = await self.db.execute(
            select(Case)
            .options(selectinload(Case.status), selectinload(Case.client))
            .where(Case.assigned_lawyer_id == lawyer.id, Case.deleted_at.is_(None))
            .order_by(Case.updated_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    def to_response(case: Case) -> CaseResponse:
        return CaseResponse(
            id=case.id,
            case_number=case.case_number,
            title=case.title,
            description=case.description,
            category=case.category,
            priority=case.priority,
            status_name=case.status.name if case.status else "",
            status_display=case.status.display_name if case.status else "",
            intake_summary=case.intake_summary,
            is_actionable=case.is_actionable,
            formally_proceeded=case.formally_proceeded,
            proceeded_at=case.proceeded_at,
            client_id=case.client_id,
            assigned_lawyer_id=case.assigned_lawyer_id,
            created_at=case.created_at,
            updated_at=case.updated_at,
        )
