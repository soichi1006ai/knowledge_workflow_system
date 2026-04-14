from pydantic import Field

from app.schemas.common import ApiResponse, KOSBaseModel


class DashboardBucketItem(KOSBaseModel):
    id: str
    title: str
    item_type: str
    priority: str | None = None
    linked_project_id: str | None = None
    note: str | None = None


class DashboardData(KOSBaseModel):
    overdue_actions: list[DashboardBucketItem] = Field(default_factory=list)
    pending_decisions: list[DashboardBucketItem] = Field(default_factory=list)
    high_priority_unresolved_questions: list[DashboardBucketItem] = Field(default_factory=list)
    stale_stable_pages: list[DashboardBucketItem] = Field(default_factory=list)


class DashboardResponse(ApiResponse):
    data: DashboardData
