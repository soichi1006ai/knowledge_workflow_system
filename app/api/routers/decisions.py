from fastapi import APIRouter

from app.schemas.decision import DecisionCreateRequest, DecisionCreateResponse, DecisionListItem, DecisionListResponse
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api/decisions", tags=["decisions"])


@router.get("", response_model=DecisionListResponse)
def list_decisions() -> DecisionListResponse:
    return DecisionListResponse(
        items=[
            DecisionListItem(
                decision_id="dec_kos001",
                title="Adopt workflow-first MVP architecture",
                status="confirmed",
                linked_project_id="prj_kos001",
                created_at="2026-04-14",
                confirmed_at="2026-04-14",
            )
        ]
    )


@router.post("", response_model=DecisionCreateResponse)
def create_decision(payload: DecisionCreateRequest) -> DecisionCreateResponse:
    return DecisionCreateResponse(decision_id="dec_demo001", message="stub")


@router.post("/{decision_id}/confirm", response_model=ApiResponse)
def confirm_decision(decision_id: str) -> ApiResponse:
    return ApiResponse(message=f"decision {decision_id} confirmed (stub)")
