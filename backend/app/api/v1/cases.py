from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import CurrentUser, DbSession, require_roles
from app.models.user import User
from app.schemas.case import CaseCreate, CaseProceedRequest, CaseResponse
from app.schemas.common import APIResponse
from app.services.case_service import CaseService

router = APIRouter()


@router.get("", response_model=APIResponse[list[CaseResponse]])
async def list_cases(current_user: CurrentUser, db: DbSession):
    service = CaseService(db)
    role = current_user.role.name if current_user.role else ""

    if role == "client":
        cases = await service.get_client_cases(current_user.id)
    elif role == "lawyer":
        cases = await service.get_lawyer_cases(current_user.id)
    else:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        from app.models.case import Case

        result = await db.execute(
            select(Case)
            .options(selectinload(Case.status))
            .where(Case.deleted_at.is_(None))
            .order_by(Case.updated_at.desc())
            .limit(50)
        )
        cases = list(result.scalars().all())

    return APIResponse(
        data=[CaseService.to_response(c) for c in cases],
        message=f"Retrieved {len(cases)} cases",
    )


@router.post("", response_model=APIResponse[CaseResponse])
async def create_case(
    data: CaseCreate,
    current_user: CurrentUser,
    db: DbSession,
    _: User = Depends(require_roles("client")),
):
    from app.models.user import Client
    from sqlalchemy import select

    client_result = await db.execute(select(Client).where(Client.user_id == current_user.id))
    client = client_result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=400, detail="Client profile not found")

    service = CaseService(db)
    case = await service.create_intake_case(client.id, data)
    await db.refresh(case, ["status"])
    return APIResponse(data=CaseService.to_response(case), message="Case created")


@router.post("/proceed", response_model=APIResponse[CaseResponse])
async def proceed_with_legal_action(
    data: CaseProceedRequest,
    current_user: CurrentUser,
    db: DbSession,
    _: User = Depends(require_roles("client")),
):
    if not data.case_id:
        raise HTTPException(status_code=400, detail="case_id is required")

    try:
        service = CaseService(db)
        case = await service.proceed_with_legal_action(data.case_id, current_user.id)
        return APIResponse(
            data=CaseService.to_response(case),
            message="You have formally proceeded with legal services. A lawyer will review your case.",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{case_id}", response_model=APIResponse[CaseResponse])
async def get_case(case_id: UUID, current_user: CurrentUser, db: DbSession):
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.models.case import Case

    result = await db.execute(
        select(Case)
        .options(selectinload(Case.status))
        .where(Case.id == case_id, Case.deleted_at.is_(None))
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return APIResponse(data=CaseService.to_response(case))
