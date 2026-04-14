from pydantic import Field

from app.core.enums import PageType
from app.schemas.common import ApiResponse, KOSBaseModel


class RawCreateRequest(KOSBaseModel):
    title: str
    body: str
    input_source_type: str
    project_id: str | None = None
    source_url: str | None = None
    quick_tags: list[str] = Field(default_factory=list)


class RawCreateResponse(ApiResponse):
    raw_id: str


class IngestPreviewRequest(KOSBaseModel):
    mode: str = "auto"
    allow_existing_page_match: bool = True


class IngestPreviewResponse(ApiResponse):
    raw_id: str
    suggested_project_id: str | None = None
    candidate_existing_pages: list[dict] = Field(default_factory=list)
    candidate_new_page_type: PageType | None = None
    extracted_summary: str = ""
    extracted_key_points: list[str] = Field(default_factory=list)
