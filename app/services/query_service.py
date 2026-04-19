import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from app.config import settings
from app.schemas.query import (
    QueryCitationPage,
    QueryCitationSource,
    QueryRequest,
    QueryResponse,
    SuggestedAction,
    SuggestedUnresolved,
)
from app.services.frontmatter_service import FrontmatterService


class QueryService:
    def __init__(self) -> None:
        self.frontmatter_service = FrontmatterService()
        self.vault_root = Path(settings.vault_root)

    def run(self, payload: QueryRequest) -> QueryResponse:
        pages = self._load_pages(include_archived=payload.include_archived)
        scored = self._score_pages(payload.query, pages)
        top = scored[: payload.max_results]

        cited_pages = []
        cited_sources = []
        answer_parts = []

        for fm, body, score in top:
            page_id = str(fm.get("page_id", ""))
            title = str(fm.get("title", ""))
            page_type = str(fm.get("type", "topic"))

            cited_pages.append(
                QueryCitationPage(page_id=page_id, title=title, page_type=page_type)
            )

            for src_id in (fm.get("source_ids") or []):
                cited_sources.append(
                    QueryCitationSource(
                        source_id=str(src_id),
                        title=f"Source for {title}",
                        canonical_source_type="raw-note",
                    )
                )

            summary = self._extract_summary(body)
            if summary:
                answer_parts.append(f"**{title}**: {summary}")

        if answer_parts:
            answer = "\n\n".join(answer_parts)
        else:
            answer = "該当するページが見つかりませんでした。"

        confidence_summary = self._build_confidence_summary(top)

        suggested_actions = self._collect_open_actions(payload.active_project_id)
        suggested_unresolved = self._collect_open_unresolved(payload.active_project_id)

        return QueryResponse(
            answer=answer,
            cited_pages=cited_pages,
            cited_sources=cited_sources,
            page_confidence_summary=confidence_summary,
            suggested_decisions=[],
            suggested_actions=suggested_actions,
            suggested_unresolved=suggested_unresolved,
        )

    def _load_pages(self, include_archived: bool) -> List[Tuple[Dict[str, Any], str]]:
        wiki_dir = self.vault_root / "wiki"
        if not wiki_dir.exists():
            return []

        pages = []
        for md_file in wiki_dir.rglob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
            except Exception:
                continue

            fm, body = self.frontmatter_service.split(text)
            if not include_archived and fm.get("archived_at"):
                continue
            pages.append((fm, body))

        return pages

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"[a-zA-Z0-9\u3040-\u9fff\u30a0-\u30ff\u4e00-\u9fff]+", text.lower())

    def _score_pages(
        self, query: str, pages: List[Tuple[Dict[str, Any], str]]
    ) -> List[Tuple[Dict[str, Any], str, float]]:
        query_tokens = set(self._tokenize(query))
        if not query_tokens:
            return [(fm, body, 0.0) for fm, body in pages]

        scored = []
        for fm, body in pages:
            title = str(fm.get("title", ""))
            full_text = f"{title} {body}"
            page_tokens = self._tokenize(full_text)
            token_count = len(page_tokens)
            if token_count == 0:
                continue

            matches = sum(1 for t in page_tokens if t in query_tokens)
            # title matches are weighted higher
            title_matches = sum(1 for t in self._tokenize(title) if t in query_tokens)
            score = (matches / token_count) * 100 + title_matches * 5
            if score > 0:
                scored.append((fm, body, score))

        scored.sort(key=lambda x: x[2], reverse=True)
        return scored

    def _extract_summary(self, body: str) -> str:
        for line in body.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                return stripped[:200]
        return ""

    def _build_confidence_summary(self, top: List[Tuple[Dict[str, Any], str, float]]) -> str:
        if not top:
            return "関連ページが見つかりませんでした"
        confidences = [str(fm.get("page_confidence", "medium")) for fm, _, _ in top]
        return f"{len(top)}件のページを参照（信頼度: {', '.join(set(confidences))}）"

    def _collect_open_actions(self, project_id: str | None) -> List[SuggestedAction]:
        actions_dir = self.vault_root / "actions" / "open"
        if not actions_dir.exists():
            return []

        items = []
        for md_file in actions_dir.rglob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
            except Exception:
                continue
            fm, _ = self.frontmatter_service.split(text)
            if fm.get("archived_at"):
                continue
            if project_id and fm.get("linked_project_id") != project_id:
                continue
            items.append(
                SuggestedAction(
                    title=str(fm.get("title", md_file.stem)),
                    description=str(fm.get("description", "")),
                    priority=str(fm.get("priority", "medium")),
                )
            )
        return items[:5]

    def _collect_open_unresolved(self, project_id: str | None) -> List[SuggestedUnresolved]:
        uq_dir = self.vault_root / "unresolved" / "active"
        if not uq_dir.exists():
            return []

        items = []
        for md_file in uq_dir.rglob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
            except Exception:
                continue
            fm, _ = self.frontmatter_service.split(text)
            if fm.get("archived_at"):
                continue
            if project_id and fm.get("linked_project_id") != project_id:
                continue
            items.append(
                SuggestedUnresolved(
                    question=str(fm.get("question", fm.get("title", md_file.stem))),
                    why_unresolved="",
                    next_step="",
                    priority=str(fm.get("priority", "medium")),
                )
            )
        return items[:5]
