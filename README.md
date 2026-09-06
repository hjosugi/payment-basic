# payment-basic

決済システムのレジリエンスを、TypeScript・Go・Javaの実装と障害実験で学ぶ教材です。日本語の解説と、Google SWE system design面接向けの短い英語スクリプトを含みます。

## リポジトリ構成

| リポジトリ名 | 内容 |
| --- | --- |
| `hjosugi/payment-basic` | この学習ガイド、共通設計、作成・push手順 |
| `hjosugi/payment-basic-ts` | Node.js 24 / TypeScript / node:sqlite |
| `hjosugi/payment-basic-go` | Go / net/http / database/sql / modernc.org/sqlite |
| `hjosugi/payment-basic-java` | Java 21 / virtual threads / HttpClient / SQLite JDBC |

配布時点ではGitHubへの作成・pushは未実施です。各ディレクトリを独立リポジトリとして作成できる状態にしてあります。実装リポジトリは他のリポジトリへの依存なしで起動・テストできます。

## 読む順番

1. [10原則の日本語解説](docs/guide-ja.md)
2. [言語別の実装対応](docs/implementation-ja.md)
3. [ハンズオン](docs/lab-ja.md)
4. [英語面接スクリプト](docs/interview-en.md)
5. [障害対応runbook](docs/runbook-ja.md)
6. [検証結果](docs/verification.md)

特に重要なのは、timeoutを決済失敗と断定しないこと、同じ操作には同じキーを使うこと、DBの一意制約とProviderの冪等性を組み合わせることです。

## 実装済み

- 原子的な冪等性予約、payload違いの409、加盟店ごとのキー範囲。
- PENDING/UNKNOWN/SUCCEEDED/DECLINEDの永続化。
- 成功状態と2行の台帳を同じDBトランザクションで保存。
- 本文を含むProvider timeout、Circuit Breaker、同時実行制限。
- 未確定操作の復旧、再起動後の回復、金額・通貨の検証。
- 明細CSV照合と差分のDB保存。
- Prometheus形式のmetrics、JSONログ、アラート設定例。
- 故障注入、負荷計測、incident・retrospectiveテンプレート。

Pythonは共通テスト・模擬Provider・運用スクリプト専用です。決済API本体はそれぞれTypeScript・Go・Javaで実装しています。

## GitHubへ分けて作成する

GitとGitHub CLIを準備し、`gh auth login`で自分の環境で認証してください。トークンをファイルや会話に貼り付ける必要はありません。

ZIPを展開し、4ディレクトリが並んでいる位置で:

```bash
python3 payment-basic/scripts/publish.py
```

まず作成予定コマンドだけを表示します。作成・pushする場合:

```bash
python3 payment-basic/scripts/publish.py --owner hjosugi --visibility private --execute
```

公開する場合は`--visibility public`へ変更します。既存リポジトリがあれば停止し、上書きしません。ネットワークエラーや権限不足でも`gh repo create`が失敗した時点で停止します。4件の作成は単一トランザクションではないため、途中で失敗した場合は作成済みのリポジトリを確認して残りを個別に扱ってください。スクリプトはそれらを削除しません。

公式: [gh repo create](https://cli.github.com/manual/gh_repo_create)

## 元記事との違い

Shopify原文は2022年の記事です。転載文のタイムアウト記述を訂正し、容量計算の前提とULIDが必須でない点を補足しました。[Shopify原文](https://shopify.engineering/building-resilient-payment-systems)

この教材はローカルの模擬決済です。実際のカード、銀行送金、認証、Webhook、決済会社の本番連携は含みません。これらの拡張方針は日本語解説と英語スクリプトに記載しています。
