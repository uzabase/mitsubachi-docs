# filter-chip-group-single

複数の選択肢から常にいずれか1つの条件のみを選択できる filter-chip のグループコンポーネントです。選択を切り替えると前の選択は自動的に解除され、ラジオボタンのように1つの条件に絞った絞り込みを実現します。

## いつ使うか

- 「すべて」「タイプA」「タイプB」など、排他的な選択肢から1つだけ絞り込むとき
- 常にいずれかの条件が選択されていることを保証したいとき

## いつ使わないか

- 複数の条件を同時に選択したい場合 → [filter-chip-group-multiple](./filter-chip-group-multiple.md) を使用する
- 選択肢が1つしかない場合
- ページやセクションを切り替えるナビゲーションには tab を使用する

## Figma

- コンポーネント: https://uzabase.github.io/mitsubachi-ui-react/?path=/story/components-chip-filterchipsingleselectgroup--default
- 各variantの値は Figma MCP(`get_design_context`)で取得

## バリアントプロパティ

| プロパティ | 値 |
|---|---|
| viewport | desktop / phone |
| size | medium |

## コンテンツルール

- [filter-chip](./filter-chip.md) を子要素(slot)として受け取る
- 子要素の [filter-chip](./filter-chip.md) は横並び(折り返しあり)に配置される

## Do

- 排他的な選択肢(1つだけ選択可能)の絞り込みに使用する
- 常にいずれか1つが選択された状態を維持する

## Don't

- 複数の条件を同時に選択したい場合に使わない → [filter-chip-group-multiple](./filter-chip-group-multiple.md) を使う
- ナビゲーションの切り替えに使わない → tab を使う
