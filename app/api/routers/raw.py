from fastapi import APIRouter

from app.schemas.raw import (
    IngestCommitRequest,
    IngestCommitResponse,
    IngestPreviewRequest,
    IngestPreviewResponse,
    RawCreateRequest,
    RawCreateResponse,
    RawListResponse,
)
from app.services.raw_service import RawService
from app.workflows.ingest_commit_flow import IngestCommitFlow
from app.workflows.ingest_preview_flow import IngestPreviewFlow

router = APIRouter(prefix="/api/raw", tags=["raw"])
raw_service = RawService()
ingest_preview_flow = IngestPreviewFlow()
ingest_commit_flow = IngestCommitFlow()


@router.get("", response_model=RawListResponse)
def list_raw() -> RawListResponse:
    return raw_service.list_raw()


@router.post("", response_model=RawCreateResponse)
def create_raw(payload: RawCreateRequest) -> RawCreateResponse:
    return raw_service.create_raw(payload)


@router.post("/{raw_id}/ingest-preview", response_model=IngestPreviewResponse)
def ingest_preview(raw_id: str, payload: IngestPreviewRequest) -> IngestPreviewResponse:
    return ingest_preview_flow.run(raw_id, payload)


@router.post("/{raw_id}/ingest-commit", response_model=IngestCommitResponse)
def ingest_commit(raw_id: str, payload: IngestCommitRequest) -> IngestCommitResponse:
    return ingest_commit_flow.run(raw_id, payload)
