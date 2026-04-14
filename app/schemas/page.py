from app.schemas.common import ApiResponse, KOSBaseModel


class PageDetailResponse(ApiResponse):
    item: dict


class PageListResponse(ApiResponse):
    items: list[dict] = []
