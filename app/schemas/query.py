from pydantic import Field

from app.core.enums import QueryMode
from app.schemas.common import ApiResponse, KOSBaseModel


class QueryRequest(KOSBaseModel):
    query: str
    mode: QueryMode
    active_project_id: str | None = None
    include_archived: bool = False
    max_results: int = 10


class QueryResponse(ApiResponse):
    answer: str
    cited_pages: list[dict] = Field(default_factory=list)
    cited_sources: list[dict] = Field(default_factory=list)
    page_confidence_summary: str = ""
    suggested_decisions: list[dict] = Field(default_factory=list)
    suggested_actions: list[dict] = Field(default_factory=list)
    suggested_unresolved: list[dict] = Field(default_factory=list)
