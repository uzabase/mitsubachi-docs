# input-chip

ユーザーが入力した内容を要素ごとに整理して表示するためのコンポーネントです。企業名やアカウント名など、選択・入力した値を個別のChipとして視覚的に表示し、削除ボタン(x)で個別に削除できます。

## いつ使うか

- text-field と組み合わせて、入力済みの値(企業名・アカウント名・タグなど)をChipとして表示したいとき
- ユーザーが入力した複数の値を一覧で確認し、個別に削除できるようにしたいとき

## いつ使わないか

- フィルター条件の選択・切り替えには、[filter-chip](./filter-chip.md) を使用する
- 削除操作を伴わない、読み取り専用のラベル表示には別の手段を検討する
- 複数の input-chip を並べて管理するときは、[input-chip-group](./input-chip-group.md) を使用する。input-chip 単体で使用するケースは限定的

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=10760-11028
- 各variantの値は Figma MCP(`get_design_context`)で取得

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-input-chip`（+ `__remove`） を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 |
|---|---|
| viewport | desktop / phone |
| state | default / hover / active / focus / disabled |

## コンテンツルール

- ラベルテキストは入力値をそのまま表示する
- ラベルテキストが長い場合、テキストは省略表示される
- 削除ボタンは常に表示する

## Do

- input-chip-group と組み合わせて使用する
- ラベルテキストは入力された値をそのまま表示する

## Don't

- フィルター条件の切り替えに使わない → [filter-chip](./filter-chip.md) を使う
- 削除操作が不要な読み取り専用のラベル表示に使わない
