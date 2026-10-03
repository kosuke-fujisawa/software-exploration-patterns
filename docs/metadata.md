# front matter の書き方

知識ファイル（`episodes/` `heuristics/` `patterns/` `sources/` 以下の `.md`）の先頭に付ける YAML front matter の仕様です。

**このスキーマは暫定であり、将来変更します。** 最初から複雑にしないことを方針としています（[ADR 0004](adr/0004-metadata-schema.md)）。

## 例

```yaml
---
id: value-meaning
type: pattern
title: 値の意味を問う
status: draft
tags:
  - requirements
  - exploration
  - risk
related:
  - ask-the-expert
sources:
  - usdm
episodes:
  - boundary-value-without-reason
created: 2026-10-04
updated: 2026-10-04
---
```

## フィールド

| フィールド | 必須 | 内容 |
|---|---|---|
| `id` | **必須** | 英小文字のケバブケース。**ファイル名（拡張子を除く）と一致させる** |
| `type` | **必須** | `episode` / `heuristic` / `pattern` / `source` のいずれか |
| `title` | **必須** | 日本語で可。本文の見出しと揃えることを推奨 |
| `status` | 任意 | `draft`（既定）/ `reviewed` / `stub` |
| `tags` | 任意 | 自由語。統制語彙は作っていない |
| `related` | 任意 | 関連する他エントリの `id` の配列 |
| `sources` | 任意 | 関連する `sources/` エントリの `id` の配列 |
| `episodes` | 任意 | 根拠になった `episodes/` エントリの `id` の配列 |
| `created` / `updated` | 任意 | `YYYY-MM-DD` |

### status の意味

- `draft` — 投稿された状態。内容の正しさは保証されない（ほとんどがこれ）
- `reviewed` — 複数人が読み、公開情報として問題がなく、意味が通ることを確認した。**内容が正しいという意味ではない**
- `stub` — 存在は分かっているが中身が埋まっていない。加筆を募集している状態

## 制約

`scripts/build_catalog.py --check` が次を検査します。CI でも実行されます。

- `id` / `type` / `title` があること
- `id` がファイル名と一致すること
- `id` がリポジトリ全体で重複しないこと
- `type` が既知の値であること
- `related` / `sources` / `episodes` に書いた `id` が実在すること
- `status` が既知の値であること

## 本文中のリンク

`related` に書くだけでなく、本文中でも相対リンクを張ってください。

```markdown
- [知っている人に聞く](../patterns/ask-the-expert.md)
```

`.md` を含む相対リンクは、GitHub 上でも、生成されたサイト上でも機能します（`jekyll-relative-links` によってサイト側で `.html` に変換されます）。

## パーサについて

front matter は、外部依存を避けるため `scripts/build_catalog.py` 内の最小パーサで読んでいます。対応しているのは次の形だけです。

- `key: value`（文字列・日付）
- `key: []`（空リスト）
- `key: [a, b]`（1行リスト）
- 次の形の複数行リスト

```yaml
key:
  - a
  - b
```

ネストしたマッピングやブロックスカラー（`|` `>`）は読めません。必要になったら、そのとき対応します。
