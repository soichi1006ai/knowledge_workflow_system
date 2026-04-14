from fastapi import APIRouter

from app.schemas.query import (
    QueryCitationPage,
    QueryCitationSource,
    QueryRequest,
    QueryResponse,
    SuggestedAction,
    SuggestedDecision,
    SuggestedUnresolved,
)

router = APIRouter(prefix="/api/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    return QueryResponse(
        answer="Knowledge OS should connect knowledge to decisions and actions, not just store notes.",
        page_confidence_summary="1 stable concept page and 1 stable project page used",
        cited_pages=[
            QueryCitationPage(page_id="pg_kos001", title="Knowledge OS", page_type="concept"),
            QueryCitationPage(page_id="pg_prj001", title="Knowledge OS MVP Project", page_type="project"),
        ],
        cited_sources=[
            QueryCitationSource(
                source_id="src_kos001",
                title="Knowledge OS direction memo",
                canonical_source_type="raw-note",
            )
        ],
        suggested_decisions=[
            SuggestedDecision(
                title="Keep workflow-first architecture",
                context="The core differentiator is end-to-end knowledge flow.",
                reason="It separates the product from generic note apps.",
            )
        ],
        suggested_actions=[
            SuggestedAction(
                title="Implement ingest preview flow",
                description="Build the first workflow surface from raw input to structured preview.",
                priority="high",
            )
        ],
        suggested_unresolved=[
            SuggestedUnresolved(
                question="What is the smallest lovable dashboard?",
                why_unresolved="The dashboard shape is not yet validated.",
                next_step="Create a low-fidelity wireframe and test it.",
                priority="high",
            )
        ],
    )
