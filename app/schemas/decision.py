from pydantic import Field

from app.schemas.common import ApiResponse, KOSBaseModel


class DecisionDocument(KOSBaseModel):
    frontmatter: dict
    body: dict


class DecisionListItem(KOSBaseModel):
    decision_id: str
    title: str
    status: str
    linked_project_id: str | None = None
    created_at: str | None = None
    confirmed_at: str | None = None


class DecisionListResponse(ApiResponse):
    items: list[DecisionListItem] = Field(default_factory=list)


class DecisionCreateRequest(KOSBaseModel):
    title: str
    linked_project_id: str | None = None
    linked_page_ids: list[str] = Field(default_factory=list)
    linked_source_ids: list[str] = Field(default_factory=list)
    context: str
    options: list[str] = Field(default_factory=list)
    chosen_option: str | None = None
    reason: str
    risks: list[str] = Field(default_factory=list)
    status: str = "draft"


class DecisionCreateResponse(ApiResponse):
    decision_id: str
