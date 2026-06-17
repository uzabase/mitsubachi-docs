# filter-chip

フィルター条件を選択・切り替えるためのChipコンポーネントです。選択された状態を視覚的に示すことで、ユーザーが現在の絞り込み条件を把握しやすくします。

## いつ使うか

- 一覧や検索結果をカテゴリや属性で絞り込むとき
- ユーザーがどの条件で絞り込んでいるかを視覚的に示したいとき
- オン/オフのトグル操作で複数の選択肢を切り替えるとき

## いつ使わないか

- 選択肢がフォームの入力値として送信される場合(チェックボックスやラジオボタンを使用する)
- 選択肢の数が非常に多くスクロールが必要になる場合(ドロップダウン等を検討する)
- ページやセクションを切り替えるナビゲーションには tab を使用する
- filter-chip を単体で使用せず、グループとして使用する場合は [filter-chip-group-single](./filter-chip-group-single.md) / [filter-chip-group-multiple](./filter-chip-group-multiple.md) を使用する

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=10771-20108
- 各variantの値は Figma MCP(`get_design_context`)で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-chip` を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 |
|---|---|
| viewport | desktop / phone |
| selected | true / false |
| state | default / hover / active / focus / disabled |

## variant の使い分け

### selected

| 値 | 表示 |
|---|---|
| **false**(未選択) | 薄いグレーの背景 |
| **true**(選択済み) | 薄い青紫の背景、先頭にチェックアイコン表示 |

## コンテンツルール

- ラベルテキストは短く、ひと目で絞り込み条件が分かる表現にする
- テキストのみで構成される。アイコンは `selected=true` のときにチェックアイコンが自動的に表示される。任意のアイコンを追加することはできない

## Do

- ラベルは短く、絞り込み条件がひと目で分かる表現にする
- グループコンポーネント([filter-chip-group-single](./filter-chip-group-single.md) / [filter-chip-group-multiple](./filter-chip-group-multiple.md))と組み合わせて使用する

## Don't

- フォーム入力の選択肢として使わない(チェックボックスやラジオボタンを使う)
- ユーザーが入力した値の表示には使わない → [input-chip](./input-chip.md) を使う
- ナビゲーションの切り替えには使わない → tab を使う
