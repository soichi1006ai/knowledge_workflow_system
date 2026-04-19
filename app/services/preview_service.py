from typing import List

from app.config import settings
from app.repositories.file_repository import FileRepository
from app.repositories.page_repository import PageRepository
from app.repositories.raw_repository import RawRepository
from app.schemas.raw import IngestPreviewResponse
from app.services.frontmatter_service import FrontmatterService
from app.services.ingest_service import IngestService


class PreviewService:
    def __init__(self) -> None:
        self.file_repository = FileRepository(settings.vault_root)
        self.raw_repository = RawRepository(self.file_repository)
        self.page_repository = PageRepository(self.file_repository)
        self.frontmatter_service = FrontmatterService()

    def build_preview(self, raw_id: str) -> IngestPreviewResponse:
        relative_path = self._find_raw_path(raw_id)
        raw_text = self.raw_repository.get_raw_text(relative_path)
        frontmatter, body = self.frontmatter_service.split(raw_text)
        input_source_type = frontmatter.get("input_source_type", "text")
        normalized = IngestService.normalize_source_type(input_source_type)

        extracted_text = self._extract_section(body, "## Extracted Text")
        summary = self._summarize(extracted_text)
        key_points = self._key_points(extracted_text)
        candidate_existing_pages = self._candidate_existing_pages(key_points)
        page_type = self._suggest_page_type(key_points, frontmatter)
        proposed_actions = self._proposed_actions(extracted_text)
        unresolved = self._unresolved_questions(extracted_text)

        return IngestPreviewResponse(
            raw_id=raw_id,
            suggested_project_id=frontmatter.get("project_candidate") or "prj_kos001",
            candidate_existing_pages=candidate_existing_pages,
            candidate_new_page_type=page_type,
            normalized_canonical_source_type=normalized,
            extracted_summary=summary,
            extracted_key_points=key_points,
            extracted_sources=[frontmatter.get("original_filename") or raw_id],
            extracted_unresolved_questions=unresolved,
            proposed_decisions=[],
            proposed_actions=proposed_actions,
            confidence="medium" if key_points else "low",
        )

    def _find_raw_path(self, raw_id: str) -> str:
        for path in self.raw_repository.list_inbox_paths():
            if path.endswith(f"{raw_id}.md"):
                return path
        raise FileNotFoundError(f"raw not found: {raw_id}")

    def _extract_section(self, body: str, heading: str) -> str:
        if heading not in body:
            return body.strip()
        _, remainder = body.split(heading, 1)
        next_heading = remainder.split("\n## ", 1)
        return next_heading[0].strip()

    def _summarize(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return " ".join(lines[:2])[:280]

    def _key_points(self, text: str) -> List[str]:
        points: List[str] = []
        for line in text.splitlines():
            cleaned = line.strip("-• \t")
            if cleaned:
                points.append(cleaned)
            if len(points) >= 5:
                break
        return points

    def _candidate_existing_pages(self, key_points: List[str]) -> list[dict]:
        page_paths = self.page_repository.list_page_paths()[:20]
        candidates: list[dict] = []
        joined = " ".join(key_points).lower()
        for path in page_paths:
            title = path.split("/")[-1].replace(".md", "").replace("-", " ")
            score = 0
            for token in title.lower().split():
                if token and token in joined:
                    score += 1
            if score > 0:
                candidates.append({"page_id": path, "title": title.title(), "match_score": score})
        return sorted(candidates, key=lambda item: item["match_score"], reverse=True)[:5]

    def _suggest_page_type(self, key_points: List[str], frontmatter: dict) -> str:
        text = " ".join(key_points).lower()
        original_filename = (frontmatter.get("original_filename") or "").lower()
        if "project" in text or "project" in original_filename:
            return "project"
        if "system" in text or "workflow" in text or "knowledge" in text:
            return "concept"
        return "topic"

    def _proposed_actions(self, text: str) -> list[dict]:
        lowered = text.lower()
        actions: list[dict] = []
        if "should" in lowered or "next" in lowered or "implement" in lowered:
            actions.append(
                {
                    "title": "Review imported raw and decide commit path",
                    "description": "Confirm whether this raw should become a new page, update an existing page, or create follow-up actions.",
                    "priority": "medium",
                }
            )
        return actions

    def _unresolved_questions(self, text: str) -> List[str]:
        questions = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.endswith("?"):
                questions.append(stripped)
        return questions[:5]
