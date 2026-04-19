"""Vault内のnon-pageオブジェクト（decision/action/unresolved）を読み込む汎用サービス。"""
from pathlib import Path
from typing import Any, Dict, List

from app.config import settings
from app.services.frontmatter_service import FrontmatterService


class VaultObjectService:
    def __init__(self) -> None:
        self.vault_root = Path(settings.vault_root)
        self.frontmatter_service = FrontmatterService()

    def list_objects(self, relative_dir: str) -> List[Dict[str, Any]]:
        target = self.vault_root / relative_dir
        if not target.exists():
            return []

        items = []
        for md_file in sorted(target.rglob("*.md")):
            try:
                text = md_file.read_text(encoding="utf-8")
            except Exception:
                continue
            fm, body = self.frontmatter_service.split(text)
            if fm.get("archived_at"):
                continue
            fm["_body"] = body.strip()
            items.append(fm)

        return items
