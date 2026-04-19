from datetime import datetime
from pathlib import Path
from typing import Optional

from app.core.enums import InputSourceType


class RawWriterService:
    def __init__(self, vault_root: Path) -> None:
        self.vault_root = vault_root
        self.raw_dir = vault_root / "raw" / "inbox"
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def write_raw_from_import(
        self,
        *,
        source_path: Path,
        detected_type: InputSourceType,
        mime_type: Optional[str],
        extracted_text: str,
        extraction_status: str,
        attachment_path: Optional[str],
    ) -> dict:
        raw_id = self._generate_raw_id()
        raw_filename = f"{raw_id}.md"
        raw_path = self.raw_dir / raw_filename
        title = source_path.stem.replace("_", " ").replace("-", " ").strip() or source_path.name
        imported_at = datetime.now().isoformat(timespec="seconds")

        body = self._build_body(
            source_path=source_path,
            detected_type=detected_type,
            mime_type=mime_type,
            extracted_text=extracted_text,
            extraction_status=extraction_status,
            attachment_path=attachment_path,
        )
        raw_path.write_text(body, encoding="utf-8")

        return {
            "raw_id": raw_id,
            "raw_path": str(raw_path.relative_to(self.vault_root)),
            "title": title,
            "imported_at": imported_at,
        }

    def _generate_raw_id(self) -> str:
        return f"raw_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

    def _build_body(
        self,
        *,
        source_path: Path,
        detected_type: InputSourceType,
        mime_type: Optional[str],
        extracted_text: str,
        extraction_status: str,
        attachment_path: Optional[str],
    ) -> str:
        imported_at = datetime.now().isoformat(timespec="seconds")
        title = source_path.stem.replace("_", " ").replace("-", " ").strip() or source_path.name
        frontmatter = [
            "---",
            f'title: "{self._escape(title)}"',
            f'input_source_type: "{detected_type.value}"',
            f'original_filename: "{self._escape(source_path.name)}"',
            f'mime_type: "{self._escape(mime_type or "application/octet-stream")}"',
            f'imported_at: "{imported_at}"',
            f'source_path: "inbox/{self._escape(source_path.name)}"',
            f'extraction_status: "{extraction_status}"',
            "project_candidate: null",
            "quick_tags: []",
        ]
        if attachment_path:
            frontmatter.append(f'attachment_path: "{self._escape(attachment_path)}"')
        frontmatter.append("---")

        extracted_block = extracted_text.strip() or "(no extracted text available yet)"
        notes = []
        if extraction_status != "full-text":
            notes.append(f"- Extraction status: {extraction_status}")
        if attachment_path:
            notes.append(f"- Attachment stored at: `{attachment_path}`")
        if not notes:
            notes.append("- Imported from inbox")

        return "\n".join(frontmatter) + "\n\n" + f"# {title}\n\n## Extracted Text\n\n{extracted_block}\n\n## Extraction Notes\n\n" + "\n".join(notes) + "\n"

    def _escape(self, value: str) -> str:
        return value.replace('"', '\\"')
