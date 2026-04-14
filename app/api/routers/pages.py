from fastapi import APIRouter

from app.core.enums import PageConfidence, PageStatus, PageType
from app.schemas.page import PageDetailResponse, PageDocument, PageListResponse, PageSummary

router = APIRouter(prefix="/api/pages", tags=["pages"])


@router.get("", response_model=PageListResponse)
def list_pages() -> PageListResponse:
    return PageListResponse(
        items=[
            PageSummary(
                page_id="pg_kos001",
                title="Knowledge OS",
                type=PageType.CONCEPT,
                status=PageStatus.STABLE,
                page_confidence=PageConfidence.HIGH,
                linked_project_id="prj_kos001",
                updated_at="2026-04-14",
                review_due="2026-05-14",
            )
        ]
    )


@router.get("/{page_id}", response_model=PageDetailResponse)
def get_page(page_id: str) -> PageDetailResponse:
    return PageDetailResponse(
        item=PageDocument(
            frontmatter={
                "page_id": page_id,
                "title": "Knowledge OS",
                "type": "concept",
                "status": "stable",
            },
            body="# Knowledge OS\n\nA Markdown-based AI-native system.",
        )
    )
