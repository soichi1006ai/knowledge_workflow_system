from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.schemas.decision import DecisionCreateRequest, DecisionCreateResponse, DecisionListItem, DecisionListResponse
from app.services.vault_object_service import VaultObjectService

router = APIRouter(prefix="/api/decisions", tags=["decisions"])
vault_service = VaultObjectService()


@router.get("", response_model=DecisionListResponse)
def list_decisions() -> DecisionListResponse:
    objects = vault_service.list_objects("decisions/active")
    items = []
    for fm in objects:
        try:
            items.append(
                DecisionListItem(
                    decision_id=str(fm.get("decision_id", "")),
                    title=str(fm.get("title", "")),
                    status=str(fm.get("status", "draft")),
                    linked_project_id=fm.get("linked_project_id") or None,
                    created_at=fm.get("created_at") or None,
                    confirmed_at=fm.get("confirmed_at") or None,
                )
            )
        except Exception:
            continue
    return DecisionListResponse(items=items)


@router.post("", response_model=DecisionCreateResponse)
def create_decision(payload: DecisionCreateRequest) -> DecisionCreateResponse:
    return DecisionCreateResponse(decision_id="dec_demo001", message="stub")


@router.post("/{decision_id}/confirm", response_model=ApiResponse)
def confirm_decision(decision_id: str) -> ApiResponse:
    return ApiResponse(message=f"decision {decision_id} confirmed (stub)")
