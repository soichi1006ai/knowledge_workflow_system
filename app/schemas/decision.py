from typing import Optional

from pydantic import Field

from app.schemas.common import ApiResponse, KOSBaseModel


class DecisionDocument(KOSBaseModel):
    frontmatter: dict
    body: dict


class DecisionListItem(KOSBaseModel):
    decision_id: str
    title: str
    status: str
    linked_project_id: Optional[str] = None
    created_at: Optional[str] = None
    confirmed_at: Optional[str] = None


class DecisionListResponse(ApiResponse):
    items: list[DecisionListItem] = Field(default_factory=list)


class DecisionCreateRequest(KOSBaseModel):
    title: str
    linked_project_id: Optional[str] = None
    linked_page_ids: list[str] = Field(default_factory=list)
    linked_source_ids: list[str] = Field(default_factory=list)
    context: str
    options: list[str] = Field(default_factory=list)
    chosen_option: Optional[str] = None
    reason: str
    risks: list[str] = Field(default_factory=list)
    status: str = "draft"


class DecisionCreateResponse(ApiResponse):
    decision_id: str
