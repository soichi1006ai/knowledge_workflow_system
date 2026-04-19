# knowledge_workflow_system

AI-native, Markdown-first Knowledge Workflow System.

This project aims to go beyond note-taking by turning knowledge into an operational system.
It is designed to connect capture, structure, reasoning, decision, and action while keeping Markdown as the source of truth.

## Product promise
A system where:
- raw notes become reusable knowledge
- knowledge is grounded in sources
- answers connect to decisions and actions
- stale knowledge and unresolved questions stay visible
- local-first assets remain portable

## Core principles
- Markdown is the source of truth
- Frontmatter is canonical for machine processing
- Page objects and non-page objects are strictly separated
- Archive is represented by archive directory plus `archived_at`
- Default query excludes archived content
- Workflow-first APIs matter more than generic CRUD

## Current MVP spine
Inbox -> Ingest Preview -> Ingest Commit -> Knowledge Page -> Query -> Decision / Action

## Repository structure
- `docs/` specifications and implementation notes
- `app/` FastAPI backend skeleton
- `sample_vault/` sample markdown pack
- `scripts/` local dev helpers
- `tests/` early verification notes

## Sample vault object model
### Page objects
- concept
- entity
- topic
- project
- source-summary

### Non-page objects
- raw item
- source
- decision
- action
- unresolved question
- review candidate
- review record
- project context

## Run locally
```bash
cd knowledge_workflow_system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/run_dev.sh
```

Then open:
- `http://127.0.0.1:8000/docs`

## Current implemented flow
This repository now supports a working MVP slice:
- inbox folder import
- raw markdown generation
- attachment preservation
- imported-file archiving
- ingest preview based on imported raw content
- ingest commit to either create a new page or merge into an existing page
- source object generation during commit
- decision, action, and unresolved generation during commit
- sample vault execution path

## Current API highlights
- `POST /api/raw/inbox/import`
- `POST /api/raw/{raw_id}/ingest-preview`
- `POST /api/raw/{raw_id}/ingest-commit`
- `GET /api/pages`
- `POST /api/query`

## Verification
```bash
source .venv/bin/activate
python -m unittest tests/test_ingest_flow.py
```

## Current limitations
- PDF extraction path exists but needs more real-file verification
- XLSX extraction is not implemented yet
- OCR for images is not implemented yet
- video transcription is not implemented yet
- generated decision, action, and unresolved records are still template-level and should become smarter
- page merge logic is conservative and append-only

## Near-term priorities
1. strengthen PDF verification and extraction quality
2. add spreadsheet extraction
3. add OCR pipeline for images
4. connect decision / action / unresolved generation
5. improve merge quality and structured source linking
