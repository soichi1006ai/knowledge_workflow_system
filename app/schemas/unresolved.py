from typing import Optional

from pydantic import Field

from app.schemas.common import ApiResponse, KOSBaseModel


class UnresolvedDocument(KOSBaseModel):
    frontmatter: dict
    body: dict


class UnresolvedListItem(KOSBaseModel):
    question_id: str
    question: str
    status: str
    priority: str
    linked_project_id: Optional[str] = None
    created_at: Optional[str] = None


class UnresolvedListResponse(ApiResponse):
    items: list[UnresolvedListItem] = Field(default_factory=list)


class UnresolvedCreateRequest(KOSBaseModel):
    question: str
    status: str = "open"
    priority: str = "medium"
    linked_project_id: Optional[str] = None
    linked_page_ids: list[str] = Field(default_factory=list)
    linked_source_ids: list[str] = Field(default_factory=list)
    why_unresolved: str
    next_step: str


class UnresolvedCreateResponse(ApiResponse):
    question_id: str
