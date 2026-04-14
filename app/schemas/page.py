from pydantic import Field

from app.core.enums import PageConfidence, PageStatus, PageType
from app.schemas.common import ApiResponse, KOSBaseModel


class PageSummary(KOSBaseModel):
    page_id: str
    title: str
    type: PageType
    status: PageStatus
    page_confidence: PageConfidence
    linked_project_id: str | None = None
    updated_at: str | None = None
    review_due: str | None = None


class PageDocument(KOSBaseModel):
    frontmatter: dict
    body: str


class PageDetailResponse(ApiResponse):
    item: PageDocument


class PageListResponse(ApiResponse):
    items: list[PageSummary] = Field(default_factory=list)
