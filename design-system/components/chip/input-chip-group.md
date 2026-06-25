# input-chip-group

複数の [input-chip](./input-chip.md) をまとめて管理・表示するコンテナコンポーネントです。入力フィールドと連携しながら、値の追加・削除などの一連の入力体験を一体として提供します。

## 使いどころと選び方

### 使うべきシーン
- ユーザーが入力した複数の値(企業名・アカウント名など)を一列のChipとして表示したいとき
- Chipの追加・削除が発生する、動的な入力エリアを構成するとき

### 使わないほうがよいシーン
- 入力された値が常に1つのみの場合は、[input-chip](./input-chip.md) 単体で十分
- フィルター選択には [filter-chip-group-single](./filter-chip-group-single.md) / [filter-chip-group-multiple](./filter-chip-group-multiple.md) を使用する

### 他コンポーネントとの違い・使い分け
- **filter-chip-group との違い**：filter-chip-group はあらかじめ定義された選択肢のオン／オフが目的です。input-chip-group はユーザーが入力した値を管理するためのコンテナです。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5815-12881
- 各variantの値は Figma MCP(`get_design_context`)で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-input-chip-group` を使う（自作しない）。

## 構成とルール

input-chip-group は内部に複数の [input-chip](./input-chip.md) を含むスロットで構成されます。

### バリエーション・状態

#### viewport
- `desktop`：デスクトップ向けのサイズです。
- `phone`：スマートフォン向けのサイズです（各Chipのタップターゲットが大きくなります）。

### コンテンツルール
- 内包する [input-chip](./input-chip.md) の数に制限はない
- Chipが複数行にわたる場合、自動的に折り返して表示される

## 振る舞い
- **Chipの追加**：入力フィールドで値が確定されると、新しい input-chip が input-chip-group 内に追加されます。
- **Chipの削除**：各Chipの削除ボタン（×）をクリック／タップすると、対象の input-chip が削除されます。
- **折り返し**：Chipの総幅がコンテナの幅を超える場合、次の行に自動的に折り返して表示されます。
- **フォーカス・キーボード操作**：Tab キーで各Chipの削除ボタンにフォーカスを順に移動できます。

## Do

- 複数の input-chip を並べる場合は input-chip-group で囲む
- 入力フィールドと組み合わせて使用する

## Don't

- フィルター選択の管理に使わない → filter-chip-group を使う
- 値が常に1つのみの場合に不要なグループ化をしない
