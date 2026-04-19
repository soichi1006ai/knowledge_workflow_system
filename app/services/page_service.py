from app.config import settings
from app.repositories.file_repository import FileRepository
from app.repositories.page_repository import PageRepository
from app.schemas.page import PageDocument, PageSummary
from app.services.frontmatter_service import FrontmatterService


class PageService:
    def __init__(self) -> None:
        self.file_repository = FileRepository(settings.vault_root)
        self.page_repository = PageRepository(self.file_repository)
        self.frontmatter_service = FrontmatterService()

    def list_pages(self) -> list[PageSummary]:
        paths = self.page_repository.list_page_paths()
        items: list[PageSummary] = []
        for path in paths:
            try:
                text = self.file_repository.read_text(path)
            except Exception:
                continue

            fm, _ = self.frontmatter_service.split(text)
            if fm.get("archived_at"):
                continue

            page_id = str(fm.get("page_id", path))
            title = str(fm.get("title", path.split("/")[-1].replace(".md", "")))
            page_type = str(fm.get("type", "topic"))
            status = str(fm.get("status", "draft"))
            confidence = str(fm.get("page_confidence", "medium"))

            try:
                items.append(
                    PageSummary(
                        page_id=page_id,
                        title=title,
                        type=page_type,  # type: ignore[arg-type]
                        status=status,  # type: ignore[arg-type]
                        page_confidence=confidence,  # type: ignore[arg-type]
                        linked_project_id=fm.get("linked_project_id") or None,
                        updated_at=fm.get("updated_at") or None,
                        review_due=fm.get("review_due") or None,
                    )
                )
            except Exception:
                continue

        return items

    def get_page(self, page_id: str) -> PageDocument:
        paths = self.page_repository.list_page_paths()
        for path in paths:
            try:
                text = self.file_repository.read_text(path)
            except Exception:
                continue
            fm, body = self.frontmatter_service.split(text)
            if str(fm.get("page_id", "")) == page_id or path == page_id:
                return PageDocument(frontmatter=fm, body=body)

        return PageDocument(frontmatter={"page_id": page_id, "error": "not found"}, body="")
