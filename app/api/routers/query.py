from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse

router = APIRouter(prefix="/api/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    return QueryResponse(
        answer="stub answer",
        page_confidence_summary="stub summary",
        cited_pages=[],
        cited_sources=[],
        suggested_decisions=[],
        suggested_actions=[],
        suggested_unresolved=[],
    )
