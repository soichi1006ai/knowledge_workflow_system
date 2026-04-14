from app.core.enums import CanonicalSourceType, InputSourceType


class IngestService:
    @staticmethod
    def normalize_source_type(input_source_type: InputSourceType | str) -> CanonicalSourceType:
        mapping = {
            InputSourceType.TEXT: CanonicalSourceType.RAW_NOTE,
            InputSourceType.MARKDOWN: CanonicalSourceType.RAW_NOTE,
            InputSourceType.URL: CanonicalSourceType.URL,
            InputSourceType.ATTACHMENT_NOTE: CanonicalSourceType.ATTACHMENT_NOTE,
            InputSourceType.CONVERSATION_SUMMARY: CanonicalSourceType.CONVERSATION_SUMMARY,
            InputSourceType.HYPOTHESIS: CanonicalSourceType.HYPOTHESIS,
        }
        key = InputSourceType(input_source_type) if isinstance(input_source_type, str) else input_source_type
        return mapping[key]
