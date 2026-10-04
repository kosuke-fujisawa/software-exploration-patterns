# 0005 表示は自前の最小レイアウトで行う

- 状態: Accepted
- 日付: 2026-10-04
- 関連: [0002 GitHub Pages 標準の Jekyll でサイトを生成する](0002-github-pages-with-jekyll.md)（置き換えではなく、その中の「テーマ」部分の決定）

## 背景

初版では `jekyll-theme-primer` をそのまま使っていた。設定ゼロで読める形になる利点があった一方、サイトを使ってみると次が足りないことが分かった。

- トップページが README 兼用で、初見の人にとって情報量が多い
- どのパターンから読めばよいかの導線がない
- front matter の `status` / `tags` / `related` / `sources` / `episodes` が表示に出ず、ナビゲーションに使えない
- 現在地が分かるナビゲーションがない

テーマの `_layouts/default.html` を上書きして差分を足す手もあるが、上書きした時点でテーマ本体の HTML を自分で持つことになり、「テーマを使っている」利点（更新に追従できる）はほとんど残らない。

## 決定

gem テーマの利用をやめ、**自前の最小レイアウトで表示する。**

- `_layouts/default.html` — ヘッダ・ナビゲーション・フッタ
- `_layouts/knowledge.html` — 知識ファイル用。front matter から status / related / sources / episodes / tags を表示
- `assets/css/main.css` — 素の CSS 1枚（SCSS を使わない）
- JavaScript は使わない

レイアウトの指定は `_config.yml` の `defaults` で与え、**コンテンツ側の Markdown には書かない**（ADR 0001・0002 の方針を維持）。

## 理由

- コンテンツ側の Markdown に Jekyll 固有の記述を増やさない、という制約は変わらずに満たせる
- SCSS のコンパイルやテーマ gem のバージョンに依存しなくなり、ビルドの振る舞いが読んで分かる
- 分量が小さい（レイアウト2枚 + CSS 1枚）。テーマの上書き差分を管理するより読みやすい
- ダークモードは `prefers-color-scheme` と CSS カスタムプロパティで完結する

## 帰結

- 見た目の保守はこのリポジトリの責任になる。代わりに、外部テーマの更新で表示が変わることはなくなった
- `_data/catalog.json` をビルド時に生成し、テンプレートが id からタイトル・URL を引けるようにした。これにより、**関連知識のリンクやタグ一覧を HTML に書き写さずに済む**（ADR 0001 の「HTML だけに情報を閉じ込めない」を守るための実装上の要）
- 表示は front matter にある情報だけを出す。`sources` や `episodes` が空なら、その見出しごと出さない
- JavaScript を使わないため、タグ検索は「タグ一覧ページ内のアンカー」で実現している。全文検索は引き続き未実装
