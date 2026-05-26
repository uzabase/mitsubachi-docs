# icon-button

テキストを持たずアイコンのみで操作を表現するコンパクトなボタンコンポーネントです。スペースが限られた場所で、アイコンを通じて操作のエントリーポイントを提供します。

## いつ使うか

- 検索・閉じる・編集・削除など、アイコンの意味が広く共有されている操作を配置する場合
- スペースが限られており、テキストラベルを配置できない場所（ヘッダー・ツールバー・カード右上など）
- 他のUI要素と並べて配置する場合

## いつ使わないか

- アイコンだけでは意味が伝わりにくいアクション（ツールチップで補完できない場合はテキスト付きの [neutral-button](./neutral-button.md) を使う）
- ページ内でもっとも重要な主要アクション → [floating-button](./floating-button.md) の使用を検討する
- 1つのボタンから複数の操作を提供したい場合 → [menu-button](./menu-button.md)

## Figma

- コンポーネント: https://uzabase.github.io/mitsubachi-ui/?path=/story/button-mi-icon-button--basic
- 各variantの値は Figma MCP（`get_design_context`）で取得

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| variant | primary / secondary / tertiary / ghost | 外観スタイル |
| size | small / medium / large | サイズ |
| selected | true / false | 選択状態（secondary・tertiary・ghost のみ） |
| state | default / hover / active / focus / loading / disabled | インタラクション状態 |

## variant の使い分け

| variant | 使いどころ |
|---------|-----------|
| **primary** | 塗りつぶし背景で最も視覚的に目立つスタイル。ページ内で強調したい操作に使う |
| **secondary** | 強いボーダーを持ち、塗りつぶしのない輪郭スタイル |
| **tertiary** | 薄いボーダーを持つ、控えめなスタイル |
| **ghost** | ボーダーも背景もなく、最も目立たないスタイル。インタラクション時のみ背景が現れる |

## selected 状態

フィルタのオン/オフやトグル操作を伴う場面で使う。

| variant | selected 対応 |
|---------|:------------:|
| **secondary** | ✅ |
| **tertiary** | ✅ |
| **ghost** | ✅ |
| **primary** | — |

## コンテンツルール

- アイコンのみで構成する。テキストラベルは持たない
- 配置するアイコンは 1 つ
- アイコンの意味が視覚的に伝わりにくいため、必ずツールチップと組み合わせて使う
- loading 状態では、アイコンの代わりに loading コンポーネントが自動的に表示される
- `aria-label` を必ず付ける

## Do

- アイコンの意味が広く共有されている操作に限定して使う（検索・閉じる・編集など）
- 必ずツールチップと組み合わせて使う
- 必ず `aria-label` を付ける

## Don't

- アイコンだけでは意味が伝わりにくいアクションに使わない
- テキストラベルが必要な場面で icon-button を使わない → [neutral-button](./neutral-button.md) を使う
- `aria-label` を省略しない
