---
id: find-exceptions-behind-absolutes
type: heuristic
title: 「すべて」「必ず」と書かれていたら、例外を探す
status: draft
tags:
  - requirements
  - exploration
related:
  - observe-the-field
  - ask-the-expert
sources: []
episodes: []
created: 2026-10-04
updated: 2026-10-04
---

# 「すべて」「必ず」と書かれていたら、例外を探す

仕様の「すべての利用者が」「必ず承認を経て」「常に表示される」といった全称的な表現は、**例外を知らないか、例外を書くのを省略したかのどちらか**であることが多い。

「この条件に当てはまらないケースを一つ挙げるとしたら何か」と聞いてみる。

**効くとき:** 業務システムや、長く運用されている仕組みの仕様を読むとき。運用には例外処理がたまりやすい。

**外れるとき:** 意図的に例外を排除した設計（不変条件として守らせている場合）。この場合は「どこで保証しているか」を確かめるほうに切り替える。

## 関連

- [現場を見る](../patterns/observe-the-field.md) — 例外は現場に現れる
- [知っている人に聞く](../patterns/ask-the-expert.md)
