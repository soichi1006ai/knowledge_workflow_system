from pydantic import Field

from app.schemas.common import ApiResponse, KOSBaseModel


class ActionDocument(KOSBaseModel):
    frontmatter: dict
    body: dict


class ActionListItem(KOSBaseModel):
    action_id: str
    title: str
    status: str
    priority: str
    owner: str | None = None
    due_date: str | None = None
    linked_project_id: str | None = None


class ActionListResponse(ApiResponse):
    items: list[ActionListItem] = Field(default_factory=list)


class ActionCreateRequest(KOSBaseModel):
    title: str
    description: str
    priority: str = "medium"
    owner: str | None = None
    due_date: str | None = None
    linked_project_id: str | None = None
    linked_decision_id: str | None = None
    linked_page_ids: list[str] = Field(default_factory=list)


class ActionCreateResponse(ApiResponse):
    action_id: str
