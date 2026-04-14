from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.schemas.unresolved import (
    UnresolvedCreateRequest,
    UnresolvedCreateResponse,
    UnresolvedListItem,
    UnresolvedListResponse,
)

router = APIRouter(prefix="/api/unresolved", tags=["unresolved"])


@router.get("", response_model=UnresolvedListResponse)
def list_unresolved() -> UnresolvedListResponse:
    return UnresolvedListResponse(
        items=[
            UnresolvedListItem(
                question_id="uq_kos001",
                question="What is the smallest lovable dashboard for daily use?",
                status="open",
                priority="high",
                linked_project_id="prj_kos001",
                created_at="2026-04-14",
            )
        ]
    )


@router.post("", response_model=UnresolvedCreateResponse)
def create_unresolved(payload: UnresolvedCreateRequest) -> UnresolvedCreateResponse:
    return UnresolvedCreateResponse(question_id="uq_demo001", message="stub")


@router.post("/{question_id}/send-to-query", response_model=ApiResponse)
def send_to_query(question_id: str) -> ApiResponse:
    return ApiResponse(message=f"unresolved {question_id} sent to query (stub)")
