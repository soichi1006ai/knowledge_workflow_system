# Knowledge OS MVP
## FastAPI用ディレクトリ構成＋Pydanticモデル設計書 v0.1

## 目的
Knowledge OS MVP を FastAPI で実装するための、バックエンドの基本ディレクトリ構成と Pydantic モデル設計の初期版。

## 前提
- Markdown が source of truth
- Page と Non-page object を厳密に分離する
- workflow-first API を中核に置く
- frontmatter が機械処理上の正本
- archive は directory + `archived_at` で canonical に扱う
- default Query では archived を除外する

## ディレクトリ構成
```text
app/
  main.py
  config.py
  api/routers/
  core/
  schemas/
  services/
  repositories/
  workflows/
```

## 実装優先
1. raw
2. ingest preview / commit
3. page detail
4. query
5. decision / action
6. dashboard
