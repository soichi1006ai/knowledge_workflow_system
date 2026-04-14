from fastapi import APIRouter

from app.schemas.review import ReviewCandidate, ReviewCandidatesResponse, ReviewHistoryItem, ReviewHistoryResponse
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.get("/candidates", response_model=ReviewCandidatesResponse)
def review_candidates() -> ReviewCandidatesResponse:
    return ReviewCandidatesResponse(
        items=[
            ReviewCandidate(
                review_candidate_id="revc_pg_kos001",
                target_page_id="pg_kos001",
                review_reason="initial sample review",
                detected_at="2026-04-14",
                suggested_action="keep",
            )
        ]
    )


@router.get("/history", response_model=ReviewHistoryResponse)
def review_history() -> ReviewHistoryResponse:
    return ReviewHistoryResponse(
        items=[
            ReviewHistoryItem(
                review_record_id="rev_pg_mvp001_20260414",
                target_page_id="pg_kos001",
                action_taken="update",
                reviewed_at="2026-04-14",
                reviewer="Master S",
            )
        ]
    )


@router.post("/{review_candidate_id}/apply", response_model=ApiResponse)
def apply_review(review_candidate_id: str) -> ApiResponse:
    return ApiResponse(message=f"review {review_candidate_id} applied (stub)")
