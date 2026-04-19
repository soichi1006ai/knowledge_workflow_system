from pathlib import Path


class FileRepository:
    def __init__(self, vault_root: str) -> None:
        self.vault_root = Path(vault_root)

    def read_text(self, relative_path: str) -> str:
        return (self.vault_root / relative_path).read_text(encoding="utf-8")

    def write_text(self, relative_path: str, content: str) -> None:
        target = self.vault_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def exists(self, relative_path: str) -> bool:
        return (self.vault_root / relative_path).exists()
