# filter-chip

フィルター条件を選択・切り替えるためのChipコンポーネントです。選択された状態を視覚的に示すことで、ユーザーが現在の絞り込み条件を把握しやすくします。

## 使いどころと選び方

### 使うべきシーン
- 一覧や検索結果をカテゴリや属性で絞り込むとき
- ユーザーがどの条件で絞り込んでいるかを視覚的に示したいとき
- オン/オフのトグル操作で複数の選択肢を切り替えるとき

### 使わないほうがよいシーン
- 選択肢がフォームの入力値として送信される場合（チェックボックスやラジオボタンを使用する）
- 選択肢の数が非常に多くスクロールが必要になる場合（ドロップダウン等を検討する）
- ページやセクションを切り替えるナビゲーションには tab を使用する
- filter-chip を単体で使用せず、グループとして使用する場合は [filter-chip-group-single](./filter-chip-group-single.md) / [filter-chip-group-multiple](./filter-chip-group-multiple.md) を使用する

### 他コンポーネントとの違い・使い分け
- **[checkbox](../checkbox/index.md) や radio-button**：フォームの入力として選択肢を提示する場合はこれらを使用します。filter-chipはフォーム入力ではなく、表示内容を即時絞り込む操作に使用します。
- **tab**：ページやセクションを切り替えるナビゲーションに使用します。filter-chipは表示内容の絞り込みに使用します。
- **filter-chip-group-single / filter-chip-group-multiple**：filter-chipを単体で使用する場合は、選択状態の管理を実装側で担う必要があります。グループとして使用する場合はこれらのグループコンポーネントを使用します。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=10771-20108
- 各variantの値は Figma MCP(`get_design_context`)で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-chip` を使う（自作しない）。

## 構成とルール

### バリエーション・状態

filter-chipは以下のバリアントを持ちます。

#### viewport
- `desktop`：デスクトップ向けのサイズで表示します。
- `phone`：スマートフォン向けのサイズで表示します。

#### selected
- `false`（未選択）：薄いグレーの背景で表示されます。
- `true`（選択済み）：薄い青紫の背景に変わり、先頭にチェックアイコンが表示されます。

#### state
- `default`：通常の表示状態です。
- `hover`：ポインターがコンポーネント上にある状態です。
- `active`：クリック/タップ中の状態です。
- `focus`：キーボード操作などでフォーカスが当たっている状態です。フォーカスリングが表示されます。
- `disabled`：操作不能な状態です。テキストが薄い色で表示されます。

### コンテンツルール
- ラベルテキストは短く、ひと目で絞り込み条件が分かる表現にする
- テキストのみで構成される。アイコンは `selected=true` のときにチェックアイコンが自動的に表示される。任意のアイコンを追加することはできない

## 振る舞い
- クリック/タップするたびに `selected` の状態（true/false）がトグルします。
- `selected=true` になると先頭にチェックアイコン（icon/check-small）が表示され、背景色が変わります。
- `disabled` 状態ではクリック/タップを受け付けません。
- フォーカス時はフォーカスリングが表示されます。

## Do

- ラベルは短く、絞り込み条件がひと目で分かる表現にする
- グループコンポーネント([filter-chip-group-single](./filter-chip-group-single.md) / [filter-chip-group-multiple](./filter-chip-group-multiple.md))と組み合わせて使用する

## Don't

- フォーム入力の選択肢として使わない(チェックボックスやラジオボタンを使う)
- ユーザーが入力した値の表示には使わない → [input-chip](./input-chip.md) を使う
- ナビゲーションの切り替えには使わない → tab を使う

## 役割と目的

- フィルター条件を選択・切り替えるための Chip（チップ：小さなタグ状のUI部品）コンポーネントです。選択された状態を視覚的に示すことで、ユーザーが現在の絞り込み条件を把握しやすくします。
- 複数の選択肢から1つのみ選択（[filter-chip-group-single](./filter-chip-group-single.md)）と複数選択（[filter-chip-group-multiple](./filter-chip-group-multiple.md)）のどちらのシーンでも使用できます。
