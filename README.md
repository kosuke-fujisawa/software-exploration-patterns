# Software Exploration Patterns

ソフトウェア開発で、未知・ズレ・リスクに気づき、理解を更新するための「探索知」を集めるオープンな知識ベースです。

要求工学 / ソフトウェアテスト / QA / アジャイル / Product Management / UX・UX Research / ソフトウェア設計 / Safety・Reliability Engineering に散らばっている「気づき方」の知識を、特定の方法論の所有物にせず、横断的に整理します。

**サイト: <https://kosuke-fujisawa.github.io/software-exploration-patterns/>**

community-maintained open knowledge base / contributions welcome

---

## 何を集めているか

「正しい開発のやり方」でも「テスト技法集」でもありません。**何かがおかしいと気づく / 前提を疑う / 不明点を見つける / 誰かに聞く / 現場を見る / リスクを見つける / そのリスクを要求・設計・実装・テスト・運用のどこで扱うか考える** —— そうした*気づき方*の知識です。

| 種類 | 内容 | 場所 |
|---|---|---|
| **Episodes** | 実際に起きた出来事や経験。整理されていなくてよい | [episodes/](episodes/) |
| **Heuristics** | 探索するときに役立つ短い判断則 | [heuristics/](heuristics/) |
| **Patterns** | 複数の経験で再利用できる程度まで整理された探索パターン | [patterns/](patterns/) |
| **Sources** | 既存研究・書籍・論文・記事・方法論 | [sources/](sources/) |

この4つは上下関係ではなく、探索知を異なる粒度で残すための分類です。一方向に昇格していく階段ではありません。

現在のパターン（いずれも**初期サンプルであり、検証されていません**）:

- [値の意味を問う](patterns/value-meaning.md)
- [失敗状態から戻る](patterns/start-from-failure-state.md)
- [知っている人に聞く](patterns/ask-the-expert.md)
- [現場を見る](patterns/observe-the-field.md)
- [リスクを設計へ返す](patterns/return-risk-to-design.md)

> **この知識ベースはまだ初期段階です。** 掲載内容は継続的に検証・修正・統合されます。体系として完成しているわけでも、標準でもありません。

## 参加する

完成したパターンを書く必要はありません。

- 実際に起きた**エピソードだけ**（「こういう状況で、こう気づいた」で十分です）
- 「**このパターンは自分の状況では使えなかった**」という反例
- 「**この話は既存研究にある**」という出典だけの共有
- 分類が合っていない、重複している、という指摘

GitHub の操作に慣れていなくても [Issue のフォーム](https://github.com/kosuke-fujisawa/software-exploration-patterns/issues/new/choose)から送れます。慣れている人は Pull Request でどうぞ。

> **実務事例を投稿する場合は、公開できない情報（顧客名・会社名・個人情報・非公開仕様・内部URL・認証情報・案件固有の詳細）を除去し、一般化してください。**

詳しくは [CONTRIBUTING.md](CONTRIBUTING.md) を読んでください。

## 詳しく知りたい人へ

- [このプロジェクトについて](docs/about.md) — なぜ作るのか、何を大切にしているか
- [GOVERNANCE.md](GOVERNANCE.md) — 共同知識基盤としての運営方針。Maintainer 不在でも Fork で継続できます
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — 行動規範
- [LLM から使う](docs/llm.md) — `catalog.json` / `llms.txt` など機械可読な出力
- [サイトとビルドの構成](docs/architecture.md) — 技術選定、ローカルでの読み方、ADR
- [front matter の書き方](docs/metadata.md)
- [ROADMAP](docs/roadmap.md)

## ライセンス

コンテンツおよびスクリプトは [CC0 1.0 Universal](LICENSE)（パブリックドメイン提供）です。誰でも、許諾や表示なしに、自由に利用・改変・再配布・Fork できます。

ただし **ライセンス上の帰属義務がないことと、出典を書かないことは別です。** このプロジェクトでは、知識がどこから来たのかを追跡できることを大切にしています。また CC0 は第三者の著作物には及びません。他者の文章をそのまま転載しないでください（[CONTRIBUTING.md](CONTRIBUTING.md) 参照）。

比較検討の経緯は [ADR 0003](docs/adr/0003-license-cc0.md) にあります。
