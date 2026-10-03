# 0002 GitHub Pages 標準の Jekyll でサイトを生成する

- 状態: Accepted
- 日付: 2026-10-04

## 背景

`main` にマージされたらサイトが自動更新され、最新の知識を閲覧できる状態にしたい。ただし、求められている優先順位は次のとおりで、UI の凝り方ではない。

1. 保守しやすい
2. Markdown が Source of Truth
3. LLM が読みやすい
4. ローカルでも閲覧できる
5. GitHub Pages で簡単に公開できる

## 決定

**GitHub Pages 標準の Jekyll** を、GitHub Actions 経由で使う。リポジトリに追加する設定ファイルは `_config.yml` 1枚のみとする。テーマは `jekyll-theme-primer`。

## 理由

GitHub Pages の gem には、次のプラグインが含まれており、**デフォルトで有効**になっている（[pages.github.com/versions](https://pages.github.com/versions)）。

| プラグイン | 効果 |
|---|---|
| `jekyll-relative-links` | `../patterns/foo.md` のような相対リンクが、サイト上でも機能する |
| `jekyll-readme-index` | 各ディレクトリの `README.md` が、そのディレクトリのトップページになる |
| `jekyll-optional-front-matter` | front matter のない `.md` もページになる |
| `jekyll-titles-from-headings` | 見出しからタイトルを取る |

この結果、**コンテンツ側の Markdown に Jekyll 固有の記述（`layout:` 指定など）を一切書かずに済む**。GitHub 上で読んでも、サイトで読んでも、同じリンクが機能する。ADR 0001 の「Markdown を正本にする」という方針と、サイト生成が衝突しない。

### 比較した選択肢

- **MkDocs + Material** — 検索 UI と見た目は上回る。しかし `mkdocs.yml` の nav 保守、Python 依存の固定、テーマ更新への追従が発生する。知識の蓄積より、サイトの保守にコストがかかる状態を避けたかった
- **サイトを作らない（GitHub で読むだけ）** — 最も軽いが、「`main` へのマージで公開内容が自動更新される」という要件を満たさない
- **GitHub Pages のブランチ公開（Actions を使わない）** — さらに設定は減るが、ビルド前に生成スクリプト（`catalog.json` など）を走らせられない

### Actions を使う理由

ブランチからの自動ビルドではなく GitHub Actions でビルドするのは、Jekyll のビルド前に `scripts/build_catalog.py` を実行して、機械可読な派生物を生成するため。

## 帰結

- 公開を開始するには、リポジトリの Settings → Pages → Source を「GitHub Actions」に設定する必要がある
- サイトの機能は Jekyll + GitHub Pages のプラグイン群でできる範囲に限られる（全文検索は現状なし）
- ローカルでサイト表示を確認するには `gem install github-pages` が必要。ただし **Markdown が正本なので、サイトを立ち上げなくても内容はすべて読める**
- 将来、サイト生成を別の仕組みに差し替えても、コンテンツ側の Markdown は無改変で移行できる
