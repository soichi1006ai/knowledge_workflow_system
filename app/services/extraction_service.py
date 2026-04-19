from pathlib import Path
from typing import Optional, Tuple

from app.core.enums import InputSourceType


class ExtractionService:
    def extract(self, source_path: Path, detected_type: InputSourceType) -> Tuple[str, str]:
        if detected_type in {InputSourceType.TEXT, InputSourceType.MARKDOWN, InputSourceType.CSV, InputSourceType.JSON}:
            return self._extract_text_file(source_path)

        if detected_type == InputSourceType.PDF:
            return self._extract_pdf(source_path)

        if detected_type == InputSourceType.DOCX:
            return self._extract_docx(source_path)

        if detected_type == InputSourceType.SPREADSHEET:
            return "", "needs-extraction"

        if detected_type in {InputSourceType.IMAGE, InputSourceType.VIDEO, InputSourceType.ATTACHMENT_NOTE}:
            return "", "metadata-only"

        return "", "metadata-only"

    def _extract_text_file(self, source_path: Path) -> Tuple[str, str]:
        try:
            return source_path.read_text(encoding="utf-8"), "full-text"
        except UnicodeDecodeError:
            return source_path.read_text(encoding="utf-8", errors="replace"), "full-text-lossy"

    def _extract_pdf(self, source_path: Path) -> Tuple[str, str]:
        try:
            from pypdf import PdfReader
        except Exception:
            return "", "needs-extraction"

        try:
            reader = PdfReader(str(source_path))
            texts = []
            for page in reader.pages:
                texts.append(page.extract_text() or "")
            joined = "\n\n".join(t.strip() for t in texts if t and t.strip()).strip()
            if joined:
                return joined, "full-text"
            return "", "metadata-only"
        except Exception:
            return "", "needs-extraction"

    def _extract_docx(self, source_path: Path) -> Tuple[str, str]:
        try:
            import docx
        except Exception:
            return "", "needs-extraction"

        try:
            document = docx.Document(str(source_path))
            paragraphs = [p.text.strip() for p in document.paragraphs if p.text and p.text.strip()]
            joined = "\n\n".join(paragraphs).strip()
            if joined:
                return joined, "full-text"
            return "", "metadata-only"
        except Exception:
            return "", "needs-extraction"
