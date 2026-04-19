from typing import Optional

from pydantic import Field

from app.core.enums import QueryMode
from app.schemas.common import ApiResponse, KOSBaseModel


class QueryRequest(KOSBaseModel):
    query: str
    mode: QueryMode
    active_project_id: Optional[str] = None
    include_archived: bool = False
    max_results: int = 10


class QueryCitationPage(KOSBaseModel):
    page_id: str
    title: str
    page_type: str


class QueryCitationSource(KOSBaseModel):
    source_id: str
    title: str
    canonical_source_type: str


class SuggestedDecision(KOSBaseModel):
    title: str
    context: str
    reason: str


class SuggestedAction(KOSBaseModel):
    title: str
    description: str
    priority: str = "medium"


class SuggestedUnresolved(KOSBaseModel):
    question: str
    why_unresolved: str
    next_step: str
    priority: str = "medium"


class QueryResponse(ApiResponse):
    answer: str
    cited_pages: list[QueryCitationPage] = Field(default_factory=list)
    cited_sources: list[QueryCitationSource] = Field(default_factory=list)
    page_confidence_summary: str = ""
    suggested_decisions: list[SuggestedDecision] = Field(default_factory=list)
    suggested_actions: list[SuggestedAction] = Field(default_factory=list)
    suggested_unresolved: list[SuggestedUnresolved] = Field(default_factory=list)
