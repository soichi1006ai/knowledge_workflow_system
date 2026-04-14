from fastapi import APIRouter

from app.schemas.action import ActionCreateRequest, ActionCreateResponse, ActionListItem, ActionListResponse
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api/actions", tags=["actions"])


@router.get("", response_model=ActionListResponse)
def list_actions() -> ActionListResponse:
    return ActionListResponse(
        items=[
            ActionListItem(
                action_id="act_kos001",
                title="Implement initial raw -> query workflow",
                status="open",
                priority="high",
                owner="Master S",
                due_date="2026-04-20",
                linked_project_id="prj_kos001",
            )
        ]
    )


@router.post("", response_model=ActionCreateResponse)
def create_action(payload: ActionCreateRequest) -> ActionCreateResponse:
    return ActionCreateResponse(action_id="act_demo001", message="stub")


@router.post("/{action_id}/move", response_model=ApiResponse)
def move_action(action_id: str) -> ApiResponse:
    return ApiResponse(message=f"action {action_id} moved (stub)")
