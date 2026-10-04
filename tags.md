---
title: タグから探す
permalink: /tags/
description: Software Exploration Patterns の知識をタグから横断して読むための一覧。
---

# タグから探す

タグは、分類（Episodes / Heuristics / Patterns / Sources）をまたいで知識を横断するための目印です。タグ体系はまだ固定していません。運用しながら統合・変更していきます。付け方に違和感があれば [意見を送ってください](https://github.com/{{ site.repository }}/issues/new?template=02-feedback-on-pattern.yml)。

{% assign all_tags = "" | split: "," -%}
{%- for entry in site.data.catalog.entries -%}
{%- if entry.tags -%}{%- assign all_tags = all_tags | concat: entry.tags -%}{%- endif -%}
{%- endfor -%}
{%- assign tags = all_tags | uniq | sort -%}

{% for tag in tags %}[{{ tag }}](#{{ tag }}){% unless forloop.last %} · {% endunless %}{% endfor %}

{% for tag in tags %}
## {{ tag }}
{% for entry in site.data.catalog.entries -%}
{%- if entry.tags contains tag %}
- [{{ entry.title }}]({{ entry.site_path | relative_url }})（{{ site.data.types[entry.type].label }}）
{%- endif -%}
{%- endfor %}
{% endfor %}
