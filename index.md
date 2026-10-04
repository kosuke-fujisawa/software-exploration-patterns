---
title: Software Exploration Patterns
wide: true
---

<div class="hero">
<h1>Software Exploration Patterns</h1>
<p class="hero__lead">ソフトウェア開発で、未知・ズレ・リスクに気づき、理解を更新するための「探索知」を集めるオープンな知識ベースです。要求工学・テスト・QA・アジャイル・PdM・UX・設計・Safety / Reliability に散らばった知識を、分野を越えて持ち寄ります。</p>
<div class="actions">
<a class="btn btn--primary" href="{{ '/patterns/' | relative_url }}">パターンを読む</a>
<a class="btn" href="https://github.com/{{ site.repository }}/issues/new?template=01-new-exploration-knowledge.yml">経験を投稿する</a>
<a class="btn" href="{{ '/docs/about.html' | relative_url }}">このプロジェクトについて</a>
</div>
</div>

ここで集めているのは、「正しい開発のやり方」でも「テスト技法集」でもありません。
**何かがおかしいと気づく / 前提を疑う / 不明点を見つける / 誰かに聞く / 現場を見る / リスクを見つける / そのリスクを要求・設計・実装・テスト・運用のどこで扱うか考える** —— そうした*気づき方*の知識です。

## まず読んでみる

{% if site.data.catalog %}
<ul class="cards">
{%- for id in site.featured_patterns -%}
{%- assign item = site.data.catalog.entries | where: "id", id | first -%}
{%- if item %}
<li class="card">
<h3><a href="{{ item.site_path | relative_url }}">{{ item.title }}</a></h3>
<p>{{ item.summary | markdownify | strip_html | strip }}</p>
<p class="card__meta"><span class="badge badge--{{ item.status }}">{{ site.data.status[item.status].label }}</span></p>
</li>
{%- endif -%}
{%- endfor %}
</ul>
{% else %}
[パターン一覧](patterns/) を見てください。
{% endif %}

いずれも**初期サンプルであり、確立されたベストプラクティスではありません**。実務で試した結果、効かなかった・前提が違ったという報告こそが、この知識ベースを次に進めます。

## 知識ベース

{% if site.data.catalog %}
<ul class="cards cards--compact">
<li class="card">
<h3><a href="{{ '/episodes/' | relative_url }}">Episodes</a></h3>
<p>実際に起きた出来事や経験。整理されていなくてよい、いちばん生の記録。</p>
<p class="card__meta"><span class="card__count">{{ site.data.catalog.counts.episode }}</span> 件</p>
</li>
<li class="card">
<h3><a href="{{ '/heuristics/' | relative_url }}">Heuristics</a></h3>
<p>探索するときに役立つ短い判断則。経験則であって、保証ではない。</p>
<p class="card__meta"><span class="card__count">{{ site.data.catalog.counts.heuristic }}</span> 件</p>
</li>
<li class="card">
<h3><a href="{{ '/patterns/' | relative_url }}">Patterns</a></h3>
<p>文脈・問題・帰結まで言語化され、複数の経験で再利用できる形になった探索パターン。</p>
<p class="card__meta"><span class="card__count">{{ site.data.catalog.counts.pattern }}</span> 件</p>
</li>
<li class="card">
<h3><a href="{{ '/sources/' | relative_url }}">Sources</a></h3>
<p>既存研究・書籍・論文・記事・方法論。再発明を避けるための来歴。</p>
<p class="card__meta"><span class="card__count">{{ site.data.catalog.counts.source }}</span> 件</p>
</li>
</ul>
{% endif %}

この4つは**上下関係ではなく、探索知を異なる粒度で残すための分類**です。エピソードからヒューリスティックが生まれることもあれば、複数のエピソードからパターン候補が立ち上がることも、既存研究がパターンを書き換えることも、パターンに反例が加わって適用範囲が狭まることもあります。読んだパターンが次の探索を生み、それがまた新しいエピソードになります。一方向に昇格していく階段ではありません。

[タグから横断して読む]({{ '/tags/' | relative_url }}) こともできます。

<div class="note">
<p><strong>この知識ベースはまだ初期段階です。</strong> 掲載内容は継続的に検証・修正・統合されます。体系として完成しているわけでも、標準でもありません。</p>
</div>

## あなたの経験も探索知になります

完成したパターンを書く必要はありません。次のどれでも歓迎します。

- 実際に起きた**エピソードだけ**（「こういう状況で、こう気づいた」で十分です）
- 「**このパターンは自分の状況では使えなかった**」という反例
- 「**この話は既存研究にある**」という出典だけの共有
- 分類が合っていない、重複している、という指摘

GitHub の操作に慣れていなくても、Issue のフォームから送れます。整理・分類・ファイル化は Maintainer や他の参加者が引き取ります。

<div class="actions">
<a class="btn btn--primary" href="https://github.com/{{ site.repository }}/issues/new?template=01-new-exploration-knowledge.yml">経験を投稿する</a>
<a class="btn" href="https://github.com/{{ site.repository }}/issues/new?template=02-feedback-on-pattern.yml">既存パターンへ意見を送る</a>
<a class="btn" href="https://github.com/{{ site.repository }}/issues/new?template=03-share-source.yml">出典を共有する</a>
</div>

<div class="note">
<p>実務事例を投稿する場合は、<strong>公開できない情報（顧客名・会社名・個人情報・非公開仕様・内部URL・認証情報・案件固有の詳細）を除去し、一般化してください。</strong> 一般化のしかたの例と、投稿の詳しいルールは <a href="{{ '/CONTRIBUTING.html' | relative_url }}">参加のしかた</a> にあります。</p>
</div>

## さらに詳しく

- [このプロジェクトについて](docs/about.md) — なぜ作るのか、探索知とは何か、何を大切にしているか
- [参加のしかた](CONTRIBUTING.md) — 投稿の流れ、書き方、公開してはいけない情報
- [ガバナンス](GOVERNANCE.md) — 共同知識基盤としての運営方針
- [LLM から使う](docs/llm.md) — `catalog.json` / `llms.txt` など機械可読な出力
- [サイトとビルドの構成](docs/architecture.md) — 技術選定、ローカルでの読み方、front matter 仕様
- [ROADMAP](docs/roadmap.md) — 今後やれること、意図的に入れなかったもの
