# Heuristics

探索するときに役立つ、短い判断則を置く場所です。

ヒューリスティックは**経験則であり、保証ではありません**。外れることがあります。外れた状況の報告も、同じくらい価値があります。

1ファイル1つ。本文は数行で構いません。「いつ効くか」「いつ外れるか」が1行ずつ添えてあると、読む人の判断が速くなります。

## 一覧

| ヒューリスティック | ファイル |
|---|---|
| 具体的な値を見たら、その値が何を守っているのかを問う | [ask-what-the-value-protects.md](ask-what-the-value-protects.md) |
| 「すべて」「必ず」と書かれていたら、例外を探す | [find-exceptions-behind-absolutes.md](find-exceptions-behind-absolutes.md) |
| 誰も答えられない質問は、要求ではなく未決定事項 | [unanswerable-means-undecided.md](unanswerable-means-undecided.md) |

## エピソード・パターンとの関係

同じヒューリスティックが何度も効いて、文脈と帰結まで言語化できるようになったら [`../patterns/`](../patterns/) に昇格させる候補になります。逆に、パターンに反例が集まって適用範囲が狭まった場合、ヒューリスティックに戻すこともあります。

まだ言語化できていない段階のものは [`../episodes/`](../episodes/) へ。

[`_TEMPLATE.md`](_TEMPLATE.md) をコピーして使ってください。
