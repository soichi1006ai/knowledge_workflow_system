from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import QueryService

router = APIRouter(prefix="/api/query", tags=["query"])
service = QueryService()


@router.post("", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    return service.run(payload)
