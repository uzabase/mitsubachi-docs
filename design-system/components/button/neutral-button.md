# neutral-button

プロダクト内で最も標準的に使用する基本のボタンコンポーネントです。画面内の主要なアクションや一般的な操作に使用します。

## いつ使うか

- 送信・保存・確認など、通常の実行操作をユーザーに促す場合
- danger-button や ai-button では意味づけが強すぎる、汎用的なアクションに使用する場合
- 複数のアクションを並置する場合（primary・secondary など variant で重要度を区別）
- ページ内でフォームや設定変更の完了ボタンとして配置する場合

## いつ使わないか

- 削除・リセットなど取り消しが困難な破壊的操作 → [danger-button](./danger-button.md)
- AIによる生成・提案を実行する操作 → [ai-button](./ai-button.md)
- テキストを持たずアイコンのみで操作を表現したい場合 → [icon-button](./icon-button.md)
- 画面に常時浮かんで表示する主要アクション → [floating-button](./floating-button.md)
- 1つのボタンから複数の操作を提供したい場合 → [menu-button](./menu-button.md)

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=178-3446
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-button--primary/--secondary/--tertiary/--ghost/--plane` を使う（自作しない）。処理中（loading）を示す場合は全 variant 共通で `.mi-button--loading` を付け、中に `<span class="mi-loading">` を置く。選択状態は variant クラスに `.mi-button--selected` を**併用**する（`--secondary/--tertiary/--ghost` のみ。primary / plane に selected は無く、`--selected` 単独では効かない）。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| variant | primary / secondary / tertiary / ghost / plane | 重要度・強調度 |
| size | medium / large / x-large | サイズ |
| selected | true / false | 選択状態 |
| state | default / hover / active / focus / loading / disabled | インタラクション状態 |

## variant の使い分け

| variant | 使いどころ |
|---------|-----------|
| **primary** | そのページで最も重要なアクション。1画面に1つが原則 |
| **secondary** | primary の次に重要なアクション。キャンセル・戻るなど |
| **tertiary** | 補助的なアクションや重要度の低い操作 |
| **ghost** | 背景に馴染む控えめなスタイル |
| **plane** | 最も視覚的な存在感を抑えたスタイル。ツールバーなどコンパクトな UI に |

## selected 状態

トグル・タブ・フィルターなど ON/OFF を示す場面で使う。

| variant | selected 対応 |
|---------|:------------:|
| **secondary** | ✅ |
| **tertiary** | ✅ |
| **ghost** | ✅ |
| **primary** | — |
| **plane** | — |

## コンテンツルール

- テキストラベルは必須。ボタンの目的を端的に表す動詞句で記述する（例：「保存する」「送信する」）
- アイコンはオプション。テキストラベルと組み合わせて使用する。アイコンのみの構成にはできない（→ [icon-button](./icon-button.md)）
- テキストラベルは簡潔に保つ。長い文章はラベルとして使用しない

## Do

- ラベルは「保存する」「送信する」のような短い動詞句にする
- 複数ボタンを並べるときは variant で重要度を区別する
- primary は 1 画面に 1 つだけ使う
- primary を右、secondary を左に配置する
- ボタン間隔は 8px

## Don't

- primary ボタンを 1 画面に複数配置しない
- 破壊的操作に neutral-button を使わない → [danger-button](./danger-button.md) を使う
- ラベルを長文にしない — 説明が必要な場合はボタンの外に書く
- ラベルを曖昧にしない —「OK」「実行」ではなく「保存」「削除」など結果を予測できるラベルを付ける
- 配置を画面ごとに変えない — 主要アクションは右、キャンセルは左
- アイコンのみの構成にしない（→ [icon-button](./icon-button.md)）
