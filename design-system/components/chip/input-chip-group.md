# input-chip-group

複数の [input-chip](./input-chip.md) をまとめて管理・表示するコンテナコンポーネントです。入力フィールドと連携しながら、値の追加・削除などの一連の入力体験を一体として提供します。

## いつ使うか

- ユーザーが入力した複数の値(企業名・アカウント名など)を一列のChipとして表示したいとき
- Chipの追加・削除が発生する、動的な入力エリアを構成するとき

## いつ使わないか

- 入力された値が常に1つのみの場合は、[input-chip](./input-chip.md) 単体で十分
- フィルター選択には [filter-chip-group-single](./filter-chip-group-single.md) / [filter-chip-group-multiple](./filter-chip-group-multiple.md) を使用する

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5815-12881
- 各variantの値は Figma MCP(`get_design_context`)で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-input-chip-group` を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 |
|---|---|
| viewport | desktop / phone |

## コンテンツルール

- 内包する [input-chip](./input-chip.md) の数に制限はない
- Chipが複数行にわたる場合、自動的に折り返して表示される

## Do

- 複数の input-chip を並べる場合は input-chip-group で囲む
- 入力フィールドと組み合わせて使用する

## Don't

- フィルター選択の管理に使わない → filter-chip-group を使う
- 値が常に1つのみの場合に不要なグループ化をしない
