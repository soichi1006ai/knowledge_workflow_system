---
page_id: pg_prj001
title: "Knowledge OS MVP Project"
type: project
status: stable
page_confidence: high
linked_project_id: prj_kos001
source_ids:
 - src_kos001
 - src_20260417_090217_103051
related_page_ids: 
linked_decision_ids: 
linked_action_ids: 
linked_question_ids: 
created_at: 2026-04-14
updated_at: 2026-04-17
review_due: 2026-05-01
archived_at: 
---

# Knowledge OS MVP Project

## Summary
Project aggregation page for the MVP.

## Imported Updates
- 2026-04-17: imported new supporting raw content.

# inbox
Drop arbitrary source files here.
Current MVP behavior:
- text-like files are converted into raw markdown under `raw/inbox/`
- binary or non-parsed files are copied into `attachments/`
- originals are archived into `system/imported/`
- use `POST /api/raw/inbox/import` to process files
