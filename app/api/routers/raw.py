from fastapi import APIRouter

from app.schemas.raw import (
    IngestPreviewRequest,
    IngestPreviewResponse,
    RawCreateRequest,
    RawCreateResponse,
)

router = APIRouter(prefix="/api/raw", tags=["raw"])


@router.post("", response_model=RawCreateResponse)
def create_raw(payload: RawCreateRequest) -> RawCreateResponse:
    return RawCreateResponse(raw_id="raw_demo001", message="stub")


@router.post("/{raw_id}/ingest-preview", response_model=IngestPreviewResponse)
def ingest_preview(raw_id: str, payload: IngestPreviewRequest) -> IngestPreviewResponse:
    return IngestPreviewResponse(
        raw_id=raw_id,
        extracted_summary="stub preview",
        extracted_key_points=["stub point"],
    )
