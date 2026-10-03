---
id: unanswerable-means-undecided
type: heuristic
title: 誰も答えられない質問は、要求ではなく未決定事項
status: draft
tags:
  - requirements
  - risk
related:
  - value-meaning
  - start-from-failure-state
sources: []
episodes: []
created: 2026-10-04
updated: 2026-10-04
---

# 誰も答えられない質問は、要求ではなく未決定事項

仕様について質問して、関係者の誰からも答えが返ってこないとき、それは「調べれば分かること」ではなく、**まだ誰も決めていないこと**である可能性が高い。

その場合は答えを探し続けるのではなく、**未決定事項として記録し、誰がいつ決めるのかを確認する**ほうが早い。

**効くとき:** 複数の関係者に聞いても回答が食い違う、または「たぶん」が付くとき。

**外れるとき:** 答えを持っている人にまだ到達していないだけのとき。聞いた相手が適切だったかを先に確かめる。

## 関連

- [値の意味を問う](../patterns/value-meaning.md)
- [失敗状態から戻る](../patterns/start-from-failure-state.md)
