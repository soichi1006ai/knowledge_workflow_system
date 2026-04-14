from datetime import date

from app.schemas.raw import RawCreateRequest, RawCreateResponse, RawListItem, RawListResponse


class RawService:
    def list_raw(self) -> RawListResponse:
        return RawListResponse(
            items=[
                RawListItem(
                    raw_id="raw_kos001",
                    title="Knowledge OS direction memo",
                    input_source_type="text",
                    project_candidate="prj_kos001",
                    created_at=date(2026, 4, 14),
                    imported_at=None,
                )
            ]
        )

    def create_raw(self, payload: RawCreateRequest) -> RawCreateResponse:
        return RawCreateResponse(raw_id="raw_demo001", message="raw created (stub)")
