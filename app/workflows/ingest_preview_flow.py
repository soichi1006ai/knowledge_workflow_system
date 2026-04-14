from app.schemas.raw import IngestPreviewRequest, IngestPreviewResponse
from app.services.ingest_service import IngestService


class IngestPreviewFlow:
    def run(self, raw_id: str, payload: IngestPreviewRequest) -> IngestPreviewResponse:
        normalized = IngestService.normalize_source_type("text")
        return IngestPreviewResponse(
            raw_id=raw_id,
            suggested_project_id="prj_kos001",
            candidate_existing_pages=[],
            candidate_new_page_type="topic",
            normalized_canonical_source_type=normalized,
            extracted_summary="This raw note argues for a workflow-first Knowledge OS.",
            extracted_key_points=[
                "Knowledge should connect to decision and action",
                "Markdown should remain the source of truth",
            ],
            extracted_sources=["raw memo"],
            extracted_unresolved_questions=[],
            proposed_decisions=[],
            proposed_actions=[],
            confidence="medium",
        )
