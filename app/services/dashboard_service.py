from app.schemas.dashboard import DashboardBucketItem, DashboardData, DashboardResponse


class DashboardService:
    def get_dashboard(self) -> DashboardResponse:
        return DashboardResponse(
            data=DashboardData(
                overdue_actions=[
                    DashboardBucketItem(
                        id="act_kos001",
                        title="Implement initial raw -> query workflow",
                        item_type="action",
                        priority="high",
                        linked_project_id="prj_kos001",
                    )
                ],
                pending_decisions=[
                    DashboardBucketItem(
                        id="dec_kos002",
                        title="Separate Page objects from Non-page objects",
                        item_type="decision",
                        priority="high",
                        linked_project_id="prj_kos001",
                    )
                ],
                high_priority_unresolved_questions=[
                    DashboardBucketItem(
                        id="uq_kos001",
                        title="What is the smallest lovable dashboard for daily use?",
                        item_type="unresolved",
                        priority="high",
                        linked_project_id="prj_kos001",
                    )
                ],
                stale_stable_pages=[
                    DashboardBucketItem(
                        id="pg_kos001",
                        title="Knowledge OS",
                        item_type="page",
                        priority="medium",
                        linked_project_id="prj_kos001",
                    )
                ],
            )
        )
