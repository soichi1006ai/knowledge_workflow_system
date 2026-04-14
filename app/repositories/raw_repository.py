from pathlib import Path

from app.repositories.file_repository import FileRepository


class RawRepository:
    def __init__(self, file_repository: FileRepository) -> None:
        self.file_repository = file_repository

    def list_inbox_paths(self) -> list[str]:
        root = self.file_repository.vault_root / "raw" / "inbox"
        if not root.exists():
            return []
        return [str(path.relative_to(self.file_repository.vault_root)) for path in root.rglob("*.md")]

    def get_raw_text(self, relative_path: str) -> str:
        return self.file_repository.read_text(relative_path)
