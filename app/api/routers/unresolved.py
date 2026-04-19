from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.schemas.unresolved import (
    UnresolvedCreateRequest,
    UnresolvedCreateResponse,
    UnresolvedListItem,
    UnresolvedListResponse,
)
from app.services.vault_object_service import VaultObjectService

router = APIRouter(prefix="/api/unresolved", tags=["unresolved"])
vault_service = VaultObjectService()


@router.get("", response_model=UnresolvedListResponse)
def list_unresolved() -> UnresolvedListResponse:
    objects = vault_service.list_objects("unresolved/active")
    items = []
    for fm in objects:
        try:
            items.append(
                UnresolvedListItem(
                    question_id=str(fm.get("question_id", "")),
                    question=str(fm.get("question", fm.get("title", ""))),
                    status=str(fm.get("status", "open")),
                    priority=str(fm.get("priority", "medium")),
                    linked_project_id=fm.get("linked_project_id") or None,
                    created_at=fm.get("created_at") or None,
                )
            )
        except Exception:
            continue
    return UnresolvedListResponse(items=items)


@router.post("", response_model=UnresolvedCreateResponse)
def create_unresolved(payload: UnresolvedCreateRequest) -> UnresolvedCreateResponse:
    return UnresolvedCreateResponse(question_id="uq_demo001", message="stub")


@router.post("/{question_id}/send-to-query", response_model=ApiResponse)
def send_to_query(question_id: str) -> ApiResponse:
    return ApiResponse(message=f"unresolved {question_id} sent to query (stub)")
