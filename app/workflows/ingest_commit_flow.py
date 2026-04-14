from app.schemas.raw import IngestCommitRequest, IngestCommitResponse


class IngestCommitFlow:
    def run(self, raw_id: str, payload: IngestCommitRequest) -> IngestCommitResponse:
        return IngestCommitResponse(
            raw_id=raw_id,
            source_id="src_generated001",
            created_page_ids=["pg_generated001"],
            updated_page_ids=[],
            created_decision_ids=[],
            created_question_ids=[],
            created_action_ids=[],
            message="ingest committed (stub)",
        )
