from app.config import settings
from app.repositories.file_repository import FileRepository
from app.repositories.page_repository import PageRepository
from app.schemas.page import PageDocument, PageSummary


class PageService:
    def __init__(self) -> None:
        self.file_repository = FileRepository(settings.vault_root)
        self.page_repository = PageRepository(self.file_repository)

    def list_pages(self) -> list[PageSummary]:
        paths = self.page_repository.list_page_paths()
        items: list[PageSummary] = []
        for path in paths[:20]:
            title = path.split("/")[-1].replace(".md", "").replace("-", " ").title()
            items.append(
                PageSummary(
                    page_id=path,
                    title=title,
                    type="topic",
                    status="stable",
                    page_confidence="medium",
                    updated_at="2026-04-14",
                )
            )
        return items

    def get_page(self, page_id: str) -> PageDocument:
        return PageDocument(
            frontmatter={
                "page_id": page_id,
                "title": "Knowledge OS",
                "type": "concept",
                "status": "stable",
            },
            body="# Knowledge OS\n\nA Markdown-based AI-native system.",
        )
