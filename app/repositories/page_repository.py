from pathlib import Path

from app.repositories.file_repository import FileRepository


class PageRepository:
    def __init__(self, file_repository: FileRepository) -> None:
        self.file_repository = file_repository

    def list_page_paths(self) -> list[str]:
        root = self.file_repository.vault_root / "wiki"
        if not root.exists():
            return []
        return [str(path.relative_to(self.file_repository.vault_root)) for path in root.rglob("*.md")]

    def get_page_text(self, relative_path: str) -> str:
        return self.file_repository.read_text(relative_path)
