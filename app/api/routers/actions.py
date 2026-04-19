from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.schemas.action import ActionCreateRequest, ActionCreateResponse, ActionListItem, ActionListResponse
from app.services.vault_object_service import VaultObjectService

router = APIRouter(prefix="/api/actions", tags=["actions"])
vault_service = VaultObjectService()


@router.get("", response_model=ActionListResponse)
def list_actions() -> ActionListResponse:
    objects = vault_service.list_objects("actions/open")
    items = []
    for fm in objects:
        try:
            items.append(
                ActionListItem(
                    action_id=str(fm.get("action_id", "")),
                    title=str(fm.get("title", "")),
                    status=str(fm.get("status", "open")),
                    priority=str(fm.get("priority", "medium")),
                    owner=fm.get("owner") or None,
                    due_date=fm.get("due_date") or None,
                    linked_project_id=fm.get("linked_project_id") or None,
                )
            )
        except Exception:
            continue
    return ActionListResponse(items=items)


@router.post("", response_model=ActionCreateResponse)
def create_action(payload: ActionCreateRequest) -> ActionCreateResponse:
    return ActionCreateResponse(action_id="act_demo001", message="stub")


@router.post("/{action_id}/move", response_model=ApiResponse)
def move_action(action_id: str) -> ApiResponse:
    return ApiResponse(message=f"action {action_id} moved (stub)")
