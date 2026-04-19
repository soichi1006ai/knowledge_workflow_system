from app.schemas.raw import IngestCommitRequest, IngestCommitResponse
from app.services.commit_service import CommitService


class IngestCommitFlow:
    def __init__(self) -> None:
        self.commit_service = CommitService()

    def run(self, raw_id: str, payload: IngestCommitRequest) -> IngestCommitResponse:
        return self.commit_service.commit(raw_id, payload)
