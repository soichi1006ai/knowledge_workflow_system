from app.schemas.raw import IngestPreviewRequest, IngestPreviewResponse
from app.services.preview_service import PreviewService


class IngestPreviewFlow:
    def __init__(self) -> None:
        self.preview_service = PreviewService()

    def run(self, raw_id: str, payload: IngestPreviewRequest) -> IngestPreviewResponse:
        return self.preview_service.build_preview(raw_id)
