---
title: LLM から使う
description: Software Exploration Patterns を LLM から利用するための、機械可読な出力（catalog.json / llms.txt など）の説明。
---

# LLM から使う

この知識ベースは、人間が読むだけでなく **LLM から利用されることを前提**に作られています。

- Markdown を一次情報（Source of Truth）とする
- 1ファイル1知識単位
- すべての知識ファイルに front matter でメタデータを付ける
- 関連知識は front matter と本文リンクの両方でつなぐ
- HTML だけに情報を閉じ込めない。JavaScript がないと本文が取れない構成にしない

設計判断の経緯は [ADR 0001](adr/0001-markdown-as-source-of-truth.md) にあります。

## 機械可読な出力

サイトのビルド時に、次のファイルを生成しています。**リポジトリにはコミットせず、サイト上にのみ存在します。**

| URL | 内容 |
|---|---|
| [`/catalog.json`](https://kosuke-fujisawa.github.io/software-exploration-patterns/catalog.json) | 全エントリのメタデータ（id / type / title / status / tags / related / sources / episodes / summary / path / url）と件数 |
| [`/patterns.json`](https://kosuke-fujisawa.github.io/software-exploration-patterns/patterns.json) | パターンのみのメタデータ |
| [`/all-patterns.html`](https://kosuke-fujisawa.github.io/software-exploration-patterns/all-patterns.html) | 全パターンの本文を1ページに連結したもの（人間向け） |
| [`/llms.txt`](https://kosuke-fujisawa.github.io/software-exploration-patterns/llms.txt) | [llmstxt.org](https://llmstxt.org) 形式の目次 |
| [`/llms-full.txt`](https://kosuke-fujisawa.github.io/software-exploration-patterns/llms-full.txt) | 全知識の本文を連結したプレーンテキスト |

`llms-full.txt` ひとつを渡せば、この知識ベースの中身はすべて渡ります。

ローカルでも同じものを生成できます（Python 3.9 以上、外部依存なし）。

```bash
python3 scripts/build_catalog.py
```

生成物をコミットしない理由は、PR ごとの衝突と commit-back ループを避けるためです。

## 想定している使い方

```text
この仕様について、適用できる探索パターンを提示して
この要求に不足している情報を指摘して
次に誰へ何を確認すべきか考えて
この設計で「何が起きたら困るか」を洗い出して
```

いずれも、LLM に `llms-full.txt`（または関連しそうなパターンの Markdown）を渡したうえで聞く想定です。

**出力されたパターンが、あなたの状況で有効とは限りません。** この知識ベースは検証済みの正解集ではなく、「次に何を見るか」を考えるための材料です。LLM の提案をそのまま適用するのではなく、自分の文脈で確かめてください。

## リポジトリをまるごと渡す

Markdown が正本なので、クローンしてディレクトリごと渡すこともできます。

```bash
git clone https://github.com/kosuke-fujisawa/software-exploration-patterns.git
```

- `patterns/` `heuristics/` `episodes/` `sources/` に知識ファイル
- `_` で始まるファイルはテンプレート
- 各ディレクトリの `README.md` が、そのディレクトリの案内

front matter の仕様は [front matter の書き方](metadata.md) にあります。
