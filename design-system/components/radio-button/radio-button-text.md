# radio-button-text

radio-button-text は、ラジオボタン（radio-button：円形の選択インジケーター）とラベルテキストを組み合わせた、選択肢の1ユニットを表すコンポーネントです。

## 使いどころと選び方

### 使うべきシーン
- 複数の選択肢から1つだけを選ばせたい場面で、各選択肢をラベル付きで表示する場合に使います。
- 補足説明が不要で、短いラベルだけで選択肢の内容が十分に伝わる場合に適しています。
- 通常は [radio-button-text-group](./radio-button-text-group.md) の内部部品として配置します。

### 使わないほうがよいシーン
- 各選択肢に補足説明（サポートテキスト）を添えたい場合は、[radio-button-card](./radio-button-card.md) を使います。
- 同時に複数の選択肢を選べるようにしたい場合は、[checkbox-text](../checkbox/checkbox-text.md) 系のコンポーネントを使います。radio-button-text は必ず1つだけの選択になります。
- 複数の選択肢をまとめて1つの選択グループとして扱う場合は [radio-button-text-group](./radio-button-text-group.md) を、グループの見出しラベルとセットで使う場合は [radio-button-text-group-unit](./radio-button-text-group-unit.md) を使います。

### 他コンポーネントとの違い・使い分け
- **[radio-button-card](./radio-button-card.md) との違い**：radio-button-text はラベルのみを表示するシンプルな形式です。radio-button-card はカード型で、ラベルに加えてサポートテキスト（補足情報）も表示でき、各選択肢に詳しい説明が必要な場合に適しています。
- **[checkbox-text](../checkbox/checkbox-text.md) との違い**：checkbox-text は複数選択が可能です。radio-button-text は同一グループ内で常に1つだけが選ばれる排他的選択です。
- **[radio-button](./index.md) との違い**：radio-button は円形の選択インジケーターのみを表す内部部品です。radio-button-text はその radio-button にラベルテキストを組み合わせ、選択肢として直接扱える単位にしたものです。

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=10589-7726
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-radio`（ラベルは `.mi-radio-label`） を使う（自作しない）。

## 構成とルール

radio-button-text は、ラベルテキスト（text）と、2つの状態軸（selected / state）の組み合わせで表現されます。

### バリエーション・状態

| プロパティ | 値 |
|---|---|
| selected | `true` / `false` |
| state | `default` / `hover` / `active` / `focus` / `disabled` |

#### selected（選択状態）
- `false`：未選択。空白の円形で表示されます。
- `true`：選択済み。円形の内側に塗りつぶしのドットを表示します。

#### state（インタラクション状態）
- `default`：通常の状態。
- `hover`：マウスカーソルが重なっている状態。オーバーレイで視覚フィードバックを表示します。
- `active`：クリック・タップ中の状態。
- `focus`：フォーカスされている状態。フォーカスリングで視覚化します。
- `disabled`：操作不可の状態。グレーアウトで表示されます。

### コンテンツルール
- ラベル（text）は、選択肢の内容が明確に伝わる簡潔な表現にします。
- ラベル文字列の途中での折り返しは禁止します。水平方向（horizontal）に配置する場合は、radio-button-text 内でのラベルの折り返しは行いません。
- 垂直方向（vertical）に配置する場合は、radio-button-text 内でのラベルの折り返しは可能です。
- ラベルが複数行になる場合、ラジオボタンはラベルの上端にそろえて表示します（上揃え）。
- 折り返さないと表示できないほど長いラベルは非推奨です。ラベルの文言を簡潔に見直すか、サポートテキストを表示できる [radio-button-card](./radio-button-card.md) の使用を検討します。

## 振る舞い
- radio-button-text のターゲットエリア（操作の対象となる領域）は、ラベル文字列を含むエリア全体です。この領域内をクリック・タップすると選択状態に切り替わります。
- 同一グループ内の選択は排他的で、常に1つだけが選ばれます。他の選択肢を選ぶと、前の選択は自動的に解除されます。
- `hover` ではオーバーレイ、`active` ではクリック・タップ中のフィードバックを表示します。
- `focus` 状態ではフォーカスリングが表示されます。
- `disabled` 状態ではクリック・タップ操作を受け付けません。

## 役割と目的
- radio-button-text は、ラジオボタン（radio-button：円形の選択インジケーター）とラベルテキストを組み合わせた、選択肢の1ユニットを表すコンポーネントです。
- 複数の選択肢から1つだけを選ぶ場面で、選択肢の名称（ラベル）とともに現在の選択状態を明確に伝えます。
- 通常は [radio-button-text-group](./radio-button-text-group.md) の内部部品として配置され、グループ内での排他的な単一選択を構成します。
- 選択状態（selected）とインタラクション状態（state）に応じた視覚フィードバックを提供し、ユーザーに現在の選択を明確に伝えます。
