# Inbox Ingestion Plan v0.1

## Goal
`knowledge_workflow_system` に、ユーザーが任意のファイルを置くだけで raw 化, 抽出, 分類候補提示, ingest preview まで進められる最小実用ラインを追加する。

## What exists now
現在あるのは以下まで。
- FastAPI skeleton
- raw CRUD stub
- ingest preview stub
- ingest commit stub
- sample vault
- page / non-page object separation

まだ無い本機能。
- monitored inbox folder
- file-type detection across binary/document/media inputs
- parser/extractor pipeline
- normalized raw object creation from files
- attachment/source registry from arbitrary files
- automatic routing candidates based on extracted content
- batch ingest from folder

## User-intended workflow
1. ユーザーが inbox フォルダにファイルを置く
2. システムが対象ファイルを検出する
3. ファイル種別を判定する
4. 抽出できるものは本文, メタデータ, 画像/OCR, 添付情報を抽出する
5. `raw` オブジェクトを生成する
6. `ingest-preview` で page化, decision化, action化の候補を返す
7. 必要に応じて commit する

## Constraints
- Markdown-first を維持する
- source of truth は vault 側に残す
- 重い AI/OCR/video transcription は後段拡張可能にする
- まずはローカル実行優先
- batch 実行で十分。常時 watcher は後からでもよい

## Non-goals for v0.1
- 完全自動の本番運用 watcher
- 高精度な semantic dedup
- 動画音声の完全 transcription
- Office/PDF 全フォーマット完全対応
- vector DB 導入

## Recommended first slice
最初に入れるべき最小スライスはこれ。

### Scope A: inbox batch import
- `sample_vault/inbox/` を追加
- API: `POST /api/inbox/import`
- 処理内容:
  - inbox 内ファイル一覧取得
  - MIME/拡張子判定
  - text-like ファイルは本文抽出
  - binary ファイルはメタデータのみ raw 化
  - raw markdown を `raw/inbox/` に生成
  - 元ファイルは `system/imported/` か `attachments/` へ移動またはコピー
  - import 結果を返す

### Scope B: supported file classes
初期対応:
- `.txt`
- `.md`
- `.pdf` (本文抽出失敗時は metadata only)
- `.docx` (同上)
- `.csv`
- `.json`
- image files `.png .jpg .jpeg .webp` (metadata only, OCR hook placeholder)
- video files `.mp4 .mov` (metadata only, transcript hook placeholder)

### Scope C: normalized raw object
各 import は raw markdown に変換する。
最低限必要な frontmatter:
- raw_id
- title
- input_source_type
- original_filename
- mime_type
- imported_at
- source_path
- extraction_status
- project_candidate
- quick_tags

本文部:
- extracted_text または summary placeholder
- extraction_notes
- unresolved extraction warnings

## Architecture changes

### New folders in sample_vault
- `inbox/`
- `attachments/`
- `system/imported/`

### New enums
`InputSourceType` を拡張する。
- pdf
- docx
- csv
- json
- image
- video
- spreadsheet

### New schemas
- `InboxImportRequest`
- `InboxImportItemResult`
- `InboxImportResponse`

### New services
- `InboxService`
- `ExtractionService`
- `RawWriterService`

### New repository helpers
- file listing
- safe move/copy
- mime detection

## Import decision rules

### text-like files
対象:
- txt
- md
- csv
- json
- extracted text success on pdf/docx

処理:
- text body を raw body に格納
- key metadata 付与
- input_source_type は type specific にする

### binary-like files
対象:
- image
- video
- unreadable pdf/docx

処理:
- 本体は attachments に保存
- raw body には placeholder summary
- extraction_status を `metadata-only` または `needs-extraction` にする

## API proposal

### POST /api/inbox/import
Request:
```json
{
  "mode": "copy",
  "limit": 20,
  "delete_from_inbox": false
}
```

Response:
```json
{
  "success": true,
  "message": "imported 3 files",
  "items": [
    {
      "filename": "meeting-note.txt",
      "detected_type": "text",
      "raw_id": "raw_20260417_001",
      "raw_path": "raw/inbox/raw_20260417_001.md",
      "attachment_path": null,
      "extraction_status": "full-text"
    }
  ]
}
```

## Implementation sequence
1. add dependency definition and local run instructions
2. extend enums and raw schema metadata
3. add inbox service + file detection
4. add text import path for txt/md/csv/json
5. add metadata-only path for image/video/pdf/docx
6. expose `/api/inbox/import`
7. write sample inbox fixtures
8. verify generated raw markdown and API response

## Recommended dependencies
Fast path:
- fastapi
- uvicorn
- pydantic
- python-multipart
- pymupdf or pypdf
- python-docx

Optional later:
- pandas / openpyxl
- pillow
- pytesseract
- whisper or external transcription integration
- watchdog

## Risks
- binary/document extraction quality varies
- OCR/video transcription should be asynchronous later
- attachment storage rules need to stay deterministic
- imported file move/delete policy must be conservative

## Recommendation
次の実装は、watcher ではなく `batch inbox import API` に絞るべき。
理由:
- 最小で価値が出る
- デバッグしやすい
- 失敗時の運用リスクが低い
- watcher は後から乗せられる

これが通れば、その次に
- OCR
- PDF/DOCX extraction hardening
- spreadsheet support
- async transcription
- scheduled watcher
を足せばよい。
