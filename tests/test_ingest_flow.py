from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import settings
from app.schemas.raw import InboxImportRequest, IngestCommitRequest
from app.services.inbox_service import InboxService
from app.workflows.ingest_commit_flow import IngestCommitFlow
from app.workflows.ingest_preview_flow import IngestPreviewFlow


class IngestFlowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp(prefix="kos_test_")
        self.original_vault_root = settings.vault_root
        settings.vault_root = self.temp_dir

        vault = Path(self.temp_dir)
        (vault / "inbox").mkdir(parents=True, exist_ok=True)
        (vault / "wiki" / "concepts").mkdir(parents=True, exist_ok=True)
        (vault / "system" / "sources").mkdir(parents=True, exist_ok=True)
        (vault / "raw" / "inbox").mkdir(parents=True, exist_ok=True)
        (vault / "decisions" / "active").mkdir(parents=True, exist_ok=True)
        (vault / "actions" / "open").mkdir(parents=True, exist_ok=True)
        (vault / "unresolved" / "active").mkdir(parents=True, exist_ok=True)

        (vault / "inbox" / "note.txt").write_text(
            "Knowledge Workflow System should update existing knowledge safely.\nWhat should be reviewed next?\n",
            encoding="utf-8",
        )
        (vault / "wiki" / "concepts" / "knowledge-os.md").write_text(
            "---\n"
            "page_id: pg_kos001\n"
            "title: \"Knowledge OS\"\n"
            "type: concept\n"
            "status: stable\n"
            "page_confidence: high\n"
            "linked_project_id: prj_kos001\n"
            "source_ids:\n"
            " - src_kos001\n"
            "related_page_ids: []\n"
            "linked_decision_ids: []\n"
            "linked_action_ids: []\n"
            "linked_question_ids: []\n"
            "created_at: 2026-04-14\n"
            "updated_at: 2026-04-14\n"
            "review_due: 2026-05-14\n"
            "archived_at: \n"
            "---\n\n"
            "# Knowledge OS\n\n"
            "## Summary\n"
            "Existing summary.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        settings.vault_root = self.original_vault_root
        shutil.rmtree(self.temp_dir)

    def test_import_preview_commit_update_existing_page(self) -> None:
        inbox_service = InboxService()
        preview_flow = IngestPreviewFlow()
        commit_flow = IngestCommitFlow()

        import_result = inbox_service.import_inbox(InboxImportRequest())
        self.assertEqual(len(import_result.items), 1)
        raw_id = import_result.items[0].raw_id

        preview = preview_flow.run(raw_id, None)
        self.assertTrue(preview.candidate_existing_pages)

        commit = commit_flow.run(
            raw_id,
            IngestCommitRequest(existing_page_path="wiki/concepts/knowledge-os.md"),
        )
        self.assertEqual(commit.created_page_ids, [])
        self.assertEqual(commit.updated_page_ids, ["wiki/concepts/knowledge-os.md"])

        updated_page = Path(self.temp_dir) / "wiki" / "concepts" / "knowledge-os.md"
        content = updated_page.read_text(encoding="utf-8")
        self.assertIn("Imported Updates", content)
        self.assertIn("Knowledge Workflow System should update existing knowledge safely.", content)

        source_file = Path(self.temp_dir) / "system" / "sources" / commit.source_id
        self.assertFalse(source_file.exists())
        source_file_md = Path(self.temp_dir) / "system" / "sources" / f"{commit.source_id}.md"
        self.assertTrue(source_file_md.exists())

        decision_file = Path(self.temp_dir) / "decisions" / "active" / "dec_202"
        self.assertTrue(any((Path(self.temp_dir) / "decisions" / "active").glob("dec_*.md")))
        self.assertTrue(any((Path(self.temp_dir) / "actions" / "open").glob("act_*.md")))
        self.assertTrue(any((Path(self.temp_dir) / "unresolved" / "active").glob("uq_*.md")))


if __name__ == "__main__":
    unittest.main()
