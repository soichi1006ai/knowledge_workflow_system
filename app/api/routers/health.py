from fastapi import APIRouter

from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("", response_model=ApiResponse)
def health_check() -> ApiResponse:
    return ApiResponse(ok=True, message="healthy")
