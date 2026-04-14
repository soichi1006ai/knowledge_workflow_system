from fastapi import APIRouter

from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
service = DashboardService()


@router.get("", response_model=DashboardResponse)
def get_dashboard() -> DashboardResponse:
    return service.get_dashboard()
