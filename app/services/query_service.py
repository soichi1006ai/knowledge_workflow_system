from app.schemas.query import (
    QueryCitationPage,
    QueryCitationSource,
    QueryRequest,
    QueryResponse,
    SuggestedAction,
    SuggestedDecision,
    SuggestedUnresolved,
)


class QueryService:
    def run(self, payload: QueryRequest) -> QueryResponse:
        return QueryResponse(
            answer="Knowledge OS should operationalize knowledge, not merely store it.",
            page_confidence_summary="stable project and concept pages were used",
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
                    title="Prioritize workflow-first architecture",
                    context="The main differentiator is knowledge-to-action flow.",
                    reason="This is where the product beats generic note systems.",
                )
            ],
            suggested_actions=[
                SuggestedAction(
                    title="Implement repository-backed query resolution",
                    description="Replace stub query logic with vault-backed retrieval.",
                    priority="high",
                )
            ],
            suggested_unresolved=[
                SuggestedUnresolved(
                    question="What is the smallest lovable dashboard?",
                    why_unresolved="The minimal differentiated dashboard is still not proven.",
                    next_step="Prototype one triage-first dashboard.",
                    priority="high",
                )
            ],
        )
