from typing import Optional, Union

from pydantic import Field

from app.core.enums import CanonicalSourceType, InputSourceType, PageType
from app.schemas.common import ApiResponse, KOSBaseModel


class RawCreateRequest(KOSBaseModel):
    title: str
    body: str
    input_source_type: Union[InputSourceType, str]
    project_id: Optional[str] = None
    source_url: Optional[str] = None
    quick_tags: list[str] = Field(default_factory=list)


class RawCreateResponse(ApiResponse):
    raw_id: str


class RawListItem(KOSBaseModel):
    raw_id: str
    title: str
    input_source_type: Union[InputSourceType, str]
    project_candidate: Optional[str] = None
    created_at: str
    imported_at: Optional[str] = None


class RawListResponse(ApiResponse):
    items: list[RawListItem] = Field(default_factory=list)


class IngestPreviewRequest(KOSBaseModel):
    mode: str = "auto"
    allow_existing_page_match: bool = True


class IngestPreviewResponse(ApiResponse):
    raw_id: str
    suggested_project_id: Optional[str] = None
    candidate_existing_pages: list[dict] = Field(default_factory=list)
    candidate_new_page_type: Optional[PageType] = None
    normalized_canonical_source_type: Optional[CanonicalSourceType] = None
    extracted_summary: str = ""
    extracted_key_points: list[str] = Field(default_factory=list)
    extracted_sources: list[str] = Field(default_factory=list)
    extracted_unresolved_questions: list[str] = Field(default_factory=list)
    proposed_decisions: list[dict] = Field(default_factory=list)
    proposed_actions: list[dict] = Field(default_factory=list)
    confidence: str = "low"


class IngestCommitRequest(KOSBaseModel):
    approved_page_title: Optional[str] = None
    approved_page_type: Optional[PageType] = None
    approved_project_id: Optional[str] = None
    existing_page_path: Optional[str] = None
    create_missing_source: bool = True
    create_actions: bool = True
    create_decisions: bool = True


class IngestCommitResponse(ApiResponse):
    raw_id: str
    source_id: Optional[str] = None
    created_page_ids: list[str] = Field(default_factory=list)
    updated_page_ids: list[str] = Field(default_factory=list)
    created_decision_ids: list[str] = Field(default_factory=list)
    created_question_ids: list[str] = Field(default_factory=list)
    created_action_ids: list[str] = Field(default_factory=list)


class InboxImportRequest(KOSBaseModel):
    mode: str = "copy"
    limit: int = 20
    delete_from_inbox: bool = False


class InboxImportItemResult(KOSBaseModel):
    filename: str
    detected_type: Union[InputSourceType, str]
    mime_type: Optional[str] = None
    raw_id: str
    raw_path: str
    attachment_path: Optional[str] = None
    extraction_status: str
    warnings: list[str] = Field(default_factory=list)


class InboxImportResponse(ApiResponse):
    items: list[InboxImportItemResult] = Field(default_factory=list)
