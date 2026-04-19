from datetime import datetime
from typing import Dict

from app.config import settings
from app.repositories.file_repository import FileRepository
from app.repositories.raw_repository import RawRepository
from app.schemas.raw import IngestCommitRequest, IngestCommitResponse
from app.services.frontmatter_service import FrontmatterService


class CommitService:
    def __init__(self) -> None:
        self.file_repository = FileRepository(settings.vault_root)
        self.raw_repository = RawRepository(self.file_repository)
        self.frontmatter_service = FrontmatterService()

    def commit(self, raw_id: str, payload: IngestCommitRequest) -> IngestCommitResponse:
        raw_path = self._find_raw_path(raw_id)
        raw_text = self.raw_repository.get_raw_text(raw_path)
        frontmatter, body = self.frontmatter_service.split(raw_text)

        title = payload.approved_page_title or frontmatter.get("title") or raw_id
        page_type = payload.approved_page_type or self._infer_page_type(frontmatter, body)
        project_id = payload.approved_project_id or frontmatter.get("project_candidate") or "prj_kos001"
        source_id = self._generate_source_id(raw_id)
        page_id = self._generate_page_id(raw_id)
        target_relative_path = payload.existing_page_path or self._target_page_path(page_type, title)
        page_exists = self.file_repository.exists(target_relative_path)

        if page_exists:
            page_content = self._merge_into_existing_page(
                relative_path=target_relative_path,
                source_id=source_id,
                body=body,
            )
        else:
            page_content = self._build_page_content(
                page_id=page_id,
                title=title,
                page_type=page_type,
                project_id=project_id,
                source_id=source_id,
                body=body,
            )
        source_path = f"system/sources/{source_id}.md"
        source_content = self._build_source_content(
            source_id=source_id,
            raw_id=raw_id,
            title=title,
            frontmatter=frontmatter,
        )
        created_decision_ids: list[str] = []
        created_action_ids: list[str] = []
        created_question_ids: list[str] = []

        if payload.create_decisions:
            decision_id = self._generate_decision_id(raw_id)
            decision_path = f"decisions/active/{decision_id}.md"
            decision_content = self._build_decision_content(
                decision_id=decision_id,
                title=title,
                project_id=project_id,
                page_ref=target_relative_path,
                source_id=source_id,
            )
            self.file_repository.write_text(decision_path, decision_content)
            created_decision_ids.append(decision_id)

        if payload.create_actions:
            action_id = self._generate_action_id(raw_id)
            action_path = f"actions/open/{action_id}.md"
            linked_decision_id = created_decision_ids[0] if created_decision_ids else ""
            action_content = self._build_action_content(
                action_id=action_id,
                title=title,
                project_id=project_id,
                page_ref=target_relative_path,
                linked_decision_id=linked_decision_id,
            )
            self.file_repository.write_text(action_path, action_content)
            created_action_ids.append(action_id)

        unresolved_question = self._first_question(body)
        if unresolved_question:
            question_id = self._generate_question_id(raw_id)
            question_path = f"unresolved/active/{question_id}.md"
            question_content = self._build_unresolved_content(
                question_id=question_id,
                question=unresolved_question,
                project_id=project_id,
                page_ref=target_relative_path,
                source_id=source_id,
            )
            self.file_repository.write_text(question_path, question_content)
            created_question_ids.append(question_id)

        self.file_repository.write_text(target_relative_path, page_content)
        self.file_repository.write_text(source_path, source_content)

        return IngestCommitResponse(
            raw_id=raw_id,
            source_id=source_id,
            created_page_ids=[] if page_exists else [page_id],
            updated_page_ids=[target_relative_path] if page_exists else [],
            created_decision_ids=created_decision_ids,
            created_question_ids=created_question_ids,
            created_action_ids=created_action_ids,
            message=(
                f"ingest merged into {target_relative_path}"
                if page_exists
                else f"ingest committed to {target_relative_path}"
            ),
        )

    def _find_raw_path(self, raw_id: str) -> str:
        for path in self.raw_repository.list_inbox_paths():
            if path.endswith(f"{raw_id}.md"):
                return path
        raise FileNotFoundError(f"raw not found: {raw_id}")

    def _infer_page_type(self, frontmatter: Dict[str, str], body: str) -> str:
        title = (frontmatter.get("title") or "").lower()
        text = body.lower()
        if "project" in title or "project" in text:
            return "project"
        if "system" in title or "workflow" in text or "knowledge" in text:
            return "concept"
        return "topic"

    def _target_page_path(self, page_type: str, title: str) -> str:
        folder_map = {
            "concept": "wiki/concepts",
            "project": "wiki/projects",
            "topic": "wiki/topics",
            "entity": "wiki/entities",
            "source-summary": "wiki/source-summaries",
        }
        folder = folder_map.get(page_type, "wiki/topics")
        slug = self._slugify(title)
        return f"{folder}/{slug}.md"

    def _build_page_content(
        self,
        *,
        page_id: str,
        title: str,
        page_type: str,
        project_id: str,
        source_id: str,
        body: str,
    ) -> str:
        created_at = datetime.now().date().isoformat()
        summary = self._extract_section(body, "## Extracted Text")
        cleaned_summary = "\n".join(line for line in summary.splitlines() if line.strip()).strip()
        if not cleaned_summary:
            cleaned_summary = "Imported from raw inbox item."

        return (
            "---\n"
            f'page_id: {page_id}\n'
            f'title: "{self._escape(title)}"\n'
            f'type: {page_type}\n'
            "status: draft\n"
            "page_confidence: medium\n"
            f'linked_project_id: {project_id}\n'
            "source_ids:\n"
            f" - {source_id}\n"
            "related_page_ids: []\n"
            "linked_decision_ids: []\n"
            "linked_action_ids: []\n"
            "linked_question_ids: []\n"
            f"created_at: {created_at}\n"
            f"updated_at: {created_at}\n"
            "review_due: \n"
            "archived_at: \n"
            "---\n\n"
            f"# {title}\n\n"
            "## Summary\n"
            f"{cleaned_summary}\n\n"
            "## Source Raw\n"
            f"Imported from raw inbox item.\n"
        )

    def _build_source_content(
        self,
        *,
        source_id: str,
        raw_id: str,
        title: str,
        frontmatter: Dict[str, str],
    ) -> str:
        imported_at = datetime.now().date().isoformat()
        canonical_source_type = self._canonical_source_type(frontmatter.get("input_source_type", "text"))
        original_filename = frontmatter.get("original_filename") or title
        return (
            "---\n"
            f"source_id: {source_id}\n"
            f"canonical_source_type: {canonical_source_type}\n"
            f'title: "{self._escape(title)}"\n'
            f"raw_ref: {raw_id}\n"
            "url: \n"
            f"captured_at: {imported_at}\n"
            f"imported_at: {imported_at}\n"
            "reliability_hint: medium\n"
            f'original_filename: "{self._escape(original_filename)}"\n'
            "---\n\n"
            "# Source\n\n"
            f"Imported from raw inbox item `{raw_id}`.\n"
        )

    def _merge_into_existing_page(self, *, relative_path: str, source_id: str, body: str) -> str:
        existing = self.file_repository.read_text(relative_path)
        frontmatter, existing_body = self.frontmatter_service.split(existing)
        source_ids = self._parse_list_block(existing, "source_ids")
        if source_id not in source_ids:
            source_ids.append(source_id)

        updated_at = datetime.now().date().isoformat()
        summary_addition = self._extract_section(body, "## Extracted Text")
        merged_summary = "\n".join(line for line in summary_addition.splitlines() if line.strip()).strip()

        title = frontmatter.get("title") or relative_path.split("/")[-1].replace(".md", "")
        page_id = frontmatter.get("page_id") or self._slugify(title)
        page_type = frontmatter.get("type") or "topic"
        status = frontmatter.get("status") or "draft"
        page_confidence = frontmatter.get("page_confidence") or "medium"
        linked_project_id = frontmatter.get("linked_project_id") or "prj_kos001"
        created_at = frontmatter.get("created_at") or updated_at
        review_due = frontmatter.get("review_due") or ""
        archived_at = frontmatter.get("archived_at") or ""

        merged_body = existing_body.strip()
        if merged_summary:
            merged_body += (
                "\n\n## Imported Updates\n"
                f"- {updated_at}: imported new supporting raw content.\n\n"
                f"{merged_summary}\n"
            )

        source_lines = "\n".join(f" - {item}" for item in source_ids) or " []"

        return (
            "---\n"
            f"page_id: {page_id}\n"
            f'title: "{self._escape(title)}"\n'
            f"type: {page_type}\n"
            f"status: {status}\n"
            f"page_confidence: {page_confidence}\n"
            f"linked_project_id: {linked_project_id}\n"
            "source_ids:\n"
            f"{source_lines}\n"
            f"related_page_ids: {frontmatter.get('related_page_ids', '[]')}\n"
            f"linked_decision_ids: {frontmatter.get('linked_decision_ids', '[]')}\n"
            f"linked_action_ids: {frontmatter.get('linked_action_ids', '[]')}\n"
            f"linked_question_ids: {frontmatter.get('linked_question_ids', '[]')}\n"
            f"created_at: {created_at}\n"
            f"updated_at: {updated_at}\n"
            f"review_due: {review_due}\n"
            f"archived_at: {archived_at}\n"
            "---\n\n"
            f"{merged_body.strip()}\n"
        )

    def _extract_section(self, body: str, heading: str) -> str:
        if heading not in body:
            return body.strip()
        _, remainder = body.split(heading, 1)
        next_heading = remainder.split("\n## ", 1)
        return next_heading[0].strip()

    def _build_decision_content(
        self,
        *,
        decision_id: str,
        title: str,
        project_id: str,
        page_ref: str,
        source_id: str,
    ) -> str:
        today = datetime.now().date().isoformat()
        return (
            "---\n"
            f"decision_id: {decision_id}\n"
            f'title: "Review and absorb {self._escape(title)}"\n'
            "status: draft\n"
            f"linked_project_id: {project_id}\n"
            "linked_page_ids:\n"
            f" - {page_ref}\n"
            "linked_source_ids:\n"
            f" - {source_id}\n"
            "linked_action_ids: []\n"
            f"created_at: {today}\n"
            "confirmed_at: \n"
            "supersedes_decision_id: \n"
            "archived_at: \n"
            "---\n\n"
            "# Decision\n\n"
            "Decide whether the imported content should materially change current knowledge or remain supporting evidence.\n"
        )

    def _build_action_content(
        self,
        *,
        action_id: str,
        title: str,
        project_id: str,
        page_ref: str,
        linked_decision_id: str,
    ) -> str:
        today = datetime.now().date().isoformat()
        return (
            "---\n"
            f"action_id: {action_id}\n"
            f'title: "Process imported content for {self._escape(title)}"\n'
            "status: open\n"
            "priority: medium\n"
            "owner: Master S\n"
            "due_date: \n"
            f"linked_project_id: {project_id}\n"
            f"linked_decision_id: {linked_decision_id}\n"
            "linked_page_ids:\n"
            f" - {page_ref}\n"
            f"created_at: {today}\n"
            "completed_at: \n"
            "archived_at: \n"
            "---\n\n"
            "# Action\n\n"
            "Review the imported raw, validate its relevance, and decide whether additional edits are required.\n"
        )

    def _build_unresolved_content(
        self,
        *,
        question_id: str,
        question: str,
        project_id: str,
        page_ref: str,
        source_id: str,
    ) -> str:
        today = datetime.now().date().isoformat()
        return (
            "---\n"
            f"question_id: {question_id}\n"
            f'title: "{self._escape(question)}"\n'
            f'question: "{self._escape(question)}"\n'
            "status: open\n"
            "priority: medium\n"
            f"linked_project_id: {project_id}\n"
            "linked_page_ids:\n"
            f" - {page_ref}\n"
            "linked_source_ids:\n"
            f" - {source_id}\n"
            f"created_at: {today}\n"
            "resolved_at: \n"
            "archived_at: \n"
            "---\n\n"
            "# Unresolved Question\n\n"
            "## Why Unresolved\n"
            "The imported content raises a question that should be tracked explicitly.\n\n"
            "## Next Step\n"
            "Review this question during the next ingest or synthesis pass.\n"
        )

    def _first_question(self, body: str) -> str:
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.endswith("?"):
                return stripped
        return ""

    def _parse_list_block(self, text: str, field_name: str) -> list[str]:
        lines = text.splitlines()
        items: list[str] = []
        inside = False
        for line in lines:
            if line.startswith(f"{field_name}:"):
                inside = True
                continue
            if inside:
                if line.startswith(" - "):
                    items.append(line.replace(" - ", "", 1).strip())
                    continue
                if line.startswith(" "):
                    continue
                break
        return items

    def _generate_source_id(self, raw_id: str) -> str:
        return raw_id.replace("raw_", "src_")

    def _generate_decision_id(self, raw_id: str) -> str:
        return raw_id.replace("raw_", "dec_")

    def _generate_action_id(self, raw_id: str) -> str:
        return raw_id.replace("raw_", "act_")

    def _generate_question_id(self, raw_id: str) -> str:
        return raw_id.replace("raw_", "uq_")

    def _canonical_source_type(self, input_source_type: str) -> str:
        if input_source_type in {"text", "markdown"}:
            return "raw-note"
        if input_source_type == "url":
            return "url"
        return "attachment-note"

    def _generate_page_id(self, raw_id: str) -> str:
        return raw_id.replace("raw_", "pg_")

    def _slugify(self, value: str) -> str:
        lowered = value.lower().strip()
        normalized = "".join(ch if ch.isalnum() else "-" for ch in lowered)
        while "--" in normalized:
            normalized = normalized.replace("--", "-")
        return normalized.strip("-") or "untitled"

    def _escape(self, value: str) -> str:
        return value.replace('"', '\\"')
