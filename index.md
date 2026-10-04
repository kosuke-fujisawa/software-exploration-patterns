ソフトウェア開発で、未知・ズレ・リスクに気づき、理解を更新するための「探索知」を集めるオープンな知識ベースです。要求工学・テスト・QA・アジャイル・PdM・UX・設計・Safety / Reliability に散らばった知識を、分野を越えて持ち寄ります。

- [パターンを見る](patterns/)
- [経験を投稿する](https://github.com/{{ site.repository }}/issues/new?template=01-new-exploration-knowledge.yml)
- [このプロジェクトについて知る](docs/about.md)

集めているのは「正しい開発のやり方」でも「テスト技法集」でもありません。何かがおかしいと気づく、前提を疑う、不明点を見つける、誰かに聞く、現場を見る、リスクを見つける、そのリスクを要求・設計・実装・テスト・運用のどこで扱うか考える —— そうした気づき方の知識です。

## まず読んでみる

{% for id in site.featured_patterns -%}
{%- assign item = site.data.catalog.entries | where: "id", id | first -%}
{%- if item %}
- **[{{ item.title }}]({{ item.site_path | relative_url }})** — {{ item.summary }}
{%- endif -%}
{%- endfor %}

いずれも初期サンプルであり、確立されたベストプラクティスではありません。実務で試して効かなかった、前提が違った、という報告こそが、この知識ベースを次に進めます。

## 知識ベース

{% assign c = site.data.catalog.counts -%}

- **[Episodes](episodes/)**（{{ c.episode }}件）— 実際に起きた出来事や経験。整理されていなくてよい、いちばん生の記録。
- **[Heuristics](heuristics/)**（{{ c.heuristic }}件）— 探索するときに役立つ短い判断則。経験則であって、保証ではない。
- **[Patterns](patterns/)**（{{ c.pattern }}件）— 文脈・問題・帰結まで言語化され、複数の経験で再利用できる形になった探索パターン。
- **[Sources](sources/)**（{{ c.source }}件）— 既存研究・書籍・論文・記事・方法論。再発明を避けるための来歴。

この4つは上下関係ではなく、探索知を異なる粒度・役割で残すための分類です。エピソードからヒューリスティックが生まれることもあれば、複数のエピソードからパターン候補が立ち上がることも、既存研究がパターンを書き換えることも、パターンに反例が加わって適用範囲が狭まることもあります。読んだパターンが次の探索を生み、それがまた新しいエピソードになります。一方向に昇格していく階段ではありません。

[タグから横断して読む]({{ '/tags/' | relative_url }})こともできます。

なお、この知識ベースはまだ初期段階です。掲載内容は継続的に検証・修正・統合されます。体系として完成しているわけでも、標準でもありません。

## あなたの経験も探索知になります

完成したパターンを書く必要はありません。次のどれでも歓迎します。

- 実際に起きたエピソードだけ（「こういう状況で、こう気づいた」で十分です）
- 「このパターンは自分の状況では使えなかった」という反例
- 「この話は既存研究にある」という出典だけの共有
- 分類が合っていない、重複している、という指摘

GitHub の操作に慣れていなくても、Issue のフォームから送れます。整理・分類・ファイル化は Maintainer や他の参加者が引き取ります。

- [経験を投稿する](https://github.com/{{ site.repository }}/issues/new?template=01-new-exploration-knowledge.yml)
- [既存パターンへ意見を送る](https://github.com/{{ site.repository }}/issues/new?template=02-feedback-on-pattern.yml)
- [出典を共有する](https://github.com/{{ site.repository }}/issues/new?template=03-share-source.yml)

> 実務事例を投稿する場合は、公開できない情報（顧客名・会社名・個人情報・非公開仕様・内部URL・認証情報・案件固有の詳細）を除去し、一般化してください。一般化のしかたの例と、投稿の詳しいルールは [参加のしかた](CONTRIBUTING.md) にあります。

## さらに詳しく

- [このプロジェクトについて](docs/about.md) — なぜ作るのか、探索知とは何か、何を大切にしているか
- [参加のしかた](CONTRIBUTING.md) — 投稿の流れ、書き方、公開してはいけない情報
- [ガバナンス](GOVERNANCE.md) — 共同知識基盤としての運営方針
- [LLM から使う](docs/llm.md) — `catalog.json` / `llms.txt` など機械可読な出力
- [サイトとビルドの構成](docs/architecture.md) — 技術選定、ローカルでの読み方、front matter 仕様
- [ROADMAP](docs/roadmap.md) — 今後やれること、意図的に入れなかったもの

コンテンツとスクリプトは CC0 1.0（パブリックドメイン提供）です。ライセンス上の帰属義務はありませんが、知識の来歴をたどれるように出典を残すことを大切にしています。誰でも修正・追加・反例の提示ができる、community-maintained な知識ベースです。
