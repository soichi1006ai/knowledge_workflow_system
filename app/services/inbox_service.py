import mimetypes
import shutil
from datetime import datetime
from pathlib import Path

from app.config import settings
from app.core.enums import InputSourceType
from app.schemas.raw import InboxImportItemResult, InboxImportRequest, InboxImportResponse
from app.services.extraction_service import ExtractionService
from app.services.raw_writer_service import RawWriterService


class InboxService:
    def __init__(self) -> None:
        self.vault_root = Path(settings.vault_root)
        self.inbox_dir = self.vault_root / "inbox"
        self.attachments_dir = self.vault_root / "attachments"
        self.imported_dir = self.vault_root / "system" / "imported"
        self.raw_writer = RawWriterService(self.vault_root)
        self.extraction_service = ExtractionService()

    def import_inbox(self, payload: InboxImportRequest) -> InboxImportResponse:
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.attachments_dir.mkdir(parents=True, exist_ok=True)
        self.imported_dir.mkdir(parents=True, exist_ok=True)

        files = [p for p in sorted(self.inbox_dir.iterdir()) if p.is_file()]
        items: list[InboxImportItemResult] = []

        for source_path in files[: payload.limit]:
            items.append(self._import_one(source_path, payload))

        return InboxImportResponse(ok=True, message=f"imported {len(items)} files", items=items)

    def _import_one(self, source_path: Path, payload: InboxImportRequest) -> InboxImportItemResult:
        detected_type = self._detect_type(source_path)
        mime_type = mimetypes.guess_type(source_path.name)[0]
        warnings: list[str] = []

        extracted_text, extraction_status = self.extraction_service.extract(source_path, detected_type)
        if extraction_status != "full-text":
            warnings.append(f"extraction_status={extraction_status}")

        attachment_path = None
        if detected_type not in {InputSourceType.TEXT, InputSourceType.MARKDOWN, InputSourceType.CSV, InputSourceType.JSON}:
            attachment_path = self._store_attachment(source_path)

        raw_record = self.raw_writer.write_raw_from_import(
            source_path=source_path,
            detected_type=detected_type,
            mime_type=mime_type,
            extracted_text=extracted_text,
            extraction_status=extraction_status,
            attachment_path=attachment_path,
        )

        self._archive_source(source_path, payload)

        return InboxImportItemResult(
            filename=source_path.name,
            detected_type=detected_type,
            mime_type=mime_type,
            raw_id=raw_record["raw_id"],
            raw_path=raw_record["raw_path"],
            attachment_path=attachment_path,
            extraction_status=extraction_status,
            warnings=warnings,
        )

    def _detect_type(self, source_path: Path) -> InputSourceType:
        ext = source_path.suffix.lower()
        mapping = {
            ".txt": InputSourceType.TEXT,
            ".md": InputSourceType.MARKDOWN,
            ".pdf": InputSourceType.PDF,
            ".docx": InputSourceType.DOCX,
            ".csv": InputSourceType.CSV,
            ".json": InputSourceType.JSON,
            ".xlsx": InputSourceType.SPREADSHEET,
            ".xls": InputSourceType.SPREADSHEET,
            ".png": InputSourceType.IMAGE,
            ".jpg": InputSourceType.IMAGE,
            ".jpeg": InputSourceType.IMAGE,
            ".webp": InputSourceType.IMAGE,
            ".gif": InputSourceType.IMAGE,
            ".mp4": InputSourceType.VIDEO,
            ".mov": InputSourceType.VIDEO,
            ".m4v": InputSourceType.VIDEO,
        }
        return mapping.get(ext, InputSourceType.ATTACHMENT_NOTE)

    def _store_attachment(self, source_path: Path) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_name = f"{timestamp}_{source_path.name}"
        target_path = self.attachments_dir / target_name
        shutil.copy2(source_path, target_path)
        return str(target_path.relative_to(self.vault_root))

    def _archive_source(self, source_path: Path, payload: InboxImportRequest) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived_path = self.imported_dir / f"{timestamp}_{source_path.name}"
        if payload.delete_from_inbox:
            shutil.move(str(source_path), archived_path)
            return
        shutil.copy2(source_path, archived_path)
