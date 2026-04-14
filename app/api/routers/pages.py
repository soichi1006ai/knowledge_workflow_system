from fastapi import APIRouter

from app.schemas.page import PageDetailResponse, PageListResponse
from app.services.page_service import PageService

router = APIRouter(prefix="/api/pages", tags=["pages"])
service = PageService()


@router.get("", response_model=PageListResponse)
def list_pages() -> PageListResponse:
    return PageListResponse(items=service.list_pages())


@router.get("/{page_id}", response_model=PageDetailResponse)
def get_page(page_id: str) -> PageDetailResponse:
    return PageDetailResponse(item=service.get_page(page_id))
