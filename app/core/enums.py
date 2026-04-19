from enum import Enum


class PageType(str, Enum):
    CONCEPT = "concept"
    ENTITY = "entity"
    TOPIC = "topic"
    PROJECT = "project"
    SOURCE_SUMMARY = "source-summary"


class PageStatus(str, Enum):
    DRAFT = "draft"
    NEEDS_REVIEW = "needs-review"
    STABLE = "stable"


class PageConfidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class InputSourceType(str, Enum):
    TEXT = "text"
    MARKDOWN = "markdown"
    PDF = "pdf"
    DOCX = "docx"
    CSV = "csv"
    JSON = "json"
    IMAGE = "image"
    VIDEO = "video"
    SPREADSHEET = "spreadsheet"
    URL = "url"
    ATTACHMENT_NOTE = "attachment-note"
    CONVERSATION_SUMMARY = "conversation-summary"
    HYPOTHESIS = "hypothesis"


class CanonicalSourceType(str, Enum):
    RAW_NOTE = "raw-note"
    URL = "url"
    ATTACHMENT_NOTE = "attachment-note"
    CONVERSATION_SUMMARY = "conversation-summary"
    HYPOTHESIS = "hypothesis"
    DERIVED_SUMMARY = "derived-summary"


class QueryMode(str, Enum):
    SUMMARIZE = "summarize"
    COMPARE = "compare"
    EVALUATE = "evaluate"
    RECOMMEND = "recommend"
    DECIDE = "decide"
    EXTRACT_ACTIONS = "extract-actions"
    FIND_GAPS = "find-gaps"
