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
bash scripts/run_dev.sh
```

Then open:
- `http://127.0.0.1:8000/docs`

## Current status
This repository currently includes:
- initial FastAPI skeleton
- initial sample vault content
- workflow-first design notes

## Near-term priorities
1. schema validation
2. ingest preview and commit flow
3. query minimum contract
4. decision and action flow
5. dashboard minimal
