---
title: サイトとビルドの構成
description: Software Exploration Patterns の技術選定、ローカルでの読み方、ビルドの仕組み。
---

# サイトとビルドの構成

このページは、リポジトリとサイトがどう動いているかの案内です。知識そのものは [Patterns](../patterns/) などにあります。

## 考え方

優先順位をこの順で決めています。

1. 保守しやすい
2. Markdown が Source of Truth
3. LLM が読みやすい
4. ローカルでも閲覧できる
5. GitHub Pages で簡単に公開できる

サイトの見た目を良くすることは、この5つより下です。

## 構成

| 要素 | 中身 |
|---|---|
| コンテンツ | `patterns/` `heuristics/` `episodes/` `sources/` の Markdown。これが正本 |
| サイト生成 | GitHub Pages の Jekyll。設定は `_config.yml` 1枚 |
| 表示 | `_layouts/` 2枚（`default` / `knowledge`）と `assets/css/main.css` 1枚。JavaScript なし |
| 派生物の生成 | `scripts/build_catalog.py`（Python 標準ライブラリのみ） |
| 公開 | `.github/workflows/pages.yml`。`main` へのマージで自動更新 |
| 検査 | 同ワークフローで front matter と内部リンクを検査。`secret-scan.yml` で簡易 Secret Scan |

コンテンツ側の Markdown には、Jekyll 固有の記述（`layout:` 指定など）を書きません。レイアウトは `_config.yml` の `defaults` でまとめて与えています。GitHub 上で読んでも、サイトで読んでも、同じ `.md` リンクが機能します。

## ローカルで読む

Markdown が正本なので、**クローンしてエディタで読むだけで内容は完全に読めます。** サイトを立ち上げる必要はありません。

メタデータと内部リンクを検査したい場合:

```bash
python3 scripts/build_catalog.py --check   # 検査のみ
python3 scripts/build_catalog.py           # 検査 + 派生物の生成
```

検査しているのは次の点です。

- front matter に `id` / `type` / `title` があること
- `id` がファイル名と一致し、リポジトリ全体で重複しないこと
- `type` / `status` が既知の値であること
- `related` / `sources` / `episodes` に書いた `id` が実在すること
- Markdown 内の相対リンクの先が実在すること

サイトの表示を手元で確認したい場合のみ（任意）:

```bash
gem install github-pages
jekyll serve
```

## 生成される派生物

`build_catalog.py` が、`catalog.json` / `patterns.json` / `all-patterns.md` / `llms.txt` / `llms-full.txt` と、Jekyll のテンプレートが読む `_data/catalog.json` を生成します。

**いずれもコミットしません。** PR ごとの衝突と commit-back ループを避けるため、ビルド時に生成してサイトへ載せています。サイト上での URL は [LLM から使う](llm.md) を見てください。

`_data/catalog.json` があることで、テンプレート側は id からタイトルと URL を引けます。関連知識のリンクやタグ一覧を、HTML に知識を書き写さずに組み立てられるのはこのためです。

## 技術選定の記録（ADR）

- [0001 Markdown を Source of Truth にする](adr/0001-markdown-as-source-of-truth.md)
- [0002 GitHub Pages 標準の Jekyll でサイトを生成する](adr/0002-github-pages-with-jekyll.md)
- [0003 コンテンツのライセンスを CC0 1.0 とする](adr/0003-license-cc0.md)
- [0004 front matter の最小スキーマ](adr/0004-metadata-schema.md)
- [0005 表示は自前の最小レイアウトで行う](adr/0005-minimal-custom-layout.md)

## 関連

- [front matter の書き方](metadata.md)
- [ROADMAP](roadmap.md)
