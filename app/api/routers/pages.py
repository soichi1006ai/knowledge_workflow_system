from fastapi import APIRouter

from app.schemas.page import PageDetailResponse, PageListResponse

router = APIRouter(prefix="/api/pages", tags=["pages"])


@router.get("", response_model=PageListResponse)
def list_pages() -> PageListResponse:
    return PageListResponse(items=[])


@router.get("/{page_id}", response_model=PageDetailResponse)
def get_page(page_id: str) -> PageDetailResponse:
    return PageDetailResponse(item={"page_id": page_id, "title": "stub"})
