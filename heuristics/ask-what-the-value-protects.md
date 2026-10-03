---
id: ask-what-the-value-protects
type: heuristic
title: 具体的な値を見たら、その値が何を守っているのかを問う
status: draft
tags:
  - requirements
  - risk
  - testing
related:
  - value-meaning
sources: []
episodes:
  - boundary-value-without-reason
created: 2026-10-04
updated: 2026-10-04
---

# 具体的な値を見たら、その値が何を守っているのかを問う

仕様に 60人・30秒・99.9%・10MB のような値が現れたら、境界値として扱う前に「この値を超えると何が起きるか」を一度聞く。

答えられないとき、守るべきものがまだ特定できていない。

**効くとき:** 値の根拠が文書に書かれておらず、その値をもとに設計・テストを始めようとしているとき。

**外れるとき:** 値が規格・法令で外から与えられていて変更の余地がないとき（それでも「超えると何が起きるか」は有効なことが多い）。確認コストが得られる情報より大きいとき。

## 関連

- [値の意味を問う](../patterns/value-meaning.md)
- [上限値の根拠が誰にも分からなかった](../episodes/boundary-value-without-reason.md)
