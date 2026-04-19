from typing import Optional

from pydantic import Field

from app.schemas.common import ApiResponse, KOSBaseModel


class ReviewCandidate(KOSBaseModel):
    review_candidate_id: str
    target_page_id: str
    review_reason: str
    stale_reason: Optional[str] = None
    detected_at: str
    suggested_action: Optional[str] = None


class ReviewHistoryItem(KOSBaseModel):
    review_record_id: str
    target_page_id: str
    action_taken: str
    reviewed_at: str
    reviewer: str


class ReviewCandidatesResponse(ApiResponse):
    items: list[ReviewCandidate] = Field(default_factory=list)


class ReviewHistoryResponse(ApiResponse):
    items: list[ReviewHistoryItem] = Field(default_factory=list)
