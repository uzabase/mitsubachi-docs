# checkbox

checkboxは、ひとつの項目に対して選択・解除を行うためのコンポーネントです。ユーザーが複数の選択肢から0個以上の項目を選べるようにします。

## 使いどころと選び方

### 使うべきシーン
- ユーザーが複数の選択肢から0個以上を選択できるフォームやリスト。
- 設定のオン・オフを切り替えるインターフェース（送信ボタンで確定するフォーム内）。
- 親子関係のある選択肢において、親checkboxが子の選択状態をまとめて制御する場合（indeterminate状態を活用）。

### 使わないほうがよいシーン
- 複数の選択肢から必ず1つだけを選ぶ場合は、[radio-button](../radio-button/index.md) を使います。
- 操作と同時に即座にアクションが発生する場合は、[switch](../switch.md) を使います（送信ボタンで確定するフォームにはcheckboxを使います）。

### 他コンポーネントとの違い・使い分け
- **[radio-button](../radio-button/index.md) との違い**：checkboxは複数選択が可能ですが、radio-buttonは選択肢の中から必ず1つだけを選びます。選択可能な数で使い分けます。
- **[switch](../switch.md) との違い**：switchは操作と同時に即座に状態が変化します。checkboxはフォーム送信などの確定操作が伴う場面に使います。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=178-197
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-checkbox` + `.mi-checkbox-label` を使う（自作しない）。

## 構成とルール

### バリエーション・状態

checkboxは以下のプロパティの組み合わせで状態が決まります。

#### checked（選択状態）
- `false`：未選択の状態。ボックスは空白で表示されます。
- `checked`：選択された状態。ボックス内にチェックマークが表示されます。
- `indeterminate`：一部選択の状態。ボックス内にインジケーター（横線）が表示されます。子要素の一部が選択されている親checkboxなどで使用します。

#### state（インタラクション状態）
- `default`：通常の状態。
- `hover`：マウスカーソルが重なっている状態。背景色でホバーを視覚化します。
- `active`：クリック・タップ中の状態。背景色でアクティブ状態を視覚化します。
- `focus`：キーボードなどでフォーカスされている状態。フォーカスリングで視覚化します。
- `disabled`：操作不可の状態。グレーアウトで表示され、操作を受け付けません。

### コンテンツルール
- checkboxは選択ボックス単体のコンポーネントです。ラベルなしで使用する場合は、スクリーンリーダー向けに別途アクセシブルなラベルを設定します。
- ラベルを伴う場合は [checkbox-text](./checkbox-text.md) を使います。

## 振る舞い
- クリック・タップ：`false` ↔ `checked` の状態を切り替えます。`indeterminate` の状態からクリックすると `checked` になります。
- キーボード操作：フォーカスを当てた状態で `Space` キーを押すと、状態を切り替えます。
- disabled状態のとき：クリック・タップおよびキーボード操作を受け付けません。

## Do

- 複数選択が可能な場面で使う
- 親子関係のある選択肢ではindeterminate状態を活用する
- ラベルなしで使用する場合はアクセシブルなラベルを別途設定する

## Don't

- 複数の選択肢から必ず1つだけを選ぶ場面で使わない → [radio-button](../radio-button/index.md) を使う
- 操作と同時に即座にアクションが発生する場面で使わない → [switch](../switch.md) を使う
