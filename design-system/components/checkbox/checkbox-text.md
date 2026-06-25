# checkbox-text

checkbox-textは、[checkbox](./checkbox.md)（選択ボックス）と選択肢の内容を示したラベルテキストを組み合わせたコンポーネントです。ユーザーに「何を選択するのか」をラベルで明示しながら、選択操作を提供します。

## 使いどころと選び方

### 使うべきシーン
- 複数の選択肢にラベルが必要なすべてのケース。
- フォーム内で複数選択を受け付ける場面。

### 使わないほうがよいシーン
- 複数の選択肢から必ず1つだけを選ぶ場合は、[radio-button](../radio-button/index.md) を使います。

### 他コンポーネントとの違い・使い分け
- **[checkbox](./checkbox.md) との違い**：checkboxは選択ボックス単体のコンポーネントです。checkbox-textはラベルテキストとセットになっており、操作対象内にラベルも含まれます。
- **[radio-button](../radio-button/index.md) との違い**：checkbox-textは複数選択が可能です。radio-button-textは必ず1つだけの選択となります。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=178-267
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-checkbox` + `.mi-checkbox-label` を使う（自作しない）。

## 構成とルール

### バリエーション・状態

checkbox-textは以下のプロパティの組み合わせで状態が決まります。

#### checked（選択状態）
- `false`：未選択の状態。ボックスは空白で表示されます。
- `checked`：選択された状態。ボックス内にチェックマークが表示されます。
- `indeterminate`：一部選択の状態。ボックス内にインジケーター（横線）が表示されます。

#### state（インタラクション状態）
- `default`：通常の状態。
- `hover`：マウスカーソルが重なっている状態。
- `active`：クリック・タップ中の状態。
- `focus`：キーボードなどでフォーカスされている状態。フォーカスリングで視覚化します。
- `disabled`：操作不可の状態。ボックス・ラベルともにグレーアウトで表示されます。

### コンテンツルール
- ラベルテキストは簡潔に、操作内容が明確に伝わる表現にします。
- ラベルの文字列が折り返すほど長い内容は非推奨です。やむを得ない限り、ラベルは1行に収まる長さにします。
- 複数行になった場合、checkboxはテキストに対して上揃えで配置されます。

## 振る舞い
- ターゲットエリア：ラベルテキストを含むエリア全体が操作対象です。ラベルエリア内でのクリック・タップで状態が変化します。
- クリック・タップ：`false` ↔ `checked` の状態を切り替えます。`indeterminate` の状態からクリックすると `checked` になります。
- フォーカス・キーボード操作：`Tab` キーでフォーカスを移動し、`Space` キーで状態を切り替えます。

## Do

- ラベルテキストは簡潔に、操作内容が明確に伝わる表現にする
- ラベルは1行に収まる長さにする

## Don't

- 複数の選択肢から必ず1つだけを選ぶ場面で使わない → [radio-button](../radio-button/index.md) を使う
- ラベルの文字列を折り返すほど長くしない
