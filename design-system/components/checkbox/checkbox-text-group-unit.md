# checkbox-text-group-unit

checkbox-text-group-unitは、[label-unit](../label-unit.md)（ラベル・必須表示・補足テキストを持つラベル用コンポーネント）と [checkbox-text-group](./checkbox-text-group.md) を組み合わせた、フォーム用の複数選択コンポーネントです。「何を入力・選択するのか」をラベルで明示しながら、複数のcheckbox-textを一つの入力グループとして提供します。

## 使いどころと選び方

### 使うべきシーン
- フォーム内で複数選択の入力グループを表示する場合。
- 選択肢のグループに対してラベルや必須表示が必要な場合。

### 使わないほうがよいシーン
- ラベルや必須表示が不要な場合は、[checkbox-text-group](./checkbox-text-group.md) を直接使います。

### 他コンポーネントとの違い・使い分け
- **checkbox-text-groupとの違い**：checkbox-text-group-unitは [label-unit](../label-unit.md) を含むセットです。ラベルや必須・補足テキストが不要な場合は [checkbox-text-group](./checkbox-text-group.md) を使います。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5276-5517
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-choice-group-unit` を使う（自作しない）。

## 構成とルール

### バリエーション・状態

#### direction（配置方向）
- `horizontal`：水平方向に選択肢を並べます。
- `vertical`：垂直方向に選択肢を並べます。

#### 構成要素

| 要素 | 説明 |
|---|---|
| [label-unit](../label-unit.md) | 入力グループのラベルを表示します。必要に応じて「必須」ラベルや補足テキストを組み合わせられます。入力内容が必須項目である場合は必須ラベルを表示します。 |
| [checkbox-text-group](./checkbox-text-group.md) | 選択肢のcheckbox-textの表示層です。directionに応じて水平または垂直に配置されます。 |

### コンテンツルール
- ラベルのテキストは、入力内容の意味が簡潔に伝わる表現にします。
- 必須項目には「必須」ラベルを必ず表示します。
- 補足テキストは必要な場合のみ表示し、入力内容の説明や制約を必要最小限にします。

## 振る舞い
- 各 [checkbox-text](./checkbox-text.md) はそれぞれ独立してクリック・タップに反応します。
- [label-unit](../label-unit.md) は操作対象外であり、[checkbox-text-group](./checkbox-text-group.md) の内容表示のみを担います。

## Do

- ラベルのテキストは入力内容の意味が簡潔に伝わる表現にする
- 必須項目には「必須」ラベルを必ず表示する
- 補足テキストは必要な場合のみ表示する

## Don't

- ラベルや必須表示が不要な場合にcheckbox-text-group-unitを使わない → [checkbox-text-group](./checkbox-text-group.md) を使う
