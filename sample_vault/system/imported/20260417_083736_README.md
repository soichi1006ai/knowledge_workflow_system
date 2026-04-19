# inbox

Drop arbitrary source files here.

Current MVP behavior:
- text-like files are converted into raw markdown under `raw/inbox/`
- binary or non-parsed files are copied into `attachments/`
- originals are archived into `system/imported/`
- use `POST /api/raw/inbox/import` to process files
