from typing import Union

from app.core.enums import CanonicalSourceType, InputSourceType


class IngestService:
    @staticmethod
    def normalize_source_type(input_source_type: Union[InputSourceType, str]) -> CanonicalSourceType:
        mapping = {
            InputSourceType.TEXT: CanonicalSourceType.RAW_NOTE,
            InputSourceType.MARKDOWN: CanonicalSourceType.RAW_NOTE,
            InputSourceType.PDF: CanonicalSourceType.ATTACHMENT_NOTE,
            InputSourceType.DOCX: CanonicalSourceType.ATTACHMENT_NOTE,
            InputSourceType.CSV: CanonicalSourceType.ATTACHMENT_NOTE,
            InputSourceType.JSON: CanonicalSourceType.ATTACHMENT_NOTE,
            InputSourceType.IMAGE: CanonicalSourceType.ATTACHMENT_NOTE,
            InputSourceType.VIDEO: CanonicalSourceType.ATTACHMENT_NOTE,
            InputSourceType.SPREADSHEET: CanonicalSourceType.ATTACHMENT_NOTE,
            InputSourceType.URL: CanonicalSourceType.URL,
            InputSourceType.ATTACHMENT_NOTE: CanonicalSourceType.ATTACHMENT_NOTE,
            InputSourceType.CONVERSATION_SUMMARY: CanonicalSourceType.CONVERSATION_SUMMARY,
            InputSourceType.HYPOTHESIS: CanonicalSourceType.HYPOTHESIS,
        }
        key = InputSourceType(input_source_type) if isinstance(input_source_type, str) else input_source_type
        return mapping[key]
